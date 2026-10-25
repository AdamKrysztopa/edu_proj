# I3 — N5 identifiability: zero catchability and planted dependence

**SYNTHETIC — not evidence about learners or experts.** Every number here comes from a specified
simulation (§12 use 1, known-truth debugging). It may shape the N5 pre-registration; it is never a
criterion and never feeds a gate. The spec, generator and estimator sha256 hashes are in `grid.json`.
Date 2026-10-24. No model is involved, and the cost was $0. Reproduce, byte-identical:
`uv run --directory residual python ../research/n5_sim/simulate.py` (about 2 minutes on 8 cores).

## Result

**Text occasions identify the written universe only.** Within it, the best tolerance any estimator
reaches is **τ = 50%**, and only with near-independent occasions, low heterogeneity and a universe of
about 200 items. At N = 50, the grid value nearest the known golds (46 and 70 items, DS4 §7), no estimator reaches
it in the DS4 grid. The jackknife reaches it in the default grid only at k = 3, where its bias happens
to be small. With text–text dependence ρ = 0.6, nothing reaches it in either grid. Neither stop
reading below is triggered as written. Read at N = 50, though, the written-only reading fails, and that is the
condition DS4 gives for switching to option 2, dropping the residual (DS4 §6, option 1, "What would
change this"). DS4 states the condition over the whole grid; reading it at N = 50 is this note's
choice, as is the "≥ 80% of replicates" meaning of achievable. R4 goes
to the owner with both readings.

1. **Zero catchability is unidentifiable from text.** Never-written items leave every frequency
   count unchanged. The simulator asserts this in every replicate with never-written items, and the
   counterexample below shows it. In the default grid (N = 200, k = 5, low heterogeneity, ρ = 0),
   Chao1 and Mh stay within 7% of the unseen written items U_w (coverage 0.94–0.96) as the
   never-written share rises from 0 to 0.5. Against the total unseen U they fall short by that share:
   −60% at 0.2 and −85% at 0.5, with coverage of U at 0.16–0.19 and 0.00. Only the gold sees
   never-written items, as an independent occasion (Lincoln–Petersen). Its unseen estimate is unbiased
   for U when the gold catches both kinds of item at the same rate (median relative bias 0.000 across
   the DS4 grid). It is −28% at g_Z/g_W = 0.5 and +10% at 1.5, and +18% with a 10% false-non-match rate.
2. **Dependence decides reachability.** In both grids no estimator reaches τ = 25% or τ = 10% on
   written items in any cell (0 of 5508). At τ = 50% (achievable means passing in at least 80% of
   replicates, which is our choice):

   | written-only (U_w truth), τ = 50%: cells where an estimator is achievable | default grid | DS4 grid |
   |---|---|---|
   | ρ = 0, low heterogeneity | 18 / 36 | 280 / 864 (all at N = 200; 0 / 432 at N = 50) |
   | ρ = 0, high heterogeneity | 10 / 36 | 107 / 864 |
   | ρ = 0.3 | 1 / 108 | 181 / 1728 (148 at σ = 0.5) |
   | ρ = 0.6 | 0 / 108 | 0 / 1728 |

   The two grids model ρ differently: a "copy one draw" mixture in the default grid and a Gaussian
   copula in DS4. So ρ = 0.3 is weaker dependence in DS4. The median bias against U_w falls from about
   0 (ρ = 0, σ = 0.5) to −50% at ρ = 0.3 and −77% at ρ = 0.6, and Mh coverage falls from 0.92 to 0.72
   and then 0.19. This is the "stable underestimate" of §14.1.
3. **The τ rule needs a stand-in clause (L7.3).** On the written-only form at ρ = 0 and low
   heterogeneity, the trivial stand-in f0 = f1 (the singleton count) also passes in 10 of the 18
   achievable default cells and in 139 of the 280 achievable DS4 cells. The zero stand-in passes in at most
   4% of replicates (default grid) and 22% (DS4), and uniform noise in at most 63% and 67%. The planted positive fires: N = 200, k = 3,
   low heterogeneity, ρ = 0, written-only, gives Chao1 0.93, Mh 0.90 and jackknife 1.00, but f1 0.90.
   At ρ = 0.3 only 9 of 181 achievable DS4 cells survive the clause.
4. **The comparison as written lets errors cancel.** The I3 spec compares against the raw count of
   gold items that no text occasion caught, G (the §22 form). That count is about g × unseen. With
   gold p = 0.6 in the default grid's planted positive, correct estimators fail it (Chao1 0.50), while
   the same estimators pass the Lincoln–Petersen and written-only forms at 0.88–0.93. In 34 DS4 cells
   an estimator passes the §22 form at τ = 25% while failing the written-only form at τ = 25% (pass
   rate below 0.5); DS4's own jackknife example is the same effect. When the never-written share is 0.5,
   even the perfect written-universe estimate passes the §22 form at τ = 50% in only 25% of replicates
   (DS4 median), and the Lincoln–Petersen form in 1%. This is DS4 §3.3: the rule measures whether there
   is no residual.
5. **Small-t forms are required, and the small-t "lower bound" is not one.** At 2–5 occasions,
   classic Chao1 overstates the unseen count: +100% at k = 2, +44% at k = 3 and +18% at k = 5 (default
   grid, low heterogeneity, ρ = 0). Lee–Chao coverage is worse, at +342%, +144% and +68%. The (t−1)/t
   factor and the Chao–Jost coverage bring both within 6%. Even so, small-t Chao1 is at or below U_w in
   only 62% of replicates at σ = 0.5 (DS4 median), against 95% at σ = 1.5. It is a lower bound only
   under strong heterogeneity. DS4 proposes iChao2 as the pre-registered bound, but iChao2 adds a term
   in f3 and f4, which are structurally zero at k = 2 (and f4 at k = 3), so it adds nothing beyond
   Chao2 there (Chiu et al. 2014, not opened). It is not implemented here.
6. **The residual estimate absorbs dependence.** The residual estimate is the Lincoln–Petersen unseen
   count minus Mh. At ρ = 0, σ = 0.5 and g_Z/g_W = 1 its median error against the never-written count
   |Z| is −2%. Over all dependence levels it is +47%, because the text estimator's loss from dependence
   is booked as residual. It also inherits the g_Z/g_W error: −52% at a ratio of 0.5 and +21% at 1.5
   (both at ρ = 0, σ = 0.5).

## Stop condition: both readings

The I3 stop rule is: "if no estimator meets even τ = 50% with independent written occasions and a
never-written share of 0, stop and raise R4." Following the coordinator's instruction, the rule is
reported as written and also on written items only.

| reading | default grid | DS4 grid | triggered? |
|---|---|---|---|
| **As written**: §22 form against raw G, ρ = 0, never-written 0 | 6 / 18 cells achievable; 2 / 18 with the f1 clause | 201 / 576; 132 / 576 with the clause, part of it by cancellation (point 4) | no |
| **Written-only** (DS4 §7): against U_w, ρ = 0, low heterogeneity | 18 / 36; 8 / 36 with the clause | 280 / 864; 141 / 864 with the clause | no |
| Written-only at N = 50, the grid value nearest the known golds | 4 / 18, all jackknife at k = 3; 4 / 18 with the clause | **0 / 432** | **yes in DS4**; in the default grid, met only where the jackknife's bias happens to cross zero |

## Decision it feeds

This note selects the estimator, the estimand and a realistic tolerance for the N5
pre-registration. It does not read N5's gate. Whether N5 keeps the residual at all is R4, which goes
to the owner.

- **Estimand: unseen written items, U_w.** It is the only quantity text occasions identify. The
  never-written part is estimated only through the gold. It is read as Lincoln–Petersen unseen minus
  the text estimate, over a pre-registered range of g_Z/g_W, and it inherits all of the text
  estimator's loss from dependence (point 6).
- **Estimator: small-t Chao1** (`chao1`, default), with the Chao–Jost Mh (`mh_coverage`) and the
  jackknife as sensitivity values.
  - Chao1 is achievable in the most DS4 cells at ρ = 0, σ = 0.5 (239, against 231 for Mh and 213 for
    the jackknife).
  - Its median bias stays within −10% to 0 across k and mean catchability.
  - Mh runs +25% at k = 3 when p = 0.15.
  - The jackknife's bias changes sign with p and k, from −58% at k = 2 to +54% at k = 5.
- **Tolerance: τ = 50%,** read on written items. That means the corpus-presence audit form (`w_obs`,
  DS4 §3.3), not the raw G. A pass is credited only when the f1 and zero stand-ins fail on the same
  data. τ = 25% is unreachable in every cell of both grids.

## Zero-catchability counterexample

There are 100 written items, k = 3 text occasions, low heterogeneity and ρ = 0 (`counterexample.json`).
73 written items are caught, with f = (47, 23, 3), and 27 written items are unseen (U_w). In the DS4
grid, every replicate with never-written items also asserts that the counts equal the counts of the
written items alone.

| never-written | true U | Chao1 f0 | Mh f0 | jackknife f0 | gold p = 1: G / LP f0 | gold p = 0.6: G / LP f0 |
|---|---|---|---|---|---|---|
| 0 | 27 | 32.0 | 32.7 | 31.3 | 27 / 27.0 | 11 / 18.5 |
| 100 | 127 | 32.0 | 32.7 | 31.3 | 127 / 127.0 | 72 / 121.1 |
| 400 | 427 | 32.0 | 32.7 | 31.3 | 427 / 427.0 | 245 / 370.0 |

The three text estimators return identical values and intervals for all three universes, while the
truth moves by 400. The gold occasion moves with the truth.

## Method

- **Default grid** (324 cells): the I3 prompt's axes, plus gold p ∈ {1.0, 0.6} and an "extreme"
  heterogeneity sensitivity level.
  - p_i ~ Beta with mean 0.3: CV 0.21 low, 0.60 high, and 0.97 extreme. The extreme level has a < 1,
    so infinite density at p = 0; every estimator fails there (−62% to −84%).
  - ρ is the probability that an item's k text captures copy one shared draw.
- **DS4 grid** (5184 cells), from `research/ds4-identifiability.md` §7 at `b4c9abf`.
  - Axes: N ∈ {50, 200}; never-written share ∈ {0, 0.2, 0.5}; k ∈ {2, 3, 5}; mean p ∈ {0.15, 0.4};
    logit-normal σ ∈ {0.5, 1.5}; family ∈ {logit-normal, two-class at matched mean and SD, weight 0.25
    on the high class (our choice)}; ρ ∈ {0, 0.3, 0.6} as an exchangeable Gaussian copula across text occasions,
    conditional on p_i; g_W ∈ {0.6, 0.9}; g_Z/g_W ∈ {0.5, 1.0, 1.5}, with g_Z capped at 1 (our choice;
    the effective ratio is 1.11 at g_W = 0.9); false-non-match ∈ {0, 0.1}, run as a full axis (our
    choice; DS4 allows running it one axis at a time).
  - A false non-match moves a caught gold item into the gold-uncaught count. The corpus-presence
    audit is exact.
  - Text, gold and match draws use separate random streams.
- **Both grids:** 500 seeded replicates per cell.
- **Comparison forms** (every cell, τ ∈ {10%, 25%, 50%}):
  - `s22`: the raw gold-uncaught count, as the I3 spec and §22 state it;
  - `lp`: the Lincoln–Petersen unseen count;
  - `w_true`: U_w, the simulation truth;
  - `w_obs`: Lincoln–Petersen on the gold items that the corpus audit finds written, the observable
    written-only form.

  Each form is computed for the estimators, the stand-ins (zero, f1, uniform noise) and the two
  ceilings (the U_w and U oracles). A failed estimate counts as a miss. The three primary estimators
  fail in at most 0.8% of replicates, and `mh_lee_chao` in up to 55%.
- **Generator self-check** (`selfcheck.json`), run before any cell:
  - no never-written item is ever text-caught;
  - the Beta means are 0.29–0.31, and the pooled correlations match ρ + (1−ρ)·Var(p)/(μ(1−μ));
  - logit-normal and two-class match the target mean within 0.01 and the CV within 0.05;
  - copula correlation rises with ρ, and the marginals hold.
- **Estimators** (`residual/src/residual/estimators.py`, stdlib and pydantic only):
  - small-t Chao1, with Chao's log-normal interval;
  - the first-order jackknife, with the Burnham–Overton variance;
  - the Lee–Chao sample-coverage Mh, with Chao–Jost coverage by default and a delta-method variance;
  - Lincoln–Petersen with the Chapman correction.

  A full Mh needed no outside dependency. `to_record` fills `EstimatedResidual` unchanged, and
  `residual.py` is untouched. The live fingerprint matches `residual/frozen/n1.json` on schema,
  features and semantics. `EstimatedResidual.estimator` cannot record the Chao1 or Mh variant, so
  the pre-registration must name it.
- **Outputs:** `cells.json`, `ds4_cells.json.gz` (gzip, mtime 0) and every cell tabulated in
  `tables.md`.

### Bias against U_w, default grid, N = 200, never-written share 0, gold p = 1 (Chao1 / Mh / jackknife)

| heterogeneity | ρ | k = 2 | k = 3 | k = 5 |
|---|---|---|---|---|
| low | 0 | +0.00 / +0.00 / −0.58 | −0.04 / +0.01 / −0.18 | −0.05 / −0.02 / +0.54 |
| low | 0.3 | −0.75 / −0.75 / −0.74 | −0.48 / −0.43 / −0.56 | −0.64 / −0.50 / −0.42 |
| low | 0.6 | −0.95 / −0.95 / −0.87 | −0.74 / −0.79 / −0.80 | −0.86 / −0.83 / −0.77 |
| high | 0 | −0.47 / −0.47 / −0.66 | −0.46 / −0.41 / −0.43 | −0.43 / −0.38 / −0.16 |
| high | 0.3 | −0.84 / −0.84 / −0.78 | −0.68 / −0.66 / −0.67 | −0.72 / −0.67 / −0.60 |

## Limits

- **Pass rates are per replicate.** N5 sees one data set, so a pass rate of 0.9 means a 10% chance
  of a false fail in the cell most favourable to N5.
- **The gold is independent of text, given its catchability.** Gold–text dependence enters only
  through g_Z/g_W. Correlation between gold and text within the written items (the same experts
  writing both) is not modelled, and it would bias Lincoln–Petersen low (§14.1 pitfall 1).
- **What is not covered:** time and behaviour effects, negative dependence, and iChao2.
- **Some formulas were checked through secondary sources** (listed under Sources), where the
  primary paper could not be opened.

## Sources

- Chao, A. (1987). Estimating the population size for capture–recapture data with unequal
  catchability. *Biometrics* 43, 783–791. The estimator, its variance (EstimateS 9.1 User's Guide,
  App. B, eqs. 1 and 5) and the log-linear interval (EstimateS: "as suggested by Chao (1987)"). The
  same point formula is Krebs (2021) eq. 2.35, which Krebs credits to Chao (1988), *J. Wildl. Manage.*
  52, 295–300. The primary paper was not opened.
- Burnham, K. P. & Overton, W. S. (1978). Estimation of the size of a closed population when capture
  probabilities vary among animals. *Biometrika* 65, 625–633. First-order jackknife. The worked
  value, 20 (19–26), comes from Program CAPTURE as printed in Krebs (2021), Box 2.4.
- Lee, S.-M. & Chao, A. (1994). Estimating population size via sample coverage for closed
  capture–recapture models. *Biometrics* 50, 88–97. Not opened; the formula is as stated in
  `estimators.py`.
- Chao, A. & Jost, L. (2012). Coverage-based rarefaction and extrapolation: standardizing samples by
  completeness rather than size. *Ecology* 93(12), 2533–2547. Not opened; the incidence coverage is
  taken as coded in iNEXT `Chat.Sam` (https://github.com/cran/iNEXT/blob/3.0.2/R/iNEXT.r).
- Chiu, C.-H., Wang, Y.-T., Walther, B. A. & Chao, A. (2014). An improved nonparametric lower bound
  of species richness via a modified Good–Turing frequency formula. *Biometrics* 70, 671–682. iChao;
  not opened.
- Krebs, C. J. *Ecological Methodology*, ch. 2 (2021 web edition):
  https://www.zoology.ubc.ca/~krebs/downloads/krebs_chapter_02_2021.pdf. Box 2.1 (the (M+1)(C+1)/(R+1) − 1 form, Krebs's eq. 2.2,
  2383 hares), Box 2.4 (the CAPTURE jackknife) and eq. 2.35 (Chao).
- Colwell, R. K. EstimateS 9.1 User's Guide (https://www.robertkcolwell.org/media_files/63). The
  (n−1)/n small-sample factor in Chao1 and Chao2.
- Edwards, W. R. & Eberhardt, L. L. (1967). Estimating cottontail abundance from livetrapping data.
  *J. Wildl. Manage.* 31(1), 87–96. 76 rabbits caught on 18 trapping nights (SpadeR
  `ChaoSpeciesData` documentation) from a confined population of known size (abstract). The size
  135, which the tests use as an anchor, is reported secondhand and not verified here. The
  frequencies were decoded from `data(cottontail)` in the CRAN package SPECIES
  (https://github.com/cran/SPECIES).
- `research/ds4-identifiability.md` (branch `ds4-identifiability`, `b4c9abf`): the grid, the
  written-only target and the R4 options; `REORIENTATION.md` §12 use 1, §14.1, §16 R4 and §22 N5;
  `docs/plans/coverage-audit.md` finding 17.
