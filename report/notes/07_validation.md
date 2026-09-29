# 07 Validation programme: from gap candidates to validated predictions of human knowledge gaps

Author: Validation Programme Researcher (worker note for the orchestrator). Date: 2026-09-29.
BibTeX: `report/notes/07_validation.bib` (no .bib path was given in the task; merge into the report .bib).
Verification lines for every key are in section 8.

Category tags used on every important statement:
**[LIT]** ESTABLISHED LITERATURE, **[POC]** OBSERVED IN THE PoC, **[INT]** INTERPRETATION,
**[HYP]** HYPOTHESIS, **[FW]** FUTURE WORK. Every study below (V0–V8) is **[FW]**: nothing in it has run.
Where this note proposes something that is not already registered in `REORIENTATION.md`, it says
"proposed here". The registered rules it reuses are cited by section.

---

## 0. Starting point (what the PoC does and does not give us)

- **[POC]** The N3 PoC produces *gap candidates*: records where a methodology lens fired on a construct
  whose content the sources do not state (`research/n3/README.md`). Final maps: PLC 9 candidates,
  GDPR v1 1, GDPR v2 6 (checked in `research/n3/*/gapmap.json`: map records by lens).
- **[POC]** The closure step, which decides whether a missing element is really unsaid, is not
  informative. In the mismatched-evidence control, the judge's closure rate on the candidate's own
  evidence equals its rate on swapped evidence: PLC 0.889 vs 0.889 (n = 54), GDPR v1 0.961 vs 0.961
  (n = 51), GDPR v2 0.958 vs 0.958 (n = 48); every map carries the flag `closure-uninformative`
  (checked in `research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.json`, `checks.mismatched_evidence_control.total`).
- **[POC, partly unverified]** Precision by adversarial judgement on the pre-final maps: 3 of 19 strict,
  8 of 19 lenient. This number appears in `research/n3/README.md`, `PROGRESS.md` and commit `ec45c31`,
  but the per-record tally is not a committed artefact, so it is **unverified at the primary level**.
  If taken at face value, the Wilson 95% interval for 3/19 is 5.5%–37.6% (computed here).
- **[POC]** N2's research validation is deferred: E-LIVE v3 blocked by the API quota; E-PLANT gated arm
  sealed and unscored, ungated baseline a_U = 5/24, below the validity floor of 8; E-ABST pipeline arm
  descriptive only (`research/n2/closeout.md`; a_U checked in `research/n2/e_plant_eabst_report.md` line 12).
- **[POC]** All three gap maps share one config hash (`35fd0af2…04c1`), and its lexicons were tuned
  in-sample on the same three ledgers (`research/n3/README.md`, Limitations).
- **[INT]** So the PoC gives a pipeline and hypotheses, not evidence that the hypotheses point at real
  human knowledge. The programme below exists to close that distance, one falsifiable link at a time.

---

## 1. The validation logic chain

Each link is a necessary condition for the next. A failed link stops or re-routes everything above it.
The order follows `REORIENTATION.md` §17 (RQ-B central; RQ-A and RQ-D necessary) and §22 (N3 gate first).

| Link | Claim to establish | Hypothesis (**[HYP]**) | Falsifier (pre-registered) | Study |
|---|---|---|---|---|
| L0 | The pipeline's outputs can be trusted as inputs | Gated reconstruction adopts fewer planted falsehoods and gives fewer false answers than the ungated model | The registered N2 gates (E-PLANT, E-ABST) read Stop, or E-LIVE v3 fails admissibility | V0 |
| L1 | The "unsaid" decision is informative | An automated closure judge agrees with blind human coders on whether a missing element is stated in the evidence, and its own-minus-control difference tracks the humans' | Judge–human κ < 0.70, or below the lower 95% bound of human–human κ; or judge own rate = control rate while humans' differ | V1 |
| L2 | The gap map beats cheap baselines on retrospective public gold | ΔAUROC(gap map − strongest §14.3 baseline) ≥ δ for areas that a published gold shows were missed | Upper 90% bound of ΔAUROC < δ (N3 stop rule, §22) | V2 (E-CTA), V3 (E-OSS) |
| L3 | The residual can be measured, not only predicted | A text-occasion estimate of unseen items matches the gold-as-occasion count within a pre-set tolerance | Estimate outside tolerance (N5 stop rule; falsifier part 2, §1) | V4 |
| L4 | Predictions hold on fresh human elicitation, not only on old published gold | In a new domain, with the map frozen before any interview, areas the map ranks high yield more validated expert-added items than random, density-chosen and LLM-chosen areas, with experts and interviewers blind to the map | Upper 90% bound of prospective ΔAUROC < δ; or the rate ratio against the strongest control has a 90% upper bound below the pre-set SESOI | V5 |
| L5a | Targeting saves expert time | Gap-map-targeted elicitation recovers more validated items per expert hour than untargeted CTA of equal length (the §17 central hypothesis) | Upper 90% bound of the per-hour ratio below the SESOI | V6 |
| L5b | It transfers to an organisation | Predicted gaps in one partner's units match where staff add knowledge and where post-departure or onboarding trouble concentrates | Hit rate not above control areas; or the pilot is blocked by law or works council | V7 |
| L5c | Gaps matter for learners | Areas confirmed as residual carry more learner errors than covered areas, beyond difficulty baselines; teaching the residual improves delayed transfer | No association beyond baselines; Track A K2 kill (RCT effect below d = 0.30) for its own topic | V8 |

**[INT]** Two orderings matter.
1. L1 comes before L2 because the gap map's candidate set depends on closure. If closure is
   uninformative, V2 tests "lens fired" plus density, and a stop result could be a closure artefact.
   The N3 plan already warns that with dead features ΔAUROC ≈ 0 by construction
   (`docs/plans/n3-gap-map-plan.md`, "Implication").
2. L4 comes after L2, not before, because `REORIENTATION.md` §20 and §22 forbid recruiting for the new
   tracks until E-CTA and E-OSS read out. Retrospective gold is cheap; experts are not.

**[INT]** The chain has one branch. If L2 stops (upper bound < δ), the programme gate in §22 pivots
to H3: EIG-driven elicitation without the reconstruction prior. V5 is then not run in its H1 form,
and V6 runs as the H3 test (section 2, V6).

---

## 2. Staged studies V0–V8

