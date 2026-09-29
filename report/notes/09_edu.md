# 09 — Education path: from gap map to learner benefit

Author: Education Researcher agent. Categories follow `00_outline.md`: ESTABLISHED LITERATURE,
OBSERVED IN THE PoC, INTERPRETATION, HYPOTHESIS, FUTURE WORK. Terminology follows the same
file (World A/B/C, gap candidate, retrieval gap, hidden-knowledge hypothesis, Human Knowledge
Residual = HKR, Validation Track A).

Repo leads used: `ai_education_research_map.md`; `research/explore-{pedagogical-content-
knowledge,conceptual-change,threshold-concepts,intelligent-tutoring-systems,knowledge-tracing,
llm-tutoring,worked-examples-self-explanation,formative-assessment,cognitive-apprenticeship,
concept-inventories}.md`; `research/experiment-ai-assisted-cta-physics.md`; `research/
roadmap.md`; `REORIENTATION.md` §2, §7, §22 (N4); `research_notes/Tacit knowledge
reorientation/synthetic_cohorts.md`.

---

## 1. Expert blind spots in physics education (ESTABLISHED LITERATURE)

Three converging findings, each independently replicated in physics or a closely adjacent
population:

1. **Principle selection, not surface features, is what experts see and novices miss.**
   Physics experts categorize problems by the governing principle (conservation of energy,
   Newton's second law); novices sort by surface objects ("inclined-plane problems," "pulley
   problems") (Chi, Feltovich & Glaser 1981). This is the founding expert–novice result in
   physics and the reason `research/experiment-ai-assisted-cta-physics.md` chose "selecting and
   combining conservation principles" as its Stage A/B topic.
2. **Experts and instructors cannot reliably predict which student difficulties are common.**
   University physics TAs and instructors, asked to predict students' most common wrong answer
   on the Force Concept Inventory, scored 65% and 68% of the maximum (chance-level simulated
   guessers: 40%); instructors did not outperform TAs, and both missed many difficulties that
   persist after traditional instruction (Maries & Singh 2016). The same pattern replicates on
   kinematics graphs (Maries & Singh 2013) and E&M (Karim, Maries & Singh 2018).
3. **The expert blind spot is general, not physics-specific, and gets worse with more expertise
   in the domain.** Preservice teachers with more mathematics training ranked symbolic algebra
   problems as easier than word problems — the reverse of students' actual performance (Nathan &
   Petrosino 2003, N = 48). This is the named "expert blind spot" and the source of the map's
   rule in `REORIENTATION.md` §2: "mis-modelled novice difficulty ... needs learner data, not
   experts and not text written by experts."

Instructors skipping representation steps (drawing a free-body diagram, defining variables
before writing equations) is the map's own worked example of tacit omission: in the one
university-physics intelligent-tutoring-system evaluation with a rubric fine enough to see it,
practice gains concentrated in drawings (d = 1.21) and variable definitions (d = 0.69), not in
equations (d = 0.11) or final answers (d = −0.08) — the steps instructors do not think to state
explicitly are exactly the steps a tutor that enforces them improves (VanLehn et al. 2005, Andes
at the US Naval Academy; non-randomized).

## 2. The education pipeline: gap map → expert questions → captured residual → instructional
material → learner diagnostics → adaptive practice

