# DS8: OSS outcomes and departure corpora (E-OSS, E-DVP, H2)

**Branch:** `ds8-oss-departures`
**Output:** `research/ds8-oss-departures.md`
**Method:** use the `anthropic-skills:deep-research` skill with OpenAlex and web search (dataset repositories, Zenodo, GitHub).

## Context
- `docs/plans/deep-search-queue.md` § DS8.
- `REORIENTATION.md` §18: the E-OSS and E-DVP rows; refs [109]–[116].
- `REORIENTATION.md` §16: R8 (authorship-based metrics break after AI-written code).
- `REORIENTATION.md` §19: the OSS row.
- `REORIENTATION.md` §21: the GDPR and pseudonymisation constraints.
- `docs/plans/n3-gap-map-plan.md` § "E-OSS needs".

## Questions
1. Can the 1,932-project departure corpus [112] and the Chromium-plus-7 data [111] be obtained? Under what licence? Which fields do they hold: departure dates, truck-factor developers?
2. Which post-departure outcomes measure knowledge loss rather than ordinary churn? Candidates are rationale-seeking issues and defect-fix commits. For each, what base rates and variance are published, and which confounders (activity level, release cycles) appear in difference-in-differences designs?
3. How many departures happened before agentic coding began, say before 2023? Which review-weighted concentration measures exist [114]?
4. Which low-visibility repositories fit the contamination option (a) in E-OSS?
5. Using the published variance, give a first power calculation for the number of departures needed.

## Done when
The note contains:
- a dataset register;
- an outcome codebook outline;
- a confounder list;
- the first power estimate, giving the departure count and minimum activity;
- a design for the text-arm and trace-arm comparison that tests H2.

`citation-verifier` has passed on it.

## Why it is in wave 2
The owner set E-OSS as the deciding experiment when E-CTA is inconclusive, and as the only one if E-CTA cannot run (`REORIENTATION.md` §22 N3 row, 2026-10-24). E-OSS needs no gold acquisition, so its feasibility is on the critical path.

## Decision it feeds
- The §22 threshold rows "E-OSS departures and minimum activity" and "dominate" for H2.
- The design of the World B Git adapter.