Common rules for all studies (from `REORIENTATION.md` §18, restated so the design reads alone):
public or consented data only; no LLM judge as a criterion; synthetic output only as a predictor;
all thresholds, the primary gold/domain, primary model and primary baseline hash-committed before
any gold or human data are seen **[LIT]** pre-registration practice (nosek2018preregistration);
cost per validated item logged for every study (E-COST, N9).

Common statistics (proposed here, anchored in **[LIT]**):
- **AUROC and ΔAUROC.** Area-level AUROC with DeLong's method for correlated curves
  (delong1988comparing); where areas cluster inside golds, repositories or experts, Obuchowski's
  clustered extension (obuchowski1997nonparametric) or a cluster bootstrap. Hanley–McNeil
  (hanley1982meaning) only for planning.
- **"Strongest baseline" chosen honestly.** The comparison is against the maximum of K baselines.
  Picking the maximum after seeing the data biases ΔAUROC upward for the baselines and makes
  the test conservative in an unknown way. Proposed here: compute min_k ΔAUROC_k inside each
  bootstrap resample, so the selection is part of the sampling distribution.
- **Decision rule.** The §22 rule is an inferiority/superiority test against a smallest effect
  of interest, the logic of equivalence testing with two one-sided tests **[LIT]**
  (schuirmann1987comparison; lakens2017equivalence; lakens2018equivalence): stop if the upper 90%
  bound < δ; continue if the lower 90% bound > 0 and the point estimate ≥ δ; otherwise inconclusive,
  one pre-registered fallback, then the same rule.
- **Proportions.** Wilson intervals (wilson1927probable).
- **Agreement.** Cohen's κ for nominal two-coder labels, Krippendorff's α for segmentation and
  multi-coder data (hayes2007answering). Krippendorff recommends α ≥ .800, and ≥ .667 only for
  tentative conclusions **[LIT]** (krippendorff2004reliability, p. 241). The project's registered
  threshold is κ ≥ 0.70 and not below the lower CI bound of human–human κ (§18). Report prevalence
  and PABAK next to κ, because high agreement can coexist with low κ when one category dominates
  **[LIT]** (feinstein1990high). Landis–Koch labels (landis1977measurement) are descriptive only,
  never a threshold.

### Choosing δ (a threshold the programme cannot avoid)

δ is "to set" in the §22 threshold table. Planning arithmetic (computed here, Hanley–McNeil with a
1:1 split of missed and not-missed areas, AUROC 0.70 vs 0.62, correlation 0.5 between the two
scores' errors; the correlation is an assumption):

| Areas per class | 90% half-width, single AUROC 0.70 | 90% half-width, ΔAUROC |
|---|---|---|
| 10 | ±0.20 | – |
| 20 | ±0.14 | ±0.14 |
| 40 | ±0.10 | ±0.10 |
| 100 | ±0.06 | ±0.06 |
| 150 | – | ±0.05 |

**[INT]** A published CTA gold such as Sullivan's has 46 items **[LIT]** (sullivan2014use: 20/46
unprompted, 31/46 prompted), which will give perhaps 15–25 areas. One gold therefore cannot
resolve any δ below about 0.15. δ = 0.05 needs roughly 150 missed and 150 not-missed areas,
which only E-OSS (hundreds of code units per repository) or pooling many golds can supply.

**Recommendation on δ: set δ = 0.05 AUROC (Recommended)**, and accept that E-CTA alone will usually
read *inconclusive* while E-OSS and the prospective study V5 carry the decision. Reason: a gain
smaller than 0.05 over the density and area-size baselines is unlikely to justify running the
reconstruction pipeline at all, and a larger δ (e.g. 0.10) would let the stop rule kill a
predictor with a real but modest gain. What would change this: a cost model (from E-COST and the
V5 pilot) showing that expert time is so expensive that even a 0.03 gain pays, or so cheap that
only 0.10 does. δ must be fixed before any gold is acquired, so the cost model can only use
pre-gold information.

### V0 — Readiness, freeze and deferred N2 validation (no participants)

- **Hypothesis.** L0: the gated pipeline is trustworthy enough to feed a gold test.
- **Design.** (1) Hash-freeze `gapmap/src/gapmap/config.py` (lexicons, denylist, stop-anchors) and the
  N1 feature set; (2) build `area_features()` and the run-admissibility check (every located extraction
  has a verdict; cross-verify and decoys ran), then report which features are live and which dead
  on the E-LIVE ledgers (N3 plan steps 1–2); (3) run the deferred N2 protocols exactly as registered:
  E-LIVE v3 at `n2-freeze-3`, E-PLANT run 2 and unsealing, E-ABST run 2 with owner and second coding
  (`docs/n2-eplant-eabst-protocol.md`); (4) build the dated-corpus mode with the DOI/title gold
  blocklist; (5) fill in the threshold table and hash-commit the V1–V4 pre-registration after a
  `methods-critic` review.
- **Participants.** None; one blind second coder for E-ABST (already registered).
- **Controls/baselines.** As registered in N2 (ungated model).
- **Primary measure.** N2 gate readings; admissibility pass; share of dated sources in a non-gold pilot.
- **Kill/continue.** N2 gate readings stand as registered. **[INT]** By the owner's 2026-09-28
  exception (`REORIENTATION.md` §22), N3 does not wait on N2's research validation, so V0's N2 part
  gates only V7 (organisational pilot) and any provenance claim, not V2/V3. The freeze and
  admissibility steps *do* gate V2/V3: no hash, no gold.
- **Cost/time.** API spend of tens of dollars (N2 domain runs cost about $0.88 each, checked in
  `research/n2/e_plant_eabst_report.md` §3; N3 needs ≥ 3 reruns per task and multi-family reruns);
  4–8 weeks of engineering.

### V1 — Closure-step validation on a human-labelled closure set (no participants; coders only)

- **Hypothesis.** L1: an automated closure judge decides "stated / partly stated / not stated" as
  blind humans do, and separates own evidence from swapped evidence as humans do.
- **Design.** Build a closure set of (lens, seed span, missing element, evidence pool) units. Two arms
  per unit, as in the PoC's fair control: own evidence and mismatched evidence (other sources swapped
  for the nearest other candidate's). Units come from the three existing ledgers **and** at least one
  new, non-gold domain run after the V0 freeze, so the judge is not scored only in-sample.
  Judges: the current local Qwen 7B, a stronger open-weight judge, and a panel of judges from
  families different from the ledger's generator and verifier (decision 0008 rule `closure-judge-other-family`).
