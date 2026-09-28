# Freeze baseline: interviewer rates from the simulated sessions

Decision 0004 (`docs/architecture/decisions/0004-data-driven-freeze.md`) requires the fallback- and rejection-rate thresholds to be set from the simulated-session baseline **before the first pilot**, and the freeze to be decided by a rule applied by code. This note gives the baseline, how it was computed, its limits, and the proposed rule. Computed 2026-09-28.

## Recomputed before the pilot (2026-09-28)

The two original sessions below ran a configuration that has since been superseded (`probe-code freeze-baseline` now refuses them). Three new simulated sessions on the current configuration, all complete (6 of 6 AI sets finished): `SIM-8437c072…`, `SIM-8e0f2501…`, `SIM-c7cbe04d…`. `SIM-f1919bc3…` was excluded because it stopped part-way when frozen files were edited during its run, which is the app's config check working, not a model event.

- **Pooled counts:** 86 AI turns delivered (85 accepted, 1 bare-stem fallback), 95 generated, 89 guard-checked; 6 sessions ended by the interviewer.
- **Rates:**
  - fallback 1/86 = 1.2% (Wilson 95% up to 6.3%);
  - guard rejection 4/89 = 4.5% (up to 11.0%);
  - contract rejection 0/95 (up to 3.9%);
  - refusals 0/86 (up to 4.3%).
- **Latency:** median 5.0 s over 80 gaps, maximum 14.0 s.
- **Thresholds for the pilot, by the rule below** (upper bound rounded to the nearest 5 points, set in `PROPOSED_THRESHOLDS` before the first pilot): fallback 5%, guard rejection 10%, contract rejection 5%, refusals 5%, median latency 6 s. Rounding puts the fallback threshold below its upper bound, so a pilot with 2 fallbacks in 30 turns lands near it; the rule's margin step then asks for simulated reruns before any change.
- **Rule outcome on this pool:** accept.

## Numbers (original baseline, superseded configuration)

Two simulated sessions exist, both AI in both sets, Sonnet 5 role-playing the expert, interviewer `claude-opus-5` (effort medium), guard `claude-haiku-4-5`. Prompt hashes in both manifests equal the current `instrument/prompts/` files, and the model IDs equal the current `models.json`.

| Metric | Definition (counts from `events.jsonl`) | SIM-2980899a (complete) | SIM-4ac7555c (aborted) | Pooled |
|---|---|---|---|---|
| AI sets started / finished | `probe_started` with arm ai / `probe_finished` | 2 / 2 | 1 / 0 | 3 / 2 |
| Turns delivered | `probe` events, source `ai` or `ai_fallback` | 32 (31 + 1) | 1 (1 + 0) | 33 |
| Fallback rate | `ai_fallback` / delivered | 1/32 = 3.1% (0.6–15.7) | 0/1 | 1/33 = 3.0% (0.5–15.3) |
| Contract rejection rate | `turn_rejected` "contract" / generated turns¹ | 0/36 = 0% (0–9.6) | 0/1 | 0/37 = 0% (0–9.4) |
| Guard rejection rate | `turn_rejected` "leading" / guard checks² | 3/34 = 8.8% (3.0–23.0) | 0/1 | 3/35 = 8.6% (3.0–22.4) |
| Refusals | `interviewer_failed` LLMRefused / delivered | 0/32 = 0% (0–10.7) | 0/1 | 0/33 = 0% (0–10.4) |
| Outages, guard failures | `interviewer_failed` LLMUnavailable; `guard_failed` | 0; 0 | 0; 0 | 0; 0 |
| Latency | `expert_answer` → next `probe` in the same set, s | n = 30, median 4.8, max 37.9 | n = 0 | n = 30, median 4.8, max 37.9 |

Brackets are Wilson 95% intervals. ¹ Generated = accepted + discarded at the cap + rejected (contract or leading) + ended by the interviewer. ² Guard checks = verdicts returned: accepted + discarded at the cap + rejected as leading (guard failures return none).

SIM-4ac7555c stopped after its first question, with no answer, so the baseline is in effect one complete session of 32 delivered turns.

## How it was computed

`instrument/src/probe_code/baseline.py` (tested in `instrument/tests/test_baseline.py` on a fake event log with hand-counted values): `session_metrics(dir)` per session, `pooled_metrics([...])` sums counts before dividing and refuses sessions whose frozen configurations differ, `thresholds_from_baseline(pooled)` derives the thresholds, and `freeze_decision(pooled)` applies the rule below. It reuses `ai_rejection_counts` from `guard_audit.py`, so the pilot report and the baseline count the same events. Until a `probe-code` subcommand is wired, from the repository root:

