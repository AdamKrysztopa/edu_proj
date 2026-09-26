from probe_app.config import load_stems
from probe_app.contract import ContractState
from probe_app.engine import ProbeContext, ProbeEngine
from probe_app.llm import LLMRefused, LLMUnavailable
from probe_app.models import STEMS, Anchor, DialogueTurn, GuardVerdict, InterviewerTurn, Segment
from probe_app.storage import SessionStore

SEGS = [Segment(id="A1-s001", problem_id="A1", start=0, end=1, text="Clearly they stick together.")]


class ScriptedLLM:
    def __init__(self, items):
        self.items, self.requests = list(items), []

    def next_turn(self, req):
        self.requests.append(req)
        item = self.items.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


class ScriptedGuard:
    def __init__(self, flags=()):
        self.flags = list(flags)

    def check(self, utterance, problem_text, expert_text):
        flagged = self.flags.pop(0) if self.flags else False
        return GuardVerdict(flagged=flagged, introduced="units" if flagged else "")


def t(**kw) -> InterviewerTurn:
    base = dict(utterance="What did you notice?", stem_id="cues", problem_id="A1",
                anchor=Anchor(kind="segments", segment_ids=["A1-s001"]),
                is_followup=False, quoted_span=None, end_session=False)
    base.update(kw)
    return InterviewerTurn(**base)


def make(tmp_path, llm, guard=None, segments=SEGS, problems=("A1",)):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    ctx = ProbeContext(set_id="A", problems={p: f"statement {p}" for p in problems},
                       segments=segments, snapshots={})
    contract = ContractState(problems=list(problems))
    engine = ProbeEngine(llm, guard or ScriptedGuard(), load_stems(), ctx, store, contract, cap_s=1200, wrap_s=1080)
    return engine, store, contract


def types(store):
    return [e["type"] for e in store.events()]


def test_valid_turn_is_emitted_and_recorded(tmp_path):
    engine, store, contract = make(tmp_path, ScriptedLLM([t()]))
    out = engine.next_turn([], 0.0)
    assert out.source == "ai" and out.stem_id == "cues"
    assert contract.used == {"A1/cues": 1}
    assert "probe" in types(store)


def test_contract_violation_regenerates_with_reason(tmp_path):
    llm = ScriptedLLM([t(problem_id="B9"), t()])
    engine, store, _ = make(tmp_path, llm)
    out = engine.next_turn([], 0.0)
    assert out.source == "ai"
    assert "problem B9" in llm.requests[1].rejection
    assert types(store).count("turn_rejected") == 1


def test_guard_flag_twice_falls_back_to_bare_stem(tmp_path):
    engine, store, contract = make(tmp_path, ScriptedLLM([t(), t()]), ScriptedGuard([True, True]))
    out = engine.next_turn([], 0.0)
    assert out.source == "ai_fallback"
    assert out.text == load_stems()["cues"]
    assert out.anchor.kind == "none"
    assert types(store).count("turn_rejected") == 2


def test_refusal_and_outage_fall_back(tmp_path):
    for exc in (LLMRefused("r"), LLMUnavailable("u")):
        engine, _, _ = make(tmp_path / type(exc).__name__, ScriptedLLM([exc]))
        assert engine.next_turn([], 0.0).source == "ai_fallback"


def test_cap_ends_session(tmp_path):
    engine, store, _ = make(tmp_path, ScriptedLLM([]))
    assert engine.next_turn([], 1200.0) is None
    assert "cap_reached" in types(store)


def test_wrap_up_flag_from_1080s(tmp_path):
    llm = ScriptedLLM([t(), t(stem_id="checks")])
    engine, _, _ = make(tmp_path, llm)
    engine.next_turn([], 1079.0)
    engine.next_turn([], 1080.0)
    assert [r.wrap_up for r in llm.requests] == [False, True]


def test_end_session_after_coverage(tmp_path):
    turns = [t(stem_id=s, anchor=Anchor(kind="none", segment_ids=[])) for s in STEMS] + [t(end_session=True)]
    engine, store, _ = make(tmp_path, ScriptedLLM(turns))
    for _ in STEMS:
        assert engine.next_turn([], 0.0) is not None
    assert engine.next_turn([], 0.0) is None
    assert "session_ended_by_interviewer" in types(store)


def test_followup_quote_checked_against_answers(tmp_path):
    answer = DialogueTurn(speaker="expert", text="I just knew it was inelastic.", t=5.0)
    fu = t(is_followup=True, quoted_span="just knew it was inelastic")
    engine, _, _ = make(tmp_path, ScriptedLLM([t(), fu]))
    first = engine.next_turn([], 0.0)
    assert engine.next_turn([first, answer], 10.0).is_followup


def test_runs_with_empty_trace_and_empty_answer(tmp_path):
    canvas = t(anchor=Anchor(kind="canvas", segment_ids=[]))
    later = t(stem_id="checks", anchor=Anchor(kind="canvas", segment_ids=[]))
    engine, _, _ = make(tmp_path, ScriptedLLM([canvas, later]), segments=[])
    first = engine.next_turn([], 0.0)
    silent = DialogueTurn(speaker="expert", text="", t=4.0)
    assert engine.next_turn([first, silent], 8.0).stem_id == "checks"
