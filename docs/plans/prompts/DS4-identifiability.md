# DS4: Identifiability of the residual under zero text catchability

**Branch:** `ds4-identifiability`
**Output:** `research/ds4-identifiability.md`
**Method:** the `research` skill. Sources: the capture–recapture and species-richness literature, software-inspection defect estimation, and qualitative saturation estimation.

## Context
- `docs/plans/deep-search-queue.md` § DS4.
- `REORIENTATION.md` §14 and §14.1: the definition, the known-truth check and the seven pitfalls. Its references are [143]–[146] and [157].
- `REORIENTATION.md` §16, R4 (fatal-class, tested first).
- `residual/src/residual/residual.py:152-179` (`EstimatedResidual`).
- I3 consumes this note's grid. Read `docs/plans/prompts/I3-residual-identifiability.md`.

## Questions
1. Suppose some items have zero catchability on every text occasion. What, formally, can any capture–recapture estimator identify? Is it only the population that can be caught at all, the written universe? Cite the identifiability results.
2. Which estimators stay defensible under heterogeneity (Mh, Chao1, jackknife, sample coverage), and under positive dependence between occasions? Which lower bounds stay valid when assumptions fail?
3. Can an independent occasion that does catch never-written items correct the estimate, and under what assumptions? Here that occasion is the gold, via Lincoln–Petersen. Is that check informative or circular?
4. Which stress regimes does the simulation literature use, so that I3's grid is comparable?
5. Precedents: software-inspection defect estimation, and saturation estimation in qualitative research [157]. How did they validate against known truth?

## Done when
- The note states the estimand that can be identified NOW, the assumptions it rests on, the recommended estimators with their known biases, and a simulation grid for I3 (parameters and ranges).
- It answers plainly whether "the human residual" is identifiable from text occasions at all. An impossibility result is acceptable.
- `citation-verifier` has passed on it.

## Decision it feeds
- I3's grid and estimand.
- If identifiability fails in principle, R4 goes to the owner before any gold (`AskUserQuestion`), together with I3's result.
