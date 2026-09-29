# Figures

Build: `report/figures/build.sh` (LuaLaTeX, standalone + `figstyle.tex`). Each entry below
documents one figure: what it shows, where its numbers/fields come from, and its natural
(un-included) page size from `pdfinfo`.

`figstyle.tex` sets `\hyphenpenalty=10000\exhyphenpenalty=10000` (plus `\sloppy`) on every node so
figure text never hyphenates, automatically or at an existing hyphen -- a split word in a small
box reads as a typo. Applied figure-wide; see the per-figure notes below for the nodes it forced
wider, resized, or manually re-wrapped.

## fig01_problem.pdf (`fig:problem`, home: `sec:problem`)

"What part of expert knowledge reaches text, and what does not?", avoiding the iceberg cliché.
Two aligned columns for one concrete task trace (PLC intermittent-fault troubleshooting): left,
what an expert does (five human-activity pills: notice the cue, rule out a rival cause, choose a
test, interpret the result, check own drift); right, what written sources say about the same five
steps (two stated, three absent -- absent steps drawn with the `planned`/dashed style reused to
mean "not in the text", not "future work"). A literature block underneath gives the omission
evidence at its original grain, explicitly labelled LITERATURE.

- Numbers copied verbatim from `report/notes/02_foundations.md` sec. 1 (the orchestrator's
  grain-exact figures, not the disputed "~70%" secondary claim): Sullivan et al. 2014 (3 surgeons,
  1 procedure) -- 73% of decision steps and 71% of clinical-knowledge steps omitted; Chao &
  Salvendy 1994 (6 programmers) -- no single expert reported more than 41% of diagnostic actions;
  reporting bias stated qualitatively (02_foundations.md sec. "reporting bias"), no invented
  number attached to it.
- Natural size: 134.5 x 109.6 mm.
- Reused convention: solid artefact box = appears in written sources; dashed (`planned`) artefact
  box = absent from written sources. This is the one figure where `implemented`/`planned` styling
  is repurposed for "stated"/"absent" rather than "built"/"not built"; the legend says so.
- Widened the four right-column boxes (34→37 mm / text 31→34 mm) after the figure-wide
  no-hyphenation rule (`figstyle.tex`) stopped "symptom" from splitting as "symp-tom".

## fig02_model.pdf (`fig:model`, home: `sec:approach`)

