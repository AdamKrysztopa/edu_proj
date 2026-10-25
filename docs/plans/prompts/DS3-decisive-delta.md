# DS3: Can N3 give a decisive reading at a meaningful δ?

**Branch:** `ds3-decisive-delta`
**Output:** `research/ds3-decisive-delta.md`
**Method:** the `research` skill (statistics literature, OpenAlex). If you need a computation, write a scratch script in the session's scratchpad. Never write it into a package; the code belongs to I5.

## Context
- `docs/plans/deep-search-queue.md` § DS3.
- `REORIENTATION.md` §14.3 (the scoring rule and the baselines) and the threshold table in §22.
- `report/sections/17_validation.tex` (the recommended δ = 0.05; the MS3 and MS5 rules; the conditional AUROC within density tertiles, around lines 95-99).
- `docs/plans/n3-gap-map-plan.md:21` (Hanley–McNeil: about ±0.20 at 20 areas).
- `docs/plans/coverage-audit.md` findings 3 and 20.

## Questions
1. What smallest effects of interest for ΔAUROC are used in screening and risk-prediction research, and how were they justified? Is δ = 0.05 sourced anywhere in the repo or in the literature?
2. Which tests fit a **paired, clustered** AUROC comparison when there are many ties? Consider DeLong, the Obuchowski clustered method, and the cluster bootstrap. Where does each break down: small n, class imbalance, ties?
3. How do you pool ΔAUROC across 2–5 golds of 15–30 areas each with random effects? What do τ² estimates and intervals do with so few studies?
4. Choosing the strongest baseline: what does selecting the maximum of several baselines inside each bootstrap resample do to error rates?
5. How should unmappable gold items be scored? The plan counts them as missed areas at a floor score. What precedents exist?
6. Which baselines can be specified before gold? Is "gold items per area" a near-oracle?

## Done when
- The note proposes a value, with its source, for each of: δ, the test, the pooling method, the minimum number of areas per gold, the minimum number of golds, the multiplicity rule (Holm or pooled), the fallback order and the unmappable floor. It also states the assumptions I5 must simulate.
- `citation-verifier` has passed on it.

## Decision it feeds
- I5's simulation inputs.
- The §22 threshold-table rows. The owner sets those through `methods-critic`; this note only proposes values.
