---
id: 0002
status: proposed
skill: migrate
date: 2026-09-27
commit: 30a2b8e
rules:
  - id: models-json-single-source
    statement: Every LLM role (interviewer, guard, simulated expert) and the transcriber are chosen only in instrument/models.json; there are no CLI flags, per-session choices or console controls for model choice.
    scope: ["instrument/src/probe_app/**", "instrument/models.json"]
    severity: blocking
    verification: narrative
  - id: model-choice-is-frozen-config
    statement: The interviewer's and guard's provider, model, effort and temperature are part of the frozen configuration, so a change to them blocks data sessions until a new freeze; one model per role for the whole study, never mixed.
    scope: ["instrument/src/probe_app/**", "instrument/models.json"]
    severity: blocking
    verification: narrative
  - id: two-backends-behind-one-call
    statement: LLM calls go through the backend interface in probe_app/llm.py, with exactly two backends, native Anthropic and one OpenAI-compatible backend serving openai and openrouter; no LiteLLM or other routing library.
    scope: ["instrument/src/probe_app/**"]
    severity: warning
    verification: narrative
  - id: uniform-refusal-mapping
    statement: Both backends raise LLMRefused for a refusal and LLMUnavailable for API errors, truncation or empty output, so refusal and outage counts mean the same on every provider.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: missing-key-fails-before-start
    statement: Building the backends fails before the server starts, naming the variable, if a configured role's API key is missing.
    scope: ["instrument/src/probe_app/**"]
    severity: warning
    verification: narrative
---
# Model choice in one committed file, two backends

## Context

The instrument's LLMs were hard-coded Anthropic constants in `config.py` and `simulate.py`. The researcher wanted to choose them, in particular to try OpenAI models as the interviewer and to reach any model through OpenRouter. The experiment design requires every expert in the study to meet the same interviewer, so the choice is per study, fixed at `probe-app freeze` and enforced by `prereg.json`; pilots are where models are compared.

## Decision

- One committed file, `instrument/models.json`, holds the provider, model and optional effort and temperature for every role, plus the transcriber model. It is validated at load; an unknown provider or role, or a missing field, fails with the file name.
- The interviewer and guard settings join the frozen configuration; the simulated expert does not, since it never meets a real expert.
- Two backends expose one `complete(...)` call: native Anthropic, and one OpenAI-compatible backend for `openai` and `openrouter`. Both map refusals and outages to the same two exceptions, because the `interviewer_refused` / `interviewer_unavailable` counts and preflight's refusal rule depend on that mapping.
- Out of scope: per-session or console choice, fallback model chains, and non-OpenAI-compatible providers except through OpenRouter.

All rules are `narrative`; no checker configuration exists in this repository to bind them to.

## Consequences (cost)

- Behaviour is not equivalent across providers (guard strictness, refusal rates, answer style), so a model change is a frozen-config change needing a pilot or simulated run, `validity-reviewer` and a new freeze.
- The OpenAI-compatible path has no explicit prompt caching and gets thinking only through `effort`, so cost and latency differ by provider.
- Using OpenRouter adds OpenRouter and the upstream provider as data processors to be named on the consent form.

## Sources

- `docs/superpowers/specs/2026-09-26-model-choice-design.md` at commit 30a2b8e: "Why", "Decisions", "`models.json`", "Frozen configuration", "LLM layer", "Out of scope" and "Validity notes".
- It supersedes the Stage A spec's single-provider stack line (see decision 0001's Sources).
