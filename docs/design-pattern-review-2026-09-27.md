# Pattern review: `instrument/` (2026-09-27)

Scope: `instrument/src/probe_app`, `instrument/src/probe_code`, `instrument/web/js`, at commit 30a2b8e. Test suite: 131 passed. Audio-recording extraction from `session.py` is covered by decision 0003 and not repeated here.

## Findings

1. **Two sources of truth for the LLM output shapes, already drifting.** `INTERVIEWER_TURN_SCHEMA` and `GUARD_SCHEMA` (`instrument/src/probe_app/llm.py:9-37`) are hand-written JSON Schemas that mirror the Pydantic models `InterviewerTurn` and `GuardVerdict` (`instrument/src/probe_app/models.py:23-47`), 9 fields in all. Nothing ties them together: neither dict is referenced by any test. They already differ: `GUARD_SCHEMA` sets `additionalProperties: false`, while `GuardVerdict` has no `extra="forbid"`. · Fix: **single source of truth**. In Python, keep the dicts, because strict structured output needs every field required and no `$ref`/`title`/`default`, which `model_json_schema()` does not emit as-is. Add one parametrised test asserting that each schema's properties, `required` and enums equal the model's fields and `Literal` values, and add `extra="forbid"` to `GuardVerdict`. · Why: a field added to one side only fails at runtime as `LLMUnavailable` on every turn, which falls back to bare stems silently. · Effort: small.

2. **The Guard is built in two places, and the second has already broken once.** `Guard(backend, log, load_prompt("guard_system.md"))` appears at `instrument/src/probe_app/session.py:288` and `instrument/src/probe_code/cli.py:67`. The CLI copy raised `AttributeError` after the constructor changed in 3871d71, with the suite green (`docs/lessons.md`, "A constructor change broke a CLI command the suite never ran"). · Fix: **Factory Function**. In Python, write a plain `make_guard(backend, log)`, and the same for the interviewer, in `llm.py` next to the classes. It loads its own prompt, and both call sites use it. · Why: one construction site means a signature change breaks in one place, and that place is covered by tests. · Effort: small.

## Leave as-is

- **Backend strategy** (`backends.py:42-162`): two classes behind one `complete(...)`, chosen by `make_backend`. That is Strategy done with duck typing, not an ABC. The three `openrouter` conditionals inside `OpenAICompatBackend` (`:107`, `:113`, `:150`) are provider quirks within one strategy, not a type switch.
- **Session phase machine** (`session.py:57`, `:135`): 6 phases as a `Literal`, one `_require` guard and 6 assignment sites. A State class hierarchy would be pure ceremony at this size.
- **AI/human arm branching** (`session.py`, 9 `ai`/`human` checks): fine with two fixed arms. Reopen as a **Strategy** (one arm object with `start`/`answer`/`finish`/`view`) only if the deferred decoding-interview arm is ever added, since that would touch all 9 sites.
- **Resources**: all 7 file accesses use `with`; there is no `try`/`finally` cleanup to replace.
- **Module-level constants** (`config.py:10-17`, `backends.py:12-13`) instead of singletons or config objects.
- **CLI dispatch** (`probe_app/cli.py`, `probe_code/cli.py`: 4 and 5 `elif` branches on the argparse subcommand): too few branches to justify a command registry.
- **Frontend** (`web/js/expert.js`, 229 lines and 17 functions; `console.js`, 104 lines; 3 `fetch` calls each): plain functions with no framework, which is right-sized.

## Out of this lens (for `validity-reviewer`)

The output schemas and the per-turn message template (`llm.py:9-37`, `:65-81`) shape what the interviewer and guard produce, but `FrozenConfig` (`config.py:63-77`) hashes only the three prompt files. A committed edit to `llm.py` after `probe-app freeze` would pass `check_preregistered`.
