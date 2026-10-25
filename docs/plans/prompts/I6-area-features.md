# I6: `area_features()`, uncapped candidates and an area score

**Branch:** `i6-area-features`
**Outputs:** a new module `residual/src/residual/features.py` (with `area_features()`), uncapped export and area score in a new `gapmap/src/gapmap/area.py`, tests for both, results in `research/area_score/RESULT.md`.
**Cost:** $0.

## Context
- Read `docs/plans/implement-queue.md` § I6 and `docs/plans/coverage-audit.md` finding 19.
- Read `docs/plans/n3-gap-map-plan.md` (§ "AreaFeatures from a ledger" and its live / confounded / dead table).
- `AreaFeatures` is in `residual/src/residual/gapmap.py:24` and is part of the frozen feature set (`residual/frozen/n1.json`). **Do not add fields.**
- Ranking caps are in `gapmap/src/gapmap/rank.py:98-108`; `k_topic` is in `record.py:131-135`; the anti-renaming statistic pins non-HYP records at −1 (`checks.py:110`).

## Steps
1. Write `area_features(ledger, sidecar, partition) -> AreaFeatures` as a pure, deterministic function, test-first on fixtures. Then run it on the committed E-LIVE ledgers (`reconstruct/runs/`, not gold) with a planner-area partition. Emit the live / confounded / dead table by code, with each feature's variance, missingness and ties.
2. Expose every merged candidate before the display caps, as a separate export. `gapmap.md` stays capped and unchanged. Report how many candidates the caps hide per domain (PLC: 15 of 24).
3. Build the area score as noisy-OR over candidate scores in an area, with max as an alternative. Add an `--areas` input at task-step grain. The output is a *score*; never name it `P(missing)` or call it calibrated.
4. Before computing any association, write down the threshold for "close to a monotone function of source count or size". Proposal: Spearman |ρ| ≥ 0.8 within HYP candidates. Then compute the association between the score and each of `k_topic`, area size and evidence density. Compute it **within HYP candidates only**, not pooled with RG records, and in both directions.
5. Show that the check can discriminate (L7.3). A planted score equal to `k_topic` must trip it, and a random score must not.

## Done when
The tests pass, the residual freeze check shows no drift, and `RESULT.md` contains the feature table, the cap counts and the association results.

## Decision it feeds
- **The score trips the threshold:** change the predictor before MS2.
- **The dead features stay dead:** the E-CTA pre-registration states that it tests size + density + type plus the lens signal only.
