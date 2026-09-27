"""Загрузка редактируемого контента: персонажи, критерии, промты."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

LANGUAGES: dict[str, dict[str, str]] = {
    "ru": {
        "name": "русский",
        "button": "🇷🇺 Русский",
        "instruction": "Говори только по-русски.",
    },
    "uz_cyrl": {
        "name": "узбекский (кириллица)",
        "button": "🇺🇿 Ўзбекча",
        "instruction": (
            "Говори только по-узбекски, кириллицей (ўзбек кирилл алифбоси). "
            "Технические термины (антискалант, флокулянт, осмос) можно оставлять по-русски, "
            "как принято на заводах Узбекистана."
        ),
    },
    "uz_latn": {
        "name": "узбекский (латиница)",
        "button": "🇺🇿 O'zbekcha",
        "instruction": (
            "Говори только по-узбекски, латиницей (o'zbek lotin alifbosi). "
            "Технические термины (antiskalant, flokulyant, osmos) можно оставлять как принято на заводах."
        ),
    },
}

DIFFICULTY_NAMES = {1: "лёгкий", 2: "средний", 3: "сложный"}


@dataclass(frozen=True)
class Persona:
    key: str
    order: int
    emoji: str
    title: str
    channel: str
    briefing: str
    name: str
    role: str
    company: str
    personality: str
    situation: str
    hidden_needs: list[str]
    objections: list[str]
    will_agree_if: str
    hangup_if: str
    difficulty: dict[int, str]

    def describe(self) -> str:
        """Описание персонажа для модели (продавец его не видит)."""
        needs = "\n".join(f"- {n}" for n in self.hidden_needs)
        objections = "\n".join(f"- {o}" for o in self.objections)
        return (
            f"Имя: {self.name}\n"
            f"Роль: {self.role}\n"
            f"Компания: {self.company.strip()}\n"
            f"Характер: {self.personality.strip()}\n"
            f"Ситуация: {self.situation.strip()}\n"
            f"Скрытые потребности:\n{needs}\n"
            f"Возражения:\n{objections}\n"
            f"Согласится на следующий шаг, если: {self.will_agree_if.strip()}\n"
            f"Положит трубку, если: {self.hangup_if.strip()}"
        )


@dataclass(frozen=True)
class Criterion:
    key: str
    name: str
    weight: float
    description: str
    anchors: dict[str, str]


@dataclass(frozen=True)
class Rubric:
    criteria: list[Criterion]
    ethics_cap: int
    no_dated_step_close_cap: int

    def describe(self) -> str:
        parts = []
        for c in self.criteria:
            anchors = "\n".join(f"  {k}: {v}" for k, v in c.anchors.items())
            parts.append(f"### {c.key} — {c.name}\n{c.description.strip()}\n{anchors}")
        return "\n\n".join(parts)


@dataclass
class Content:
    personas: dict[str, Persona]
    rubric: Rubric
    persona_base: str
    reviewer: str
    root: Path = field(default=Path("."))

    def personas_sorted(self) -> list[Persona]:
        return sorted(self.personas.values(), key=lambda p: p.order)


def _load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_persona(path: Path) -> Persona:
    data = _load_yaml(path)
    data["difficulty"] = {int(k): str(v) for k, v in data["difficulty"].items()}
    missing = {1, 2, 3} - data["difficulty"].keys()
    if missing:
        raise ValueError(f"{path.name}: нет описания уровней сложности {sorted(missing)}")
    return Persona(**data)


def load_rubric(path: Path) -> Rubric:
    data = _load_yaml(path)
    criteria = [Criterion(**c) for c in data["criteria"]]
    total = sum(c.weight for c in criteria)
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"{path.name}: сумма весов критериев = {total}, должна быть 1.0")
    rules = data["rules"]
    return Rubric(
        criteria=criteria,
        ethics_cap=int(rules["ethics_cap"]),
        no_dated_step_close_cap=int(rules["no_dated_step_close_cap"]),
    )


def load_content(root: Path) -> Content:
    personas = {}
    for path in sorted((root / "personas").glob("*.yaml")):
        persona = load_persona(path)
        personas[persona.key] = persona
    if not personas:
        raise ValueError(f"В {root / 'personas'} нет персонажей")
    return Content(
        personas=personas,
        rubric=load_rubric(root / "rubrics" / "negotiation.yaml"),
        persona_base=(root / "prompts" / "persona_base.md").read_text(encoding="utf-8"),
        reviewer=(root / "prompts" / "reviewer.md").read_text(encoding="utf-8"),
        root=root,
    )
