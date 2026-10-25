# I8: Admissibility as code (Phase 1, V0)

**Branch:** `i8-admissibility`
**Outputs:** changes in `reconstruct/src/reconstruct/run.py` (setting `n3_input`) and `gapmap/src/gapmap/__main__.py` (`_admissibility_note`), with tests; results in `research/admissibility/RESULT.md`.
**Cost:** $0.

## Context
- Read `docs/plans/implement-queue.md` § I8 and `docs/plans/coverage-audit.md` finding 12.
- Read `docs/plans/n3-gap-map-plan.md:13` (the required rule) and `report/sections/17_validation.tex:223-225` (V0).
- `run.py:653-661` sets `n3_input` from `complete`.
- `gapmap/__main__.py:21-29` checks only `n3_input is False` and pending verdicts.
- The PLC v1 and GDPR v1 sidecars predate the `n3_input`, `failed_calls_by_task` and `cross_checks` fields (pre-fix commit `600ba2e`).

## Steps
1. Replay first. Before you change any rule, compute what the strict rule would do on every committed run in `reconstruct/runs/`. The strict rule:
   - every located extraction has a verdict;
   - cross-verify ran;
   - decoys ran;
   - no failed calls.

   Report admitted / refused per run, and which N3 maps and V1 pools each refusal would remove. Expect every committed ledger to fail it.
2. **N2.** Set `n3_input` true only when the strict rule holds. Record the per-criterion booleans in the sidecar.
3. **N3.** Refuse a missing sidecar. Refuse `n3_input` false. For a sidecar that predates the fields, set `admissibility = "legacy"`, with the missing fields named. Never refuse it silently, and never call it admissible.
4. The committed maps under `research/n3/` must not change. Legacy status is reported by a separate audit command, not by re-rendering.
5. Tests: one per criterion, a legacy sidecar, a missing sidecar, and a fully admissible fixture.

## Done when
The tests pass, and `RESULT.md` gives the per-run table and the rule as implemented.

## Decision it feeds
The MS2 admissibility rule, and the admissible share of runs made after the freeze. The V1 pools stay usable as "legacy", and they are labelled as such.
