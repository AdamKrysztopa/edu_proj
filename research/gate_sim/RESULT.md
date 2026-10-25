# I5: gate reachability, the §14.3 baselines and AUROC code

- **Question:** At the N3 rules set on 2026-10-24 and the expected 16/4 split, which designs can read Continue or Stop? And can N2's registered gates still read Continue?
- **Answer:** A true gain of 0.20 continues with P = 0.62 at DS3's 3 golds × 20 areas (16/4, ICC 0, map–baseline correlation r = 0.6). P ≥ 0.8 needs 5 × 20 (0.855) or 3 × 30 (0.892) at r = 0.6, and 5 × 30 (0.843) at r = 0.3. A true null stops with P = 0.44 at 3 × 20 and r = 0.6 (0.44–0.53 over three to six golds of 20). E-PLANT cannot read Continue (best: Change). (SYNTHETIC.)
- **Changed:** The minimum design is adopted (owner, 2026-10-24) as a function of the map–baseline correlation, measured on the pre-gold partition before gold, instead of DS3's fixed minority floor of 25. Two baselines change in K: the rank mean of K joins it, and gold items per area leaves it. No E-PLANT floor amendment is proposed.

**SYNTHETIC: a known-truth planning simulation from the specification in `grid.json`.** It informs the §22 threshold rows and is never a criterion or a gate input. The N2 part (§1) is an exact enumeration, not a simulation.
- Date: 2026-10-24. Cost: $0, no model calls.
- These figures replace DS3's 0.86 / 0.39, which assumed one baseline, the 1.645 boundary and balanced classes.

**Reproduce:**
- `uv run --directory reconstruct python ../research/gate_sim/reach_n2.py` (about 30 s).
- `uv run --directory residual python ../research/gate_sim/simulate.py` (about 13 min on 11 cores).
- `uv run --directory residual python ../research/gate_sim/keycells.py` (about 6 min).
- `python3 research/gate_sim/analyse.py`.

**Sources.**
- Every figure is read from `summary.json`, which `analyse.py` builds from `cells.json.gz`, `l73_cells.json.gz`, `bootstrap.json`, `near_oracle.json`, `stand_in_mean_of_k.json`, `null_one_strong_r.json` and `n2_reach.json`.
- `tables.md` holds the design table.
- After the grid ran, `baselines.py` changed (hash `1cf24c…` in `grid.json`, `547fdd…` now); the author reports a docstring-only edit, which cannot be checked from history.

**Reviews.** `methods-critic` and `citation-verifier` reviewed the first draft. Their corrections are folded in, among them a wrong pairing of a floor of 30 with designs that reach 20 and 18 (lesson queued in `docs/lessons.md`).

## Result and the decision it feeds

The rules as set separate a large gain from no gain, and the stand-ins do not pass, once one combination baseline is added (§3). The operating characteristics, though, depend most on a quantity nobody has measured yet: **r, the correlation between the map's scores and each baseline's scores**.
- **At r = 0.6, no gain.** Golds of 20 areas at 16/4 stop a null map with P = 0.44–0.53 at r = 0.6, at three to six golds (0.44–0.48 at ICC 0). With no gain, E-CTA most often reads inconclusive, and by the owner's rule (2026-10-24) the decision then passes to E-OSS (whose first SYNTHETIC power estimate, DS8 §5, warns it may stop even an oracle map under over-dispersed counts). E-CTA can still stop H1 on its own: about 45% of the time at no gain, and about 6% of the time at 3 × 20 (5% at 5 × 20) when the true gain is exactly δ (a false Stop).
- **At r = 0.9.** Five golds of 20 stop a null map with P = 0.87.
- **E-OSS has not been simulated.** Nothing here shows its power to Stop.

**Decision fed:** the owner decided 2026-10-24 (`docs/plans/implement-queue.md` § I5): the minimum design keyed to r, K plus a pre-registered rank mean without gold items per area, c = 1.85 for both, clustered DeLong with a cluster-bootstrap co-gate, and no E-PLANT floor amendment. Still to enter: the §22 δ row's figures, which this note replaces.

