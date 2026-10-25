# I1c: control2 with seed-free arms, through qwen, Luna and gpt-6.1-sol (2026-10-24)

**Result.** Both arms of control2 now drop the seed sources of both candidates. With that change, the top-tier judge `gpt-6.1-sol` (reasoning effort high) passes the pre-stated real-judge L7.3 check, and passes it identically on a retest. `qwen2.5:7b-instruct` fails the check, because its stand-ins fire. `gpt-5.6-luna` (effort medium) passed in run 1 but failed in run 2 on the same prompts.

On the pre-declared primary comparison (seed-free in both arms, closed only, seed-resampled 95% CI lower bound above 0), sol separates a candidate's own evidence from a donor's in GDPR v1. It does not separate them in PLC. The length-only stand-in passes nowhere.

| Domain | sol (eligible) | qwen (ineligible) | Luna (ineligible in run 2) | Length-only stand-in | Verdict, sol |
|---|---|---|---|---|---|
| PLC | +0.13 [−0.02, +0.28] | +0.06 [−0.09, +0.20] | +0.07 [−0.08, +0.24] | +0.13 [−0.19, +0.42] | uninformative |
| GDPR v1 | **+0.23 [+0.07, +0.39]** | +0.18 [+0.00, +0.37] | +0.23 [+0.05, +0.40] | +0.14 [−0.07, +0.32] | discriminates |
| GDPR v2 (not admissible) | +0.07 [−0.02, +0.18] | +0.14 [+0.00, +0.29] | +0.14 [−0.05, +0.32] | −0.05 [−0.21, +0.11] | not evidence |

**No reading counts under ADR 0009's agreement rule combined with the L7.3 eligibility rule.** In GDPR v1, qwen and sol disagree in direction: qwen's lower bound is exactly 0.00, sol's is +0.07. Qwen is ineligible in any case. ADR 0009 is active (promoted by the owner on 2026-10-24, before this run's result).

On the secondary split (closed or partial), sol separates the arms in PLC too: +0.43 [+0.19, +0.63], own 0.69 against control 0.26. That split was not the declared primary.

**Decision it feeds (is control2 the MS1 instrument?).** Change: control2 with symmetric seed-free arms becomes the MS1 instrument candidate, with sol as its judge. It does not yet become the registered instrument, for three reasons:
- **The guard arm is ineligible.** ADR 0009 needs an other-family arm that agrees with sol, and qwen fails L7.3. This is the owner decision below.
- **Sol is not deterministic.** On the prompts both runs sent, its reply state agrees 92–94 % between runs (kappa 0.87–0.90; on the L7.3 fixtures, 100 %). The seed-resampled interval does not include that judge noise.
- **The evidence is narrow.** The passing check uses three synthetic SEL fixtures, and the lenses and thresholds are in-sample.

Every contrast here is a contrast of judge: model, serving and decoding together (L7.4), not family alone.

## Owner decision now due: the other-family arm of ADR 0009

ADR 0009 counts a reading only where the same-family arm (sol) and the other-family arm (qwen) agree in direction. The I1c checklist adds that a judge failing either real-judge L7.3 arm is ineligible (`docs/plans/implement-queue.md`, "Before E-CTA registration"). Qwen fails: its own seed-free arm closes on 8 of 12 stand-ins, identically in both runs. So no reading can count. The options, by technical merit:

1. **(Recommended) Replace qwen as the guard arm with a non-OpenAI, non-Anthropic judge that first passes this same L7.3** (`l73.py`), then re-run the three domains beside sol's cached run.
   - Evidence: sol passes L7.3 twice with identical states, and qwen fails twice. Qwen's kappa with sol is 0.24 pooled; Luna's is 0.50. So qwen is the outlier judge, not sol.
   - A local model costs $0 to screen first. This machine's Ollama lists `qwen2.5-coder:32b-instruct-q4_K_M`. That is the same vendor as qwen, but neither OpenAI nor Anthropic.
   - What would change this: no other-family model passing L7.3. Then option 2 is the only route.
