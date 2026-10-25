# Deep-search queue: needs study before anything is built (2026-10-24)

This queue merges three passes: [C] Claude, [X] Codex and [R2] an adversarial second round (see [coverage-audit.md](coverage-audit.md); finding numbers refer to it). Items are ordered by what each unblocks on the critical path, strongest first.

**Rules for every search:**
- **Gold contents stay unseen.** Gold availability is checked by metadata and author contact only: existence, format, item count, date and licence (§14.3). Nothing from a gold enters the repo before the pre-registration is hash-committed.
- **Track A eligibility.** Anyone who reads reconstructed conservation content becomes ineligible for any Track A human role (§18.1).
- **Output.** Each search ends in a note in `research/`, and `citation-verifier` runs on it. Use the `research` skill for one question, `deep-research` for a synthesis.

## Tier 1: unblocks MS1, MS2 and the gold test

### DS1. Which CTA golds are itemised and obtainable? (recommended first) [C+X+R2]
- **Status 2026-10-24:** 0 golds confirmed eligible and 17 provisional, pending only whether the list is printed (C4). RQ-I is not testable NOW. The owner decision on MS3 is due. Note: `research/ds1-gold-availability.md`. Commit `87d5a5e`.
- **Owner decision 2026-10-24:** fix a provisional MS2 list now; the enquiries were not chosen. Primary set: ranks 2–4 (Okoli 2020, Madani 2015, Logishetty 2019). Sullivan 2014 is out as a test gold, because the type feature was derived from it, and stays as the descriptive recall comparator. Fallbacks: ranks 5–17 in order (`REORIENTATION.md` §22 threshold table). A gold whose list proves unavailable falls to the next rank, and that domain's one-shot reconstruction is spent.
- **Candidates** (as queued; superseded by DS1's ranks, where Sullivan is itemised but not confirmed obtainable, and Crandall, Chao and PARI are unknown). Sullivan 2014 [1], Chao & Salvendy 1994 [2], Crandall & Getchell-Reiter 1993 (70 cues) [4], the PARI aircraft-maintenance study [106], and the studies in [3] (Velmahos, Schaafstal, …).
- **Done when.** A register built from metadata only gives, for each candidate: itemised or not, item count, number of experts, date, access route, licence and fallback rank. It also says whether a text-poor test (RQ-I) is feasible.
- **Unblocks.** The MS2 list of eligible golds (V2 needs at least 3; `report/sections/17_validation.tex:239-246`), the type-prior baseline (it needs at least 2 golds up front) and DS4.
- **Why first.** Nothing in the repo can substitute for it, author contact takes time, and if only Sullivan is confirmed it kills MS3 (`26_risks.tex:51-59`). **What would change it:** the owner already holding confirmed access to 3 or more itemised golds. Then DS2 leads.

### DS2. Codebook anchors and κ benchmarks for "stated / partial / unstated" [C+X, narrowed by R2]
- **Status 2026-10-24: done; continue to I4.** κ 0.70 is reachable on a binary split: 10 comparable published values have a median of 0.725 (7 of 10 ≥ 0.70), and the binary ones 0.75 (5 of 6). The one scheme with a partial class reaches α 0.62. Recommendations:
  - Gate MS1 on closed vs not closed at κ ≥ 0.70, read on the point estimate.
  - Report the three-state agreement, but do not gate on it.
  - Define partial as a component count.
  - Compute seed vs independent support from metadata.

  No owner decision is due on the floor. Note `research/ds2-closure-codebook.md`; commit 9c65b09; citation-verifier passed.
- **Question.** What annotation constructs separate seed support from independent support, partial from full statement, and retrieval failure from absence? Candidates: unanswerability (SQuAD 2.0-style), NLI "not entailed", evidence sufficiency. What κ do comparable annotation tasks reach?
- **Scope.** Control design is now I1's job, in code.
- **Unblocks.** The V1 codebook (I4.1) and a realistic κ floor.

### DS3. Can N3 give a decisive reading at a meaningful δ? [C+X]
- **Question.**
  - Where does the report's δ = 0.05 come from?
  - What precedents exist for a ΔAUROC smallest effect of interest?
  - Which method fits paired, clustered AUROC: DeLong, Obuchowski, or a cluster bootstrap?
  - How should results pool across golds of about 20 areas, given imbalance, ties and strongest-baseline selection?
  - How should unmappable gold items be treated?
- **Done when.** δ, minimum areas, multiplicity and fallback order each have a sourced value, ready for I5 and `methods-critic`.
- **Status 2026-10-24: done.** N3 can Continue but cannot reliably Stop at δ ≤ 0.10 on CTA golds. The note proposes δ = 0.10, intersection–union and Bonferroni across baselines, common-effect pooling, c = 1.85 at both looks, and a strict floor. The report's bootstrap-minimum rule over-stops when baselines are close (55% against Bonferroni's 3% with 8 equally close baselines). Note `research/ds3-decisive-delta.md`; commit 1343d86.
- **Owner decision 2026-10-24:** δ = 0.10 (`REORIENTATION.md` §22). The fallback order is set provisionally from DS1, not from DS3's §6 order. The other proposed rows are not yet decided.