## 1. N2: reachable readings under the registered rules (exact)

Both registered rules are called directly: `reconstruct.eplant.eplant_decision` and `reconstruct.eabst.e_abst_gate`. They run over every count the unrun arms could still produce, given the run-1 baselines (`research/n2/e_plant_eabst_report.md` §1.1 and §2.1). The space applies arithmetic constraints only, so the reachable set is a superset of what the pipeline could produce. Results are in `n2_reach.json`.

**E-PLANT** (a_u = 5 of 24; floor ⌈24/3⌉ = 8):
- **Continue is unreachable.** Over 1,386,699 count tuples, the readings are Change (742,343) and Stop (644,356). The best reachable reading is **Change**.
- With t-conc-08 excluded, the enumeration uses 5 of 23. Amendment 2 P4 keeps the floor on all 24 targets. The reading is the same either way, because ⌈23/3⌉ = ⌈24/3⌉ = 8.
- **The amendment floor.** `eplant_decision` reads a_u_full only in its floor check (`eplant.py:534`). Suppose the floor were met. Then Continue occurs in one corner only: b = 5, c = 0, with McNemar p = 1/32 = 0.031, e ≥ ⌈n/3⌉ and r_g ≥ ⌈n/2⌉. That corner needs all five baseline adoptions to survive the cap rule, the gated arm to adopt none of them, and no new adoption.
- So an amendment opens Continue only with a floor of at most 5. That is ⌈n/5⌉, or 21% of 24 targets.

**E-ABST** (5 of 24 raw answers): Continue is reachable in 35 of 95,750 tuples, in the seven corners already in the closeout report:
- f_r = 5, f_p = 0 at every n_included from 20 to 24;
- f_r = 4, f_p = 0 at n_included = 20;
- f_r = 5, f_p = 1 at n_included = 20.

Inconclusive dominates, with 92,300 tuples.

**Recommendation on the E-PLANT amendment: do not register it.**
- The registered floor ⌈n/3⌉ asks for 33% baseline adoption, which is itself about half the > 60% expected from ClashEval-style evidence (`docs/n2-eplant-eabst-protocol.md:83`). A ⌈n/5⌉ floor would admit the observed 21%.
- It would be chosen after seeing the run-1 baseline, so it would be outcome-informed. And it would open only the one corner above.
- If N2 validation is resumed, the registered tree already names the better route: re-plant under a new registration.

## 2. Code (`residual/`, stdlib only, outside the frozen semantics hash)

- **`auroc.py`**
  - AUROC with midrank ties.
  - DeLong covariance. With registered clusters it uses the clustered form of Obuchowski (1997), which equals DeLong for singleton clusters. When either class sits in a single cluster it falls back to DeLong.
  - The paired ΔAUROC.
  - Common-effect pooling with golds as fixed strata, weighted by n1·n0.
  - Random effects as a sensitivity: DerSimonian–Laird τ² with modified Knapp–Hartung and Student t.
  - A cluster bootstrap that resamples whole clusters within each gold, stratified by cluster composition.
  - Tested against pROC 1.18.5's expected values on its aSAH data (`residual/tests/data/asah.json`). The wfns AUROC is 0.823678861788618, and the DeLong variances agree to a relative 10⁻⁹. The wfns − s100b test gives Z = 2.20898359144091 with 95% CI [0.0104, 0.1742].
- **`baselines.py`**
  - The ten baselines as typed, dated (2026-10-24) records.
  - K is DS3's: area size from the pre-gold partition, retrieval-support density, corpus term frequency, plain-LLM (spec only: prompt, other-family model, no call), the type prior (only once every gold has two others) and Jev/text-form.
  - Random and the naive type rule are `REPORTED`. Verbalised confidence is `SPEC_ONLY`. Gold items per area is `NEAR_ORACLE`.
  - The gate is `n3_reading`: Continue by intersection–union at c, Stop by Bonferroni over K. Reported only: `bootstrap_reading`, `bootstrap_min_reading`, `max_t_reading` (single step), `ms3_screen` and `ms5_reading`.
