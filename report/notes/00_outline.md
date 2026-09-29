# Report outline, terminology and drafting rules (orchestrator, binding)

Working title: **Finding What Experts Leave Unsaid**
Subtitle: *Evidence reconstruction and methodology-guided gap mapping — final report of the
proof of concept, and a research programme for validating it*
Date: September 2026. Author line: Adam Krysztopa (project lead), with AI-assisted analysis
(state in the front matter how the report was produced: multi-agent drafting, human-owned
decisions, every PoC number traced to a repository artefact).

## The central model (improves the user's chain; supported by the PoC)

```
DOMAIN / CAPABILITY  (e.g. "diagnose intermittent PLC faults")
  → 1 RECONSTRUCT      autonomous search of World A evidence, claim extraction, span location,
                       cross-model verification, independence clustering        [PoC: N2]
  → 2 EVIDENCE LEDGER  explicit knowledge model: claim records with epistemic label,
                       verbatim provenance, contradictions, searched-but-UNKNOWN slots [PoC: N1/N2]
  → 3 LENSES           methodology lenses ask "the sources name construct X; do they state
                       its content?" (DISC, DIAG, SEL, HEDGE, GUARD, WHY, RESULT)    [PoC: N3]
  → 4 ABSENCE CHECK    is the missing element really unsaid anywhere in the ledger?
                       ("closure"; THE WEAK LINK in the PoC)                         [PoC: N3]
  → 5 TRIAGE           two different kinds of gap:
                         retrieval gap  → action: search / verify more (never ask a human)
                         gap candidate  → hidden-knowledge hypothesis (label: inferred)
  → 6 QUESTIONS        ranked questions for humans, each with a predicted knowledge type
                       and an elicitation channel (CDM probe, contrasting cases, observation)
  ⇢ 7 HUMAN EVIDENCE   [FUTURE] experts answer; what they add that the ledger lacked is the
                       measured Human Knowledge Residual (World C)
  ⇢ 8 CALIBRATE        [FUTURE] residual outcomes score the gap map (AUROC vs baselines);
                       improve lenses/absence check
  ⇢ 9 APPLY            [FUTURE] learning (instruction that states hidden steps; learner
                       diagnostics from learner data) and organisations (onboarding, retention)
```
Solid = implemented in the PoC. Dashed/⇢ = not built. Figures must follow this convention.

## Terminology (use exactly these; define once; glossary in appendix)

- **explicit knowledge model / evidence ledger** — the N1 `Ledger` of claim records.
- **claim record** — use the real class name from code in technical sections (see 05_architecture.md), "claim record" in prose.
- **epistemic label** — the six labels: observed human evidence, literature-supported,
  organisational-artefact-supported, inferred, synthetic extrapolation, unknown (use code enum names in tables).
- **World A / World B / World C** — public / organisation-specific / human evidence.
- **methodology lens** (not "detector"); **lens firing**.
- **absence check** (the code calls it *closure*; say "absence check (closure)" at first use).
- **gap candidate** (never "gap" alone when meaning a hypothesis record), **retrieval gap**.
- **hidden-knowledge hypothesis** — always labelled inferred; never "hidden knowledge found".
- **Human Knowledge Residual (HKR)** — a research construct: knowledge that competent humans
  hold and use that is absent from the available evidence. Hypothesis-level language only.
- **Validation Track A** — the frozen physics study and its instrument.
- Evidence categories in prose: ESTABLISHED LITERATURE, OBSERVED IN THE PoC, INTERPRETATION,
  HYPOTHESIS, FUTURE WORK — use the template's boxes/tags (see 10_visual_language.md).

## Structure (file → content → primary notes → figures)

Front matter: title page; "How to read this report" (the five categories, figure convention);
contents.
- `sections/00_executive_summary.tex` — 1.5–2 pages. Problem, idea, PoC, main result (works as
  engineering; prediction not demonstrated; absence check is the bottleneck), limitations, why
  further research matters, what we ask for. Written LAST.

Part I — Problem and approach
- `01_problem.tex` — experts skip automated steps; omission evidence (surgery/CTA numbers,
  NICU cues, programmers); reporting bias in text; one education and one organisational
  example; why it matters. Fig 1 (explicit vs hidden knowledge).
- `02_question.tex` — RQ-B; hypotheses H1 (reconstruction with provenance is feasible),
  H2 (lenses + absence check locate where the reconstruction is thin in a way that predicts the
  human residual better than strong baselines), H3 (prioritized questions cut expert time);
  the falsifier (ΔAUROC upper bound < δ). Which of these the PoC could touch (H1 partly, H2
  mechanism only).
- `03_foundations.tex` — DtD, CTA/CDM/PARI, expert–novice & expert blind spot, PCK,
  threshold concepts, conceptual change, tacit knowledge (Polanyi, Collins), KM, reporting
  bias, ECD/KLI; each with "what it contributes to this system"; table methodology → lens;
  "investigated but not central". Fig 4 (lenses from methodologies).
