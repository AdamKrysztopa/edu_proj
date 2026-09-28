"""Model boundary: a single OpenAI-compatible backend against OpenRouter (owner instruction:
everything goes through OpenRouter; there is no direct Anthropic credential). Backend copied/
trimmed from instrument/src/probe_app/backends.py (copy, never import). Every role in
models.json gets a pinned, exact OpenRouter slug and a config-declared family; family is never
inferred from the backend or the response.
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any, Callable, Mapping, Protocol

import openai

from residual.provenance import Agent

OPENROUTER_API_KEY_ENV = "OPENROUTER_API_KEY"
KEY_ENV = {"openrouter": OPENROUTER_API_KEY_ENV}
OPENROUTER_URL = "https://openrouter.ai/api/v1"
_ROLE_KEYS = {"provider", "model", "family"}
_FORBIDDEN_OPENROUTER_MODELS = {"openrouter/auto", "auto"}
# OpenRouter's web plugin (A13's corpus for evidence.py's future Search records is
# "web:openrouter-exa"); ignore the model's own text, read only the url_citation annotations.
_WEB_PLUGIN = {"id": "web", "engine": "exa"}


class ConfigError(Exception):
    pass


class LLMUnavailable(Exception):
    pass


class LLMRefused(Exception):
    pass


class ServedModelMismatch(LLMUnavailable):
    """The response named a model other than the one configured for the role (A13):
    OpenRouter silently routed elsewhere. The caller must discard the result — evidence stays
    PENDING, never attributed to the configured model."""


class BudgetExceeded(Exception):
    """Raised before a call is dispatched, not after: no network request is made once the
    log's running cost total has reached the budget. The caller stops the run and marks it
    incomplete — this is not an LLM failure, so it is not an LLMUnavailable."""


@dataclass(frozen=True)
class Budget:
    max_usd: float

    def check(self, spent_usd: float) -> None:
        if spent_usd >= self.max_usd:
            raise BudgetExceeded(f"spent ${spent_usd:.4f} of a ${self.max_usd:.4f} budget; refusing the next call")


@dataclass(frozen=True)
class Hit:
    url: str
    title: str


@dataclass(frozen=True)
class SearchResult:
    executed_query: str
    on: date
    hits: tuple[Hit, ...]


class Backend(Protocol):
    def complete_json(self, task: str, system: str, user: str, schema: dict) -> dict: ...
    def search(self, query: str, *, max_results: int) -> SearchResult: ...


@dataclass(frozen=True)
class Model:
    agent: Agent
    backend: Backend

    def json(self, task: str, system: str, user: str, schema: dict) -> dict:
        return self.backend.complete_json(task, system, user, schema)


@dataclass
class CallLog:
    """One JSON line per model call, appended to calls.jsonl. Tracks a running cost total
    against an optional Budget, checked by the backend before each call is dispatched."""

    path: Path
    budget: Budget | None = None
    total_cost: float = 0.0

    def ensure_budget(self) -> None:
        if self.budget is not None:
            self.budget.check(self.total_cost)

    def append(self, *, task: str, role: str, model_id: str, family: str, served_model: str,
               system: str, user: str, schema: dict, input_tokens: int, output_tokens: int,
               cost: float | None = None) -> None:
        spec_sha256 = hashlib.sha256(
            "\x1f".join([system, user, json.dumps(schema, sort_keys=True)]).encode()
        ).hexdigest()
        record = {
            "task": task,
            "role": role,
            "model": model_id,
            "family": family,
            "served_model": served_model,
            "spec_sha256": spec_sha256,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost": cost,
            "utc": datetime.now(UTC).isoformat(),
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        self.total_cost += cost or 0.0


def _extract_json_object(task: str, text: str | None) -> dict:
    if text is None:
        raise LLMUnavailable(f"{task} returned no text")
    data = json.loads(text)
    if not isinstance(data, dict):
        raise LLMUnavailable(f"{task} did not return a JSON object")
    return data


@dataclass
class OpenRouterBackend:
    client: Any
    model_id: str
    family: str
    role: str
    log: CallLog

    def complete_json(self, task: str, system: str, user: str, schema: dict) -> dict:
        self.log.ensure_budget()
        messages = ([{"role": "system", "content": system}] if system else []) + \
                   [{"role": "user", "content": user}]
        params: dict = {
            "model": self.model_id,
            "max_tokens": 8192,
            "messages": messages,
            "response_format": {"type": "json_schema",
                                 "json_schema": {"name": task, "schema": schema, "strict": True}},
        }
        try:
            response = self.client.chat.completions.create(**params)
        except openai.APIError as e:
            raise LLMUnavailable(repr(e)) from e
        if not response.choices:
            raise LLMUnavailable(f"{task} returned no choices")
        choice = response.choices[0]
        if getattr(choice.message, "refusal", None) or choice.finish_reason == "content_filter":
            raise LLMRefused(f"{task} refused")
        if choice.finish_reason == "length":
            raise LLMUnavailable(f"{task} output truncated")
        data = _extract_json_object(task, choice.message.content)
        served_model = response.model
        self.log.append(task=task, role=self.role, model_id=self.model_id, family=self.family,
                         served_model=served_model, system=system, user=user, schema=schema,
                         input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens,
                         cost=getattr(response.usage, "cost", None))
        if served_model != self.model_id:
            raise ServedModelMismatch(f"{task}: requested {self.model_id!r}, served {served_model!r}")
        return data

    def search(self, query: str, *, max_results: int) -> SearchResult:
        """OpenRouter's web plugin (engine exa). Only url_citation annotations are read — the
        model's own text is never used (R11: the planner must not see fetched page text)."""
        self.log.ensure_budget()
        params: dict = {
            "model": self.model_id,
            "max_tokens": 2048,
            "messages": [{"role": "user", "content": query}],
            "extra_body": {"plugins": [{**_WEB_PLUGIN, "max_results": max_results}]},
        }
        try:
            response = self.client.chat.completions.create(**params)
        except openai.APIError as e:
            raise LLMUnavailable(repr(e)) from e
        choice = response.choices[0] if response.choices else None
        annotations = (getattr(choice.message, "annotations", None) or []) if choice else []
        hits = tuple(
            Hit(url=a.url_citation.url, title=a.url_citation.title)
            for a in annotations if getattr(a, "type", None) == "url_citation"
        )
        served_model = response.model
        usage = getattr(response, "usage", None)
        self.log.append(task="web_search", role=self.role, model_id=self.model_id, family=self.family,
                         served_model=served_model, system="", user=query, schema={},
                         input_tokens=getattr(usage, "prompt_tokens", 0),
                         output_tokens=getattr(usage, "completion_tokens", 0),
                         cost=getattr(usage, "cost", None))
        if served_model != self.model_id:
            raise ServedModelMismatch(f"web_search: requested {self.model_id!r}, served {served_model!r}")
        return SearchResult(executed_query=query, on=datetime.now(UTC).date(), hits=hits)


