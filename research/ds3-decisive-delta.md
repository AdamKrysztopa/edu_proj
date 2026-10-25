# DS3: Can N3 give a decisive reading at a meaningful δ?

**Result** [SYNTHETIC planning figures, independent areas]. Only in one direction. If 3–6 golds of 15–25 areas each prove eligible, they would give 45–150 areas (`17_validation.tex:149,245,268`). No gold is confirmed eligible yet (DS1, `research/ds1-gold-availability.md`): Sullivan's list is itemised, but whether the full list is obtainable is unconfirmed. That many areas is enough for N3 to **Continue** a map with a large gain, but not enough to **Stop** a map with no gain at any δ ≤ 0.10. At δ = 0.05, a decisive Stop with probability 0.8 needs about 384 areas per class. At δ = 0.10 it needs about 97 per class, and at δ = 0.15 about 44. At δ = 0.10, pooled over three golds of 20 balanced areas, N3 continues a true gain of 0.20 with probability 0.86 and stops a true gain of 0 with probability 0.39. The rest of the time it reads inconclusive. The proposed values are in the table below. The main changes from the report are three:
- Raise δ from 0.05 to **0.10**.
- Read the strongest-baseline comparison as an **intersection–union test**, not as a minimum taken inside each bootstrap resample. With 8 equally close baselines, the bootstrap minimum stopped 55% of maps that truly beat every baseline by δ.
- Drop **gold items per area** from the set of competing baselines, because it is a near-oracle.

**Decision it feeds.** It feeds I5's simulation inputs (§9) and the §22 threshold-table rows for δ, the multiplicity rule, the minimum number of areas and golds, the fallback golds and the floor for unmappable items. These are proposals. The owner sets the rows through `methods-critic`, and nothing here is registered.

**Method.** The literature comes from OpenAlex, with abstracts read through PubMed or OpenAlex. "Abstract" means only the abstract was read. The planning computations are first-order and assume independent areas. They are **SYNTHETIC** (simulations from a specification). They inform the design and never feed a gate. Each operating characteristic uses the Hanley–McNeil variance at the true AUROCs of its scenario: both at 0.62 under the null, and 0.62 + Δ against 0.62 under a gain Δ. Using 0.70 against 0.62 throughout gives about 5–10% fewer areas (for example 360 instead of 384). The scripts are scratch files and deliberately not committed, because the code belongs to I5: `ds3_calc.py` (sha256 `2a7ebd5e…bee20`) and `ds3_calc2.py` (sha256 `2573056f…56779`). The planning figures follow the report: Hanley–McNeil errors, AUROC 0.70 against 0.62, and a correlation of 0.5 between the two AUROC estimates. Ties count ½. One-sided bounds are at 5% (the 90% intervals of §22).

## Proposed values

| Row | Proposed value | Source of the value |
|---|---|---|
| δ | **0.10** AUROC | Two radiology non-inferiority margins (0.05, 0.10) as a scale reference, plus the top-k anchor and the reachability arithmetic in §1 |
| Test | Paired Mann–Whitney ΔAUROC with pairs formed only within a gold. DeLong variance summed over golds, using Obuchowski's clustered form when a cluster level is registered. A gold-stratified bootstrap is the sensitivity analysis. The gate reads Stop or Continue only when both agree; otherwise it reads inconclusive | §2 |
| Pooling | Common effect across golds, with golds as fixed strata. Inference is limited to these golds. Random-effects models (modified Hartung–Knapp, and Bayesian with a half-normal τ prior) are sensitivity analyses only | §3 |
| Minimum areas per gold | **20** in the pre-gold partition. Unmappable pseudo-areas do not count | §1, §2 |
| Minimum pooled minority class | **25** real areas. Below that, the reading is inconclusive by design | §2 |
| Minimum golds | **3** for a gate reading; 4–6 is the aim | §1, §3 |
| Multiplicity across golds | **Pooled**, not Holm per gold | §3 |
| Multiplicity across baselines | Continue by **intersection–union test** (no adjustment); Stop by **Bonferroni** upper bounds (one-sided α/K) | §4 |
| Multiplicity across looks | The same boundary **c = 1.85** at both looks: the pooled primary set, then one fallback gold pooled in | §6 |
| Fallback order | Golds in the report's eligibility order, filtered by DS1. The primary is the pooled set of all golds eligible at MS2; the fallback is the next eligible gold not in that set | §6 |
| Unmappable floor | One pseudo-area per unmappable gold item, labelled missed, scored at a **strict floor below every real score in every arm** | §5 |
| Competing baselines (K) | Area size measured in the pre-gold partition, retrieval-support density, corpus term frequency, plain-LLM ranking, the cross-gold type prior when ≥ 2 other golds exist, and Jev/text-form. Random and the naive type rule are reported but are not candidates for "strongest" | §4, §7 |

