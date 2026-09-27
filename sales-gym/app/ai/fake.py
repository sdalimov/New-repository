"""Офлайн-заглушка Claude: для тестов и демо-режима без API-ключа (бесплатно)."""

import re

from app.ai.budget import FAKE_MODEL, Usage
from app.ai.client import ChatResult, StructuredResult

DATE_RE = re.compile(
    r"\b\d{1,2}[.:/]\d{2}\b|\b\d{1,2}\s+(январ|феврал|март|апрел|ма[яй]|июн|июл|август|сентябр|октябр|ноябр|декабр)"
    r"|понедельник|вторник|сред[ау]|четверг|пятниц|суббот",
    re.IGNORECASE,
)
PROMISE_RE = re.compile(r"гарант\w*.*(эконом|сниз|%)|(эконом|сниз)\w*.*гарант", re.IGNORECASE)

CANNED = [
    "Слушаю вас. Только коротко, у меня совещание.",
    "У другого поставщика дешевле. Почему я должна платить больше?",
    "Пришлите предложение на почту, мы посмотрим.",
    "Это не мне решать, честно говоря.",
    "А вы гарантируете результат?",
]


class FakeLLM:
    def __init__(self):
        self.calls: list[dict] = []

    async def chat(self, *, model, system, messages, effort, max_tokens) -> ChatResult:
        self.calls.append({"kind": "chat", "model": model, "messages": messages})
        last = messages[-1]["content"]
        seller_turns = sum(1 for m in messages if m["role"] == "user")
        if DATE_RE.search(last):
            text = "Хорошо, давайте так и сделаем. До встречи. <<AGREED>>"
        elif "скидк" in last.lower() and seller_turns >= 3:
            text = "Понятно, тогда выберем по цене. Спасибо. <<HANGUP>>"
        else:
            text = CANNED[(seller_turns - 1) % len(CANNED)]
        return ChatResult(text=text, usage=Usage(model=FAKE_MODEL, input_tokens=1500, output_tokens=60))

    async def structured(self, *, model, system, prompt, schema, effort, max_tokens) -> StructuredResult:
        self.calls.append({"kind": "structured", "model": model, "prompt": prompt})
        seller = [
            line.removeprefix("ПРОДАВЕЦ: ")
            for line in prompt.split("\n\n")
            if line.startswith("ПРОДАВЕЦ: ")
        ]
        questions = sum("?" in s for s in seller)
        dated = any(DATE_RE.search(s) for s in seller)
        promise = next((s for s in seller if PROMISE_RE.search(s)), "")
        needs = min(10, 3 + 2 * questions)
        data = schema(
            score_needs=needs,
            score_value=5,
            score_objections=5,
            score_close=8 if dated else 5,
            ethics_violation=bool(promise),
            ethics_quote=promise,
            next_step_with_date=dated,
            rephrasings=[
                {"said": s, "better": "Что для вас сейчас самое критичное по воде?", "why": "Открытый вопрос о боли."}
                for s in (seller + ["(не сказано)"] * 3)[:3]
            ],
            strengths=["Вы начали разговор уверенно."],
            summary="Демо-разбор (без ИИ). На следующей тренировке задайте минимум 3 открытых вопроса.",
        )
        return StructuredResult(data=data, usage=Usage(model=FAKE_MODEL, input_tokens=3000, output_tokens=800))
