import pytest
from fastapi.testclient import TestClient

from fakes import FakeAnthropic, FakeResponse, FakeTranscriber, fake_backends, turn_payload
from probe_app.server import create_app
from probe_app.session import Deps
from probe_app.transcribe import RawSegment

PNG = bytes.fromhex("89504e470d0a1a0a")
LAPTOP = ("127.0.0.1", 50000)
TABLET = ("192.168.1.23", 50000)


def seg(text):
    return [RawSegment(start=0, end=1, text=text)]


@pytest.fixture
def app(tmp_path):
    deps = Deps(FakeTranscriber([seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("They stick.")]),
                fake_backends(FakeAnthropic(interviewer=[FakeResponse(turn_payload()), FakeResponse(turn_payload(stem_id="checks"))])))
    return create_app(tmp_path, deps)


@pytest.fixture
def client(app):
    return TestClient(app, client=LAPTOP)


@pytest.fixture
def tablet(app):
    return TestClient(app, client=TABLET)


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
    c = TestClient(create_app(tmp_path, deps), raise_server_exceptions=False, client=LAPTOP)
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
    c = TestClient(create_app(tmp_path, deps, clock), client=LAPTOP)
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


EXPERT_PATHS = {"/expert", "/api/sessions/{sid}/expert-view", "/api/sessions/{sid}/recording/start",
                "/api/sessions/{sid}/recording/chunk", "/api/sessions/{sid}/snapshot/{pid}",
                "/api/sessions/{sid}/think-aloud/{pid}/end", "/api/sessions/{sid}/probe/answer",
                "/api/sessions/{sid}/probe/finalize"}

CONSOLE_ROUTES = [("get", "/"), ("post", "/api/sessions"), ("get", "/api/sessions/{sid}/console-view"),
                  ("post", "/api/sessions/{sid}/think-aloud/start"), ("post", "/api/sessions/{sid}/keep-talking"),
                  ("post", "/api/sessions/{sid}/segments/{seg_id}"), ("post", "/api/sessions/{sid}/segments"),
                  ("post", "/api/sessions/{sid}/probe/start"), ("post", "/api/sessions/{sid}/probe/answer-text"),
                  ("post", "/api/sessions/{sid}/probe/end"), ("post", "/api/sessions/{sid}/human/marker"),
                  ("post", "/api/sessions/{sid}/human/stem"), ("post", "/api/sessions/{sid}/human/anchor"),
                  ("post", "/api/sessions/{sid}/pause"), ("post", "/api/sessions/{sid}/resume")]


def test_every_route_is_either_expert_or_loopback_only(app):
    from fastapi.routing import APIRoute

    from probe_app.server import loopback_only
    routes = [r for r in app.routes if isinstance(r, APIRoute)]
    guarded = {r.path for r in routes if any(d.call is loopback_only for d in r.dependant.dependencies)}
    assert {r.path for r in routes} - guarded == EXPERT_PATHS
    assert guarded == {path for _, path in CONSOLE_ROUTES}


@pytest.mark.parametrize("method, path", CONSOLE_ROUTES)
def test_console_route_refuses_a_network_client(client, tablet, method, path):
    sid = create(client)
    url = path.format(sid=sid, seg_id="A1-s001")
    r = tablet.get(url) if method == "get" else tablet.post(url, json={})
    assert r.status_code == 403


def test_ipv6_loopback_reaches_the_console(app):
    assert TestClient(app, client=("::1", 50000)).get("/").status_code == 200


def test_expert_routes_answer_a_network_client(client, tablet):
    sid = create(client)
    assert tablet.get("/expert").status_code == 200
    for pid in ("A1", "A2", "B1", "B2"):
        assert client.post(f"/api/sessions/{sid}/think-aloud/start").status_code == 200
        part = tablet.post(f"/api/sessions/{sid}/recording/start", json={"stream": f"think_{pid}"}).json()["part"]
        r = tablet.post(f"/api/sessions/{sid}/recording/chunk", params={"stream": f"think_{pid}", "part": part, "seq": 0},
                        content=b"xx", headers={"Content-Type": "application/octet-stream"})
        assert r.status_code == 200
        r = tablet.post(f"/api/sessions/{sid}/think-aloud/{pid}/end",
                        files={"snapshot": ("s.png", PNG, "image/png")}, data={"strokes": "[]"})
        assert r.status_code == 200, r.text
    assert tablet.get(f"/api/sessions/{sid}/snapshot/A1").content == PNG
    assert client.post(f"/api/sessions/{sid}/probe/start").status_code == 200
    assert tablet.get(f"/api/sessions/{sid}/expert-view").json()["question"]
    r = tablet.post(f"/api/sessions/{sid}/probe/answer", files={"audio": ("a.webm", b"x", "audio/webm")},
                    data={"turn_index": "1"})
    assert r.status_code == 200, r.text
    assert tablet.post(f"/api/sessions/{sid}/probe/finalize").status_code == 409


def test_console_view_carries_the_tablet_origin(tmp_path):
    deps = Deps(FakeTranscriber([]), fake_backends(FakeAnthropic()))
    client = TestClient(create_app(tmp_path, deps, expert_origin="https://10.0.0.5:8000"), client=LAPTOP)
    view = client.get(f"/api/sessions/{create(client)}/console-view").json()
    assert view["expert_origin"] == "https://10.0.0.5:8000"
