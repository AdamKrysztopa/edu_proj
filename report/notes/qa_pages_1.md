# PDF visual QA — physical pages 1-45 (front matter, executive summary, Part I, Part II up to §11)

Rendered every page at 70 dpi, inspected visually, zoomed to 150-200 dpi on suspicious pages.

| Page(s) (orig. PDF) | Issue | Fix | Status |
|---|---|---|---|
| Physical p.17 (printed p.13), `sections/03_foundations.tex` Table 2 (`tab:methods`) | 18-row table set in a plain `table`+`tabular` environment overflowed the page: the last row ("DtD ... decoding interview not evidential") ran into the footer and its text collided with the printed page number ("evidenT3tial"). | Converted the `table`/`tabular` to a `longtable` (already loaded via preamble) with `\endfirsthead`/`\endhead`/`\endfoot`/`\endlastfoot`, so the table now breaks cleanly across two pages with a "continued from previous page" header. | Fixed, rebuilt and re-inspected — table now spans printed pages 13-14 cleanly, no overlap. |
| Physical p.33 (printed p.29), `sections/08_evolution.tex` Table 7 (`tab:now-verdicts`), row N0 | The "What was built" cell used `\code{scripts/hook_tests/test_check_dois.py}` (plain `\texttt`, no break points) inside a `tabularx` X-column; the long unbreakable string overflowed into the adjacent "Registered verdict" column, visibly overlapping "Done, gate passed (2026-09-28)". | Changed `\code{...}` to `\repo{...}` for that path (consistent with the neighboring `\repo{residual/}` in the same cell and with how other file paths are handled in this table); `\repo` uses `\nolinkurl`, which allows breaks at `/` and `_`. | Fixed, rebuilt and re-inspected — path now wraps inside its own column, no overlap. |

All other pages in range (1-16, 18-32, 34-45) were inspected at 70 dpi with no issues found: no margin overflow, no bad breaks, no misplaced floats, no oversized blank areas, no LaTeX artifacts, figures/tables sized and placed correctly, captions readable, footers/headers consistent.

Both fixes are confined to `sections/03_foundations.tex` and `sections/08_evolution.tex`; no changes to `figures/src`, `preamble.tex`, or `bibliography.bib`. Rebuilt in a scratch copy (`qa1b/`) via `latexmk -r latexmkrc main.tex`; build succeeded (143 pages total after all agents' concurrent fixes — down from the original 148, consistent with other QA agents' page-range fixes running in parallel).
