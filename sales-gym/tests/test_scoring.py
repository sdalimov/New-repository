from app.trainer.scoring import ReviewDraft, clamp_score, finalize_review, seller_stats


def draft(**overrides) -> ReviewDraft:
    base = dict(
        score_needs=8,
        score_value=8,
        score_objections=8,
        score_close=8,
        ethics_violation=False,
        ethics_quote="",
        next_step_with_date=True,
        rephrasings=[{"said": f"фраза {i}", "better": "лучше", "why": "потому"} for i in range(4)],
        strengths=["a", "b", "c"],
        summary=" вывод ",
    )
    base.update(overrides)
    return ReviewDraft(**base)


def test_overall_is_weighted_average(content):
    r = finalize_review(draft(score_needs=6, score_value=8, score_objections=7, score_close=9), content.rubric, [])
    assert r.overall == 7.5
    assert r.caps_applied == []


def test_ethics_violation_caps_overall(content):
    r = finalize_review(
        draft(ethics_violation=True, ethics_quote="Гарантирую экономию 30%"), content.rubric, []
    )
    assert r.overall == content.rubric.ethics_cap == 4
    assert r.ethics_quote == "Гарантирую экономию 30%"
    assert any("этик" in c.lower() or "аудит" in c for c in r.caps_applied)


def test_ethics_cap_does_not_raise_low_score(content):
    r = finalize_review(
        draft(score_needs=2, score_value=2, score_objections=2, score_close=2, ethics_violation=True),
        content.rubric,
        [],
    )
    assert r.overall == 2.0


def test_quote_dropped_without_violation(content):
    r = finalize_review(draft(ethics_quote="мусор"), content.rubric, [])
    assert r.ethics_quote == ""


def test_no_dated_step_caps_close(content):
    r = finalize_review(draft(score_close=9, next_step_with_date=False), content.rubric, [])
    assert r.scores["close"] == content.rubric.no_dated_step_close_cap == 6
    assert r.overall == 7.5  # (8+8+8+6)/4


def test_close_below_cap_untouched(content):
    r = finalize_review(draft(score_close=3, next_step_with_date=False), content.rubric, [])
    assert r.scores["close"] == 3
    assert r.caps_applied == []


def test_scores_clamped_and_lists_trimmed(content):
    r = finalize_review(draft(score_needs=15, score_value=0), content.rubric, [])
    assert r.scores["needs"] == 10 and r.scores["value"] == 1
    assert len(r.rephrasings) == 3
    assert len(r.strengths) == 2
    assert r.summary == "вывод"


def test_clamp_score():
    assert [clamp_score(x) for x in (-3, 1, 5, 10, 99)] == [1, 1, 5, 10, 10]


def test_seller_stats():
    ratio, words = seller_stats(["Как у вас с накипью?", "Мы лучшие на рынке", "Когда удобно встретиться?", "Ок"])
    assert ratio == 0.5
    assert words == (5 + 4 + 3 + 1) / 4


def test_seller_stats_empty():
    assert seller_stats([]) == (0.0, 0.0)
