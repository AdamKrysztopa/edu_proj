"""Stream invariants (decision 0003, empty-stream-is-an-error): no problem is probed on an incomplete trace
without the console being told. Either the problem is held in `untranscribed` (the human arm: `state.error`)
with an error naming what is missing, or the request is refused with a status the tablet shows."""
import pytest
from fastapi.testclient import TestClient

from fakes import FakeAnthropic, FakeClock, FakeTranscriber, fake_backends
from probe_app.server import create_app
from probe_app.session import Deps, PhaseError, Session
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")
LAPTOP = ("127.0.0.1", 50000)
OCTET = {"Content-Type": "application/octet-stream"}
STREAMS = ["think", "human"]


def seg(text, start=0.0):
    return [RawSegment(start=start, end=start + 1, text=text)]


def open_stream(kind, tmp_path, transcripts=(), clock=None):
    if kind == "think":
        deps = Deps(FakeTranscriber([*transcripts, seg("A2"), seg("B1"), seg("B2")]), fake_backends(FakeAnthropic()))
        s = Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "ai", "B": "human"},
                           set_order=["A", "B"], pilot=True, clock=clock or FakeClock())
        return s, f"think_{s.start_think_aloud()}"
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2"), *transcripts]),
                fake_backends(FakeAnthropic()))
    s = Session.create(tmp_path, deps, expert_id="E01", cell=1, arms={"A": "human", "B": "ai"},
                       set_order=["A", "B"], pilot=True, clock=clock or FakeClock())
    while s.state.phase == "ready":
        s.end_think_aloud(s.start_think_aloud(), b"audio", PNG, [])
    s.start_probe()
    s.human_marker("expert")  # the stream tests are about audio, so their speech is attributed as in a real session
    return s, "probe_A"


def close_stream(s, stream):
    if stream.startswith("think_"):
        s.end_think_aloud(stream.removeprefix("think_"), None, PNG, [])
    else:
        s.end_probe()
        s.finalize_human_probe()


def assert_console_told(s, stream, needle):
    assert needle in s.state.error
    if stream.startswith("think_"):
        pid = stream.removeprefix("think_")
        assert pid in s.state.untranscribed
        while s.state.phase == "ready":
            s.end_think_aloud(s.start_think_aloud(), b"audio", PNG, [])
        with pytest.raises(PhaseError, match="type the transcript"):
            s.start_probe()
    else:
        assert s.state.dialogue["A"] == []


def assert_incomplete(s, stream, transcribed):
    assert f"missing in {stream}" in s.state.error
    if stream.startswith("think_"):
        assert " ".join(x.text for x in s.state.segments) == transcribed
        assert_console_told(s, stream, f"missing in {stream}")
    else:
        assert [x.text for x in s.state.dialogue["A"]] == [transcribed]


def part_file(s, stream, n):
    return s.store.path(f"audio/{stream}.part{n}.webm")


@pytest.mark.parametrize("kind", STREAMS)
def test_stream_never_started_is_reported(tmp_path, kind):
    s, stream = open_stream(kind, tmp_path)
    close_stream(s, stream)
    assert stream not in s.state.recordings
    assert_console_told(s, stream, "no speech")


@pytest.mark.parametrize("kind", STREAMS)
def test_stream_with_no_parts_is_reported(tmp_path, kind):
    s, stream = open_stream(kind, tmp_path)
    with pytest.raises(ValueError, match="unknown part"):
        s.recording_chunk(stream, 1, 0, b"x")
    assert s.state.recordings[stream] == []
    close_stream(s, stream)
    assert_console_told(s, stream, "no speech")


@pytest.mark.parametrize("kind", STREAMS)
def test_missing_part_file_is_reported_by_name(tmp_path, kind):
    s, stream = open_stream(kind, tmp_path)
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"aa")
    part_file(s, stream, part).unlink()
    close_stream(s, stream)
    assert_console_told(s, stream, f"{stream}.part1.webm")