The report's central model (`00_outline.md` "central model") on an explicit coordinate grid: six
columns 25 mm apart (origin to origin), every box 20 mm wide with a 9 pt title and a 7 pt second
line. Row 1 (implemented, left to right): Domain or capability -> 1 Reconstruct (LLM) -> 2 Evidence
ledger (store) -> 3 Lenses (deterministic, 7 methodology lenses) -> 4 Absence check (LLM, amber "!"
and the note "weak link: ties its fair control") -> 5 Triage (gate). Row 0 is a feedback lane only:
Triage -> "Retrieval gap: search or verify more" (solid, "not enough sources"), then a dashed edge
back into Reconstruct labeled "re-search (manual today)", because no code feeds retrieval gaps back;
the RG records are an output list. Row 2 (implemented, right to left): Triage -> Gap candidate
("attested but unstated") -> 6 Prioritized questions. Row 3 (planned, dashed, right to left):
7 Human evidence -> 8 Residual measured -> 9 Calibrate -> 10 Apply, with a dashed feedback from
Calibrate through the empty column-3/4 space into the lenses ("recalibrate lenses and absence
check"). A dotted gray region with an inside top-left label marks "Implemented in the PoC (N1-N3)"
around rows 0-2; "Not built yet" labels row 3. Legend: two rows (4 + 3), centered under the diagram.

- "Ties its fair control": `research/n3/README.md` closure-vs-control section (own rate = control
  rate on every lens and ledger).
- Departures from the 26 mm / 20 mm-text-width brief, each forced by a measured constraint: column
  pitch 25 mm and text width 19 mm (the 26 mm pitch plus region padding put the width over 150 mm);
  rows 2 and 3 at -30 mm and -58 mm instead of -24 mm and -52 mm (row-2 boxes need 20 mm for their
  wrapped text, and the Triage -> Gap candidate label needs a clear gap); step 3 titled "Lenses" with
  "7 methodology lenses" as the second line ("3 Methodology" alone is wider than a 20 mm box).
- Text uses `align=flush center`: with figstyle's `\sloppy`, plain `align=center` stretched the
  interword spaces visibly.
- Natural size: 149.9 x 113.7 mm.

## fig03_lenses.pdf (`fig:lenses`, home: `sec:foundations`)

The seven N3 lenses as a 7-row matrix, no graph edges: lens badge (`procdet` style), source
construct (methodology), what the lens looks for (missing element), predicted knowledge type with
tacitness (7 pt gray line), and the human channel to ask. A one-line note under the matrix says the
literature supports the constructs in column 2, not the lenses themselves.

- Content from `report/sections/B_lenses.tex` (checked against `gapmap/src`), abridged to at most
  two short lines per cell. Where `research/n3/README.md`'s "Lenses" table differs, B_lenses wins:
  DISC's source is CTA (the README says CDM; drawn "CTA (CDM)"), HEDGE's source is case-based
  reasoning (README: CBM); tacitness and the DISC/GUARD/HEDGE channel details are B_lenses only.
- Layout: five column left edges and one 12.5 mm row pitch, set once at the top of the source;
  header in small caps gray, `gray200` rules between rows.
- Natural size: 149.7 x 96.7 mm.

## fig04_architecture.pdf (`fig:architecture`, home: `sec:architecture`)

Implemented PoC architecture. Top band: `residual` (N0/N1 evidence model), with dotted "imports"
arrows into two package frames. Left frame `reconstruct` (N2): plan → search → fetch → extract →
locate → verify → contradict → assemble, fed by "Web (World A)"; model tags `claude-haiku-4.5`
(plan, extract) and `gpt-5.4-mini (other family)` (bracketed over verify and contradict). Between
the frames, `ledger.json` and `sidecar.json` (from assemble, into lenses). Right frame `gapmap`
(N3): lenses → absence check (`qwen2.5:7b` local, cached; two-way arrow to
`closure_judgements.json`) → triage + records → merge → rank by breadth + display cap → checks →
render, writing `gapmap.json / .md`. Bottom: `instrument/` (Track A, frozen, not used) and a
dashed "Expert answers (not built)" node. One-row legend.

- Stage order from `reconstruct/src/reconstruct/run.py` (docstring and stage comments) and
  `gapmap/src/gapmap/__main__.py` (`build_gapmap`, `run`). Contradict is drawn LLM-driven: the
  pairwise contradiction stage was replaced by cross-cluster re-verification, which calls the
  verifier model. Search is drawn deterministic: OpenRouter's web plugin (Exa) is used for its URL
  citations only, never its text. In gapmap the display cap lives in `rank.build`, so it sits with
  "rank by breadth", and all checks finish before `render`, so checks precede render.
- Model ids from `reconstruct/models.json` and `gapmap/src/gapmap/config.py`.
- Layout: one x lane list and one 12.5 mm row pitch at the top of the source; all arrows orthogonal
  through two free lanes between the frames. Planned nodes keep opaque text here
  (`planned/.append style={text opacity=1}`, local to the file).
- Natural size: 148.5 x 164.1 mm.

## fig05_evidence.pdf (`fig:evidence`, home: `sec:evidence-model`)

Anatomy of one claim's provenance chain: fetched snapshot (sha256 of normalized text) →
`Selector` (`exact` verbatim span, re-sliced from the snapshot — never the model's quote;
`locator`) → claim record fields (`assertion`, `knowledge_type`, `world: A (public)`,
`practice`) → `Verification` (verdict by a verifier of a different model family than the
generator) → the epistemic label, drawn as a gate/diamond because it is a **computed** property,
never asserted. A second row hangs each side condition under the node it annotates: a 7 pt note
under Selector ("quote not found → no selector; claim labeled `synthetic_extrapolation`, never a
criterion", per revision_R1 D4), `Source.independence_key` under the claim record (union-find: same
registrable domain, OR 5-shingle containment ≥0.5, OR a shared ≥25-word verbatim run; dashed
attached-field connector), and the UNKNOWN slot condition under the label (searched, fetched,
extracted, fully verified — nothing found).

- Field names verified directly against `residual/src/residual/provenance.py` (`Selector`,
  `Evidence`, `Verification`, `Source`) and `residual/src/residual/claims.py`
  (`ClaimRecord.label`).
- Independence-key rule and UNKNOWN condition: `report/notes/05_architecture.md` sec. 3, steps 6
  and 9 (`reconstruct/src/reconstruct/evidence.py`).
- Natural size: 423.82 × 206.99 pt ≈ 149.5 × 73.0 mm.

## fig06_n2.pdf (`fig:n2`, home: `sec:n2`) — data figure

Grouped horizontal bar chart (pgfplots), two panels: E-LIVE v1 claim-stage counts for PLC and
GDPR in pipeline order, top to bottom: claims extracted, located, verified-supports. Sources
fetched is a page count, a different unit, so it is a 7 pt note under each panel ("sources
fetched: 35" / "20"), above the run ID.

- Numbers (verified 2026-09-29 against `sidecar.json` `stats`: `n_sources_fetched`,
  `n_extracted`, `n_located`, `n_supports`): PLC v1
  (`reconstruct/runs/20260928T133336Z-59ec876b3d7e/`) 35 sources, 370 / 337 / 321; GDPR v1
  (`reconstruct/runs/20260928T135354Z-eb840a85b7d1/`) 20 sources, 259 / 204 / 195. Same numbers
  in `figures/src/fig06_n2.dat`.
- Tick labels and bar values use `assume math mode` so numerals render in Source Sans.
- Natural size: 394.24 × 117.83 pt ≈ 139.1 × 41.6 mm.
- Build gotcha (documented in the `.tex` source): inside `\begin{groupplot}[...]`, pgfkeys
  processes `bar width` before the `xbar` style has installed the bar-plot handler, and raises
  `I do not know the key '/pgfplots/bar width'`. Fix: pre-register both via
  `\pgfplotsset{every axis/.append style={xbar, bar width=...}}` before the `tikzpicture`, not as
  inline `groupplot` options. Reproduced and confirmed in isolation before applying the fix.

## fig07_n3.pdf (`fig:n3`, home: `sec:n3`) — data figure

Process diagram on a 4-column grid with per-domain counts (PLC / GDPR v1 / GDPR v2). Row 1: lens
firings (155 total: 56/51/48) → closure judge → judge-state table (closed / partial / open /
synth-closed). Row 2: triage into retrieval gaps (RG-SINGLE, RG-UNVER, RG-SIBLING, RG-UNK — thin
support, not ranked) and gap candidates (HYP) 32 / 1 / 6 → merge + display cap (≤12 total, ≤3
per lens, ≤4 per area; after merge 24 / 1 / 6, shown 9 / 1 / 6) → ranked gap map + template
questions (map length 10 / 2 / 7, +1 CONTROL slot each). A note under the cap stage says PLC's 15
capped HYP appear in no output array (revision_R1 D6, review_B B3).

- Judge-state table and RG-* counts verified 2026-09-29 against
  `research/n3/{plc,gdpr_v1,gdpr_v2}/gapmap.json` (`checks.judge_lexical_confusion` target
  states; `retrieval_gaps`). RG-SIBLING is n/a for PLC: its run has no sibling ledger.
- HYP counts from an offline replay with the committed `closure_judgements.json` caches
  (`gapmap.__main__._primary_records`, `record.unk_gaps`, `checks.apply_sibling`, `rank.merge`,
  `rank.build`): before merge 32/1/6, after merge 24/1/6 (PLC: RESULT 13, WHY 8, DIAG 2, GUARD 1),
  shown after `rank._cap` 9/1/6; the replayed map `gap_id`s equal the committed ones. Cap limits
  from `gapmap/src/gapmap/config.py` (`MAP_TOP_N`, `MAP_PER_LENS`, `MAP_PER_AREA`).
- Natural size: 414.65 × 239.35 pt ≈ 146.3 × 84.4 mm.

## fig08_closure.pdf (`fig:closure`, home: `sec:n3`) — data figure, title-free

The central negative result, two pgfplots panels (caption carries the title). Panel A: a
dot/dumbbell plot of own-evidence vs. fair mismatched-evidence-control closed-or-partial rate per
ledger (x-axis "closed-or-partial rate"; `checks._closed_or_partial`) —
the two dots coincide on every ledger. Panel B: the lexical donor null, observed count vs. the
null's mean and "5–95% null interval" (legend wording), per ledger; PLC's observed count falls
*below* its null interval.

- Panel A numbers (verified 2026-09-29 against `checks.mismatched_evidence_control.total` in each
  `research/n3/*/gapmap.json`): PLC own=control=0.8889 (n=54); GDPR v1 0.9608 (n=51); GDPR v2
  0.9583 (n=48).
- Panel B numbers (verified against `checks.lexical_donor_null` in the same files): PLC observed
  22, null mean 33.48, interval [26, 41]; GDPR v1 observed 11, mean 12.735, [8, 17]; GDPR v2
  observed 11, mean 8.08, [5, 12].
- Natural size: 387.29 × 168.12 pt ≈ 136.6 × 59.3 mm.

## fig09_trace.pdf (`fig:trace`, home: `sec:demos`)

One complete, real trace, vertical flow: source (seed URL + rival-claim URLs) → verbatim seed span
→ seed claim ID + label + the extractor's assertion the lens reads (7 pt note: the anchor is that
assertion cut at 80 characters) → lens fired (DIAG: 7 independent sources discuss the topic, 5
rival causes) → inferred gap (`closure_state: open`; no rival fully distinguished, 4 of 5 partly
addressed with 5 partial rival hits, the fifth only by an unverified sentence; the DIAG rule counts
a partial rival as unsigned) → hypothesis (verbatim, including each "(no sign found)", with a 7 pt
note on what that marker means) → template question + channel (verbatim) → expert answer ("not
collected: zero participants by design (NOW program)"). Border color carries the evidence
category: green observed, purple hypothesis, gray dashed future work.

- Verbatim text from `research/n3/plc/gapmap.json` `map[0]` (`g-59164a9db5bd`): `anchor`,
  `hypothesis.text`, `question.text`, `inferred_gap.judge_reason`, `partial_hits` (5),
  `confidence.k_topic` (7), `observed_evidence` (seed `c-d7bce12d16755797`, `liambee.me`; 4 rivals
  from `automate.org`, 1 from `ecsintl.com`). The assertion is from the PLC v1 `ledger.json`.
- Per-rival judge states from an offline replay with the committed cache
  (`semantic._judge_diag`): 4 `partial`, 1 `synthetic-closed` (aliasing), none `closed`;
  34 = verified sentences retrieved summed over the 5 rival probes (8+2+8+8+8).
- URLs are shortened with `...` to fit one line each; JSON straight quotes print as
  `\textquotedbl`.
- Natural size: 354.99 × 562.83 pt ≈ 125.2 × 198.6 mm (≤ 210 mm ceiling).

## fig10_worlds.pdf (`fig:worlds`, home: `sec:platform`)

The three evidence worlds, stacked in a left column (36 mm boxes): World A "Public text" (solid;
literature, standards, forums, manuals; `label: literature_supported`), World B "Organizational
records" (dashed; procedures, tickets, logs, code; `label: organisational_artefact_supported`,
wrapped) and World C "Human evidence" (dashed; elicitation, traces, learner data;
`label: observed_human_evidence`). A (solid) and B (dashed) enter one tall "Evidence ledger" store
with straight unlabeled arrows; ledger → Gap map → Questions for humans (all solid). The planned
loop: Questions → down and along a bottom lane → World C ("ask") → Residual measured →
Gap map ("calibrate"). Legend: implemented in PoC (solid), planned (dashed).

- World contents from `report/notes/06_platform.md` secs. 1.1-1.3; label names are the code's
  epistemic-label enum names.
- Label lines use Latin Modern Mono Light Cond (7.5 pt): the regular monos (Latin Modern,
  Libertinus) are too wide for the 36 mm boxes. Planned nodes keep opaque text in this file.
- Natural size: 142.3 x 100.7 mm.

## fig12_residual.pdf (`fig:residual`, home: `sec:residual`)

The Human Knowledge Residual as a construct, not a measurement: two aligned horizontal bars of
equal width (not to scale), on fixed grid constants (`\barW`, `\splitA`, `\splitB`). Bar 1,
"Knowledge competent practitioners use": "stated in the evidence base" (observed green) and "not
in the evidence base: Human Knowledge Residual" (hypothesis purple, dashed). Bar 2, "What the
evidence base states", spans exactly bar 1's first segment: "captured by the reconstruction"
(observed green) and "retrieval gap (stated, not captured)" (gray, dotted). All labels sit inside
their segments. A "Gap map (PoC: lenses + absence check)" box below sends a straight dashed arrow
up into the residual segment, labeled "predicts where" beside it. Two definition notes (≤ 3 lines
each): residual (HYPOTHESIS; measurable only with World C evidence) and retrieval gap (search or
verify, never ask a human). One-row legend.

- Construct and definitions from `report/notes/00_outline.md` terminology and `REORIENTATION.md`
  sec. 14. Bar proportions are illustrative, not measured data.
- Natural size: 415.05 × 221.53 pt ≈ 146.4 × 78.2 mm.

## fig11_platform.pdf (`fig:platform`, home: `sec:platform`)

Future platform in six full-width bands, top to bottom, each labeled in small caps at its top-left:
Evidence sources (World A public text, solid; World B organizational records and World C experts
and learners, dashed) -> Ingestion (web search and fetch, solid; repository and commit adapter "for
E-OSS", dashed; company connectors and the optional candidate-passage provider "e.g. Weft", dotted)
-> Evidence ledger (one wide solid store) -> Analysis (verification and independence, solid;
contradiction analysis "coded; not run live", dashed; gap map, solid; area score and question
selection "incl. EIG", dashed) -> Human evidence (blind expert elicitation -> residual measurement
-> "Valid?" gate, all dashed, reading right to left) -> Applications (learning; organizations,
dotted), reached only through the gate.

- Grid: four columns at a 34 mm pitch, 31 mm boxes; band tops computed once with `\pgfmathsetmacro`
  from label strip + box height + padding + gap. Every box is a bold title plus at most one 7 pt line.
- Arrows run one per column where data flows; solid only between solid boxes. The calibration loop
  is a direct dashed arrow from residual measurement up to the gap map in their shared column
  (label "calibrate"); the right-hand lane carries World C down to blind elicitation instead.
- Column-1 arrows through the ledger band sit 7 mm right of centre so they clear the band label.
- Statuses follow `tab:components` in `sections/18_platform.tex`, except blind expert elicitation
  (dashed here per the figure spec; the table says long-term for new tracks). The table's domain
  learning model is not drawn.
- Natural size: 145.2 x 165.4 mm.

## fig13_validation.pdf (`fig:validation`, home: `sec:validation`)

Restructured validation program (R2) in three light gray phase bands, each labeled inside at top
left and read left to right, on the fig14 box/gate vocabulary (explicit mm grid; 9 pt bold study
code and title, one 7 pt line). Phase 0 --- before any grant: PoC today (solid; "absence check ties
its control") -> V1 Closure study (">=100 double-coded units"; tag "blind coder") -> MS1, with a
dashed "stop" exit to Pivots ("audit tool; interview-only"). Phase 1 --- lean methods grant: V0
Admissibility + area score -> MS2 freeze (a blue bar on the arrow, "MS2 freeze" beneath, not a
gate) -> V2 Pooled CTA golds (">=3 published golds; V4 on V2 data") -> MS3, with a dashed "stop" exit
to the Interview-only pivot ("costed separately"). Phase 2 --- released only on MS3 continue: V5
pilot (6 experts) -> MS4 -> V5 Blind elicitation ("decides H2; ~300 areas, 45 experts") -> MS5 ->
three stacked lanes, V6 Efficiency (H3) -> MS6, V7 Organizational pilot -> MS7, V8 Novices -> MS8.
Each "continue" from MS1 and MS3 runs down through the white gap between bands and along a left
margin rail into the next band's first box. Below the bands, unconnected to the H2 chain: the
dashed "Organizational track: V3 H-OSS" ("Git adapter + code lenses; own freeze MS2b; cannot stop or
license H2") and the gray "Validation Track A (frozen; own preconditions)" rail, reached only by one
dashed arrow from V8 labeled "sealed, non-gating".

- Content follows `sections/17_validation.tex` and `notes/program_structure_R2.md`. Gate diamonds
  hold only their code; each rule sits in a 7 pt note of at most two lines that repeats the code in
  bold (MS1: kappa >= 0.70, recall >= floor, a judge beats the fair control; MS3: screening, point
  >= delta, lower bound > -delta/2, beats density; MS4: areas fit the funded ceiling, alpha >= 0.80,
  stratum guessing near chance; MS5: H2 verdict). MS6--MS8 carry no note; their lane names say it.
- The MS1 and MS3 notes sit above the gate's stop arrow; the MS4 note sits below the Phase 2 row
  because the MS5 fork leaves no room above.
- Every study, pivot, the H-OSS track and the Track A rail are dashed (future work); only PoC today
  is solid. One-row legend: observed, future work, gate, freeze.
- Natural size: 149.1 x 151.3 mm. At `width=0.92\linewidth` the 9 pt labels print near 8.4 pt.

## fig14_roadmap.pdf (`fig:roadmap`, home: `sec:roadmap`)

Gated roadmap of the restructured program. Row 1: S0 PoC (solid, "complete, Sept 2026") -> Phase 0:
V1 closure study (owner-run, before any grant) -> MS1 -> S1 Phase 1: lean methods grant (V0, V2
pooled, V4; MS2 freeze at M4) -> MS3. Each gate's exit hangs below it: MS1 -> "Pivots (audit tool;
interview-only)", MS3 -> "Interview-only pivot (costed separately)". A return connector carries MS3
into a gray Phase 2 band ("released only if MS3 reads continue") with three lanes: S2 Research
prototype (V5 pilot) -> MS4 -> S3 Prospective validation (V5 main, V6) -> MS5/6; the
organizational track, S4 H-OSS (V3, MS2b freeze at M23) -> H-OSS gate, and S4 Partner pilot (V7)
-> MS7; the education lane, S5 Learner data (V8a, no gate) and S5 Novices (V8c) -> MS8. MS5/6
drops into V7 and V8c; MS7 and MS8 merge into S6 Full platform (not grant-funded). All stages
after S0 are dashed.

- Stages, studies, months and gate rules from the stage table in `sections/22_roadmap.tex` and
  `tab:milestones` in `sections/23_workpackages.tex`: MS1 end of Phase 0, MS3 M14, MS4 M24, H-OSS
  M33, MS5 M38, MS6 and MS8 M46, MS7 M48.
- Grid: Phase 2 columns computed from box 24 mm, gate 11.5 mm, gap 4.8 mm; V7 and V8c sit in the
  MS5/6 column so the chart stays under 150 mm. Diamonds hold only the code; each rule is a 7 pt
  note of two or three lines beside its diamond.
- Natural size: 149.3 x 119.0 mm.

## fig15_gantt.pdf (`fig:gantt`, home: `sec:workpackages`)

Gantt chart, WP1-WP11 in number order plus a Track A rail, from Phase 0 (drawn as months -3 to 0,
axis label "P0") to M48 at 1.8 mm per month; month m occupies [m-1, m], so a gate at Mm sits at
x = m. Phase 0 and Phase 2 are shaded, and brackets above the axis name the three phases. Coin
markers (EUR) at MS1 and MS3 mark the tranche releases. Gates (MS1, MS3, MS4, H-OSS, MS5, MS6/MS8,
MS7) are diamonds on an upper tier; the freezes MS2 and MS2b are squares on a lower tier, because
MS2b (M23) and MS4 (M24) would otherwise overlap. The rule for each milestone is in a two-column
key under the chart.

- Bars from the WP text in `sections/23_workpackages.tex`: WP1 P0-M48; WP2 M1-M8; WP3 P0 and
  M5-M10; WP4 M1-M14; WP5 M15-M36; WP6 M15-M30; WP7 V5 pilot M21-M24, V5 main M25-M38, V6
  M39-M46; WP8 M39-M48; WP9 V8a M15-M20, V8c and materials M39-M48; WP10 M15-M38, then M39-M48
  after MS5; WP11 P0-M48.
- Two bar hues (accent for science and human studies, gray for engineering), rounded corners for
  human-participant studies, and dashed bars at 55% fill opacity for segments conditional on MS4
  or MS5 (every Phase 2 bar already waits for MS3, which the shading shows).
- Smallest text 7 pt; row labels 8.5 pt.
- Natural size: 148.3 x 161.8 mm.
