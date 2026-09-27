from app.bot.trainer_router import chunks
from app.trainer import render
from app.trainer.scoring import FinalReview, Rephrasing


def sample(**kw) -> FinalReview:
    base = dict(
        scores={"needs": 7, "value": 5, "objections": 6, "close": 8},
        overall=6.5,
        ethics_violation=False,
        ethics_quote="",
        next_step_with_date=True,
        question_ratio=0.5,
        avg_words=12.0,
        rephrasings=[Rephrasing(said="Цена <ниже>", better="Сколько стоит простой?", why="Про деньги клиента")],
        strengths=["Хороший первый вопрос"],
        summary="Задавайте больше вопросов.",
    )
    base.update(kw)
    return FinalReview(**base)


def test_review_escapes_html_and_shows_scores():
    text = render.review(sample())
    assert "6.5/10" in text
    assert "&lt;ниже&gt;" in text
    assert "Шаг с датой: ✅ да" in text
    assert "Нарушение этики" not in text


def test_review_shows_ethics_warning():
    text = render.review(sample(ethics_violation=True, ethics_quote="Гарантирую 30%", caps_applied=["cap"]))
    assert "Нарушение этики" in text and "Гарантирую 30%" in text


def test_plain_strips_tags():
    assert render.plain("<b>Разбор</b> &amp; итог") == "Разбор & итог"


def test_briefing(content):
    text = render.briefing(content.personas["silent_after_kp"], "uz_latn", 3)
    assert "узбекский (латиница)" in text and "/end" in text


def test_chunks_split_long_text():
    text = "\n".join(["x" * 100] * 100)
    parts = chunks(text, 1000)
    assert all(len(p) <= 1000 for p in parts)
    assert "".join(parts).replace("\n", "") == text.replace("\n", "")
