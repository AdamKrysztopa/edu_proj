# DS10: EIG question selection for expert elicitation (N6, H1 vs H3)

**Branch:** `ds10-eig`
**Output:** `research/ds10-eig.md`
**Method:** the `research` skill, using OpenAlex and arXiv via web search.

## Context
- `docs/plans/deep-search-queue.md` § DS10.
- `REORIENTATION.md`:
  - §14.4, the EIG design and refs [147], [148], [156], [175];
  - §12.2, the deterministic gold oracle, whose results are upper bounds;
  - §14.2, the unknown-unknowns guard;
  - §18, the E-EIG row;
  - §22, the N6 row.
- `report/sections/13_not_demonstrated.tex`, item D10.

## Questions
1. Which LLM-based expected-information-gain and Bayesian experimental design methods exist for question selection? Cover BED-LLM-style methods, information-gain rewards, and 20-Questions and preference elicitation. What predictive distribution does each one need, and what does a question cost?
2. Has any study applied EIG to expert, CTA or knowledge-elicitation interviews? The notes found none. Re-check from 2025 onwards.
3. The oracle returns only verbatim gold item IDs through a frozen matcher. Which matching rule and response model would make "EIG with versus without the reconstruction prior" a meaningful H1-versus-H3 test? What can a cooperative oracle not establish about real interviews?
4. What partition-sampling designs, and what unknown-unknowns fraction, does the literature support for high-confidence errors [149]?

## Done when
- The note gives a design for E-EIG: objective, question generator, oracle and matcher, recovery-curve metric, all baselines (random, plain LLM, expert-written, partition sampling, EIG without prior), what the result cannot claim, and a proposed unknown-unknowns fraction.
- `citation-verifier` has passed on it.

## Decision it feeds
- The N6 design and the §22 row "unknown-unknowns question fraction".
- N6 itself starts only after N3 reads Continue or pivots.