- **Participants.** Coders, not participants: owner under origin blinding plus one blind second coder
  (§22); proposed here: a second non-owner coder for any unit set that will gate V2, so the gating
  κ does not depend on the owner, who built the lenses.
- **Materials.** A written closure codebook with anchors per lens (what counts as the boundary of a
  judgement term, an exception condition, a rationale), fixed before coding.
- **Blinding.** Coders see neither the arm (own vs swapped), the judge's answer, the lens's rank, nor
  the domain run ID.
- **Primary measure.** Judge–human κ on the binary "not stated" label (open vs partial-or-closed),
  against the human–human κ and its lower 95% bound.
- **Secondary.** Human own-minus-control difference vs judge own-minus-control difference; per-lens κ;
  confusion by lens; judge cost per unit.
- **Reliability plan.** All units double-coded; disagreements adjudicated by discussion after κ is
  computed and frozen. Human–human κ below 0.70 means the construct itself is unreliable: revise the
  codebook once on a fresh sample, then stop.
- **Sample size.** Approximate 95% half-width of κ ≈ 0.70 (observed agreement 0.85, chance 0.50):
  ±0.20 at 50 units, ±0.14 at 100, ±0.10 at 200 (computed here with the large-sample SE).
  **Proposed: 200 units per arm-type (≈ 400 codings per coder)**, stratified by lens, so the
  adoption rule can be read to ±0.10.
- **Kill/continue.** Continue with the automated judge if it meets the §18 adoption rule (κ ≥ 0.70
  and not below the human–human lower bound) **and** its own–control gap is within ±0.10 of the
  humans'. If no judge passes: closure is coded by humans in V2 (costly but valid), or the closure
  feature is dropped and V2 is pre-registered as a test of lens firing plus the other features.
  **[INT]** Either way V2 can run; what V1 decides is whether V2 tests the full map.
- **Cost/time.** About 15–25 coder-hours per coder (planning assumption: 2–3 minutes per unit);
  judge compute negligible (local). 3–5 weeks.

### V2 — E-CTA: CTA replay against published gold (no participants; coders only)

- **Hypothesis.** L2 (RQ-B): the frozen gap map ranks areas that a published CTA gold shows the
  reconstruction missed above areas it did not miss, by at least δ over the strongest baseline.
- **Design.** As registered (`REORIENTATION.md` §18 E-CTA, §18.2; `docs/plans/n3-gap-map-plan.md`):
  pre-register and hash-commit; check itemised availability by metadata only; build the area
  partition from a dated pre-gold procedural source by a written procedure; reconstruct from a
  corpus frozen at the gold's publication date (OpenAlex dates, Wayback snapshots); run the gap map;
  only then acquire the gold, sealed; run per-item guided-completion memorisation probes **[LIT]**
  (golchin2023time; contamination must be measured per benchmark, sainz2023nlp) and exclude
  probe-positive items; map gold items to areas; label an area *missed* if it holds ≥ 1 important
  gold item the reconstruction lacks; score. Unmappable gold items count as missed areas at the
  pre-set floor score.
- **Materials.** Primary gold (suggested in the N3 plan): Sullivan et al. cricothyrotomy task list
  **[LIT]** (sullivan2014use). First fallback: Chao & Salvendy's troubleshooting data **[LIT]**
  (chao1994percentage). Further candidates: Crandall & Getchell-Reiter NICU cues (crandall1993critical;
  the itemised list's availability is unverified), PARI-based maintenance task lists (hall1995procedural;
  availability unverified). Leave-one-gold-out throughout.
- **Controls/baselines (all §14.3).** Random; naive type rule; verbalised confidence; area size / gold
  items per area; retrieval-support density; corpus frequency of area terms; **plain-LLM prompt**
  ("where would text omit expert knowledge?", run on the strongest available model of a family other
  than the generator); type prior with rates from the other golds.
- **Blinding.** Coders mapping gold items to areas see no P(missing), no origin, no model family
  (§14.3). The owner cannot be blind to the map and codes under origin blinding only.
- **Primary measure.** ΔAUROC against the strongest baseline, on the primary gold.
- **Secondary.** Recall by step type against the 44% unprompted-expert comparator (Wilson 95% roughly
  30–59%) and the 66% prompted level **[LIT]** (sullivan2014use); gold-residual hits per ranked
  question; probe-positive share.
- **Reliability plan.** All gold-item → area assignments and ≥ 20% of reconstruction–gold pairs
  double-coded; an LLM matcher is adopted only under the §18 rule, else humans code all pairs.
- **Sample size.** Fixed by the gold, not chosen. **[INT]** One gold gives about ±0.14–0.20 on
  ΔAUROC (table above), so the pre-registration must state (a) the minimum missed areas per gold,
  (b) the multiplicity rule (Holm) or a pooled random-effects ΔAUROC across golds, and (c) that a
  single-gold result wider than 2δ is reported as *inconclusive by design*, not as a stop.
- **Kill/continue.** The N3 rule (§22). Recall decides only whether reconstruction survives as a
  draft for experts to correct.
- **Cost/time.** Gold acquisition (library access, possibly author contact); ≈ 20–60 coder-hours per
  gold; API tens of dollars. 2–4 months including pre-registration.

### V3 — E-OSS: developer-departure natural experiment (no participants; coders only)

- **Hypothesis.** L2 in the organisational family (RQ-H): coverage computed only from artefacts dated
  ≤ t predicts where knowledge loss shows up after a truck-factor developer leaves, beyond authorship
  concentration.
- **Design.** As registered (§18 E-OSS). Freeze each repository at t before the departure; compute the
  gap map from artefacts ≤ t via a World B Git adapter (commits, blame at t, issues, PRs, review threads,
  dated docs); unit = code unit existing at t. Outcome: blind double-coded rationale-seeking issues and
  defect-fix commits per unit of post-t activity, as a difference-in-differences against the same
  units' pre-t rate. Departures happen at different dates, so use a staggered-adoption estimator
  **[LIT]** (callaway2021difference) for any pooled effect; the primary score is still unit-level
  ΔAUROC or rank-correlation gain.
