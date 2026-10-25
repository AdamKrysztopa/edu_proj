# I1: the closure control, rebuilt so it can discriminate (2026-10-24)

**Result.** The rebuilt control (`gapmap/src/gapmap/control2.py`) works mechanically. The planted positive fires, the fixture stand-in does not, and 149 of 153 pairs can discriminate (the old control had 121 of 153 with non-identical arms). The local qwen judge separates a candidate's own evidence from a donor's in GDPR v1, but only once the seed is taken out of the arms, and a length-only judge passes there too (see the length caveat). It does not separate them in PLC.

On the pre-declared primary comparison (seed-free, closed only, seed-resampled 95% CI lower bound above 0):

| Domain | Primary own − control | Verdict |
|---|---|---|
| PLC | +0.04 [−0.09, +0.17] | uninformative |
| GDPR v1 | +0.26 [+0.11, +0.39] | discriminates (see the length caveat) |
| GDPR v2 (not admissible) | +0.29 [+0.14, +0.44] | not evidence |

With the seed inside both arms (equal-cap, closed), neither admissible domain separates: PLC +0.07 [−0.02, +0.19], GDPR v1 +0.06 [−0.08, +0.20].

**Length caveat.** A judge that reads only arm length also passes on GDPR v1: +0.28 [+0.06, +0.49]. Own arms there run longer than donor arms (median ratio 1.22). On the 27 GDPR v1 pairs whose arm lengths are within 25 % of each other, the primary difference holds at +0.22 [+0.04, +0.41]. That restriction was added after the stand-in result, so it is post hoc.

**Decision it feeds.** This sits between the item's first two branches.
- Control2 is the MS1 instrument candidate, with two changes before anything is registered:
  - the comparison is seed-free;
  - the two arms are matched on non-seed length, or the length stand-in becomes part of the gate.
- Qwen is uninformative in PLC even on the count-matched control, where the arms are also close in length (median own/donor ratio 1.04; 46 of 54 pairs within 25 %). I2 should run Jev on control2 to test whether a different judge separates there.
- The planted positive fired, so the design-wrong branch does not apply.

## What was built

- **Parser precondition** (`semantic.py`). A reply is `undecided` unless `states` or `partially` is present and every present key is a list (finding 11).
  - Replay of all 641 committed replies (PLC 193, GDPR v1 229, GDPR v2 219): 0 flips. The 16 states-only replies stay decided.
  - All three committed maps replay byte-identically: `gapmap.json`, `gapmap.md` and the cache.
- **Retrieval.** Retrieval scoring is factored into `seed_sentences` / `ranked_sentences`. The replay is still byte-identical.
- **Control2.** For each lens with at least 2 candidates, candidate *i* is paired with the nearest other candidate *j* of the same lens.
  - Nearness is the maximum Jaccard over probe stems. Ties go to sorted seed claim ids, then the lens, never the config hash (finding 7).
  - Both arms carry the same number `k = min(8, |own pool|, |donor pool|)` of other-source, non-seed sentences. The cap applies after the seed (finding 6).
  - The donor pool is *j*'s retrieval minus *i*'s seed source and minus *i*'s own capped pool, so the arms share no non-seed sentence.
  - Equal-cap arms are *i*'s seed plus *k*. Seed-free arms are the *k* sentences alone.
  - Only pairs with `k ≥ 1` are judged, so an empty arm never reads "open" without a judge call (finding 9).
  - Both splits are reported (finding 8). Intervals use 2000 cluster-bootstrap resamples by seed claim (the smallest seed claim id of the probe).
- **Fixed before the run.** The primary rule was committed before any control2 judgement (commit `398ef7f`).
- **Outputs.** All outputs went to `research/n3_control/<domain>/`: `control2.json` and a new `closure_judgements.json` (finding 18). `research/n3/` is unchanged.

## The current control, measured (step 2, offline from the committed caches)

| | PLC | GDPR v1 | GDPR v2 | Total |
|---|---|---|---|---|
| Pairs | 54 | 51 | 48 | 153 |
| Identical arms | 8 | 11 | 13 | 32 |
| Own arm closed or partial | 48 | 49 | 46 | 143 |
| … resting on seed sentences only | 38 | 27 | 26 | 91 |
| Control arm truncated by the cap | 30 | 28 | 22 | **80** |
| Own arm truncated by the cap | 0 | 0 | 0 | 0 |
| Seed alone fills the cap | 0 | 10 | 9 | **19** |
| Donor tied | 18 | 19 | 16 | **53** |
| Own other-source pool empty | 0 | 11 | 10 | **21** |
| Donor other-source pool empty | 0 | 6 | 1 | **7** |

