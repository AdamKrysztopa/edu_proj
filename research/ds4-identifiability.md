# DS4: Identifiability of the residual under zero text catchability

**Result.** The human residual cannot be identified from text occasions. This is an impossibility result, not a power problem. An item with zero catchability on every text occasion contributes nothing to the distribution of the observed capture histories. So two universes that differ only in how many never-written items they hold produce the same data, and every text-only estimator returns the same value for both (§1). Even the *written* universe has only a lower bound without a parametric assumption: confidence intervals are one-sided for the number of classes (Mao & Lindsay 2007, Theorem 3.4), they claim the same for population size (Mao & Lindsay 2007, their §7), and reasonable heterogeneity models fit equally well yet disagree on N (Link 2003). What text occasions can identify NOW is a **lower bound on the number of written items no text occasion caught**. The residual becomes estimable only with an occasion that can catch never-written items, which here is the gold. Even then it rests on one assumption the data cannot test: the gold's catchability must not depend on text catchability (§3).

**A defect this finding exposes in the N5 rule.** As written, N5's continue rule (`REORIENTATION.md` §22, N5 row) and R4's trigger (§16) compare the text estimate of unseen items with the count from the gold-as-occasion. These two numbers estimate different things. The text estimate targets at most the unseen *written* items. The gold count targets unseen written items plus never-written items. Even with perfect estimators, the relative gap is the never-written share of everything unseen. So the rule passes at tolerance τ only when that share is at most τ (§3.3). It stops the residual objective exactly when the residual is large, the case the objective exists to measure.

**Decision it feeds.**
- **I3's grid and estimand.** §7 gives both. It keeps I3's default axes, adds the axes this note shows are decisive, and changes the comparison target in I3 step 4.
- **R4 to the owner before any gold.** Identifiability fails in principle for text occasions, so the DS4 item routes R4 to the owner together with I3's result. The question is stated in §6.

**Method.**
- Primary sources were found through OpenAlex.
- Mao & Lindsay (2007, via arXiv:0708.2153) and van Rijnsoever (2017) were read in full. For every other source only the abstract was read, marked "(abstract)".
- Chao (1984) and Chapman (1951) were not read. They are cited only for the estimator formulas they introduced. Chapman (1951) is not indexed in OpenAlex or Crossref.
- Claims derived here rather than taken from a source are labelled **inferred**. A small seeded simulation checks them (appendix). It is labelled **SYNTHETIC** and is a debugging aid only. It never feeds a gate.

## 1. What can any capture–recapture estimator identify under zero catchability?

**Setting.** The universe is U = W ∪ Z.
- W holds the written items. Each item i has text catchabilities p_ij > 0 on at least one of the k text occasions.
- Z holds the never-written items, with p_ij = 0 on every text occasion.
- The data are the capture histories of the S_obs items caught at least once, summarised for an Mh model by the capture frequencies f_1 … f_k. Burnham & Overton (1978, abstract) show these frequencies are a sufficient statistic when catchabilities vary by individual.

**Zero mass is not identifiable (literature-supported, and immediate).** The probability of any observed history is a function of W's catchabilities alone. An item in Z has the all-zero history with probability 1 and never enters the observed table. Mao & Lindsay (2007) state it directly for the mixture formulation: "the mass of Q at zero is nonidentifiable and mass near zero is nearly undetectable" (§3, before Lemma 3.1). Q is the mixing distribution reweighted by detection probability (eq. 2.1), so "Q has no mass on zero" (§2): zero-rate classes leave no trace. **Inferred:** the Mh estimators below can therefore estimate only the catchable population.

