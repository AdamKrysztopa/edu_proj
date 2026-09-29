# Review fixes: independent review of the Main Research Report

Scope: the findings of the independent adversarial review of the Main Research Report, plus the JEV
spike. Every finding was checked against the committed artefacts, the code and the primary sources
before anything changed. Three checks ran first: a repository evidence audit, a statistics and methods
review, and a literature audit. After the fixes, a separate adversarial review (final row) looked for
remaining defects.
Audited commit and release: see the title page of either PDF and `research/results_manifest.json`.

The report is not declared validated. The review findings have been addressed, and the report has been
made consistent with the frozen repository artefacts.

| # | Review finding | Verification | Change made | File / section | Status |
|---|---|---|---|---|---|
| 1 | GDPR-v2 "Located = 351" should be 366 | **Refuted as an error.** `sidecar.json stats.n_located` = 351 counts claims with at least one span. The ledger holds 366 evidence spans (a claim can have several). PLC 337/337 and GDPR v1 204/206 follow the same split, and 909 = 337 + 206 + 366 spans is correct. | Added an "Evidence" column beside "Located" and defined both in the caption, so the two units cannot be confused. No number changed. | Main §6.1 Table 4; manifest `n2.*.n_located`, `n2.*.evidence_items` | Fixed (clarified) |
| 2 | Lexical closure: README says PLC 42 vs [33,47], report says 22 vs 33.48 [26,41] | Confirmed. The canonical value is `checks.lexical_donor_null.total` in the final `gapmap.json` (22; 33.48; 26–41). 42 vs [33,47] came from the pre-final maps. | README and PROGRESS now give the current values and mark the old figure as superseded. Added `research/results_manifest.json` with `scripts/results_manifest.py --check`. | `research/n3/README.md`, `PROGRESS.md`, `scripts/results_manifest.py` | Fixed |
| 3 | "Verdict does not depend on which evidence it is shown" is too strong | Confirmed. `checks.py` keeps the seed's sentences in both arms, and retrieval injects the seed span. | Every occurrence now reads: under this control, the judge did not tell a candidate's own additional cross-source evidence from the donor's. | Main §1, §3 table, §6.2, §13; Ext. §0, 2, 4, 10, 14, 17, 29 | Fixed |
| 4 | "Fair control" is unqualified | Confirmed. The donor is the nearest same-lens candidate, so its evidence can be genuinely relevant. | Renamed "mismatched-evidence control", which matches the code field `mismatched_evidence_control`; the old name is explained once. Four candidate causes of the tie are listed, and the report says the test does not pick between them. | All sections and figures 2, 8, 13, 14, 15 | Fixed (see note A) |
| 5 | Seed-evidence dominance not explicit | Confirmed: own 0.889 = control 0.889, other-source-only 0.667 (PLC); 17 of 22 pre-final PLC closures cited only the seed or its source (`checks.py` docstring). | Stated as an observed warning with a plausible reading, not a diagnosis. Added the other-source-only arm to Figure 8. | Main §6.2, Fig. 8; Ext. §10 | Fixed |
| 6 | V1 pseudoreplication (214 "units") | Confirmed. | The firing is the unit of inference. Identical pools are coded once, intervals resample by seed claim, and ±0.10/±0.14 are called independent floors. The MS1 lower bound is paired, clustered and adjusted for the number of judges. | Main §10 box and V1; Ext. §17 V1, Table 17 | Fixed |
| 7 | κ ≥ 0.70 is agreement, not validity; owner as coder | Confirmed. Registered NOW allows the owner plus one blind coder (REORIENTATION §22). | Preferred design: two non-owner coders with adjudication; the owner keeps a codebook-ruling log. The report says this needs a recorded NOW amendment, and that without it MS1 is provisional. States that κ shows reproducibility, not correctness. | Main §1, §9, §10, §12; Ext. §16, 17, 24, App. I | Fixed |
| 8 | V5 score-conditioned sampling | Confirmed. The G/D/L/R strata had undefined inclusion probabilities. | V5 now probes every area of the frozen partition, or a simple random sample of it. Pre-set inclusion probabilities with an IPW AUROC are the fallback. The old design is named and dropped, and "decides H2" is replaced by "prospective test of H2" throughout. | Main §10; Ext. §17, 21–26, App. F, I; Fig. 13, 15 | Fixed |
| 9 | V5 power assumes independence | Confirmed. At the reference size the MS5 rule stops or continues only about half the time. | The Hanley–McNeil figure is kept as a first-order reference only. The confirmatory size is set at MS4 by simulation over a pre-registered range. "No underpowered V5 is ever run" is removed. No ICC values are stated. | Main §10; Ext. §17, 22, 25, 26 | Fixed |
| 10 | Human-residual observable | Confirmed. | The latent HKR is now separated from the residual a stated protocol elicits (a lower bound). "None found by this protocol" is never read as "no residual". The asymmetric-miss effect on ΔAUROC is described, and a proposed longer second interview on a random subsample checks it. | Main §3, §9, §10; Ext. §2, 16, 17 | Fixed |
| 11 | V2 is construct-aligned | Confirmed. The lenses carry CTA/CDM constructs (`gapmap/src/gapmap/lenses.py`). | V2 is called a construct-aligned retrospective screen that shows compatibility, not independent support. It stays as the MS3 screen. | Main §9, §10, §8; Ext. §2, 16, 17 | Fixed |
| 12 | H2 wording vs SESOI rule | Confirmed. | H2 is now a minimum-effect hypothesis (ΔAUROC ≥ δ). MS5: STOP falsifies H2 (upper bound < δ). CONTINUE means H2 survives, which rejects "no gain" but does not establish a gain of at least δ. H3 is aligned the same way. | Main §3, §10; Ext. §2, 17 | Fixed (see note B) |
| 13 | δ = 0.05 not derived | Confirmed. | δ is called a provisional program decision threshold, to be justified and signed off before the confirmatory pre-registration against four named quantities. No numbers are invented. | Main §3, §10; Ext. §2, 17 | Fixed |
| 14 | Mutable `main` links | Confirmed: `\repourl` pointed at `blob/main`, and 3 hard-coded `main` links existed. | All links are pinned to the audited commit (`\auditcommit`). The title pages name the commit and release. Tag `report-v1.1` and a GitHub release carry the PDFs. The stale N3 README is named as the reason. | `preamble.tex`, `short.tex`, `main.tex`, Ext. §6, App. E | Fixed |
| 15 | `literature_supported` meaning | Confirmed. Decoys: PLC 7/20 (4/17 without 3 entailed), GDPR 3/20 (`sidecar.json decoys[]`). | The label is defined once as "a locatable public span that a verifier model accepted", not an established fact. The report says verifier error passes into lens firing and candidates. | Main §6.1 | Fixed |
| 16 | Reporting-bias transfer; Figure 1 | Confirmed. Gordon & Van Durme and Paik et al. cover commonsense facts only (primary text checked). | The transfer to expert documentation is tagged as a hypothesis. Figure 1's trace is marked illustrative, its literature box scoped to other domains, and its caption rewritten. | Main §2, Fig. 1; Ext. §1 | Fixed |
| 17 | Szulanski claim too narrow | Confirmed against the primary abstract. It names three barriers (absorptive capacity, causal ambiguity, arduous relationship), contrasted with motivational explanations. | Rewritten in all five places that dropped the third barrier. | Main §2, §11; Ext. §1, §20 (×2) | Fixed |
| 18 | Chao & Salvendy numbers | The primary paper is closed access and was not checked. Clark et al. 2008 p. 585 gives the exact values. | The prose now says the values are as reported by Clark et al. and that the original tables were not checked. Figure 1 says the same. | Main §2, Fig. 1 | Fixed |
| 19 | ClashEval self-correction | Verified against the primary paper: GPT-4o 60.8%, GPT-3.5 62.6%, single-document setting. | Kept unchanged. | Main §6.1; Ext. §9 | Kept |
| JEV | Incorporate the spike | Re-derived from `analysis*.json`. Part 1: the pre-set rule read PROMISING, word length also passed it, and the form test's rule read NO SIGNAL on the inflated pooled ρ. Part 2: κ 0.53 vs 0.27 against Sonnet on 100 prompts. Jev was never run on the control. | One paragraph in Main §6.2 (INCONCLUSIVE, exploratory comparator, not HKR detection). Full subsection Ext. §10 (`sec:jev`). Jev is added to the V1 judge panel, and Jev plus a text-form baseline to the V2/V5 baselines, never a gate. Added to the manifest. | Main §1, §6.2, §10, §13; Ext. §0, 10, 17, App. E | Done |
| Final | Independent adversarial review (Opus, no access to the earlier reviews) | 11 findings; each checked against the artefacts | See the section below | Both reports | Fixed |

