# I1b: control2 with the judge swapped to gpt-5.6-luna (2026-10-24)

**Result.** With `gpt-5.6-luna` as the judge, control2 does not separate a candidate's own evidence from a donor's on the pre-declared primary comparison (seed-free, closed only, seed-resampled 95% CI lower bound above 0) in any domain:

| Domain | Primary own − control, Luna | Primary, qwen (I1) | Verdict, Luna (FakeJudge L7.3 flags) |
|---|---|---|---|
| PLC | +0.11 [−0.06, +0.30] | +0.04 [−0.09, +0.17] | uninformative |
| GDPR v1 | +0.10 [−0.06, +0.25] | +0.26 [+0.11, +0.39] | uninformative |
| GDPR v2 (not admissible) | +0.13 [−0.04, +0.32] | +0.29 [+0.14, +0.44] | not evidence |

With the real-judge L7.3 flags below, `control2.verdict` returns `design-wrong` for both judges in every domain.

Luna does separate the arms with the seed inside both (equal-cap, closed) in both admissible domains: PLC +0.13 [+0.02, +0.25] and GDPR v1 +0.14 [+0.02, +0.27]. Qwen does not separate them there. That comparison was not the declared primary.

The two judges agree only weakly, pair by pair. Cohen's kappa on closed/partial/open is 0.12 on PLC and 0.20 on GDPR v1 (0.14 pooled over 413 arm judgements). Luna closes far more often: its control rate on the primary comparison is 0.56 on PLC, against 0.15 for qwen.

The L7.3 checks were also run through both real judges, not only through the fake judge. Neither judge passes both:
- Luna fails the planted positive, because the donor arm carries the donor's own seed sentence.
- Qwen passes the planted positive but fires on the random-letter stand-in.

**Decision it feeds (I1 → I2).** A stronger judge does not rescue the primary comparison.
- Swapping qwen for Luna removes the one primary separation I1 found (GDPR v1). The separation it adds is on equal-cap only.
- Every difference in this item is a difference of judge: the model together with its serving and decoding settings. Qwen ran on Ollama with `format: json`, temperature 0 and seed 0; Luna ran on Chat Completions with `json_object` and reasoning effort medium. Prompts, pairs, domains and parser were shared. Each cache's keys are recomputed exactly from the same prompt set under its own model ID, and `pairs` matches.
- Luna is OpenAI's cost tier. Its model page says it "roughly corresponds to the nano model tier". So this does not test a top-tier judge.
- The real-judge L7.3 result changes I1's reading that "the planted positive fired, so the design-wrong branch does not apply". That holds only for `FakeJudge`. Through Luna, the planted positive does not fire, so control2's donor arm needs a fix before it is used as an MS1 instrument with any real judge. The fix: drop the donor's own seed sentences from its pool, or anchor the question to the seed's topic.

## Run

