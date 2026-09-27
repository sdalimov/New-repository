from app.content import DIFFICULTY_NAMES, LANGUAGES, Content, Persona

HANGUP = "<<HANGUP>>"
AGREED = "<<AGREED>>"

OUTCOMES = {
    "finished": "продавец завершил разговор сам (команда /end)",
    "hung_up": "клиент прекратил разговор",
    "agreed": "клиент согласился на следующий шаг (по мнению персонажа — проверь сам)",
    "max_turns": "достигнут лимит реплик",
}


def _fill(template: str, **values: str) -> str:
    for key, value in values.items():
        template = template.replace("{{" + key + "}}", value)
    return template


def persona_system_prompt(content: Content, persona: Persona, language: str, difficulty: int) -> str:
    return _fill(
        content.persona_base,
        persona=persona.describe(),
        channel=persona.channel,
        difficulty=f"{difficulty} ({DIFFICULTY_NAMES[difficulty]}). {persona.difficulty[difficulty]}",
        language=LANGUAGES[language]["instruction"],
    )


def review_prompts(
    content: Content,
    persona: Persona,
    language: str,
    difficulty: int,
    outcome: str,
    transcript: list[tuple[str, str]],
) -> tuple[str, str]:
    system = _fill(
        content.reviewer,
        persona=persona.describe(),
        difficulty=f"{difficulty} ({DIFFICULTY_NAMES[difficulty]})",
        language_name=LANGUAGES[language]["name"],
        outcome=OUTCOMES.get(outcome, outcome),
        rubric=content.rubric.describe(),
    )
    lines = [f"{'ПРОДАВЕЦ' if role == 'seller' else 'КЛИЕНТ'}: {text}" for role, text in transcript]
    prompt = "Разговор:\n\n" + "\n\n".join(lines) + "\n\nСделай разбор по правилам."
    return system, prompt


def parse_markers(text: str) -> tuple[str, str | None]:
    """Убрать служебные маркеры из реплики персонажа и вернуть исход."""
    outcome = None
    if HANGUP in text:
        outcome = "hung_up"
    elif AGREED in text:
        outcome = "agreed"
    clean = text.replace(HANGUP, "").replace(AGREED, "").strip()
    return clean, outcome
