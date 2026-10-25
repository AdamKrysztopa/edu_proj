# DS1: Which CTA golds are itemised and obtainable?

**Branch:** `ds1-gold-availability`
**Output:** `research/ds1-gold-availability.md`. Correspondence drafts go to `research/ds1-author-contact/` as drafts only; never send them.
**Method:** the `anthropic-skills:deep-research` skill. The OpenAlex MCP handles metadata, `resolve_references` and `list_citations`; web search covers publisher pages and supplements.

## Hard rule: metadata only
- You may record **only** these facts about each gold:
  - whether an itemised list exists;
  - where it sits (table, appendix, supplement, separate report);
  - the item count, and the step / decision / cue split if the abstract or metadata states it;
  - how many experts it was built from;
  - the publication date;
  - the access route and licence.
- Do **not** open, read, quote, download or summarise the list itself.
- If a page displays list items, stop reading that page and record only that it is there.
- This is the §14.3 anti-circularity rule. A breach makes the gold ineligible. Record any breach as a deviation in the note.
- Do not download PDFs into the repo (`research/pdf/` is git-ignored and off limits for commits).

## Context
- `docs/plans/deep-search-queue.md` § DS1.
- `REORIENTATION.md` §18 (E-CTA row), §18.2 and §19 (clinical and maintenance rows).
- `report/sections/17_validation.tex:239-246` (eligibility rule and candidate order) and `26_risks.tex:51-59`.
- The candidate references are in `REORIENTATION.md` §26: [1] Sullivan 2014, [2] Chao & Salvendy 1994, [3] Clark et al. (CTA review), [4] Crandall & Getchell-Reiter 1993, [106] the PARI aircraft-maintenance study.

## Steps
1. Resolve each candidate's DOI and metadata with OpenAlex.
2. Look in [3] and its citing works for further CTA studies that publish itemised outputs: Velmahos, Schaafstal, and any surgical, nursing or military CTA with a published task list. Search OpenAlex for CTA-derived task lists in medicine, maintenance and process control, 1990–2025. Aim for 10 or more candidates.
3. Apply the eligibility rule to each candidate:
   - itemised steps, decisions or cues;
   - built by CTA from more than one expert;
   - the domain is not PLC, GDPR or Track A physics;
   - obtainable for coding.

   Record each condition as yes / no / unknown, with its evidence.
4. For each "unknown", draft (do not send) a one-paragraph author or publisher enquiry that asks only about availability and format.
5. Note, for each gold, whether a text-poor domain test (RQ-I) becomes possible.

## Done when
- The note has a register table: gold, DOI, date, itemised (y/n/?), location, item count, expert count, access, licence, eligibility, fallback rank.
- It has a ranked eligible list, and a statement of whether at least 3 eligible golds exist (V2's minimum).
- It has a deviations section.
- `citation-verifier` has passed on the note.

## Decision it feeds
- The MS2 eligible-gold list. It also decides whether the type-prior baseline is possible, since that needs at least 2 golds.
- **Fewer than 3 eligible golds:** say so first. The MS3 route is then dead, and the owner must choose a pivot (report §26). Ask with `AskUserQuestion` before closing.
