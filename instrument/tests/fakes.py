class FakeClock:
    def __init__(self, t: float = 0.0):
        self.t = t

    def now(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


from pathlib import Path

from probe_app.transcribe import RawSegment


class FakeTranscriber:
    model = "fake"

    def __init__(self, results: list):
        self.results = list(results)
        self.calls: list[Path] = []

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        self.calls.append(audio_path)
        item = self.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


import json as _json
from types import SimpleNamespace

from probe_app.config import GUARD_MODEL


class FakeResponse:
    def __init__(self, payload: dict | None, stop_reason: str = "end_turn"):
        self.stop_reason = stop_reason
        self.content = [] if payload is None else [SimpleNamespace(type="text", text=_json.dumps(payload))]

    def model_dump(self, mode: str = "json") -> dict:
        return {"stop_reason": self.stop_reason, "content": [{"type": "text", "text": c.text} for c in self.content]}


class FakeAnthropic:
    def __init__(self, interviewer: list | None = None, guard: list | None = None):
        self.queues = {"interviewer": list(interviewer or []), "guard": list(guard or [])}
        self.calls: list[dict] = []
        self.messages = self

    def create(self, **kwargs):
        self.calls.append(kwargs)
        role = "guard" if kwargs["model"] == GUARD_MODEL else "interviewer"
        queue = self.queues[role]
        if not queue and role == "guard":
            return FakeResponse({"flagged": False, "introduced": ""})
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def turn_payload(**overrides) -> dict:
    payload = {"utterance": "What did you notice first?", "stem_id": "cues", "problem_id": "A1",
               "anchor": {"kind": "none", "segment_ids": []}, "is_followup": False,
               "quoted_span": None, "end_session": False}
    payload.update(overrides)
    return payload
