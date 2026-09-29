# Visual language rulebook

Phase 1 deliverable (identity + template). Read this before writing prose or
figures for the report so everything matches. Source of truth for colors:
`report/style/colors.tex` (included by both `report/preamble.tex` and
`report/figures/src/figstyle.tex` -- never hardcode a hex value elsewhere).

## Build

- `cd report && make` builds figures then `final_report.pdf`. `make figures`
  alone recompiles `figures/src/fig[0-9]*.tex` to `figures/pdf/*.pdf`.
- Engine is **LuaLaTeX** (`latexmkrc` sets `$pdf_mode = 4`), not pdflatex --
  Libertinus/Source Sans are loaded as OpenType via `fontspec`. `figstyle.tex`
  standalone figures also need `fontspec` + `\setsansfont{Source Sans Pro}`.
- `figstyle.tex` is `\input`, never compiled directly; the build script's glob
  (`fig[0-9]*.tex`) already excludes it. A new figure source must start with
  `fig` + a digit (e.g. `fig02_...tex`) or the build script will skip it.

## Page and type

- A4, KOMA `scrartcl`. Margins: left 28mm / right 32mm / top 27mm /
  bottom 30mm (room for a 16mm marginpar column, currently unused).
- Body: Libertinus Serif, 11pt, `parskip=half-` (spaced paragraphs, no
  first-line indent). Headings/captions/figure text/UI chrome: Source Sans
  Pro. Mono: Libertinus Mono (Scale 0.92).
- Heading color: `part`/`section` in `accent`; `subsection` and deeper in
  `ink` (only the top two levels carry color, to keep the hierarchy
  "restrained" per the brief).
- `\part` is a full divider page built by `\reportpart{title}{subtitle}`
  (not KOMA's raw `\part`) -- gives full control over the "PART n / rule /
  title" layout. Use it, not `\part{}`, for top-level divisions.
- Avoid hyphenation in display-size text (title page, part titles): wrap in
  `\hyphenpenalty=10000\exhyphenpenalty=10000` as `main.tex` does for the
  title, or hyphenation can break oddly at 28-36pt.

## Color palette (hex)

| Role | Name | Hex |
|---|---|---|
| Body text | `ink` | `#1A1A1A` |
| Captions / secondary text / footers | `gray700` | `#4D4D4D` |
| Rules, borders, neutral node fill-border | `gray400` | `#A6A6A6` |
| Hairlines | `gray200` | `#DDDCDA` |
| Subtle tints | `gray100` | `#F4F2F0` |
| Primary accent (headings, links, Finding/Key-question) | `accent` | `#7A2048` |
| Accent tint (Finding box fill) | `accentlight` | `#F2E6EC` |
| ESTABLISHED LITERATURE | `evlitcol` | `#0B5FA5` (blue) |
| OBSERVED IN THE PoC | `evobscol` | `#00815D` (bluish green) |
| INTERPRETATION | `evintcol` | `#B36A00` (amber/ochre) |
| HYPOTHESIS | `evhypcol` | `#9C3D72` (purple) |
| FUTURE WORK | `evfutcol` | `#5A5A5A` (neutral gray) |

The five evidence colors are Okabe-Ito-derived (color-blind-safe) and
darkened from the textbook values so white badge text clears WCAG AA. They
are deliberately a *different* hue set from `accent`, so a Finding/Key-question
box is never confused with an evidence-category box.

## The five evidence categories

Every substantive claim in the report body gets exactly one tag. Three
redundant channels so the category survives grayscale print and color
blindness: **color + a single letter + a small-caps word**.

| Category | Inline tag | Badge letter | Block box |
|---|---|---|---|
| Established literature | `\evlit` | L | `evlitbox` |
| Observed in the PoC | `\evobs` | O | `evobsbox` |
| Interpretation | `\evint` | I | `evintbox` |
| Hypothesis | `\evhyp` | H | `evhypbox` |
| Future work | `\evfut` | F | `evfutbox` |

- Inline tags (`\evlit{}` etc.) print a small colored roundel with the letter
  in white, followed by a small-caps word (`lit.`, `obs.`, `int.`, `hyp.`,
  `fut.`). Use inline for a single sentence, in a table cell, or in a margin
  note.
- Block boxes (`evlitbox` etc., a `tcolorbox` environment) are for a claim
  that needs a paragraph. Style is deliberately restrained: **left rule
  only** (2.6pt), no full frame, no gradient, a 5%-tint background, the
  category's badge + small-caps name as the first line of body text (not a
  separate title bar). `evfutbox` additionally uses a **dashed** left rule
  (future work = not yet real).