**The near-zero tail makes even the catchable count unbounded above (literature-supported for the number of classes; claimed for population size).**
- Mao & Lindsay (2007) prove that the odds that a class is undetected are Hellinger-discontinuous (Lemma 3.1). No locally unbiased, informative estimator exists, and if a confidence interval has a finite upper limit with probability one somewhere in the model, its coverage is zero somewhere in the model (Theorem 3.4). These results are proved for the Poisson-mixture number of classes.
- They state without proof (their §7) that the same holds for population size under partial sampling: "confidence intervals for the population size must be one-sided, but identifiable lower bounds to the population size exist".
- Link (2003, abstract): reasonable heterogeneity models "may predict essentially identical observations from populations of substantially different sizes … even with very large samples".
- Holzmann, Munk & Zucchini (2006, abstract) restore identifiability only *within* chosen parametric families of mixing distributions, such as finite and beta mixtures.
- Dorazio & Royle (2003, abstract) find abundance and richness estimates "sensitive to model-specific assumptions about the latent distribution". Deviance cannot pick the family that gives valid inference.

**Answer to Q1.**
- Text occasions identify nothing about |Z|.
- About |W| they identify a lower bound. A point estimate needs a parametric heterogeneity family, chosen on grounds outside the data.
- The estimand is the written universe, more precisely its catchable part, and only from below.
- The counterexample I3 must build (step 3) is exact, not approximate. Hold W's histories fixed and vary |Z|: every text estimator returns byte-identical output. The appendix confirms this on one cell: rows A and A′ differ only in |Z| (40 versus 0) and give identical Chao2 and jackknife values.

## 2. Estimators that stay defensible under heterogeneity and dependence

| Estimator (incidence form, k occasions) | What it is valid for | Known bias |
|---|---|---|
| **Chao lower bound** (Chao2 / Mh lower bound): S_obs + ((k−1)/k)·f_1²/(2f_2); bias-corrected form S_obs + ((k−1)/k)·f_1(f_1−1)/(2(f_2+1)) | A lower bound under arbitrary heterogeneity. It is built for the case where most captured items are caught once or twice, where the jackknife "usually does not work well" (Chao 1987, abstract; Chao 1984 for the abundance form) | Low whenever many items are nearly uncatchable. The improved bound iChao (Chiu et al. 2014, abstract) uses f_3 and f_4, is "universally valid for any species abundance distribution", has an incidence version, and in their simulations always reduced bias against the traditional bound |
| **First-order jackknife** (Mh-JK): S_obs + ((k−1)/k)·f_1 | Nonparametric under Mh; linear in the capture frequencies (Burnham & Overton 1978, abstract) | Does not work well when most captured items are caught once or twice (Chao 1987, abstract). With too few occasions, no model is sufficiently accurate and underestimation may be substantial (Briand et al. 2000, abstract). It is the model most often recommended in software-inspection evaluations (§5) |
| **Sample coverage** (Chao, Lee & Jeng 1992; Lee & Chao 1994) | Mth, the case where catchability varies by occasion and by item. It can also model local dependence between lists (Chao et al. 2001, abstract) | "Generally works satisfactorily when the coefficient of variation of the individual capture probabilities is relatively large" (Chao et al. 1992, abstract), so it is presumably poorer at low heterogeneity (inferred) |
| **Parametric mixtures** (finite two-class, Pledger 2000; logit-normal, Coull & Agresti 1999; beta-binomial, Dorazio & Royle 2003) | Point estimates within an assumed family; identifiable there (Holzmann et al. 2006) | The family drives the answer (Link 2003; Dorazio & Royle 2003). With small p or large heterogeneity "the log-likelihood surface is relatively flat", and homogeneity models give intervals whose "actual coverage probability [is] much lower than the nominal level" (Coull & Agresti 1999, abstract) |
| **Log-linear models** (Fienberg 1972) | k lists form an incomplete 2^k table with one missing cell. The simplest model that fits the observed cells is projected onto the missing cell (abstract). Pairwise list dependence can be modelled | The k-way interaction is never estimable, and with k = 3 the model with all two-way terms is saturated (standard result; inferred). For k = 3, Darroch et al. (1993, abstract) handle heterogeneity with Rasch quasi-symmetry, but the projection still "involves the log-linear model of no second-order interaction" |

