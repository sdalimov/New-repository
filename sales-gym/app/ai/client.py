"""Обёртка над Claude API. В тестах подменяется FakeLLM с тем же интерфейсом."""

import logging
from dataclasses import dataclass
from typing import Protocol, TypeVar

import anthropic
from pydantic import BaseModel

from app.ai.budget import Usage

log = logging.getLogger(__name__)

T = TypeVar("T", bound=BaseModel)

# Модели, для которых включаем серверный fallback при отказе (refusal)
FALLBACK_MODELS = ("claude-opus-5", "claude-opus-5-5", "claude-fable-5-1")
FALLBACK_BETA = "server-side-fallback-2026-07-01"


class LLMError(Exception):
    """Ошибка вызова ИИ, текст можно показать пользователю."""


@dataclass
class ChatResult:
    text: str
    usage: Usage
    refused: bool = False


@dataclass
class StructuredResult:
    data: BaseModel | None
    usage: Usage
    refused: bool = False


class LLM(Protocol):
    async def chat(
        self, *, model: str, system: str, messages: list[dict], effort: str, max_tokens: int
    ) -> ChatResult: ...

    async def structured(
        self,
        *,
        model: str,
        system: str,
        prompt: str,
        schema: type[T],
        effort: str,
        max_tokens: int,
    ) -> StructuredResult: ...


def supports_effort(model: str) -> bool:
    return not model.startswith(("claude-haiku-4-5", "claude-sonnet-4-5"))


def _usage(model: str, u) -> Usage:
    return Usage(
        model=model,
        input_tokens=u.input_tokens or 0,
        output_tokens=u.output_tokens or 0,
        cache_write_tokens=getattr(u, "cache_creation_input_tokens", 0) or 0,
        cache_read_tokens=getattr(u, "cache_read_input_tokens", 0) or 0,
    )


class ClaudeLLM:
    def __init__(self, api_key: str):
        if not api_key:
            raise LLMError("ANTHROPIC_API_KEY не задан в .env")
        self.client = anthropic.AsyncAnthropic(api_key=api_key, timeout=120.0, max_retries=3)

    @staticmethod
    def _effort(model: str, effort: str) -> dict:
        return {"output_config": {"effort": effort}} if supports_effort(model) else {}

    async def chat(
        self, *, model: str, system: str, messages: list[dict], effort: str, max_tokens: int
    ) -> ChatResult:
        try:
            response = await self.client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=messages,
                # Кешируем растущий префикс диалога: каждая следующая реплика дешевле
                cache_control={"type": "ephemeral"},
                **self._effort(model, effort),
            )
        except anthropic.APIError as e:
            raise LLMError(_describe_error(e)) from e

        usage = _usage(response.model, response.usage)
        if response.stop_reason == "refusal":
            return ChatResult(text="", usage=usage, refused=True)
        text = "".join(b.text for b in response.content if b.type == "text").strip()
        return ChatResult(text=text, usage=usage)

    async def structured(
        self,
        *,
        model: str,
        system: str,
        prompt: str,
        schema: type[T],
        effort: str,
        max_tokens: int,
    ) -> StructuredResult:
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            system=system,
            messages=[{"role": "user", "content": prompt}],
            output_format=schema,
            **self._effort(model, effort),
        )
        try:
            if model.startswith(FALLBACK_MODELS):
                response = await self.client.beta.messages.parse(
                    betas=[FALLBACK_BETA], fallbacks="default", **kwargs
                )
            else:
                response = await self.client.messages.parse(**kwargs)
        except anthropic.APIError as e:
            raise LLMError(_describe_error(e)) from e

        usage = _usage(response.model, response.usage)
        if response.stop_reason == "refusal":
            return StructuredResult(data=None, usage=usage, refused=True)
        return StructuredResult(data=response.parsed_output, usage=usage)


def _describe_error(e: anthropic.APIError) -> str:
    if isinstance(e, anthropic.AuthenticationError):
        return "Неверный ANTHROPIC_API_KEY."
    if isinstance(e, anthropic.PermissionDeniedError):
        return "У ключа нет доступа к модели или закончились средства на счёте Anthropic."
    if isinstance(e, anthropic.NotFoundError):
        return "Модель не найдена — проверьте CLAUDE_MODEL_* в .env."
    if isinstance(e, anthropic.RateLimitError):
        return "Превышен лимит запросов Claude API, попробуйте через минуту."
    if isinstance(e, anthropic.BadRequestError):
        log.error("Claude bad request: %s", e.message)
        return f"Ошибка запроса к Claude: {e.message}"
    if isinstance(e, anthropic.APIConnectionError):
        return "Нет связи с Claude API."
    if isinstance(e, anthropic.APIStatusError):
        return f"Claude API вернул ошибку {e.status_code}, попробуйте позже."
    return "Ошибка Claude API."
