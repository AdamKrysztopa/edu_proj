# Coverage audit: what is explored, what is not (2026-10-24)

Three passes are merged here:
- **[C]**: Claude (this session).
- **[X]**: Codex, an independent read-only first round that did not see [C].
- **[R2]**: an adversarial second round by a fresh Claude reviewer, read-only and offline, which checked every cited claim against files, caches and code.

Codex's own second round stopped at its usage limit. The main session re-checked [R2]'s most consequential claims itself: the MS1 sign, the seed-in-cap retrieval, the config-dependent `gap_id`, the conflict with ADR 0008, the residual freeze scope, and the 16 cached replies that carry only `states`.

"Explored" means a note, a run or code with a recorded result. A term that appears only in `REORIENTATION.md`, `research_notes/` or the report's prose counts as not explored. Neither "explored" nor "implemented" means validated.

Follow-ups: [deep-search-queue.md](deep-search-queue.md), [implement-queue.md](implement-queue.md).

## 1. Explored, with a result

| Area | Result | Where |
|---|---|---|
| 13 method families of the map | Each has a note and a rating decision; DtD falsified to "narrow". Do not rediscover | `research/explore-*.md`, `research/falsify-decoding-the-disciplines.md` |
| Route comparison, decision gaps, Track A roadmap | Done | `research/route-comparison.md`, `decision-gaps.md`, `roadmap.md` |
| Reorientation evidence notes (8) | Raw notes behind `REORIENTATION.md` | `research_notes/Tacit knowledge reorientation/` |
| N0 | Gate passed | `PROGRESS.md:40` |
| N2 engineering | Pipeline end to end on PLC and GDPR; E-LIVE v1–v2 defects fixed; residual defects R1–R10 characterised with fixes specified | `reconstruct/`, `research/n2/final_adversarial_review.md`, `closeout.md:36` |
| N3 PoC (candidate list) | Pipeline end to end; closure step ties its control; precision 3/19 strict (AI judgement) | `gapmap/`, `research/n3/README.md` |
| JEV spike | Tacit signal INCONCLUSIVE (form-driven); as a closure judge, κ 0.53 vs qwen 0.27 against a Sonnet reference | `research/spikes/jev/RESULTS.md` |
| R6 synthetic leakage (engineering) | Typed refusal and bypass safeguards [X] | `residual/src/residual/gates.py:45-138` |
| Track A instrument and M1 kit | Built; waiting on people | `instrument/` |
| Report v1.1 | Phased roadmap: Phase 0 = V1 closure study (MS1) | `report/` |

## 2. Partly explored: built or run, not validated

| Area | What exists | What is missing |
|---|---|---|
| N1 | Schema, labels and freeze, checked against **self-authored gold-shape fixtures** [X] | The gate says "every gold item". The allowance is spent, so treat N1 as provisionally shape-validated (`docs/plans/n0-n1-plan.md:10-11`, `REORIENTATION.md:651`) |
| N2 research gate | Ungated baselines only | **Continue is unreachable as registered**: E-PLANT a_u 5/24 < floor 8; E-ABST reaches its margin only in a narrow corner [C+X] (`research/n2/e_plant_eabst_report.md:38-48,76-87`) |
| N3 as registered | A capped, claim-level candidate list | The registered object is an area-level P(missing) scored against gold. `AreaFeatures` and `GapMapPrediction` have no computation [X]. No AUROC code and no §14.3 baseline exists anywhere [R2] |
| Closure check | Lexical (chance); qwen judge ties its control | See findings 3–6 |
| N5 | Recall and observed-residual arithmetic | `EstimatedResidual` stores a supplied estimate. There is no estimator and no dependence experiment (`residual/src/residual/residual.py:152-179`) |
| N7 | Generation metadata and synthetic-criterion refusal [X] | No T1–T3 experiment (`residual/src/residual/provenance.py:138-156`) |
| N9 | Per-run spend recorded [X] | No ledger and no per-item denominator (`reconstruct/src/reconstruct/run.py:654`) |
| R11 prompt injection | Offline fixture [X] | Live and adaptive resistance unverified |
| RQ-A, B, E, F, G, I, J; H1, H4, H5 | Components or adjacent literature | No gold-scored or discriminating result |
| `methods-critic` | Already checks evidence routes and synthetic criteria | `PROGRESS.md` box unticked; never run on an E-CTA or E-OSS pre-registration |

## 3. Not explored

- **NOW items:** N4, N6 and N8 have no work at all; N5, N7 and N9 have infrastructure only.
- **Experiments:** none for E-CTA, E-OSS, E-DVP, E-EIG, E-SYN, E-HOLD, E-NOV or E-DIFF.
- **Hypotheses:** H2 (traces-first), H3 and H6 have no comparative work.
- **Research questions:** RQ-C, RQ-D and RQ-H.
- **Risks with no project measurement:** R2, R4 (fatal-class, "tested first", `REORIENTATION.md:495`), R7, R8, R9 and R10.
- **Critical-path inputs nobody has checked:**
  - whether the CTA golds other than Sullivan are itemised;
  - pre-gold full-text access;
  - learner-data licences;
  - the OSS departure corpora.