**Positive dependence between occasions.**
- Capture–recapture models must handle two kinds of source dependence: local (list) dependence and dependence due to heterogeneity (Chao et al. 2001, abstract). The International Working Group (1995, abstract) lists independence between samples and homogeneous catchability among the four assumptions of the two-list estimator.
- **Inferred, with the direction checked by simulation (appendix, row C).** Under positive dependence, items tend to be caught by many occasions or by none. That shrinks f_1 relative to f_2, so the Chao bound and the jackknife fall further below the truth. The lower bound stays a lower bound in direction and becomes more conservative. In row C (ρ = 0.5), Chao2 drops from 26.6 to 14.8 while the true number of unseen written items rises from 49.7 to 66.1. Negative dependence can push an estimate *above* the truth, so the lower-bound property holds only under positive or zero dependence.
- **Which bounds stay valid when assumptions fail (inferred; row C).** The Chao bound and iChao, provided dependence is non-negative. No nonparametric upper confidence limit has guaranteed coverage (Mao & Lindsay 2007, Theorem 3.4; for population size, claimed in their §7).

**Recommendation for N5 (inferred).**
- **Pre-register iChao2 as the lower bound.** It is the most defensible bound and needs no family.
- **Report the jackknife and sample coverage alongside it as sensitivity values**, each labelled heterogeneity-sensitive.
- **Report no parametric mixture as primary.** The data cannot choose a family, and the point estimate depends on that choice (Link 2003; Dorazio & Royle 2003).
- **Prefer log-linear models with k ≥ 4.** At k = 3 the model with all pairwise dependences is saturated, so not every pairwise dependence can be modelled at once.

## 3. Can the gold, as an independent occasion, correct the estimate?

### 3.1 When Lincoln–Petersen is valid

Take the union of text occasions as list 1 (caught items S, |S| = S_obs) and the gold as list 2 (n_g items, m of them also in S). The Chapman form is N̂ = (S_obs + 1)(n_g + 1)/(m + 1) − 1 (Chapman 1951).

**Inferred, by standard algebra.** Let g_i be item i's gold catchability and c_i its probability of entering S. Then E[m]/N = E[c·g] = E[c]·E[g] + Cov(c, g). The estimator is consistent when Cov(c, g) = 0. Heterogeneity in c is harmless when g does not covary with it, so one list behaving like a random sample of U is enough. For never-written items c_i = 0, so the condition reads: **the gold must catch never-written items at the same rate as written ones**, g_Z = g_W. Row A of the appendix meets this condition: the Lincoln–Petersen estimate of unseen items is 89.8 against a truth of 89.7.

### 3.2 Is the check informative or circular?

**It is informative, not circular.** The gold is a non-text occasion with positive catchability on Z, so it carries information the text occasions cannot. **But it rests on an assumption the data cannot test.** In the two-list table the cell "missed by both" is empty by construction. So Cov(c, g) cannot be estimated from these two lists. The same holds for k lists, where the top-order interaction is unidentified (standard result for the incomplete 2^k table of Fienberg 1972; inferred).

**Plausible signs (inferred).**
- **Positive, g_Z < g_W.** CTA golds are elicited from experts, and their omission of automated knowledge is the premise of the project. Then Lincoln–Petersen underestimates the residual (appendix row B: 69.7 against a truth of 89.7).
- **Negative, g_Z > g_W.** A gold built specifically to elicit tacit steps. Then it overestimates.

**The defensible design.**
- Pre-register a sensitivity range for g_Z/g_W.
- Report the residual as an interval over that range, not as a point.
- Where more than one gold exists for a task, treat the golds as extra non-text occasions. Even then, items with zero catchability in *every* occasion, text and gold, stay unidentified. This is the same §1 result one level up.

### 3.3 Why the N5 / R4 comparison cannot discriminate (L7.3 best reachable outcome)

