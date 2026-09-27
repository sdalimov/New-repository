import asyncio
import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand, TelegramObject, User

from app.ai.client import ClaudeLLM
from app.bot.trainer_router import router as trainer_router
from app.config import get_settings
from app.content import load_content
from app.db.session import make_engine, make_sessionmaker
from app.trainer.service import TrainerService

log = logging.getLogger("sales_gym")


class WhitelistMiddleware(BaseMiddleware):
    """Бот отвечает только владельцу (ALLOWED_TG_IDS)."""

    def __init__(self, allowed: list[int]):
        self.allowed = set(allowed)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User | None = data.get("event_from_user")
        if user is None or user.id in self.allowed:
            return await handler(event, data)
        log.warning("Отклонён пользователь %s (@%s)", user.id, user.username)
        if not self.allowed and hasattr(event, "answer"):
            # Первый запуск: подсказать владельцу его ID
            await event.answer(f"Доступ закрыт. Ваш Telegram ID: {user.id} — впишите его в ALLOWED_TG_IDS в .env")
        return None


def build_dispatcher(trainer: TrainerService, allowed_tg_ids: list[int]) -> Dispatcher:
    dp = Dispatcher()
    dp["trainer"] = trainer
    dp.message.outer_middleware(WhitelistMiddleware(allowed_tg_ids))
    dp.callback_query.outer_middleware(WhitelistMiddleware(allowed_tg_ids))
    dp.include_router(trainer_router)
    return dp


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    settings = get_settings()
    if not settings.telegram_bot_token:
        raise SystemExit("TELEGRAM_BOT_TOKEN не задан в .env")

    content = load_content(settings.content_dir)
    engine = make_engine(settings.database_url)
    trainer = TrainerService(make_sessionmaker(engine), ClaudeLLM(settings.anthropic_api_key), content, settings)

    bot = Bot(settings.telegram_bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = build_dispatcher(trainer, settings.allowed_tg_ids)

    await bot.set_my_commands(
        [
            BotCommand(command="train", description="Новая тренировка"),
            BotCommand(command="end", description="Завершить и получить разбор"),
            BotCommand(command="history", description="Последние тренировки"),
            BotCommand(command="budget", description="Расход на ИИ"),
            BotCommand(command="help", description="Помощь"),
        ]
    )
    log.info("Бот запущен. Персонажей: %d, модели: %s / %s", len(content.personas),
             settings.claude_model_dialog, settings.claude_model_review)
    try:
        await dp.start_polling(bot)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
