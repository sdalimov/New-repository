from functools import lru_cache
from pathlib import Path
from typing import Annotated

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    telegram_bot_token: str = ""
    allowed_tg_ids: Annotated[list[int], NoDecode] = Field(default_factory=list)

    anthropic_api_key: str = ""
    claude_model_dialog: str = "claude-sonnet-5"
    claude_model_review: str = "claude-opus-5"
    claude_effort_dialog: str = "low"
    claude_effort_review: str = "medium"
    ai_monthly_budget_usd: float = 10.0
    ai_budget_warn_ratio: float = 0.8

    database_url: str = f"sqlite+aiosqlite:///{BASE_DIR / 'local.db'}"
    content_dir: Path = BASE_DIR / "content"
    timezone: str = "Asia/Tashkent"

    max_turns: int = 20

    @field_validator("allowed_tg_ids", mode="before")
    @classmethod
    def _split_ids(cls, value):
        if isinstance(value, str):
            return [int(x) for x in value.replace(" ", "").split(",") if x]
        if isinstance(value, int):
            return [value]
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
