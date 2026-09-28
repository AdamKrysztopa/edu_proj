from dataclasses import dataclass, replace
from typing import Callable

from pydantic import ValidationError

from probe_app.backends import LLMRefused, LLMUnavailable, Part
from probe_app.config import load_prompt
from probe_app.models import STEMS, DialogueTurn, GuardVerdict, InterviewerTurn

INTERVIEWER_TURN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["utterance", "stem_id", "problem_id", "anchor", "is_followup", "quoted_span", "end_session"],
    "properties": {
        "utterance": {"type": "string"},
        "stem_id": {"type": "string", "enum": list(STEMS)},
        "problem_id": {"type": "string"},
        "anchor": {
            "type": "object",
            "additionalProperties": False,
            "required": ["kind", "segment_ids"],
            "properties": {
                "kind": {"type": "string", "enum": ["segments", "canvas", "none"]},
                "segment_ids": {"type": "array", "items": {"type": "string"}},
            },
        },
        "is_followup": {"type": "boolean"},
        "quoted_span": {"anyOf": [{"type": "string"}, {"type": "null"}]},
        "end_session": {"type": "boolean"},
    },
}

GUARD_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["flagged", "introduced"],
    "properties": {"flagged": {"type": "boolean"}, "introduced": {"type": "string"}},
}


@dataclass
class TurnRequest:
    problems: dict[str, str]
    transcript: str
    snapshots: dict[str, bytes]
    dialogue: list[DialogueTurn]
    remaining_s: float
    wrap_up: bool
    unused: list[str]
    rejection: str | None = None


def _render_dialogue(dialogue: list[DialogueTurn]) -> str:
    lines = []
    for d in dialogue:
        if d.speaker == "interviewer":
            tag = f"{d.problem_id}/{d.stem_id}{' follow-up' if d.is_followup else ''}"
            lines.append(f"INTERVIEWER [{tag}]: {d.text}")
        else:
            lines.append(f"EXPERT: {d.text}")
    return "\n".join(lines) or "(no questions asked yet)"


class InterviewerLLM:
    def __init__(self, backend, log: Callable[[dict], object], system_prompt: str):
        self.backend, self.log, self.system_prompt = backend, log, system_prompt

    def _parts(self, req: TurnRequest) -> list[Part]:
        problems = "\n".join(f"{pid}: {text}" for pid, text in req.problems.items())
        parts = [Part(text=f"PROBLEMS\n{problems}\n\nTHINK-ALOUD TRANSCRIPT\n{req.transcript}")]
        for pid, png in req.snapshots.items():
            parts += [Part(text=f"Written work for {pid}:"), Part(png=png, name=pid)]
        parts[-1] = replace(parts[-1], cache=True)
        status = [f"PROBE DIALOGUE SO FAR\n{_render_dialogue(req.dialogue)}",
                  f"Time remaining: {int(req.remaining_s)} s.",
                  f"Stems not yet used: {', '.join(req.unused) or 'none'}."]
        if req.wrap_up:
            status.append("Less than two minutes remain: ask at most one more question, "
                          "or end the session if every stem has been used.")
        if req.rejection:
            status.append(f"Your previous proposed turn was rejected ({req.rejection}). Propose a different turn.")
        status.append("Return the next turn.")
        return parts + [Part(text="\n\n".join(status))]

    def next_turn(self, req: TurnRequest) -> InterviewerTurn:
        text = self.backend.complete("interviewer", self.system_prompt, self._parts(req), INTERVIEWER_TURN_SCHEMA,
                                     16000, self.log, thinking=True)
        try:
            return InterviewerTurn.model_validate_json(text)
        except ValidationError as e:
            raise LLMUnavailable(f"interviewer output failed validation: {e}") from e


class Guard:
    def __init__(self, backend, log: Callable[[dict], object], system_prompt: str):
        self.backend, self.log, self.system_prompt = backend, log, system_prompt

    def check(self, utterance: str, problem_text: str, expert_text: str) -> GuardVerdict:
        user = (f"PROBLEM STATEMENTS\n{problem_text}\n\nEXPERT'S WORDS SO FAR\n{expert_text}\n\n"
                f"PROPOSED QUESTION\n{utterance}")
        text = self.backend.complete("guard", self.system_prompt, [Part(text=user)], GUARD_SCHEMA, 1024, self.log)
        try:
            return GuardVerdict.model_validate_json(text)
        except ValidationError as e:
            raise LLMUnavailable(f"guard output failed validation: {e}") from e


def make_interviewer(backend, log: Callable[[dict], object]) -> InterviewerLLM:
    return InterviewerLLM(backend, log, load_prompt("interviewer_system.md"))


def make_guard(backend, log: Callable[[dict], object]) -> Guard:
    """The one construction of the guard, so `probe-code guard-audit` runs the guard the sessions ran."""
    return Guard(backend, log, load_prompt("guard_system.md"))