```
uv run --directory instrument python -c "import json, sys; from probe_code.baseline import *; \
ms = [session_metrics(p) for p in sys.argv[1:]]; p = pooled_metrics(ms); \
print(json.dumps({'sessions': ms, 'pooled': p, 'decision': freeze_decision(p)}, indent=1))" \
"$PWD/sessions/SIM-2980899a" "$PWD/sessions/SIM-4ac7555c"
```

## Limits

- **One complete session, 32 turns.** Every interval is wide: the fallback rate is compatible with anything from under 1% to about 16%.
- **Sonnet role-play, not physicists.** Simulated answers are fluent, on topic and typed; real answers are spoken, transcribed, hesitant and sometimes off topic. Contract rejections (quotes checked against the expert's words) and refusals are the rates most likely to rise with real speech.
- **Latency excludes transcription.** `expert_answer` is logged after the answer is transcribed, so the expert waits longer than the measured gap. The 37.9 s maximum had no logged retry or outage; its cause is unknown.
- **The guard rejections look like guard errors.** All three rejected questions used the `alternatives` stem and quoted the expert, for example: In A2, at the point where you wrote "cos theta is one minus h over L" — what else could you have done there instead? The guard flagged each as introducing "alternative methods". Under its own definition a neutral question about what the expert considered is not leading, so the guard-rejection rate currently measures the guard as much as the interviewer. The guard calibration of decision 0004 (about 60 labelled questions, sensitivity and specificity) is what shows which.
- The manifests predate the `guard_temperature` and provider fields, so the guard's temperature in these runs cannot be verified from the logs.
- Outages (`interviewer_unavailable`, `guard_failed`) have no threshold of their own; there were none here. In a pilot they show up only as fallbacks, so a fallback rate over threshold caused by outages reads as "change one variable" when the fix is infrastructure; check the outage counts before acting on that outcome.
- The code in `llm.py` and `engine.py` has changed since these runs (refusals split from outages, model choice in `models.json`, discarding a turn completed after the cap); the prompts and models have not.

## Threshold rule for the pilot

**Recommended: thresholds at the baseline's upper 95% bound, rounded to the nearest 5 points, fixed now.** They are the highest rates the simulated behaviour is compatible with; a pilot above one is evidence that real experts drive the interviewer somewhere the simulation did not. Values (`PROPOSED_THRESHOLDS`): fallback 15%, guard rejection 20%, contract rejection 10%, refusals 10% (the pilot protocol's "about 1 in 10"), median latency 6 s (the protocol's target). `thresholds_from_baseline` reproduces the four rates from the pooled counts (tested). The rule, as `freeze_decision` applies it to the pilot sessions and the simulated sessions of the same configuration, pooled (sessions of different configurations are refused):
1. Under 30 delivered AI turns, or a rate with no denominator: add a simulated session on that configuration and apply the rule again. Each pilot yields about 16 AI turns, so this usually fires once.
2. Refusals over threshold: change the model or provider.
3. Any other rate over threshold, or median latency over 6 s: change one variable (prompt wording or effort) and re-run.
4. A rate within 5 points below its threshold while the pool holds fewer than 3 simulated sessions: add simulated sessions until it holds 3, then decide by the thresholds alone. The count comes from the manifests, so no one decides when the reruns are done.
5. Otherwise: accept and freeze.

Alternatives considered:
- *Validity-anchored ceilings, independent of the baseline* (for example fallback at most 10%, because every fallback is a bare stem that weakens the AI arm). Defensible for fallbacks, but there is no argument of this kind for the other rates, and it sets numbers without data.
- *A multiple of the baseline point estimate* (for example twice the rate). It fails where the baseline is 0/36: any single contract rejection or refusal would then trip the rule.

What would change the recommendation:
- 3–5 more simulated sessions before the pilot (decision 0004 allows them) would narrow the intervals; the thresholds are then recomputed by `thresholds_from_baseline`, and `PROPOSED_THRESHOLDS` updated before the first pilot, never after. This is the cheapest improvement and is worth doing before the pilot.
- If guard calibration shows that most guard rejections are false positives, the guard-rejection threshold measures the guard, not the interviewer. Then the guard prompt is fixed first (the human script must follow it word for word; a test enforces this) and the baseline is re-run.
- A model change in `models.json` voids this baseline; it is re-run on the new model.