- **Never** blend categories in one box/sentence. If a paragraph mixes an
  observation and an interpretation, split it into two boxes.
- Gotcha we hit once: any custom title text in one of these boxes needs an
  explicit `coltitle=<matching color>`. `attach title to upper` puts the
  title directly on the box's near-white body, but tcolorbox's own title
  default assumes a solid colored title bar and picks a very light text
  color -- without the override the category name is nearly invisible.

## Finding and Key question boxes

Structurally different from the five evidence boxes, and from each other, so
they are never mistaken for an evidence grade:

- `findingbox`: same left-rule-only treatment as the evidence boxes, but in
  `accent`/`accentlight`, with a bullet badge and the label "Finding". Use
  for a conclusion the report is prepared to defend.
- `keyquestionbox`: **full thin frame** (0.6pt, all four sides), not a left
  rule -- the shape difference is the tell in grayscale. `accent` colored,
  "?" badge, label "Key question". Use for an open question the next work
  item must resolve.

## Figures (`report/figures/src/figstyle.tex`)

Six node kinds, each a color + shape pair (redundant, as with the evidence
tags):

| Kind | Shape | Color | TikZ style |
|---|---|---|---|
| Evidence artefact | rectangle | `gray400`/`gray100` | `artefact` |
| Process (deterministic) | rectangle | `accent` | `procdet` |
| Process (LLM-driven) | rectangle | `evintcol` (amber) | `procllm` |
| Human activity | pill (rounded corners = half height) | `evobscol` (green) | `human` |
| Data store | cylinder | `gray400`/`gray100` | `datastore` |
| Gate / decision | diamond | `evlitcol` (blue) | `gate` |

Reuse note: `procllm` reuses the INTERPRETATION amber (an LLM step produces
interpretive/generative output) and `human` reuses the OBSERVED green (a
human-activity node is where a human would act/observe) -- intentional, not
arbitrary; `procdet` uses the main `accent` (the project's own deterministic
machinery); `gate` uses the LIT blue. This keeps the figure palette inside
the same core set of colors as the prose, per the brief.

- **Implemented vs planned**: apply the extra style `implemented` (solid,
  the default) or `planned` (dashed border + `fill opacity=0.5`) after the
  node kind, e.g. `\node[artefact, planned] {...}`.
- **Arrows**: `flowimpl` (solid) for a real/checked flow, `flowplan` (dashed)
  for a planned one. Both use the same `gray700` `Latex` arrowhead.
- **Font**: fixed at `\fontsize{9}{10.5}` Source Sans in the TikZ source for
  node labels, `\fontsize{7}{8}` for small annotations (arrow labels, legend
  text). This is set once in `figstyle.tex`'s `every node` style -- do not
  override per figure.
- **Cylinder shape pitfall**: pgf's `cylinder` shape degenerates to a plain
  rectangle (the elliptical cap disappears) below roughly 16mm width. For a
  small legend swatch, draw the cylinder at its natural size and shrink it
  with `scale=0.3, transform shape` on the node -- do not shrink it via
  `minimum width`/`minimum height`, which triggers the degeneration. See
  `fig01_demo_pipeline.tex`'s legend for the working pattern.
