# Finding What Experts Leave Unsaid

Reports on the edu_proj proof of concept (NOW items N0–N3) and the research program that could
validate it. Three documents, three purposes:

| PDF | Source | Purpose |
|---|---|---|
| `main_research_report.pdf` (about 34 pp) | `short.tex`, `sections_short/` | the argument: problem, approach, results, validation program, plan |
| `extended_technical_report.pdf` (about 143 pp) | `main.tex`, `sections/` | the complete technical record: protocols, full results, implementation, appendices |
| `executive_summary.pdf` (2 pp) | `summary.tex` (shares `sections/00_executive_summary.tex`) | two-page summary; section numbers refer to the Extended Technical Report |

The Main Research Report points to the Extended Technical Report for detail; it does not replace it.

## Build

Needs TeX Live 2025 (LuaLaTeX, biber, TikZ/pgfplots) and the fonts Libertinus and Source Sans Pro.

```
make            # figures, then all three PDFs
make extended   # Extended Technical Report only
make main       # Main Research Report only
make summary    # executive summary (builds the Extended Technical Report first)
make figures    # only figures/src/*.tex -> figures/pdf/*.pdf
make clean      # remove build/ (keeps the PDFs)
```

The build uses LuaLaTeX; pdfLaTeX is not supported.

## Layout

| Path | Contents |
|---|---|
| `main.tex`, `short.tex`, `summary.tex` | the three documents |
| `preamble.tex`, `style/colors.tex` | shared visual identity, evidence tags and boxes |
| `sections/` | Extended Technical Report: one file per section (`00`–`29`) and appendix (`A`–`I`) |
| `sections_short/` | Main Research Report: one file per section (`01`–`13`) |
| `bibliography.bib` | verified references (biblatex, author–year) |
| `figures/src/` | editable TikZ/pgfplots sources; `figstyle.tex` holds the shared figure style |
| `figures/pdf/` | compiled vector figures, included at natural size |
| `figures/README.md` | what each figure shows and where its numbers come from |
| `notes/` | the evidence trail: research notes, the claim/evidence audit, both review rounds, revision decisions, final audits and page QA |

## How to read the notes

- `notes/01_evidence_audit.md`: every PoC claim with its artifact and strength.
- `notes/review_A.md`, `review_B.md`: Round 1 reviews (scientific, technical).
- `notes/review_C.md`, `review_D.md`: Round 2 reviews (hostile grant, clarity and reproducibility).
- `notes/revision_R1.md`, `revision_R2.md`: the decisions taken on those reviews.
- `notes/audit_final.md`, `audit_bib.md`, `audit_citations.md`, `qa_pages_*.md`: final checks.

Numbers in the report come from committed artifacts in this repository (`research/n2`, `research/n3`,
`reconstruct/runs`) and from offline test runs; Appendix E gives the commands to reproduce them.