## 1. δ: precedents, and what N3 can reach

**Where 0.05 comes from.** In this repo, δ = 0.05 first appears as a recommendation in `report/notes/07_validation.md:119-122`. Its reason is a judgement: "a gain smaller than 0.05 over the density and area-size baselines is unlikely to justify running the reconstruction pipeline at all". It cites no source and no data. The report calls it "a provisional program decision threshold … not a value derived from theory or data" (`report/sections/17_validation.tex:137-139`). `REORIENTATION.md` §22 leaves it "to set". The independent review flagged that it is not derived (`report/REVIEW_FIXES.md:27`). [inferred]

**Literature.** No field-wide smallest effect of interest for ΔAUROC was found, and no survey of margins was done. Two radiology reader studies used non-inferiority margins of 0.05 and 0.10 without deriving them. A non-inferiority margin is a tolerable *loss* of accuracy, not a smallest *gain* worth paying for, so these serve here only as a scale reference [inferred]:
- Kim et al. (2018) analysed clustered CT-urography reads "on the basis of a noninferiority margin of 0.05" (abstract). https://doi.org/10.2214/AJR.17.19370
- Cole et al. (2012) tested photon-counting against conventional digital mammography with "a noninferiority margin Δ value of 0.10" (abstract). https://doi.org/10.1016/j.acra.2012.03.005
- Neither abstract derives its margin. Ahn, Park & Lee (2013) say a margin "should be justified both clinically and statistically" (abstract). https://doi.org/10.1148/radiol.12120725
- In 273 randomized double-blind non-inferiority trials, margins whose method of definition was unreported were similar in number to those whose method was reported (ratio 1.35, not significant; Althunian et al. 2017, abstract). https://doi.org/10.1186/s13063-017-1859-x
- Accepted risk factors such as lipids, hypertension and smoking "have only marginal impact on the c statistic individually" (Cook 2007, abstract; https://doi.org/10.1161/CIRCULATIONAHA.106.672402). Pencina et al. (2008) proposed reclassification measures in response (https://doi.org/10.1002/sim.2929). Whether this insensitivity lies in the measure or in invalid tests is disputed (Pepe et al. 2013, abstract; https://doi.org/10.1002/sim.5727).
- Lakens, Scheel & Isager (2018) set out approaches to justifying a SESOI (https://doi.org/10.1177/2515245918770963). Lakens (2022) lists resource constraints among six approaches to justifying a sample size, and advises considering which effect sizes the data could reject (abstract). https://doi.org/10.1525/collabra.33267

**A substantive anchor** [SYNTHETIC, binormal, prevalence 0.5]. When the top 30% of areas are probed, precision tracks AUROC almost one for one. It is 0.603, 0.655, 0.707, 0.760 and 0.814 at AUROC 0.60, 0.65, 0.70, 0.75 and 0.80. So δ = 0.10 means about one more residual-bearing area per ten probed, and δ = 0.05 about half of one. This connects δ to the "gold-residual hits per question" score in §14.3.

**Reachability** [SYNTHETIC, independent areas]. Hanley–McNeil 90% half-widths of ΔAUROC are ±0.204, ±0.142, ±0.100, ±0.081, ±0.063 and ±0.051 at 10, 20, 40, 60, 100 and 150 areas per class. These reproduce `17_validation.tex:143-146`. Imbalance widens them: at 80 areas, a 20/60 split gives ±0.121 and 12/68 gives ±0.150.

Under the N3 rule (Stop if the upper bound < δ; Continue if the lower bound > 0 and the point estimate ≥ δ):

- **False Continue is at most 0.05 at every n.** At a true gain of exactly δ, Continue is at most 0.50, because it needs the point estimate to reach δ.
- **Areas per class for P(Stop | true 0) ≥ 0.8:** 384 at δ = 0.05, 171 at 0.075, 97 at 0.10 and 44 at 0.15.
- **Areas per class for P(Continue | true 2δ) ≥ 0.8:** 89, 38, 21 and 9 for the same δ values.
- **Pooled golds of 20 areas, balanced** (P(Stop | true 0) / P(Continue | true 2δ)):

  | Golds | δ = 0.05 | δ = 0.10 | δ = 0.15 |
  |---|---|---|---|
  | 3 | 0.17 / 0.39 | 0.39 / 0.86 | 0.65 / 0.98 |
  | 4 | 0.19 / 0.47 | 0.47 / 0.93 | 0.76 / 0.99 |
  | 6 | 0.25 / 0.61 | 0.61 / 0.97 | 0.89 / 1.00 |

  A 15/5 split per gold lowers each cell by about 0.03–0.08.

**Why 0.10 and not 0.05.** At 0.05, the Stop rule is decorative for E-CTA: it fires on a null map at most a quarter of the time, even with six golds. That is the "best reachable outcome" failure that L7.3 forbids. At 0.10, Stop is reachable but not reliable, and Continue is reliable for large gains. The cost is that the rule can stop a real but modest gain: with a true gain of 0.05, P(Stop) is 0.17 with three golds and 0.19 with four. That is the objection recorded at `07_validation.md:121-122`, now quantified.

**What would change it.** E-COST evidence that a 0.05 gain pays for the pipeline would argue for 0.05, but then the decisive test must move to E-OSS-scale samples of hundreds of code units, not CTA golds. Evidence that experts' time is cheap would argue for 0.15.

## 2. The test: paired, clustered, tied and imbalanced

**DeLong.** DeLong, DeLong & Clarke-Pearson (1988) give a nonparametric covariance for correlated AUROCs computed on the same cases, from generalized U-statistics (abstract). https://doi.org/10.2307/2531595 It handles ties through the ½ kernel and needs no binormal assumption. It breaks down in three ways:
- **Clustering.** Tests that assume independence have inflated size under intracluster correlation (Obuchowski 1997, abstract). https://doi.org/10.2307/2533958
- **Nested models.** When a predictor is added to a model fitted on the same data, the DeLong null distribution is non-normal and the test is conservative (Demler, Pencina & D'Agostino 2012, abstract; https://doi.org/10.1002/sim.5328). Tests of ΔAUC that ignore estimated coefficients are "extremely conservative" (Pepe et al. 2013, abstract; https://doi.org/10.1002/sim.5727). This affects only the report's secondary logistic analysis, which nests density and area size (`17_validation.tex:97-99`). It does not affect the primary comparison of separately built scores. [inferred]
- **Small n.** For the *difference* of two AUROCs, asymptotic intervals had adequate coverage "even when the sample size was very small (20 patients)". A single AUROC needed far more (Obuchowski & Lieber 1998, abstract). https://doi.org/10.1016/s1076-6332(98)80208-0

**Ties and imbalance** [SYNTHETIC; 3,000 replications each; half the map's areas tied at its minimum; nominal coverage 0.90]. The DeLong coverage of ΔAUROC was:
- 0.905 at 10/10 and 0.889 at 12/8;
- 0.881 at 17/8 and at 22/8;
- 0.867 at 14/6, 0.855 at 15/5 and 0.846 at 20/5;
- 0.843 at 16/4.

So ties at this level do not break DeLong, but a minority class under about 8 per gold does. Each one-sided tail rises from 5% to about 8%. Imbalance is likely. If the reconstruction's per-item miss rate were near the 56% of steps that Sullivan's three experts left out in unprompted recall (`REORIENTATION.md` §8.1), about 79% of areas would be labelled missed, given a "missed" label over about 2.3 items per area (§7). That is an analogy from expert recall to reconstruction recall, with n = 3 experts [inferred]. It is the reason for the pooled minority-class floor of 25.

**Obuchowski's clustered method** extends DeLong's structural components with a design effect and an effective sample size (Obuchowski 1997, abstract). It needs a registered cluster level inside each gold, such as areas that share a gold section or a source. It is asymptotic in the number of clusters, so with a handful of clusters per gold it only approximates. [inferred]

**Cluster bootstrap.** With clustered multisite data, analytic and bootstrap coverage was similar. Bootstrap was slightly better with many sites per patient, and percentile intervals beat normal bootstrap intervals (Rutter 2000, abstract). https://doi.org/10.1016/s1076-6332(00)80381-5 With tiny minority classes, an unstratified resample can contain no negatives. So the resampling is stratified by gold and class. [inferred]

**Proposal.**
- Primary: DeLong (Obuchowski form if a cluster level is registered), pairs formed only within a gold, variance summed over golds.
- Sensitivity: a gold- and class-stratified percentile bootstrap, B ≥ 2,000.
- Agreement rule: a Stop or Continue counts only if both methods give it; otherwise the reading is inconclusive.
- The rule that a map with "more than half its areas tied at zero" is uninformative (`17_validation.tex:89-90`) stays.

## 3. Pooling 2–5 golds

**What the literature says.**
- In simulations of 2–20 trials, DerSimonian–Laird type I error rates "could be over 30%", worst with unequal sizes and heterogeneity. HKSJ "at most doubled" the nominal 5% (IntHout, Ioannidis & Borm 2014, abstract). https://doi.org/10.1186/1471-2288-14-25
- HKSJ exceeds nominal error when study precisions vary. The modified version (mKH) is "recommended, especially when only a few studies contribute" (Röver, Knapp & Friede 2015, abstract). https://doi.org/10.1186/s12874-015-0091-1
- Hartung–Knapp coverage is "slightly too low when the heterogeneity is low (I² < 30%) and the study sizes are quite varied" (Partlett & Riley 2017, abstract). https://doi.org/10.1002/sim.7140
- With 2–4 studies, heterogeneity "cannot be reliably estimated", and Knapp–Hartung "has very low power" (Bender et al. 2018, abstract). https://doi.org/10.1002/jrsm.1297
- Bayesian intervals with weakly informative half-normal priors on τ were conservative but shorter than Knapp–Hartung (Friede et al. 2017, abstract). https://doi.org/10.1002/jrsm.1217
- Paule–Mandel or REML is the τ² estimator to use, with Q-profile intervals (Veroniki et al. 2016, abstract). https://doi.org/10.1002/jrsm.1164
- Inference on the mean of a random-effects distribution is not inference on the whole distribution, which needs prediction intervals (Higgins, Thompson & Spiegelhalter 2009, abstract). https://doi.org/10.1111/j.1467-985x.2008.00552.x

**Computed here** [SYNTHETIC, per-gold SE 0.10]. With k golds, the HKSJ one-sided 95% t-quantile is 6.31, 2.92, 2.35 and 2.13 for k = 2, 3, 4 and 5. That is 3.84, 1.78, 1.43 and 1.30 times the normal 1.645. The DerSimonian–Laird τ̂² was exactly 0:
- with k = 2: in 68%, 63% and 52% of replications at true τ = 0, 0.05 and 0.10;
- with k = 5: in 59%, 47% and 28%.

**Proposal.** Pool golds as fixed strata, which gives a common-effect ΔAUROC. It is the area-weighted mean of the within-gold ΔAUROCs, with each gold weighted by n₁·n₀. The conclusion is scoped to these golds, which `17_validation.tex:264-266` already states. Report τ² with its Q-profile interval, mKH and a half-normal Bayesian model as sensitivity analyses when k ≥ 3. None of them gates. This settles the threshold-table option "Holm correction, or pooled random-effects" in favour of **pooled common-effect**. Holm per gold would test single golds of 20 areas, each of which is about ±0.20 wide.

## 4. The strongest baseline: what choosing the maximum does

The report proposes choosing the strongest baseline inside each bootstrap resample, as min_k ΔAUROC_k (`17_validation.tex:127-129`). The minimum of several estimates is a non-differentiable functional:
- For φ(θ̂) with a Gaussian limit, "(full) differentiability of φ is a necessary and sufficient condition for bootstrap consistency" (Fang & Santos 2019, abstract). https://doi.org/10.1093/restud/rdy049
- No locally asymptotically unbiased estimator exists for such targets (Hirano & Porter 2012, "Impossibility Results for Nondifferentiable Functionals", abstract). https://doi.org/10.3982/ECTA8681

The bias bites hardest when several baselines are close to the strongest. [inferred]

**Computed here** [SYNTHETIC; 40 areas per class; K = 8 baselines; latent pairwise correlation 0.5; δ = 0.10; 300 replications, so MC SE ≈ 0.01 near 0.05 and ≈ 0.03 near 0.5; bootstrap B = 200].

| Scenario | False Continue: IUT | False Continue: bootstrap-min | False Stop: unadjusted min of upper bounds | False Stop: Bonferroni | False Stop: bootstrap-min | Bias of the minimum point estimate |
|---|---|---|---|---|---|---|
| All 8 baselines tied with the map (true gain 0) | 0.000 | 0.000 | correct to stop | correct to stop | correct to stop | −0.059 |
| One tied, seven weak (true gain 0) | 0.050 | 0.043 | correct to stop | correct to stop | correct to stop | −0.003 |
| Map beats all 8 by exactly δ | n/a | n/a | 0.207 | **0.033** | **0.553** | −0.063 |
| Map beats one by δ, the rest weak | n/a | n/a | 0.050 | 0.007 | 0.147 | −0.016 |

(In the two true-gain-0 rows, stopping is the right outcome, so false Stop does not apply. In the two true-gain-δ rows, continuing is not an error, so false Continue does not apply.)

**Reading.** Continue should be an **intersection–union test**: every pairwise lower bound must exceed 0, and the minimum point estimate must reach δ. Testing "each parameter individually" and accepting only if each passes attains exactly the prespecified error, with no multiplicity adjustment (Berger 1982, abstract; https://doi.org/10.1080/00401706.1982.10487790; also Berger & Hsu 1996 https://doi.org/10.1214/ss/1032280304). Stop is a union claim ("some baseline is within δ"), so its upper bounds need a family-wise adjustment. Bonferroni held false Stop at or below 0.05. A resampling max-T or stepdown bound (Romano & Wolf 2005, abstract; https://doi.org/10.1198/016214504000000539) should be tighter, and I5 should compare it. The bootstrap minimum stops a map that truly beats every baseline by δ more than half the time when the baselines are close together. It should not be the gate statistic. The minimum point estimate is biased downward by up to 0.06, which makes Continue harder. That is acceptable as conservatism, but I5 should report it. "Best of many against a benchmark" is White's (2000) data-snooping problem (abstract, https://doi.org/10.1111/1468-0262.00152). Here the direction is reversed, "the map against the best of many", so the intersection–union test applies, not White's reality check. [inferred]

**Keep K small.** At one-sided α = 0.05, the Bonferroni z is 2.24 at K = 4 and 2.39 at K = 6, against 1.645. Random (expected AUROC 0.5) and the naive type rule (nearly constant on Sullivan, per §14.3) can be strongest only if the map is near or below chance. They are reported, but they are not in the minimum. [inferred]

## 5. Unmappable gold items

`REORIENTATION.md` §14.3 already requires counting gold items that map to no area "as missed areas at a pre-registered floor score". There are three precedents for scoring an unscorable positive at the worst value:
- **Information retrieval.** "When a relevant document is not retrieved at all, the precision value … is taken to be 0" (Manning, Raghavan & Schütze 2008, *Introduction to Information Retrieval*, §8.4, online edition). https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html
- **Free-response ROC.** "Unmarked lesions are assigned negative infinity ratings and are observable events" (Chakraborty, *The RJafroc Book*, ch. 25 "Empirical plots", §25.4.1, online). https://dpc10ster.github.io/RJafrocBook/froc-empirical.html In that paradigm a non-diseased case with no mark also sits at −∞, so ties at the floor earn ½. That has no analogue here, because every real area receives a score. [inferred]
- **Diagnostic accuracy.** An intention-to-diagnose 3 × 2 table keeps non-evaluable results instead of dropping them. In 26 coronary-CT studies this lowered pooled sensitivity from 98.2% to 92.7% and AUC from 0.99 to 0.93 (Schuetz, Schlattmann & Dewey 2012, abstract; https://doi.org/10.1136/bmj.e6717). Shinkins et al. (2013) give reporting guidance for inconclusive results (abstract; https://doi.org/10.1136/bmj.f2778).

**Computed here** [SYNTHETIC]. With u pseudo-areas at a floor strictly below every real score in every arm, ΔAUROC becomes exactly (n₁ʳ / (n₁ʳ + u)) × ΔAUROC on the real areas. At n₁ʳ = 15 it shrinks 0.267 → 0.222 → 0.200 → 0.160 at u = 0, 3, 5 and 10. The pseudo-areas dilute any real gain and can never create one. The alternative, flooring each arm at its *own* minimum, is asymmetric. In the test case, a map with 8 areas tied at its minimum scored 0.222 against 0.180 under the strict floor at u = 5, because ties earn ½. That rewards a map for having many uninformative areas.

**Proposal.**
- Create one pseudo-area per unmappable item, labelled missed, at the strict floor, in every arm alike. The arms then differ only in their scores on real areas (L7.4).
- Coders map items to areas blind to every score.
- Pseudo-areas are excluded from the minimum-area counts.
- Report ΔAUROC with and without them.
- If pseudo-areas exceed 25% of the missed areas, report it as a partition-coverage finding. The gate is unchanged. [our choice]

## 6. Fallback golds and the looks

**The fallback order** is the report's eligibility order (`17_validation.tex:239-244`), filtered by DS1's availability register (DS1's own output, not yet on `main`):
1. Sullivan's cricothyrotomy task list, itemised, but not yet confirmed obtainable (DS1);
2. the Crandall NICU cue study;
3. Chao & Salvendy's troubleshooting study;
4. the PARI worked analyses;
5. the review-listed studies.

One gold of about 20 areas is about ±0.20 wide and cannot reach a decision (§1). So the *primary* reading should be the pooled set of every gold eligible at MS2, and the fallback is the next eligible gold not in that set. If no further gold exists, inconclusive is final for E-CTA, and E-OSS carries the decision.

**Looks.** Adding data after an inconclusive look is a sequential design. In IR evaluation, adding topics until power is reached "leads to a bias in favour of finding both power and significance" (Webber, Moffat & Zobel 2008, abstract; https://doi.org/10.1145/1458082.1458158). Topic-set-size design instead fixes the number of topics in advance, from stated statistical requirements and the within-system variance (Sakai 2016, abstract; https://doi.org/10.1007/s10791-015-9273-z), and small topic sets give "larger than anticipated" error rates (Voorhees & Buckley 2002, abstract; https://doi.org/10.1145/564376.564432).

**Computed here** [SYNTHETIC; primary set of about 80 areas, then one 20-area fallback pooled in]. With the 1.645 boundary at both looks:
- false Continue (true 0) is 0.061–0.069, and false Stop (true δ) is 0.068;
- reading the fallback alone instead of pooling gives 0.074–0.091.

A common boundary of **c = 1.85** holds both at 0.045. At δ = 0.10, P(Continue | true 0.20) is 0.963, against 0.970 at 1.645. So the adjustment costs almost no power. I5 should re-derive c under its own assumptions.

## 7. Baselines that can be specified before gold

**Can be specified and computed before gold:**
- random, with a registered seed;
- the naive type rule, which needs type tags on the pre-gold partition;
- verbalised confidence;
- **area size measured in the pre-gold partition** (for example, sub-steps or tokens per area);
- retrieval-support density;
- corpus term frequency;
- a plain-LLM ranking, with a frozen prompt and a model from another family;
- the text-form and Jev baselines added after the Jev spike (`17_validation.tex:254-257`).

**Can be specified before gold but computed only from other golds:** the type prior, fitted leave-one-gold-out. With one gold it does not exist. With two golds it rests on a single other gold. Coverage-audit finding 20 already notes the timing mismatch with the fallback rule (`docs/plans/coverage-audit.md:112`, in the main checkout and not yet committed).

**Gold items per area** can be specified, but it is computed from the target gold, so it is a near-oracle. When an area is "missed" if any of its n items is missed, P(missed) = 1 − (1 − p)ⁿ rises with n by arithmetic alone.

**Computed here** [SYNTHETIC; 20 areas; 1 + Poisson(1.3) items per area, mean about 2.3, chosen to match a 46-item list over 20 areas]. The AUROC of the item count is shown at each per-item miss rate p:

| Per-item miss rate p | Share of areas missed | AUROC of the item count |
|---|---|---|
| 0.10 | 0.21 | 0.64 |
| 0.30 | 0.53 | 0.69 |
| 0.56 (analogy: Sullivan's experts omitted 56% unprompted) | 0.79 | 0.74 |
| 0.70 | 0.88 | 0.79 |

At p = 0.56, a Continue at δ = 0.10 would need a map with an AUROC of at least about 0.84 against a label it does not see. That is close to the "Continue unreachable" pattern that L7.3 warns about.

**Proposal.**
- Drop gold items per area from the strongest set.
- Use area size measured in the pre-gold partition as the size baseline.
- Use gold items per area only as a conditioning variable: AUROC within item-count strata, pooled the same way as the density-tertile analysis (`17_validation.tex:95-99`).
- Size baselines are strong in a neighbouring field. Mende & Koschke (2010) report their earlier finding that a classifier ordering files "just by their size" performs "surprisingly good" in defect prediction when effort is ignored (abstract; https://doi.org/10.1109/CSMR.2010.18). So the pre-gold size baseline stays in the minimum. [inferred]

## 8. Points that change the report's text

- **Bootstrap minimum of baselines.** `17_validation.tex:127-129` (min_k inside each resample) should become the intersection–union and Bonferroni rule (§4).
- **δ = 0.05.** The value in `17_validation.tex:137`, `00_executive_summary.tex:102`, `02_question.tex:61` and `23_workpackages.tex:40` is still provisional. This note proposes 0.10 (§1).
- **Gold items per area.** "Area size or gold items per area" in `REORIENTATION.md` §14.3 should become "area size from the pre-gold partition" (§7).

None of these is edited here. They are the owner's choice through `methods-critic`.

## 9. Assumptions I5 must simulate

1. **Areas per gold and number of golds.** 15–25 areas per gold, unequal across golds; 2–6 golds.
2. **Class balance.** The prevalence of missed areas runs from 0.2 to 0.9, and follows from the per-item miss rate (0.1–0.7) and the item counts per area. The "residual-present" label of `17_validation.tex:250-253` is rarer than "missed".
3. **Map ties.** At least 50% of areas tied at the floor, with the >50% uninformative rule applied.
4. **Score correlation.** Correlation between the map and baseline scores from 0.3 to 0.7. Baseline AUROCs spread so that several baselines lie within 0.02 of the strongest, which is the worst case in §4.
5. **Number of baselines.** K = 4–7, and the IUT, Bonferroni, max-T and bootstrap-minimum rules side by side.
6. **Clustering.** Within-gold clustering of areas that share a gold section or source, with ICC 0–0.3. DeLong, the Obuchowski form and the stratified bootstrap compared.
7. **Heterogeneity.** Between-gold τ from 0 to 0.10, with common-effect pooling against mKH and Bayesian half-normal models.
8. **Unmappable items.** 0–30% of missed areas, at the strict floor.
9. **Density confounding.** The map score correlated with density at ρ ≈ 0.8–0.9, and the conditional AUROC within tertiles. The within-HYP figures are about 0.83 on PLC and 0.87 on GDPR v2. The pooled PLC ρ of 0.91 is inflated by non-HYP records pinned at −1 (coverage-audit finding 19, `docs/plans/coverage-audit.md:106-111`). These are record-level, not area-level, figures.
10. **Looks.** The two-look procedure, with c re-derived.
11. **Memorisation probes.** Exclusions that shrink the areas per gold (`17_validation.tex:111-113`).
12. **Reported outputs.** The best reachable outcome of each rule from the observed baseline, a planted positive that must fire, and a trivial stand-in (area size alone, or a length statistic) that must not pass (L7.3).
