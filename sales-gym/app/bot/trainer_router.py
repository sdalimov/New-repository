import asyncio
from collections import defaultdict
from datetime import timezone
from zoneinfo import ZoneInfo

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.utils.chat_action import ChatActionSender

from app.content import DIFFICULTY_NAMES, LANGUAGES
from app.trainer import render
from app.trainer.service import TrainerError, TrainerService

router = Router(name="trainer")

# Одна реплика за раз: пока персонаж «думает», следующее сообщение ждёт
_locks: dict[int, asyncio.Lock] = defaultdict(asyncio.Lock)

TG_LIMIT = 4000

HELP = (
    "<b>Sales Gym — тренажёр переговоров</b>\n\n"
    "/train — новая тренировка (персонаж → язык → уровень)\n"
    "/end — завершить и получить разбор\n"
    "/history — последние тренировки и оценки\n"
    "/budget — расход на ИИ в этом месяце\n\n"
    "Во время тренировки просто пишите реплики — персонаж отвечает."
)


def chunks(text: str, size: int = TG_LIMIT) -> list[str]:
    if len(text) <= size:
        return [text]
    parts, current = [], ""
    for line in text.split("\n"):
        if len(current) + len(line) + 1 > size and current:
            parts.append(current)
            current = ""
        current += line + "\n"
    if current:
        parts.append(current)
    return parts


async def send_long(message: Message, text: str) -> None:
    for part in chunks(text):
        await message.answer(part)


def personas_kb(trainer: TrainerService) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"{p.emoji} {p.title}", callback_data=f"p:{p.key}")]
            for p in trainer.content.personas_sorted()
        ]
    )


def languages_kb(persona_key: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=v["button"], callback_data=f"l:{persona_key}:{k}")
                for k, v in LANGUAGES.items()
            ]
        ]
    )


def difficulty_kb(persona_key: str, lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{n} · {name}", callback_data=f"d:{persona_key}:{lang}:{n}")
                for n, name in DIFFICULTY_NAMES.items()
            ]
        ]
    )


@router.message(CommandStart())
@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(HELP)


@router.message(Command("train"))
async def cmd_train(message: Message, trainer: TrainerService) -> None:
    note = ""
    if await trainer.has_active(message.from_user.id):
        note = "\n\n<i>Текущая тренировка будет закрыта без разбора. Разбор сейчас: /end</i>"
    await message.answer("С кем тренируемся?" + note, reply_markup=personas_kb(trainer))


@router.callback_query(F.data.startswith("p:"))
async def cb_persona(cb: CallbackQuery) -> None:
    key = cb.data.split(":", 1)[1]
    await cb.message.edit_text("Язык разговора?", reply_markup=languages_kb(key))
    await cb.answer()


@router.callback_query(F.data.startswith("l:"))
async def cb_language(cb: CallbackQuery) -> None:
    _, key, lang = cb.data.split(":")
    await cb.message.edit_text("Уровень сложности?", reply_markup=difficulty_kb(key, lang))
    await cb.answer()


@router.callback_query(F.data.startswith("d:"))
async def cb_difficulty(cb: CallbackQuery, trainer: TrainerService) -> None:
    _, key, lang, level = cb.data.split(":")
    try:
        result = await trainer.start(cb.from_user.id, key, lang, int(level))
    except TrainerError as e:
        await cb.message.edit_text(f"⛔ {e}")
        await cb.answer()
        return
    text = render.briefing(result.persona, lang, int(level))
    if result.budget.warning:
        text += f"\n\n⚠️ {render.budget_line(result.budget)}"
    await cb.message.edit_text(text)
    await cb.answer()


@router.message(Command("end"))
async def cmd_end(message: Message, trainer: TrainerService) -> None:
    async with _locks[message.from_user.id]:
        try:
            async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
                review = await trainer.end(message.from_user.id)
        except TrainerError as e:
            await message.answer(f"⛔ {e}")
            return
    await send_long(message, render.review(review))


@router.message(Command("history"))
async def cmd_history(message: Message, trainer: TrainerService) -> None:
    items = await trainer.history(message.from_user.id)
    if not items:
        await message.answer("Тренировок пока нет. Начните: /train")
        return
    tz = ZoneInfo(trainer.settings.timezone)
    lines = ["<b>Последние тренировки</b>", ""]
    for it in items:
        s = it.session
        started = s.started_at if s.started_at.tzinfo else s.started_at.replace(tzinfo=timezone.utc)
        when = started.astimezone(tz).strftime("%d.%m %H:%M")
        score = f"<b>{it.review.overall}</b>/10" if it.review else "без разбора"
        flags = ""
        if it.review:
            flags = (" ✅" if it.review.next_step_with_date else "") + (" ⚠️" if it.review.ethics_violation else "")
        lines.append(
            f"{when} · {it.persona_title} · {LANGUAGES[s.language]['name']} · ур.{s.difficulty} → {score}{flags}"
        )
    lines += ["", "✅ — шаг с датой, ⚠️ — обещание экономии до аудита"]
    await message.answer("\n".join(lines))


@router.message(Command("budget"))
async def cmd_budget(message: Message, trainer: TrainerService) -> None:
    status = await trainer.budget()
    await message.answer(render.budget_line(status))


@router.message(F.text & ~F.text.startswith("/"))
async def on_text(message: Message, trainer: TrainerService) -> None:
    async with _locks[message.from_user.id]:
        try:
            async with ChatActionSender.typing(bot=message.bot, chat_id=message.chat.id):
                result = await trainer.reply(message.from_user.id, message.text)
        except TrainerError as e:
            await message.answer(f"⛔ {e}")
            return

    await message.answer(result.persona_text, parse_mode=None)
    if result.outcome:
        await message.answer(render.OUTCOME_TEXT[result.outcome])
    if result.review:
        await send_long(message, render.review(result.review))