@dataclass(frozen=True)
class RoleConfig:
    role: str
    provider: str
    model: str
    family: str


def _parse_role(role: str, spec: object) -> RoleConfig:
    if not isinstance(spec, dict):
        raise ConfigError(f"role {role!r} must be a JSON object")
    extra = set(spec) - _ROLE_KEYS
    if extra:
        raise ConfigError(f"role {role!r} has config keys {sorted(extra)} beyond "
                           f"{sorted(_ROLE_KEYS)}; a fallback/models list is forbidden (A13)")
    missing = _ROLE_KEYS - set(spec)
    if missing:
        raise ConfigError(f"role {role!r} is missing {sorted(missing)}")
    provider, model_id, family = spec["provider"], spec["model"], spec["family"]
    if provider not in KEY_ENV:
        raise ConfigError(f"role {role!r} uses unknown provider {provider!r}; "
                           f"expected one of {sorted(KEY_ENV)}")
    if model_id.strip().casefold() in _FORBIDDEN_OPENROUTER_MODELS:
        raise ConfigError(f"role {role!r}: {model_id!r} is forbidden — reconstruct pins an "
                           f"exact served model, never OpenRouter auto-routing (A13)")
    prefix = model_id.split("/", 1)[0].strip().casefold()
    if prefix != family.strip().casefold():
        raise ConfigError(f"role {role!r}: openrouter model {model_id!r} has slug prefix "
                           f"{prefix!r}, which must equal family {family!r}")
    return RoleConfig(role=role, provider=provider, model=model_id, family=family)


def _default_client(provider: str, key: str) -> Any:
    return openai.OpenAI(api_key=key, base_url=OPENROUTER_URL)


def _make_backend(cfg: RoleConfig, client: Any, log: CallLog) -> Backend:
    return OpenRouterBackend(client=client, model_id=cfg.model, family=cfg.family, role=cfg.role, log=log)


def load_models(path: str | Path, *, log: CallLog, env: Mapping[str, str] = os.environ,
                 client_factory: Callable[[str, str], Any] | None = None) -> dict[str, Model]:
    """Build every role's Model from a committed models.json. Fails before any network call:
    unknown providers, malformed OpenRouter slugs and a missing API key are all config errors."""
    raw = json.loads(Path(path).read_text())
    if not isinstance(raw, dict):
        raise ConfigError(f"{path}: expected a JSON object mapping role -> config")
    factory = client_factory or _default_client
    configs = {role: _parse_role(role, spec) for role, spec in raw.items()}
    models: dict[str, Model] = {}
    for role, cfg in configs.items():
        key_name = KEY_ENV[cfg.provider]
        key = env.get(key_name)
        if not key:
            raise ConfigError(f"{key_name} is not set, but models.json uses {cfg.provider} "
                               f"for role {role!r} ({cfg.model})")
        client = factory(cfg.provider, key)
        backend = _make_backend(cfg, client, log)
        agent = Agent(kind="model", id=cfg.model, family=cfg.family)
        models[role] = Model(agent=agent, backend=backend)
    return models


def web_search(model: Model, query: str, *, max_results: int) -> SearchResult:
    return model.backend.search(query, max_results=max_results)
