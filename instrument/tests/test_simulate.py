import json

from fakes import FakeAnthropic, FakeResponse, turn_payload
from probe_app.config import INSTRUMENT_DIR
from probe_app.models import STEMS
from probe_app.session import Deps
from probe_app.simulate import FixtureTranscriber, run_simulation


class EchoExpert:
    def answer(self, problems, transcript, dialogue):
        return f"Answer to: {dialogue[-1].text}"


def test_simulation_runs_ai_arm_to_completion(tmp_path):
    turns = []
    for set_problems in (["A1", "A2"], ["B1", "B2"]):
        turns += [FakeResponse(turn_payload(problem_id=p, stem_id=s)) for p in set_problems for s in STEMS]
        turns.append(FakeResponse(turn_payload(problem_id=set_problems[0], end_session=True)))
    fixture = json.loads((INSTRUMENT_DIR / "problems" / "simulated_think_aloud.json").read_text())
    deps = Deps(FixtureTranscriber(fixture), FakeAnthropic(interviewer=turns))
    sid = run_simulation(tmp_path, deps, EchoExpert(), ["A", "B"])
    state = json.loads((tmp_path / sid / "state.json").read_text())
    manifest = json.loads((tmp_path / sid / "manifest.json").read_text())
    assert state["phase"] == "done" and manifest["simulated"] is True
    assert len([d for d in state["dialogue"]["A"] if d["speaker"] == "expert"]) == 10
    assert state["dialogue"]["A"][1]["source"] == "simulated"
