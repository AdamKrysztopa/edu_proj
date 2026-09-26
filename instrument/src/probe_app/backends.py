import base64
import hashlib
import os
from dataclasses import dataclass
from typing import Callable, Mapping

import anthropic
import openai

from probe_app.config import Models, RoleModel

OPENROUTER_URL = "https://openrouter.ai/api/v1"
KEY_ENV = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY", "openrouter": "OPENROUTER_API_KEY"}

Log = Callable[[dict], object]


class LLMUnavailable(Exception):
    pass


class LLMRefused(Exception):
    pass


@dataclass(frozen=True)
class Part:
    text: str | None = None
    png: bytes | None = None
    name: str = ""
    cache: bool = False


def _logged_image(p: Part) -> dict:
    return {"type": "image", "snapshot": p.name, "sha256": hashlib.sha256(p.png).hexdigest()}


def _b64(png: bytes) -> str:
    return base64.standard_b64encode(png).decode()


class AnthropicBackend:
    def __init__(self, client, role: RoleModel):
        self.client, self.role = client, role

    def _block(self, p: Part, for_log: bool) -> dict:
        if p.png is None:
            block = {"type": "text", "text": p.text}
        elif for_log:
            block = _logged_image(p)
        else:
            block = {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": _b64(p.png)}}
        return {**block, "cache_control": {"type": "ephemeral"}} if p.cache else block

    def complete(self, kind: str, system: str, parts: list[Part], schema: dict | None, max_tokens: int,
                 log: Log, thinking: bool = False) -> str:
        params: dict = {"model": self.role.model, "max_tokens": max_tokens}
        if system:
            params["system"] = system
        if thinking:
            params["thinking"] = {"type": "adaptive"}
        output_config = {}
        if self.role.effort:
            output_config["effort"] = self.role.effort
        if schema:
            output_config["format"] = {"type": "json_schema", "schema": schema}
        if output_config:
            params["output_config"] = output_config
        if self.role.temperature is not None:
            # SDK 1.x dropped the temperature keyword; the API still honours it in the request body.
            params["extra_body"] = {"temperature": self.role.temperature}
        loggable = {**params, "provider": "anthropic",
                    "messages": [{"role": "user", "content": [self._block(p, True) for p in parts]}]}
        params["messages"] = [{"role": "user", "content": [self._block(p, False) for p in parts]}]
        try:
            response = self.client.messages.create(**params)
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


class OpenAICompatBackend:
    def __init__(self, client, role: RoleModel):
        self.client, self.role = client, role

    def _part(self, p: Part, for_log: bool) -> dict:
        if p.png is None:
            return {"type": "text", "text": p.text}
        if for_log:
            return _logged_image(p)
        return {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{_b64(p.png)}"}}

    def complete(self, kind: str, system: str, parts: list[Part], schema: dict | None, max_tokens: int,
                 log: Log, thinking: bool = False) -> str:
        head = [{"role": "system", "content": system}] if system else []
        params: dict = {"model": self.role.model}
        # OpenAI reasoning models reject max_tokens; OpenRouter documents only max_tokens.
        params["max_tokens" if self.role.provider == "openrouter" else "max_completion_tokens"] = max_tokens
        if schema:
            params["response_format"] = {"type": "json_schema",
                                         "json_schema": {"name": kind, "schema": schema, "strict": True}}
        if self.role.temperature is not None:
            params["temperature"] = self.role.temperature
        if self.role.provider == "openrouter":
            routing = {"require_parameters": True, "data_collection": "deny"}
            if self.role.route:
                routing |= {"order": self.role.route, "allow_fallbacks": False}
            params["extra_body"] = {"provider": routing}
            if self.role.effort:
                params["extra_body"]["reasoning"] = {"effort": self.role.effort}
        elif self.role.effort:
            params["reasoning_effort"] = self.role.effort
        loggable = {**params, "provider": self.role.provider,
                    "messages": head + [{"role": "user", "content": [self._part(p, True) for p in parts]}]}
        params["messages"] = head + [{"role": "user", "content": [self._part(p, False) for p in parts]}]
        try:
            response = self.client.chat.completions.create(**params)
        except openai.APIError as e:
            log({"kind": kind, "request": loggable, "error": repr(e)})
            raise LLMUnavailable(repr(e)) from e
        log({"kind": kind, "request": loggable, "response": response.model_dump(mode="json")})
        if not response.choices:
            raise LLMUnavailable(f"{kind} returned no choices")
        choice = response.choices[0]
        if getattr(choice.message, "refusal", None) or choice.finish_reason == "content_filter":
            raise LLMRefused(f"{kind} refused")
        if choice.finish_reason == "length":
            raise LLMUnavailable(f"{kind} output truncated")
        if not choice.message.content:
            raise LLMUnavailable(f"{kind} returned no text")
        return choice.message.content


def make_backend(name: str, role: RoleModel, env: Mapping[str, str] = os.environ):
    key_name = KEY_ENV[role.provider]
    key = env.get(key_name)
    if not key:
        raise ValueError(f"{key_name} is not set, but models.json uses {role.provider} for the {name} ({role.model})")
    if role.provider == "anthropic":
        return AnthropicBackend(anthropic.Anthropic(api_key=key), role)
    base_url = OPENROUTER_URL if role.provider == "openrouter" else None
    return OpenAICompatBackend(openai.OpenAI(api_key=key, base_url=base_url), role)


@dataclass
class Backends:
    interviewer: AnthropicBackend | OpenAICompatBackend
    guard: AnthropicBackend | OpenAICompatBackend


def make_backends(models: Models, env: Mapping[str, str] = os.environ) -> Backends:
    return Backends(interviewer=make_backend("interviewer", models.interviewer, env),
                    guard=make_backend("guard", models.guard, env))