**The gate's best reachable outcome (inferred).** The §22 N5 rule passes when |f̂_0,text − U_gold| ≤ τ·U_gold.
- f̂_0,text targets at most |W∖S|.
- The gold-side target is |W∖S| + |Z|.
- Give both sides perfect estimators. The relative error is then |Z| / (|W∖S| + |Z|), and the rule **passes only if the never-written share of all unseen items is at most τ**.

**What it implies.** With 20% never-written items and half of the written items unseen, the share is already 0.2/(0.4 + 0.2) = 33%. The rule fails τ = 25% before any estimator error is counted. It measures the absence of a residual, not the quality of an estimator.

**A second defect: the comparison target in I3 step 4.** I3 compares the text estimate with "the count of gold items no text occasion caught" (U_gold = n_g − m). That raw count equals g × (unseen items), not the unseen count. A low text estimate can therefore pass by offsetting errors. Appendix row A′ shows it with no never-written items at all:
- The jackknife (36.9) underestimates the 49.7 unseen written items by 26%.
- The raw gold count (39.8) underestimates the same 49.7 by 20%.
- So the jackknife sits within 10% of the raw count and "passes τ = 10%" while being 26% wrong.

The gold-side quantity with the right target is the Lincoln–Petersen unseen estimate N̂ − S_obs, which equals U_gold·S_obs/m. The raw U_gold is only a floor.

**A rule that does discriminate (inferred; for the owner and I3, not adopted here).** Split the gold items no text occasion caught into two groups:
1. items present somewhere in the fixed source corpus but missed by every extraction occasion;
2. items absent from the whole corpus.

The text occasions are extractions from a finite corpus, so this corpus-presence audit makes written versus never-written observable for gold items. It is subject to the matcher rules of pitfall (5), and it runs only after the pre-registration is hash-committed.

- The text estimator is then judged only on group 1, its real estimand.
- The residual is read from group 2, scaled by the gold's catchability on the written items, ĝ_W = m / S_obs.

The kill rule for the residual objective would then read the text estimator's error on written items. A large residual would no longer count as a failure.

## 4. Stress regimes in the simulation literature

These are the regimes I3's grid should span to stay comparable. Each is read from the source's abstract, except van Rijnsoever (full text).
- **Heterogeneity indexed by the coefficient of variation of individual capture probabilities.** Sample-coverage methods work when the CV is "relatively large" (Chao et al. 1992).
- **Small capture probability and large heterogeneity**, where the likelihood flattens and intervals under-cover. Studied under a logit-normal model with a random item effect plus fixed occasion effects (Coull & Agresti 1999).
- **Mixing family misspecified at matched fit.** Simulation shows deviance cannot select the family (Dorazio & Royle 2003); reasonable families predict near-identical data (Link 2003).
- **Sparse data, with most items caught once or twice** (Chao 1987, Monte Carlo).
- **Few occasions.**
  - Accuracy depends strongly on the number of inspectors. With too few, "no model is sufficiently accurate and underestimation may be substantial". The effect of the actual number of defects was also examined (Briand et al. 2000).
  - A Monte Carlo study of exactly two inspectors (El Emam & Laitenberger 2001).
- **Mean detection probability.** It matters more than the number of codes for the sample size needed to reach saturation: 1,100 hypothetical populations, number of codes 1–101, mean probability of observing a code 0.09–0.91 (van Rijnsoever 2017, "Simulation of scenarios").
- **Sample size.** Initial samples of 25–200, then doubled (Tran et al. 2017).

## 5. Precedents and how they validated against known truth

**Software inspection.**
- Capture–recapture entered software inspection in 1992 (Petersson et al. 2004, abstract); the 1992 paper is presumably Eick et al. (1992) [145] (not read). The ten-year review finds most evaluations end "in recommendation of the Mh-JK model".
- Briand et al. (2000) compared predicted with *actual* remaining defects on real inspection data. They found substantial underestimation with too few inspectors and recommended the jackknife.
- Wohlin, Runeson & Brantestam (1995) found that the assumptions are "not completely fulfilled in software development, leading to an underestimation". They corrected with an experience factor (abstract). Briand et al. calibrated on relative error from past inspections and found theoretical limits to that approach "confirmed by the data".
- El Emam & Laitenberger (2001) validated by Monte Carlo and recommended, for two inspectors, an estimator that allows inspectors of different capability.

