"""Оценка сессии: схема ответа модели-тренера и детерминированные правила поверх неё."""

import re
from dataclasses import dataclass, field

from pydantic import BaseModel, Field

from app.content import Rubric

CRITERIA_KEYS = ("needs", "value", "objections", "close")


class Rephrasing(BaseModel):
    said: str = Field(description="Дословная цитата продавца или '(не сказано)'")
    better: str = Field(description="Как сказать лучше, на языке разговора")
    why: str = Field(description="Почему так лучше, по-русски, одно предложение")


class ReviewDraft(BaseModel):
    """То, что возвращает модель-тренер (structured output)."""

    score_needs: int = Field(description="Выявление потребности, 1-10")
    score_value: int = Field(description="Донесение ценности, 1-10")
    score_objections: int = Field(description="Работа с возражениями, 1-10")
    score_close: int = Field(description="Закрытие на следующий шаг, 1-10")
    ethics_violation: bool = Field(description="Обещал экономию/результат до аудита")
    ethics_quote: str = Field(description="Цитата-нарушение или пустая строка")
    next_step_with_date: bool = Field(description="Согласован шаг с конкретной датой")
    rephrasings: list[Rephrasing] = Field(description="Ровно 3 фразы")
    strengths: list[str] = Field(description="1-2 сильные стороны")
    summary: str = Field(description="2-3 предложения: вывод и действие")


@dataclass
class FinalReview:
    scores: dict[str, int]
    overall: float
    ethics_violation: bool
    ethics_quote: str
    next_step_with_date: bool
    question_ratio: float
    avg_words: float
    rephrasings: list[Rephrasing]
    strengths: list[str]
    summary: str
    caps_applied: list[str] = field(default_factory=list)


def clamp_score(value: int) -> int:
    return max(1, min(10, int(value)))


_WORD = re.compile(r"\w+", re.UNICODE)


def seller_stats(seller_messages: list[str]) -> tuple[float, float]:
    """Доля реплик продавца с вопросом и средняя длина реплики в словах."""
    if not seller_messages:
        return 0.0, 0.0
    with_question = sum(1 for m in seller_messages if "?" in m)
    words = [len(_WORD.findall(m)) for m in seller_messages]
    return with_question / len(seller_messages), sum(words) / len(words)


def finalize_review(draft: ReviewDraft, rubric: Rubric, seller_messages: list[str]) -> FinalReview:
    scores = {key: clamp_score(getattr(draft, f"score_{key}")) for key in CRITERIA_KEYS}
    caps: list[str] = []

    close_cap = rubric.no_dated_step_close_cap
    if not draft.next_step_with_date and scores["close"] > close_cap:
        scores["close"] = close_cap
        caps.append(f"Нет шага с конкретной датой → «закрытие» не выше {close_cap}")

    weights = {c.key: c.weight for c in rubric.criteria}
    overall = sum(scores[k] * weights.get(k, 0.0) for k in CRITERIA_KEYS)

    if draft.ethics_violation and overall > rubric.ethics_cap:
        overall = float(rubric.ethics_cap)
        caps.append(f"Обещание экономии до аудита → итог не выше {rubric.ethics_cap}")

    question_ratio, avg_words = seller_stats(seller_messages)
    return FinalReview(
        scores=scores,
        overall=round(overall, 1),
        ethics_violation=draft.ethics_violation,
        ethics_quote=draft.ethics_quote.strip() if draft.ethics_violation else "",
        next_step_with_date=draft.next_step_with_date,
        question_ratio=round(question_ratio, 2),
        avg_words=round(avg_words, 1),
        rephrasings=draft.rephrasings[:3],
        strengths=draft.strengths[:2],
        summary=draft.summary.strip(),
        caps_applied=caps,
    )
