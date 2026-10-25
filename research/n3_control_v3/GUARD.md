# I2: a guard judge for control2, and Jev as a cheap substitute (2026-10-24)

- **Question:** Is there an eligible other-family judge (ADR 0009's guard arm) for control2, and can Jev stand in for sol at lower cost?
- **Answer:** No guard yet: coder32 was dropped, because it is not runnable on local hardware. Jev passes L7.3 twice, identically, but is far from sol: in GDPR v1 it gives +0.14 [−0.05, +0.31] against sol's +0.23, noise-inflated CI [+0.05, +0.38], and its pooled κ with sol is 0.41.
- **Changed:** Judge substitution is no longer treated as the closure repair. ADR 0009 still has no eligible guard arm, so no sol reading counts yet, and the choice of guard is open. Sol's GDPR v1 direction survives its own judge noise.

## Result

**coder32: dropped** (not runnable on local hardware: 24 GB RAM, 76 s per trivial reply, first L7.3 run hung about 4 h with nothing saved). This is the owner's decision of 2026-10-24, in the owner's words; there is no follow-up run.

So ADR 0009 still has no eligible guard arm, and no sol reading counts yet. The choice of guard is open.

The parts that ran:
1. **Pair identity (step 1).** sol's and qwen's six domain outputs replay offline with identical `pairs`, `summary` and `length_stand_in`; no other field differs. `pairs_sha256` is added to each (`pairs_sha.py`).
2. **Sol's noise-inflated CI (step 6).** GDPR v1's lower bound stays above 0: +0.05, against +0.07 without the judge noise.
3. **Jev (step 5).** Eligible on L7.3, but far from sol by the pre-stated rule. By the pre-stated decision list it is not a substitute for sol; whether it has any V1 panel role is not decided here.

**Decision it feeds.** Under the item's decision list:
- Jev is "far from sol", so judge substitution stops being treated as the closure repair.
- control2 stays the MS1 instrument candidate judged by sol, not the registered instrument, until a guard arm passes L7.3 and agrees with sol.
- I4 (V1 kit) cannot build on a guarded control2 yet.

## Step 2: coder32 (dropped)

`l73.py --tag coder32 --model qwen2.5-coder:32b-instruct-q4_K_M --judge ollama` ran for about 4 h and produced nothing.
- **Hardware.** The machine has 24 GB of RAM (`hw.memsize`), and the model is 19 GB on disk (`ollama list`). The orchestrator's session measurements, not committed: 6% of RAM free while the model swaps, and 76.08 s for one trivial reply against 6.44 s for `qwen2.5:7b-instruct`.
- **The run.** The client sat at about 0% CPU, waiting on Ollama, until the harness stopped it for low system memory. Requests sampled during the run lasted about 90 to 180 s. Both are observations of this session, with no committed file.
- **Nothing was saved.** `l73.py` writes its cache only when the run ends, so there is no `coder32/` output.
- **The timeout matters too.** `OllamaJudge` times out at 180 s (`gapmap/src/gapmap/judge.py:56`). A timed-out call becomes `undecided` and is not cached, so even a completed run could have failed L7.3 for serving reasons alone.
- **Wall time.** 76 prompts did not finish in about 4 h (a session observation, no committed log): roughly 190 s or more per prompt, near the 180 s per-call timeout. At that rate the 532 domain prompts would take about 27 h per pass.

## Step 1: pair identity

`pairs_sha.py` replays each domain in a temporary directory from its committed cache (no `--judge`, no network). It compares every field except `pairs_sha256` and `spend`; an offline replay of an OpenAI cache reports zero calls, so the committed `spend` is kept.

| Domain | `pairs_sha256` (first 12) | sol: fields differing | qwen: fields differing |
|---|---|---|---|
| PLC | `1aa6cd022b95` | none | none |
| GDPR v1 | `129beef55ad6` | none | none |
| GDPR v2 | `92f340b1448b` | none | none |

Sol's and qwen's hashes are equal in each domain, as are Jev's (step 5), so all three judged the same pairs.

## Step 6: sol's direction with its own judge noise

`sol_noise.py` counts P(run-2 state | run-1 state) over the prompts that I1c's two sol runs both sent. Inside the seed bootstrap (B = 2000, the committed seed), it redraws each pair's own and control seed-free states from those rows. Cluster draws use the committed seed and the noise a second stream, so an identity matrix reproduces the committed CI exactly; it does in all three domains.

| Domain | Retest prompts | State agreement | Primary | Committed CI | Noise-inflated CI | Direction |
|---|---|---|---|---|---|---|
| PLC | 146 | 0.92 | +0.13 | [−0.02, +0.28] | [+0.00, +0.30] | 0 |
| GDPR v1 | 88 | 0.94 | +0.23 | [+0.07, +0.39] | **[+0.05, +0.38]** | **+** |
| GDPR v2 (not admissible) | 92 | 0.93 | +0.07 | [−0.02, +0.18] | [−0.07, +0.20] | 0 |

GDPR v1's lower bound stays above 0. PLC's lower bound is exactly 0.00, so not above 0, and its direction stays 0. Pooling both run orders (a symmetrised matrix) moves no direction (`sol_noise.json`, `symmetrised_ci95`).

## Step 5: Jev

**The judge.** `gapmap/src/gapmap/jev.py` (14 tests in `gapmap/tests/test_judge_jev.py`, fake transport, no socket).
- It rebuilds the JEV spike's request body from a control2 prompt: one three-way choice per sentence, the same wording.
- It maps Jev's top choices onto control2's reply, so an arm is closed iff a sentence's top choice is "states", partial iff none is and one is "partially", else open. That is the rule stated in the item before any call.

**Cache rule.** The spike's raw cache comes first, then this run's; a live call is made only for a miss.
- A miss on a prompt the old control issued stops the run. `jev_run.py check` rebuilt the body for all 542 unique prompts the spike sent, and the spike cache holds all 542.
- Four control2 prompts (2 in GDPR v1, 2 in GDPR v2) were ones the old control issued, and the spike cache answered them. The other 528 were live calls. No prompt recurs across domains.
- Jev's `choice` is its top choice. On 8 of the spike cache's 4,163 answers it differs from the most probable option: 7 are exact ties at the stored precision, and 1 is within 0.01.

**L7.3**, the same fixtures and rule as `l73.py`. The retest read no earlier cache, so it re-asked all 76 prompts live.

| Run | Plants firing | Stand-ins closing the own seed-free arm | Eligible |
|---|---|---|---|
| 1 | 3/3 | 0/12 | yes |
| 2 (retest) | 3/3 | 0/12 | yes |

The reply state agrees on 76 of 76 prompts between runs, and the target states are identical, so Jev is eligible. On each topic's target pair, the planted own seed-free arm closes, while its control seed-free arm and every stand-in's own seed-free arm stay open. The equal-cap arms close throughout and are not ruled on.

**Domains.** The primary is seed-free, closed only, own − control, with its seed-resampled 95% CI. Sol's direction is its noise-inflated one (step 6).

| Domain | Jev own vs control | Jev primary | Jev direction | Sol primary, direction | Δ (Jev − sol) | κ Jev–sol | Close |
|---|---|---|---|---|---|---|---|
| PLC | 0.50 vs 0.43 | +0.07 [−0.10, +0.27] | 0 | +0.13, 0 | −0.06 | 0.40 | no |
| GDPR v1 | 0.43 vs 0.30 | +0.14 [−0.05, +0.31] | **0** | +0.23, **+** | −0.09 | 0.43 | no |
| GDPR v2 (n/a) | 0.26 vs 0.29 | −0.02 [−0.20, +0.16] | 0 | +0.07, 0 | −0.10 | 0.47 | no |

The rule, stated before any Jev domain result: the same direction as sol in every domain, |Δ primary| ≤ 0.05, and κ ≥ 0.6.
- Jev fails every part. Its direction differs from sol's in GDPR v1, every |Δ| exceeds 0.05, and no κ reaches 0.6.
- Pooled over the admissible domains, κ is 0.41 with sol, 0.47 with Luna and 0.13 with qwen 7b.

On the secondary split (closed or partial), Jev separates in PLC: +0.22 [+0.09, +0.40]. That split is not the primary. Jev left no arm undecided, and the length-only stand-in is unchanged (same pairs).

**Cost.** 680 live Jev calls, $0.0473 of the $0.10 cap:
- L7.3: $0.0024 per run (76 calls each).
- Domains: $0.0426 (528 calls; 4 prompts the old control had issued were answered from the spike cache).
- Per judged arm, Jev cost $0.00008 and sol $0.0038 ($2.031 over 532 domain calls, `RESULT.md`), about 47× more. The OpenRouter key read $14.99 remaining at wave 2's preflight (`scripts/key_headroom.py`; L7.2 record, wave 2, in `docs/plans/implement-queue.md`).

## Limits

- Every contrast here is a contrast of judge (model, serving, decoding together), not family alone (L7.4). Jev is a per-sentence decision model behind a different request, so it never shares control2's prompt and parser, and it is not ADR 0009's guard arm.
- The L7.3 fixtures are synthetic, SEL only, and topic-built. The rule rules on the seed-free arms only.
- Jev's 76/76 retest agreement shows stability on these fixtures only; its decoding was not checked.
- The noise model uses one retest per prompt from one earlier run. The overlap is 88–146 prompts per domain.
- No human labels exist: "closed" is each judge's reading, not ground truth. All lenses and thresholds are in-sample.

## Files

- `pairs_sha.py`: step 1, run with `--write`. It adds `pairs_sha256` to `sol/*/control2.json` and `qwen/*/control2.json`.
- `sol_noise.py` → `sol_noise.json`: step 6.
- `jev_run.py`, with `check`, `l73 run1|retest` and `domains`. Its outputs are in `jev/`:
  - `l73/` and `l73_retest/`: `l73.json`, the closure cache, and `raw/` (each request and response);
  - `plc/`, `gdpr_v1/`, `gdpr_v2/`: `control2.json` and the closure cache;
  - `raw/`: the domains' requests and responses;
  - `jev_spend.jsonl`: one line per live call, the ledger the cap reads.
- `compare.py` → `compare.json`: I1c's tables are unchanged, with Jev added beside them, plus `i2_l73_screen` and `i2_jev_vs_sol`.
- `research/spikes/jev/RESULTS.md`: the count is corrected to 641 entries holding 542 unique prompts, the causal sentence is replaced, and "fair control" becomes "mismatched-evidence control" throughout.

**Replay offline**, from the repository root, with no key. All Jev outputs replay byte-identically, and the recorded spend is kept:
- `uv run --directory gapmap python ../research/n3_control_v3/jev_run.py l73 run1` (or `retest`, or `domains`). A cache miss stops the run; `--live --max-usd X` fills it.
- `python3 research/n3_control_v3/compare.py`
