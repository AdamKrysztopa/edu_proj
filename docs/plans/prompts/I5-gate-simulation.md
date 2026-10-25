# I5: Gate reachability, §14.3 baselines and AUROC code

**Branch:** `i5-gate-simulation`
**Outputs:**
- code: `residual/src/residual/auroc.py`, `residual/src/residual/baselines.py` and `residual/src/residual/reach.py`, with tests;
- results: `research/gate_sim/RESULT.md` and its grid outputs, labelled `SYNTHETIC` where simulated.

**Cost:** $0.

## Context
- Read `docs/plans/implement-queue.md` § I5 and `docs/plans/coverage-audit.md` findings 3, 8, 20 and 22.
- Read `REORIENTATION.md` §14.3 (the scoring rule and the baseline list) and §22 (the N2 and N3 gate rows, and the threshold table).
- Read `research/n2/e_plant_eabst_report.md` (the run-1 baselines: a_u 5/24, floor 8; E-ABST 5/24 answered).
- Read the power note in `docs/plans/n3-gap-map-plan.md:21`.
- **Set by the owner (2026-10-24; `REORIENTATION.md` §22 threshold table, `research/ds3-decisive-delta.md`). Use these, not placeholders:**
  - δ = 0.10;
  - golds pooled by common effect as fixed strata; random effects only as a sensitivity;
  - across baselines: intersection–union for Continue (beat every baseline), Bonferroni for Stop;
  - across looks: boundary c = 1.85 at both looks; the fallback gold is pooled into the primary set once, never read alone;
  - DS3 expects about 79% of areas missed: a 16/4 split of 20 areas per gold (15/5 is DS3's computed case).
- DS3's 0.86 / 0.39 (P(Continue | gain 0.20), P(Stop | no gain)) were computed at one baseline, the unadjusted 1.645 boundary and balanced areas. This item replaces them at the set rules and the expected split.
- No AUROC or baseline code exists in the repository today.

## Steps
1. **`auroc.py`.** Build:
   - AUROC with tie handling;
   - a paired ΔAUROC with a cluster bootstrap that resamples clusters, with DeLong as a cross-check where clusters are absent;
   - common-effect pooling of ΔAUROC across golds as fixed strata, with random-effects pooling as a sensitivity.

   Test against known values: a perfect score gives 1, a constant gives 0.5, and include a published DeLong example.
2. **`baselines.py`.** Specify each baseline as a typed, dated function. The **competing set K** is DS3's (§4, §7): area size measured in the pre-gold partition, retrieval-support density, corpus term frequency, plain-LLM ranking (spec only: model, prompt and date, no call), the cross-gold type prior when at least 2 other golds exist, and Jev/text-form. Random and the naive type rule are built and **reported only**, never in K. Verbalised confidence is a spec only. Gold items per area appears in step 5 only (a near-oracle), never in K.

   **Gate statistic:** intersection–union for Continue (every pairwise lower bound above 0 at boundary c, and the minimum point estimate at least δ); Bonferroni over K for Stop. Report the bootstrap minimum and max-T beside them (DS3 §9.5), never as the gate: the bootstrap minimum stopped 55% of maps that truly beat every baseline (DS3 §4).
3. **`reach.py`, N2.** From the run-1 baselines, enumerate every reachable reading of E-PLANT and E-ABST under the registered rules. Print the best reachable reading. Expect that Continue is unreachable for E-PLANT. Then report the floor an amendment would need for Continue to be reachable.
4. **N3 simulation.** Simulate areas with missed and not-missed labels and with predictor and baseline scores. Use 1, 2 and 3 golds of 15, 20 and 30 areas, missed share 0.3–0.6, clustering ICC 0–0.3, ties, and predictor and baseline correlation 0.3–0.9.

   Add the class splits balanced, 15/5 and 16/4, and 4–6 golds (the fallback pooled once). δ = 0.10; show 0.05 and 0.15 as sensitivities only. For each cell, report the frequency of Continue, Stop and inconclusive under the §22 N3 rule as set (common effect, intersection–union Continue, Bonferroni Stop, c = 1.85 at both looks, fallback pooled once). Report the report's MS3 screen and MS5 as secondary rows.

   L7.3, stated before the grid runs:
   - **Best reachable case:** a perfect predictor at 3 golds × 20 areas, 16/4. Report its P(Continue); if it is below 0.8, the design cannot Continue at all, and that is the first line of the result.
   - **Planted positive:** a true gain of 0.20 over every baseline must give P(Continue) ≥ 0.8 in every cell whose pooled minority class is at least 25 (DS3's floor). Report cells below the floor separately, not as failures of the predictor.
   - **Stand-ins:** a random score, and area size plus noise (correlation 0.9 with size), must each give P(Continue) ≤ 0.05.
   - A pooled minority class of 25 is unreachable at 3 × 20 areas with 79% missed: report the minimum areas per gold that make Stop decisive (P(Stop | no gain) ≥ 0.8) at 16/4.
   - The threshold table says I5 re-derives c: run the grid at c = 1.85 (set) and report the c that holds the false-Continue rate at 0.05 under these assumptions. A different c is a proposal for the owner, not a change.
5. **The near-oracle check.** Show whether the "gold items per area" baseline makes Continue unreachable for a predictor that is truly informative. If it does, recommend excluding it, or defining it on a pre-gold proxy.

## Done when
- The tests pass, and the freeze check shows no drift.
- `RESULT.md` gives: N2's reachable regions and the amendment floor; per-design decision frequencies; a recommendation on minimum areas, the number of golds and multiplicity; and the near-oracle ruling.

## Decision it feeds
- The §22 threshold rows: the δ row's figures are replaced by this item's at the set rules and 16/4; the minimum areas per gold and class are proposed. The owner decides, through `methods-critic`.
- Whether an E-PLANT floor amendment is worth registering before any N2 rerun.