| Step | What it does | Evidence status | Data needed |
|---|---|---|---|
| Gap map (N3 PoC) | Methodology lenses flag constructs sources name but do not state the content of (rationale, selection rule, cue) | OBSERVED IN THE PoC (pipeline runs end to end; `research/n3/README.md`) but **prediction not demonstrated**: adversarial review found precision 3/19 strict on the pre-final maps, and the absence-detection step does not beat a fair control (`research/n3/README.md`) | Curated World A text; N2 evidence ledgers |
| Expert questions | Ranked gap candidates become prioritized questions, each tagged with a predicted knowledge type and an elicitation channel (CDM probe, contrasting cases, observation) | OBSERVED IN THE PoC as an artefact (the pipeline emits questions); HYPOTHESIS that the questions target real residual, since N3's own gate (N5, residual measurement against gold) has not run | Gold task lists / expert-corrected answers for calibration (`REORIENTATION.md` §19) |
| Captured residual | An expert answers a question; what the expert adds that the ledger lacked is the measured HKR (World C) | FUTURE WORK. No human answers exist yet outside the frozen Track A, which is a separate, registered study, not an N3 output | Human time (LATER/Track A only, not NOW) |
| Instructional material | CTA-based instruction, and worked examples that make a recovered operation explicit via a self-explanation prompt rather than added text | ESTABLISHED LITERATURE that CTA-based instruction beats other or conventional methods for identifying content, in a meta-analysis of a few, small studies (Hedges g = 0.871; Tofel-Grehl & Feldon 2013); ESTABLISHED that provided explanations added to worked examples give minimal benefit versus prompts that make the learner generate the step (Wittwer & Renkl 2010; Bisra et al. 2018, self-explanation g = 0.35 over instructional explanation, k = 6) | The recovered operation, in the form the experiment specifies: performed in a worked step, carried by a self-explanation prompt, in at least two of four worked examples |
| Learner diagnostics | Item response or dialogue used to infer what a learner is missing | ESTABLISHED LITERATURE that this must use learner data, not expert or LLM prediction (Nathan & Petrosino 2003; Maries & Singh 2016 above); ESTABLISHED that a single item response is a poor diagnostic unit — 31% of Force Concept Inventory answers changed on a one-week retest despite total-score reliability r = 0.89 (Lasry et al. 2011) | Item-level or dialogue-level learner response logs, several observations per construct, not one |
| Adaptive practice | A policy (knowledge tracing, mastery rule, LLM tutor) that changes what a learner sees next | ESTABLISHED that prediction of the next response is solved well enough by interpretable models (extended BKT, logistic regression) and that *learning* gains from knowledge-tracing-driven redesign are real but small, short, and concentrated in hand-picked units (Liu & Koedinger 2017, d = 0.47, N = 91, immediate; a 2026 replication on units chosen by topic found no difference — Lyu et al. 2026); ESTABLISHED that no study has tested a knowledge-tracing-driven policy against a simple mastery rule (N-correct-in-a-row) on a delayed or transfer outcome | Logged practice data per skill, and a comparison arm against a simple heuristic |

The pipeline is therefore evidence-complete only up to "instructional material." Everything from
"learner diagnostics" onward needs real learner data the project does not yet have (NOW has
zero participants), and even with that data the map's own graded evidence (§1 above) shows every
later stage has a modest, mostly-immediate effect ceiling, not a large one.

## 3. Where learner evidence enters, and why synthetic learners predict but never decide

**Where it must enter.** `REORIENTATION.md` §2's own table is explicit: "What is difficult?"
has one primary evidence source — learner response data and error logs — and two things that
cannot answer it: experts, and text written by experts (including LLM output conditioned on
that text). This is not a preference; it follows directly from finding 2 above (experts and
instructors predict student difficulty only slightly better than chance) and from the general
literature on knowledge-in-pieces versus framework theory, both of which imply that whether a
learner uses an intuitive idea is context-dependent and only observable in that learner's actual
responses (Vosniadou & Brewer 1992; diSessa 1993).

**Why synthetic learners can be a predictor but never a criterion.** The evidence-note
`research_notes/Tacit knowledge reorientation/synthetic_cohorts.md` reviews this in depth and the
verdict is unambiguous for physics specifically:

- LLM-simulated students achieve moderate item-difficulty correlations with real cohorts
  (r ≈ 0.72–0.82) only in favorable, aggregate, ensembled settings (Lu & Wang 2024; Liu, Bhandari
  & Pardos 2024).
- They fail at the properties a diagnostic needs: the "competence paradox" (unguided LLMs
  outperform the learner they are meant to imitate at every grade; Srivatsa, Maurya & Kochmar
  2025), near-zero "misconception faithfulness" under corrective feedback (Selective Flip Score
  ≈ 0; Do, Sonkar & Sachan 2026, preprint), and — directly on this project's target population —
  a GPT-4 simulation of the Force Concept Inventory showed *no response variance at all* when
  told to answer as a different cohort, and only reproduced human-like variance when explicitly
  told which preconception to hold (Kieser, Wulff, Kuhn & Küchemann 2023). A surrogate cohort
  therefore returns the misconception taxonomy it was given; it cannot discover a new one or
  report its prevalence.
