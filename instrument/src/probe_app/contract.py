import re
import unicodedata

from pydantic import BaseModel

from probe_app.models import STEMS, InterviewerTurn, Segment


class ContractViolation(Exception):
    pass


class ContractState(BaseModel):
    problems: list[str]
    used: dict[str, int] = {}
    last_primary: str | None = None
    last_primary_followed: bool = False


def _key(problem_id: str, stem_id: str) -> str:
    return f"{problem_id}/{stem_id}"


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    return " ".join(re.sub(r"[^\w\s]", " ", text).split())


def uncovered(state: ContractState) -> list[str]:
    return [_key(p, s) for p in state.problems for s in STEMS if state.used.get(_key(p, s), 0) == 0]


def next_fallback(state: ContractState) -> tuple[str, str] | None:
    missing = uncovered(state)
    if not missing:
        return None
    problem_id, stem_id = missing[0].split("/")
    return problem_id, stem_id


def check_turn(turn: InterviewerTurn, state: ContractState, segments: list[Segment], expert_text: str) -> None:
    if turn.end_session:
        missing = uncovered(state)
        if missing:
            raise ContractViolation(f"end_session before full coverage; unused: {missing}")
        return
    if turn.problem_id not in state.problems:
        raise ContractViolation(f"problem {turn.problem_id} is not in this set {state.problems}")
    if turn.anchor.kind == "segments":
        owner = {s.id: s.problem_id for s in segments}
        bad = [i for i in turn.anchor.segment_ids if owner.get(i) != turn.problem_id]
        if not turn.anchor.segment_ids or bad:
            raise ContractViolation(f"anchor segments must belong to {turn.problem_id}; bad: {bad or 'none given'}")
    if turn.is_followup:
        if state.last_primary != _key(turn.problem_id, turn.stem_id):
            raise ContractViolation("a follow-up must directly follow the stem question it belongs to")
        if state.last_primary_followed:
            raise ContractViolation("second follow-up on the same stem question")
        quote = normalize(turn.quoted_span or "")
        if not quote or quote not in normalize(expert_text):
            raise ContractViolation("quoted_span is not the expert's own words")


def record(turn: InterviewerTurn, state: ContractState) -> None:
    if turn.end_session:
        return
    key = _key(turn.problem_id, turn.stem_id)
    if turn.is_followup:
        state.last_primary_followed = True
        return
    state.used[key] = state.used.get(key, 0) + 1
    state.last_primary = key
    state.last_primary_followed = False
