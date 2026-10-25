# I9: Provenance fixes already specified (N2 review R3, R4, R9, plus `quote_in_span`)

**Branch:** `i9-provenance-fixes`
**Outputs:** changes in `reconstruct/src/reconstruct/{evidence,run,verify_run}.py`, with tests; results in `research/n2/provenance_fixes.md`.
**Cost:** $0 (offline; no live run).

## Context
- Read `docs/plans/implement-queue.md` § I9 and `docs/plans/coverage-audit.md` finding 14.
- Read `research/n2/final_adversarial_review.md` (R2–R4, R6, R9; lines ~112-160). It already specifies the fixes. Implement those, and do not re-audit.
- Read decision 0007 and the active rules shown at session start (`independence-before-corroboration`, `budget-before-every-call`).
- Code locations:
  - `evidence.py:90-95` (`quote_in_span` accepts any non-empty substring);
  - `:393-425` (`span_duplicates`, a 25-word floor that splits on single spaces);
  - `:593-598` (`decoy_is_valid`);
  - `run.py:485-508, 863` (REFUTES ignores drift flags);
  - `verify_run.py:25-42` (no digest recompute).

## Steps
1. **Baseline first.** Run the current code over the committed runs in `reconstruct/runs/` offline. Record the contradiction count, the coverage per slot, the duplicate-supported claims and the `verify_run` problems.
2. **R3.** Test spans verbatim against the claim's own sources. Normalise whitespace and case before shingling. Identical-assertion merges must not bypass the check.
3. **R4.** Scope-flagged REFUTES go to a separate `scope_refutes` list. They are not contradictions.
4. **R9.** `verify_run` recomputes each snapshot's SHA-256 and checks that every source binds to its snapshot.
5. **`quote_in_span`.** Require a minimum length, proposed at 5 words or the whole span if shorter. Write the threshold into the commit message.
6. **Decoys.** Do not change `decoy_is_valid` semantics here; DS6 decides the rubric. Add only a test that documents the current behaviour.
7. Replay on the committed runs, and report every count before and after. `uv run --directory reconstruct pytest -q` must pass. The rules shown at session start must still hold.

## Done when
`research/n2/provenance_fixes.md` gives the counts before and after, per fix and per run.

## Decision it feeds
Whether the fixed pipeline is ready for I4's out-of-sample domain run (the effective E-LIVE v3) and for any later dated reconstruction.