- Social-science replications of the same method show synthetic respondents under-disperse and
  over-detect effects that are null in real humans in 68–83% of cases (Cui, Li & Zhou 2025) —
  the worst possible bias for a project whose gates are falsification tests.

INTERPRETATION: synthetic learners belong at the "instrument and pipeline debugging" and
"hypothesis generation" tiers only (known-truth simulation, candidate misconception and probe
generation) — never as evidence for a gate, a power calculation, or a claim about prevalence or
individual learner state. This mirrors, at the learner layer, the rule `REORIENTATION.md`
already states for surrogate experts (§12).

## 4. How the frozen Validation Track A fits, unchanged

Track A (`research/experiment-ai-assisted-cta-physics.md`, `research/roadmap.md`) is not an
output of the NOW gap-map pipeline and does not depend on N3 succeeding. It is a separately
registered, gated study that starts only on its own preconditions (experts, a course, ethics),
and its registered rules are used unchanged:

- **Stage A** (12 physicists, within-expert): ordinary explanation → non-directed think-aloud →
  retrospective CDM-style probes, AI-led on one problem set and human-led on the other,
  counterbalanced. **K1** passes only if the AI-assisted pipeline yields at least 3 new shared
  operations, at least 2 of them AI-probe-added (not merely corroborated in the trace), and the
  AI-minus-human contradicted-rate 95% CI upper bound is at most 15 pp.
- **K0** (before Stage B; also run "early," on an earlier course offering, before the 12 experts
  are even recruited): codes about 100 errored open-response conservation-problem solutions;
  stops the study if under 30% of first errors are principle-selection or representation errors,
  i.e. if the bottleneck this topic targets does not actually show up in real student work.
- **Stage B** (~370 first-year students, two-arm RCT, both arms static worked examples with
  self-explanation prompts, delayed transfer 2–3 weeks out as the primary, correctness-only
  outcome): a pre-registered **futility test at SESOI d = 0.30**, valid only if compliance is at
  least 70% per arm. **K2** kills the "teach the elicited operations" claim for this topic if the
  90% CI upper bound sits below d = 0.30.