- **Materials.** Departures from the truck-factor corpora **[LIT]** (avelino2016novel;
  avelino2019abandonment); turnover-loss replications as prior-trouble baselines **[LIT]**
  (rigby2016quantifying; nassif2017revisiting).
- **Controls/baselines.** Prior trouble, size, churn, doc-link/comment density, truck factor, KaR /
  abandoned-file share (covariate only, since it is defined by authorship), and a plain-LLM ranking.
- **Blinding.** Outcome coders see issue text with unit and repository pseudonymised, not the gap map.
- **Primary measure.** Gain of the gap map over the strongest baseline, clustered by repository
  (obuchowski1997nonparametric or a repository-level bootstrap).
- **Secondary.** Stratified by knowledge type; review-weighted concentration; pre- vs post-cutoff windows.
- **Reliability plan.** Two coders classify a stratified sample of ≥ 200 issues (rationale-seeking or not;
  defect-fix or not) to κ ≥ 0.70; then one coder with a 10% drift re-check every 200 items.
- **Sample size.** Units are many, repositories few, so the effective n is closer to the number of
  departures. **Proposed pilot: 5 departures** to estimate the post-t outcome base rate, the
  intra-repository correlation and coding time. **Decision rule:** compute the number of departures
  at which the clustered 90% half-width of ΔAUROC ≤ δ; run the main study only if that number is
  obtainable from the corpora with the minimum post-departure activity; otherwise pre-register E-OSS
  as descriptive and let V5 carry L2's organisational half.
- **Contamination.** Low-visibility repositories plus memorisation probes on post-t issue titles, or
  outcome windows after every model's cutoff (§18 E-OSS). Developers pseudonymised; legitimate-interest
  basis recorded.
- **Kill/continue.** Upper 90% bound of the gain below δ: stop H1 in the organisational family. The
  "change to H2" route (traces first) is readable only here (§22).
- **Cost/time.** Engineering for the Git adapter (weeks); 60–150 coder-hours; API tens to low hundreds
  of dollars. 3–5 months.

### V4 — Residual measurement known-truth check (N5; no participants)

- **Hypothesis.** L3 (RQ-D): the unseen-item estimate from text occasions matches the count of gold
  items that no text occasion captured.
- **Design.** First a labelled synthetic simulation with planted dependence (a known-truth use of
  synthetic data, not a criterion). Then on V2 gold: heterogeneity-robust capture–recapture over text
  occasions **[LIT]** (chao1987estimating; briand2000comprehensive), Chao1 as a lower bound, the gold
  as an independent occasion.
- **Primary measure.** |estimate − gold-as-occasion count| against the pre-set tolerance.
- **[INT]** Positive dependence (literature is written by experts) biases the estimate low
  (`REORIENTATION.md` §14.1), so a "stable" estimate proves nothing. The tolerance must be fixed first.
- **Kill/continue.** Out of tolerance: stop using the residual as an objective (falsifier part 2).
  This does not stop L4; V5 then reports observed counts only, never an estimated total.
- **Cost/time.** Days of analysis on V2 data; no new coding.

### V5 — Prospective expert elicitation, blind to predictions, with control areas (first human study)

Runs only if V2/V3 read *continue* or *inconclusive with a positive point estimate*. **[FW]**; proposed
here in detail, building on `REORIENTATION.md` §20 steps 2–3.