@pytest.mark.parametrize("kind", STREAMS)
def test_missing_later_part_file_is_reported_even_when_others_transcribe(tmp_path, kind):
    clock = FakeClock()
    s, stream = open_stream(kind, tmp_path, transcripts=[seg("first part")], clock=clock)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"aa")
    clock.advance(1)
    part2 = s.recording_start(stream)
    s.recording_chunk(stream, part2, 0, b"bb")
    part_file(s, stream, part2).unlink()
    close_stream(s, stream)
    assert_console_told(s, stream, f"{stream}.part2.webm")


@pytest.mark.parametrize("kind", STREAMS)
def test_part_opened_without_chunks_is_not_an_error(tmp_path, kind):
    clock = FakeClock()
    s, stream = open_stream(kind, tmp_path, transcripts=[seg("spoken")], clock=clock)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"aa")
    clock.advance(1)
    s.recording_start(stream)
    close_stream(s, stream)
    assert s.state.error is None
    if kind == "think":
        assert [x.text for x in s.state.segments] == ["spoken"]
    else:
        assert [x.text for x in s.state.dialogue["A"]] == ["spoken"]


@pytest.mark.parametrize("kind", STREAMS)
def test_missing_chunk_is_refused_and_holds_the_trace_after_assembly(tmp_path, kind):
    s, stream = open_stream(kind, tmp_path, transcripts=[seg("partial")])
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"c0")
    assert s.recording_chunk(stream, part, 2, b"c2") is True
    assert f"gap in {stream} part {part}" in s.console_view()["state"]["error"]
    close_stream(s, stream)
    assert part_file(s, stream, part).read_bytes() == b"c0"
    assert s.state.recordings[stream][0]["gap_at"] == 1
    assert_incomplete(s, stream, "partial")


def test_gap_hold_survives_a_later_failure_and_its_typed_fix(tmp_path):
    s, stream = open_stream("think", tmp_path, transcripts=[seg("A1 partial"), *[RuntimeError("down")] * 3])
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"c0")
    s.recording_chunk(stream, part, 2, b"c2")
    close_stream(s, stream)
    s.end_think_aloud(s.start_think_aloud(), b"audio", PNG, [])
    s.add_segment("A2", "typed A2")
    with pytest.raises(PhaseError, match="A1"):
        while s.state.phase == "ready":
            s.end_think_aloud(s.start_think_aloud(), b"audio", PNG, [])
        s.start_probe()
    s.add_segment("A1", "what the expert said in the gap")
    assert s.state.untranscribed == [] and s.state.error is None


@pytest.mark.parametrize("kind", STREAMS)
def test_out_of_order_chunk_is_reported_and_never_written_out_of_order(tmp_path, kind):
    s, stream = open_stream(kind, tmp_path)
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"c0")
    assert s.recording_chunk(stream, part, 2, b"c2") is True
    assert s.recording_chunk(stream, part, 1, b"c1") is False
    assert s.recording_chunk(stream, part, 3, b"c3") is True
    assert part_file(s, stream, part).read_bytes() == b"c0c1"
    assert f"gap in {stream} part {part}" in s.state.error


@pytest.mark.parametrize("kind", STREAMS)
def test_duplicate_chunk_is_acknowledged_and_written_once(tmp_path, kind):
    s, stream = open_stream(kind, tmp_path)
    part = s.recording_start(stream)
    for seq, data in ((0, b"c0"), (0, b"c0"), (1, b"c1"), (1, b"c1")):
        assert s.recording_chunk(stream, part, seq, data) is False
    assert part_file(s, stream, part).read_bytes() == b"c0c1"
    assert s.state.error is None and "gap_at" not in s.state.recordings[stream][0]


@pytest.mark.parametrize("kind", STREAMS)
def test_gap_forces_a_new_part_on_the_server_clock_and_is_still_reported(tmp_path, kind):
    clock = FakeClock(100.0)
    s, stream = open_stream(kind, tmp_path, transcripts=[seg("before", 0.0), seg("after", 0.5)], clock=clock)
    t0 = clock.now()
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"c0")
    clock.advance(3)
    assert s.recording_chunk(stream, part, 2, b"c2") is True
    part2 = s.recording_start(stream)
    s.recording_chunk(stream, part2, 0, b"d0")
    close_stream(s, stream)
    assert (part_file(s, stream, part).read_bytes(), part_file(s, stream, part2).read_bytes()) == (b"c0", b"d0")
    if kind == "think":
        assert [(x.text, x.start) for x in s.state.segments[-2:]] == [("before", t0), ("after", t0 + 3.5)]
    assert_incomplete(s, stream, "before after")


