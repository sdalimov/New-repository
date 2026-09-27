"""Сценарий тренировки: старт → реплики → завершение → разбор."""

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from app.ai.budget import BudgetStatus, budget_status, record_usage
from app.ai.client import LLM, LLMError
from app.config import Settings
from app.content import LANGUAGES, Content, Persona
from app.db.models import SessionReview, TrainingMessage, TrainingSession, User
from app.trainer.prompts import parse_markers, persona_system_prompt, review_prompts
from app.trainer.scoring import FinalReview, ReviewDraft, finalize_review

DIALOG_MAX_TOKENS = 2000
REVIEW_MAX_TOKENS = 8000
ENDED = ("finished", "hung_up", "agreed")


class TrainerError(Exception):
    """Ошибка сценария, текст показывается пользователю."""


class BudgetExceeded(TrainerError):
    pass


@dataclass
class StartResult:
    session_id: int
    persona: Persona
    budget: BudgetStatus


@dataclass
class TurnResult:
    persona_text: str
    outcome: str | None = None  # hung_up | agreed | max_turns
    review: FinalReview | None = None


@dataclass
class HistoryItem:
    session: TrainingSession
    persona_title: str
    review: SessionReview | None


class TrainerService:
    def __init__(self, sessionmaker: async_sessionmaker, llm: LLM, content: Content, settings: Settings):
        self.sm = sessionmaker
        self.llm = llm
        self.content = content
        self.settings = settings

    # ---------- helpers ----------

    async def _user(self, db: AsyncSession, tg_id: int) -> User:
        user = await db.scalar(select(User).where(User.tg_id == tg_id))
        if user is None:
            user = User(tg_id=tg_id, tz=self.settings.timezone)
            db.add(user)
            await db.flush()
        return user

    async def _active(self, db: AsyncSession, user_id: int) -> TrainingSession | None:
        return await db.scalar(
            select(TrainingSession)
            .where(TrainingSession.user_id == user_id, TrainingSession.status == "active")
            .options(selectinload(TrainingSession.messages))
            .order_by(TrainingSession.id.desc())
        )

    async def _budget(self, db: AsyncSession) -> BudgetStatus:
        s = self.settings
        return await budget_status(db, s.ai_monthly_budget_usd, s.ai_budget_warn_ratio, s.timezone)

    def persona(self, key: str) -> Persona:
        try:
            return self.content.personas[key]
        except KeyError:
            raise TrainerError(f"Нет персонажа «{key}»") from None

    # ---------- public API ----------

    async def budget(self) -> BudgetStatus:
        async with self.sm() as db:
            return await self._budget(db)

    async def has_active(self, tg_id: int) -> bool:
        async with self.sm() as db:
            user = await self._user(db, tg_id)
            await db.commit()
            return await self._active(db, user.id) is not None

    async def start(self, tg_id: int, persona_key: str, language: str, difficulty: int) -> StartResult:
        persona = self.persona(persona_key)
        if language not in LANGUAGES:
            raise TrainerError(f"Неизвестный язык «{language}»")
        if difficulty not in (1, 2, 3):
            raise TrainerError("Уровень сложности: 1, 2 или 3")

        async with self.sm() as db:
            budget = await self._budget(db)
            if budget.exceeded:
                raise BudgetExceeded(
                    f"Месячный лимит ИИ исчерпан: ${budget.spent:.2f} из ${budget.limit:.2f}. "
                    "Новые сессии — с 1-го числа (или увеличьте AI_MONTHLY_BUDGET_USD)."
                )
            user = await self._user(db, tg_id)
            old = await self._active(db, user.id)
            if old is not None:
                old.status = "abandoned"
                old.ended_at = datetime.now(timezone.utc)
            session = TrainingSession(
                user_id=user.id, persona_key=persona.key, language=language, difficulty=difficulty
            )
            db.add(session)
            await db.commit()
            return StartResult(session_id=session.id, persona=persona, budget=budget)

    async def reply(self, tg_id: int, text: str) -> TurnResult:
        text = text.strip()
        if not text:
            raise TrainerError("Пустое сообщение")

        async with self.sm() as db:
            user = await self._user(db, tg_id)
            session = await self._active(db, user.id)
            if session is None:
                raise TrainerError("Нет активной тренировки. Начните: /train")

            persona = self.persona(session.persona_key)
            history = [
                {"role": "user" if m.role == "seller" else "assistant", "content": m.content}
                for m in session.messages
            ]
            history.append({"role": "user", "content": text})

            result = await self.llm.chat(
                model=self.settings.claude_model_dialog,
                system=persona_system_prompt(self.content, persona, session.language, session.difficulty),
                messages=history,
                effort=self.settings.claude_effort_dialog,
                max_tokens=DIALOG_MAX_TOKENS,
            )
            await record_usage(db, "dialog", result.usage)
            if result.refused or not result.text:
                await db.commit()
                raise TrainerError("Персонаж не смог ответить. Перефразируйте реплику.")

            persona_text, outcome = parse_markers(result.text)
            session.messages.append(TrainingMessage(role="seller", content=text))
            session.messages.append(TrainingMessage(role="persona", content=persona_text))
            session.turns += 1

            if outcome is None and session.turns >= self.settings.max_turns:
                outcome = "max_turns"
            if outcome is not None:
                session.status = "finished" if outcome == "max_turns" else outcome
                session.ended_at = datetime.now(timezone.utc)
            await db.commit()

            if outcome is None:
                return TurnResult(persona_text=persona_text)
            review = await self._review(db, session, outcome)
            return TurnResult(persona_text=persona_text, outcome=outcome, review=review)

    async def end(self, tg_id: int) -> FinalReview:
        """Завершить активную сессию (или повторить разбор последней, если он не удался)."""
        async with self.sm() as db:
            user = await self._user(db, tg_id)
            session = await self._active(db, user.id)
            if session is not None:
                outcome = "finished"
            else:
                session = await db.scalar(
                    select(TrainingSession)
                    .where(TrainingSession.user_id == user.id)
                    .options(
                        selectinload(TrainingSession.messages),
                        selectinload(TrainingSession.review),
                    )
                    .order_by(TrainingSession.id.desc())
                )
                if session is None or session.status not in ENDED or session.review is not None:
                    raise TrainerError("Нет активной тренировки. Начните: /train")
                outcome = session.status

            if not any(m.role == "seller" for m in session.messages):
                session.status = "abandoned"
                session.ended_at = datetime.now(timezone.utc)
                await db.commit()
                raise TrainerError("Вы не сказали ни одной реплики — разбирать нечего. Сессия закрыта.")

            if session.status == "active":
                session.status = "finished"
                session.ended_at = datetime.now(timezone.utc)
                await db.commit()
            return await self._review(db, session, outcome)

    async def _review(self, db: AsyncSession, session: TrainingSession, outcome: str) -> FinalReview:
        persona = self.persona(session.persona_key)
        transcript = [(m.role, m.content) for m in session.messages]
        system, prompt = review_prompts(
            self.content, persona, session.language, session.difficulty, outcome, transcript
        )
        try:
            result = await self.llm.structured(
                model=self.settings.claude_model_review,
                system=system,
                prompt=prompt,
                schema=ReviewDraft,
                effort=self.settings.claude_effort_review,
                max_tokens=REVIEW_MAX_TOKENS,
            )
        except LLMError as e:
            raise TrainerError(f"{e} Разбор можно повторить командой /end.") from e
        await record_usage(db, "review", result.usage)
        if result.refused or result.data is None:
            await db.commit()
            raise TrainerError("Модель-тренер не смогла сделать разбор. Повторите: /end")

        seller = [m.content for m in session.messages if m.role == "seller"]
        review = finalize_review(result.data, self.content.rubric, seller)
        db.add(
            SessionReview(
                session_id=session.id,
                score_needs=review.scores["needs"],
                score_value=review.scores["value"],
                score_objections=review.scores["objections"],
                score_close=review.scores["close"],
                overall=review.overall,
                ethics_violation=review.ethics_violation,
                ethics_quote=review.ethics_quote,
                next_step_with_date=review.next_step_with_date,
                question_ratio=review.question_ratio,
                avg_words=review.avg_words,
                rephrasings=[r.model_dump() for r in review.rephrasings],
                strengths=review.strengths,
                summary=review.summary,
            )
        )
        await db.commit()
        return review

    async def history(self, tg_id: int, limit: int = 10) -> list[HistoryItem]:
        async with self.sm() as db:
            user = await self._user(db, tg_id)
            await db.commit()
            sessions = (
                await db.scalars(
                    select(TrainingSession)
                    .where(TrainingSession.user_id == user.id, TrainingSession.status != "abandoned")
                    .options(selectinload(TrainingSession.review))
                    .order_by(TrainingSession.id.desc())
                    .limit(limit)
                )
            ).all()
            return [
                HistoryItem(
                    session=s,
                    persona_title=self.content.personas[s.persona_key].title
                    if s.persona_key in self.content.personas
                    else s.persona_key,
                    review=s.review,
                )
                for s in sessions
            ]

