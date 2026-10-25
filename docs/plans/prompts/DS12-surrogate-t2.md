# DS12: Surrogate difficulty ranking (N7, tier T2)

**Branch:** `ds12-surrogate-t2`
**Output:** `research/ds12-surrogate-t2.md`
**Method:** the `research` skill (LLM item-difficulty estimation, simulated test takers, IRT).

## Context
- `docs/plans/deep-search-queue.md` § DS12.
- `REORIENTATION.md` §12.1: the record, the five legitimate uses, the "Never" list, the T1–T4 tiers and their references [49], [63]–[73], [80]–[82].
- `REORIENTATION.md` §22: the T1 SD ratio and the T2 ρ rows.
- `research/ds9-learner-licences.md`, if it exists, for data access.

## Rule
Synthetic prevalence, effect-size and power claims stay banned (`REORIENTATION.md:359`). This note designs a licence test only.

## Questions
1. Which studies validated LLM-simulated difficulty against real aggregate item correctness? What features do the positive results share: an induced proficiency spread, ensembles, weaker models? What ρ did they reach on held-out items? Check the reported 0.72–0.82 against its sources.
2. Which baselines must a surrogate beat? Consider text-feature regressors and direct "rate the difficulty" prompts, and give their reported performance.
3. Which population definition and which spread and stability criteria apply: ≥ 3 seeds, ≥ 2 model families, ≥ 2 independently built surrogate models (the Robust Evaluation Matrix)?
4. Which public datasets with item-level correctness can host T2 legally, given DS9?

## Done when
- The note proposes a T2 protocol (data, split, baselines, ρ threshold and its source, stability rules) and states what a pass licenses (use 5 only) and what it does not.
- `citation-verifier` has passed on it.

## Decision it feeds
The §22 row for the T2 ρ, and whether N7 can license use 5. With no passing design, surrogates stay limited to uses 1–4.
