"""Сквозной сценарий тренировки на офлайн-заглушке Claude."""

from datetime import datetime, timezone

import pytest
from sqlalchemy import func, select

from app.db.models import AIUsage, SessionReview, TrainingSession
from app.trainer.service import BudgetExceeded, TrainerError

TG = 111


async def test_full_session_with_end(trainer, llm, sessionmaker):
    await trainer.start(TG, "purchaser_price", "ru", 2)
    r1 = await trainer.reply(TG, "Добрый день! Как сейчас работает ваша котельная?")
    assert r1.persona_text and r1.outcome is None
    await trainer.reply(TG, "Сколько промывок мембран было за год?")

    review = await trainer.end(TG)
    assert review.question_ratio == 1.0
    assert 1 <= review.overall <= 10
    assert len(review.rephrasings) == 3

    # История передаётся модели целиком, роли чередуются
    last_chat = [c for c in llm.calls if c["kind"] == "chat"][-1]
    assert [m["role"] for m in last_chat["messages"]] == ["user", "assistant", "user"]

    async with sessionmaker() as db:
        s = await db.scalar(select(TrainingSession))
        assert s.status == "finished" and s.turns == 2
        assert await db.scalar(select(func.count()).select_from(SessionReview)) == 1
        assert await db.scalar(select(func.count()).select_from(AIUsage)) == 3


async def test_agreed_step_ends_session_and_reviews(trainer):
    await trainer.start(TG, "ecologist_non_dm", "uz_cyrl", 1)
    await trainer.reply(TG, "Кто у вас принимает решение по аудиту?")
    result = await trainer.reply(TG, "Давайте встретимся с главным инженером в среду в 10:00?")
    assert result.outcome == "agreed"
    assert result.review is not None and result.review.next_step_with_date
    with pytest.raises(TrainerError):
        await trainer.reply(TG, "ещё реплика")


async def test_hangup(trainer, sessionmaker):
    await trainer.start(TG, "purchaser_price", "ru", 3)
    await trainer.reply(TG, "Дадим скидку")
    await trainer.reply(TG, "Ещё скидку")
    result = await trainer.reply(TG, "Хорошо, скидка 15%")
    assert result.outcome == "hung_up"
    assert "<<" not in result.persona_text
    async with sessionmaker() as db:
        assert (await db.scalar(select(TrainingSession))).status == "hung_up"


async def test_ethics_violation_detected_and_capped(trainer):
    await trainer.start(TG, "ecologist_non_dm", "ru", 2)
    await trainer.reply(TG, "Гарантирую экономию 30% на реагентах!")
    review = await trainer.end(TG)
    assert review.ethics_violation
    assert review.overall <= 4


async def test_max_turns_triggers_review(trainer, settings):
    await trainer.start(TG, "silent_after_kp", "ru", 1)
    result = None
    for i in range(settings.max_turns):
        result = await trainer.reply(TG, f"Реплика {i}")
    assert result.outcome == "max_turns" and result.review is not None


async def test_new_start_abandons_previous(trainer, sessionmaker):
    await trainer.start(TG, "purchaser_price", "ru", 1)
    await trainer.start(TG, "silent_after_kp", "ru", 1)
    async with sessionmaker() as db:
        statuses = (await db.scalars(select(TrainingSession.status).order_by(TrainingSession.id))).all()
    assert statuses == ["abandoned", "active"]


async def test_end_without_replies(trainer):
    await trainer.start(TG, "purchaser_price", "ru", 1)
    with pytest.raises(TrainerError, match="ни одной реплики"):
        await trainer.end(TG)


async def test_reply_without_session(trainer):
    with pytest.raises(TrainerError, match="/train"):
        await trainer.reply(TG, "Привет")


async def test_budget_exceeded_blocks_start(trainer, sessionmaker, settings):
    async with sessionmaker() as db:
        db.add(AIUsage(purpose="dialog", model="x", cost_usd=settings.ai_monthly_budget_usd,
                       created_at=datetime.now(timezone.utc)))
        await db.commit()
    with pytest.raises(BudgetExceeded):
        await trainer.start(TG, "purchaser_price", "ru", 1)


async def test_review_retry_after_failure(trainer, llm):
    await trainer.start(TG, "purchaser_price", "ru", 1)
    await trainer.reply(TG, "Как дела с котлом?")

    original = llm.structured

    async def boom(**kwargs):
        from app.ai.client import LLMError
        raise LLMError("Нет связи с Claude API.")

    llm.structured = boom
    with pytest.raises(TrainerError, match="/end"):
        await trainer.end(TG)
    llm.structured = original
    review = await trainer.end(TG)  # повтор разбора последней сессии
    assert review.overall > 0
    with pytest.raises(TrainerError):
        await trainer.end(TG)  # разбор уже есть


async def test_history(trainer):
    await trainer.start(TG, "purchaser_price", "ru", 1)
    await trainer.reply(TG, "Вопрос?")
    await trainer.end(TG)
    items = await trainer.history(TG)
    assert len(items) == 1 and items[0].review is not None
    assert items[0].persona_title == "Закупщик-«ценовик»"
