# Bibliography audit — final pass (2026-09-29)

## Scope
153 unique citation keys used across `sections/*.tex` (all `\textcite`, `\parencite`, `\cite`,
`\citeauthor`, `\citeyear`, multi-key forms). `bibliography.bib` has 200 entries; 47 are unused
(biblatex prints only cited entries, so left in place, not removed).

## 1. Missing keys
None. All 153 used keys resolve to an entry in `bibliography.bib`.

## 2. DOI / metadata verification
131 of 153 used entries carry a DOI, all checked against `api.crossref.org/works/<doi>`
(no email/mailto parameter used). The 22 without a DOI were checked via OpenAlex, the arXiv
API, ACL Anthology's own `.bib` export, or the source publisher/library page.

### Fixed
- **orr1996talking** — DOI `10.7591/9781501707407` resolves to the 2016 Cornell UP eBooks
  reissue, not the 1996 original. Kept `year = 1996`; added `note = {Reissued 2016}`.
- **vanlehn2005andes** — DOI `10.3233/irg-2005-15(3)02` actually resolves to *"The Andes
  Physics Tutoring System: Lessons Learned"* (Int. J. Artificial Intelligence in Education),
  not *"Five Years of Evaluations of the Andes Tutoring System"* / *Interactive Learning
  Environments* as previously recorded — those belong to a different, DOI-less VanLehn report.
  Corrected `title` and `journal` to match the DOI target.
- **lyu2026redesign** — `author` field was garbled (`Lyu, Conrad Borchers and others` merged
  two people into one name) and `title` did not match the DOI's actual paper. Corrected to
  `author = {Lyu, Qianru and Borchers, Conrad and others}` and
  `title = {Evaluating a Data-Driven Redesign Process for Intelligent Tutoring Systems}`
  (verified against Crossref, OpenAlex, and the arXiv preprint).
- **liu2017closing** — JEDM's own citation metadata gives `doi = 10.5281/zenodo.3554625` and
  pages 25–41; added both (previously had neither).
- **anthonio2022clarifying** — ELRA has registered a DOI for this LREC 2022 paper
  (`10.63317/5jncetxyfscr`, confirmed resolving via doi.org); added it.
- **golchin2023time** — added an explicit `url` field for consistency with sibling arXiv
  entries (had `doi`/`eprint` only).
- **lebo2013provo**, **sanderson2017web** — pure web references (W3C Recommendations, no
  DOI/eprint); added `urldate = {2026-09-29}`.
- Title-case protection (braces) added for acronyms/roman numerals that were unprotected:
  **bastani2025generative** (`{AI}`), **greshake2023not** (`{LLM}`), **hollnagel2018safety**
  (`{I}`, `{II}`), **kestin2025aitutoring** (`{AI}`, `{RCT}`).
- **meyer2003threshold** — removed `isbn = {1873576682}`. The University of Edinburgh
  Research Explorer page for this item lists that exact ISBN, but it fails the ISBN-10
  checksum (biber flagged it as invalid) — the source's own metadata appears to have a
  transcription error, no corrected ISBN could be independently confirmed, so the field was
  dropped rather than kept invalid or guessed.
- **clark2008cognitive** — reviewed: the DOI `10.4324/9780203880869` resolves to the *book*
  (Handbook of Research on Educational Communications and Technology, 3rd ed.), not the
  chapter. An OpenAlex-listed chapter DOI (`...ch43`) does **not** actually resolve
  (404 at doi.org) — left as the book-level DOI, which is standard practice for Routledge
  handbook chapters lacking a registered chapter DOI. No change needed.

### Verified, no change needed
- All 13 arXiv-only entries without a DOI-in-Crossref (`asai2024openscholar`,
  `choudhury2025bedllm`, `handa2024bayesian`, `kirichenko2025abstentionbench`,
  `piriyakulkij2023active`, `salem2025gapmap`, `shen2025requirements`,
  `skarlinski2024language`, `venkit2025deeptrace`, `wu2024clasheval`, `jin2026chat`,
  `kassis2026mimeo`, `taranukhin2026infogatherer`) — confirmed via OpenAlex or the arXiv API
  directly (Crossref 404s on arXiv-prefixed DOIs because arXiv DOIs are DataCite-registered,
  not Crossref — expected, not an error).
- `ono2026mapping` (ChemRxiv DOI) — confirmed via Crossref.
- `anthonio2020wikihowtoimprove` — confirmed via ACL Anthology's own `.bib` (no DOI registered
  by ELRA for this one, unlike the 2022 paper).
- `delong2004lost`, `polanyi1966tacit`, `meyer2003threshold` (title/author/year/venue) — no
  DOI exists for these older items; publisher/library page checked and matches.
- `hansen1999whats` — a real DOI exists (`10.4324/9780080941042-9`) but it points to a 2013
  *Knowledge Management Yearbook* reprint, not the original 1999 *Harvard Business Review*
  article being cited; left without a DOI rather than attach the wrong container.

### Unverifiable
None outright unverifiable — every used entry was confirmed against at least one
independent source (Crossref, OpenAlex, arXiv, ACL Anthology, or the publisher's own page).

## 3. Field validity (biblatex)
Checked required fields per type (article: journal/journaltitle+volume/pages or DOI;
inproceedings/incollection: booktitle; book/incollection: publisher; misc/online: url).
Two used `@misc` entries lacked `url`/`urldate` coverage — fixed above (`lebo2013provo`,
`sanderson2017web`); `golchin2023time` had DOI/eprint but no `url` — fixed above. No DOI in
the bibliography carries the `https://doi.org/` prefix (checked with a global grep — none
found). All checked URLs return HTTP 200 (or a valid redirect, e.g. the anthonio2022 DOI).

## 4. Unused entries
47 entries in `bibliography.bib` are not cited by any section and were left untouched
(biblatex renders only cited entries; nothing to fix or remove per instructions).

## 5. Scratch build
Repo rsynced to `/private/tmp/.../scratchpad/fabib/` (excluding `build/`, `notes/`) and built
with `latexmk -r latexmkrc main.tex`. Result: clean 150-page PDF.
- Biber log (`build/main.blg`): one warning before fixes —
  `WARN - ISBN '1873576682' in entry 'meyer2003threshold' is invalid` — resolved by removing
  the ISBN field (see above). Second build: **0 warnings, 0 errors** in the biber log.
- `main.log`: no undefined-citation or undefined-reference warnings; remaining warnings are
  unrelated font/microtype notices (missing guillemet glyphs, a bold mono font shape) and
  underfull hboxes in a table, pre-existing and out of scope for a bibliography audit.

## Summary
- Citation keys used: 153 (all resolve)
- Entries fixed: 12 (`orr1996talking`, `vanlehn2005andes`, `lyu2026redesign`,
  `liu2017closing`, `anthonio2022clarifying`, `golchin2023time`, `lebo2013provo`,
  `sanderson2017web`, `bastani2025generative`, `greshake2023not`, `hollnagel2018safety`,
  `kestin2025aitutoring`) plus `meyer2003threshold` (invalid ISBN removed) = 13 entries touched
- Missing keys: 0
- Unverifiable: 0
- Unused entries (left in place): 47
- Final scratch build: 0 biber warnings, 0 errors
