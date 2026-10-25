# DS5: Pre-gold full-text access and memorisation controls

**Branch:** `ds5-pregold-fulltext`. Start after the DS1 register exists.
**Output:** `research/ds5-pregold-fulltext.md`
**Method:** the `research` skill. Use the OpenAlex MCP (`search_works` with `to_publication_date`, open-access status, `group_works`), web search for publisher text-and-data-mining terms, and the Wayback CDX documentation.

## Rule
Count and characterise **metadata** only. Do not fetch the gold papers or any work that reproduces their lists. Apply DS1's blocklist (DOI, title).

## Context
- `docs/plans/deep-search-queue.md` § DS5.
- `REORIENTATION.md` §18.2 and §19; reference [151] for memorisation probes.
- `report/sections/17_validation.tex:107`.
- `docs/plans/coverage-audit.md`, finding 21: the binding constraint is pre-gold full text, not Wayback.
- `research/ds1-gold-availability.md`.

## Questions
1. For each eligible gold in DS1, how many works in its domain were published before the gold's date (OpenAlex `to_publication_date`)? What share is open access with full text? What share is reachable through publisher text-and-data-mining terms under EU DSM Art. 4?
2. For golds published after 1996 (Sullivan 2014, for example), how much web material does Wayback hold from before the gold, by snapshot count for candidate domains and sites?
3. What blocking does each gold need: its DOI, its title, its citing works, and textbooks known to restate it?
4. Memorisation probes. What does current guided-completion probing practice look like [151]? How are its false-positive and false-negative rates controlled, and how is "probe-positive" defined?
5. Which open-weight models document their training cutoffs as of October 2026, and which of them are on OpenRouter or Ollama, at what price?

## Done when
- The note gives, per gold domain: the pre-gold full-text count and its route, a proposed corpus floor, the blocklist spec, a probe protocol, and a model shortlist with cutoffs and prices.
- `citation-verifier` has passed on it.

## Decision it feeds
- I10's design and corpus floor.
- Dropping any gold whose domain falls below the floor.
- The choice of primary model for E-CTA: a blank in the §22 threshold table ("primary model and baseline"), filled after I5, I12 and this note.
