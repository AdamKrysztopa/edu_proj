# Model Choice Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every LLM role in `instrument/` (interviewer, guard, simulated expert) and the transcriber is chosen in one committed `instrument/models.json`, with Anthropic, OpenAI or OpenRouter as the provider.

**Architecture:** `config.py` loads and validates `models.json` and puts the interviewer and guard choice into `FrozenConfig`, so `prereg.json` locks it. A new `probe_app/backends.py` holds two backends behind one `complete()` call: native Anthropic (today's request shape) and OpenAI-compatible (OpenAI direct or OpenRouter via `base_url`). `InterviewerLLM`, `Guard` and `SimulatedExpert` build provider-neutral `Part`s and call a backend; `Deps` carries backends instead of an Anthropic client.

**Tech Stack:** Python 3, pydantic 2.13, anthropic SDK 1.8, openai SDK 3.19, pytest, uv.

**Spec:** `docs/superpowers/specs/2026-09-26-model-choice-design.md`

## Global Constraints

- Providers: exactly `anthropic`, `openai`, `openrouter`. OpenRouter base URL `https://openrouter.ai/api/v1`.
- Keys: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`, loaded by the app from `instrument/.env`. Never read or name `.env` in a tool call (the `guard-secrets` hook denies it).
- The committed `models.json` reproduces today's constants exactly: interviewer `claude-opus-5` effort `medium`; guard `claude-haiku-4-5` temperature `0`; simulated expert `claude-sonnet-5` effort `low`; transcriber `scribe_v2`.
- `temperature` is sent only when configured; `effort` only when configured.
- A refusal maps to `LLMRefused`; API error, truncation, empty output map to `LLMUnavailable`, on both backends.
- Logged requests never contain image bytes: images are logged as `{"type": "image", "snapshot": <pid>, "sha256": ...}`.
- `instrument/prompts/` is not edited. Tests: `uv run --directory instrument pytest -q`, all green after every task.
- Tests must not depend on the contents of the committed `models.json`: they use `TEST_MODELS` from `tests/fakes.py` or a temporary file.

## Review Focus

1. An OpenRouter model without strict JSON-schema support returns prose: must surface as `LLMUnavailable` (invalid JSON), never crash the engine. Pinned in Task 3 (`test_interviewer_over_openai_backend_validates_output`).
2. An OpenAI reasoning model rejects `temperature` and `max_tokens`: the backend must send `max_completion_tokens` to `openai` and send `temperature` only when configured. Pinned in Task 2.
3. `models.json` names a provider whose key is missing: `probe-app serve` must stop before the server starts with the key name in the message, not fail on the first interviewer turn mid-session. Pinned in Task 2 (`test_make_backend_names_the_missing_key`) and Task 3 (`test_serve_stops_before_starting_without_a_key`).
4. `models.json` edited after a session was created: the session's `_check_config` must refuse the next probe (drift), because provider and model are frozen fields. Pinned in Task 1.
5. OpenRouter returns `choices == []` or `message.content is None` on an upstream error: must be `LLMUnavailable`. Pinned in Task 2.

---

### Task 1: `models.json` and the frozen configuration

**Files:**
- Create: `instrument/models.json`
- Modify: `instrument/src/probe_app/config.py`
- Modify: `instrument/src/probe_app/transcribe.py:7,104`, `instrument/src/probe_app/cli.py:8,24`
- Modify: `.claude/skills/preflight/preflight.sh:38`
- Test: `instrument/tests/test_config.py`, `instrument/tests/test_cli.py`

**Interfaces:**
- Produces: `config.MODELS_PATH: Path`; `config.RoleModel` (pydantic: `provider: Literal["anthropic","openai","openrouter"]`, `model: str`, `effort: str | None = None`, `temperature: float | None = None`); `config.Models` (`interviewer`, `guard`, `simulated_expert: RoleModel`; `transcriber: TranscriberModel` with `model: str`); `config.load_models(path: Path = MODELS_PATH) -> Models` raising `ConfigMismatch` on invalid content; `config.current_config(prompts_dir=PROMPTS_DIR, models_path=MODELS_PATH) -> FrozenConfig`.
- `FrozenConfig` fields become: `interviewer_provider, interviewer_model, interviewer_effort, guard_provider, guard_model, guard_temperature, transcriber_model, system_prompt_sha256, stems_sha256, guard_prompt_sha256`.
- `INTERVIEWER_MODEL`, `INTERVIEWER_EFFORT`, `GUARD_MODEL` stay in `config.py` until Task 3 deletes them (llm.py still imports them). `TRANSCRIBER_MODEL` is deleted here.

- [ ] **Step 1: Write the failing tests** in `instrument/tests/test_config.py`. Add a fixture and tests, and change `test_current_config_hashes_prompt_files` to read models from the fixture:

```python
import json

MODELS = {
    "interviewer": {"provider": "anthropic", "model": "claude-opus-5", "effort": "medium"},
    "guard": {"provider": "anthropic", "model": "claude-haiku-4-5", "temperature": 0},
    "simulated_expert": {"provider": "anthropic", "model": "claude-sonnet-5", "effort": "low"},
    "transcriber": {"model": "scribe_v2"},
}


@pytest.fixture
def models(tmp_path: Path) -> Path:
    p = tmp_path / "models.json"
    p.write_text(json.dumps(MODELS))
    return p


def test_current_config_hashes_prompt_files(prompts, models):
    cfg = config.current_config(prompts, models)
    assert (cfg.interviewer_provider, cfg.interviewer_model, cfg.interviewer_effort) == ("anthropic", "claude-opus-5", "medium")
    assert (cfg.guard_provider, cfg.guard_model, cfg.guard_temperature) == ("anthropic", "claude-haiku-4-5", 0)
    assert cfg.transcriber_model == "scribe_v2"
    assert cfg.system_prompt_sha256 == config.sha256_file(prompts / "interviewer_system.md")


def test_committed_models_file_is_valid():
    config.load_models()


@pytest.mark.parametrize("bad", [
    {**MODELS, "interviewer": {"provider": "gemini", "model": "x"}},
    {k: v for k, v in MODELS.items() if k != "guard"},
    {**MODELS, "narrator": {"provider": "openai", "model": "x"}},
])
def test_invalid_models_file_is_refused(tmp_path, bad):
    p = tmp_path / "models.json"
    p.write_text(json.dumps(bad))
    with pytest.raises(config.ConfigMismatch, match="models.json"):
        config.load_models(p)


def test_changing_the_interviewer_breaks_the_preregistration(prompts, models, tmp_path):
    prereg = tmp_path / "prereg.json"
    config.freeze(config.current_config(prompts, models), prereg)
    models.write_text(json.dumps({**MODELS, "interviewer": {"provider": "openrouter", "model": "openai/some-model"}}))
    with pytest.raises(config.ConfigMismatch, match="interviewer_provider"):
        config.check_preregistered(config.current_config(prompts, models), prereg)
```

In `instrument/tests/test_cli.py` change the freeze assertion to:

```python
    assert json.loads(target.read_text())["interviewer_model"] == config.load_models().interviewer.model
```

- [ ] **Step 2: Run and watch them fail**

Run: `uv run --directory instrument pytest -q tests/test_config.py tests/test_cli.py`
Expected: FAIL (`current_config() takes ... positional argument`, `no attribute load_models`).

- [ ] **Step 3: Create `instrument/models.json`**

```json
{
  "interviewer": {"provider": "anthropic", "model": "claude-opus-5", "effort": "medium"},
  "guard": {"provider": "anthropic", "model": "claude-haiku-4-5", "temperature": 0},
  "simulated_expert": {"provider": "anthropic", "model": "claude-sonnet-5", "effort": "low"},
  "transcriber": {"model": "scribe_v2"}
}
```

- [ ] **Step 4: Implement in `config.py`**

Add after the path constants, delete `TRANSCRIBER_MODEL`:

```python
from typing import Literal

from pydantic import BaseModel, ConfigDict, ValidationError

MODELS_PATH = INSTRUMENT_DIR / "models.json"


class RoleModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    provider: Literal["anthropic", "openai", "openrouter"]
    model: str
    effort: str | None = None
    temperature: float | None = None


class TranscriberModel(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    model: str


class Models(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)
    interviewer: RoleModel
    guard: RoleModel
    simulated_expert: RoleModel
    transcriber: TranscriberModel


def load_models(path: Path = MODELS_PATH) -> Models:
    try:
        return Models.model_validate_json(path.read_text())
    except ValidationError as e:
        raise ConfigMismatch(f"{path.name} is invalid: {e}") from e
```

`ConfigMismatch` must be defined above `load_models`. Replace `FrozenConfig` and `current_config`:

```python
@dataclass(frozen=True)
class FrozenConfig:
    interviewer_provider: str
    interviewer_model: str
    interviewer_effort: str | None
    guard_provider: str
    guard_model: str
    guard_temperature: float | None
    transcriber_model: str
    system_prompt_sha256: str
    stems_sha256: str
    guard_prompt_sha256: str


def current_config(prompts_dir: Path = PROMPTS_DIR, models_path: Path = MODELS_PATH) -> FrozenConfig:
    m = load_models(models_path)
    return FrozenConfig(
        interviewer_provider=m.interviewer.provider,
        interviewer_model=m.interviewer.model,
        interviewer_effort=m.interviewer.effort,
        guard_provider=m.guard.provider,
        guard_model=m.guard.model,
        guard_temperature=m.guard.temperature,
        transcriber_model=m.transcriber.model,
        system_prompt_sha256=sha256_file(prompts_dir / "interviewer_system.md"),
        stems_sha256=sha256_file(prompts_dir / "stems.json"),
        guard_prompt_sha256=sha256_file(prompts_dir / "guard_system.md"),
    )
```

- [ ] **Step 5: Move the transcriber default off the deleted constant**

`transcribe.py`: replace the `TRANSCRIBER_MODEL` import with `from probe_app.config import load_models`, and:

```python
def make_transcriber(model: str | None = None, client=None) -> Transcriber:
    model = model or load_models().transcriber.model
    if model.startswith("scribe"):
        return ScribeTranscriber(model, client)
    return OpenAITranscriber(model, client)
```

`cli.py`: drop `TRANSCRIBER_MODEL` from the import; `tr.add_argument("--model", default=None, help="default: models.json transcriber; scribe_v2 or whisper-1")`.

`.claude/skills/preflight/preflight.sh` line 38:

```bash
  models=$(py 'from probe_app.config import load_models; print(load_models().transcriber.model)')
```

- [ ] **Step 6: Run the whole suite**

Run: `uv run --directory instrument pytest -q`
Expected: all pass (93 + 5 new = 98, counting the parametrized cases as 3).

- [ ] **Step 7: Commit**

```bash
git add instrument/models.json instrument/src/probe_app/config.py instrument/src/probe_app/transcribe.py instrument/src/probe_app/cli.py instrument/tests/test_config.py instrument/tests/test_cli.py .claude/skills/preflight/preflight.sh
git commit -m "Models chosen in instrument/models.json; provider and model per role enter the frozen config"
```

---

### Task 2: Provider backends

**Files:**
- Create: `instrument/src/probe_app/backends.py`
- Modify: `instrument/src/probe_app/llm.py:43-48` (exceptions move to `backends.py`, re-imported)
- Test: create `instrument/tests/test_backends.py`; add `FakeOpenAI` and `TEST_MODELS` to `instrument/tests/fakes.py`

**Interfaces:**
- Consumes: `config.RoleModel`, `config.Models` (Task 1).
- Produces, in `probe_app.backends`: `LLMRefused`, `LLMUnavailable` (re-exported by `probe_app.llm`, so existing imports keep working); `Part(text: str | None = None, png: bytes | None = None, name: str = "", cache: bool = False)`; `AnthropicBackend(client, role: RoleModel)`; `OpenAICompatBackend(client, role: RoleModel)`; both with `complete(kind: str, system: str, parts: list[Part], schema: dict | None, max_tokens: int, log: Callable[[dict], object], thinking: bool = False) -> str`; `make_backend(name: str, role: RoleModel, env: Mapping[str, str] = os.environ)` raising `ValueError` naming the missing key; `Backends(interviewer, guard)` dataclass; `make_backends(models: Models, env=os.environ) -> Backends`.
- In `tests/fakes.py`: `TEST_MODELS: Models` (the four values from Global Constraints), `FakeOpenAI(responses: list)` with `.calls` and `.chat.completions.create(**kw)`, `openai_response(content: str | None, finish_reason="stop", refusal=None)`.

- [ ] **Step 1: Confirm the openai 3.19 chat-completions surface**

Use context7 (`resolve-library-id` "openai-python", then `query-docs` on "chat completions response_format json_schema strict refusal max_completion_tokens reasoning_effort") and OpenRouter's docs (`ctx_fetch_and_index` https://openrouter.ai/docs/api-reference/overview). Confirm: `client.chat.completions.create` still exists in 3.x; `message.refusal`; `finish_reason` values `length` and `content_filter`; `max_completion_tokens` (OpenAI) versus `max_tokens` (OpenRouter); OpenRouter's `reasoning: {"effort": ...}`. If any name differs, use the documented one in Steps 3–5 and note it in the commit message.

- [ ] **Step 2: Add fakes to `instrument/tests/fakes.py`**

```python
from probe_app.config import Models

TEST_MODELS = Models.model_validate({
    "interviewer": {"provider": "anthropic", "model": "claude-opus-5", "effort": "medium"},
    "guard": {"provider": "anthropic", "model": "claude-haiku-4-5", "temperature": 0},
    "simulated_expert": {"provider": "anthropic", "model": "claude-sonnet-5", "effort": "low"},
    "transcriber": {"model": "scribe_v2"},
})


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
```

Change `FakeAnthropic.create` routing to `role = "guard" if kwargs["model"] == TEST_MODELS.guard.model else "interviewer"` and delete the `GUARD_MODEL` import.

- [ ] **Step 3: Write the failing tests** in `instrument/tests/test_backends.py`

```python
import json

import httpx2
import openai
import pytest

from fakes import TEST_MODELS, FakeAnthropic, FakeOpenAI, FakeResponse, openai_response
from probe_app.backends import (AnthropicBackend, LLMRefused, LLMUnavailable, OpenAICompatBackend, Part,
                                make_backend, make_backends)
from probe_app.config import RoleModel

PNG = bytes.fromhex("89504e470d0a1a0a")
SCHEMA = {"type": "object", "additionalProperties": False, "required": ["a"], "properties": {"a": {"type": "string"}}}
PARTS = [Part(text="static"), Part(png=PNG, name="A1", cache=True), Part(text="dynamic")]


def oa(provider="openai", **kw) -> OpenAICompatBackend:
    return OpenAICompatBackend(kw.pop("client"), RoleModel(provider=provider, model="m", **kw))


def test_openai_request_shape():
    client = FakeOpenAI([openai_response('{"a": "x"}')])
    logged = []
    text = oa(client=client, effort="high").complete("interviewer", "SYS", PARTS, SCHEMA, 500, logged.append)
    assert text == '{"a": "x"}'
    call = client.calls[0]
    assert call["messages"][0] == {"role": "system", "content": "SYS"}
    image = call["messages"][1]["content"][1]
    assert image["type"] == "image_url" and image["image_url"]["url"].startswith("data:image/png;base64,")
    assert call["response_format"]["json_schema"]["strict"] is True
    assert call["max_completion_tokens"] == 500 and "max_tokens" not in call
    assert call["reasoning_effort"] == "high"
    assert "temperature" not in call
    assert "base64" not in json.dumps(logged[0]["request"])


def test_openrouter_uses_its_own_token_and_reasoning_fields():
    client = FakeOpenAI([openai_response("ok")])
    oa("openrouter", client=client, effort="low", temperature=0).complete("guard", "S", [Part(text="t")], None, 50,
                                                                          lambda r: None)
    call = client.calls[0]
    assert call["max_tokens"] == 50 and "max_completion_tokens" not in call
    assert call["extra_body"] == {"reasoning": {"effort": "low"}}
    assert call["temperature"] == 0
    assert "response_format" not in call


@pytest.mark.parametrize("response, exc", [
    (openai_response(None, refusal="I can't help with that."), LLMRefused),
    (openai_response("", finish_reason="content_filter"), LLMRefused),
    (openai_response('{"a": "tr', finish_reason="length"), LLMUnavailable),
    (openai_response(None), LLMUnavailable),
])
def test_openai_outcomes_map_to_the_two_exceptions(response, exc):
    with pytest.raises(exc):
        oa(client=FakeOpenAI([response])).complete("interviewer", "S", PARTS, SCHEMA, 10, lambda r: None)


def test_openai_empty_choices_is_unavailable():
    empty = openai_response("x")
    empty.choices = []
    with pytest.raises(LLMUnavailable):
        oa(client=FakeOpenAI([empty])).complete("interviewer", "S", PARTS, SCHEMA, 10, lambda r: None)


def test_openai_api_error_is_unavailable_and_logged():
    err = openai.APIConnectionError(request=httpx2.Request("POST", "https://api.openai.com"))
    logged = []
    with pytest.raises(LLMUnavailable):
        oa(client=FakeOpenAI([err])).complete("interviewer", "S", PARTS, SCHEMA, 10, logged.append)
    assert "error" in logged[0]


def test_anthropic_sends_temperature_only_when_configured():
    client = FakeAnthropic(interviewer=[FakeResponse({"a": "x"})], guard=[FakeResponse({"a": "y"})])
    AnthropicBackend(client, TEST_MODELS.interviewer).complete("interviewer", "S", PARTS, SCHEMA, 10, lambda r: None)
    AnthropicBackend(client, TEST_MODELS.guard).complete("guard", "S", [Part(text="t")], SCHEMA, 10, lambda r: None)
    assert "extra_body" not in client.calls[0]
    assert client.calls[1]["extra_body"] == {"temperature": 0}


def test_make_backend_names_the_missing_key():
    role = RoleModel(provider="openrouter", model="openai/x")
    with pytest.raises(ValueError, match="OPENROUTER_API_KEY"):
        make_backend("interviewer", role, env={})


def test_make_backends_picks_backend_per_provider():
    env = {"ANTHROPIC_API_KEY": "a", "OPENROUTER_API_KEY": "o"}
    models = TEST_MODELS.model_copy(update={"interviewer": RoleModel(provider="openrouter", model="openai/x")})
    b = make_backends(models, env)
    assert isinstance(b.interviewer, OpenAICompatBackend) and isinstance(b.guard, AnthropicBackend)
    assert str(b.interviewer.client.base_url).startswith("https://openrouter.ai/api/v1")
```

`openai.APIConnectionError` takes an `httpx.Request`; the project's Anthropic tests use the `httpx2` package for the same purpose. If openai 3.19 needs plain `httpx`, import that instead.

- [ ] **Step 4: Run and watch them fail**

Run: `uv run --directory instrument pytest -q tests/test_backends.py`
Expected: FAIL with `ModuleNotFoundError: probe_app.backends`.

- [ ] **Step 5: Implement `instrument/src/probe_app/backends.py`**

```python
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
        if self.role.effort:
            if self.role.provider == "openrouter":
                params["extra_body"] = {"reasoning": {"effort": self.role.effort}}
            else:
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
```

In `llm.py`, delete the `LLMUnavailable` and `LLMRefused` class definitions and add `from probe_app.backends import LLMRefused, LLMUnavailable` so `engine.py` and the tests keep importing them from `probe_app.llm`.

- [ ] **Step 6: Run the suite**

Run: `uv run --directory instrument pytest -q`
Expected: all pass.

- [ ] **Step 7: Commit**

```bash
git add instrument/src/probe_app/backends.py instrument/src/probe_app/llm.py instrument/tests/test_backends.py instrument/tests/fakes.py
git commit -m "Anthropic and OpenAI-compatible backends behind one complete() call; refusals and outages map alike"
```

---

### Task 3: Route every role through its backend

**Files:**
- Modify: `instrument/src/probe_app/llm.py` (`_call`, `InterviewerLLM`, `Guard`), `instrument/src/probe_app/simulate.py`, `instrument/src/probe_app/session.py:30-32,268-272`, `instrument/src/probe_app/cli.py:41-63`, `instrument/src/probe_app/config.py` (delete the three leftover constants)
- Test: `instrument/tests/test_llm.py`, `instrument/tests/test_session.py`, `instrument/tests/test_server.py`, `instrument/tests/test_simulate.py`, `instrument/tests/fakes.py`, `instrument/tests/test_cli.py`

**Interfaces:**
- Consumes: `Part`, `AnthropicBackend`, `Backends`, `make_backend`, `make_backends`, `TEST_MODELS`, `FakeOpenAI`, `openai_response` (Task 2); `load_models` (Task 1).
- Produces: `InterviewerLLM(backend, log, system_prompt)`; `Guard(backend, log, system_prompt)`; `SimulatedExpert(backend)`; `Deps(transcriber, backends: Backends)`; `fakes.fake_backends(client: FakeAnthropic) -> Backends`.

- [ ] **Step 1: Add `fake_backends` to `tests/fakes.py`**

```python
from probe_app.backends import AnthropicBackend, Backends


def fake_backends(client) -> Backends:
    return Backends(interviewer=AnthropicBackend(client, TEST_MODELS.interviewer),
                    guard=AnthropicBackend(client, TEST_MODELS.guard))
```

- [ ] **Step 2: Update the tests to the new constructors (they fail until Step 4)**

- `test_llm.py`: every `InterviewerLLM(client, ...)` becomes `InterviewerLLM(AnthropicBackend(client, TEST_MODELS.interviewer), ...)`, every `Guard(client, ...)` becomes `Guard(AnthropicBackend(client, TEST_MODELS.guard), ...)`; import `AnthropicBackend` from `probe_app.backends` and `TEST_MODELS` from `fakes`. The existing assertions stay unchanged: they pin that the Anthropic request is byte-for-byte what it was.
- `test_session.py` (lines 17, 39, 179), `test_server.py` (18, 97, 112), `test_simulate.py` (21): wrap the client: `Deps(..., fake_backends(FakeAnthropic(...)))`.
- Add to `test_llm.py` an interviewer run over the OpenAI-compatible backend, which pins Review Focus 1:

```python
def test_interviewer_over_openai_backend_validates_output():
    from fakes import FakeOpenAI, openai_response
    from probe_app.backends import OpenAICompatBackend
    from probe_app.config import RoleModel

    role = RoleModel(provider="openrouter", model="openai/x")
    ok = FakeOpenAI([openai_response(json.dumps(turn_payload()))])
    assert InterviewerLLM(OpenAICompatBackend(ok, role), lambda r: None, "S").next_turn(request()).stem_id == "cues"
    prose = FakeOpenAI([openai_response("Sure! Here's a question: what did you notice?")])
    with pytest.raises(LLMUnavailable):
        InterviewerLLM(OpenAICompatBackend(prose, role), lambda r: None, "S").next_turn(request())
```

(add `import json` at the top of `test_llm.py`).

- `test_simulate.py`: add

```python
def test_simulated_expert_calls_its_backend():
    from fakes import FakeOpenAI, openai_response
    from probe_app.backends import OpenAICompatBackend
    from probe_app.config import RoleModel
    from probe_app.simulate import SimulatedExpert

    client = FakeOpenAI([openai_response("  I looked at the collision first.  ")])
    expert = SimulatedExpert(OpenAICompatBackend(client, RoleModel(provider="openai", model="m")))
    assert expert.answer({"A1": "p"}, "t", []) == "I looked at the collision first."
```

- `test_cli.py`: add

```python
def test_serve_stops_before_starting_without_a_key(monkeypatch):
    import uvicorn

    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: None)
    for key in ("ANTHROPIC_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setattr(uvicorn, "run", lambda *a, **k: pytest.fail("server started without a key"))
    with pytest.raises(ValueError, match="_API_KEY"):
        cli.main(["serve"])
```

(add `import pytest` at the top of `test_cli.py`).

- [ ] **Step 3: Run and watch them fail**

Run: `uv run --directory instrument pytest -q`
Expected: FAIL (`Deps.__init__` / `InterviewerLLM` signature errors; the serve test fails because the server starts, or constructs `anthropic.Anthropic()` without complaint).

- [ ] **Step 4: Rewire `llm.py`**

Delete `_call` and the config-constant import. Import `from dataclasses import replace` and `from probe_app.backends import LLMRefused, LLMUnavailable, Part`. Then:

```python
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
```

Remove the now-unused `base64`, `hashlib` and `anthropic` imports from `llm.py`.

- [ ] **Step 5: Rewire `simulate.py`, `session.py`, `config.py`, `cli.py`**

`simulate.py`: delete `EXPERT_MODEL` and its comment (the reason now lives in `models.json`'s choice and the pilot protocol); import `Part` from `probe_app.backends`;

```python
class SimulatedExpert:
    def __init__(self, backend):
        self.backend = backend

    def answer(self, problems: dict[str, str], transcript: str, dialogue: list[DialogueTurn]) -> str:
        history = "\n".join(f"{d.speaker.upper()}: {d.text}" for d in dialogue)
        problem_text = "\n".join(f"{p}: {t}" for p, t in problems.items())
        prompt = (f"{EXPERT_PROMPT}\n\nPROBLEMS\n{problem_text}\n\n"
                  f"DR. LEE'S THINK-ALOUD\n{transcript}\n\nINTERVIEW SO FAR\n{history}")
        return self.backend.complete("simulated_expert", "", [Part(text=prompt)], None, 2000, lambda r: None).strip()
```

`session.py`: `Deps` becomes

```python
@dataclass
class Deps:
    transcriber: object
    backends: Backends
```

(import `Backends` from `probe_app.backends`), and in `_engine`:

```python
        llm = InterviewerLLM(self.deps.backends.interviewer, self.store.log_llm, load_prompt("interviewer_system.md"))
        guard = Guard(self.deps.backends.guard, self.store.log_llm, load_prompt("guard_system.md"))
```

`config.py`: delete `INTERVIEWER_MODEL`, `INTERVIEWER_EFFORT`, `GUARD_MODEL`.

`cli.py`, `serve` and `simulate` branches:

```python
    elif args.cmd == "serve":
        import uvicorn

        from probe_app.backends import make_backends
        from probe_app.server import create_app
        from probe_app.session import Deps
        from probe_app.transcribe import make_transcriber

        backends = make_backends(load_models())
        app = create_app(args.root, Deps(make_transcriber(), backends))
        uvicorn.run(app, host=args.host, port=args.port,
                    ssl_certfile=args.ssl_certfile, ssl_keyfile=args.ssl_keyfile)
    elif args.cmd == "simulate":
        from probe_app.backends import make_backend, make_backends
        from probe_app.session import Deps
        from probe_app.simulate import FixtureTranscriber, SimulatedExpert, run_simulation

        models = load_models()
        expert = SimulatedExpert(make_backend("simulated expert", models.simulated_expert))
        fixture = json.loads((INSTRUMENT_DIR / "problems" / "simulated_think_aloud.json").read_text())
        sid = run_simulation(args.root, Deps(FixtureTranscriber(fixture), make_backends(models)), expert,
                             args.set_order.split(","))
        print(f"simulated session: {args.root / sid}")
```

Add `load_models` to the `probe_app.config` import in `cli.py`. A missing key raises `ValueError` before `uvicorn.run`; let it propagate (the traceback ends with the key name).

- [ ] **Step 6: Run the suite and grep for leftovers**

Run: `uv run --directory instrument pytest -q && grep -rnE "INTERVIEWER_MODEL|INTERVIEWER_EFFORT|GUARD_MODEL|EXPERT_MODEL|anthropic_client" instrument/src instrument/tests .claude/skills`
Expected: all tests pass; grep prints nothing.

- [ ] **Step 7: Commit**

```bash
git add instrument/src instrument/tests
git commit -m "Interviewer, guard and simulated expert call the backend models.json names"
```

---

### Task 4: Reporting, protocol, live check

**Files:**
- Modify: `.claude/skills/session-report/report.py:19-21`, `instrument/pilot-protocol.md` ("Before the session" item 1, "Refusals"), `CLAUDE.md` (test count)

**Interfaces:**
- Consumes: the `FrozenConfig` field names from Task 1 as stored in `manifest["config"]`.

- [ ] **Step 1: Session report prints provider and model per role**

In `report.py` replace the `config:` print with (older manifests lack the provider keys, hence `.get`):

```python
    print(f"config: interviewer {cfg.get('interviewer_provider', 'anthropic')}:{cfg['interviewer_model']} "
          f"effort={cfg['interviewer_effort']} guard {cfg.get('guard_provider', 'anthropic')}:{cfg['guard_model']} "
          f"transcriber={cfg['transcriber_model']} commit={manifest['git_commit'][:7]}")
```

Run: `uv run --directory instrument python ../.claude/skills/session-report/report.py ../sessions/SIM-2980899a | head -3`
Expected: the `config:` line shows `interviewer anthropic:claude-opus-5`.

- [ ] **Step 2: Pilot protocol**

In `instrument/pilot-protocol.md`, "Before the session" item 1, replace the fixed processor list with: the consent form names every provider in `instrument/models.json` (interviewer, guard, transcriber) as a processor, with its data-processing terms and retention confirmed; if a role uses `openrouter`, name OpenRouter and the upstream provider of the chosen model. In "Refusals", replace "a different interviewer model" with "a different interviewer model or provider in `models.json`".

- [ ] **Step 3: CLAUDE.md test count**

Run `uv run --directory instrument pytest -q | tail -1` and put the count into the Tests line of `CLAUDE.md`.

- [ ] **Step 4: Validity review**

Launch the `validity-reviewer` agent on `git diff 737aa8e..HEAD -- instrument/`. Fix anything it marks BLOCKING, test-first.

- [ ] **Step 5: Live check**

Run `bash .claude/skills/preflight/preflight.sh pilot` (timeout 600000 ms). Expected: `PASS simulation` with the committed Anthropic `models.json`, confirming the refactor changed no live behaviour. Trying an OpenAI or OpenRouter interviewer is the researcher's pilot step: edit `models.json` and rerun the same command.

- [ ] **Step 6: Commit**

```bash
git add .claude/skills/session-report/report.py instrument/pilot-protocol.md CLAUDE.md
git commit -m "Session report and pilot protocol name the provider per role"
```