@pytest.mark.parametrize("kind", STREAMS)
def test_reload_mid_stream_keeps_the_old_part_and_its_late_chunk(tmp_path, kind):
    clock = FakeClock(100.0)
    s, stream = open_stream(kind, tmp_path, transcripts=[seg("old tab", 0.0), seg("new tab", 0.0)], clock=clock)
    t0 = clock.now()
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"c0")
    clock.advance(1.5)
    part2 = s.recording_start(stream)
    s.recording_chunk(stream, part, 1, b"c1")
    s.recording_chunk(stream, part2, 0, b"d0")
    close_stream(s, stream)
    assert part_file(s, stream, part).read_bytes() == b"c0c1"
    assert s.state.error is None
    if kind == "think":
        assert [(x.text, x.start) for x in s.state.segments[-2:]] == [("old tab", t0), ("new tab", t0 + 1.5)]
    else:
        assert [x.text for x in s.state.dialogue["A"]] == ["old tab new tab"]


@pytest.mark.parametrize("kind", STREAMS)
def test_reload_that_drops_unsent_chunks_is_reported(tmp_path, kind):
    clock = FakeClock(100.0)
    s, stream = open_stream(kind, tmp_path, transcripts=[seg("old tab"), seg("new tab")], clock=clock)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"c0")
    clock.advance(8)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"d0")
    assert f"hole in {stream}" in s.state.error
    close_stream(s, stream)
    assert s.state.recordings[stream][0]["hole_s"] == 7.0
    assert_incomplete(s, stream, "old tab new tab")


def test_whole_audio_upload_never_replaces_streamed_parts(tmp_path):
    s, stream = open_stream("think", tmp_path)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"c0")
    with pytest.raises(ValueError, match="streamed"):
        s.end_think_aloud("A1", b"whole", PNG, [])
    assert part_file(s, stream, 1).read_bytes() == b"c0"


def test_reload_while_probe_uploads_still_finalizes_every_part(tmp_path):
    clock = FakeClock()
    s, stream = open_stream("human", tmp_path, transcripts=[seg("one"), seg("two")], clock=clock)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"c0")
    s.end_probe()
    clock.advance(2)
    s.recording_chunk(stream, s.recording_start(stream), 0, b"d0")
    s.finalize_human_probe()
    assert s.state.error is None and [x.text for x in s.state.dialogue["A"]] == ["one two"]


def serve(tmp_path, transcripts):
    deps = Deps(FakeTranscriber(transcripts), fake_backends(FakeAnthropic()))
    c = TestClient(create_app(tmp_path, deps, FakeClock()), client=LAPTOP)
    sid = c.post("/api/sessions", json={"expert_id": "E01", "cell": 1, "set_order": ["A", "B"],
                                        "arms": {"A": "human", "B": "ai"}, "pilot": True}).json()["session_id"]
    return c, sid


def chunk(c, sid, stream, part, seq, data=b"xx"):
    return c.post(f"/api/sessions/{sid}/recording/chunk", params={"stream": stream, "part": part, "seq": seq},
                  content=data, headers=OCTET)


def think_aloud(c, sid, pid):
    c.post(f"/api/sessions/{sid}/think-aloud/start")
    part = c.post(f"/api/sessions/{sid}/recording/start", json={"stream": f"think_{pid}"}).json()["part"]
    assert chunk(c, sid, f"think_{pid}", part, 0).status_code == 200
    r = c.post(f"/api/sessions/{sid}/think-aloud/{pid}/end",
               files={"snapshot": ("s.png", PNG, "image/png")}, data={"strokes": "[]"})
    assert r.status_code == 200, r.text
    return part


