from datetime import datetime, timezone

import pytest

from app.ai.budget import (
    BudgetStatus,
    Usage,
    budget_status,
    cost_usd,
    month_start,
    price_for,
    record_usage,
)
from app.db.models import AIUsage


def test_cost_sonnet():
    # 1M вход × $2 + 100k выход × $10 = $3
    assert cost_usd(Usage("claude-sonnet-5", input_tokens=1_000_000, output_tokens=100_000)) == pytest.approx(3.0)


def test_cost_cache_multipliers():
    u = Usage("claude-opus-5", cache_write_tokens=1_000_000, cache_read_tokens=1_000_000)
    assert cost_usd(u) == pytest.approx(5 * 1.25 + 5 * 0.1)


def test_unknown_model_uses_most_expensive_price():
    assert price_for("claude-unknown-9") == (10.0, 50.0)


def test_prefix_match_for_versioned_ids():
    assert price_for("claude-opus-5-5") == (4.0, 20.0)
    assert price_for("claude-opus-5") == (5.0, 25.0)


def test_status_levels():
    assert not BudgetStatus(7.9, 10, 0.8).warning
    assert BudgetStatus(8.0, 10, 0.8).warning
    s = BudgetStatus(10.0, 10, 0.8)
    assert s.exceeded and not s.warning


def test_month_start_uses_local_timezone():
    # 30 сентября 20:00 UTC = 1 октября 01:00 в Ташкенте → месяц уже октябрь
    now = datetime(2026, 9, 30, 20, 0, tzinfo=timezone.utc)
    assert month_start(now, "Asia/Tashkent") == datetime(2026, 9, 30, 19, 0, tzinfo=timezone.utc)


async def test_month_spent_ignores_previous_month(sessionmaker):
    async with sessionmaker() as db:
        db.add(AIUsage(purpose="dialog", model="x", cost_usd=5.0, created_at=datetime(2026, 8, 31, 12, tzinfo=timezone.utc)))
        await record_usage(db, "dialog", Usage("claude-sonnet-5", input_tokens=500_000))  # $1
        await db.commit()
        status = await budget_status(db, 10.0, 0.8, "Asia/Tashkent")
    assert status.spent == pytest.approx(1.0)
