# DS9: Licensed learner data for N4, N7, H4 and H6

**Branch:** `ds9-learner-licences`
**Output:** `research/ds9-learner-licences.md`
**Method:** the `research` skill. Read each dataset's terms on its official page.

## Rule
Read terms and metadata only. Do not download any dataset (`REORIENTATION.md` §24, step 6).

## Context
- `docs/plans/deep-search-queue.md` § DS9.
- `REORIENTATION.md` §18: the E-MISC, E-DIST, E-KC and E-SYN rows. Refs: [137]–[142], [66], [49] and [103]–[104].
- `REORIENTATION.md` §19: the licence column. NC/ND material is excluded from anything that could become commercial.
- `REORIENTATION.md` §12.1: the T1–T3 tiers.

## Datasets
- Eedi Misconception Graph
- NeurIPS 2020 Education Challenge
- Kaggle Eedi competition
- DataShop (per dataset)
- ASSISTments
- AAAS item bank
- FCI on PhysPort
- MaintIE / MaintNet
- O*NET
- the Stack Exchange data dump (evaluation use)
- NAEP released statistics
- EdNet and Junyi, to confirm they are excluded

## For each dataset
- The exact licence or terms, with their URL and the date read.
- Whether research, evaluation and commercial use are allowed, and whether NC or ND applies.
- Its schema: item, option, response, KC tags, time stamps.
- Whether an expert or default KC model exists.
- Its release date against model cutoffs, which matters for the post-cutoff falsifier in E-MISC.
- Whether a leakage-safe split is possible.

## Also
- Find a defensible non-inferiority margin for E-KC ΔRMSE from the KC-model comparison literature.

## Done when
- The register is complete, with a "usable for which experiment" column and the ΔRMSE margin proposal.
- `citation-verifier` has passed.

## Decision it feeds
- Which N4 and N7 experiments can be built, plus the E-KC margin row in the §22 table.
- Any dataset whose terms bar the intended use is dropped.
