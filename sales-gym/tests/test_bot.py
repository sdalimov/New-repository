"""Бот целиком: апдейты Telegram → хендлеры → сервис, без сети (подставная сессия aiogram)."""

from datetime import datetime

import pytest
from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.base import BaseSession
from aiogram.enums import ParseMode
from aiogram.methods import EditMessageText, GetMe, SendMessage
from aiogram.types import CallbackQuery, Chat, Message, Update, User

from app.bot.main import build_dispatcher

OWNER = 111
STRANGER = 999


class FakeSession(BaseSession):
    def __init__(self):
        super().__init__()
        self.sent: list = []

    async def make_request(self, bot, method, timeout=None):
        if isinstance(method, GetMe):
            return User(id=1, is_bot=True, first_name="Gym", username="gym_bot")
        if isinstance(method, (SendMessage, EditMessageText)):
            self.sent.append(method)
            return Message(message_id=len(self.sent), date=datetime.now(), chat=Chat(id=OWNER, type="private"),
                           text=method.text)
        return True

    async def stream_content(self, *args, **kwargs):
        yield b""

    async def close(self):
        pass


_dp = None


@pytest.fixture
def env(trainer):
    global _dp
    if _dp is None:  # роутер модульный — подключаем к одному диспетчеру
        _dp = build_dispatcher(trainer, [OWNER])
    _dp["trainer"] = trainer
    session = FakeSession()
    bot = Bot("42:TEST", session=session, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    return _dp, bot, session


def msg(text: str, user_id: int = OWNER) -> Update:
    return Update(
        update_id=1,
        message=Message(
            message_id=1,
            date=datetime.now(),
            chat=Chat(id=user_id, type="private"),
            from_user=User(id=user_id, is_bot=False, first_name="S"),
            text=text,
        ),
    )


def cb(data: str) -> Update:
    return Update(
        update_id=2,
        callback_query=CallbackQuery(
            id="1",
            from_user=User(id=OWNER, is_bot=False, first_name="S"),
            chat_instance="x",
            data=data,
            message=Message(message_id=5, date=datetime.now(), chat=Chat(id=OWNER, type="private"), text="menu"),
        ),
    )


async def test_help(env):
    dp, bot, session = env
    await dp.feed_update(bot, msg("/start"))
    assert "Sales Gym" in session.sent[-1].text


async def test_stranger_is_ignored(env):
    dp, bot, session = env
    await dp.feed_update(bot, msg("/start", STRANGER))
    assert session.sent == []


async def test_full_flow_via_menu(env):
    dp, bot, session = env
    await dp.feed_update(bot, msg("/train"))
    kb = session.sent[-1].reply_markup.inline_keyboard
    assert len(kb) == 3

    await dp.feed_update(bot, cb("p:ecologist_non_dm"))
    await dp.feed_update(bot, cb("l:ecologist_non_dm:uz_cyrl"))
    await dp.feed_update(bot, cb("d:ecologist_non_dm:uz_cyrl:2"))
    assert "Эколог завода" in session.sent[-1].text

    await dp.feed_update(bot, msg("Ассалому алайкум! Сбросларда қандай муаммолар бор?"))
    assert session.sent[-1].text  # ответ персонажа

    await dp.feed_update(bot, msg("/end"))
    assert "Разбор" in session.sent[-1].text

    await dp.feed_update(bot, msg("/history"))
    assert "Эколог завода" in session.sent[-1].text

    await dp.feed_update(bot, msg("/budget"))
    assert "$0.00 из $10.00" in session.sent[-1].text


async def test_text_without_session(env):
    dp, bot, session = env
    await dp.feed_update(bot, msg("Привет"))
    assert "/train" in session.sent[-1].text