**How it connects to the education pipeline above (INTERPRETATION, not a registered rule):**
Stage A is the human-answered version of "expert questions → captured residual" (row 2–3 of the
table); its K0 is the human-data check that a candidate bottleneck is real, which is exactly what
an N3 gap candidate would need before being trusted; and Stage B is the "does the captured
residual, turned into instructional material, move a learner outcome" test, with the field's own
worked-examples evidence (§5.8 of the map) predicting the true effect is probably below the
SESOI, which is why Stage B is framed as a futility test rather than a discovery study. None of
this changes a single Track A number: additions from NOW (e.g., a sealed, unopened N3/N2
reconstruction of the same topic, compared post hoc to Stage A's coded operations under E-SEAL)
are pre-registered as secondary and non-gating, per `REORIENTATION.md` §18.1 and §20.

## 5. A candidate education pilot for the gap-map → instruction pathway

**Purpose.** Test whether a gap-map-derived instructional addition (not an elicited-from-live-
experts one, since NOW has zero participants) changes anything measurable, at the smallest
defensible scale, before proposing any learner-facing deployment.

- **Setting.** One introductory university mechanics course, one topic already used in the
  frozen instrument (conservation-principle selection), so materials and the EMCS secondary
  measure (Singh & Rosengrant 2003, excluding items Q16/Q22/Q23 per Wu, Li & Rebello 2025) can
  be reused without a new validity argument.
- **Participants.** ~370 first-year students (Stage B's own power calculation, r = .4 pretest
  correlation, 20% attrition, d = 0.30 SESOI), or, as a smaller first pass, one section (~100–150
  students) run only as a manipulation check on time-on-task and prompt-answer rates, not as a
  powered outcome study.
- **Materials.** Two arms of the same static worked-example module. Both carry the same number
  of self-explanation prompts from one fixed stem list. The treatment arm's prompts carry one or
  two operations proposed as "candidate" by the gap-map pipeline on this topic's public evidence
  base (textbook chapters, published problem-solving frameworks), explicitly labeled as
  **inferred, unvalidated candidates**, not as recovered expert knowledge.
- **Measures.** Delayed transfer (2–3 weeks), correctness-only scoring, by instructors blind to
  the operations list (guards against test-alignment inflation; Kulik & Fletcher 2016); logged
  time on task and prompt completion (manipulation check); EMCS pre/delayed as an exploratory,
  arm-level secondary measure only, since no item subset is individually validated.
- **Controls.** Same design discipline as Stage B: word-count and time matched arms, identical
  prompt stems and counts, answers locked before a model answer is shown, a pre-set compliance
  floor (≥70% of prompts answered, ≥60 of 80 logged minutes) before any effect is interpreted.
- **What this pilot would NOT claim, even on a positive result:**
  - It would **not** claim the gap map found "hidden expert knowledge" — its inputs are public
    text, and its candidates are unvalidated against any human gold (N3's own closeout: pipeline
    complete, prediction not demonstrated).
  - It would **not** claim individual-learner diagnosis — any inventory or dialogue-based
    measure used is validated for cohort/class comparison only (Madsen, McKagan & Sayre 2017);
    single-item answers are not stable enough for one student (Lasry et al. 2011).
  - It would **not** substitute for, compare against, or gate Track A. A positive or negative
    result here says nothing about whether AI-assisted expert elicitation (Track A's actual
    question) works; it only tests whether a text-derived candidate operation, taught the same
    way Track A's treatment is taught, moves a learning outcome at all.
  - It would **not** use synthetic learners for anything beyond generating candidate prompts to
    pilot before real students see them (§3 above).

---

## Notes on citation verification

All DOIs below were checked to resolve on Crossref (`https://api.crossref.org/works/<doi>`) and
the returned title/authors/venue/year match the citation as used. arXiv preprints are marked as
such and are cited only for descriptive claims about method or existence, never as the sole
support for an effect-size claim used above.

- `chi1981categorization` — verified via Crossref: title "Categorization and Representation of
  Physics Problems by Experts and Novices," Chi/Feltovich/Glaser, *Cognitive Science*, 1981.
- `nathan2003expert` — verified: "Expert Blind Spot Among Preservice Teachers," Nathan &
  Petrosino, *American Educational Research Journal*, 2003.
- `maries2016teaching` — verified: title on Crossref matches (TAs and FCI difficulties), Maries
  & Singh, *Phys. Rev. Phys. Educ. Res.*, 2016.
- `vanlehn2005andes` — used as in `explore-intelligent-tutoring-systems.md`; DOI is the IJAIED
  "Five Years of Evaluations" journal record (`10.3233/irg-2005-15(3)02`), full text was read by
  that branch's own verification (OLI-hosted PDF).
- `tofelgrehl2013cta` — verified: "Cognitive Task Analysis-Based Training," Tofel-Grehl & Feldon,
  *Journal of Cognitive Engineering and Decision Making*, 2013.
- `wittwer2010explanations` — carried from `explore-worked-examples-self-explanation.md`
  (verified there); not re-verified independently here beyond confirming the DOI resolves.
- `bisra2018selfexplanation` — carried from the same branch.
- `lasry2011fci` — verified: DOI resolves to the Lasry et al. FCI test-retest paper (used in
  `explore-concept-inventories.md`).
- `liu2017closing` — carried from `explore-knowledge-tracing.md`.
- `lyu2026redesign` — carried from `explore-knowledge-tracing.md` (Springer LNCS record).
- `madsen2017inventories` — carried from `explore-concept-inventories.md`.
- `kieser2023chatgpt` — verified: "Educational data augmentation in physics education research
  using ChatGPT," Kieser/Wulff/Kuhn/Küchemann, *Phys. Rev. Phys. Educ. Res.*, 2023.
- `srivatsa2025naep` — arXiv preprint (BEA@ACL 2025); existence confirmed via arXiv abstract
  page (2507.08232), carried from the repo's own synthetic-cohorts note.
- `do2026selectiveflip` — arXiv preprint (2605.12748); existence confirmed via the repo's own
  synthetic-cohorts note; not independently re-fetched (preprint, not peer-reviewed — used only
  for the descriptive "near-zero Selective Flip Score" claim, not as the sole evidentiary basis
  for any gate-relevant statement in this report).
- `cui2025replication` — verified: DOI `10.1038/s43588-025-00840-7` (Nature Computational
  Science) resolves in the synthetic-cohorts note's own citation check; used descriptively.
- `posner1982accommodation` — verified: "Accommodation of a scientific conception," Posner et
  al., *Science Education*, 1982.
- `sadler2013influence` — verified: "The Influence of Teachers' Knowledge on Student Learning in
  Middle School Physical Science Classrooms," Sadler et al., *AERJ*, 2013.
- `bao2006model` — verified: "Model analysis: Representing and assessing the dynamics of student
  learning," Bao & Redish, *Phys. Rev. ST-PER*, 2006.
- `schroeder2022refutation` — verified: "Refutation Text Facilitates Learning," Schroeder &
  Kucera, *Educational Psychology Review*, 2022.
- `sweller1988cognitive` — verified: "Cognitive Load During Problem Solving: Effects on
  Learning," Sweller, *Cognitive Science*, 1988 (DOI `10.1207/s15516709cog1202_4`).
- `collins1989apprenticeship` — verified: "Cognitive Apprenticeship: Teaching the Crafts of
  Reading, Writing, and Mathematics," Collins/Brown/Newman, Routledge reissue, 2018 (original
  1989 chapter).