- **`reach.py`** enumerates the outcome spaces through an injected decision function, because `residual` must not import `reconstruct`. `reconstruct/tests/test_reach_n2.py` pins the §1 results against the real rules.
- **Tests:** on the merged tree (2026-10-24), residual 356, reconstruct 492 and gapmap 329 pass. `test_freeze` shows no drift, because no file in the semantics hash changed.

## 3. N3 simulation: model and pre-stated checks

**Model** (`simulate.py`, `grid.json`):
- **Areas and labels.** Areas sit in clusters of 4, registered in every cell. A latent liability ranks them, with a cluster share equal to the ICC, and the top n1 are labelled missed.
- **Scores.** Every score is μ·y plus unit-variance noise. The noise has a cluster part and an area part, each equicorrelated at r across the map and all baselines.
- **Baselines.** The strongest baseline (area size) has AUROC 0.62, and the other baselines in K have 0.60, within 0.02 of it (DS3's worst case). The map has AUROC 0.62 + gain.
- **Ties.** In a tied cell, 30% of the map's areas sit at a floor, with μ re-calibrated to keep the target AUROC. DS3's 50% is infeasible for a gain of 0.20 at 16/4: the AUROC cannot then exceed (40 + 12)/64 = 0.81.
- **Looks.** The primary set of k golds comes first. If it is inconclusive, one fallback gold of the same design is pooled in, once. At k = 2, the type prior enters K only at the second look. From k = 3 it is in both looks.
- **Grid.** k from 1 to 6; 15, 20 or 30 areas; missed share 0.3, 0.45, 0.5, 0.6, 0.75 or 0.8; ICC 0 or 0.3; ties 0 or 0.3; r of 0.3, 0.6 or 0.9; gain 0, 0.10 or 0.20.
- **Size.** 3,888 cells plus 690 L7.3 cells, at 1,000 replicates each. The Monte Carlo SE is at most 0.016.
- **Variance method.** The grid reads the gate with clustered-DeLong bounds. §5 checks them against the cluster bootstrap.

**L7.3 checks.** Rows 1 to 4 were stated before the grid ran. Rows 5 and 6 were added at review.

| Check | Pass mark | Result |
|---|---|---|
| 1. Best reachable: a perfect map, 3 × 20, 16/4 | P(Continue) ≥ 0.8 | **1.000** at ICC 0 and at ICC 0.3. Continue is reachable. |
| 2. Planted positive: gain 0.20 over every baseline, cells with a pooled minority class (k × min(n1, n0)) of at least 25 | P(Continue) ≥ 0.8 in every cell | **Fails in 70 of 552 cells** (minimum 0.532): 66 at r = 0.3 and 4 at r = 0.6 (0.788–0.799). Every cell passes once the minority class is at least 43 at r = 0.3, 29 at r = 0.6 and 10 at r = 0.9. The 744 cells below the floor range from 0.055 to 1.0. |
| 3. Stand-in: a random score | P(Continue) ≤ 0.05 | **0.008** at most, over 216 cells |
| 4. Stand-in: area size plus noise (correlation 0.9 with size) | ≤ 0.05 | **0.004** at most, over 216 cells |
| 5. Stand-in: the rank mean of the six baselines | ≤ 0.05 | **Fails at r = 0**, where the mean has AUROC 0.73 against 0.62: 0.152 at 5 × 30 (24/6), and 0.012–0.049 at the 20-area designs. 0.000 at r = 0.3 and r = 0.6, where the mean has AUROC 0.62–0.66. |
| 6. The least-favourable null at r = 0.3 and 0.9 (one baseline tied, the rest weak) | false Continue ≤ 0.05 | 0.045 and 0.033 (`null_one_strong_r.json`) |

Two of these checks pass for a weak reason, and one fails:
- **Stand-ins 3 and 4 pass by construction.** Their true gain is about −0.12 and −0.02, so they cannot pass a rule that needs a minimum point estimate of at least δ.
- **Stand-in 5 is the informative one.** The gate compares the map with each baseline singly, so a map that only averages weakly correlated baselines can beat each of them.
- **Fix for stand-in 5 (proposed):** add a pre-registered rank mean of K to K. It is fixed before gold and costs nothing to compute.

## 4. Decision frequencies at the set rules (δ = 0.10, c = 1.85, two looks)

All rows are ICC 0 / ICC 0.3 with no ties (`summary.json` `candidate_designs_16_4_or_24_6`). "Golds" counts the primary set; the fallback adds one more. "False S | δ" is P(Stop) when the true gain is exactly δ; its nominal bound is 1 − Φ(1.85) = 0.032.

| Design | Pooled minority | r | P(C \| 0.20) | P(S \| 0) | False S \| δ |
|---|---|---|---|---|---|
| 3 × 20, 16/4 | 12 | 0.3 | 0.354 / 0.368 | 0.317 / 0.332 | 0.073 / 0.067 |
| 3 × 20, 16/4 | 12 | 0.6 | **0.622 / 0.591** | 0.437 / 0.437 | 0.064 / 0.063 |
| 3 × 20, 16/4 | 12 | 0.9 | 0.975 / 0.968 | 0.758 / 0.727 | 0.061 / 0.052 |
| 5 × 20, 16/4 | 20 | 0.3 | 0.620 / 0.624 | 0.388 / 0.374 | 0.051 / 0.053 |
| 5 × 20, 16/4 | 20 | 0.6 | **0.855 / 0.848** | 0.470 / 0.480 | 0.052 / 0.035 |
| 5 × 20, 16/4 | 20 | 0.9 | 0.993 / 0.994 | 0.870 / 0.842 | 0.031 / 0.034 |
| 3 × 30, 24/6 | 18 | 0.6 | **0.892 / 0.856** | 0.509 / 0.482 | 0.044 / 0.043 |
| 5 × 30, 24/6 | 30 | 0.3 | **0.843 / 0.841** | 0.440 / 0.439 | 0.033 / 0.038 |
| 5 × 30, 24/6 | 30 | 0.6 | 0.971 / 0.968 | 0.613 / 0.602 | 0.022 / 0.025 |

**Compared with DS3** (3 × 20, ICC 0, r = 0.6), the readings are P(C | 0.20) / P(S | 0):

| Split | This grid | DS3 |
|---|---|---|
| balanced | 0.878 / 0.513 | 0.86 / 0.39 |
| 15/5 | 0.736 / 0.451 | |
| 16/4 | 0.622 / 0.437 | |

Stop is higher than in DS3 because the fallback look and the five close baselines each give the minimum upper bound more chances to fall below δ.

**Decisive Stop** (P ≥ 0.8) at 16/4, three golds and r = 0.6 needs about **80 areas per gold**. At that size P(S | 0) is 0.838 at ICC 0 and 0.818 at ICC 0.3, against 0.687 at 60 areas.

**Sensitivities** at 3 × 20, 16/4, ICC 0, r = 0.6:
- **δ.** At δ = 0.05, P(C | 0.20) is 0.626 and P(S | 0) is 0.177. At δ = 0.15, they are 0.495 and 0.707.
- **Ties.** 30% ties move P(C | 0.20) by at most 0.006.

**Secondary rows** (`tables.md`, same design):
- **MS3** releases a gain of 0.20 in 0.672 of runs, and a null map in 0.008.
- **MS5** (the unadjusted 1.645 boundary, one look) continues 0.513 of the time and stops 0.649 of the time.
- **Random-effects pooling** continues a gain of 0.20 in 0.059 of runs. It stays a sensitivity analysis only, as set.

**The minimum point estimate is biased low.** At a gain of 0.20, 20 areas, 16/4 and r = 0.6, the mean of min_k ΔAUROC falls 0.042–0.064 below the true gain at three to five golds (ICC 0 and 0.3), as DS3 §4 predicted. Over the full grid the shortfall at k = 3–5 runs from 0.006 to 0.103.

## 5. Multiplicity, c and the variance rule

**False Continue** (true gain 0) holds at c = 1.85:
- The maximum is 0.039 over the 216 least-favourable null cells at r = 0.6. It is 0.045 at r = 0.3 and 0.033 at r = 0.9.
- c = 1.645 would give 0.058.
- **Keep c = 1.85.** The clause "minimum point estimate ≥ δ" does most of this work.

**False Stop at a true gain of exactly δ is above its nominal 0.032 in small designs.**
- **Size.** Over cells with a pooled minority class of at least 25, the maximum is 0.070 and the median 0.029. With a minority class of at least 30, the mean is 0.028, the maximum 0.059, and 12 of 480 cells exceed 0.05. At one gold of 15 areas it reaches 0.27. The maxima sit about two or three Monte Carlo SEs high.
- **Causes.** There are two:
  - *The second look.* Look 1 alone has a maximum of 0.056 over the floor-25 cells; two looks have 0.070.
  - *The clustered variance, estimated from about five clusters per gold.* At ICC 0.3, the unclustered DeLong is lower in 96 of 108 cells: a maximum of 0.143 against 0.208 overall, and 0.046 against 0.058 in the floor cells. It is still above nominal at one gold.
- **What not to do.** A separate Stop boundary of 2.15 would hold the floor cells at 0.05, but it costs Stop power: P(S | 0) at 3 × 20 drops from 0.437 to 0.357.
- **Proposed instead:** meet the minimum design (§7), and make "at least 5 clusters per gold" a registered minimum. Then record the simulated two-look false Stop at the chosen design beside the nominal 0.032, for example 0.052 / 0.035 at 5 × 20, r = 0.6. A t reference on the cluster degrees of freedom is the cause-targeted fix, but it needs its own L7.3 run first.

**The bootstrap beside the gate** (`bootstrap.json`: 300 replicates, B = 2,000, both looks). The agreement rule is DS3 §2's: a reading counts only if the analytic and the bootstrap readings agree; otherwise it is inconclusive.

| Key cell | Analytic gate | Agreement rule | Cluster-bootstrap percentile | Bootstrap minimum | Max-T |
|---|---|---|---|---|---|
| 3 × 20, 16/4, ICC 0.3, gain 0.20: P(C) | 0.627 | 0.627 | 0.760 | 0.730 | 0.627 |
| same, gain δ: P(false S) | 0.073 | 0.067 | 0.137 | **0.413** | 0.163 |
| same, gain 0: P(S) | 0.437 | 0.430 | 0.617 | 0.913 | 0.620 |
| 3 × 20, balanced, ICC 0, gain δ: P(false S) | 0.050 | 0.050 | 0.093 | **0.377** | 0.067 |
| 5 × 20, 16/4, ICC 0, gain 0.20: P(C) | 0.833 | 0.833 | 0.883 | 0.870 | 0.833 |
| same, gain δ: P(false S) | 0.027 | 0.027 | 0.077 | **0.393** | 0.080 |

What the comparison shows:
- **The bootstrap minimum** stops maps that beat every baseline by δ 38–41% of the time (DS3 found 55% with eight baselines). It stays out of the gate.
- **The percentile bootstrap** has a false Stop of 0.08–0.14 in every tested design: balanced (minority 30), 16/4 with 3 golds (12) and 16/4 with 5 golds (20). It agrees with the analytic reading in 82–95% of replicates.
- **Under the agreement rule**, the conjunction matches the analytic gate to within 0.007 everywhere. So it adds protection at almost no cost.
- **Proposed:** the analytic clustered DeLong as primary, and the cluster bootstrap (B ≥ 2,000) as a co-gate under the agreement rule. This is DS3 §2's order. I5 step 1 had named the bootstrap as primary.

## 6. The near-oracle ruling

`near_oracle.json` models items per area as 1 + Poisson(1.3). An area is missed if any item is missed, at p = 0.56 per item, which gives 78–79% missed. The map is conditionally independent of the item count, and K is as in §3.
- Gold items per area has a mean AUROC of 0.74, as in DS3 §7.
- With it in K, a truly informative map continues far less often. For a map of AUROC 0.82 (a gain of 0.20 over K):

  | Design | Item count in K | Item count not in K |
  |---|---|---|
  | 3 × 20 | 0.186 | 0.632 |
  | 3 × 30 | 0.29 | 0.895 |
  | 5 × 20 | 0.255 | 0.847 |

- At 3 × 20, a map needs AUROC 0.92 to continue 0.751 of the time with the item count in K.
- These figures assume a map unrelated to item count given the label. A map that tracks item count would lose less.

**Ruling: exclude gold items per area from K.** Two follow-ups:
- Keep DS3 §7's AUROC within item-count strata as a reported secondary analysis.
- A pre-gold size proxy correlated 0.6 with item count (AUROC 0.64) costs less: P(C) is 0.381 against 0.632 at 3 × 20. Whether K's own area-size baseline behaves like that proxy is not shown here, because in the grid area size is a binormal score unrelated to items.

## 7. Recommendation for the §22 rows

1. **δ = 0.10, as set.**
2. **The minimum design, keyed to r.** Before gold, measure r, the correlation between the map's scores and each K baseline's scores on the pre-gold partition. This needs no participants and no gold. Then register the minimum by the smallest correlation found, r_min:
   - **r_min ≥ 0.6:** at least 5 primary golds of 20 areas (P(C | 0.20) = 0.855 / 0.848), or 3 of 30 (0.892 / 0.856).
   - **0.3 ≤ r_min < 0.6:** at least 5 golds of 30 (0.843 / 0.841).
   - **Lower:** E-CTA reads inconclusive by design.

   In every case, add at least 5 clusters per gold and one fallback gold.

   The pooled-minority floor does not work as a single number, for three reasons:
   - It must be 43 at r = 0.3 but only 10 at r = 0.9.
   - 3 × 30 passes at r = 0.6 with a minority class of 18.
   - DS1's three provisional primary golds are short of every r ≥ 0.6 design except 3 × 30, so either the partitions reach 30 areas or two fallback golds join the primary set.
3. **K:** add the pre-registered rank mean of K (stand-in 5), and exclude gold items per area (§6).
4. **Multiplicity:** intersection–union and Bonferroni, as set, with c = 1.85 for both. No separate Stop boundary.
5. **Variance:** the analytic clustered DeLong as primary, with the cluster bootstrap (B ≥ 2,000) under the agreement rule.
6. **What E-CTA can do.** At the minimum designs of item 2 (r_min from 0.3 up), E-CTA stops a null map 44–61% of the time, so it can falsify H1 but not decisively; at 3 × 20 and r = 0.3 it stops only 32–33% of the time. At r = 0.9 it can, with 5 golds of 20 (0.84–0.87) or 3 of 30 (0.88–0.89), but not with 3 of 20 (0.73–0.76). E-OSS's §22 row still says "to set by power calculation"; DS8's first SYNTHETIC estimate is in `research/ds8-oss-departures.md` §5.

## Limits

These simplifications each push P(Continue) up and the error rates down, so the golds proposal is optimistic:
- equal gold sizes and a fixed class split, where DS3 §9.1–9.2 expect unequal golds and a split that varies by gold;
- no between-gold heterogeneity (τ = 0);
- no pseudo-areas for unmappable items. With unmappable items at 30% of missed areas, a gain of 0.20 shrinks to about 0.15 (DS3 §5's dilution, inferred);
- no memorisation exclusions;
- one r shared by all baselines. Intersection–union is bound by the least-correlated close baseline, so mixed correlations need the per-baseline r_min rule above.

Other limits:
- The scores are binormal; real size and density baselines may be skewed or discrete.
- The bootstrap comparison covers six cells at 300 replicates (MC SE about 0.03).
- The near-oracle item model is DS3 §7's, itself an analogy from expert recall [inferred].
