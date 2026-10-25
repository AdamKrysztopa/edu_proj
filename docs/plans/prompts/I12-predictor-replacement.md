# I12: Replace the gap-map predictor that is source count in disguise

New 2026-10-24, from I6's result.

**Branch:** `i12-predictor`, from `plans-2026-10-24`.
**Outputs:** code in `gapmap/src/gapmap/area.py` (new functions; the I6 score stays replayable) with tests; note `research/area_score/PREDICTOR.md` with its `report.json` (`_common.md` § Finish).
**Cost:** $0. Replay only, no network.

## Context
- Read `research/area_score/RESULT.md` whole and `docs/plans/implement-queue.md` § I6.
- I6's finding: on PLC the candidate score has Spearman ρ = 0.96 with `k_topic` (independent-source count) over all 24 merged HYP candidates, against a pre-stated trip line of |ρ| ≥ 0.8. The rubric's main term is a step function of the source count. The noisy-OR area score saturates (0.991–0.999 on every candidate-bearing PLC area), and the max ties three of four areas.
- Six of the 20 frozen features are constant in every ledger and two are missing everywhere. The E-CTA pre-registration tests size, density and type plus the lens signal only.
- Area size and retrieval-support density are §14.3 baselines (`REORIENTATION.md` §14.3). A predictor that is a monotone function of either can at best tie that baseline: ΔAUROC near 0 by construction.
- GDPR v1 has one HYP, so association checks run on PLC; GDPR v2 is reported, not decided on (140 pending verdicts).
- **The candidate pool is conditional on an ineligible judge.** Which candidates are HYP, and the rubric's P term, come from qwen 7b's closure caches (`research/n3/*/closure_judgements.json`; `gapmap/src/gapmap/area.py:260`, `record.py:114-122`). qwen 7b failed the real-judge L7.3 check (`research/n3_control_v3/RESULT.md`). Use no closure term in any predictor, say in the note that every result is conditional on that pool, and leave re-judging the gap map's closure to the wave 3 item (sol plus I2's guard judge) that the MS2 freeze needs.

## Steps
1. **Pre-state the rules and commit them before computing any association** (as I6 did in `ef5131e`). In that commit, also declare a **lens-signal reference** built from lens type and lexical state only: no `k_topic`, no `k_step`, no closure term. A candidate predictor passes only if all hold:
   - (a) it does not trip I6's test (|ρ| ≥ 0.8 with `k_topic`, `|X|`, `n_claims` or `evidence_density`, both signs, uncapped HYP population), nor |ρ| ≥ 0.8 with `k_step`;
   - (b) its pooled within-`k_topic`-stratum Spearman with the lens-signal reference is at least 0.5, and its |ρ| with candidate text length is below 0.3;
   - (c) uniform-random and length-only stand-ins fail (b) in at least 95% of 2,000 draws (seed 0).

   An area aggregate is a mean or a fixed top-k mean, never monotone in candidate count (no noisy-OR, no sum). PLC has 4 strata with 2 or more candidates and 4 candidate-bearing areas, so area-level association with size is untestable there: say so rather than report it as a pass.
2. **Build two or three candidate predictors** that carry the lens signal net of source count, for example:
   - the rubric's lens terms ranked within `k_topic` strata (residualised on source count and density);
   - an area aggregate that does not saturate (a mean or a top-k mean of candidate weights, not a noisy-OR).
   Each is a typed, deterministic function with no new ledger field.
3. **L7.3 for the checks:** a planted score equal to `k_topic` fails (a); the stand-ins fail (b) as (c) requires; a planted score equal to the lens-signal reference plus small noise, independent of `k_topic`, passes all three.
4. Run every candidate through step 1's rules on PLC (GDPR v1 and v2 reported). Never compute anything against a gold; this is structural only.

## Owner decision (stop and ask, `_common.md`)
Which candidate becomes the E-CTA predictor that I7 freezes. Order the options by merit, recommend one with its numbers, and say what would change the recommendation. If none passes, say so first and offer: (a) pre-register the lens signal as the predictor and accept that ΔAUROC may tie the density baseline, or (b) defer E-CTA until boundary sources (DS7) revive a feature.

## Done when
`PREDICTOR.md` and `report.json` give each candidate's ρ with every covariate, its within-stratum result, its area-level spread, and the L7.3 results. The rules commit predates every association. Tests pass. `citation-verifier` has passed on the note.

## Decision it feeds
The predictor that I7's manifest hashes and the MS2 freeze uses. Also the threshold-table blank "primary model and baseline", with I5 and DS5.
