# I4: V1 closure-study kit (Phase 0, gate MS1)

**Branch:** `i4-v1-kit`, from `plans-2026-10-24` (I1, I2 and DS2 are merged there).
**Outputs:** `research/v1_closure/` containing the codebook, the blinded export, the analysis script and its tests, the retrieval-recall sheets, the stability check and the pre-registration draft. The κ/α code is copied into `residual/` per decision 0006.
**Cost:** $0 for the kit. The out-of-sample domain run costs about $0.5–1 and happens only after the owner approves it in step 0.

## Context
- Read:
  - `docs/plans/implement-queue.md` § I4;
  - `docs/plans/coverage-audit.md` findings 2–5, 10 and 15–16;
  - `report/sections/17_validation.tex` (Phase 0, V1, around lines 170-220);
  - `report/sections/26_risks.tex:77-83,130-137`;
  - `research/n3_control/RESULT.md` and `research/n3_control/jev/RESULT.md`;
  - the DS2 note (`research/ds2-*.md`).
- `instrument/src/probe_code/agreement.py` exists. Copy it, do not import it. `instrument/` stays untouched.

## Step 0: owner decisions, asked before building
Ask with `AskUserQuestion`, at most four questions per call. Each question gets one option marked "(Recommended)" with its evidence.
1. **Which programme governs:**
   - the report's MS1 → MS3 → MS5;
   - or `REORIENTATION.md` §22 N3 (its rule matches the report's MS5; the difference is the inconclusive and fallback route).
2. **The blind second coder** (§22): confirm one, or fall back to the owner coding under origin blinding, with MS1 provisional.
3. **The external gate reader** the report requires (`26_risks.tex:77-83`; none exists per `24_team.tex:6`). Choose between:
   - approve a second human input;
   - amend the report so the owner reads MS1, with the limitation stated.
4. **Phase 0 "no new software"** (`22_roadmap.tex:122`): amend the report, given that I1 and I4 build software.
5. **The judge panel against ADR 0008** (`closure-judge-other-family`), given that the report's panel lists `claude-haiku-4.5` and `gpt-5.4-mini`:
   - drop them from the panel;
   - or amend 0008 so that a judge's family need only differ from that of the ledger it judges.
6. **The out-of-sample domain** for about 100 pools:
   - Propose two or three non-gold, non-PLC, non-GDPR candidates, none of them Track A physics.
   - The run is effectively E-LIVE v3 (amendment 2 P1) and needs the I7 freeze plus the I9 fixes first.
   - State its cap. Do not run it in this prompt unless I7 and I9 are merged and the owner approves.

## Steps
1. **Codebook.** Define closed / partial / open, with anchors per lens (DISC, DIAG, SEL, HEDGE, GUARD, WHY, RESULT), built from the DS2 note. Use GDPR v2's 48 firings as training examples only.
2. **Blinded exporter.**
   - It reads I1's `control2` pools and writes the sheets coders see, with no arm, judge answer, rank, run or domain shown.
   - The arm key and unit-ID key go in a separate file.
   - Pools identical across arms are coded once.
   - Freeze the export by hashing it before anything else changes.
   - Check the counts against the report: 105 firings with a donor, 210 pools, 19 identical.
3. **Analysis script**, tested on `SYNTHETIC` labels:
   - weighted κ and ordinal Krippendorff's α, with the gating split fixed as chosen in the pre-registration;
   - intervals that resample seed claims together with all their firings and both arms, plus a source-level sensitivity check;
   - the judge margin with the **correct sign**: the own-minus-control difference in the *closed* rate must have a 95% lower bound above 0, Bonferroni-adjusted over the panel, and must lie within ±0.10 of the coders' difference. Prove the sign with a planted perfect judge, which must pass, and a constant judge, which must fail.
4. **Retrieval-recall sampler.** Draw 50 firings with a seed and produce full-snapshot search sheets for a non-owner coder. Recall is the share of elements found in the snapshots that the pool also holds. Proposed floor: 0.80.
5. **Retrieval-stability check under a frozen corpus.** Re-run retrieval on the same ledgers twice, and with a perturbed sentence order. Report the pool overlap (Jaccard) before any human time is spent.
6. **Pre-registration draft:** κ floor 0.70, recall floor 0.80, the judge margin, the panel from step 0, the split, units, resampling and the analysis-script hash. Run `methods-critic` on it, fix the fatal and major findings, then hash-commit it.

## Done when
The kit is committed and the pre-registration is hash-committed. `research/v1_closure/READY.md` lists exactly what the coders receive and what remains: the coding itself and the out-of-sample domain run.

## Decision it feeds
MS1 is read once coding is complete. **Continue** means writing the Phase 1 case with these numbers. **Stop** means stopping the automated absence check and choosing a pivot (report §26).
