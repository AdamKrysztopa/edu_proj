---
id: 0004
status: proposed
skill: agentic-patterns
date: 2026-09-27
commit: 30a2b8e
rules:
  - id: freeze-covers-model-facing-code
    statement: The frozen configuration includes a hash of every source file that builds what the interviewer or guard is sent or decides what reaches the expert (at least probe_app/llm.py, engine.py, contract.py and models.py), and a data session is refused when it differs from prereg.json.
    scope: ["instrument/src/probe_app/**"]
    severity: blocking
    verification: narrative
  - id: guard-calibrated-before-freeze
    statement: Before probe-app freeze the leading-question guard is run over a labelled set of about 60 probe questions (two labellers, kappa reported), and its sensitivity and specificity with 95% CIs are pre-registered with the guard prompt; any change to the guard model or prompt repeats the calibration.
    scope: ["instrument/prompts/**", "instrument/src/probe_code/**"]
    severity: blocking
    verification: narrative
  - id: freeze-by-computed-rule
    statement: The interviewer configuration is frozen only when a pre-stated rule over measured pilot and simulated-session metrics passes, computed by code from the session logs; the outcome is accept, change one variable and re-run, or change the model.
    scope: ["instrument/src/probe_code/**", "instrument/pilot-protocol.md"]
    severity: blocking
    verification: narrative
  - id: rules-not-agents-decide
    statement: The freeze and the study gates (K0, K1, K2) are decided by pre-registered rules applied by code to measured results, never by an LLM agent.
    scope: ["instrument/**", "research/experiment-ai-assisted-cta-physics.md"]
    severity: blocking
    verification: narrative
---
# A data-driven freeze for the Stage A interviewer

## Context

A review of `instrument/` through three lenses (agent design, tests, design patterns) on 2026-09-27 found the interviewer at the right autonomy. It is one structured call per turn inside a code workflow, a generator plus a guard, with bounded retries, a time cap and full logging. The same review found that `probe-app freeze`, the point after which every expert must meet the same interviewer, rests on three unmeasured or unchecked things:

- **The freeze misses code.** `FrozenConfig` (`instrument/src/probe_app/config.py:62-111`) hashes the prompt files and reads `models.json`. It does not cover the per-turn message template, the wrap-up and rejection text, the output schemas, the guard's user template or the contract rules in `llm.py`, `engine.py` and `contract.py`, so a committed edit to them after the freeze passes `check_preregistered` (`docs/lessons.md`).
- **The guard is uncalibrated.** It is the only semantic check that an AI question does not lead the expert. The tests drive it with scripted verdicts, and `probe-code guard-audit` reports flag rates, never whether a flag was right. The agent and test lenses both named it the highest-leverage gap.
- **The freeze choice has no rule.** Pilots measure latency, refusals, contract and guard rejections and fallbacks (`instrument/pilot-protocol.md`), but only latency (median under 6 s) and refusals (about 1 in 10) have thresholds. `models.json` makes model switches easy, and one has already broken behaviour the fakes could not show.

The user asked for the system's decisions to be data-driven. The review's reading is that the data should drive rules applied by code, not an agent: the decisions here are pre-registered gates whose value depends on nobody exercising judgement at decision time.

## Decision

| Layer | Pattern | Why it's here | Watch out for |
|-------|---------|---------------|---------------|
| Governance | Freeze by data flow: the frozen set is everything that reaches the model or decides what reaches the expert, whether a prompt file or code | Closes the gap where code changes the interviewer after pre-registration | Hashing whole files freezes unrelated edits in them too; keep validity-critical code in these few files |
| Evaluation | A calibrated LLM judge: guard sensitivity and specificity on a labelled set, with CIs pre-registered | The guard is the gate on the AI arm; its recall has to be a number | About 60 items gives wide CIs; label leading and non-leading items in roughly equal numbers so both rates are estimable |
| Decision | A computed freeze rule over the logged metrics | Replaces judgement on 1–2 pilots with a stated rule | Thresholds for fallback and rejection rates are set from the simulated-session baseline before the first pilot, not after |
| Autonomy | Unchanged: a single call per turn plus the guard | The least autonomy that words questions from the expert's answers | Re-run the freeze rule on any model switch (stale-scaffold check) |

Smaller fixes from the same review are work items in `PROGRESS.md`, not part of this decision: one test that ties each output schema to its Pydantic model, a single `make_guard()` factory, CLI smoke tests, and the audio error-path tests (decision 0003).

## Consequences (cost)

- The freeze now also blocks harmless edits to `llm.py`, `engine.py`, `contract.py` and `models.py`; any post-freeze change there needs a re-freeze and a pre-registration amendment.
- Calibration costs two labellers about an hour per 60 items, repeated whenever the guard's model or prompt changes.
- A computed rule can say "change the model" on thin pilot data; the rule states its minimum turn count, and a repeated simulated session (3–5 runs) is allowed when a rate sits near a threshold.
- Least-autonomy check: nothing here adds an agent. The signal that would justify one is a decision that cannot be written as a rule in advance, and nothing in the freeze or the gates is of that kind.