## Notes on choices that differ from the review's suggestion

- **A. Control name.** The review suggested "matched-evidence control". We use "mismatched-evidence
  control" instead, because it is the code field's name (`checks.mismatched_evidence_control`), and the
  opposite adjective would break the audit trail from prose to artefact. The report explains that the
  donor is *topically matched* and its evidence *mismatched*, and it drops the unqualified "fair".
- **B. MS5 rule.** The review asked for H2 and its decision rule to be coherent. We kept the rule and
  reworded H2 as a minimum-effect hypothesis. STOP (upper bound < δ) is the test that can falsify H2.
  CONTINUE only means "H2 survives". A gate on "lower bound > δ" passes with probability 0.05 when the
  true gain equals δ, whatever the sample size. The lower bound against δ is reported but does not gate.
- **C. Two non-owner coders.** The registered NOW programme allows one non-owner coder
  (REORIENTATION §18/§22). The report states the preferred two-coder design and says it needs a
  recorded amendment. It does not amend REORIENTATION itself: that decision belongs to the owner.

## Final adversarial review: findings and fixes

All 11 findings were checked and applied:
1. "A better judge cannot fix the tie" was untested and contradicted other sections. It now reads: whether a different judge would break the tie is untested.
2. The Jev judge result now says the first pre-set rule (agreement with qwen) failed before Sonnet became the reference, and gives n = 100 prompts from 68 seeds with the CI.
3. The Jev Part 1 verdict now reads NO SIGNAL under the pre-set form rule (`analysis_loop2.json`). The within-domain reading, which is post-hoc and not in the committed analysis files, would be INCONCLUSIVE.
4. "418 claims have no locatable span" was wrong. It now reads: 260 have no span and 158 have a span the verifier did not accept; all 418 are labeled synthetic.
5. V1 is no longer described as "a validated way to judge". It now reads "a reproducible human label", and the V8 fallback became an upper bound.
6. The conclusion's "checkable record of what sources say" is qualified: a sample of sources, with accuracy and completeness unmeasured.
7. H1 "engineering part: yes" is limited to the pre-fix pipeline; the fixed pipeline has not completed a live run.
8. The trace's "seven independent sources" now reads seven independence keys, two of them vendor pages.
9. V1 now says 105 of the 107 firings have a donor (210 pools).
10. "Viable" became "can be run".
11. Citation overreach: the organizational blind spots are a mapping of ours; the 8-minute probe is a shortened format the CDM work does not test; "all fail" became "can suffer".

## Findings not applied

- Finding 1 (351 → 366): not applied as a correction, because both values are correct for different
  units. A clarifying column was added instead.