- **Model ID:** `gpt-5.6-luna`. It appears as that exact ID in `GET /v1/models`, and every call was served as `gpt-5.6-luna`.
- **Price:** $0.20 input and $1.20 output per 1M tokens. Source: platform.openai.com/docs/models/gpt-5.6-luna, read 2026-10-24. The spend counts reasoning tokens as output; the page does not say so. That is consistent with the recorded PLC spend: 71,158 × 0.20 + 79,829 × 1.20 per 1M = $0.110.
- **Settings**, recorded in each cache's `_meta`:
  - Chat Completions with `response_format: json_object`;
  - `reasoning_effort: medium` (the model's default);
  - `max_completion_tokens: 6000`;
  - no temperature sent.
- **Calls:** all 568 returned `finish_reason: stop`, and no arm was `undecided`.
- **Code.** The live run used `398ef7f`'s control2, semantic and prompt code, plus the OpenAI backend and CLI flags later committed in `35c7c64` (`judge.py`, and `control2.main` only). Just before it, `git diff 398ef7f i1-closure-control -- gapmap/` was empty. I1 then committed `535d7b5`, which adds only `control2.length_matched`, a post hoc summary that changes nothing the judge is sent. This branch was rebased onto `535d7b5`. Replaying the Luna caches offline on that code reproduces `pairs`, `summary`, `length_stand_in` and `audit_current` exactly. The replay also gives the length-matched rows (`<domain>/length_matched.json`).
- **Same pairs in both arms.** `pairs` (lens, seeds, donor, k), `length_stand_in` and `audit_current` are identical to I1's `research/n3_control/<domain>/control2.json`.

| | Calls | Prompt tokens | Completion tokens (reasoning) | Spend | Cap |
|---|---|---|---|---|---|
| PLC | 188 | 71,158 | 79,829 (70,188) | $0.110 | $1.50 |
| GDPR v1 | 200 | 90,550 | 81,094 (70,337) | $0.115 | $1.60 |
| GDPR v2 | 180 | 91,108 | 78,285 (68,531) | $0.112 | $1.50 |
| L7.3 fixtures | 18 | 2,802 | 2,925 (2,104) | $0.004 | $0.40 |
| **Total** | 586 | | | **$0.342** | $5.00 |

**Estimate before any call** (`estimate.json`): 616 calls.
- The expected cost was $0.83. It assumed 1,000 reasoning tokens per call; the measured figure was about 360.
- The worst case was $4.50, with every reply at the 6,000-token ceiling.

**Budget enforcement.** Before every call, the cap is checked against the spend so far plus that call's worst case. A blocked call raises `BudgetExceeded`, and the run is written as `complete: false`. No run was blocked.

`scripts/key_headroom.py` reads only the OpenRouter key, so it does not cover direct OpenAI spend.

## Discrimination checks (L7.3)

**Mechanical (FakeJudge, `gapmap/tests/test_control2.py`).** This is the same code as I1, and it passes on this branch: the planted positive fires and the stand-in does not.

**Real judge on the same fixture** (`l73.py`).
- The `CLOSES_HERE` marker is replaced by plain text: "When an intermittent fault appears, choose first the test whose failure likelihood is highest."
- The stand-in keeps the same word lengths with random letters, keeping `failure` and `likelihood`. It is run with RNG seeds 7, 8 and 9.
- Planted pair, k = 2:

| Judge | own_sf | ctrl_sf | Planted fires (seed-free) | Stand-in fires | `control2.verdict` |
|---|---|---|---|---|---|
| Luna | closed | closed | no | no (own_sf open, all 3 seeds) | design-wrong |
| qwen | closed | partial | yes | **yes** (own_sf closed, all 3 seeds) | design-wrong |

Why Luna's planted positive fails:
- The donor pool starts with the donor candidate's own seed sentences (`control2.py:123`, `(*seed_rows[j], *ranked[j])`).
- In the fixture, the control arm is "Sampling rate should be selected based on the suspected event." A donor seed is by construction a sentence of the same lens type. The SEL question ("Does any sentence state a condition that says which option to choose in which situation?") does not name the seed's topic.
- Luna answers it literally and closes the control arm: "Both sentences explicitly state that the sampling rate should be selected according to the suspected event."
- On the stand-in, Luna correctly leaves the own arm open, but it still closes the control arm. The pair difference is therefore negative.

Qwen closes the own arm on random letters, so it does not pass the stand-in.

**Length-only stand-in on the observed pairs.** This check does not use a judge, so it is identical for both arms (I1's numbers): PLC +0.11 [−0.08, +0.32], GDPR v1 **+0.28 [+0.06, +0.49]**, GDPR v2 +0.02 [−0.16, +0.20]. Luna's primary difference on GDPR v1 (+0.10) is below the length-only judge's.

**Best reachable difference.** This equals the share of pairs that can discriminate, the same as in I1: PLC 1.00, GDPR v1 0.98, GDPR v2 0.94.

## Per domain and lens (Luna)

Each cell is own rate vs control rate, then own − control with its seed-resampled 95% CI (2000 resamples). Only pairs that can discriminate (k ≥ 1) are used. The same small-n caveats as in I1 apply: PLC DIAG has 2 seed clusters, PLC SEL has 2 pairs, GDPR v1 SEL has 4, and HEDGE has 5.

### PLC

| Lens | Pairs | Can discriminate | Equal-cap, closed or partial | Equal-cap, closed | Seed-free, closed or partial | Seed-free, closed |
|---|---|---|---|---|---|---|
| DIAG | 9 | 9 (1.00) | 1.00 vs 0.00, +1.00 [+1.00, +1.00] | 0.11 vs 0.00, +0.11 [+0.00, +1.00] | 1.00 vs 0.89, +0.11 [+0.00, +1.00] | 1.00 vs 0.89, +0.11 [+0.00, +1.00] |
| RESULT | 19 | 19 (1.00) | 0.95 vs 0.89, +0.05 [−0.11, +0.21] | 0.79 vs 0.58, +0.21 [−0.05, +0.47] | 0.84 vs 0.95, −0.11 [−0.32, +0.11] | 0.63 vs 0.68, −0.05 [−0.37, +0.26] |
| SEL | 2 | 2 (1.00) | 1.00 vs 1.00, +0.00 [+0.00, +0.00] | 0.50 vs 1.00, −0.50 [−1.00, +0.00] | 1.00 vs 1.00, +0.00 [+0.00, +0.00] | 0.50 vs 1.00, −0.50 [−1.00, +0.00] |
| WHY | 24 | 24 (1.00) | 0.88 vs 0.75, +0.12 [+0.00, +0.29] | 0.75 vs 0.62, +0.12 [+0.00, +0.25] | 0.75 vs 0.54, +0.21 [+0.00, +0.46] | 0.58 vs 0.29, +0.29 [+0.08, +0.50] |
| **All** | 54 | 54 (1.00) | 0.93 vs 0.69, +0.24 [+0.02, +0.46] | 0.65 vs 0.52, +0.13 [+0.02, +0.25] | 0.83 vs 0.76, +0.07 [−0.08, +0.22] | 0.67 vs 0.56, +0.11 [−0.06, +0.30] |

### GDPR v1

| Lens | Pairs | Can discriminate | Equal-cap, closed or partial | Equal-cap, closed | Seed-free, closed or partial | Seed-free, closed |
|---|---|---|---|---|---|---|
| DISC | 13 | 12 (0.92) | 1.00 vs 0.75, +0.25 [+0.00, +0.50] | 0.92 vs 0.75, +0.17 [+0.00, +0.38] | 0.58 vs 0.42, +0.17 [−0.30, +0.50] | 0.50 vs 0.33, +0.17 [−0.30, +0.50] |
| HEDGE | 5 | 5 (1.00) | 0.80 vs 0.60, +0.20 [−0.40, +0.80] | 0.80 vs 0.60, +0.20 [−0.40, +0.80] | 0.60 vs 0.60, +0.00 [−0.60, +0.60] | 0.60 vs 0.60, +0.00 [−0.60, +0.60] |
| RESULT | 21 | 21 (1.00) | 0.81 vs 0.81, +0.00 [−0.24, +0.24] | 0.48 vs 0.38, +0.10 [−0.10, +0.29] | 0.81 vs 0.62, +0.19 [+0.00, +0.43] | 0.48 vs 0.43, +0.05 [−0.19, +0.29] |
| SEL | 4 | 4 (1.00) | 1.00 vs 1.00, +0.00 [+0.00, +0.00] | 1.00 vs 1.00, +0.00 [+0.00, +0.00] | 1.00 vs 1.00, +0.00 [+0.00, +0.00] | 1.00 vs 1.00, +0.00 [+0.00, +0.00] |
| WHY | 8 | 8 (1.00) | 0.50 vs 0.62, −0.12 [−0.38, +0.00] | 0.50 vs 0.25, +0.25 [+0.00, +0.62] | 0.38 vs 0.25, +0.12 [−0.25, +0.50] | 0.25 vs 0.00, +0.25 [+0.00, +0.62] |
| **All** | 51 | 50 (0.98) | 0.82 vs 0.76, +0.06 [−0.09, +0.20] | 0.66 vs 0.52, +0.14 [+0.02, +0.27] | 0.68 vs 0.54, +0.14 [−0.02, +0.29] | 0.50 vs 0.40, +0.10 [−0.06, +0.25] |

### GDPR v2 (not admissible: 140 pending verifications)

| Lens | Pairs | Can discriminate | Equal-cap, closed or partial | Equal-cap, closed | Seed-free, closed or partial | Seed-free, closed |
|---|---|---|---|---|---|---|
| DISC | 14 | 12 (0.86) | 0.75 vs 0.75, +0.00 [+0.00, +0.00] | 0.75 vs 0.67, +0.08 [+0.00, +0.21] | 0.75 vs 0.50, +0.25 [−0.08, +0.64] | 0.58 vs 0.17, +0.42 [+0.00, +0.73] |
| HEDGE | 5 | 5 (1.00) | 0.40 vs 0.00, +0.40 [+0.00, +0.80] | 0.20 vs 0.00, +0.20 [+0.00, +0.60] | 0.20 vs 0.00, +0.20 [+0.00, +0.60] | 0.20 vs 0.00, +0.20 [+0.00, +0.60] |
| RESULT | 9 | 9 (1.00) | 0.56 vs 0.67, −0.11 [−0.33, +0.00] | 0.33 vs 0.44, −0.11 [−0.44, +0.22] | 0.67 vs 0.67, +0.00 [−0.44, +0.44] | 0.11 vs 0.22, −0.11 [−0.44, +0.22] |
| SEL | 11 | 11 (1.00) | 1.00 vs 1.00, +0.00 [+0.00, +0.00] | 0.91 vs 0.91, +0.00 [+0.00, +0.00] | 1.00 vs 0.82, +0.18 [+0.00, +0.45] | 0.91 vs 0.64, +0.27 [+0.00, +0.55] |
| WHY | 9 | 8 (0.89) | 1.00 vs 0.88, +0.12 [+0.00, +0.38] | 0.75 vs 0.88, −0.12 [−0.50, +0.25] | 0.88 vs 0.75, +0.12 [+0.00, +0.38] | 0.38 vs 0.62, −0.25 [−0.62, +0.25] |
| **All** | 48 | 45 (0.94) | 0.78 vs 0.73, +0.04 [−0.04, +0.13] | 0.64 vs 0.64, +0.00 [−0.12, +0.12] | 0.76 vs 0.60, +0.16 [+0.00, +0.30] | 0.49 vs 0.36, +0.13 [−0.04, +0.32] |

## Back-to-back: qwen2.5:7b-instruct (I1) vs gpt-5.6-luna (I1b)

Both arms use the same pairs and prompts. The qwen numbers are from `research/n3_control/<domain>/control2.json` at `535d7b5`.

### All lenses, own − control

| Domain | Comparison, split | qwen | Luna |
|---|---|---|---|
| PLC | equal-cap, closed or partial | +0.04 [−0.07, +0.15] | **+0.24 [+0.02, +0.46]** |
| | equal-cap, closed | +0.07 [−0.02, +0.19] | **+0.13 [+0.02, +0.25]** |
| | seed-free, closed or partial | +0.09 [−0.05, +0.24] | +0.07 [−0.08, +0.22] |
| | seed-free, closed (primary) | +0.04 [−0.09, +0.17] | +0.11 [−0.06, +0.30] |
| GDPR v1 | equal-cap, closed or partial | +0.08 [−0.02, +0.18] | +0.06 [−0.09, +0.20] |
| | equal-cap, closed | +0.06 [−0.08, +0.20] | **+0.14 [+0.02, +0.27]** |
| | seed-free, closed or partial | **+0.16 [+0.06, +0.27]** | +0.14 [−0.02, +0.29] |
| | seed-free, closed (primary) | **+0.26 [+0.11, +0.39]** | +0.10 [−0.06, +0.25] |
| GDPR v2 (n/a) | seed-free, closed (primary) | +0.29 [+0.14, +0.44] | +0.13 [−0.04, +0.32] |

### Primary (seed-free, closed) by lens

| Domain | Lens | qwen | Luna |
|---|---|---|---|
| PLC | DIAG | +0.00 [+0.00, +0.00] | +0.11 [+0.00, +1.00] |
| | RESULT | +0.05 [−0.16, +0.26] | −0.05 [−0.37, +0.26] |
| | SEL | −0.50 [−1.00, +0.00] | −0.50 [−1.00, +0.00] |
| | WHY | +0.08 [−0.12, +0.29] | **+0.29 [+0.08, +0.50]** |
| GDPR v1 | DISC | +0.33 [+0.00, +0.57] | +0.17 [−0.30, +0.50] |
| | HEDGE | +0.20 [−0.40, +0.80] | +0.00 [−0.60, +0.60] |
| | RESULT | **+0.33 [+0.10, +0.57]** | +0.05 [−0.19, +0.29] |
| | SEL | +0.25 [+0.00, +0.75] | +0.00 [+0.00, +0.00] |
| | WHY | +0.00 [+0.00, +0.00] | +0.25 [+0.00, +0.62] |
| GDPR v2 (n/a) | DISC | +0.50 [+0.25, +0.75] | +0.42 [+0.00, +0.73] |
| | HEDGE | +0.20 [+0.00, +0.60] | +0.20 [+0.00, +0.60] |
| | RESULT | +0.00 [+0.00, +0.00] | −0.11 [−0.44, +0.22] |
| | SEL | +0.55 [+0.27, +0.82] | +0.27 [+0.00, +0.55] |
| | WHY | +0.00 [−0.38, +0.38] | −0.25 [−0.62, +0.25] |

### Length-matched subset (arm lengths within 25 %, post hoc, I1's `length_matched`)

| Domain | n | qwen, seed-free closed | Luna, seed-free closed | qwen, equal-cap closed | Luna, equal-cap closed |
|---|---|---|---|---|---|
| PLC | 46 | +0.00 [−0.12, +0.13] | +0.11 [−0.07, +0.32] | +0.04 [−0.06, +0.16] | +0.13 [+0.00, +0.27] |
| GDPR v1 | 27 | **+0.22 [+0.04, +0.41]** | +0.19 [−0.04, +0.40] | +0.00 [−0.15, +0.16] | **+0.19 [+0.04, +0.34]** |
| GDPR v2 (n/a) | 32 | +0.28 [+0.14, +0.44] | +0.03 [−0.16, +0.21] | +0.06 [+0.00, +0.15] | +0.00 [−0.16, +0.15] |

On the 27 length-matched GDPR v1 pairs, the two judges give nearly the same seed-free point estimate (+0.22 qwen, +0.19 Luna). Only qwen's interval excludes 0.

### Per-pair agreement

The unit is one arm judgement (pair × arm, 4 per pair), comparing closed/partial/open. Qwen's 3 `undecided` PLC arms are excluded.

| Domain | Lens | n | Raw agreement | Cohen's kappa |
|---|---|---|---|---|
| PLC | DIAG | 36 | 0.28 | 0.07 |
| | RESULT | 76 | 0.32 | 0.05 |
| | SEL | 8 | 0.62 | −0.09 |
| | WHY | 93 | 0.43 | 0.14 |
| | **All** | 213 | 0.37 | **0.12** |
| GDPR v1 | DISC | 48 | 0.69 | 0.37 |
| | HEDGE | 20 | 0.25 | 0.04 |
| | RESULT | 84 | 0.30 | −0.10 |
| | SEL | 16 | 0.94 | 0.00 |
| | WHY | 32 | 0.59 | 0.13 |
| | **All** | 200 | 0.485 | **0.20** |
| GDPR v2 (n/a) | **All** | 180 | 0.52 | 0.29 |
| Admissible pooled | | 413 | 0.43 | 0.14 |

Luna gives 232 of the 413 admissible arm judgements `closed`, against 138 for qwen. Most disagreements are Luna `closed` where qwen says `open` (71) or `partial` (62); the reverse, qwen `closed` with Luna `open`, happens 13 times.

## Reading it (judge model only, L7.4)

The arms differ only in the judge (the model with its serving and decoding settings), so every contrast below is a contrast of judge.
- **Where the separation appears moves with the judge model.**
  - With Luna, the separation appears when the seed is in both arms.
  - With qwen, it appears only when the seed is out of both arms.
  - Neither judge separates the arms on both comparisons in any admissible domain.
- **The judges agree on fewer than half the arm judgements, and only slightly above chance.** Raw agreement is 0.43 and kappa 0.14, pooled. Whatever qwen's closure rates measure, Luna's measure something largely different on the same prompts.
- **The control design fails a real judge either way.**
  - Luna reads the donor's same-lens seed as an answer to a topic-free question.
  - Qwen closes on random letters.
  - So the planted positive and the stand-in, as built, are not yet a working L7.3 proof for any real judge. They prove the plumbing.

**Limits.**
- One OpenAI tier was tested, at one reasoning effort.
- Lenses, lexicons and thresholds are in-sample.
- DIAG is judged through its first rival only.
- The length-matched restriction is post hoc.
- The real-judge L7.3 check uses one fixture (SEL).

## Files

- `plc/`, `gdpr_v1/`, `gdpr_v2/`: per domain:
  - `control2.json`, the live run, with `spend` and `judge_settings`;
  - `closure_judgements.json`, the Luna cache with `_meta`;
  - `judge_calls.jsonl`, per-call usage and cost;
  - `length_matched.json`, the offline replay of 535d7b5's `length_matched` on this branch (`--model gpt-5.6-luna` needs the backend from 35c7c64).
- `l73.py`, `l73/`: the real-judge L7.3 fixture checks for both judges, with their caches.
- `estimate.py`, `estimate.json`: the pre-run estimate.
- `run_live.sh`: the live commands with their caps.
- `compare.py`: the tables above. Pass `--qwen research/n3_control` for the back-to-back rows.

**Replay offline, with no key and no network:**

```
uv run --directory gapmap python -m gapmap.control2 --ledger ../reconstruct/runs/<run>/ledger.json \
  --sidecar ../reconstruct/runs/<run>/sidecar.json --domain "<name>" --out <dir holding the cache> \
  --audit-cache ../research/n3/<domain>/closure_judgements.json --model gpt-5.6-luna
```
