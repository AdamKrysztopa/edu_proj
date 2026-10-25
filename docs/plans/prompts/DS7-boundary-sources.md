# DS7: Public boundary sources that would revive dead features

**Branch:** `ds7-boundary-sources`
**Output:** `research/ds7-boundary-sources.md`
**Method:** the `research` skill. Use web search and OpenAlex.

## Rule
Do not search for or read any gold's contents. If DS1 exists, apply its blocklist.

## Context
- `docs/plans/deep-search-queue.md` § DS7.
- `REORIENTATION.md` §13 (Worlds A, B and C) and §14.2 (boundary-text density, reporting bias [25]).
- `docs/plans/n3-gap-map-plan.md` § "AreaFeatures from a ledger": `n_boundary_sources` is 0 everywhere, and the date features are unreliable.
- `reconstruct/` `Source.kind` values, in `residual/src/residual/provenance.py` and `vocab.py`.
- `research/ds1-gold-availability.md` for the domain list: the primary golds are Okoli 2020 (incident command), Madani 2015 and Logishetty 2019 (surgical); fallbacks are DS1 ranks 5–17.
- `research/area_score/RESULT.md` (I6): six of the 20 frozen features are constant in every ledger, including `n_boundary_sources` and `has_done_support`.

## Questions
1. Per candidate gold domain (incident command, for Okoli; surgical, for Madani and Logishetty; then the fallback domains of DS1 ranks 5–17), which public texts record practice at the novice–expert boundary? Candidates:
   - professional forums and Q&A sites;
   - morbidity-and-mortality and case-report series;
   - incident and near-miss databases (NTSB, FAA Service Difficulty Reports, ASRS, MAUDE);
   - postmortems and training-programme FAQs.
2. For each source, what are its access route, licence or terms, date coverage (does it predate each gold?), volume, and the `Source.kind` it maps to (with a proposed mapping, no new field)?
3. What evidence is there that these texts contain "obvious" steps that expert-to-expert text omits (reporting bias)?

## Done when
- The note has a source table per domain, the proposed `Source.kind` mappings, and an assessment of which dead features each source could revive (`n_boundary_sources`, `has_done_support`, dated support).
- `citation-verifier` has passed on it.

## Decision it feeds
Whether the E-CTA pre-registration revives the dead features, or states that it tests size, density, type and the lens signal only (finding 19, I6).