- **Open thresholds:** 12 of the 18 §22 threshold rows are still "to set", and 2 more have only a default.
- **People:** the blind second coder is unconfirmed, and so is the report's external gate reader [R2].
- **§9 areas:** most are not explored. Safety-II, reporting bias, rationale gaps and type→channel routing are partial. §9's own rule defers most until an experiment needs them.
- **§10.2 objects:** the cue-as-discrimination object is partial (the DISC lens); the other three are not built.
- **Worlds and domains:** no World B adapter, no World A learner layer, none of the five §19 panel domains. PLC and GDPR have no gold.
- **Track A:** M1–M8 wait on people; the 4 literature gaps in `PROGRESS.md` are unsearched; Zotero is not seeded.

## 4. Findings that change planning

Tags give who found each finding; *(corrected)* marks a finding that [R2] changed.

### Programme and gates
1. **Nothing run so far can be scored** [C]. Every scorable test needs a new reconstruction in a gold domain.
2. **The report's MS1 margin is sign-inverted** [R2, verified]. It requires the own-minus-control difference *in the not-closed rate* to have a lower bound above 0 (`report/sections/17_validation.tex:213-215`). A discriminating judge closes its own pools more often, which makes that difference negative (compare `gapmap/src/gapmap/checks.py:207`). As written, a perfect judge fails MS1. Fix it before anything is registered.
3. **The two programmes differ less than first stated** *(corrected)* [C+X → R2].
   - REORIENTATION's N3 rule matches the report's **MS5** (lower bound > 0, point ≥ δ; `17_validation.tex:40-44`).
   - MS3 (> −δ/2) is a funding screen, "not a verdict on H2".
   - The real difference: REORIENTATION has an inconclusive route plus a fallback gold, while the report has only a screen.
   - The hypothesis numbering differs, but the report maps its H2 to the strategic H1 (`02_question.tex:45-47`).
   - The owner should still choose which programme governs.
4. **The report's Phase 0 says "no new software"** (`22_roadmap.tex:122`) [R2]. The implement queue builds software for it. One of the two must change.
5. **External gate reader.** The report requires one for MS1 (`26_risks.tex:77-83`), and `24_team.tex:6` says none exists. It would be a second human input beyond the NOW rule's one blind second coder. This is an owner decision [R2].

### The closure control (the MS1 instrument)
6. **The arms are uneven by construction** *(corrected)* [C → X → R2, verified].
   - `retrieve()` places the seed's sentences *inside* the 8-sentence cap (`gapmap/src/gapmap/semantic.py:80-101`, then `build_retrieval`, `:70`). The own arm is a subset of that capped retrieval and is never truncated; only the control arm is.
   - Measured offline: the control arm is truncated in 80 of 153 pairs (PLC 30/54, GDPR v1 28/51, GDPR v2 22/48).
   - In 19 GDPR candidates the seed alone fills the cap, so the primary judgement saw no other evidence.
   - Equal own and control rates therefore say nothing yet about the judge.
7. **Donor pairing depends on the config hash** [R2, verified]. Ties are broken by `gap_id` (`checks.py:139-150`), which hashes `CONFIG_SHA256` (`record.py:107-111`). The donor is tied in 53 of 153 pairs, so any config or manifest change silently re-pairs them, and with them the pools V1 would code.
8. **The split is inconsistent** [R2]. The control counts partial as closed (`checks.py:135-136`), while MS1 gates on closed versus not. Both should be reported, and the MS1 split fixed in advance.
9. **A seed-free arm has a confound** [R2]. An empty retrieval reads "open" without a judge call (`gapmap/tests/test_semantic.py:94-107`). Own other-source evidence is empty in 21 pairs and donor evidence in 7, so the comparison must be restricted to pairs where both arms are non-empty.
10. **V1's judge panel breaks proposed ADR 0008** [R2, verified]. `closure-judge-other-family` excludes the generator's and verifier's families (anthropic, openai) (`docs/architecture/decisions/0008-*.md:26-30`), yet the panel lists `claude-haiku-4.5` and `gpt-5.4-mini` (`17_validation.tex:196-199`).

### Pipeline and data
11. **A malformed judge reply becomes "open", but the defect is latent** *(corrected)* [X → R2, verified].
    - The path exists: no key gives two empty lists, which falls through to `state="open"` (`semantic.py:177-199`).
    - But 0 of 641 cached replies lack both keys.
    - 16 valid replies carry only `states` (GDPR v1 5, v2 11), so the fix is "undecided unless at least one key is present and every present key is a list", not "both keys present".
    - This recurs L7.8 (queued in `docs/lessons.md`).
