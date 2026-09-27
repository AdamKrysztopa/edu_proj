# Agentic system review: the Stage A interviewer (2026-09-27)

**Current design:** Autonomy: a code-controlled workflow of single calls; per turn, one stateless structured-output call chooses the stem, wording, anchor and whether to follow up (`instrument/src/probe_app/llm.py:63-91`) · Loop: generator plus evaluator, where code checks the turn contract (`contract.py:41-62`), then a guard call checks for leading content, with one regeneration and a bare-stem fallback (`engine.py:31-85`) · Agents: one interviewer plus one guard; the simulated expert is a test double · Memory: none needed; every turn rebuilds context from the session log · Governance: a frozen config checked against `prereg.json`, full request/response logging, and the researcher's pause.

The expert drives the outer loop, so the model never acts without an expert answer in between. The model's autonomy is the independent variable the study compares with a human interviewer, so it is fixed, not open.

## Findings

1. **The guard validates every AI turn, but nothing measures the guard.** (Checklist 4: outputs are validated by an unvalidated validator.) The leading-question guard (`llm.py:93-104`, `claude-haiku-4-5` at temperature 0) is the only semantic check against the §11 threat of plausible-but-false reconstruction. The tests drive it with scripted verdicts, and `probe-code guard-audit` (`instrument/src/probe_code/guard_audit.py:29-36`) reports flag *rates*, never whether a flag was right. A guard that misses leading questions passes every current check and biases the AI arm towards "probe-added" operations. · Impact: the K1(b) and contradicted-rate estimates rest on an unknown recall. · Fix: a labelled evaluation set, with the frozen guard's recall and false-flag rate measured against it and a minimum recall stated before `probe-app freeze`. · First step: after the first pilot, pool every AI turn, rejected turn and human-arm question (`turn_rejected` and `probe` events), add about 20 deliberately leading variants, and have two people label them leading or not.

2. **The freeze choice has metrics but no decision rule.** (Checklist 9: stale scaffold.) The regenerate-once loop, the 16,000-token thinking budget, the guard prompt and the wrap-up message were all tuned on `claude-opus-5`. `models.json` now allows any provider, and a model switch has already broken behaviour the fakes could not show (`docs/lessons.md`, "Model switch broke the simulator…"). The pilot measures latency, refusals, rejections, fallbacks and guard flags (`instrument/pilot-protocol.md:27-38`). Thresholds exist only for latency (median under 6 s) and refusals (about 1 in 10); the fallback and rejection rates, and the guard recall from finding 1, have none. · Impact: which configuration gets frozen, and whether a second model is tried, is decided by impression on one or two pilots. · Fix: one pre-stated freeze rule over those metrics, computed by code from the session logs, that says accept, change one variable and re-run a simulated session, or change the model. · First step: add fallback-rate and rejection-rate thresholds next to the existing two in the pilot protocol, and have `probe-code guard-audit` print a pass or fail line per threshold.

## Simplify

Nothing. Neither finding adds autonomy: both replace judgement with measurement. The freeze decision should be a rule applied by code, not an agent. The study's gates (K0, K1, K2) are the same kind of decision and should stay pre-registered rules for the same reason, because an agent deciding them would add judgement no one can audit.

## Sound as-is

- **(1) and (8), autonomy level.** A single call per turn inside a code workflow is the least autonomy that still lets the interviewer word questions from what the expert said. No tools are needed, because the whole trace fits in each request.
- **(2)** The interviewer plus the guard is a generator and an evaluator, not a multi-agent design.
- **(3) Budgets.** At most 2 attempts per turn, a 20-minute cap enforced on every poll, and a wrap-up request from 18 minutes; a refusal breaks straight to the fallback without retrying.
- **(5)** Stateless turns rebuilt from the log; there is no carried thinking to lose.
- **(6)** There is deliberately no human gate on AI questions: a researcher approving each one would put a human into the AI arm. Contract plus guard is the gate; the researcher can pause.
- **(7)** Every request and response is logged, with images logged by hash.
