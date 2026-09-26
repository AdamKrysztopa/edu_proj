import pytest

from fakes import FakeAnthropic, FakeClock, FakeResponse, FakeTranscriber, turn_payload
from probe_app.config import ConfigMismatch
from probe_app.models import Anchor
from probe_app.session import Deps, DuplicateSubmission, PhaseError, Session
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")


def seg(text, start=0.0):
    return [RawSegment(start=start, end=start + 1, text=text)]


def new_session(tmp_path, interviewer=(), transcripts=(), arms=None, clock=None):
    deps = Deps(FakeTranscriber(list(transcripts)), FakeAnthropic(interviewer=list(interviewer)))
    return Session.create(tmp_path, deps, expert_id="E01", cell=1, arms=arms or {"A": "ai", "B": "human"},
                          set_order=["A", "B"], pilot=True, clock=clock or FakeClock())


def through_think_aloud(s):
    while s.state.phase == "ready":
        pid = s.start_think_aloud()
        s.end_think_aloud(pid, b"audio", PNG, [{"points": [[0, 0, 0]]}])


def test_think_aloud_order_and_trace(tmp_path):
    s = new_session(tmp_path, transcripts=[seg("A1 talk"), seg("A2 talk"), seg("B1 talk"), seg("B2 talk")])
    through_think_aloud(s)
    assert s.state.think_aloud_done == ["A1", "A2", "B1", "B2"]
    assert s.state.phase == "trace_review"
    assert [x.id for x in s.state.segments][:2] == ["A1-s001", "A2-s001"]
    assert s.snapshot_path("A1").read_bytes() == PNG


def test_data_session_refuses_without_prereg(tmp_path, monkeypatch):
    monkeypatch.setattr("probe_app.session.PREREG_PATH", tmp_path / "none.json")
    deps = Deps(FakeTranscriber([]), FakeAnthropic())
    with pytest.raises(ConfigMismatch):
        Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                       set_order=["A", "B"], pilot=False)


def test_failed_transcription_sets_error_and_allows_typing(tmp_path):
    s = new_session(tmp_path, transcripts=[RuntimeError("x")] * 3 + [seg("A2"), seg("B1"), seg("B2")])
    pid = s.start_think_aloud()
    s.end_think_aloud(pid, b"a", PNG, [])
    assert "A1" in s.state.error
    s.add_segment("A1", "typed transcript")
    assert s.state.segments[-1].id == "A1-m001" and s.state.error is None


def test_ai_probe_flow_and_duplicate_answer(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("Because they stick.")], clock=clock)
    through_think_aloud(s)
    assert s.start_probe() == "A"
    view = s.expert_view()
    assert view["question"] == "What did you notice first?" and view["expected_answer_index"] == 1
    clock.advance(30)
    s.answer_ai_audio(1, b"answer")
    d = s.state.dialogue["A"]
    assert [x.speaker for x in d] == ["interviewer", "expert", "interviewer"]
    assert d[1].text == "Because they stick." and d[1].t == 30
    with pytest.raises(DuplicateSubmission):
        s.answer_ai_audio(1, b"answer")
    assert len(s.state.dialogue["A"]) == 3


def test_silent_answer_passes_empty_text(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"), []])
    through_think_aloud(s)
    s.start_probe()
    s.answer_ai_audio(1, b"silence")
    assert s.state.dialogue["A"][1].text == ""
    assert s.state.dialogue["A"][2].stem_id == "checks"


def test_failed_answer_transcription_waits_for_typed_answer(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")] + [RuntimeError("x")] * 3)
    through_think_aloud(s)
    s.start_probe()
    s.answer_ai_audio(1, b"a")
    assert len(s.state.dialogue["A"]) == 1 and "type it" in s.state.error
    s.answer_ai_text(1, "I saw they stick.")
    assert s.state.dialogue["A"][1].source == "typed" and len(s.state.dialogue["A"]) == 3


def test_reload_resumes_same_question(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    s.start_probe()
    again = Session.load(tmp_path, s.store.session_id, s.deps)
    assert again.expert_view()["question"] == s.expert_view()["question"]
    assert again.state.contract["A"].used == {"A1/cues": 1}


def test_pause_stops_timer(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")], clock=clock)
    through_think_aloud(s)
    s.start_probe()
    clock.advance(10); s.pause(); clock.advance(100); s.resume(); clock.advance(5)
    assert s.elapsed() == 15


def test_human_arm_markers_upload_and_finish(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, arms={"A": "human", "B": "ai"}, clock=clock,
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"),
                                 [RawSegment(start=0.2, end=1, text="What did you see?"),
                                  RawSegment(start=2, end=3, text="The stick.")]])
    through_think_aloud(s)
    s.start_probe()
    s.human_marker("interviewer"); s.human_stem("A1", "cues")
    clock.advance(1.5); s.human_marker("expert")
    s.push_anchor("A1", Anchor(kind="segments", segment_ids=["A1-s001"]))
    assert s.expert_view()["anchor_view"]["text"] == "A1"
    with pytest.raises(PhaseError):
        s.answer_ai_text(0, "x")
    s.end_probe()
    assert s.state.phase == "probe_uploading"
    s.upload_human_probe("A", b"audio")
    assert [x.speaker for x in s.state.dialogue["A"]] == ["interviewer", "expert"]
    assert s.state.dialogue["A"][0].stem_id == "cues"
    assert s.state.phase == "trace_review" and s.state.probes_done == ["A"]