- `04_approach.tex` — synthesis: from existing methods to the proposed approach; the central
  model figure (Fig 2); what is known / adapted / new (novelty ledger table); closest work.

Part II — The proof of concept
- `05_scope.tex` — what the PoC was meant to demonstrate and not; zero-participant constraint;
  how the project reached this design (Track A → reorientation, one page max, not a diary).
- `06_architecture.tex` — implemented architecture (Fig 8), packages, models, determinism.
- `07_evidence_model.tex` — claim record, labels, provenance chain, UNKNOWN, contradictions,
  independence, worlds, residual accounting, frozen schema. Fig (provenance chain) optional.
- `08_evolution.tex` — N0–N3 in one table + short text; registered verdicts.
- `09_n2.tex` — N2 implementation and results: E-LIVE numbers, defects found live, E-PLANT/
  E-ABST designs and INCONCLUSIVE verdicts, budget stop; what it taught. Fig 3.
- `10_n3.tex` — lenses, absence check, triage, ranking by breadth, questions, checks; results
  per domain; closure-control failure; precision 3/19; stability. Fig 5.
- `11_demonstrations.tex` — 2–3 complete real traces (source → span → claim → lens → gap →
  hypothesis → question), one failure trace. Fig 6.
- `12_demonstrates.tex` — what the PoC demonstrates (table with strength + artefact).
- `13_not_demonstrated.tex` — mandatory; explicit list.
- `14_interpretation.tex` — scientific interpretation; the absence check as bottleneck;
  thinness vs residual; what would change our mind.
- `15_threats.tex` — threats to validity (construct, internal, external, statistical,
  contamination, in-sample tuning, single operator, AI-assisted development).

Part III — Research programme
- `16_residual.tex` — HKR as a construct/hypothesis; how it would be measured. Fig 10.
- `17_validation.tex` — validation programme V0..Vn with gates. Fig 11.
- `18_platform.tex` — three evidence worlds (Fig 7) and future architecture (Fig 9);
  implemented vs next stage vs long-term; Weft as optional future World B layer.
- `19_education.tex` — education application.
- `20_organisations.tex` — organisational application.
- `21_domains.tex` — domain strategy (scientific vs commercial validation domains).
- `22_roadmap.tex` — gated stages PoC→…→Full platform. Fig 12.
- `23_workpackages.tex` — WPs derived from the programme. Fig 13 (WP/Gantt) optional.
- `24_team.tex` — lean / grant-scale / product teams; why, when, FTE.
- `25_resources.tex` — resources and indicative timeline (orders of magnitude, no fake precision).
- `26_risks.tex` — risks, kill criteria, pivots.
- `27_contributions.tex` — expected scientific contributions (graded).
- `28_impact.tex` — expected practical impact (sober).
- `29_conclusion.tex`.

Appendices
- `A_claim_evidence.tex` — the PoC claim/evidence table (from 01_evidence_audit.md).
- `B_lenses.tex` — lens specifications (firing rule, missing element, type, channel).
- `C_records.tex` — record/JSON excerpts.
- `D_defects.tex` — defects found by live runs and adversarial reviews, and fixes.
- `E_reproduce.tex` — how to reproduce (commands, run IDs, hashes).
- `F_glossary.tex` — glossary and acronyms.
- `G_method.tex` — how this report was produced and verified (agents, reviews, audit).

## Drafting rules (every section author)

1. English Simplified, American spelling. Short sentences. One idea per paragraph. No
   "leverage", "robust", "cutting-edge", "novel" (unless graded), "holistic", "synergy",
   "paradigm", "unlock", "seamless", "state-of-the-art" (unless literal), "delve".
2. Every important statement carries its category (box, tag, or explicit wording).
   PoC numbers cite the artefact path in a footnote or \artefact{} macro.
3. Cite with \textcite/\parencite from `bibliography.bib` keys only. No invented keys.
4. Never draw or describe a future component as existing.
5. Prefer a clear table or figure to a long list. No bullet-point walls.
6. Section length budgets are in the task prompt; respect them.

## Orchestrator consistency rulings (binding)

- Test counts: use the counts from actually running the suites (01_evidence_audit.md):
  residual 268, reconstruct 416, gapmap 172 (~2 min), instrument 311 passed. The grep-based
  counts in 05_architecture.md (153/342/161) count test functions, not collected tests; do not use them.
- N3 PLC #1 in the final map is a DIAG record; the "loose terminal" DISC record appears only in the
  pre-final prototype (spec §9) and must be labelled as such if mentioned.
- Numbers in `docs/plans/n3-poc-lens-spec.md` §8/§9 are pre-review prototype numbers; the committed
  `research/n3/*/gapmap.{md,json}` are authoritative.
