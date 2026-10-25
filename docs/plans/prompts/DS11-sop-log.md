# DS11: A public pair of an SOP and its execution log

**Branch:** `ds11-sop-log`
**Output:** `research/ds11-sop-log.md`
**Method:** the `research` skill. Search process-mining dataset repositories, such as the 4TU.ResearchData BPI Challenge collection, and the conformance-checking literature.

## Context
- `docs/plans/deep-search-queue.md` § DS11.
- `REORIENTATION.md` §9: the Safety-II [19] and process mining / conformance [124] rows.
- `REORIENTATION.md` §13, reordering 2: in the company track, traces come before prose.
- `REORIENTATION.md` §15 H2 and §18 E-DVP.
- `REORIENTATION.md` §19: a qualification noting that no public SOP-plus-log pair was found.

## Questions
1. Which public event logs come with a **documented reference process or procedure**: BPI Challenge 2011–2020, the road traffic fines log, the sepsis log, hospital billing logs, and others? For each, what does the procedure document contain? Is it prose, a BPMN model or a regulation?
2. What licence does each have, which fields does it carry, and how large is it?
3. Which of them let a gap map built from the procedure *before* time *t* be scored against deviations in the log *after* *t*? Deviations here mean skipped, extra or reordered steps.
4. Do any of them include the rationale behind a deviation, or comments that show why practice diverges?

## Done when
- The note has a register of candidate pairs and a feasibility verdict for E-DVP outside OSS and for a test of H2 (traces first).
- `citation-verifier` has passed on it.

## Decision it feeds
Whether E-DVP and H2 can be tested outside OSS. If no pair fits, OSS remains the only proxy, as `REORIENTATION.md` §18 assumes.
