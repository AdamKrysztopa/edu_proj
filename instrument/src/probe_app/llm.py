import base64
import hashlib
from dataclasses import dataclass
from typing import Callable

import anthropic
from pydantic import ValidationError

from probe_app.config import GUARD_MODEL, INTERVIEWER_EFFORT, INTERVIEWER_MODEL
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


class LLMUnavailable(Exception):
    pass


class LLMRefused(Exception):
    pass


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


def _call(client, log: Callable[[dict], object], kind: str, params: dict, loggable: dict) -> str:
    try:
        response = client.messages.create(**params)
    except anthropic.APIError as e:
        log({"kind": kind, "request": loggable, "error": repr(e)})
        raise LLMUnavailable(repr(e)) from e
    log({"kind": kind, "request": loggable, "response": response.model_dump(mode="json")})
    if response.stop_reason == "refusal":
        raise LLMRefused(f"{kind} refused")
    if response.stop_reason == "max_tokens":
        raise LLMUnavailable(f"{kind} output truncated")
    text = next((b.text for b in response.content if b.type == "text"), None)
    if text is None:
        raise LLMUnavailable(f"{kind} returned no text")
    return text


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
    def __init__(self, client, log: Callable[[dict], object], system_prompt: str,
                 model: str = INTERVIEWER_MODEL, effort: str = INTERVIEWER_EFFORT):
        self.client, self.log, self.system_prompt = client, log, system_prompt
        self.model, self.effort = model, effort

    def _content(self, req: TurnRequest) -> tuple[list[dict], list[dict]]:
        problems = "\n".join(f"{pid}: {text}" for pid, text in req.problems.items())
        content = [{"type": "text", "text": f"PROBLEMS\n{problems}\n\nTHINK-ALOUD TRANSCRIPT\n{req.transcript}"}]
        loggable = list(content)
        for pid, png in req.snapshots.items():
            label = {"type": "text", "text": f"Written work for {pid}:"}
            content += [label, {"type": "image", "source": {"type": "base64", "media_type": "image/png",
                                                             "data": base64.standard_b64encode(png).decode()}}]
            loggable += [label, {"type": "image", "snapshot": pid, "sha256": hashlib.sha256(png).hexdigest()}]
        content[-1] = {**content[-1], "cache_control": {"type": "ephemeral"}}
        status = [f"PROBE DIALOGUE SO FAR\n{_render_dialogue(req.dialogue)}",
                  f"Time remaining: {int(req.remaining_s)} s.",
                  f"Stems not yet used: {', '.join(req.unused) or 'none'}."]
        if req.wrap_up:
            status.append("Less than two minutes remain: ask at most one more question, "
                          "or end the session if every stem has been used.")
        if req.rejection:
            status.append(f"Your previous proposed turn was rejected ({req.rejection}). Propose a different turn.")
        status.append("Return the next turn.")
        dynamic = {"type": "text", "text": "\n\n".join(status)}
        return content + [dynamic], loggable + [dynamic]

    def next_turn(self, req: TurnRequest) -> InterviewerTurn:
        content, loggable_content = self._content(req)
        params = dict(model=self.model, max_tokens=16000, system=self.system_prompt,
                      thinking={"type": "adaptive"},
                      output_config={"effort": self.effort,
                                     "format": {"type": "json_schema", "schema": INTERVIEWER_TURN_SCHEMA}},
                      messages=[{"role": "user", "content": content}])
        loggable = {**params, "messages": [{"role": "user", "content": loggable_content}]}
        text = _call(self.client, self.log, "interviewer", params, loggable)
        try:
            return InterviewerTurn.model_validate_json(text)
        except ValidationError as e:
            raise LLMUnavailable(f"interviewer output failed validation: {e}") from e


class Guard:
    def __init__(self, client, log: Callable[[dict], object], system_prompt: str, model: str = GUARD_MODEL):
        self.client, self.log, self.system_prompt, self.model = client, log, system_prompt, model

    def check(self, utterance: str, problem_text: str, expert_text: str) -> GuardVerdict:
        user = (f"PROBLEM STATEMENTS\n{problem_text}\n\nEXPERT'S WORDS SO FAR\n{expert_text}\n\n"
                f"PROPOSED QUESTION\n{utterance}")
        # SDK 1.x dropped the temperature keyword; Haiku 4.5 still honours it in the request body.
        params = dict(model=self.model, max_tokens=1024, extra_body={"temperature": 0}, system=self.system_prompt,
                      output_config={"format": {"type": "json_schema", "schema": GUARD_SCHEMA}},
                      messages=[{"role": "user", "content": user}])
        text = _call(self.client, self.log, "guard", params, params)
        try:
            return GuardVerdict.model_validate_json(text)
        except ValidationError as e:
            raise LLMUnavailable(f"guard output failed validation: {e}") from e
