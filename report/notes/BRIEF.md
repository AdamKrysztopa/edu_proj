# Shared brief for every agent working on the final PoC report

Repository: /Users/adamkrysztopa/projects/edu_proj (GitHub: AdamKrysztopa/edu_proj).
Deliverable: a LaTeX research report in `report/` (the final PoC report; also the base of a
grant proposal, a document for university researchers and industrial partners, and the
blueprint for the full platform). You are one worker in a multi-agent team. The orchestrator
merges your output. Agent agreement is not evidence.

## Project in one paragraph

Experts skip reasoning steps that have become automatic, so what they write and say leaves
knowledge out. The project asks whether AI can (1) reconstruct what is already written about a
domain or capability from public (and later organisational) evidence, with provenance, and
(2) predict where that reconstruction is thin, i.e. where the knowledge that only humans hold
(the "human knowledge residual") is likely to lie, before any human is asked; and then
(3) turn those predictions into prioritized questions for experts. Physics education was the
original setting (now the frozen "Validation Track A", with a built interview instrument in
`instrument/`); the strategy changed on 2026-09-28 (`REORIENTATION.md`) to the zero-participant
NOW programme N0–N9. N0–N1 built the evidence model (`residual/`), N2 the reconstruction
pipeline (`reconstruct/`), N3 a proof-of-concept methodology-guided gap map (`gapmap/`,
`research/n3/`). N2 ends as "engineering PoC complete, research validation deferred";
N3 ends as "pipeline complete, hidden-knowledge prediction not demonstrated".

## Key files

- `REORIENTATION.md` (strategy; §1 summary, §22 NOW programme), `PROGRESS.md`, `CLAUDE.md`
- `ai_education_research_map.md` (graded literature evidence), `research/explore-*.md`,
  `research/falsify-decoding-the-disciplines.md`, `research/route-comparison.md`
- `research_notes/Tacit knowledge reorientation/*.md` (raw evidence notes; REORIENTATION wins)
- `docs/plans/*.md`, `docs/architecture/decisions/0001..0008`, `docs/lessons.md`, `docs/LESSONS-ARCHIVE.md`
- `docs/poc-explained.html`, `docs/n2-eplant-eabst-protocol.md`, `docs/n1-*.md`
- `research/n2/*.md` (closeout, E-LIVE, E-PLANT/E-ABST reports, adversarial review)
- `research/n3/README.md` and `research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.{md,json}`
- code: `residual/src`, `reconstruct/src`, `gapmap/src`, tests in each package; runs in `reconstruct/runs/`

## Hard rules

1. Every important statement belongs to exactly one category: ESTABLISHED LITERATURE,
   OBSERVED IN THE PoC, INTERPRETATION, HYPOTHESIS, FUTURE WORK. Never blur them.
   "Predicted hidden knowledge" is NOT "observed expert knowledge". The PoC has no human
   validation. Do not write that the system "identifies tacit knowledge".
2. Every PoC number must be checked in the primary artefact (JSON, code, report file), not
   copied from an intermediate summary. If you cannot verify a number, say "unverified".
3. Every literature citation must be real and verified: title, authors, year, venue, DOI or
   stable URL. Verify with OpenAlex MCP tools (`mcp__openalex__*`, load via ToolSearch),
   Crossref (https://api.crossref.org/works/<doi>), or the publisher page. Never cite a paper
   because a model (or a repo note) says it exists; the repo notes are leads, not proof. If
   you cannot verify, mark it UNVERIFIED and do not put it in the .bib.
4. NEVER include the user's email address in any request, URL, header or payload
   (no "mailto=" polite-pool parameters). A hook will deny it.
5. Do not read `.env` files, `.private/`, `sessions/`, `instrument/sessions/`, or any sealed
   E-PLANT gated-arm/answer-key file. Aggregates in committed reports are fine.
6. Do not modify anything outside `report/`. Do not commit. Do not run live model calls
   (`--live`, `--judge ollama`). Running offline tests is fine.
7. Writing style for any prose meant for the report: American English, "English Simplified":
   short sentences, plain words, technically precise, no marketing, no grant-speak, no filler.
   Explain unavoidable jargon once.

## Output conventions

- Write your notes to the file path given in your task (under `report/notes/`).
- BibTeX entries go to the `.bib` path given in your task. Keys: `firstauthorYEARword`
  (lowercase, e.g. `klein1989critical`). Include `doi` when one exists, else `url`.
  Add a `note = {verified: <how>}` field? NO: instead keep a separate verification line per key
  in your notes file ("key — verified via OpenAlex W..., DOI resolves"). Keep the .bib clean.
- Your final message back to the orchestrator: at most 250 words — what you wrote, where,
  and the 3–6 findings that matter most. The detail lives in the files.