### DS4. Identifiability of the residual under zero text catchability (moved up by R2: R4 is fatal-class) [X]
- **Status (2026-10-24).** Done. The residual cannot be identified from text occasions, by an impossibility result: zero-catchability items leave the data unchanged. Text gives only a lower bound on the written universe. The residual needs the gold, under an untestable independence assumption. The N5/R4 rule cannot discriminate as written. The note fixes I3's grid and raises R4 to the owner. Note: [`research/ds4-identifiability.md`](../../research/ds4-identifiability.md); branch `ds4-identifiability`; citation-verifier passed.
- **Question.** What can capture–recapture identify when some items have zero catchability on every text occasion? Is the estimand the written unseen items or the human residual? Which estimators, bounds and stress regimes apply? An impossibility result is acceptable.
- **Done when.** A note fixes I3's simulation grid.

### DS5. Pre-gold full-text access and memorisation controls [C+X, refocused by R2]
- **Status 2026-10-24: done.** Free-to-read pre-gold works per domain query range from 4 to 5,457. Phillips 1998, Phillips 2001 and Grover TAR fall below a proposed screen of 100. Same-team precursors move 5 golds' cut-offs earlier, among them Okoli's to 2015. A blocklist spec, a decoy-calibrated probe protocol and a shortlist of documented-cutoff models feed I10 and the §22 model blank. Note `research/ds5-pregold-fulltext.md`; commit d262b24; citation-verifier passed.
- **Question.**
  - For each eligible gold, which pre-gold print and scholarly full text can be obtained legally (OpenAlex OA links, institutional access, publisher TDM terms), and how much of it is there?
  - Where does Wayback matter (post-1996 golds, e.g. Sullivan)?
  - Which DOI, title and citation blocking applies?
  - What is current practice for per-item guided-completion probes [151], and what is its false-positive control?
  - Which open-weight models have documented cutoffs (as of Oct 2026)?
- **Done when.** There is a full-text count per gold domain, a proposed corpus floor and a model shortlist. This feeds I10 and §18.2 (R2).

### DS6. Independent verifier and decoy validity; a reachable robustness contrast [X]
- **Status 2026-10-24: done; owner decided 2026-10-24.**
  - **Owner decision 2026-10-24: stage E-PLANT-2.** Verifier-validity coding first (human, $0), then I5's reachability check, then a 24-target calibration pilot of the ungated arm (with its top-tier parallel arm and a `key_headroom.py` estimate). Register only if the pilot gives a_u ≥ 10/24 and I5 shows Continue is reachable.
  - **The floor miss.** ClashEval's >60% is GPT-4o's rate. Claude models adopt 31–40% with one document, and Opus 24% with five. N2's 5/24 under 18 documents is in line with that. The old design had P(floor) = 0.11 and McNemar power ≤ 0.33 at its own baseline [SYNTHETIC].
  - **Decoys.** `decoy_is_valid` excludes 0 of the 40 committed decoys, and about 6 of the 10 accepted ones have debatable falsity (one AI reader).
  - **The note proposes:**
    - a decoy rubric judged by blind human coders;
    - a 125 + 50 verifier-validity sample;
    - an 8-code error taxonomy;
    - E-PLANT-2: weak-prior targets, 2:1 planted evidence, a calibration pilot and an unplanted-control specificity check, with thresholds for I5.
  - The old registration stays INCONCLUSIVE.
  - **Flag for the E-PLANT-2 design (post-merge citation check, 2026-10-24).** With p held fixed, a one-sided 95% upper bound ≤ 15% at a true 10% needs n ≥ 139, not 124, so the proposed 125 SUPPORTS misses that target (upper bound 15.3%); it still meets the ≤ 20% gate bound at a true 12% (n ≥ 68).
  - Note: `research/ds6-verifier-validity.md`; branch `ds6-verifier-validity`. The citation-verifier passed on its second pass.
- **Question.** How can decoy falsity and verifier validity be established independently of the pipeline? Today decoy validity checks only that the wording changed and a rationale exists (`reconstruct/src/reconstruct/evidence.py:593-598`). What N2 contrast has a reachable best case, given that the registered one cannot Continue?
- **Done when.** There is a validity rubric, a natural-error taxonomy and a proposed contrast whose thresholds I5 computes. The old registration stays INCONCLUSIVE.

