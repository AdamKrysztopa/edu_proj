import json

import pytest

from probe_code.export import export_blind, export_trace, read_csv, split_units
from probe_code.loader import SimulatedSession, load_session
from probe_app.session import SessionState
from probe_app.models import DialogueTurn, Segment

PNG = bytes.fromhex("89504e470d0a1a0a")


def make_session(tmp_path, name, arms=None, simulated=False):
    d = tmp_path / name
    (d / "canvas" / "snapshots").mkdir(parents=True)
    (d / "canvas" / "snapshots" / "A1.png").write_bytes(PNG)
    state = SessionState(sets={"A": ["A1", "A2"], "B": ["B1", "B2"]}, set_order=["A", "B"],
                         arms=arms or {"A": "ai", "B": "human"}, phase="done")
    state.segments = [Segment(id="A1-s001", problem_id="A1", start=0, end=1, text="Energy first.")]
    state.dialogue = {
        "A": [DialogueTurn(speaker="interviewer", text="SECRET AI QUESTION", t=0, source="ai"),
              DialogueTurn(speaker="expert", text="They stick. So momentum!", t=1, source="transcribed")],
        "B": [DialogueTurn(speaker="interviewer", text="SECRET HUMAN QUESTION", t=0, source="human"),
              DialogueTurn(speaker="expert", text="Spring energy.", t=1, source="transcribed")]}
    (d / "state.json").write_text(state.model_dump_json())
    (d / "manifest.json").write_text(json.dumps({"expert_id": name, "pilot": True, "simulated": simulated}))
    return d


def test_split_units():
    assert split_units("They stick. So momentum! Right?") == ["They stick.", "So momentum!", "Right?"]


def test_simulated_sessions_refused(tmp_path):
    with pytest.raises(SimulatedSession):
        load_session(make_session(tmp_path, "SIM", simulated=True))
    assert load_session(make_session(tmp_path, "SIM2", simulated=True), allow_simulated=True)


def test_blind_export_has_no_interviewer_text_and_separate_key(tmp_path):
    sessions = [load_session(make_session(tmp_path, n)) for n in ("E01", "E02")]
    out = tmp_path / "out"
    export_blind(sessions, out, seed=1)
    coder_text = (out / "coder_units.csv").read_text()
    assert "SECRET" not in coder_text and "ai" not in read_csv(out / "coder_units.csv")[0].values()
    assert "arm" not in read_csv(out / "coder_units.csv")[0]
    rows = read_csv(out / "coder_units.csv")
    key = {r["unit_id"]: r for r in read_csv(out / "key_units.csv")}
    assert len(rows) == 6 and set(key) == {r["unit_id"] for r in rows}
    assert {key[r["unit_id"]]["arm"] for r in rows} == {"ai", "human"}
    assert len({r["blind_session"] for r in rows}) == 4


def test_trace_export_has_no_probe_material(tmp_path):
    sessions = [load_session(make_session(tmp_path, "E01"))]
    out = tmp_path / "trace"
    export_trace(sessions, out, seed=1)
    text = (out / "trace_units.csv").read_text()
    assert "Energy first." in text and "stick" not in text and "SECRET" not in text
    blind = read_csv(out / "key_trace.csv")[0]["blind_session"]
    assert (out / "snapshots" / f"{blind}_A1.png").read_bytes() == PNG
