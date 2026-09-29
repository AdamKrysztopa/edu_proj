# Visual QA — physical pages 103–148 (§27–§29, References, Appendices A–I)

Scope: original PDF physical pages 103–148 (§27 Expected scientific contributions, §28 Expected
practical impact, §29 Conclusion, References, Appendices A–I). Rendered every page at 70 dpi,
zoomed to 150–300 dpi on anything suspicious, then rebuilt in a scratch copy
(`latexmk -r latexmkrc main.tex`) and re-inspected by content (page numbers shifted during the
session as other QA agents edited earlier sections concurrently — the build ended at 143 pages
instead of 148).

Per-instruction constraint: layout fixes only, no content removed. Every fix below is a LaTeX
markup/escaping change (an unbroken macro made breakable, or a spurious literal backslash
removed) — no word, sentence, or table row was added, removed or reworded.

## Findings and fixes

| Page (content-located) | Issue | Fix | Status |
|---|---|---|---|
| Appendix A, Table 32, row E33 | `\code{MAP\_TOP\_N=12}` rendered with **visible literal backslashes** (`MAP\_TOP\_N=12`) because `\code` uses `\detokenize`, which prints escaped control sequences literally instead of consuming them | Removed the spurious backslashes: `\code{MAP_TOP_N=12}` | Fixed |
| Appendix B §"Shared machinery, once." (lines ~12–14) | Overfull hbox 66.7pt + 22.8pt — `\code{literature_supported}` and `\code{synthetic_extrapolation}` are fully unbreakable (texttt+detokenize), so the line ran ~0.9cm and ~0.3cm past the right margin (confirmed visibly overflowing past the page's text block in a 300dpi render) | Changed both to `{\small\nolinkurl{...}}`, matching the pattern already used for the neighboring `organisational_artefact_supported` in the same sentence — `nolinkurl` allows breaking at underscores | Fixed |
| Appendix B, `_best_sentence` / `_diag_anchor()` / `checks.apply_sibling` (prose, lines ~26, ~91, ~239) | Same literal-backslash artifact as E33 (`\_best\_sentence` etc. printed with visible backslashes) | Removed spurious backslashes | Fixed |
| Appendix D, Table 36, row EL11 | `\code{UnicodeEncodeError}` (unbreakable monospace) ran directly into the adjacent "Found by" column with no gap — text visibly collided (confirmed at 300dpi: "UnicodeEncodeErro" abutting "v2 run") | Split into `\code{Unicode}\allowbreak\code{EncodeError}`, matching the existing `\allowbreak` convention used elsewhere in the same table (row EL1) | Fixed |
| Appendix D, Table 36, row TR2 | Same collision pattern: `\code{checks.apply_sibling}` ran into "Reviewer B, code read" in the next column, and also carried the literal-backslash artifact (`checks.apply\_sibling`) | Removed the backslash and split with `\allowbreak`: `\code{checks.apply}\allowbreak\code{_sibling}` | Fixed |
| Appendix E "What cannot be reproduced offline" (line ~149) | Worst case found: `\code{reconstruct/runs/**/snapshots/}` is fully unbreakable and was **cut off at the page's right edge** (83.2pt overfull — confirmed visually, the bullet's first line ran past the printable area) | Changed to `{\small\nolinkurl{reconstruct/runs/**/snapshots/}}`, letting it wrap at the slashes | Fixed |
| Appendix E, `config_sha256` / `reconstruct.verify_run` (lines ~99, ~102, ~152) | Same literal-backslash artifact | Removed spurious backslashes | Fixed |

## Checked, no visible defect (left as-is)

- Appendix A, Table 32, rows E06 and E28 (overfull hbox 7.5pt / 8.5pt): long `\repo{}`/`\code{}`
  path strings in table cells; confirmed at 200dpi the text stays inside the column, no visible
  bleed. Below the threshold worth restructuring given the "minimal changes" instruction.
- Appendix B, DIAG section (overfull hbox 23.7pt at "interpretation plus cue…" and 8.0pt at the
  question-template quote): confirmed at 300dpi both wrap cleanly inside the text block; the
  warning is absorbed by justification stretch, not a visible overflow.
- Appendix E, "Package internals" paragraph (lines 27–44, three overfull warnings 19.6–36.1pt) and
  the N2 run-ID itemize (lines 110–113, 10.4pt): dense inline `\code{}` module/class listings and
  long run-ID strings; confirmed at 200dpi every line stays inside the margin.
- References (pp. 104–112): all DOIs/URLs wrap correctly, no raw BibTeX artifacts, no duplicated
  entries found. The `Feldon, D. F.` "–" entries (repeated-author dash) and Pace's two entries are
  the standard bibliography convention, not defects.
- Longtables (Table 32 claim/evidence table, Table 36 defects table, Table 37 glossary): headers
  repeat correctly across page breaks, no split-row artifacts, no broken continuations.
- Appendices C, F, G, H, I: no overflow, no bad breaks, no LaTeX artifacts, no large empty areas.
- §27, §28, §29: clean.

## Not touched

- `figures/src`, `preamble.tex`, `main.tex`, `bibliography.bib` — no issues found that required
  changes there; the bibliography's formatting was checked and found consistent (no missing-brace
  or malformed-URL defects to fix).

## Files edited

- `report/sections/A_claims.tex`
- `report/sections/B_lenses.tex`
- `report/sections/D_defects.tex`
- `report/sections/E_reproduce.tex`

No sentence, clause or table row was removed or reworded in any of these files — every change is
either (a) deleting a spurious backslash that was making an underscore print literally, or (b)
swapping `\code{...}` for `{\small\nolinkurl{...}}` / inserting `\allowbreak` so an identifier can
wrap instead of overflowing the column or margin. Rebuilt clean (`latexmk`, no errors, no new
overfull boxes above the pre-existing baseline in sections outside this scope).