- Expert questions are template-generated (Python f-strings with verbatim quotes), not LLM-generated.
- Precision "3 of 19 strict (8 of 19 lenient)": stated in `research/n3/README.md` and `PROGRESS.md`
  from an adversarial AI (Opus) review of the PRE-FINAL maps; the per-record tally is not committed
  as a data file, and the final maps were not re-tallied. Always state it with those qualifiers; never as
  a measured precision of the final maps.
- Closure own-rate vs fair-control rate (from JSON): PLC 0.889 = 0.889, GDPR v1 0.961 = 0.961,
  GDPR v2 0.958 = 0.958 (README rounds to 0.89/0.96/0.96).
- Weft: a retrieval engine indexing .txt/.md/.pdf with source link + SHA-256 of the document, no
  in-document span positions, no per-user access control. Integration NOT justified now; possible
  later as a World B candidate-passage provider only (edu_proj re-hashes, locates, verifies). Needs a new ADR.
- Lexical donor null and other N3 checks: use the numbers in the committed final `research/n3/*/gapmap.json`
  `checks` blocks (e.g. PLC observed 22 vs null [26, 41] per 04_results.md). The README's figures
  (42 vs [33, 47] …) are the earlier reviewer figures on pre-final maps; if quoted, say so.
- PLC ranking correlates with source density (Spearman 0.91; J10 with ten highest-density 0.58): the
  anti-renaming check excludes "low density renamed", not "high density renamed". Report this.
- 13 of 16 final candidates are in the "partial" closure state (04_results.md).
- N2 recorded spend ≈ $4.82 against a $5/week key limit.
- Omission evidence: NEVER write "experts omit ~70% of what they know" as an established fact. Use the
  primary numbers with n and domain: Sullivan et al. 2014 (3 surgeons, one procedure; 73% of decision
  steps omitted); Chao & Salvendy 1994 (6 programmers; no single expert reported >41% of diagnostic
  actions / >29% of interpretations); Crandall & Getchell-Reiter 1993 (NICU cues, 25 of 70 absent from
  literature) — check exact wording in 02_foundations.md. The ~70% figure may be mentioned only as a
  widely repeated secondary claim whose primary basis is thin.
- The literature supports the lens CONSTRUCTS, not the lenses themselves. Say so.
- Ranking in the PoC is a rubric/breadth score (`gapmap/src/gapmap/rank.py`), NOT expected information
  gain. EIG question selection is FUTURE WORK (N6). Never imply EIG is implemented.
- "GAPMAP" is also the name of Salem et al. 2025; in prose say "gap map", and `gapmap` only for the package.
- Novelty wording: use 03_novelty.md §4 paragraph; do not claim "no product separates documented from
  expert-only knowledge" (Interloom press coverage). Do not cite van den Bent et al. as a published result.
- Bibliography: `report/bibliography.bib` (merged, deduplicated). Key aliases — use the LEFT key:
  tofelgrehl2013cognitive (not tofelgrehl2013cta), cui2025large (not cui2025replication),
  hestenes1992force (not hestenes1992fci), stamper2011human (not stamper2011datashop),
  disessa1993toward (not disessa1993pieces).
- SPELLING: American English everywhere in prose: "program" (research program), "organization",
  "organizational", "artifact", "prioritize", "modeling", "labeled", "behavior". Keep British spellings
  only inside code identifiers/paths in \texttt (e.g. `organisational_artefact_supported`, `research_notes/`).
  Subtitle becomes "... and a research program for validating it".
- Domains: PLC and GDPR (the in-sample tuning ledgers) may be used for pilots only; decisive studies use
  held-out domains/subdomains reconstructed for the first time AFTER the config freeze (11_programme.md wins over 07).
- Education: instruction and learner-facing material use only claims validated by human evidence
  (06_platform.md §2.12 wins over 09_edu.md §5). Unvalidated gap candidates never reach learners.
- Grant scale and roadmap: 11_programme.md (S0–S6, WP1–WP11, MS1–MS8) is authoritative.
- Gap-map counts: `map` arrays hold one CONTROL record each (lengths 10/2/7); HYP gap candidates are
  PLC 9, GDPR v1 1, GDPR v2 6. RG-UNK counts in gapmap.json are 10/28/44 (PLC/v1/v2); the ledger-level
  UNKNOWN slot counts are a different quantity — never mix them. One GDPR v2 RG-SIBLING record still carries a
  question/hypothesis: do not claim retrieval gaps never carry questions; say their action is search/verify.
- HYPOTHESIS NAMES (report-wide): H1 = reconstruction with provenance is feasible and checkable;
  H2 = lenses + absence check predict the human residual better than the strongest baseline (THE central
  hypothesis; REORIENTATION.md, 04_results.md, 07_validation.md and 11_programme.md call this "H1");
  H3 = prioritized questions cut expert time. When a note says "H1" for the central hypothesis, write H2.
  The pivot hypothesis in 11_programme.md ("H3: targeted interviewing without reconstruction") must be
  renamed in prose (e.g. "the interview-only pivot") so it does not clash with H3.
