# Revision decisions after Review Round 2 (orchestrator, binding)

Inputs: `review_C.md` (hostile grant reviewer: C1–C3, M1–M9, minor, reject reasons, flip conditions) and
`review_D.md` (clarity and reproducibility). Also still binding: `revision_R1.md` except where this file
changes it (the gate structure below REPLACES D2 of revision_R1.md). Accept all review findings that
locate to your files unless a decision below says otherwise. Check before you change: reviewer claims
about the repository must be verified in the artifact.

## The restructured program (replaces R1-D2; must read identically everywhere)

The central change: the program no longer asks for money before its cheapest decisive test has run, and
each tranche of money is released only by a gate reading CONTINUE.

**Phase 0 — V1 closure study, before any grant submission (recommended next action).** Owner-run, within
the NOW program's one permitted human input (a blind second coder, who labels and does not participate).
Scope: the 107 admissible lens firings plus new units to reach at least 100 double-coded units; a
non-owner blind coder; human–human κ (three states closed/partial/open, weighted; gating split closed vs
not closed); a corpus-level retrieval-recall check (is the element stated anywhere in the ledger's
sources, not only in the retrieved sentences — review C M2); a panel of candidate judges scored against
the fair control. Cost: small (coder hours plus local compute; give an order of magnitude only). Gate
**MS2 (closure verdict)**: CONTINUE if human κ ≥ 0.70, retrieval recall meets its pre-registered floor, and
at least one judge beats the fair control by the pre-registered margin; otherwise STOP the automated absence
check → pivots (reconstruction-with-provenance as an audit tool; interview-only).
The report says plainly: the V1 numbers should be on page 1 of any grant proposal; this report is the
design for them.

**Phase 1 — lean methods grant (≈ EUR 0.3–0.5M, ≈ 12–15 months), released only on MS2 CONTINUE.**
Build the area score, freeze the configuration (two-step freeze: judge chosen at MS2, then hash-freeze
lexicons, thresholds, judge and area score; then acquire gold), validate the chosen judge on the text type
of the later studies (review C M3), and run **V2 as a POOLED retrospective study over several published
CTA golds** (plus V4 residual check on V2 data). Pre-register the incremental analysis: the map's value
over density and area size (conditional AUROC within density strata, or incremental value in a model
already containing density and area size; report the partial correlation before MS1) — review C M4.
Gate **MS3 = screening gate for Phase 2 money, not a verdict on H2**: CONTINUE (release Phase 2) only if
the pooled retrospective ΔAUROC has point estimate ≥ δ AND lower 90% bound > −δ/2 AND the map adds value
over density and area size; otherwise STOP H2 funding and take the interview-only pivot (costed separately).
There is no "inconclusive → continue anyway" route and no second-inconclusive rule any more: MS3 either
releases Phase 2 or it does not.

**Phase 2 — full program, released only on MS3 CONTINUE.** **V5 (blind prospective elicitation) decides H2
as defined** (the human residual), and is BUDGETED FOR POWER: enough areas for δ = 0.05 (about 150 per
class), with each area rated by 3 experts and each expert covering many short area probes; state the
expert-hours this implies honestly and cost it. Gate **MS5 (H2 verdict)**: STOP if the upper 90% bound of
ΔAUROC < δ; CONTINUE if the lower 90% bound > 0 and the point estimate ≥ δ; otherwise the reading is
inconclusive and is reported as not supporting H2 (terminal for H2 funding). V6 tests H3 (superiority at
1.25 items per expert hour; a null counts against it). V7 organizational pilot and V8 learner link follow
their own gates.

