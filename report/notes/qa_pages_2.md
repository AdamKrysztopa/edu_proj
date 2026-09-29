# Visual QA — physical pages 46–102 (§12–§26)

Scope: PDF visual QA of `final_report.pdf`, physical pages 46–102, covering
sections 12 (What the proof of concept demonstrates) through 26 (Risks, kill
criteria and pivots) — i.e. `sections/12_demonstrates.tex` through
`sections/26_risks.tex`.

Method: rendered every page in range at 70 dpi with `pdftoppm`, viewed each
one; zoomed to 150 dpi on the two most complex diagrams (Figure 11, p.57;
Figure 15, p.86) and on dense tables to check for clipping.

## Findings

No defects found. Specifically checked for and did not find:

- text overflowing the margin / overfull lines
- tiny or oversized figures, or figures far from their first reference
- broken or overflowing tables (Tables 15–29 all render within margins,
  including the multi-page Table 29 continuation on pp. 97–98, which carries
  a "continued on next page" note and repeats its header correctly)
- bad page breaks (heading orphaned at page bottom, lone lines, a box split
  awkwardly)
- misplaced floats
- large blank areas exceeding ~1/3 page outside of intended section/part
  ends — the only near-miss is p.77 (end of §20.7), which is followed by the
  Part IV divider page; this is the same intentional part-opening pattern
  already used before Part III (p.56) and is not a defect
- unreadable captions
- visible LaTeX artifacts (`??`, literal `\_`, stray backslashes)
- broken URLs
- badge/tag rendering problems (the OBS/INT/HYP/LIT/FUT tag boxes throughout
  render cleanly and consistently)

Diagrams inspected at 150 dpi (Figure 11 "validation program phases", p.57;
Figure 15 "work packages Gantt", p.86) have no text clipping, no overlapping
boxes, and all arrows/labels are legible.

## Page → issue → fix → status

| Page(s) | Issue | Fix | Status |
|---|---|---|---|
| 46–102 | None found | None needed | OK — no LaTeX changes made |

No edits were made to `sections/12_*.tex`–`26_*.tex`. No rebuild was
required since no changes were made.
