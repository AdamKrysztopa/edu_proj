import json as _json
from pathlib import Path
from types import SimpleNamespace

from probe_app.backends import AnthropicBackend, Backends
from probe_app.config import Models
from probe_app.transcribe import RawSegment


class FakeClock:
    def __init__(self, t: float = 0.0):
        self.t = t

    def now(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


TEST_MODELS = Models.model_validate({
    "interviewer": {"provider": "anthropic", "model": "claude-opus-5", "effort": "medium"},
    "guard": {"provider": "anthropic", "model": "claude-haiku-4-5", "temperature": 0},
    "simulated_expert": {"provider": "anthropic", "model": "claude-sonnet-5", "effort": "low"},
    "transcriber": {"model": "scribe_v2"},
})


class FakeTranscriber:
    model = TEST_MODELS.transcriber.model

    def __init__(self, results: list):
        self.results = list(results)
        self.calls: list[Path] = []

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        self.calls.append(audio_path)
        item = self.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def openai_response(content: str | None, finish_reason: str = "stop", refusal: str | None = None):
    message = SimpleNamespace(content=content, refusal=refusal)
    response = SimpleNamespace(choices=[SimpleNamespace(message=message, finish_reason=finish_reason)])
    response.model_dump = lambda mode="json": {"choices": [{"content": content, "refusal": refusal,
                                                            "finish_reason": finish_reason}]}
    return response


class FakeOpenAI:
    def __init__(self, responses: list):
        self.responses, self.calls = list(responses), []
        self.chat = SimpleNamespace(completions=self)

    def create(self, **kwargs):
        self.calls.append(kwargs)
        item = self.responses.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


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
        role = "guard" if kwargs["model"] == TEST_MODELS.guard.model else "interviewer"
        queue = self.queues[role]
        if not queue and role == "guard":
            return FakeResponse({"flagged": False, "introduced": ""})
        item = queue.pop(0)
        if isinstance(item, Exception):
            raise item
        return item


def fake_backends(client) -> Backends:
    return Backends(interviewer=AnthropicBackend(client, TEST_MODELS.interviewer),
                    guard=AnthropicBackend(client, TEST_MODELS.guard))


def turn_payload(**overrides) -> dict:
    payload = {"utterance": "What did you notice first?", "stem_id": "cues", "problem_id": "A1",
               "anchor": {"kind": "none", "segment_ids": []}, "is_followup": False,
               "quoted_span": None, "end_session": False}
    payload.update(overrides)
    return payload