Every count in the audit's finding 6 reproduces. The donor tie count stays at 53 under control2, because the ties are in the Jaccard score. They are now broken deterministically, independent of the config hash.

## Discrimination proof (L7.3)

All of these are in `gapmap/tests/test_control2.py` and all pass.
- **Planted positive.** The element is stated (with the `CLOSES_HERE` marker) in an other-source sentence in the own arm only; by the fixture's design, no donor pool carries it. It fires: own closed, control not, in both the equal-cap and the seed-free arms, and own − control > 0 for the lens.
- **Length-matched stand-in.** The same sentence with every word replaced by random letters of the same length; only the two retrieval words `failure` and `likelihood` are kept, so it is retrieved in the same place. It does not fire: own − control ≤ 0.
- **Count stand-in.** A judge that closes on the number of offered sentences gives own = control on every pair, because the caps are equal.
- **Best reachable difference** on the observed data is, by definition, the share that can discriminate (own always closed, control never):

  | | Pairs that can discriminate | Best reachable difference |
  |---|---|---|
  | PLC | 54/54 | 1.00 |
  | GDPR v1 | 50/51 | 0.98 |
  | GDPR v2 | 45/48 | 0.94 |

  Within the pairs that can discriminate, the best reachable difference is 1.0.

### Stand-in on the observed pairs

A "judge" closes an arm whose non-seed character total reaches the median over all arms. Its result is the seed-free, closed difference.

| Domain | Length-only own − control | Primary on pairs within 25 % in length (n) |
|---|---|---|
| PLC | +0.11 [−0.08, +0.32] | +0.00 [−0.12, +0.13] (46) |
| GDPR v1 | **+0.28 [+0.06, +0.49]** | +0.22 [+0.04, +0.41] (27) |
| GDPR v2 | +0.02 [−0.16, +0.20] | +0.28 [+0.14, +0.44] (32) |

## Per domain and lens

Each cell is own − control with its seed-resampled 95% CI. Every comparison uses only pairs that can discriminate (k ≥ 1). The CIs for PLC DIAG (2 seed clusters), PLC SEL (2 pairs), GDPR v1 SEL (4) and HEDGE in both GDPR runs (5) carry no information.

### PLC

| Lens | Pairs | Can discriminate | Equal-cap, closed or partial | Equal-cap, closed | Seed-free, closed or partial | Seed-free, closed |
|---|---|---|---|---|---|---|
| DIAG | 9 | 9 (1.00) | +0.11 [+0.00, +1.00] | +0.00 [+0.00, +0.00] | +0.11 [+0.00, +1.00] | +0.00 [+0.00, +0.00] |
| RESULT | 19 | 19 (1.00) | +0.00 [-0.16, +0.16] | +0.16 [+0.00, +0.32] | +0.16 [-0.11, +0.42] | +0.05 [-0.16, +0.26] |
| SEL | 2 | 2 (1.00) | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | -0.50 [-1.00, +0.00] | -0.50 [-1.00, +0.00] |
| WHY | 24 | 24 (1.00) | +0.04 [-0.12, +0.21] | +0.04 [-0.12, +0.21] | +0.08 [-0.12, +0.29] | +0.08 [-0.12, +0.29] |
| **All** | 54 | 54 (1.00) | +0.04 [-0.07, +0.15] | +0.07 [-0.02, +0.19] | +0.09 [-0.05, +0.24] | +0.04 [-0.09, +0.17] |

Primary rates (seed-free, closed): own 0.19, control 0.15, 36 seed clusters. 3 WHY arms were `undecided`.

### GDPR v1

