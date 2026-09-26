import json

import pytest

from fakes import TEST_MODELS, FakeAnthropic, FakeClock, FakeOpenAI, FakeResponse, FakeTranscriber, fake_backends, turn_payload
from probe_app.backends import AnthropicBackend, Backends, OpenAICompatBackend
from probe_app.config import ConfigMismatch, RoleModel
from probe_app.models import Anchor
from probe_app.session import Deps, DuplicateSubmission, PhaseError, Session
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")


def seg(text, start=0.0):
    return [RawSegment(start=start, end=start + 1, text=text)]


def new_session(tmp_path, interviewer=(), transcripts=(), arms=None, clock=None):
    deps = Deps(FakeTranscriber(list(transcripts)), fake_backends(FakeAnthropic(interviewer=list(interviewer))))
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
    deps = Deps(FakeTranscriber([]), fake_backends(FakeAnthropic()))
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
    s.finalize_human_probe(b"audio")
    assert [x.speaker for x in s.state.dialogue["A"]] == ["interviewer", "expert"]
    assert s.state.dialogue["A"][0].stem_id == "cues"
    assert s.state.phase == "trace_review" and s.state.probes_done == ["A"]


def test_trace_of_a_probed_set_is_locked(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(end_session=False, stem_id="checks"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    s.start_probe()
    s.end_probe()
    assert s.state.phase == "trace_review"
    with pytest.raises(PhaseError, match="locked"):
        s.correct_segment("A1-s001", "changed after the probe")
    with pytest.raises(PhaseError, match="locked"):
        s.add_segment("A2", "added after the probe")
    s.correct_segment("B1-s001", "set B is not probed yet")


def test_probe_waits_for_failed_transcripts_of_its_set(tmp_path):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[RuntimeError("x")] * 3 + [seg("A2")] + [RuntimeError("y")] * 3 + [seg("B2")])
    through_think_aloud(s)
    assert s.state.untranscribed == ["A1", "B1"]
    with pytest.raises(PhaseError, match="A1"):
        s.start_probe()
    s.add_segment("A1", "typed")
    assert s.state.untranscribed == ["B1"]
    assert s.start_probe() == "A"


def test_prompt_edited_after_creation_blocks_the_probe(tmp_path, monkeypatch):
    s = new_session(tmp_path, interviewer=[FakeResponse(turn_payload())],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    from probe_app import config
    real = config.current_config()
    monkeypatch.setattr("probe_app.session.current_config",
                        lambda: config.FrozenConfig(**{**real.__dict__, "system_prompt_sha256": "edited"}))
    with pytest.raises(ConfigMismatch, match="system_prompt_sha256"):
        s.start_probe()


def test_data_session_refuses_uncommitted_instrument_changes(tmp_path, monkeypatch):
    from probe_app import config
    prereg = tmp_path / "prereg.json"
    config.freeze(config.current_config(), prereg)
    monkeypatch.setattr("probe_app.session.PREREG_PATH", prereg)
    monkeypatch.setattr("probe_app.session.git_dirty", lambda: True)
    deps = Deps(FakeTranscriber([]), fake_backends(FakeAnthropic()))
    with pytest.raises(ConfigMismatch, match="uncommitted"):
        Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                       set_order=["A", "B"], pilot=False)
    pilot = Session.create(tmp_path, deps, expert_id="E02", cell=1, arms={"A": "ai", "B": "human"},
                           set_order=["A", "B"], pilot=True)
    assert pilot.manifest["git_dirty"] is True


def test_think_aloud_audio_streams_in_parts_across_a_reload(tmp_path):
    clock = FakeClock(10.0)
    s = new_session(tmp_path, transcripts=[seg("before reload", 0.0), seg("after reload", 1.0)], clock=clock)
    pid = s.start_think_aloud()
    clock.advance(0.5)
    part = s.recording_start(f"think_{pid}")
    s.recording_chunk(f"think_{pid}", part, 0, b"aa")
    s.recording_chunk(f"think_{pid}", part, 0, b"aa")
    s.recording_chunk(f"think_{pid}", part, 1, b"bb")
    clock.advance(30)
    part2 = s.recording_start(f"think_{pid}")
    s.recording_chunk(f"think_{pid}", part2, 0, b"cc")
    s.end_think_aloud(pid, None, PNG, [])
    assert s.store.path(f"audio/think_{pid}.part1.webm").read_bytes() == b"aabb"
    assert [(x.text, x.start) for x in s.state.segments] == [("before reload", 10.5), ("after reload", 41.5)]


def test_chunk_gap_is_recorded_once_and_reported_on_the_console(tmp_path):
    s = new_session(tmp_path)
    pid = s.start_think_aloud()
    stream = f"think_{pid}"
    part = s.recording_start(stream)
    assert s.recording_chunk(stream, part, 1, b"x") is True
    assert s.recording_chunk(stream, part, 2, b"y") is True
    assert s.state.recordings[stream][0]["gap_at"] == 0
    assert "gap" in s.console_view()["state"]["error"]
    assert not s.store.path(f"audio/{stream}.part{part}.webm").exists()
    assert [e["type"] for e in s.store.events()].count("chunk_refused") == 1


@pytest.mark.parametrize("audio, transcript", [(None, []), (b"silence", [[]])])
def test_think_aloud_without_speech_waits_for_typing(tmp_path, audio, transcript):
    s = new_session(tmp_path, transcripts=transcript)
    pid = s.start_think_aloud()
    s.end_think_aloud(pid, audio, PNG, [])
    assert pid in s.state.untranscribed and pid in s.state.error


def test_human_probe_without_speech_sets_error(tmp_path):
    s = new_session(tmp_path, arms={"A": "human", "B": "ai"},
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    s.start_probe()
    s.end_probe()
    s.finalize_human_probe()
    assert "set A" in s.state.error


def test_human_arm_uses_one_clock_despite_recorder_lag_and_pause(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, arms={"A": "human", "B": "ai"}, clock=clock,
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"),
                                 [RawSegment(start=99.1, end=101.0, text="What did you look at first?"),
                                  RawSegment(start=409.5, end=412.0, text="The masses.")]])
    through_think_aloud(s)
    s.start_probe()
    clock.advance(0.6)
    part = s.recording_start("probe_A")
    s.recording_chunk("probe_A", part, 0, b"audio")
    clock.advance(99.4); s.human_marker("interviewer"); s.human_stem("A1", "cues")
    clock.advance(10); s.pause(); clock.advance(300); s.resume()
    clock.advance(0); s.human_marker("expert")
    s.end_probe()
    s.finalize_human_probe()
    assert [(x.speaker, x.stem_id) for x in s.state.dialogue["A"]] == [("interviewer", "cues"), ("expert", None)]


def test_cap_ends_both_arms_on_the_clock(tmp_path):
    clock = FakeClock()
    s = new_session(tmp_path, arms={"A": "human", "B": "ai"}, clock=clock,
                    interviewer=[FakeResponse(turn_payload(problem_id="B1"))],
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2")])
    through_think_aloud(s)
    s.start_probe()
    clock.advance(1199)
    assert not s.enforce_cap()
    clock.advance(1)
    assert s.enforce_cap() and s.state.phase == "probe_uploading"
    s.finalize_human_probe()
    s.start_probe()
    clock.advance(1200)
    assert s.enforce_cap() and s.state.phase == "done"


def _other_backends():
    client = FakeAnthropic()
    return Backends(interviewer=AnthropicBackend(client, RoleModel(provider="anthropic", model="claude-other")),
                    guard=AnthropicBackend(client, TEST_MODELS.guard))


def test_session_refused_when_backends_differ_from_models_json(tmp_path):
    root = tmp_path / "sessions"
    deps = Deps(FakeTranscriber([]), _other_backends())
    with pytest.raises(ConfigMismatch, match=r"\(interviewer\): restart probe-app serve"):
        Session.create(root, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                       set_order=["A", "B"], pilot=True)
    assert not root.exists()


def test_session_refused_when_transcriber_differs_from_models_json(tmp_path):
    transcriber = FakeTranscriber([])
    transcriber.model = "whisper-1"
    with pytest.raises(ConfigMismatch, match=r"\(transcriber\)"):
        Session.create(tmp_path, Deps(transcriber, fake_backends(FakeAnthropic())), expert_id="E01", cell=1,
                       arms={"A": "ai", "B": "human"}, set_order=["A", "B"], pilot=True)


def test_models_json_edit_mid_session_stops_the_next_probe(tmp_path, test_models_file):
    s = new_session(tmp_path)
    s._check_config()
    edited = json.loads(test_models_file.read_text())
    edited["guard"]["model"] = "claude-other"
    test_models_file.write_text(json.dumps(edited))
    with pytest.raises(ConfigMismatch):
        s._check_config()


def test_resumed_session_refused_when_server_backends_differ_from_models_json(tmp_path):
    s = new_session(tmp_path)
    resumed = Session.load(tmp_path, s.store.session_id, Deps(FakeTranscriber([]), _other_backends()))
    with pytest.raises(ConfigMismatch, match="restart probe-app serve"):
        resumed._check_config()


@pytest.mark.parametrize("route, refusal", [(None, "route"), (["openai"], "freeze")])
def test_data_session_on_openrouter_needs_a_route(tmp_path, monkeypatch, test_models_file, route, refusal):
    monkeypatch.setattr("probe_app.session.PREREG_PATH", tmp_path / "none.json")
    role = RoleModel(provider="openrouter", model="openai/x", route=route)
    test_models_file.write_text(TEST_MODELS.model_copy(update={"interviewer": role}).model_dump_json())
    backends = Backends(interviewer=OpenAICompatBackend(FakeOpenAI([]), role),
                        guard=AnthropicBackend(FakeAnthropic(), TEST_MODELS.guard))
    with pytest.raises(ConfigMismatch, match=refusal):
        Session.create(tmp_path / "sessions", Deps(FakeTranscriber([]), backends), expert_id="E01", cell=1,
                       arms={"A": "ai", "B": "human"}, set_order=["A", "B"], pilot=False)
