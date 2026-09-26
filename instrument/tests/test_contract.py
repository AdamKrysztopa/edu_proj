import pytest

from probe_app.contract import (ContractState, ContractViolation, check_turn, next_fallback,
                                normalize, record, uncovered)
from probe_app.models import STEMS, Anchor, InterviewerTurn, Segment

SEGS = [Segment(id="A1-s001", problem_id="A1", start=0, end=1, text="It's obviously not elastic."),
        Segment(id="A2-s001", problem_id="A2", start=0, end=1, text="Bullet sticks.")]
EXPERT = " ".join(s.text for s in SEGS)


def turn(**kw) -> InterviewerTurn:
    base = dict(utterance="q", stem_id="cues", problem_id="A1",
                anchor=Anchor(kind="segments", segment_ids=["A1-s001"]),
                is_followup=False, quoted_span=None, end_session=False)
    base.update(kw)
    return InterviewerTurn(**base)


@pytest.fixture
def state() -> ContractState:
    return ContractState(problems=["A1", "A2"])


def test_primary_turn_passes(state):
    check_turn(turn(), state, SEGS, EXPERT)


def test_unknown_problem_rejected(state):
    with pytest.raises(ContractViolation, match="problem"):
        check_turn(turn(problem_id="B1"), state, SEGS, EXPERT)


def test_anchor_segment_from_other_problem_rejected(state):
    with pytest.raises(ContractViolation, match="anchor"):
        check_turn(turn(anchor=Anchor(kind="segments", segment_ids=["A2-s001"])), state, SEGS, EXPERT)


def test_empty_segment_anchor_rejected(state):
    with pytest.raises(ContractViolation, match="anchor"):
        check_turn(turn(anchor=Anchor(kind="segments", segment_ids=[])), state, SEGS, EXPERT)


def test_followup_must_follow_its_primary(state):
    with pytest.raises(ContractViolation, match="follow"):
        check_turn(turn(is_followup=True, quoted_span="not elastic"), state, SEGS, EXPERT)


def test_one_followup_only(state):
    record(turn(), state)
    fu = turn(is_followup=True, quoted_span="not elastic")
    check_turn(fu, state, SEGS, EXPERT)
    record(fu, state)
    with pytest.raises(ContractViolation, match="second follow-up"):
        check_turn(fu, state, SEGS, EXPERT)


def test_followup_quote_must_be_experts_words(state):
    record(turn(), state)
    with pytest.raises(ContractViolation, match="quoted"):
        check_turn(turn(is_followup=True, quoted_span="momentum is conserved"), state, SEGS, EXPERT)


def test_followup_quote_matches_despite_curly_quotes_and_case(state):
    record(turn(), state)
    check_turn(turn(is_followup=True, quoted_span="“It’s OBVIOUSLY not elastic”"), state, SEGS, EXPERT)


def test_end_session_needs_full_coverage(state):
    with pytest.raises(ContractViolation, match="coverage"):
        check_turn(turn(end_session=True), state, SEGS, EXPERT)
    for p in ("A1", "A2"):
        for s in STEMS:
            record(turn(problem_id=p, stem_id=s, anchor=Anchor(kind="none", segment_ids=[])), state)
    check_turn(turn(end_session=True), state, SEGS, EXPERT)


def test_uncovered_and_fallback_order(state):
    assert len(uncovered(state)) == 10
    record(turn(stem_id="cues"), state)
    assert "A1/cues" not in uncovered(state)
    assert next_fallback(state) == ("A1", "alternatives")


def test_normalize():
    assert normalize("  “It’s”  OK!! ") == "it s ok"
