from app.content import LANGUAGES
from app.trainer.prompts import parse_markers, persona_system_prompt, review_prompts
from app.trainer.scoring import CRITERIA_KEYS


def test_three_mvp_personas(content):
    assert set(content.personas) == {"purchaser_price", "ecologist_non_dm", "silent_after_kp"}
    for p in content.personas.values():
        assert set(p.difficulty) == {1, 2, 3}
        assert p.objections and p.hidden_needs


def test_rubric_matches_review_schema(content):
    assert [c.key for c in content.rubric.criteria] == list(CRITERIA_KEYS)
    assert abs(sum(c.weight for c in content.rubric.criteria) - 1.0) < 1e-9


def test_persona_prompt_fully_filled(content):
    for persona in content.personas.values():
        for lang in LANGUAGES:
            prompt = persona_system_prompt(content, persona, lang, 2)
            assert "{{" not in prompt
            assert persona.name in prompt
            assert LANGUAGES[lang]["instruction"] in prompt


def test_review_prompt_contains_transcript(content):
    persona = content.personas["silent_after_kp"]
    system, prompt = review_prompts(
        content, persona, "uz_latn", 3, "hung_up", [("seller", "Salom!"), ("persona", "Salom")]
    )
    assert "{{" not in system
    assert "ПРОДАВЕЦ: Salom!" in prompt and "КЛИЕНТ: Salom" in prompt
    assert "клиент прекратил разговор" in system


def test_parse_markers():
    assert parse_markers("До свидания. <<HANGUP>>") == ("До свидания.", "hung_up")
    assert parse_markers("Договорились <<AGREED>>") == ("Договорились", "agreed")
    assert parse_markers("Слушаю вас") == ("Слушаю вас", None)