**Qualitative saturation.**
- Tran et al. (2017) [157] model theme elicitation as a mixture of zero-truncated binomials, which is the Mh model (inferred). They validated by Monte Carlo (mean error 3% to 1%) and on the 1,053-participant burden-of-treatment survey (error below 2%; abstract).
- Lowe et al. (2018) validated a saturation model on two datasets, by consistency of its estimates.
- Barker (2023, abstract) [146] shows on the Guest et al. (2006) data that "saturation may occur more than once in a sequence of interviews". This is pitfall (7).

**What every precedent shares (inferred).** The known truth always lay inside the same capture process's catchable population. That means defects some inspector could find, or themes some respondent of the same survey could voice. No precedent validates against units with zero catchability on the estimating occasions. Their accuracy figures therefore bound the written-universe estimand, not the residual. Tran's 1–3% in particular says nothing about never-written items. The persistent underestimation found in software inspection fits unmodelled heterogeneity, and possibly near-zero-catchability defects, but no source separates the two.

## 6. Owner decision now due (R4, fatal-class)

The DS4 item says to raise this with I3's result, before any gold. It is stated here so that I3's result can be read against it.

**What should N5 estimate, given that the residual is not identifiable from text?**

1. **(Recommended) Re-specify N5 and rewrite R4's trigger.**
   - NOW estimand: the written universe, with iChao2 as the pre-registered lower bound and the jackknife and sample coverage as sensitivity values.
   - The residual is estimated only with the gold, as the Lincoln–Petersen unseen count minus the written-unseen estimate, or through the corpus-presence audit of §3.3.
   - It is reported as an interval over a pre-registered range of g_Z/g_W.
   - R4 fires on the text estimator's error on written gold items only.
   - Evidence: the §1 impossibility leaves the text estimand fixed whatever the owner chooses. Lincoln–Petersen is consistent under one stated assumption (§3.1). The current rule cannot discriminate (§3.3).
   - What would change this: if I3 finds that no text estimator gets within τ = 50% of the unseen *written* items, even at ρ = 0 and low heterogeneity, the estimand is unusable too, and option 2 becomes the right one.