- **Legend layout**: a single row of 6 legend entries is wider than the
  diagram itself, because label *text* -- not swatch size -- dominates the
  row's width. Use two rows of three. Anchor the legend off a `fit` node
  around the diagram's real content nodes (`\node[fit=(a)(b)(c), inner
  sep=0pt] (pipelinebox) {};` then position the legend `below=of
  pipelinebox`), never a fixed `yshift` from the picture origin -- text
  wrapping changes node heights in ways a fixed offset will not track, and
  the legend will overlap the diagram.

### Figure width convention

Figures are authored as standalone TikZ (`documentclass[tikz,border=2mm]
{standalone}`), so their PDF's natural page size **is** the figure's design
size. `\includegraphics` then scales that PDF to fit the requested width --
and because the node font is a fixed point size (9pt/7pt), any scaling
changes the font's *effective* size in print. Design each figure so the
scaling stays mild (roughly 0.9x-1.15x), not the 0.4x-0.7x shrink that comes
from laying a diagram out at whatever size is convenient and then jamming it
into `\includegraphics[width=...]`.

- **Full-width figure**: target a natural width close to the text block
  (~150mm on this A4 setup: 210mm - 28mm - 32mm margins), then include at
  `width=0.92\linewidth` (leaves a small gutter of white space). A natural
  width around 125-145mm lands the effective node font in the 8.5-11pt
  range once placed -- comfortably at or above the 8pt floor.
- **Half-width figure** (two side by side via `subcaption`): target roughly
  half that, ~70mm natural width; include each at `width=0.47\linewidth`.
- Check the actual natural size after any edit: `pdfinfo
  figures/pdf/figNN_*.pdf | grep "Page size"` (in points; divide by 2.83 for
  mm), then compare against the target inclusion width before trusting the
  font stays legible. This is not optional -- `fig01`'s first two drafts
  came out 195mm and 243mm wide and would have shrunk its 9pt labels to
  under 7pt in print; only checking `pdfinfo` caught it.

## Tables

- `booktabs` rules only (`\toprule`/`\midrule`/`\bottomrule`), no vertical
  rules.
- `siunitx` is loaded with `\sisetup{detect-all}` and nothing else global.
  **Do not** set a global `round-mode`/`round-precision` -- it reformats
  every number in every `S` column to a fixed decimal count regardless of
  that column's `table-format`, so a plain count like `3` renders as
  `3.00`. Set rounding per table (`\sisetup{...}` inside the table
  environment, scoped by the surrounding group) if a specific table needs
  it.
- Inline evidence tags read fine inside a table cell (see the demo table in
  `sections/_demo_01_boxes.tex`).

## Front matter

- `howtoreadbox` (gray, full frame, dark title bar) is the one-time
  explanation of the tag/box/figure conventions; it goes right after the
  title page, before the table of contents. It is not one of the evidence
  or Finding/Key-question box families and does not need to be reused
  elsewhere.

## Bibliography

- `biblatex` + `biber`, `style=authoryear-comp`. DOIs and URLs render as
  clickable links (`hyperref` loaded after `biblatex`, `cleveref` loaded
  last). Citation links are colored `evlitcol` (the same blue as the LIT
  evidence tag -- a citation *is* established-literature evidence); internal
  cross-references use `accent`; bare URLs use `gray700`.
- `report/refs.bib` currently holds one placeholder entry
  (`shannon1948mathematical`) that exists only to prove the toolchain
  compiles. It is not project evidence. Content-writing agents: delete it
  and follow `BRIEF.md`'s citation rules (verify every real entry via
  OpenAlex/Crossref before adding it).

## What is a phase-1 placeholder

- `sections/_demo_01_boxes.tex`, `sections/_demo_02_figures.tex`,
  `sections/_demo_03_appendix.tex`: delete once real content sections exist;
  remove the matching `\input` lines (and the two `\reportpart{...}` calls
  that wrap them) from `main.tex`.
- `refs.bib`'s single entry: delete per above.
- Everything else (`preamble.tex`, `style/colors.tex`,
  `figures/src/figstyle.tex`, `Makefile`, `latexmkrc`,
  `figures/build.sh`) is the real, load-bearing template -- keep it.

## Layout method (orchestrator, binding for all figure work)

Use the TikZ/PGF manual through Context7 (library `/websites/tikz_dev_tikz`, tool
`mcp__plugin_context7_context7__query-docs`) before writing layout code. Lay figures out on an explicit grid
(`\matrix` of nodes, `chains`, or `positioning` with fixed `node distance` and equal `text width` per band);
never hand-tune absolute coordinates. Group regions with `fit` + `on background layer`. Route arrows
orthogonally (`-|`, `|-`, calc waypoints) so they never cross text. Fixed `text width`, no hyphenation.
Full-width figures: natural width ≤ 150 mm, height ≤ 190 mm.
