# Short report — outline and rules (orchestrator, binding)

Goal: a self-contained short version of the final report, **at most 40 PDF pages in total** (title, contents,
body, references), carrying all the substance: the problem, the idea, what was built, what it showed and
did not show (with the key numbers), why, the validation program with its gates and kill rules, the plan
with money and team status, and what to do next. A reader who reads only this must be able to evaluate the
project. It is a condensation of the long report (`main.tex` + `sections/`), which stays the reference.

Source of truth: the long report's CURRENT sections (read them; they are final and audited), plus
`notes/program_structure_R2.md`. Do not introduce any fact, number or citation that is not in the long
report. Use the same bibliography keys (`bibliography.bib`), the same figures (`figures/pdf/*.pdf`, included at
natural size with `\includegraphics{figures/pdf/figNN_name.pdf}`), the same evidence tags/boxes, the same
terminology and hypothesis/milestone names. English Simplified, American spelling.

## Files
- `report/short.tex` (document; copy the title page and "How to read" box from main.tex, adapted: title
  "Finding What Experts Leave Unsaid", subtitle "Short report: the proof of concept, what it shows, and the
  research program that could validate it"; \setcounter{tocdepth}{1}; contents on one page; override the footer:
  `\ifoot{\sffamily\small\color{gray700}Finding What Experts Leave Unsaid --- Short Report}` after \input{preamble.tex}).
- `report/sections_short/*.tex` (one file per section below).
- Add a `short` target to `report/Makefile` (latexmk on short.tex, copy build/short.pdf → `short_report.pdf`).
  latexmk -r latexmkrc short.tex writes build/short.pdf (out_dir = build).
- Where detail is omitted, point to the long report in plain text: "(full report, Section 17)". Do not \cref
  across documents.

## Structure and page budget (target 36–38 pages of body incl. figures; references ~2–3 pages)
1. Summary (1.5 p) — result first; the recommendation (V1 before any grant); what was built; what is new;
   the program; team status.
2. The problem (2 p) — Fig 1. Omission evidence with n and domain; reporting bias; one education and one
   organizational example.
3. Question and hypotheses (1 p) — RQ, H1/H2/H3, the falsifier; status table (3 rows).
4. From existing methods to the approach (3.5 p) — what each tradition contributes (compact table:
   methodology → construct → lens), Fig 3 (lenses), Fig 2 (central model), closest prior work and a
   condensed novelty ledger (≤ 8 rows).
5. What was built (4 p) — architecture in prose + Fig 4; evidence model essentials (claim record, labels,
   provenance, UNKNOWN, worlds as typed fields); evolution N0–N3 in 4 lines.
6. Results (6 p) — N2 (E-LIVE numbers, spans, defects found live, E-PLANT/E-ABST and the INCONCLUSIVE
   verdict, the budget stop, decoy false-accept rate); N3 (lenses, absence check, triage, counts incl. the
   display cap, Fig 7, the closure-control result Fig 8, precision with qualifiers, density correlation,
   stability); one complete trace Fig 9 with its weaknesses.
7. What the PoC shows and does not show (2 p) — two compact tables (or one two-part table).
8. Interpretation and threats to validity (2 p).
9. The Human Knowledge Residual (1 p) — construct, how it would be measured (Fig 12 optional if space).
10. The validation program (5 p) — logic chain, Phase 0/1/2, each study with hypothesis, design,
    participants, baselines, blinding, measure, sample-size reasoning, gate rule; Fig 13; external gate reader.
11. Platform and applications (3 p) — three worlds (Fig 10 optional), Fig 11, what exists vs planned,
    Weft in two sentences, education and organizational applications and their limits.
12. Plan (4 p) — domains (compact table), roadmap Fig 14, phases with euro tranches and what each buys,
    team (lean vs grant-scale in one table) and honest team status, top risks and kill criteria (compact
    table), expected contributions (if H2 holds / even if it fails).
13. Conclusion (0.5 p).
References (printbibliography; only cited entries print).

Figures: Figs 1, 2, 3, 7, 8, 9, 11, 13, 14 are required; 4, 6, 10, 12, 15 only if the page cap allows.
Tables: small type (\small or \footnotesize) allowed; booktabs; no longtables longer than one page.

## Hard checks before done
- Total PDF pages ≤ 40 (pdfinfo). If over, cut prose first, optional figures second, never the Results or
  the "does not show" content.
- 0 undefined references/citations; no overfull boxes > 5pt.
- Every number matches the long report exactly.
- Render every page at 70 dpi and look at it; fix layout problems (float placement, empty areas, orphans).