2. **Amend ADR 0009 so that the guard is any second judge passing L7.3.** No judge other than sol passes in run 2, so this also needs a new judge. If that judge is from OpenAI or Anthropic, it gives up the guard against verifier self-preference (R5).
3. **Keep ADR 0009 as written, with qwen as the guard.** Then control2 can never feed MS1.

**Owner decision, 2026-10-24: option 1.** Wave 2 first screens the local `qwen2.5-coder:32b-instruct-q4_K_M` on `l73.py` ($0). If it passes, it re-runs the three domains beside sol's cached run; if it fails, a hosted non-OpenAI, non-Anthropic model on OpenRouter is screened next, after an OpenRouter judge backend is added (`l73.py` and `control2.py` accept only `--judge ollama|openai`). control2 now refuses a live same-family judge without `--parallel-arm` (ADR 0009), so the other-family arm runs first.

**Update, 2026-10-24 (I2, [GUARD.md](GUARD.md)).** coder32 was dropped by the owner: it is not runnable on this laptop (24 GB RAM, 76 s per trivial reply, its first L7.3 run hung about 4 h with nothing saved), and no hosted coder32 run follows. Jev passed L7.3 but is far from sol, and it cannot be the guard in any case (it does not share control2's prompt and parser). No guard arm is eligible, so no sol reading counts under ADR 0009; choosing a guard is open.

## Step 1: the donor fix and what it changes

The owner asked that the donor's seed sentences be dropped from the donor arm. This fix is stricter: `control2.build_pairs` (`gapmap/src/gapmap/control2.py`) now drops the seed sources of both *i* and *j* from both pools.
- The own pool is *i*'s ranked retrieval.
- The donor pool is *j*'s ranked retrieval, minus *i*'s capped own pool so the arms share no sentence.

So both arms drop the same seed sources (`docs/plans/prompts/_common.md`, L7.3 rule 4). To keep the arms disjoint, the donor arm also drops *i*'s capped pool, so a sentence that both retrievals rank goes to the own arm.

The first version (run 1, commit `dca3b0b`) applied the exclusion to the donor arm only. Its own arms still carried a donor seed-source sentence in 69 of the 142 pairs it judged (PLC 19/54, GDPR v1 28/46, GDPR v2 22/42; computed with `dca3b0b`'s `build_pairs`, as recorded in commit `cccff1d`). The citation-verifier found this, and run 1's outputs are kept as superseded in `run1_asymmetric/`.

`--legacy-donor-seed` rebuilds I1/I1b's pairs. With it, all six committed runs replay offline with identical `pairs`, `summary` and `length_stand_in`: `research/n3_control/` and `research/n3_control_luna/`, three domains each.

The counts below are offline, with no judge (`donor_fix.py` → `donor_fix.json`).

| | PLC | GDPR v1 | GDPR v2 | Total |
|---|---|---|---|---|
| Pairs | 54 | 51 | 48 | 153 |
| I1 control arms holding a donor seed sentence | 31 | 26 | 20 | **77** |
| … holding a donor seed-source sentence | 34 | 35 | 28 | 97 |
| I1 own arms holding a donor seed sentence | 10 | 26 | 22 | **58** |
| … holding a donor seed-source sentence | 19 | 34 | 25 | 78 |
| Can discriminate, I1 pool | 54 | 50 | 45 | 149 |
| Can discriminate, donor seed sentences dropped only | 54 | 50 | 45 | 149 |
| Can discriminate, fixed (both arms) | 54 | 44 | 42 | **140** |
| Best reachable own − control, I1 | 1.00 | 0.98 | 0.94 | 0.97 |
| Best reachable own − control, fixed | 1.00 | 0.86 | 0.88 | **0.92** |
| Pairs whose control arm changes | 34 | 41 | 33 | 108 |
| Pairs whose own arm changes | 19 | 34 | 25 | 78 |
| Pairs whose k drops | 0 | 17 | 10 | 27 |

So I1's "seed-free" comparison was not seed-free in either arm. Its control arms carried the donor's own seed in 77 of 153 pairs, and its own arms in 58. The best reachable difference is the share of pairs that can discriminate, with own always closed and control never; within those pairs it is 1.0.

**Verdict (step 2).** `control2.verdict` takes the length stand-in's row. It returns `design-wrong` when that row's CI lower bound is above 0. It also returns `design-wrong` when the planted positive does not fire or a stand-in fires.

## Step 5: real-judge L7.3 on plain-text fixtures

The fixtures are in `gapmap/tests/l73_fixtures.py`, checked offline by `test_l73_fixtures.py`. The checks:
- each plant is in the own arms and in neither control arm;
- no seed of either candidate is in a seed-free arm;
- each stand-in matches the plant's length exactly (94, 103 and 101 characters);
- the fake judge does not fire on a plant, because the plants carry no marker.

There are three SEL topics (PLC test order, cable shielding, GDPR retention), each with one planted pair (k = 2). Each plant has two kinds of stand-in:
- three random-letter stand-ins (RNG seeds 7, 8, 9), keeping the word lengths and the retrieval words;
- one plain-English, length-matched non-answer.

The symmetric fix leaves every fixture prompt unchanged: runs 1 and 2 sent the same 76 prompts.

**Rule, stated before any call** (`l73.py`, commit `dca3b0b`, which predates every result file):
- the planted positive fires iff, on every planted pair, the seed-free arms give own = closed and control ≠ closed;
- a stand-in fires iff any stand-in's own seed-free arm is closed;
- a judge is eligible iff the plant fires and no stand-in fires.

The rule rules on the seed-free arms only.

| Judge | Plants firing, run 1 / run 2 | Stand-ins closing the own arm | Eligible, run 1 / run 2 |
|---|---|---|---|
| qwen2.5:7b-instruct | 3/3 / 3/3 | **8/12** in both runs (random letters 7/9, length-matched 1/3) | no / no |
| gpt-5.6-luna, effort medium | 3/3 / **2/3** | 0/12 in both runs | yes / **no** |
| gpt-6.1-sol, effort high | 3/3 / 3/3 | 0/12 in both runs (all open) | yes / yes |

Luna's run-2 failure is on the cable-shielding pair. On the same prompt, Luna now closes the control arm ("Fuse ratings selection practice is documented for the load current."), which it left open in run 1. Luna's reply state differs between runs on 10 of the 76 identical fixture prompts. Qwen's differs on 0 and sol's on 0.

Equal-cap results:
- For qwen and Luna, both equal-cap arms close, so the plant cannot fire there.
- Sol closes the own equal-cap arm and leaves the control partial, so its plant also fires at equal cap.

## Step 6 → 7: the fixed control on the three domains (run 2)

Each cell is own − control with its seed-resampled 95% CI (2000 resamples). Only pairs that can discriminate are used: PLC 54, GDPR v1 44, GDPR v2 42.

| Domain | Judge | Seed-free, closed (primary) | Seed-free, closed or partial | Equal-cap, closed | Equal-cap, closed or partial |
|---|---|---|---|---|---|
| PLC | qwen | 0.15 vs 0.09, +0.06 [−0.09, +0.20] | +0.07 [−0.07, +0.23] | +0.02 [−0.12, +0.17] | +0.00 [−0.14, +0.15] |
| | Luna | 0.46 vs 0.39, +0.07 [−0.08, +0.24] | **+0.15 [+0.03, +0.28]** | +0.02 [−0.13, +0.17] | **+0.11 [+0.02, +0.23]** |
| | sol | 0.24 vs 0.11, +0.13 [−0.02, +0.28] | **+0.43 [+0.19, +0.63]** | +0.02 [−0.11, +0.13] | **+0.24 [+0.02, +0.46]** |
| GDPR v1 | qwen | 0.41 vs 0.23, +0.18 [+0.00, +0.37] | +0.09 [−0.02, +0.23] | **+0.16 [+0.05, +0.29]** | +0.05 [−0.07, +0.18] |
| | Luna | 0.59 vs 0.36, **+0.23 [+0.05, +0.40]** | **+0.20 [+0.05, +0.35]** | +0.07 [−0.10, +0.22] | +0.09 [−0.05, +0.24] |
| | sol | 0.43 vs 0.20, **+0.23 [+0.07, +0.39]** | +0.18 [+0.00, +0.35] | **+0.16 [+0.02, +0.30]** | +0.09 [−0.09, +0.27] |
| GDPR v2 (n/a) | qwen | 0.38 vs 0.24, +0.14 [+0.00, +0.29] | +0.19 [+0.05, +0.35] | +0.07 [+0.00, +0.16] | +0.02 [−0.07, +0.12] |
| | Luna | 0.50 vs 0.36, +0.14 [−0.05, +0.32] | +0.07 [−0.10, +0.25] | −0.05 [−0.21, +0.11] | +0.05 [−0.15, +0.23] |
| | sol | 0.29 vs 0.21, +0.07 [−0.02, +0.18] | +0.10 [+0.00, +0.21] | +0.07 [+0.00, +0.15] | +0.07 [−0.02, +0.18] |

**Length-only stand-in** on the fixed pairs. It closes an arm whose non-seed character total reaches the median, and it uses no model.

| Domain | Length-only result |
|---|---|
| PLC | +0.13 [−0.19, +0.42] |
| GDPR v1 | +0.14 [−0.07, +0.32] |
| GDPR v2 | −0.05 [−0.21, +0.11] |

It passes nowhere. In I1 it passed GDPR v1, at +0.28 [+0.06, +0.49]. In run 1 its lower bound there was exactly 0.

**Primary by lens, sol.**
- PLC WHY, +0.29 [+0.12, +0.50], n = 24.
- GDPR v1 HEDGE, +0.60 [+0.20, +1.00], n = 5, which carries little information.

Every other sol lens interval reaches 0, including GDPR v1 DISC at +0.38 [+0.00, +0.73]. Luna also excludes 0 in PLC WHY, GDPR v1 DISC and HEDGE, and GDPR v2 WHY. All rows are in `compare.json`. PLC DIAG has 9 pairs from 2 seed clusters, so its intervals carry no information.

**Undecided arms:** qwen 2 (PLC own seed-free), Luna 0, sol 0. All 2,448 OpenAI calls across both runs returned `finish_reason: stop` and were served as the requested model.

### ADR 0009 reading (qwen and sol, primary)

Direction is "+" when the CI lower bound is above 0, "−" when the upper bound is below 0, and "0" otherwise.

| Domain | qwen | sol | Agree | Counts |
|---|---|---|---|---|
| PLC | 0 | 0 | yes | no: qwen ineligible |
| GDPR v1 | 0 | + | no | no |
| GDPR v2 (n/a) | 0 | 0 | yes | no: qwen ineligible |

### Agreement between judges, and with themselves

**Between judges (Cohen's kappa).** There is one judgement per unique (seed, lens, arm), on pairs that can discriminate, on closed/partial/open, with `undecided` excluded. 8 of PLC's 9 DIAG pairs share a seed and lens, so PLC n is 188 = (54 − 7) × 4, not 216 (186 for pairs with qwen, which left 2 arms undecided).

| Pair | PLC | GDPR v1 | GDPR v2 | Admissible pooled (n) | Raw agreement, pooled |
|---|---|---|---|---|---|
| qwen–Luna | 0.16 | 0.28 | 0.27 | 0.22 (362) | 0.47 |
| qwen–sol | 0.26 | 0.22 | 0.27 | 0.24 (362) | 0.50 |
| Luna–sol | 0.46 | 0.55 | 0.38 | **0.50** (364) | 0.67 |

**Test-retest.** This compares the reply state on the prompts that runs 1 and 2 both sent: non-empty `states`, else non-empty `partially`, else open, read before the parser validates the sentence numbers.

| Judge | L7.3 (76) | PLC (146) | GDPR v1 (88) | GDPR v2 (92) |
|---|---|---|---|---|
| qwen | 1.00 | 1.00 | 1.00 | 1.00 |
| Luna | 0.87 (κ 0.77) | 0.88 (κ 0.80) | 0.82 (κ 0.69) | 0.77 (κ 0.62) |
| sol | 1.00 | 0.92 (κ 0.87) | 0.94 (κ 0.90) | 0.93 (κ 0.87) |

## Reading it (a contrast of judge, L7.4)

- **The fix changes what the controls measure.**
  - In run 1, own arms could carry the donor's seed. There, qwen's GDPR v1 primary was +0.26 [+0.09, +0.44] and sol's +0.13 [−0.07, +0.33].
  - With the seed out of both arms, qwen falls to +0.18 [+0.00, +0.37] and sol rises to +0.23 [+0.07, +0.39].
  - The run-1 and run-2 pairs differ, so this compares control designs, not judge noise alone.
- **The Luna change is a judge-retest effect, not a design effect.** The L7.3 fixture prompts are identical in both runs. Luna, with the same model and effort, flips its control-arm state on the cable pair, so its eligibility is not stable.
- **Sol is the only judge that is both discriminating and stable on the fixtures.**
  - On the domains, its own-arm closure rates are low (PLC 0.24, GDPR v1 0.43). Its control rates are lower still (0.11, 0.20).
  - It marks many own arms partial, so in PLC it separates on closed-or-partial (+0.43) but not on closed (+0.13).
- **The judges disagree about what the arms say.**
  - Luna and sol, both OpenAI, agree moderately (kappa 0.50).
  - Qwen agrees with either at about 0.2. Its stand-in failures are consistent with closing on the topic words alone.
- **The arms differ in the whole judge, not only in family.**
  - Qwen runs on Ollama (JSON format, temperature 0, seed 0).
  - Luna and sol run on Chat Completions (`json_object`, no temperature, reasoning effort medium and high).
  - Sol's price per token is 10× Luna's for input and 8.3× for output ($2 / $10 against $0.20 / $1.20 per 1M).

**Limits.**
- All lenses, lexicons and thresholds are in-sample.
- The L7.3 fixtures are synthetic, SEL only, and topic-built. The rule rules on the seed-free arms only.
- DIAG is judged through its first rival only.
- The fixed pairs are not I1's pairs: 27 pairs shortened when the pools shrank.
- The length stand-in is one surface statistic.
- Judge noise is outside the CI. Sol's state changes on about 6–8 % of identical domain prompts between runs, and each arm was judged once.
- There are no human labels yet: "closed" is each judge's reading, not ground truth.

## Run

**gpt-6.1-sol**
- It appears in `GET /v1/models` (checked 2026-10-24), and every call was served as `gpt-6.1-sol`.
- Prices, from platform.openai.com/docs/models/gpt-6.1-sol (redirected to developers.openai.com/api/docs/models/gpt-6.1-sol, read 2026-10-24): input $2, cached input $0.10, output $10 per 1M tokens.
- Reasoning efforts listed: low, medium (default), high, xhigh and max. The page does not say whether reasoning tokens bill as output. Spend counts them as output, an upper bound.
- No prompt was cached: `cached_tokens` was 0 on all calls.

**Settings**, recorded in each OpenAI cache's `_meta`: Chat Completions, `response_format: json_object`, `max_completion_tokens: 6000`, no temperature. Sol ran at `reasoning_effort: high`, Luna at `medium`. Qwen's caches carry no `_meta`.

**One cap.** `--max-usd 10` covered every OpenAI call in steps 5 and 6, both runs included.
- Each run charged `openai_spend.jsonl`.
- `OpenAIJudge` checked the ledger's prior spend, plus its own spend, plus the next call's worst case against the cap before every call.
- The OpenAI runs ran one after another, so the ledger was never read stale.
- `scripts/key_headroom.py` covers the OpenRouter key only, which was not used here; it read $14.99 remaining.

**Estimate before any call** (`estimate.json`, from I1b's measured tokens), with sol at Luna's completion tokens per call:
- Luna $0.36 and sol $3.08, a total of **$3.44**.
- At 3× sol's completion tokens: $8.63.
- Worst case, every reply at the 6,000-token ceiling: $41.9 (Luna $4.48 + sol $37.45). That case is enforced per call by the guard.

After run 1's step 5, sol used 0.98× Luna's completion tokens per fixture call, so the domain runs went ahead. Run 2's estimate (`estimate_run2.json`) was $3.39, against the $7.46 then left under the cap.

| | Calls | Prompt tokens | Completion (reasoning) | Spend |
|---|---|---|---|---|
| Run 1 (superseded), Luna + sol, L7.3 and domains | 1,232 | | | $2.545 |
| Run 2, Luna, L7.3 | 76 | 12,256 | 11,474 (7,954) | $0.016 |
| Run 2, Luna, PLC / GDPR v1 / GDPR v2 | 188 / 176 / 168 | 227,124 | 210,711 (182,913) | $0.298 |
| Run 2, sol, L7.3 | 76 | 12,256 | 11,616 (8,148) | $0.141 |
| Run 2, sol, PLC / GDPR v1 / GDPR v2 | 188 / 176 / 168 | 227,124 | 157,690 (130,715) | $2.031 |
| **Total OpenAI, both runs** | 2,448 | | | **$5.031** of the $10 cap |
| qwen, local Ollama, run 1 / run 2 | 616 / 608 | | | $0 |

## Files

- **`qwen/`, `luna/`, `sol/`** hold run 2, the result above:
  - `l73/`: `l73.json`, the judge cache, and `judge_calls.jsonl` for the OpenAI judges;
  - `plc/`, `gdpr_v1/`, `gdpr_v2/`: `control2.json`, `closure_judgements.json`, and `judge_calls.jsonl` for the OpenAI judges.
- **`run1_asymmetric/`** holds run 1 (superseded), with the same layout plus its `compare.json` and `donor_fix.json`. It replays only on commit `dca3b0b`'s `control2.py`.
- **`openai_spend.jsonl`** is the shared spend ledger, one line per OpenAI call: run 1 is lines 1–1,232, run 2 the rest.
- **Scripts and their outputs:**
  - `donor_fix.py` → `donor_fix.json`: step 1;
  - `estimate.py` → `estimate.json` and `estimate_run2.json`: the estimates and the stop rule;
  - `l73.py`: the step-5 runner and its rule;
  - `compare.py` → `compare.json`: the tables above (`compare.py run1_asymmetric` gives run 1's);
  - `run_live.sh`: the live commands.

**Replay offline**, from the repository root, with no key and no network. The run IDs are as in I1. Add `--model gpt-6.1-sol --reasoning-effort high` or `--model gpt-5.6-luna` to replay the OpenAI caches. All nine run-2 domain outputs replay with identical `pairs`, `summary` and `length_stand_in`.

```
uv run --directory gapmap python -m gapmap.control2 --ledger ../reconstruct/runs/<run>/ledger.json \
  --sidecar ../reconstruct/runs/<run>/sidecar.json --domain "<name>" --out <dir holding the cache> \
  --audit-cache ../research/n3/<domain>/closure_judgements.json [--model M --reasoning-effort E]
```

On this code, the committed `research/n3/` maps replay byte-identically: `gapmap.json`, `gapmap.md` and the cache, in all three domains. `research/n3/`, `research/n3_control/` and `research/n3_control_luna/` are unchanged.
