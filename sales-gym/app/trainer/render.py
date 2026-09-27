"""Форматирование сообщений тренажёра (Telegram HTML)."""

import re
from html import escape, unescape

from app.ai.budget import BudgetStatus
from app.content import DIFFICULTY_NAMES, LANGUAGES, Persona
from app.trainer.scoring import FinalReview

CRITERIA_NAMES = {
    "needs": "Выявление потребности",
    "value": "Ценность",
    "objections": "Возражения",
    "close": "Закрытие на шаг",
}

OUTCOME_TEXT = {
    "hung_up": "📵 Клиент закончил разговор.",
    "agreed": "🤝 Клиент согласился на следующий шаг.",
    "max_turns": "⏱ Достигнут лимит реплик.",
}


def bar(score: float) -> str:
    filled = max(0, min(10, round(score)))
    return "▰" * filled + "▱" * (10 - filled)


def briefing(persona: Persona, language: str, difficulty: int) -> str:
    return (
        f"{persona.emoji} <b>{escape(persona.title)}</b>\n"
        f"Канал: {escape(persona.channel)} · Язык: {LANGUAGES[language]['name']} · "
        f"Уровень: {difficulty} ({DIFFICULTY_NAMES[difficulty]})\n\n"
        f"{escape(persona.briefing.strip())}\n\n"
        "Вы начинаете первым — напишите первую реплику.\n"
        "Завершить и получить разбор: /end"
    )


def review(r: FinalReview) -> str:
    lines = [f"<b>📊 Разбор: {r.overall}/10</b>  {bar(r.overall)}", ""]
    for key, name in CRITERIA_NAMES.items():
        lines.append(f"{bar(r.scores[key])} {r.scores[key]:>2} — {name}")
    lines.append("")
    lines.append(
        f"Шаг с датой: {'✅ да' if r.next_step_with_date else '❌ нет'} · "
        f"Реплик с вопросом: {round(r.question_ratio * 100)}% · "
        f"Средняя длина: {r.avg_words:g} слов"
    )
    if r.ethics_violation:
        lines += ["", "⚠️ <b>Нарушение этики: обещание экономии до аудита</b>"]
        if r.ethics_quote:
            lines.append(f"<i>«{escape(r.ethics_quote)}»</i>")
    for cap in r.caps_applied:
        lines.append(f"• {escape(cap)}")

    if r.strengths:
        lines += ["", "<b>👍 Сильные стороны</b>"]
        lines += [f"• {escape(s)}" for s in r.strengths]

    if r.rephrasings:
        lines += ["", "<b>✍️ Сказать иначе</b>"]
        for i, p in enumerate(r.rephrasings, 1):
            lines += [
                f"{i}. Было: <i>{escape(p.said)}</i>",
                f"   Лучше: <b>{escape(p.better)}</b>",
                f"   {escape(p.why)}",
            ]

    lines += ["", f"<b>🎯 Вывод</b>\n{escape(r.summary)}"]
    return "\n".join(lines)


def budget_line(b: BudgetStatus) -> str:
    return f"ИИ в этом месяце: ${b.spent:.2f} из ${b.limit:.2f} ({round(b.ratio * 100)}%)"


_TAG = re.compile(r"<[^>]+>")


def plain(html_text: str) -> str:
    """HTML → обычный текст для консольного режима."""
    return unescape(_TAG.sub("", html_text))
