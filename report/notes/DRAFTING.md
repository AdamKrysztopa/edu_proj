# Drafting protocol for section and figure agents (binding)

Read first: `report/notes/BRIEF.md`, `report/notes/00_outline.md` (structure, terminology and the
"Orchestrator consistency rulings" at the end — they override any note), and
`report/notes/10_visual_language.md` (macros, boxes, figure conventions).

## LaTeX conventions

- Engine: LuaLaTeX via latexmk. Class scrartcl (KOMA). Sections use `\section`, `\subsection`,
  `\subsubsection`, `\paragraph`. Each section file starts with `\section{Title}\label{sec:KEY}`.
  Do NOT use `\part` or `\reportpart` (the orchestrator adds parts in main.tex).
- Do not edit `main.tex`, `preamble.tex`, or another agent's files. Write only your assigned files.
- Evidence categories: inline tags `\evlit`, `\evobs`, `\evint`, `\evhyp`, `\evfut`; block boxes
  `evlitbox`, `evobsbox`, `evintbox`, `evhypbox`, `evfutbox`; `findingbox`; `keyquestionbox`.
  Use boxes sparingly (at most 2–3 per section) for the statements that matter most; use inline tags at
  the start of paragraphs or table cells where the category is not obvious from wording. Do not tag
  every sentence. Plain wording ("We observed…", "We hypothesize…", "The literature shows…") also
  carries the category.
- Repository references: `\repo{path/to/file}` (clickable link to GitHub; plain path, no escaping of `_`
  needed inside \repo). Code identifiers: `\code{ClaimRecord}`. PoC numbers should point to the artefact
  once, e.g. in a footnote: `\footnote{\repo{research/n3/plc/gapmap.json}, key \code{checks}.}`
- Citations: biblatex authoryear. Use `\textcite{key}` / `\parencite{key}` / `\parencite[p.~5]{key}`.
  Use ONLY keys present in `report/bibliography.bib` (grep it). Honor the key aliases in 00_outline.md.
  If you need a source that is not there, write `\todo{cite: ...}`?? NO — instead leave it uncited and
  list the needed source in your final reply. Never invent a key.
- Cross-references: `\cref{sec:...}`, `\cref{fig:...}`, `\cref{tab:...}`. Use the labels below.
- Tables: booktabs (`\toprule \midrule \bottomrule`), `tabularx` or `p{}` columns for text; caption above
  the table; `\label{tab:...}` after caption. Small font (`\small`) allowed for dense tables. No vertical
  rules. For long tables use `longtable` (loaded? check preamble; if not, keep tables ≤ 1 page).
- Figures: 
  ```
  \begin{figure}[tbp]
    \centering
    \includegraphics[width=\linewidth]{figures/pdf/figNN_name.pdf}
    \caption[Short title]{Caption that says what question the figure answers and how to read it.}
    \label{fig:key}
  \end{figure}
  ```
  Include each figure ONLY in its home section (table below). Other sections reference it with \cref.
- Numbers: use `\num{}` only if needed; plain numbers are fine. Use en-dash for ranges (`3--5`).
  Use `\,` thin spaces sensibly; `p~=`, `n~=`.
- Quotation marks: use \enquote{...}.
- American spelling. English Simplified. No filler, no marketing words (see 00_outline.md rule 1).

## Section keys (labels)

sec:summary, sec:problem, sec:question, sec:foundations, sec:approach, sec:scope, sec:architecture,
sec:evidence-model, sec:evolution, sec:n2, sec:n3, sec:demos, sec:demonstrates, sec:not-demonstrated,
sec:interpretation, sec:threats, sec:residual, sec:validation, sec:platform, sec:education,
sec:organizations, sec:domains, sec:roadmap, sec:workpackages, sec:team, sec:resources, sec:risks,
sec:contributions, sec:impact, sec:conclusion; appendices: app:claims, app:lenses, app:records,
app:defects, app:reproduce, app:glossary, app:method.

## Figures (file → label → home section → owner)

| file (figures/pdf/) | label | home section | what question it answers |
|---|---|---|---|
| fig01_problem.pdf | fig:problem | sec:problem | What part of expert knowledge reaches text, and what does not? |
| fig02_model.pdf | fig:model | sec:approach | What is the whole approach, and which parts exist today? |
| fig03_lenses.pdf | fig:lenses | sec:foundations | Which research method gives which lens, and what missing element does each lens look for? |
| fig04_architecture.pdf | fig:architecture | sec:architecture | How is the implemented PoC built (packages, artefacts, models)? |
| fig05_evidence.pdf | fig:evidence | sec:evidence-model | How does a claim stay tied to its source (provenance chain and labels)? |
| fig06_n2.pdf | fig:n2 | sec:n2 | How much survives each N2 stage in the two live domains? (data) |
| fig07_n3.pdf | fig:n3 | sec:n3 | How does a lens firing become a gap candidate, a retrieval gap, or nothing? (with counts) |
| fig08_closure.pdf | fig:closure | sec:n3 | Does the absence check beat its fair control? (data: it does not) |
| fig09_trace.pdf | fig:trace | sec:demos | One complete real trace from source to expert question |
| fig10_worlds.pdf | fig:worlds | sec:platform | How do public, organizational and human evidence interact? |
| fig11_platform.pdf | fig:platform | sec:platform | What would the full platform contain, and what exists today? |
| fig12_residual.pdf | fig:residual | sec:residual | What is the Human Knowledge Residual and how would it be measured? |
| fig13_validation.pdf | fig:validation | sec:validation | Which studies, in which order, turn candidates into validated predictions? |
| fig14_roadmap.pdf | fig:roadmap | sec:roadmap | Which gated stages lead from PoC to platform? |
| fig15_gantt.pdf | fig:gantt | sec:workpackages | When does each work package run, and where are the milestones? |

## Final reply

≤200 words: files written, approximate page count, any citation you needed but could not find in the
bib, any fact you could not verify, any conflict between notes you noticed.
