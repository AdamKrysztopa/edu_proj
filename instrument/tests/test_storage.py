import json
import re

import pytest

from fakes import FakeClock
from probe_app.models import InterviewerTurn
from probe_app.storage import SessionStore


def test_create_writes_manifest_and_dirs(tmp_path):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    assert re.fullmatch(r"E01-[0-9a-f]{32}", store.session_id)
    assert store.manifest == {"expert_id": "E01"}
    for d in ("audio", "canvas/snapshots", "transcripts", "llm"):
        assert (store.dir / d).is_dir()


def test_log_appends_with_both_timestamps(tmp_path):
    clock = FakeClock(5.0)
    store = SessionStore.create(tmp_path, {"expert_id": "E01"}, clock)
    store.log("keep_talking", problem_id="A1")
    clock.advance(2.5)
    store.log("probe", text="q")
    events = store.events()
    assert [e["type"] for e in events] == ["keep_talking", "probe"]
    assert events[1]["t_mono"] == 7.5
    assert "t_wall" in events[0] and events[0]["problem_id"] == "A1"


def test_write_and_read_json_roundtrip(tmp_path):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    store.write_json("state.json", {"phase": "ready"})
    assert store.read_json("state.json") == {"phase": "ready"}
    assert not list(store.dir.glob("*.tmp"))


def test_log_llm_numbers_files(tmp_path):
    store = SessionStore.create(tmp_path, {"expert_id": "E01"})
    a = store.log_llm({"kind": "interviewer"})
    b = store.log_llm({"kind": "guard"})
    assert (a.name, b.name) == ("0001.json", "0002.json")
    assert json.loads(b.read_text()) == {"kind": "guard"}


def test_interviewer_turn_forbids_extra_fields():
    with pytest.raises(ValueError):
        InterviewerTurn.model_validate({
            "utterance": "q", "stem_id": "cues", "problem_id": "A1",
            "anchor": {"kind": "none", "segment_ids": []}, "is_followup": False,
            "quoted_span": None, "end_session": False, "extra": 1,
        })