- `hestenes1992fci` — verified: "Force concept inventory," Hestenes/Wells/Swackhamer, *The
  Physics Teacher*, 1992.
- `stamper2011datashop` — verified: "Human-Machine Student Model Discovery and Improvement
  Using DataShop," Stamper & Koedinger, AIED 2011 (Springer LNCS).
- `corbett1995knowledge` — verified: "Knowledge tracing: Modeling the acquisition of procedural
  knowledge," Corbett & Anderson, *User Modelling and User-Adapted Interaction*, 1995.
- `vanlehn2011relative` — verified: "The Relative Effectiveness of Human Tutoring, Intelligent
  Tutoring Systems, and Other Tutoring Systems," VanLehn, *Educational Psychologist*, 2011.
- `kestin2025aitutoring` — verified: "AI tutoring outperforms in-class active learning,"
  Kestin/Miller/Klales/Milbourne/Ponti, *Scientific Reports*, 2025.
- `bastani2025generative` — verified: "Generative AI without guardrails can harm learning,"
  Bastani et al., *PNAS*, 2025.
- `barbieri2023metaanalysis` — verified: "A Meta-analysis of the Worked Examples Effect on
  Mathematics Performance," Barbieri et al., *Educational Psychology Review*, 2023.
- `lichtenberger2024formative` — verified: "Enhanced conceptual understanding through formative
  assessment," Lichtenberger/Hofer/Stern/Vaterlaus, *Educational Assessment, Evaluation and
  Accountability*, 2024.
- `kaser2024simulated` — verified: "Simulated Learners in Educational Technology: A Systematic
  Literature Review and a Turing-like Test," Käser & Alexandron, *IJAIED*, 2024.
- `doroudi2019wheres` — verified: "Where's the Reward?," Doroudi/Aleven/Brunskill, *IJAIED*,
  2019.
- `wang2020neuripschallenge` — arXiv preprint 2007.12061, "Instructions and Guide for Diagnostic
  Questions: The NeurIPS 2020 Education Challenge" (Wang, Lamb, Saveliev et al.); this is the
  Eedi NeurIPS 2020 dataset paper referenced in `REORIENTATION.md` ref [138]; licence for the
  underlying data is explicitly marked unverified there, and the same caveat is kept here.
- `diSessa1993pieces` and `vosniadou1992framework` — carried from `explore-conceptual-
  change.md` (both independently verified there).

Not put in the .bib (per Hard rule 3): any claim resting only on an unverifiable secondary
summary. Effect-size numbers quoted above (e.g., d = 1.21/0.69/0.11/−0.08 for Andes rubric
components; d = 0.47 for Liu & Koedinger; Hedges g = 0.871 for CTA-based instruction) are taken
from the `research/explore-*.md` branches' own full-text or abstract reads, not recomputed here;
see those files for the underlying study details.