2. **Drop the residual as an objective** (R4's stated falsifier, §22 N5). Keep RQ-B as localisation, scored by AUROC, which needs no size estimate. No untestable assumption remains, but the claim about how much knowledge is missing is lost.
3. **Keep §14.1 and N5 as written.** Not defensible. The rule fails whenever the residual is large and can pass by offsetting errors (§3.3).

## 7. Simulation grid for I3

**Estimand per cell.** I3 reports three quantities for each cell, against the simulation's known truth:
- **Text estimators** against the unseen written items |W∖S|. Report bias, interval coverage, and for the Chao bound and iChao the rate at which the bound holds, P(estimate ≤ truth).
- **Lincoln–Petersen unseen** against the total unseen |W∖S| + |Z|.
- **Residual estimate** (Lincoln–Petersen unseen minus the text estimate) against |Z|.

It also reports the raw gold-uncaught count as a floor, and the τ check in both forms, the §22 form and the written-only form, so the owner sees the difference. τ ∈ {10%, 25%, 50%} of the matching truth.

**The grid** (all labelled SYNTHETIC; 500 seeded replicates per cell; separate random streams for text and gold, so that matched pairs share text histories exactly):

| Axis | Values | Source / reason |
|---|---|---|
| N | {50, 200} | I3 default. The golds already known have 46 and 70 items (§14.3) |
| never-written share | {0, 0.2, 0.5} | I3 default |
| k text occasions | {2, 3, 5} | I3 default. k = 2 matches El Emam & Laitenberger (2001); k = 3 is where the all-pairwise log-linear model saturates (inferred; Fienberg 1972, Darroch et al. 1993) |
| mean text catchability | {0.15, 0.4} | **added.** Small p is where likelihoods flatten (Coull & Agresti 1999), and mean detection probability dominates the sample size needed for saturation (van Rijnsoever 2017) |
| heterogeneity | logit-normal σ ∈ {0.5, 1.5}, reporting the implied CV of p | I3's low/high, made concrete. CV is the index in Chao et al. (1992); logit-normal follows Coull & Agresti (1999) |
| mixing family | {logit-normal, two-class finite mixture at matched mean and CV} | **added.** Two-class family from Pledger 2000; the family drives N (Link 2003; Dorazio & Royle 2003) |
| text–text dependence ρ | {0, 0.3, 0.6}, as a Gaussian copula with exchangeable correlation across text occasions only, conditional on p_i | I3 default, defined operationally. It is local dependence, separate from heterogeneity (Chao et al. 2001) |
| gold catchability g_W | {0.6, 0.9} | **added.** Raw gold-uncaught = g × unseen (§3.3) |
| gold–text dependence g_Z/g_W | {0.5, 1.0, 1.5} | **added.** This decides whether Lincoln–Petersen is valid (§3.1–3.2) |
| matching false-non-match rate | {0, 0.1}; extension axis, may be run one-at-a-time from the reference cell | **added.** Pitfalls (4)–(5). A missed match inflates the gold-uncaught count |

**Counterexample (I3 step 3).** For each (N, k, heterogeneity, ρ) cell, pair never-written shares 0 and 0.5 with shared text streams. Assert that the text-estimator outputs are identical, and show that the Lincoln–Petersen unseen estimate separates them.

**I3's stop condition.** Read it on the *written-only* comparison. Under the §22 form it fails by construction whenever the never-written share exceeds τ (§3.3).

## Appendix: SYNTHETIC check of the derivations

- Spec: `ds4_check.py` below.
- SHA-256 of the script file: `fe8eb207630282d585730b8c5c41d97f11829e9483859633ed827d1c98677ff0`.
- Run with `python3 -I ds4_check.py` (standard library only; 2,000 replicates per row).
- Settings: k = 3, logit-normal heterogeneity with μ = −0.6 and σ = 1.0, gold catchability 0.8 unless stated. It illustrates §1–3. It is not I3's grid and is never a criterion.

| Row | W, Z | Chao2 | Jackknife | Unseen written (truth) | LP unseen | Raw gold-uncaught | Unseen total (truth) |
|---|---|---|---|---|---|---|---|
| A | 160, 40 | 26.6 | 36.9 | 49.7 | 89.8 | 71.9 | 89.7 |
| A′ | 160, 0 | 26.6 | 36.9 | 49.7 | 49.6 | 39.8 | 49.7 |
| B: g_Z = 0.4 | 160, 40 | 26.6 | 36.9 | 49.7 | 69.7 | 55.8 | 89.7 |
| C: ρ = 0.5 | 160, 40 | 14.8 | 23.8 | 66.1 | 106.0 | 84.9 | 106.1 |
| D: complete gold | 160, 40 | 26.6 | 36.9 | 49.7 | 89.7 | 89.7 | 89.7 |

What each row shows:
- **A and A′:** identical text estimates under different |Z|. This is the §1 counterexample.
- **A:** Lincoln–Petersen recovers the total when g_Z = g_W.
- **B:** Lincoln–Petersen underestimates under positive gold–text dependence.
- **C:** the lower bounds become more conservative under positive text dependence.
- **A′:** the offsetting-error pass described in §3.3.
- **D:** raw gold-uncaught equals the unseen count only when the gold is complete.

```python
import math
import random
import statistics as st

PHI = st.NormalDist()


def cell(n_written, n_never, k=3, mu=-0.6, sigma=1.0, rho=0.0, g_w=0.8, g_z=0.8, reps=2000, seed=1):
    rng = random.Random(seed)
    rng_gold = random.Random(seed + 1)
    acc = {key: [] for key in ("chao2", "jk1", "unseen_written", "lp_unseen", "gold_uncaught", "unseen_total")}
    for _ in range(reps):
        seen = q1 = q2 = gold = recaught = uncaught = 0
        for i in range(n_written + n_never):
            never = i >= n_written
            caps = 0
            if not never:
                p = 1 / (1 + math.exp(-(mu + sigma * rng.gauss(0, 1))))
                cut = PHI.inv_cdf(min(max(p, 1e-9), 1 - 1e-9))
                shared = rng.gauss(0, 1)
                caps = sum(math.sqrt(rho) * shared + math.sqrt(1 - rho) * rng.gauss(0, 1) < cut for _ in range(k))
            seen += caps > 0
            q1 += caps == 1
            q2 += caps == 2
            if rng_gold.random() < (g_z if never else g_w):
                gold += 1
                recaught += caps > 0
                uncaught += caps == 0
        acc["chao2"].append((k - 1) / k * q1 * (q1 - 1) / (2 * (q2 + 1)))
        acc["jk1"].append((k - 1) / k * q1)
        acc["unseen_written"].append(n_written - seen)
        acc["lp_unseen"].append((seen + 1) * (gold + 1) / (recaught + 1) - 1 - seen)
        acc["gold_uncaught"].append(uncaught)
        acc["unseen_total"].append(n_written + n_never - seen)
    return {key: round(st.mean(v), 1) for key, v in acc.items()}


if __name__ == "__main__":
    runs = {
        "A  W=160 Z=40 (reference)": dict(n_written=160, n_never=40),
        "A' W=160 Z=0 (pair of A)": dict(n_written=160, n_never=0),
        "B  W=160 Z=40, gold half as likely on Z": dict(n_written=160, n_never=40, g_z=0.4),
        "C  W=160 Z=40, text dependence rho=0.5": dict(n_written=160, n_never=40, rho=0.5),
        "D  W=160 Z=40, complete gold": dict(n_written=160, n_never=40, g_w=1.0, g_z=1.0),
    }
    for name, kw in runs.items():
        print(name, cell(**kw))
```

## References

- Barker C (2023). Pragmatic estimation of sample size for number of interviews for PRO development in the 2009 FDA PRO guidance. arXiv:2301.04760 (abstract). [146]
- Briand LC, El Emam K, Freimut BG, Laitenberger O (2000). A comprehensive evaluation of capture-recapture models for estimating software defect content. IEEE TSE 26(6):518–540. https://doi.org/10.1109/32.852741 (abstract) [145]
- Burnham KP, Overton WS (1978). Estimation of the size of a closed population when capture probabilities vary among animals. Biometrika 65(3):625–633. https://doi.org/10.1093/biomet/65.3.625 (abstract)
- Chao A (1984). Nonparametric estimation of the number of classes in a population. Scand J Stat 11:265–270. OpenAlex W1558982506 (not read; formula only) [144]
- Chao A (1987). Estimating the population size for capture-recapture data with unequal catchability. Biometrics 43(4):783–791. https://doi.org/10.2307/2531532 (abstract) [144]
- Chao A, Lee SM, Jeng SL (1992). Estimating population size for capture-recapture data when capture probabilities vary by time and individual animal. Biometrics 48(1):201–216. https://doi.org/10.2307/2532750 (abstract)
- Chao A, Tsay PK, Lin SH, Shau WY, Chao DY (2001). The applications of capture-recapture models to epidemiological data. Stat Med 20(20):3123–3157. https://doi.org/10.1002/sim.996 (abstract)
- Chapman DG (1951). Some properties of the hypergeometric distribution with applications to zoological sample censuses. Univ Calif Publ Stat 1:131–160 (not indexed; formula only)
- Chiu CH, Wang YT, Walther BA, Chao A (2014). An improved nonparametric lower bound of species richness via a modified Good–Turing frequency formula. Biometrics 70(3):671–682. https://doi.org/10.1111/biom.12200 (abstract)
- Coull BA, Agresti A (1999). The use of mixed logit models to reflect heterogeneity in capture-recapture studies. Biometrics 55(1):294–301. https://doi.org/10.1111/j.0006-341x.1999.00294.x (abstract)
- Darroch JN, Fienberg SE, Glonek GFV, Junker BW (1993). A three-sample multiple-recapture approach to census population estimation with heterogeneous catchability. JASA 88(423):1137–1148. https://doi.org/10.1080/01621459.1993.10476387 (abstract)
- Dorazio RM, Royle JA (2003). Mixture models for estimating the size of a closed population when capture rates vary among individuals. Biometrics 59(2):351–364. https://doi.org/10.1111/1541-0420.00042 (abstract)
- Eick SG, Loader CR, Long MD, Votta LG, Vander Wiel S (1992). Estimating software fault content before coding. ICSE '92:59–65. https://doi.org/10.1145/143062.143090 (not read) [145]
- El Emam K, Laitenberger O (2001). Evaluating capture-recapture models with two inspectors. IEEE TSE 27(9):851–864. https://doi.org/10.1109/32.950319 (abstract)
- Fienberg SE (1972). The multiple recapture census for closed populations and incomplete 2^k contingency tables. Biometrika 59(3):591–603. https://doi.org/10.1093/biomet/59.3.591 (abstract)
- Holzmann H, Munk A, Zucchini W (2006). On identifiability in capture–recapture models. Biometrics 62(3):934–936. https://doi.org/10.1111/j.1541-0420.2006.00637_1.x (abstract)
- International Working Group for Disease Monitoring and Forecasting (1995). Capture-recapture and multiple-record systems estimation I: History and theoretical development. Am J Epidemiol 142(10):1047–1058. https://doi.org/10.1093/oxfordjournals.aje.a117558 (abstract)
- Lee SM, Chao A (1994). Estimating population size via sample coverage for closed capture-recapture models. Biometrics 50(1):88–97. https://doi.org/10.2307/2533199 (abstract)
- Link WA (2003). Nonidentifiability of population size from capture-recapture data with heterogeneous detection probabilities. Biometrics 59(4):1123–1130. https://doi.org/10.1111/j.0006-341x.2003.00129.x (abstract)
- Lowe A, Norris AC, Farris AJ, Babbage DR (2018). Quantifying thematic saturation in qualitative data analysis. Field Methods 30(3):191–207. https://doi.org/10.1177/1525822X17749386 (abstract)
- Mao CX, Lindsay BG (2007). Estimating the number of classes. Ann Stat 35(2):917–930. https://doi.org/10.1214/009053606000001280; full text arXiv:0708.2153
- Petersson H, Thelin T, Runeson P, Wohlin C (2004). Capture–recapture in software inspections after 10 years research — theory, evaluation and application. J Syst Softw 72(2):249–264. https://doi.org/10.1016/S0164-1212(03)00090-6 (abstract)
- Pledger S (2000). Unified maximum likelihood estimates for closed capture–recapture models using mixtures. Biometrics 56(2):434–442. https://doi.org/10.1111/j.0006-341x.2000.00434.x (abstract)
- Tran V-T, Porcher R, Tran V-C, Ravaud P (2017). Predicting data saturation in qualitative surveys with mathematical models from ecological research. J Clin Epidemiol 82:71–78.e2. https://doi.org/10.1016/j.jclinepi.2016.10.001 (abstract) [157]
- van Rijnsoever FJ (2017). (I can't get no) saturation: a simulation and guidelines for sample sizes in qualitative research. PLoS ONE 12(7):e0181689. https://doi.org/10.1371/journal.pone.0181689 (full text)
- Wohlin C, Runeson P, Brantestam J (1995). An experimental evaluation of capture-recapture in software inspections. Softw Test Verif Reliab 5(4):213–232. https://doi.org/10.1002/stvr.4370050403 (abstract)
