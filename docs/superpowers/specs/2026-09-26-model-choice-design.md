# Model choice for the Stage A instrument

## Why

Every LLM in `instrument/` is a hardcoded Anthropic model: `INTERVIEWER_MODEL`, `GUARD_MODEL` in `probe_app/config.py`, `EXPERT_MODEL` in `probe_app/simulate.py`. The researcher wants to choose them, in particular to try OpenAI models as the interviewer because they may sound more human, and to reach any model through OpenRouter.

Constraint from the design (`research/experiment-ai-assisted-cta-physics.md`): within the study every expert meets the same interviewer, so the choice is per study, fixed at `probe-app freeze` and enforced by `prereg.json`. Pilots are where models are compared.

## Decisions

- One committed file, `instrument/models.json`, holds the choice for every role. No CLI flags, no per-session choice, no console dropdown.
- Two backends: native Anthropic, and one OpenAI-compatible backend serving both `openai` and `openrouter`. No LiteLLM.

## `models.json`

```json
{
  "interviewer":      {"provider": "anthropic", "model": "claude-opus-5", "effort": "medium"},
  "guard":            {"provider": "anthropic", "model": "claude-haiku-4-5", "temperature": 0},
  "simulated_expert": {"provider": "anthropic", "model": "claude-sonnet-5", "effort": "low"},
  "transcriber":      {"model": "scribe_v2"}
}
```

- `provider`: `anthropic` | `openai` | `openrouter`. `model`: the provider's own id (`openai/<model>` style for OpenRouter).
- `effort` (optional): Anthropic `output_config.effort`; OpenAI `reasoning_effort`; OpenRouter `reasoning.effort`.
- `temperature` (optional): sent only when present, because reasoning models reject it.
- The initial file reproduces today's constants exactly, so the change is behaviour-neutral until someone edits it.
- Loaded and validated by a pydantic model in `config.py`; an unknown provider or role, or a missing field, fails at load with the file name in the message.

## Frozen configuration

`FrozenConfig` gains `interviewer_provider`, `guard_provider`, and the optional `effort`/`temperature` of the interviewer and guard, next to the existing model fields. `current_config()` reads them from `models.json`. `check_preregistered` then refuses a data session on any drift, as today. The simulated expert is not frozen: it never meets a real expert.

## LLM layer (`probe_app/llm.py`)

A backend exposes one call:

```python
complete(kind: str, system: str, parts: list[Part], schema: dict, max_tokens: int) -> str
```

`Part` is text or a PNG. Both backends raise `LLMRefused` for a refusal and `LLMUnavailable` for API errors, truncation or empty output. The `interviewer_refused`/`interviewer_unavailable` counts and preflight's 1-in-10 rule depend on that mapping being the same on both.

| | Anthropic | OpenAI-compatible |
|---|---|---|
| Client | `anthropic.Anthropic()` | `openai.OpenAI()`; OpenRouter adds `base_url="https://openrouter.ai/api/v1"`, `OPENROUTER_API_KEY` |
| Schema | `output_config.format` json_schema | `response_format` json_schema, `strict: true` |
| Images | base64 image block | `image_url` data URI |
| Caching | `cache_control` on the last static block, as today | none (provider-side automatic caching only) |
| Thinking | `thinking: adaptive` for the interviewer, as today | via `effort` only |
| Refused | `stop_reason == "refusal"` | `message.refusal` set, or `finish_reason == "content_filter"` |
| Unavailable | API error, `max_tokens`, no text | API error, `finish_reason == "length"`, empty content |

`InterviewerLLM`, `Guard` and `SimulatedExpert` build `Part`s and call their backend; their prompts, schemas and validation are unchanged. Logged requests record provider and model, and images stay logged by hash only.

`Deps.anthropic_client` becomes `Deps.backends`: a mapping from role to backend, built by `make_backends(models)` in `cli.py`. `make_backends` fails before the server starts if a role's key (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY`) is missing.

## Transcriber

`TRANSCRIBER_MODEL` moves into `models.json` (`transcriber.model`); `make_transcriber` and preflight read it from there. Transcriber providers are unchanged.

## Checks and reporting

- Preflight's live simulated session already runs the configured interviewer and guard, so it exercises an OpenRouter model's vision and strict-schema support. A model without them shows up as `interviewer_unavailable` and the fallback warning.
- `/session-report` prints provider and model per role from the manifest.
- `pilot-protocol.md` "Before the session" item 1: the processors named on the consent form are the providers in `models.json`. Using OpenRouter means naming OpenRouter, which forwards transcripts and images to the upstream provider of the chosen model.

## Tests

- A `FakeOpenAI` in `tests/fakes.py` returning valid JSON, `refusal`, `content_filter`, `length`, empty content and invalid JSON; each maps to the right result or exception for both the interviewer and the guard.
- The OpenAI-compatible request carries `strict` schema, a data-URI image, `temperature` only when configured, and the OpenRouter base URL for `openrouter`.
- `models.json` load: valid file, unknown provider, missing role.
- `current_config` reflects `models.json`, and editing it makes `check_preregistered` fail.
- `make_backends` fails with a named missing key.
- Existing Anthropic tests pass unchanged apart from construction.

## Out of scope

Per-session or console model choice; a fallback model chain; non-OpenAI-compatible providers (Gemini native, local models) except through OpenRouter.

## Validity notes

- A model change is a frozen-config change: it needs a pilot or simulated run, `validity-reviewer`, and a new freeze before data sessions.
- Behaviour across providers is not equivalent (guard strictness, refusal rates, answer style). Compare models on pilots, choose one, freeze it; never mix within the study.