| Lens | Pairs | Can discriminate | Equal-cap, closed or partial | Equal-cap, closed | Seed-free, closed or partial | Seed-free, closed |
|---|---|---|---|---|---|---|
| DISC | 13 | 12 (0.92) | +0.08 [+0.00, +0.30] | +0.00 [+0.00, +0.00] | +0.25 [+0.05, +0.50] | +0.33 [+0.00, +0.57] |
| HEDGE | 5 | 5 (1.00) | +0.20 [+0.00, +0.60] | +0.00 [-0.60, +0.60] | +0.40 [+0.00, +0.80] | +0.20 [-0.40, +0.80] |
| RESULT | 21 | 21 (1.00) | +0.05 [+0.00, +0.14] | +0.14 [-0.10, +0.38] | +0.14 [+0.00, +0.29] | +0.33 [+0.10, +0.57] |
| SEL | 4 | 4 (1.00) | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.25 [+0.00, +0.75] |
| WHY | 8 | 8 (1.00) | +0.12 [-0.25, +0.50] | +0.00 [-0.38, +0.38] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] |
| **All** | 51 | 50 (0.98) | +0.08 [-0.02, +0.18] | +0.06 [-0.08, +0.20] | +0.16 [+0.06, +0.27] | +0.26 [+0.11, +0.39] |

Primary rates (seed-free, closed): own 0.52, control 0.26, 45 seed clusters.

### GDPR v2 (not admissible: 140 pending verifications)

| Lens | Pairs | Can discriminate | Equal-cap, closed or partial | Equal-cap, closed | Seed-free, closed or partial | Seed-free, closed |
|---|---|---|---|---|---|---|
| DISC | 14 | 12 (0.86) | +0.08 [+0.00, +0.27] | +0.08 [+0.00, +0.21] | +0.00 [+0.00, +0.00] | +0.50 [+0.25, +0.75] |
| HEDGE | 5 | 5 (1.00) | +0.40 [+0.00, +0.80] | +0.00 [+0.00, +0.00] | +0.60 [+0.20, +1.00] | +0.20 [+0.00, +0.60] |
| RESULT | 9 | 9 (1.00) | +0.00 [-0.33, +0.33] | +0.00 [+0.00, +0.00] | +0.33 [+0.00, +0.67] | +0.00 [+0.00, +0.00] |
| SEL | 11 | 11 (1.00) | +0.00 [+0.00, +0.00] | +0.09 [+0.00, +0.27] | +0.09 [+0.00, +0.27] | +0.55 [+0.27, +0.82] |
| WHY | 9 | 8 (0.89) | +0.12 [+0.00, +0.38] | +0.12 [+0.00, +0.38] | +0.25 [-0.25, +0.62] | +0.00 [-0.38, +0.38] |
| **All** | 48 | 45 (0.94) | +0.09 [+0.00, +0.20] | +0.07 [+0.00, +0.14] | +0.20 [+0.07, +0.33] | +0.29 [+0.14, +0.44] |

Primary rates (seed-free, closed): own 0.40, control 0.11, 42 seed clusters.

## Reading it

- **The seed still decides most closures.**
  - Under the old control, 91 of 143 own-arm closures cited seed sentences only.
  - Under control2, putting the seed back into both arms brings the difference to about 0 in both admissible domains. The seed-free arms are the only place where qwen reacts to whose evidence it is shown.
  - So an MS1 that codes pools with the seed included would be measuring the seed.
- **Rates are lower than under the old control.** On PLC, equal-cap closed-or-partial is now 0.59 for the own arm, against 0.89 in the committed map (`research/n3/README.md`). The arms now carry 8 other-source sentences next to the seed. This item does not test whether longer prompts make qwen close less often.
- **Limits.**
  - Every lens, lexicon and threshold is in-sample on these ledgers.
  - Donor ties remain in 53 pairs (now broken deterministically).
  - DIAG is judged through its first rival only.
  - The length-matched restriction is post hoc.

## Reproduce

Live judgements are local Ollama `qwen2.5:7b-instruct` at $0. Omit `--judge ollama` to replay from the cache, offline.

```
uv run --directory gapmap python -m gapmap.control2 \
  --ledger ../reconstruct/runs/<run>/ledger.json --sidecar ../reconstruct/runs/<run>/sidecar.json \
  --domain "<name>" --out ../research/n3_control/<domain> \
  --audit-cache ../research/n3/<domain>/closure_judgements.json [--judge ollama]
```

The runs are:
- PLC: `20260928T133336Z-59ec876b3d7e`
- GDPR v1: `20260928T135354Z-eb840a85b7d1`
- GDPR v2: `20260928T145943Z-bc1cc9a30a02`

Run the command from the repository root; `--directory gapmap` makes the `../` paths resolve from `gapmap/`. Caches: PLC 188, GDPR v1 200, GDPR v2 180 replies.