### DS7. Public boundary sources that would revive dead features [C]
- **Question.** For each gold domain, which public practice texts exist (forums, Q&A, M&M write-ups, NTSB and FAA service-difficulty reports, postmortems)? Give each one's access route, date coverage and `Source.kind`. `n_boundary_sources` is 0 everywhere today.
- **Status (2026-10-24).** Done: boundary sources that predate the gold exist for Okoli, Madani and Logishetty, and they map to existing kinds with no new field. But 0 of 108 URLs the committed runs recorded is a forum or incident host, so host rules alone revive nothing, and no public text is a `DONE` record, so `has_done_support` stays dead. Recommended: the E-CTA primary test covers size, density, type and the lens signal only; `n_boundary_sources` and `imagined_only` enter as secondary only after a pre-freeze retrieval probe. That decision is the owner's. Note: `research/ds7-boundary-sources.md`; branch `ds7-boundary-sources`.
- **Owner decision 2026-10-24.** The E-CTA primary test covers size, density, type and the lens signal only; `has_done_support` is dead for public text. `n_boundary_sources` and `imagined_only` are pre-registered as secondary, and count only if a retrieval probe run before the freeze, without the gold, shows them taking at least 2 values across areas in the gold's domain (threshold fixed before the probe).

## Tier 2: the parallel experiments

### DS8. OSS outcomes and departure corpora [C+X]
- **Status 2026-10-24: done.** The Avelino 2019 register (CC-BY-4.0) gives 315 projects with a dated pre-2023 truck-factor departure, all in popular repositories, so option (a) needs a new low-visibility scan. SYNTHETIC power: about 600 leaver-owned units (30 × 20) stop a null map (P 0.87–0.95, Bonferroni over 6); Continue needs near-Poisson period noise at ≥ 10 corrective commits per unit per window (P 0.90), else ≤ 0.34. Proposes a pre-*t* dispersion go/no-go, the "dominate" rule and the World B adapter needs. Note `research/ds8-oss-departures.md`; commit b465a90; citation-verifier passed.
- **Question.**
  - Which post-departure outcomes measure knowledge loss rather than ordinary churn?
  - Can the 1,932-project corpus [112] and Chromium+7 [111] be obtained?
  - What are the base rates and variance of the outcomes?
  - How many departures predate agentic coding (R8)?
  - Which confounders matter, and which review-weighted baselines exist?
  - What text-vs-trace arms would test H2?

  This feeds E-OSS and E-DVP power, "dominate" for H2, and the World B adapter.

### DS9. Licensed learner data for N4, N7, H4 and H6 [C+X]
- **Datasets.** Eedi / NeurIPS 2020, Kaggle Eedi, DataShop, ASSISTments, AAAS, FCI on PhysPort, MaintIE / MaintNet, O*NET, the Stack Exchange dump (evaluation use) and NAEP released statistics.
- **For each:** licence and NC/ND status, schemas, whether an expert or default KC model exists, leakage-safe splits, and an E-KC ΔRMSE margin.

### DS10. EIG for expert elicitation (N6, H1 vs H3) [C+X]
- **Question.** Drawing on LLM-based EIG and Bayesian experimental design [147][148][175], what objective, question cost, oracle-response model and matching rule make "with vs without the reconstruction prior" meaningful? What does a deterministic oracle fail to establish about real interviews?

### DS11. A public SOP-plus-execution-log pair [C]
- **Sources.** BPI Challenge logs and other process-mining benchmarks with a reference model.
- **Uses.** E-DVP outside OSS, Safety-II's imagined-vs-done, and H2 where traces exist.

### DS12. Surrogate difficulty ranking (N7, T2) [X]
- **Question.** Which population, spread and stability criteria, and which text-regressor and direct-prompt baselines, would license use 5 without implying individual realism? Prevalence, effect-size and power claims stay banned (`REORIENTATION.md:359`).

## Tier 3: deferred until an experiment needs it (the §9 rule)

| ID | Topic | Trigger |
|---|---|---|
| DS13 | §10.2 objects: cue as discrimination, bottleneck hypothesis (ECD KSAs), crosswalk, GRADE-style certainty | A pre-registration needs a field N1 cannot express. That means a re-freeze |
| DS14 | Cooke, Prelec "surprisingly popular", learnersourcing, ENA, KST, conformal factuality, requirements elicitation, job analysis/EPAs, knowledge hiding | Expert raters (§20 step 2), learnersourcing, or a human-labelled calibration set exists |
| DS15 | E-NOV (expert–novice categorisation data) and E-HOLD (post-cutoff CTA or misconception papers) | N3 continues, or E-HOLD's window is non-empty |
| DS16 | Track A's 4 literature gaps (`PROGRESS.md`) | Any time. Read-only; cannot change a registered rule |
| DS17 | EUR-Lex check of Regulation (EU) 2026/1744 and the Annex III dates; incumbent scan (R9) | Before any organisational pilot or commercial text |
