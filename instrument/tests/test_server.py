import pytest
from fastapi.testclient import TestClient

from fakes import FakeAnthropic, FakeResponse, FakeTranscriber, fake_backends, turn_payload
from probe_app.server import create_app
from probe_app.session import Deps
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")


def seg(text):
    return [RawSegment(start=0, end=1, text=text)]


@pytest.fixture
def client(tmp_path):
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("They stick.")]),
                fake_backends(FakeAnthropic(interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))])))
    return TestClient(create_app(tmp_path, deps))


def create(client) -> str:
    r = client.post("/api/sessions", json={"expert_id": "E01", "cell": 1, "set_order": ["A", "B"],
                                           "arms": {"A": "ai", "B": "human"}, "pilot": True})
    assert r.status_code == 200
    return r.json()["session_id"]


def think_all(client, sid):
    for pid in ("A1", "A2", "B1", "B2"):
        assert client.post(f"/api/sessions/{sid}/think-aloud/start").status_code == 200
        r = client.post(f"/api/sessions/{sid}/think-aloud/{pid}/end",
                        files={"audio": ("a.webm", b"x", "audio/webm"), "snapshot": ("s.png", PNG, "image/png")},
                        data={"strokes": "[]"})
        assert r.status_code == 200, r.text


def test_pages_served(client):
    assert client.get("/").status_code == 200
    assert client.get("/expert").status_code == 200


def test_full_ai_probe_round_and_duplicate(client):
    sid = create(client)
    think_all(client, sid)
    assert client.get(f"/api/sessions/{sid}/snapshot/A1").content == PNG
    client.post(f"/api/sessions/{sid}/probe/start")
    view = client.get(f"/api/sessions/{sid}/expert-view").json()
    assert view["question"] and view["expected_answer_index"] == 1
    files = {"audio": ("a.webm", b"x", "audio/webm")}
    assert client.post(f"/api/sessions/{sid}/probe/answer", files=files, data={"turn_index": "1"}).status_code == 200
    assert client.post(f"/api/sessions/{sid}/probe/answer", files=files, data={"turn_index": "1"}).status_code == 409


def test_wrong_phase_is_409(client):
    sid = create(client)
    assert client.post(f"/api/sessions/{sid}/probe/start").status_code == 409


def test_unknown_or_malformed_session(client):
    assert client.get("/api/sessions/nope/expert-view").status_code == 404
    assert client.get("/api/sessions/..%2Fx/expert-view").status_code in (400, 404)


def test_expert_view_hides_trace(client):
    sid = create(client)
    think_all(client, sid)
    assert "segments" not in client.get(f"/api/sessions/{sid}/expert-view").json()
    assert client.get(f"/api/sessions/{sid}/console-view").json()["state"]["segments"]


def test_data_session_without_prereg_is_400(client, monkeypatch, tmp_path):
    monkeypatch.setattr("probe_app.session.PREREG_PATH", tmp_path / "none.json")
    r = client.post("/api/sessions", json={"expert_id": "E01", "cell": 1, "set_order": ["A", "B"],
                                           "arms": {"A": "ai", "B": "human"}, "pilot": False})
    assert r.status_code == 400 and "freeze" in r.text


def test_expert_id_with_path_characters_is_rejected(client, tmp_path):
    for bad in ("../escape", "a/b", ""):
        r = client.post("/api/sessions", json={"expert_id": bad, "cell": 1, "set_order": ["A", "B"],
                                               "arms": {"A": "ai", "B": "human"}, "pilot": True})
        assert r.status_code in (400, 422), bad
    assert not (tmp_path.parent / "escape").exists()


class Boom:
    model = "fake"

    def transcribe(self, path):
        raise TypeError("unexpected SDK change")


def test_unexpected_exception_rolls_back_in_memory_state(tmp_path):
    from fakes import FakeTranscriber
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2")]),
                fake_backends(FakeAnthropic(interviewer=[FakeResponse(turn_payload()), TypeError("sdk changed")])))
    c = TestClient(create_app(tmp_path, deps), raise_server_exceptions=False)
    sid = create(c)
    think_all(c, sid)
    c.post(f"/api/sessions/{sid}/probe/start")
    r = c.post(f"/api/sessions/{sid}/probe/answer-text", json={"turn_index": 1, "text": "hello"})
    assert r.status_code == 500
    view = c.get(f"/api/sessions/{sid}/expert-view").json()
    assert view["expected_answer_index"] == 1 and view["question"]


def test_streamed_think_aloud_and_polling_enforces_cap(tmp_path):
    from fakes import FakeClock
    clock = FakeClock()
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2")]),
                fake_backends(FakeAnthropic(interviewer=[FakeResponse(turn_payload())])))
    c = TestClient(create_app(tmp_path, deps, clock))
    sid = c.post("/api/sessions", json={"expert_id": "E01", "cell": 1, "set_order": ["A", "B"],
                                        "arms": {"A": "human", "B": "ai"}, "pilot": True}).json()["session_id"]
    for pid in ("A1", "A2", "B1", "B2"):
        c.post(f"/api/sessions/{sid}/think-aloud/start")
        part = c.post(f"/api/sessions/{sid}/recording/start", json={"stream": f"think_{pid}"}).json()["part"]
        for seq in (0, 1, 1):
            r = c.post(f"/api/sessions/{sid}/recording/chunk", params={"stream": f"think_{pid}", "part": part, "seq": seq},
                       content=b"xx", headers={"Content-Type": "application/octet-stream"})
            assert r.status_code == 200 and r.json()["gap"] is False
        r = c.post(f"/api/sessions/{sid}/think-aloud/{pid}/end",
                   files={"snapshot": ("s.png", PNG, "image/png")}, data={"strokes": "[]"})
        assert r.status_code == 200, r.text
    assert (tmp_path / sid / "audio" / "think_A1.part1.webm").read_bytes() == b"xxxx"
    c.post(f"/api/sessions/{sid}/probe/start")
    clock.advance(1200)
    assert c.get(f"/api/sessions/{sid}/expert-view").json()["phase"] == "probe_uploading"
    assert c.post(f"/api/sessions/{sid}/probe/finalize").status_code == 200
    assert c.get(f"/api/sessions/{sid}/console-view").json()["state"]["phase"] == "trace_review"