**V3 (E-OSS) is re-labeled as a separate hypothesis on the organizational path** ("H-OSS: the gap map,
adapted to code and commit evidence, predicts where knowledge is lost when developers leave"). It needs
the Git adapter and code lenses, is scheduled with the organizational track (after its components exist),
and can neither kill nor license H2.

**External gate reader.** An independent statistician (or a small advisory board with one) reads MS2, MS3
and MS5 against the pre-registration and has authority over them. Any owner exception requires the gate
reader's sign-off. Acknowledge honestly that the N2 → N3 step was an owner exception without such a reader
(review C M6).

**Team status, stated honestly.** No host institution, named PI record, statistician, CTA collaborator or
letters exist yet; the PoC was built by a single operator with AI assistance. List what must be named
before submission. Never invent names or commitments.

## Other decisions

R2-1 (M8). The Executive summary leads with the result: "The absence check ties its fair control;
prediction of hidden knowledge is untested." Then the recommendation (Phase 0 V1 before any grant). The
build inventory comes after. No grant-speak ("first bounded test of the idea" etc.).
R2-2 (M7). Add Torre et al. 2020 (RE; construct-based completeness checking of GDPR text), Anthonio et al.
2020/2022 (underspecification in instructional text), DRMiner 2024 (rationale mining from issue trackers),
Foucault et al. 2015 (developer turnover and quality) — only after verifying each via Crossref/OpenAlex;
add to bibliography.bib; revise the novelty ledger down where they overlap.
R2-3 (M9). Surface the decoy false-accept rate (≈35% on PLC per review C — verify in the artifact) in §9's
main text, with what it means.
R2-4 (M5b). Specify where E-CTA's dated corpora come from (web archive snapshots / publication-dated
sources) and the memorization probe.
R2-5 (review D). The interview-only pivot must never be labeled H3 (22_roadmap.tex:56,
23_workpackages.tex:143). Define H3 and a_U before use in the Executive summary, or avoid them there.
Rewrite the 25 worst sentences listed in review_D.md; bring sentences over 35 words down, priority §6,
§22, §7, §3. Fix the §23 "Milestones" heading float (place the table with [H] or after the heading with
\FloatBarrier; placeins is now loaded in the preamble).
R2-6 (contradictions). Maries & Singh: one description at its true grain everywhere (TAs 65%, instructors
68%, no significant difference, above the 40% chance level per the paper — verify). pytest-archon: say
what the code actually has (hand-written import-boundary checks with ast; no pytest-archon install) —
verify. Appendix "How this report was produced": describe both review rounds as completed.
R2-7. Figures 13 and 14 will be redrawn by the orchestrator's figure agent to this structure; section
authors update their captions only.

## Assignment

- R2-a (Opus): 02_question, 16_residual, 17_validation — the restructured program in full (Phase 0–2, V1
  scope, pooled V2, MS3 screening, V5 powered with expert-hours, MS5 rule, V3 re-labeled, conditional
  analysis, judge validation on text type, dated corpora).
- R2-b (Opus): 21_domains, 22_roadmap, 23_workpackages, 24_team, 25_resources, 26_risks,
  I_programdetail — phases with euro tranches released by gates, pivot costed separately, lean schedule
  re-costed by month and consistent with Phase 0/1, V3 moved to the organizational track, external gate
  reader, team status, H3-label fix, float fix, sentence simplification in these files.
- R2-c (Opus): 00_executive_summary, 03_foundations, 04_approach, 08_evolution, 09_n2, 14_interpretation,
  27_contributions, 28_impact, 29_conclusion — R2-1, R2-2, R2-3, R2-6 (Maries), M6 acknowledgement in §8,
  Phase 0 recommendation in summary and conclusion, sentence simplification in these files.
- R2-d (Sonnet): clarity pass on 01, 05, 06, 07, 10, 11, 12, 13, 15, 18, 19, 20 and appendices A–I —
  review_D sentence rewrites and terminology, R2-6 (pytest-archon in 06; Maries wherever it appears in
  these; appendix method statement), any C/D finding locating to these files. No content changes beyond
  the findings; keep every number.

Budgets: keep the main body ≤ ~98 pages. Keep labels stable. Compile in a scratch copy
(rsync -a --exclude build --exclude notes report/ <SCRATCH>/<name>/; latexmk -r latexmkrc main.tex).
Final reply ≤ 200 words: applied IDs, rejected IDs with reason, page counts.