12. **Admissibility is weak, and tightening it now would empty the sample** *(corrected)* [X → R2]. N2 sets `n3_input` from `complete` (`run.py:653-661`), and N3 checks only `n3_input is False` and pending verdicts (`gapmap/src/gapmap/__main__.py:21-29`). The PLC v1 and GDPR v1 sidecars predate `n3_input`, `failed_calls_by_task` and `cross_checks` (pre-fix commit `600ba2e`). So the strict rule refuses every committed ledger, the 107 firings included. Admissibility as code belongs to Phase 1, V0 (`17_validation.tex:223-225`).
13. **The config hash cannot be the pre-gold freeze** [X, verified]. It hashes values, not lens, retrieval, parser or prompt code (`config.py:135-166`).
14. **The provenance defects are already characterised** *(corrected: stale as findings)* [X → R2]. They are the 25-word duplicate floor (`evidence.py:393`; whitespace and case also defeat it, `:415,418`), decoy validity (`:593-598`), scope-flagged REFUTES becoming contradictions (`run.py:493-500,863`) and the unrecomputed digest (`verify_run.py:33-41`). Each one, with its fix, is already in `research/n2/final_adversarial_review.md` R2–R4, R6 and R9 (lines 112-160).
    - New [R2]: `quote_in_span` accepts any non-empty substring, so a one-word quote passes (`evidence.py:90-95`). That one is not in R1–R10.
15. **New domains need the freeze first** [R2]. "Hash-frozen before any gold or new domain is touched" (`26_risks.tex:130`). V1's out-of-sample domain is also the first live run of the fixed pipeline, which is effectively E-LIVE v3 (amendment 2 P1), and should be registered as such.
16. **Retrieval instability under a frozen corpus** must be "checked before any human time is spent" (`26_risks.tex:133-137`) [R2]. No queued item does this before V1 coding.
17. **Changing the residual estimators triggers a re-freeze** [R2, verified]. `residual.py` is in the frozen semantics hash (`residual/src/residual/freeze.py:27`), so new estimators go in a new module.
18. **I2/I3-style reruns would rewrite committed artefacts** [R2]. They would break the manifest SHA pins (L7.10) and the byte-identical replay claim (`research/n3/README.md:77`). Write to a separate output directory.

### Evidence framing
19. **Density** *(corrected)* [C+X → R2]. "ΔAUROC ≈ 0 by construction" is overstated:
    - `knowledge_types`, `n_unknown` and `rationale_present` are live (`n3-gap-map-plan.md:31`);
    - lens firing is not a function of density;
    - the report already pre-registers a conditional AUROC within density tertiles (`17_validation.tex:95-99`).

    What holds: within candidates, ranking is a monotone function of `k_topic`, an independent-source count (`record.py:131-135`), and the closure step is uninformative. The PLC ρ = 0.906 is mostly the HYP-vs-RG split, since non-HYP records are pinned at −1 (`checks.py:110`). Within the 9 PLC HYPs ρ ≈ 0.83, and within the 6 GDPR v2 HYPs ≈ 0.87. A high-density flag exists (`checks.py:126-127`) but does not fire.
20. **The baseline set** *(corrected)* [X → R2]. "Gold items per area" only needs to be *specified* before gold. Its risk is being a near-oracle that makes Continue unreachable (L7.3). The type prior needs at least two golds before the gate, while the gate opens a fallback gold only on inconclusive. One CTA list may give too few areas (`n3-gap-map-plan.md:21`).
21. **Gold-era corpora** *(corrected)* [C → R2]. The binding constraint for the 1993–94 golds is pre-gold *full-text* access, not Wayback's 1996 start (`17_validation.tex:107`). The only local-corpus route, `--corpus`, is hard-coded as not N3-admissible (`run.py:657-658`).
22. **Budget** [C+X]. The deferred N2 caps total $3 + $14.40 + about $2 = about $19.40, with $5–10 expected. Headroom is $14.99 of $15/week (checked locally 2026-10-24; the $5/week in `e_plant_eabst_report.md:17` is historical). Amendment 2 P1 makes the runs sequential anyway.

### Stale text
23. Several status lines are out of date:
    - `PROGRESS.md:89` ("2nd addition") and `:47-49` (N7 and N9 "not started");
    - the `methods-critic` box;
    - the N3 "NEXT" line;
    - `ai_education_research_map.md:785,1169`;
    - E-SEAL's "start at once" at `REORIENTATION.md:548` (lines 542 and 706 already state the K0 dependency).
24. **JEV write-up** [X + R2].
    - `analysis_judge_swap.json` is direct Jev–qwen agreement, not the control.
    - `RESULTS.md:80` counts "all 641 prompts", but 99 GDPR prompts are shared, which leaves 542 unique.
    - `RESULTS.md:118` asserts a cause the test cannot establish and calls the control "fair" (L7.4).
    - Cache coverage is settled: every prompt the existing control issues is cached (542 Jev calls). Only a seed-free arm needs new calls, about $0.01.
