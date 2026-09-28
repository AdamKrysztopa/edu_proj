import json
from dataclasses import asdict

from fakes import FakeAnthropic, FakeClock, FakeResponse, FakeTranscriber, fake_backends, turn_payload
from probe_app.config import INSTRUMENT_DIR, current_config, load_problems, load_prompt, load_stems
from probe_app.llm import Guard
from probe_app.models import DialogueTurn, GuardVerdict
from probe_app.session import Deps, Session, SessionState
from probe_code.export import export_leading, read_csv
from probe_code.guard_audit import config_drift, guard_audit, leading_by_arm
from probe_code.loader import load_session
from test_export import make_session
from test_session import new_session, seg, through_think_aloud

SCRIPT = INSTRUMENT_DIR / "human-script.md"


def _guard_definition() -> str:
    return next(p for p in load_prompt("guard_system.md").split("\n\n") if p.startswith("A question is leading if"))


def test_human_script_states_the_guard_rule_verbatim():
    assert _guard_definition().strip() in SCRIPT.read_text()


def test_guard_prompt_holds_no_rule_beyond_the_shared_definition():
    paragraphs = [p for p in load_prompt("guard_system.md").split("\n\n") if p.strip()]
    assert len(paragraphs) == 3, "a rule added to the guard prompt must also go into human-script.md"


def test_human_script_uses_the_frozen_stems_verbatim():
    script = SCRIPT.read_text()
    assert all(text in script for text in load_stems().values())


def test_console_human_panel_states_the_rule():
    assert "has not said" in (INSTRUMENT_DIR / "web" / "console.html").read_text()


def _statements() -> dict[str, str]:
    return {k: v["statement"] for k, v in load_problems()["problems"].items()}


class Recorder:
    def __init__(self):
        self.calls = []

    def check(self, *args):
        self.calls.append(args)
        return GuardVerdict(flagged=False, introduced="")


def test_audit_gives_the_guard_the_inputs_it_had_live(tmp_path, monkeypatch):
    live = []

    class LiveGuard(Guard):
        def check(self, *args):
            live.append(args)
            return super().check(*args)

    monkeypatch.setattr("probe_app.session.Guard", LiveGuard)
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1 talk"), seg("A2 talk"), seg("B1 talk"), seg("B2 talk"), seg("They stick.")])
    through_think_aloud(s)
    s.start_probe()
    s.answer_ai_audio(1, b"answer")
    audit = Recorder()
    guard_audit([load_session(s.store.dir)], audit, _statements())
    assert len(live) == 2 and audit.calls == live


def _with_fallback_and_fillers(path):
    state = SessionState.model_validate_json((path / "state.json").read_text())
    state.dialogue["A"].append(DialogueTurn(speaker="interviewer", text="FALLBACK STEM", t=2, source="ai_fallback"))
    state.dialogue["B"][0].text = "Um, so, uh, SECRET HUMAN QUESTION"
    (path / "state.json").write_text(state.model_dump_json())
    return path


def test_leading_export_hides_arm_and_carries_the_guard_context(tmp_path):
    sessions = [load_session(_with_fallback_and_fillers(make_session(tmp_path, n))) for n in ("E01", "E02")]
    statements = {p: f"statement {p}" for p in ("A1", "A2", "B1", "B2")}
    out = tmp_path / "leading"
    export_leading(sessions, out, seed=1, statements=statements)
    rows = read_csv(out / "leading_items.csv")
    key = {r["item_id"]: r for r in read_csv(out / "key_leading.csv")}
    assert list(rows[0]) == ["item_id", "problems", "expert_said", "question", "leading", "introduced", "arm_guess"]
    assert len(rows) == 4 and set(key) - {r["item_id"] for r in rows} == {
        k for k, r in key.items() if r["source"] == "ai_fallback"}
    assert {r["preset_leading"] for r in key.values() if r["source"] == "ai_fallback"} == {"0"}
    assert {key[r["item_id"]]["arm"] for r in rows} == {"ai", "human"}
    assert "FALLBACK" not in (out / "leading_items.csv").read_text()
    ai = next(r for r in rows if r["question"] == "SECRET AI QUESTION")
    human = next(r for r in rows if key[r["item_id"]]["arm"] == "human")
    assert human["question"] == "so, SECRET HUMAN QUESTION"
    assert ai["expert_said"] == "Energy first." and ai["problems"] == "A1: statement A1\nA2: statement A2"
    assert human["expert_said"] == "" and ai["leading"] == ""
    audit = Recorder()
    guard_audit(sessions[:1], audit, statements)
    assert ("SECRET AI QUESTION", ai["problems"], ai["expert_said"]) in audit.calls


def test_audit_refuses_a_session_whose_frozen_config_has_changed(tmp_path, monkeypatch):
    path = make_session(tmp_path, "E01")
    manifest = json.loads((path / "manifest.json").read_text())
    manifest["config"] = asdict(current_config())
    (path / "manifest.json").write_text(json.dumps(manifest))
    assert config_drift(load_session(path)) == []
    manifest["config"]["guard_prompt_sha256"] = "0" * 64
    (path / "manifest.json").write_text(json.dumps(manifest))
    assert config_drift(load_session(path)) == ["guard_prompt_sha256"]


def test_leading_by_arm_unblinds_coder_labels(tmp_path):
    key = [{"item_id": "i1", "arm": "ai", "preset_leading": ""}, {"item_id": "i2", "arm": "ai", "preset_leading": ""},
           {"item_id": "i3", "arm": "human", "preset_leading": ""}, {"item_id": "i4", "arm": "ai", "preset_leading": "0"}]
    labels = {"i1": "1", "i2": "0", "i3": "yes"}
    assert leading_by_arm(labels, key) == {"ai": {"leading": 1, "coded": 3}, "human": {"leading": 1, "coded": 1}}


class SlowAnthropic(FakeAnthropic):
    def __init__(self, clock, seconds, **queues):
        super().__init__(**queues)
        self.clock, self.seconds = clock, seconds

    def create(self, **kwargs):
        self.clock.advance(self.seconds)
        return super().create(**kwargs)


def test_rejected_attempts_are_logged_and_their_time_counts_against_the_cap(tmp_path):
    clock = FakeClock()
    client = SlowAnthropic(clock, 5, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload())],
                           guard=[FakeResponse({"flagged": True, "introduced": "units"})])
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2")]), fake_backends(client))
    s = Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                       set_order=["A", "B"], pilot=True, clock=clock)
    through_think_aloud(s)
    s.start_probe()
    rejected = [e for e in s.store.events() if e["type"] == "turn_rejected"]
    assert len(rejected) == 1 and rejected[0]["reason"].startswith("leading")
    assert s.elapsed() == 20
    clock.advance(1180)
    assert s.enforce_cap()


def test_a_turn_finished_after_the_cap_is_never_shown(tmp_path):
    clock = FakeClock()
    client = SlowAnthropic(clock, 5, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))])
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("They stick.")]), fake_backends(client))
    s = Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                       set_order=["A", "B"], pilot=True, clock=clock)
    through_think_aloud(s)
    s.start_probe()
    clock.advance(1185)
    s.answer_ai_audio(1, b"answer")
    assert [t.speaker for t in s.state.dialogue["A"]] == ["interviewer", "expert"]
    events = s.store.events()
    assert sum(e["type"] == "probe" for e in events) == 1
    late = next(e for e in events if e["type"] == "cap_reached")
    assert late["discarded"]["stem_id"] == "checks" and late["source"] == "ai" and s.state.phase == "trace_review"