def test_chunk_after_the_think_aloud_ended_is_refused_and_changes_nothing(tmp_path):
    c, sid = serve(tmp_path, [seg("A1"), seg("A2")])
    part = think_aloud(c, sid, "A1")
    before = c.get(f"/api/sessions/{sid}/console-view").json()["state"]["recordings"]
    assert chunk(c, sid, "think_A1", part, 1).status_code == 409
    assert c.post(f"/api/sessions/{sid}/recording/start", json={"stream": "think_A1"}).status_code == 409
    c.post(f"/api/sessions/{sid}/think-aloud/start")
    assert chunk(c, sid, "think_A1", part, 1).status_code == 409
    assert c.get(f"/api/sessions/{sid}/console-view").json()["state"]["recordings"] == before
    assert (tmp_path / sid / "audio" / "think_A1.part1.webm").read_bytes() == b"xx"


def test_chunk_for_an_unknown_part_is_refused_without_opening_the_stream(tmp_path):
    c, sid = serve(tmp_path, [])
    c.post(f"/api/sessions/{sid}/think-aloud/start")
    assert chunk(c, sid, "think_A1", 1, 0).status_code == 400
    assert "think_A1" not in c.get(f"/api/sessions/{sid}/console-view").json()["state"]["recordings"]


def test_human_probe_tail_is_kept_until_finalize_and_refused_after(tmp_path):
    c, sid = serve(tmp_path, [seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("probe talk")])
    for pid in ("A1", "A2", "B1", "B2"):
        think_aloud(c, sid, pid)
    c.post(f"/api/sessions/{sid}/probe/start")
    part = c.post(f"/api/sessions/{sid}/recording/start", json={"stream": "probe_A"}).json()["part"]
    assert chunk(c, sid, "probe_A", part, 0, b"p0").status_code == 200
    c.post(f"/api/sessions/{sid}/probe/end")
    assert chunk(c, sid, "probe_A", part, 1, b"p1").status_code == 200
    assert c.post(f"/api/sessions/{sid}/probe/finalize").status_code == 200
    assert chunk(c, sid, "probe_A", part, 2, b"p2").status_code == 409
    assert (tmp_path / sid / "audio" / "probe_A.part1.webm").read_bytes() == b"p0p1"


def test_acknowledged_gap_releases_the_problem_without_adding_a_segment(tmp_path):
    s, stream = open_stream("think", tmp_path, transcripts=[seg("partial")])
    part = s.recording_start(stream)
    s.recording_chunk(stream, part, 0, b"c0")
    s.recording_chunk(stream, part, 2, b"c2")
    close_stream(s, stream)
    s.acknowledge_incomplete_audio("A1", "expert paused, nothing said")
    assert "A1" not in s.state.untranscribed and [x.text for x in s.state.segments] == ["partial"]
    last = s.store.events()[-1]
    assert (last["type"], last["problem_id"], last["note"]) == ("audio_incomplete_acknowledged", "A1",
                                                                "expert paused, nothing said")


@pytest.mark.parametrize("breakage", ["no audio", "missing file"])
def test_acknowledgement_never_releases_a_problem_without_a_transcript(tmp_path, breakage):
    s, stream = open_stream("think", tmp_path)
    if breakage == "missing file":
        s.recording_chunk(stream, s.recording_start(stream), 0, b"c0")
        part_file(s, stream, 1).unlink()
    close_stream(s, stream)
    with pytest.raises(PhaseError, match="type the transcript"):
        s.acknowledge_incomplete_audio("A1", "")
    assert "A1" in s.state.untranscribed


def test_acknowledge_route_is_console_only_and_releases_the_hold(tmp_path):
    c, sid = serve(tmp_path, [seg("A1")])
    c.post(f"/api/sessions/{sid}/think-aloud/start")
    part = c.post(f"/api/sessions/{sid}/recording/start", json={"stream": "think_A1"}).json()["part"]
    chunk(c, sid, "think_A1", part, 0)
    assert chunk(c, sid, "think_A1", part, 2).json()["gap"] is True
    c.post(f"/api/sessions/{sid}/think-aloud/A1/end", files={"snapshot": ("s.png", PNG, "image/png")})
    url = f"/api/sessions/{sid}/think-aloud/A1/acknowledge-audio"
    assert TestClient(c.app, client=("192.168.1.23", 50000)).post(url, json={"text": ""}).status_code == 403
    r = c.post(url, json={"text": "nothing said"})
    assert r.status_code == 200, r.text
    assert r.json()["state"]["untranscribed"] == []
