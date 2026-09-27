import pytest

from app.ai.fake import FakeLLM
from app.config import BASE_DIR, Settings
from app.content import load_content
from app.db.session import create_all, make_engine, make_sessionmaker
from app.trainer.service import TrainerService


@pytest.fixture(scope="session")
def content():
    return load_content(BASE_DIR / "content")


@pytest.fixture
def settings():
    return Settings(
        _env_file=None,
        database_url="sqlite+aiosqlite:///:memory:",
        ai_monthly_budget_usd=10.0,
        max_turns=5,
    )


@pytest.fixture
async def sessionmaker(settings):
    engine = make_engine(settings.database_url)
    await create_all(engine)
    yield make_sessionmaker(engine)
    await engine.dispose()


@pytest.fixture
def llm():
    return FakeLLM()


@pytest.fixture
def trainer(sessionmaker, llm, content, settings):
    return TrainerService(sessionmaker, llm, content, settings)