**V5a — Expert raters (minutes, before interviews).** §20 says the first human spend after a pass is
expert raters, not interviews. Design: 6–10 experts per domain rate each candidate gap ("practitioners
rely on knowledge here that these sources do not state": yes / partly / no), with **decoy candidates**
built from covered areas mixed in at a fixed ratio, blind to which is which (the decoy logic reuses
Track A's false-corroboration check, `research/experiment-ai-assisted-cta-physics.md`). Primary: rater
discrimination (AUROC of ratings, real vs decoy) and candidate precision with Wilson CI. **[INT]** This
measures content plausibility, not observed knowledge; it cannot pass L4 by itself, but it is cheap
and it filters the question set before V5b.

**V5b — The prospective study.**
- **Hypothesis.** L4: in a new domain, the gap-map score predicts which areas yield validated,
  expert-added items that are absent from text.
- **Design.** Within-expert, area-level, stratified random sampling of areas across the whole score
  range (not only the top), so ΔAUROC is estimable and inverse-probability weights are known.
  1. Choose 2 domains with public reconstruction material and reachable experts, one diagnostic
     (e.g. PLC fault diagnosis, already reconstructed) and one normative or procedural, and exclude
     introductory mechanics (Track A eligibility, §18.1).
  2. Freeze the reconstruction, the dated corpus, the gap map and the area partition; hash-commit.
  3. From the partition, sample areas into four labelled strata: top of the gap map (G), lowest
     retrieval density (D), top of a plain-LLM ranking "what would experts know that is not written
     here" (L), and uniform random (R), plus the §14.2 unknown-unknowns fraction of
     confident-but-unverified areas. Overlaps are resolved by the pre-registered sampling rule.
  4. Each expert is interviewed about a fixed set of about 10–12 areas (balanced across strata,
     order randomised). **The probe is the same for every area**: a neutral CDM-style script
     **[LIT]** (klein1989critical) — "Walk me through the last time you handled <area>. What did you
     notice? What did you check? What would a newcomer miss?" — never the gap map's own question.
     At most one follow-up per scripted probe, restating the expert's own words (the Track A rule).
  5. Each area is covered by 3 experts, so the area outcome is a small union-of-experts gold.
     **[LIT]** Chao & Salvendy found acquired procedural knowledge roughly doubled from one to six
     experts, with three the best cost–benefit point (chao1994percentage).
- **Participants.** Domain experts with at least several years of practice in the task scope,
  recruited outside any Track A pool. Interviewer: one trained human interviewer per domain (or the
  instrument's AI interviewer with the same script; a second arm is a separate question and not
  mixed in here). Coders: 2 blind coders plus 1 validator.
- **Outcome per area.** Validated expert-added items: expert utterances segmented into items
  (cue, decision rule, check, rationale, expectancy); an item counts if (a) it is absent from the
  frozen reconstruction and from the dated corpus under the V1 closure codebook and a fixed search
  protocol, and (b) it is corroborated by a second expert in the same area or by an artefact or trace.
  Importance: rated a week later by other experts blind to stratum (the Track A importance-rating rule).
  Area label *residual present* = at least one validated, important new item.
- **Controls/baselines.** Strata D, L and R (above); area size as a covariate; the strongest §14.3
  baseline recomputed on the prospective outcome.
- **Blinding.** Experts: not told that areas were chosen by a model or that strata exist. Interviewer:
  sees only area names in random order, never scores or candidate content. Coders: see segmented
  expert utterances with interviewer turns removed, area names pseudonymised, no stratum or score;
  a guess-the-stratum check on 20% of areas, guess rate reported (Track A's blinding check).
- **Primary measure.** Prospective ΔAUROC: gap-map score vs strongest baseline score, predicting
  *residual present*, clustered by expert and area (obuchowski1997nonparametric).
- **Secondary.** Rate ratio of validated important items per area, G vs the strongest of D, L, R
  (mixed-effects negative binomial with expert and area random effects **[LIT]**, bates2015fitting);
  precision of the map's candidate *content* (did experts say the predicted missing element?);
  reported-only and contradicted rates; Res_obs by knowledge type (§14.1); expert minutes per
  validated item; saturation by run length **[LIT]** (guest2020simple).
- **Reliability plan.** Segmentation: Krippendorff's α ≥ 0.80 target (0.667 tentative floor, below
  which the study pauses for codebook revision) on 25% of sessions; "new vs in-text" and "same item
  across experts": κ ≥ 0.70 each (Track A's thresholds); corroboration coder checks a list with
  decoy items and the false-corroboration rate is reported.
- **Sample size (no fake precision).** The hit rate per area and the expert-level clustering are
  unknown. **Pilot:** 6 experts × 12 areas in one domain (72 area-interviews, 24 areas × 3 experts).
  It estimates the base rate of *residual present*, the intra-expert correlation, coding time and
  blinding leakage. It is not analysed for effect. **Decision rule:** from the pilot, compute the
  number of areas giving a 90% ΔAUROC half-width ≤ δ; with 3 experts per area and 12 areas per
  expert, experts needed = areas / 4. Illustration only (not a plan): 40 missed and 40 not-missed
  areas give about ±0.10; that is 80 areas and 20 experts per domain. If the pilot implies more than
  the budget can buy, pre-register V5 as an estimation study (effect with CI, no gate) and say so.
- **Kill/continue.** Stop the H1 claim if the upper 90% bound of prospective ΔAUROC < δ. Continue to V6
  if the lower bound > 0 and the point estimate ≥ δ. Inconclusive: run the second domain once.
- **Cost/time.** Pilot: 6 expert-hours plus ≈ 30–50 coder-hours. Main (2 domains): ≈ 40 experts ×
  1–1.5 h, plus importance raters, plus ≈ 300–500 coder-hours (planning assumption: 3–4 coding hours
  per session-hour, including corroboration). Honoraria at local rates. 6–9 months including ethics.

### V6 — Targeted elicitation efficiency (L5a; the §17 central hypothesis)

- **Hypothesis.** Questions chosen by expected information gain from the gap map recover more
  validated items per expert hour than an untargeted CTA interview of equal length.
- **Precursor (no participants).** E-EIG (N6): recovery curves against held-out gold oracles for EIG,
  EIG without the reconstruction prior, partition sampling, plain-LLM lists, expert-written lists
  and random (`REORIENTATION.md` §18). Gate: EIG beats random and plain-LLM lists.
- **Design.** Between-area, within-expert crossover: each expert gives two equal-time blocks on
  different, matched area sets; block A uses the gap map's ranked questions, block B a standard
  unprompted-then-CDM interview; order and area sets counterbalanced. Proposed third arm: plain-LLM
  question list. In the H3 branch (L2 failed), arm A is EIG without the reconstruction prior.
- **Leading-question control.** Targeted questions presuppose content, which can plant it
  **[LIT]** (loftus1975leading). Items whose content first appears in the question are coded
  *question-seeded* and count in the primary outcome only if corroborated by a trace, artefact or
  a second expert who was not asked that question. The instrument's leading-question guard and turn
  contract are reused.
- **Primary measure.** Validated important new items per expert hour, ratio A/B, with a
  pre-registered SESOI (proposed here: a 1.25× ratio, i.e. 25% more yield per hour; our choice,
  to fix before data). Equivalence-style reading as in V2.
- **Participants.** Set from the V5 pilot variance; illustration only: 20–30 experts per domain.
  Coders as in V5.
- **Kill/continue.** Upper 90% bound of the ratio below the SESOI: stop the efficiency claim.
- **Cost/time.** Similar to V5 main; 6 months. **[INT]** V5 and V6 can share recruitment and
  coding infrastructure but not the same areas for the same expert, or the V5 blind breaks.

### V7 — Organisational pilot (L5b)

- **Hypothesis.** In one partner organisation, predicted gaps in critical units coincide with (a) what
  staff add in blind interviews and (b) where departures or onboarding produced trouble.
- **Design.** Artefact-coverage mode only, pseudonymised concentration, no evaluation use of outputs,
  DPIA, and a works agreement where German co-determination applies (§20 step 6; §21). Two parts:
  (1) retrospective, E-OSS inside the partner: past departures or onboarding tickets as the outcome,
  artefacts ≤ t as input; (2) prospective, V5b's design on 1–2 critical units at small scale.
- **Participants.** 1 partner; 6–12 staff experts; 2 coders with partner confidentiality terms.
- **Primary measure.** Descriptive with CIs: hit rate of G vs D and R areas; retrospective ΔAUROC if
  enough departures exist. **[INT]** One partner cannot validate a predictor; the pilot tests
  feasibility, legal viability and whether the organisational outcome can be measured at all.
- **Secondary.** Expert minutes per validated item; share of predicted gaps that the partner already
  knew (a usefulness signal, never a validity criterion).
- **Kill/continue.** Stop if the DPIA or works council blocks the design, or if the outcome cannot be
  measured from the partner's records. Continue to a multi-partner study only if G beats D and R
  in both parts.
- **Prerequisite.** V0's N2 validation (E-PLANT, E-ABST) read out, because a partner's documents
  raise the prompt-injection and false-support stakes (§16 R11).
- **Cost/time.** 4–8 months, dominated by legal and data-access work.

### V8 — Learner-side link (L5c) and how Track A fits

**V8a — Public learner data (no participants; N4 extension).** For mathematics, test whether
KC areas that the gap map flags carry higher error rates or misconception prevalence than covered
KCs, beyond the dataset's KC-model difficulty (AFM/LFA baselines **[LIT]**, cen2006learning) and
beyond the N4 baselines (E-KC, E-DIST, E-MISC). **[INT]** The gap map reads expert-voiced text, so a
null here is informative: expert residual and learner difficulty may be different things. The PoC
makes no learner-difficulty claim (`research/n3/README.md`).

**V8b — Track A, unchanged.** Track A's registered design runs on its own preconditions: Stage A with
12 physicists (extendable to 16), K1 (≥ 3 performed, shared, absent operations; ≥ 2 AI-probe-added;
contradicted-rate CI bound ≤ 15 pp), K0 (≥ 30% principle-selection or representation errors among
about 100 coded errors), Stage B two-arm RCT with about 370 students, delayed transfer, SESOI
d = 0.30, K2 valid only with ≥ 70% compliance per arm (`research/experiment-ai-assisted-cta-physics.md`;
`CLAUDE.md`). The validation programme touches it only through E-SEAL (§18.1): predictions generated
by script into an encrypted, hash-committed file before Stage A, unsealed after K1 adjudication is
locked, matched by coders with no Track A role, secondary and non-gating. **Proposed here, to be
pre-registered before Stage A if the owner approves:** add the sealed gap-map *scores* for the Stage A
problems' operations, so that after unsealing, Stage A's validated operations serve as a fresh,
post-cutoff gold for a secondary ΔAUROC, and K0 error codes can be tabulated against flagged vs
unflagged operations. **[INT]** This is the only place in the programme where expert residual,
learner error and a learning RCT meet in one topic, and it cannot change what K0, K1 or K2 decide.
Anyone who has seen reconstructed conservation content stays ineligible for any Track A human role.

**V8c — Novice performance in a V5 domain (LATER).** 30–60 novices (apprentices, new hires) perform
tasks covering V5 areas; errors and time per area are coded blind. Hypothesis: V5-confirmed residual
areas show more novice errors than covered areas at matched difficulty. Sample size from a pilot of
10 novices (error base rate per area and between-person variance), with the same decision-rule logic
as V5.

**V8d — Instructional effect (MUCH LATER).** Teaching confirmed residual items vs matched control
material, delayed transfer. Use Track A Stage B as the registered template (ITT, SESOI, compliance
rule, delayed test); a CTA-derived vs expert-authored contrast has precedent **[LIT]**
(feldon2010translating), and field effects in education are usually small **[LIT]** (kraft2020interpreting).
Outside physics this is a new study with its own registration; nothing in Track A's rules moves.

---

## 3. Order, gates and dependencies

```
V0 freeze + admissibility ──► V1 closure set ──► V2 E-CTA ─┐
            │                                    V3 E-OSS ─┼─► N3 programme gate (§22)
            └─(N2 deferred validation)──► gates V7 only    V4 residual check (from V2 data)
N3 continue ─► V5a raters ─► V5b pilot ─► V5b main ─► V6 efficiency ─► V7 org pilot ─► V8c/V8d
N3 stop     ─► H3 pivot: V6 run as "EIG without reconstruction prior", V5 not run in H1 form
Track A (own preconditions) ─► E-SEAL secondary comparisons (V8b), non-gating
V8a runs any time after V0 (public data)
```

---

## 4. Threats to validity for the programme, and mitigations

| Threat | Where it bites | Mitigation |
|---|---|---|
| **Memorisation / contamination** | V2 (1993–2014 golds are in pretraining; content diffused into textbooks) | Corpus frozen at gold date; per-item guided-completion probes, probe-positive items excluded (golchin2023time; sainz2023nlp); open-weight models with documented cutoffs; recall reported as an upper bound (§18.2). V3 and V5 are the contamination-free legs: post-cutoff windows and fresh elicitation. Track A (V8b) gives a post-cutoff gold |
| **Gold incompleteness** | V2, V5 (a gold lists what a few experts said; items outside it look like false positives) | Union-of-experts gold (3 per area in V5, chao1994percentage); report R∖H separately and never as error; never declare the residual zero (§14.1 pitfall 7); saturation run-length checks (guest2020simple; hennink2022sample: 9–17 interviews in homogeneous samples) |
| **In-sample tuning** | All (lexicons tuned on the three PoC ledgers) | Hash-freeze config before any gold; leave-one-gold-out and leave-one-domain-out; V1 includes a new domain |
| **Coder drift** | V1–V5 | Frozen codebook with anchors; κ/α on a double-coded start sample; 10% re-check every 200 items, re-training if κ drops below 0.70; drift plotted over time |
| **Coder knowledge of the map** | V2, V5 (owner built the map) | Origin blinding; a non-owner second coder for gating analyses; guess-the-stratum check |
| **Judge becomes the gold** | V1, V2 | LLM judges only as matchers after the §18 adoption rule, from a different family; never a criterion |
| **Expert fatigue** | V5, V6 | ≤ 75-minute sessions, ≤ 12 areas, randomised area order so fatigue spreads evenly across strata; order entered as a covariate |
| **Interviewer effects** | V5, V6 | One fixed script; interviewer blind to strata; follow-up rule; interviewer as a random effect; with one interviewer the claim is "vs this interviewer" (Track A wording) |
| **Leading questions / planted content** | V6 most, V5 some | Neutral area-generic probes in V5; *question-seeded* coding in V6 counted only with independent corroboration (loftus1975leading) |
| **Reactivity of verbal reports** | V5, V8c | Directed "explain" prompts can change performance; non-directed think-aloud does not (fox2011procedures; ericsson1980verbal). Use retrospective CDM probes after the task, not during it |
| **Reported-but-not-performed knowledge** | V5, V6 | Corroboration by second expert or trace; report reported-only and contradicted rates (Track A outcome 2) |
| **Domain selection bias** | V2–V5 (text-rich domains flatter reconstruction, §16 R3) | Spread text-richness on purpose (§19); include one text-poor domain once a gold exists (PARI list, hall1995procedural); claim nothing general before it passes (RQ-I) |
| **Baseline selection after the fact** | V2, V3, V5 | Baselines fixed in advance; min-over-baselines ΔAUROC computed inside each bootstrap resample |
| **Clustering ignored** | V3, V5 | Clustered ROC (obuchowski1997nonparametric) or cluster bootstrap; mixed models with expert and area random effects |
| **Underpowered golds read as nulls** | V2 | "Inconclusive by design" rule when the CI is wider than 2δ; pooled random-effects ΔAUROC; decisions carried by V3/V5 |
| **Synthetic leakage into conclusions** | All | Label rule in code; synthetic outputs only as predictors (§12, R6) |
| **Authorship metrics after agentic coding** | V3 | Pre-agent histories; review-weighted concentration (§16 R8) |
| **Legal and ethical blockers** | V5, V7 | Ethics approval before V5; DPIA and works agreement before V7; artefact-coverage mode; no evaluation of individuals (§21) |

---

## 5. One-page summary table

| Stage | Link | Humans | Primary measure | Continue if | Stop / change if | Order of cost & time |
|---|---|---|---|---|---|---|
| V0 Freeze, admissibility, N2 deferred | L0 | 1 coder (E-ABST) | N2 gate readings; admissibility | Hash committed; runs admissible | N2 Stop → no V7; no hash → no gold | Tens of $ API; 1–2 months |
| V1 Closure set | L1 | 2–3 coders | Judge–human κ; own–control gap | κ ≥ 0.70 and ≥ human lower bound; gap within ±0.10 | Human coding of closure, or drop closure feature | ≈ 20 h/coder; 1 month |
| V2 E-CTA | L2 | 2 coders | ΔAUROC vs strongest baseline | Lower 90% > 0 and point ≥ δ | Upper 90% < δ → H3; wide CI → inconclusive by design | 20–60 h/gold; 2–4 months |
| V3 E-OSS | L2 (org) | 2 coders | Clustered ΔAUROC / rank gain | Same rule | Same rule; H2 route only here | 60–150 h; 3–5 months |
| V4 Residual check | L3 | none | Estimate vs gold-as-occasion | Within tolerance | Drop residual as objective | Days |
| V5a Expert raters | (pre-L4) | 6–10 experts/domain | Real-vs-decoy AUROC of ratings | Discrimination above chance | Revise candidate generation | Expert minutes; 1 month |
| V5b Prospective elicitation | L4 | Pilot 6 experts; main ≈ 20/domain (set by pilot) | Prospective ΔAUROC | Lower 90% > 0 and point ≥ δ | Upper 90% < δ → stop H1 claim | Pilot ≈ 40 h; main 6–9 months |
| V6 Targeted efficiency | L5a | 20–30 experts/domain (set by V5 variance) | Validated items per expert hour, A/B | Lower bound > 1 and point ≥ SESOI | Upper bound < SESOI | ≈ 6 months |
| V7 Org pilot | L5b | 1 partner, 6–12 staff | Hit rate G vs D/R; feasibility | G > D and R in both parts | Legal block; unmeasurable outcome | 4–8 months |
| V8a Public learner data | L5c | none | Flagged-KC error excess over AFM baselines | Excess with CI > 0 | Null → expert residual ≠ learner difficulty | Weeks |
| V8b Track A (unchanged) | L5c | Track A's own (12 experts; ≈ 370 students) | Registered K0/K1/K2; E-SEAL secondary | Registered rules only | Registered rules only | Track A's own schedule |
| V8c/d Novices; instruction | L5c | 30–60 novices; RCT sized like Stage B | Error excess; delayed transfer | Excess; effect ≥ SESOI | Null; K2-style futility | LATER / MUCH LATER |

---

## 6. Figure description (one figure)

**Title:** "Ladder of evidence: from gap candidates to validated predictions."

A vertical ladder, read bottom to top, with six rungs. Each rung is a box with the study IDs, the
claim it establishes, and the human input it needs (icon: none / coder / expert / learner). Between
rungs sits a diamond gate with its rule in a few words.

1. Bottom (ground, shaded grey, labelled "PoC today"): "Gap candidates. Closure uninformative
   (own = control: 0.89, 0.96, 0.96). Precision 3/19 strict (reported)."
2. Rung 1 — V0 + V1, "Trustworthy inputs and an informative closure step" (coder icon). Gate:
   "κ ≥ 0.70; config hash-frozen."
3. Rung 2 — V2 + V3 (+ V4 beside it as a side box), "Beats the strongest baseline on retrospective
   public gold" (coder icon). Gate diamond: "ΔAUROC ≥ δ?" with three exits: up (continue), a
   horizontal arrow to a side box "H3 pivot: EIG without reconstruction prior → V6", and a loop
   "inconclusive → one fallback gold".
4. Rung 3 — V5a + V5b, "Predicts what fresh experts add, blind" (expert icon). Gate: "prospective
   ΔAUROC ≥ δ".
5. Rung 4 — V6, "Saves expert time" (expert icon). Gate: "items per hour ≥ SESOI".
6. Rung 5 — V7 and V8a/c side by side, "Transfers to organisations; links to learner difficulty"
   (partner and learner icons).
7. Top — V8d, "Improves learning" (learner icon), with a dashed line to a separate rail on the right.

A separate vertical rail on the right, labelled "Validation Track A (frozen; own preconditions)",
shows Stage A → K1 → K0 → Stage B → K2, connected to the ladder only by a dashed, one-way arrow
"E-SEAL: sealed predictions, secondary, non-gating". Width of each rung grows upward to show rising
cost; a small side scale reads "coder-hours → expert-hours → learner cohorts".

---

## 7. Findings that matter most (for the orchestrator)

1. **[INT]** The closure step must be validated before the gold test (V1). Without it, E-CTA tests
   density plus lens firing, and a stop result would be a closure artefact, not a verdict on RQ-B.
2. **[INT, computed]** A single CTA gold cannot resolve a realistic δ: 20 areas per class give a 90%
   ΔAUROC half-width of about ±0.14; δ = 0.05 needs about 150 per class. E-OSS and the prospective
   study must carry the decision; E-CTA needs an "inconclusive by design" rule.
3. **[INT]** "Strongest baseline" must be chosen inside the bootstrap, or the headline comparison is
   biased by selection.
4. **[FW]** The prospective study (V5b) uses neutral area-generic probes, strata G/D/L/R, three
   experts per area, and blinding of experts, interviewer and coders. Its size comes from a
   6-expert pilot and a stated decision rule, not from an assumed effect.
5. **[INT]** Track A can supply the only post-cutoff, trace-corroborated gold in the programme via
   E-SEAL, if sealed gap-map scores are added and pre-registered before Stage A, secondary and
   non-gating.
6. **[POC, unverified]** The 3/19 precision figure has no committed per-record tally; the report
   should cite it as reported, or the tally should be committed.

---

## 8. Citation verification lines

All verified 2026-09-29 via OpenAlex `resolve_references` (DOI exact match) unless stated.
"Claim check" says what was read to support the specific use in this note.

- sullivan2014use — W1984195792, DOI 10.1097/acm.0000000000000224 resolves; claim check: abstract read (46-step gold; 44% (20/46) unprompted, 66% (31/46) prompted; 3 + 3 surgeons).
- chao1994percentage — W2046788628, DOI 10.1080/10447319409526093; claim check: abstract read (knowledge roughly doubled from 1 to 6 experts; 3 experts optimal cost–benefit).
- crandall1993critical — W2014940456, DOI 10.1097/00012272-199309000-00006; title-level only (the 25/70 cue figure is not used here; itemised-list availability unverified).
- klein1989critical — W2080862045, DOI 10.1109/21.31053; title-level (CDM as the probe method).
- hall1995procedural — W15311681, DOI 10.21236/ada303654 (PARI procedural guide); title-level.
- hoffman1995eliciting — W1973007630, DOI 10.1006/obhd.1995.1039; title-level only (no abstract in OpenAlex). Not used for any number. Candidate background citation for "elicitation methods have been compared".
- burton1990efficacy — W2046702042, DOI 10.1016/s1042-8143(05)80010-x; title-level only. Same use as above.
- fox2011procedures — W2077979711, DOI 10.1037/a0021663; claim check: abstract read (directed verbalisation changes performance; think-aloud does not). OpenAlex lists 2010 (online); print Psychol Bull 137(2), 2011.
- ericsson1980verbal — W2041656211, DOI 10.1037/0033-295x.87.3.215; title-level.
- loftus1975leading — W2141606903, DOI 10.1016/0010-0285(75)90023-7; title-level (leading questions alter reports).
- krippendorff2004reliability — W2012378416, DOI 10.1111/j.1468-2958.2004.tb00738.x; claim check: full text (UPenn repository copy) p. 241 citation: require α ≥ .800, ≥ .667 for tentative conclusions.
- hayes2007answering — W2061504941, DOI 10.1080/19312450709336664; title-level (α as a standard reliability measure).
- landis1977measurement — W2164777277, DOI 10.2307/2529310; title-level.
- feinstein1990high — W1983897914, DOI 10.1016/0895-4356(90)90158-l; title-level (high agreement, low κ paradox).
- hanley1982meaning — W2157825442, DOI 10.1148/radiology.143.1.7063747; used for the planning SE formula (recomputed here).
- delong1988comparing — W2328176404, DOI 10.2307/2531595; claim check: abstract read (comparing correlated ROC areas).
- obuchowski1997nonparametric — W2066063421, DOI 10.2307/2533958; claim check: abstract read (extends DeLong to clustered data; independence-assuming tests are inflated). A first DOI guess for this paper resolved to a different Biometrics article; use only the DOI above.
- schuirmann1987comparison — W2037698344, DOI 10.1007/bf01068419; title-level (TOST).
- lakens2017equivalence — W2610765860, DOI 10.1177/1948550617697177; claim check: abstract read (equivalence bounds from the SESOI; TOST).
- lakens2018equivalence — W2788930055, DOI 10.1177/2515245918770963; title-level.
- nosek2018preregistration — W2779812635, DOI 10.1073/pnas.1708274114; title-level.
- callaway2021difference — W3113269512, DOI 10.1016/j.jeconom.2020.12.001; J. Econometrics 225(2):200–230 (OpenAlex year 2020 = online; issue 2021). Title-level.
- avelino2016novel — W2344103814, DOI 10.1109/icpc.2016.7503718; title-level.
- avelino2019abandonment — W2981180236, DOI 10.1109/esem.2019.8870181; abstract read (core-developer loss and project survival).
- rigby2016quantifying — W2360973814, DOI 10.1145/2884781.2884851; abstract read (turnover-induced loss in Chromium and an Avaya project).
- nassif2017revisiting — W2767247175, DOI 10.1109/icsme.2017.64; abstract read (replication on Chromium plus seven projects).
- golchin2023time — W4385965989, arXiv 2308.08493 (DOI 10.48550/arxiv.2308.08493); abstract read (guided-instruction completion flags contaminated instances).
- sainz2023nlp — W4389518953, DOI 10.18653/v1/2023.findings-emnlp.722; title-level.
- guest2006how — W2129660502, DOI 10.1177/1525822x05279903; abstract read (60 interviews; saturation study). Field Methods 18(1):59–82 (print 2006; OpenAlex year 2005 = online). Bib page ranges trimmed to first page where Crossref and OpenAlex give only the first page.
- guest2020simple — W3023639742, DOI 10.1371/journal.pone.0232076; title-level (run-length saturation method).
- hennink2022sample — W3208645186, DOI 10.1016/j.socscimed.2021.114523; abstract read (saturation within 9–17 interviews in empirical studies). Soc Sci Med 292 (2022; OpenAlex year 2021 = online).
- chao1987estimating — W2041457600, DOI 10.2307/2531532; title-level.
- briand2000comprehensive — W2165921013, DOI 10.1109/32.852741; title-level.
- bates2015fitting — W1951724000, DOI 10.18637/jss.v067.i01; title-level.
- wilson1927probable — W2020018978, DOI 10.1080/01621459.1927.10502953; title-level.
- cen2006learning — W1562092080, DOI 10.1007/11774303_17; title-level (LFA/AFM).
- feldon2010translating — W2129373075, DOI 10.1002/tea.20382; title-level.
- kraft2020interpreting — W2968077443, DOI 10.3102/0013189x20912798; title-level.

Not used (could not verify): Efron & Tibshirani bootstrap book (no OpenAlex match); Clark et al. 2008
CTA handbook chapter (no OpenAlex match; REORIENTATION cites a web copy only); Hoffman & Lintern 2006
Cambridge Handbook chapter (no match); ForecastBench (no OpenAlex match under that title).
