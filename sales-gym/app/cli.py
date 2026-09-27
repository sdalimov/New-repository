"""Консольный режим тренажёра — проверка без Telegram.

  python -m app.cli                      # интерактивный выбор, реальный Claude
  python -m app.cli --demo               # офлайн-заглушка, бесплатно
  python -m app.cli -p purchaser_price -l ru -d 2
"""

import argparse
import asyncio

from app.ai.client import ClaudeLLM
from app.ai.fake import FakeLLM
from app.config import get_settings
from app.content import DIFFICULTY_NAMES, LANGUAGES, load_content
from app.db.session import create_all, make_engine, make_sessionmaker
from app.trainer import render
from app.trainer.service import TrainerError, TrainerService

CLI_USER = 0  # условный tg_id для консоли


def choose(title: str, options: list[tuple[str, str]]) -> str:
    print(f"\n{title}")
    for i, (_, label) in enumerate(options, 1):
        print(f"  {i}. {label}")
    while True:
        raw = input("> ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1][0]
        print("Введите номер из списка")


async def run(args: argparse.Namespace) -> None:
    settings = get_settings()
    content = load_content(settings.content_dir)
    engine = make_engine(settings.database_url)
    if settings.database_url.startswith("sqlite"):
        await create_all(engine)
    llm = FakeLLM() if args.demo else ClaudeLLM(settings.anthropic_api_key)
    trainer = TrainerService(make_sessionmaker(engine), llm, content, settings)

    persona = args.persona or choose(
        "Персонаж:", [(p.key, f"{p.emoji} {p.title}") for p in content.personas_sorted()]
    )
    lang = args.lang or choose("Язык:", [(k, v["name"]) for k, v in LANGUAGES.items()])
    level = args.difficulty or int(choose("Уровень:", [(str(k), v) for k, v in DIFFICULTY_NAMES.items()]))

    try:
        start = await trainer.start(CLI_USER, persona, lang, level)
    except TrainerError as e:
        print(f"⛔ {e}")
        return
    print("\n" + render.plain(render.briefing(start.persona, lang, level)) + "\n")

    try:
        while True:
            text = input("Вы: ").strip()
            if not text:
                continue
            try:
                if text == "/end":
                    print("\n" + render.plain(render.review(await trainer.end(CLI_USER))))
                    break
                result = await trainer.reply(CLI_USER, text)
            except TrainerError as e:
                print(f"⛔ {e}")
                continue
            print(f"\n{start.persona.name}: {result.persona_text}\n")
            if result.outcome:
                print(render.OUTCOME_TEXT[result.outcome])
            if result.review:
                print("\n" + render.plain(render.review(result.review)))
                break
    except (EOFError, KeyboardInterrupt):
        print("\nВыход без разбора.")
    print("\n" + render.budget_line(await trainer.budget()))
    await engine.dispose()


def main() -> None:
    parser = argparse.ArgumentParser(description="Тренажёр переговоров в консоли")
    parser.add_argument("-p", "--persona")
    parser.add_argument("-l", "--lang", choices=list(LANGUAGES))
    parser.add_argument("-d", "--difficulty", type=int, choices=[1, 2, 3])
    parser.add_argument("--demo", action="store_true", help="офлайн-заглушка вместо Claude (бесплатно)")
    asyncio.run(run(parser.parse_args()))


if __name__ == "__main__":
    main()
