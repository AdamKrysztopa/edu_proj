# I3: N5 identifiability: zero catchability and planted dependence

**Branch:** `i3-residual-identifiability`
**Outputs:** a new module `residual/src/residual/estimators.py` with tests in `residual/tests/test_estimators.py`, and a simulation in `research/n5_sim/` containing `RESULT.md`, `grid.json` and the outputs, all labelled `SYNTHETIC`.
**Cost:** $0.

## Context
- Read `docs/plans/implement-queue.md` § I3 and `docs/plans/coverage-audit.md` finding 17.
- Read `REORIENTATION.md` §14.1 (definition, known-truth check, the seven pitfalls), §12 use 1 (known-truth debugging), and §16 R4.
- If `research/` already has a DS4 note (`research/ds4-*.md`), use its grid and estimand. Otherwise use the default grid below and say so.
- `EstimatedResidual` (`residual/src/residual/residual.py:152-179`) is a record type with no computation. `residual.py` is inside the frozen semantics hash (`residual/src/residual/freeze.py:27`). **Do not edit it.** The new module only produces values that fit the record.

## Steps
1. **Implement the estimators**, test-first against published worked examples. Cite each example's source in the test docstring.
   - Chao1, the lower bound, with its standard interval.
   - The first-order jackknife.
   - Mh, heterogeneity-robust. If a full Mh needs a dependency outside pydantic and the standard library, implement the Chao Mh lower bound and note it.
   - Lincoln–Petersen, with the Chapman correction.
2. **Simulator.** Build a finite universe of N items, split into written items (each with a catchability per occasion) and never-written items (catchability 0 on every text occasion). It has k text occasions plus one gold occasion, which is independent and covers items of both kinds.
   - Default grid: N ∈ {50, 200}; never-written share ∈ {0, 0.2, 0.5}; k ∈ {2, 3, 5}; catchability heterogeneity low and high; positive dependence between text occasions ρ ∈ {0, 0.3, 0.6}; 500 replicates per cell, seeded.
3. **Zero-catchability counterexample.** Construct pairs of universes with identical observed text-capture histories but different never-written counts, and show what each estimator returns for both members of a pair.
4. **Known-truth check.** For each cell, give the estimate of the unseen items, the true count, and the count of gold items no text occasion caught. Report bias, interval coverage, and whether |estimate − gold-uncaught| ≤ a tolerance τ, for τ ∈ {10%, 25%, 50%} of the gold-uncaught count.

## Done when
- The tests pass and the freeze check still matches: `uv run --directory residual python -m residual.freeze` shows no drift.
- `research/n5_sim/RESULT.md` states:
  - which estimand is identifiable from text occasions: the written universe only, or more;
  - which estimator and τ are achievable under which dependence;
  - the counterexample.

## Decision it feeds
- It selects the estimator, the estimand and a realistic tolerance for N5's pre-registration. It does not read N5's gate.
- If no estimator meets even τ = 50% with independent written occasions and a never-written share of 0, stop and raise R4 with the owner ("drop the residual as an objective", `REORIENTATION.md` §22 N5) before any gold. Ask with `AskUserQuestion`.
