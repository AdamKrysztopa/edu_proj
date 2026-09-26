import base64
from pathlib import Path

from probe_app.backends import Part
from probe_app.config import load_problems
from probe_app.models import DialogueTurn
from probe_app.session import Deps, Session
from probe_app.trace import render_transcript
from probe_app.transcribe import RawSegment

BLANK_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==")

EXPERT_PROMPT = (
    "Role-play Dr. Lee, a human physics lecturer taking part in an education research interview. Below are the "
    "problems Dr. Lee solved and a transcript of what Dr. Lee said aloud while solving them. Reply to the "
    "interviewer's last question as Dr. Lee would say it aloud: two to five sentences, first person, consistent "
    "with the transcript. Reply with Dr. Lee's words only.")


class FixtureTranscriber:
    model = "fixture"

    def __init__(self, fixture: dict[str, list[dict]]):
        self.fixture = fixture
        self.current: str | None = None

    def load(self, problem_id: str) -> None:
        self.current = problem_id

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        return [RawSegment(**s) for s in self.fixture[self.current]]


class SimulatedExpert:
    def __init__(self, backend):
        self.backend = backend

    def answer(self, problems: dict[str, str], transcript: str, dialogue: list[DialogueTurn]) -> str:
        history = "\n".join(f"{d.speaker.upper()}: {d.text}" for d in dialogue)
        problem_text = "\n".join(f"{p}: {t}" for p, t in problems.items())
        prompt = (f"{EXPERT_PROMPT}\n\nPROBLEMS\n{problem_text}\n\n"
                  f"DR. LEE'S THINK-ALOUD\n{transcript}\n\nINTERVIEW SO FAR\n{history}")
        return self.backend.complete("simulated_expert", "", [Part(text=prompt)], None, 2000, lambda r: None).strip()


def run_simulation(root: Path, deps: Deps, expert, set_order: list[str], max_turns: int = 60) -> str:
    session = Session.create(root, deps, expert_id="SIM", cell=0, arms={s: "ai" for s in set_order},
                             set_order=set_order, pilot=True, simulated=True)
    statements = {p: v["statement"] for p, v in load_problems()["problems"].items()}
    while session.state.phase == "ready":
        pid = session.start_think_aloud()
        deps.transcriber.load(pid)
        session.end_think_aloud(pid, b"", BLANK_PNG, [])
    while session.state.phase == "trace_review":
        set_id = session.start_probe()
        pids = session.state.sets[set_id]
        transcript = render_transcript([s for s in session.state.segments if s.problem_id in pids])
        while session.state.phase == "probe":
            dialogue = session.state.dialogue[set_id]
            if len(dialogue) >= max_turns:
                session.end_probe()
                break
            text = expert.answer({p: statements[p] for p in pids}, transcript, dialogue)
            session.answer_ai_text(len(dialogue), text, source="simulated")
    return session.store.session_id
