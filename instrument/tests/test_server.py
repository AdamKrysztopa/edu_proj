import pytest
from fastapi.testclient import TestClient

from fakes import FakeAnthropic, FakeResponse, FakeTranscriber, turn_payload
from probe_app.server import create_app
from probe_app.session import Deps
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")


def seg(text):
    return [RawSegment(start=0, end=1, text=text)]


@pytest.fixture
def client(tmp_path):
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("They stick.")]),
                FakeAnthropic(interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))]))
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
