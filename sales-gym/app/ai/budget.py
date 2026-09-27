"""Учёт стоимости вызовов Claude и месячный лимит."""

import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import AIUsage

log = logging.getLogger(__name__)

FAKE_MODEL = "fake"  # офлайн-заглушка, бесплатно

# USD за 1M токенов: (input, output). Запись в кеш = 1.25 × input, чтение = 0.1 × input.
PRICES: dict[str, tuple[float, float]] = {
    "claude-fable-5-1": (10.0, 50.0),
    "claude-opus-5-5": (4.0, 20.0),
    "claude-opus-5": (5.0, 25.0),
    "claude-opus-4-8": (5.0, 25.0),
    "claude-sonnet-5": (2.0, 10.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
    FAKE_MODEL: (0.0, 0.0),
}
# Неизвестная модель считается по самой дорогой цене, чтобы не превысить бюджет незаметно.
FALLBACK_PRICE = max(PRICES.values())


@dataclass
class Usage:
    model: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_write_tokens: int = 0
    cache_read_tokens: int = 0


def price_for(model: str) -> tuple[float, float]:
    if model in PRICES:
        return PRICES[model]
    for known, price in PRICES.items():
        if model.startswith(known):
            return price
    log.warning("Нет цены для модели %s — считаю по максимальной", model)
    return FALLBACK_PRICE


def cost_usd(usage: Usage) -> float:
    p_in, p_out = price_for(usage.model)
    total = (
        usage.input_tokens * p_in
        + usage.cache_write_tokens * p_in * 1.25
        + usage.cache_read_tokens * p_in * 0.1
        + usage.output_tokens * p_out
    )
    return total / 1_000_000


@dataclass
class BudgetStatus:
    spent: float
    limit: float
    warn_ratio: float

    @property
    def ratio(self) -> float:
        return self.spent / self.limit if self.limit > 0 else 1.0

    @property
    def exceeded(self) -> bool:
        return self.spent >= self.limit

    @property
    def warning(self) -> bool:
        return not self.exceeded and self.ratio >= self.warn_ratio


def month_start(now: datetime, tz: str) -> datetime:
    local = now.astimezone(ZoneInfo(tz))
    start = local.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return start.astimezone(timezone.utc)


async def record_usage(db: AsyncSession, purpose: str, usage: Usage) -> float:
    cost = cost_usd(usage)
    db.add(
        AIUsage(
            purpose=purpose,
            model=usage.model,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            cache_write_tokens=usage.cache_write_tokens,
            cache_read_tokens=usage.cache_read_tokens,
            cost_usd=cost,
        )
    )
    return cost


async def month_spent(db: AsyncSession, tz: str, now: datetime | None = None) -> float:
    since = month_start(now or datetime.now(timezone.utc), tz)
    result = await db.execute(
        select(func.coalesce(func.sum(AIUsage.cost_usd), 0.0)).where(AIUsage.created_at >= since)
    )
    return float(result.scalar_one())


async def budget_status(
    db: AsyncSession, limit: float, warn_ratio: float, tz: str, now: datetime | None = None
) -> BudgetStatus:
    return BudgetStatus(spent=await month_spent(db, tz, now), limit=limit, warn_ratio=warn_ratio)
