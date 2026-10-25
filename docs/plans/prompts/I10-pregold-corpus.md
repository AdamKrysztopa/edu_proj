# I10: A pre-gold corpus route

**Branch:** `i10-pregold-corpus`. Start only after the DS1 and DS5 notes exist.
**Outputs:** a dated local-corpus mode in `reconstruct/` with its tests, and a pilot under `reconstruct/runs/<new>/` with `research/pregold_corpus/RESULT.md`.
**Cost:** one pilot with a cap of `--max-usd 1`.

## Context
- Read these first:
  - `docs/plans/implement-queue.md` § I10;
  - `docs/plans/coverage-audit.md` finding 21;
  - the DS1 register and the DS5 note (`research/ds1-*.md`, `research/ds5-*.md`);
  - `docs/plans/n3-gap-map-plan.md` § "Dated corpus and `as_of`".
- `reconstruct/src/reconstruct/run.py:657-658` hard-codes `--corpus` mode as not N3-admissible.
- `Ledger.as_of(t)` exists, but nothing enforces it at fetch.
- Reuse I7's `admit()` fixtures if I7 is merged; otherwise write the same rules here.

## Steps
1. Add a `--dated-corpus <manifest>` mode. The manifest lists documents with:
   - a source;
   - a date and its kind: OpenAlex `publication_date`, or a Wayback snapshot timestamp;
   - a licence or access basis;
   - a local file.

   `admit()` gates every document. Undated and `Last-Modified`-only documents are rejected. The mode sets `n3_eligible` from its own rule, not from `complete`.
2. Write a manifest builder that queries OpenAlex (`to_publication_date`) and the Wayback CDX API for a given task and cut-off date, and writes the manifest. It records which documents have legal full text, following DS5's access rules. It never fetches gold papers and applies the DS1 blocklist.
3. Tests: future-dated, undated, blocklisted and fully admitted fixtures; `as_of` enforced at fetch.
4. **Pilot.**
   - Pick one non-gold, non-PLC, non-GDPR task, with a cut-off date matching a candidate gold's era, from DS1.
   - Run `python3 scripts/key_headroom.py`, then `python -m reconstruct.run --live --dated-corpus ... --max-usd 1`.
   - Report: the dated share, the full-text share, the verification completeness and the cost.

## Done when
The tests pass and `RESULT.md` gives the pilot figures plus a proposed corpus floor.

## Decision it feeds
- The corpus floor for gold eligibility.
- Golds whose domain cannot reach that floor are dropped from the MS2 eligible list.
