# I11: N9 cost reconciliation

**Branch:** `i11-cost-ledger`
**Outputs:**
- the script `scripts/cost_ledger.py`, with tests under `scripts/` or `reconstruct/tests/`;
- the data `research/cost_ledger/ledger.json`;
- the note `research/cost_ledger/RESULT.md`.

**Cost:** $0.

## Context
- Read `docs/plans/implement-queue.md` § I11.
- Read `REORIENTATION.md` §18 (E-COST) and §22 (N9).
- Spending is recorded in:
  - `reconstruct/runs/*/sidecar.json` and the run logs (`run.py:654`);
  - `research/spikes/jev/cache/` and `RESULTS.md` (the $0.45 total);
  - the N3 runs ($0, local Ollama).
- `obsolete/` holds moved run stdout logs. Read it only where a sidecar lacks costs.

## Steps
1. Aggregate every recorded call into one ledger, one row per call. Each row carries run or spike, stage, model, tokens and USD. It also records:
   - success / retry / failure;
   - engineering vs evaluation (E-LIVE and spikes are engineering; E-PLANT and E-ABST runs are evaluation).
2. Reconcile against each run's recorded total, and against `RESULTS.md`'s $0.45. Report any gap.
3. Report:
   - cost per verified claim;
   - cost per gap candidate;
   - the share of spend lost to failures and retries.

   "Cost per validated item" is shown explicitly as unavailable, because no item is validated. It is never computed from model-supported claims.
4. Add a prospective table: the planned caps for I2, I4's domain run, I10 and the deferred N2 reruns, set against `python3 scripts/key_headroom.py`.

## Done when
The ledger reconciles within $0.01 per run, or the gaps are explained, and `RESULT.md` is written.

## Decision it feeds
The I4 and I10 budgets, and any request to raise the key limit. It has no gate of its own.
