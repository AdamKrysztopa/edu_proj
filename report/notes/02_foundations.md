# 02 Scientific foundations (literature base for the final PoC report)

Author: Scientific Foundations Researcher. Date: 2026-09-29.
Bib file: `report/notes/02_foundations.bib` (verified entries only; keys below).

## How to read this note

- Every statement carries one category. **[LIT]** = ESTABLISHED LITERATURE (what a cited source reports).
  **[PoC]** = OBSERVED IN THE PoC (what exists in this repository's code or reports).
  **[INT]** = INTERPRETATION (our reading of how the literature bears on the system).
  **[HYP]** = HYPOTHESIS. **[FUT]** = FUTURE WORK.
- "Lens" means one of the seven N3 gap-map lenses in `docs/plans/n3-poc-lens-spec.md` §2 and
  `gapmap/src/gapmap/lenses.py`: DISC, DIAG, SEL, HEDGE, GUARD, WHY, RESULT.
- "Evidence label" means one of the six labels in `residual/src/residual/vocab.py`:
  `observed_human_evidence`, `literature_supported`, `organisational_artefact_supported`, `inferred`,
  `synthetic_extrapolation`, `unknown`.
- "Tacitness" means the `Tacitness` enum in the same file: explicit, relational, automated,
  perceptual, somatic, collective.
- A lens is a construct taken from the literature. The literature does **not** validate the lens.
  The N3 PoC has no human validation. Its README states "hidden-knowledge prediction not
  demonstrated" and calls its records *candidates* (`research/n3/README.md`). [PoC]
- Where a claim rests on a source whose full text was not read in this pass, the verification log
  says so ("content not re-read"). Existence and metadata of every bib entry were checked.

---

## 1. The omission premise: Cognitive Task Analysis (CTA)

### What it is
CTA is a family of methods that capture the knowledge, decisions and cues behind skilled work,
including the parts that do not show in behaviour [LIT] (`schraagen2000cognitive`,
`crandall2006working`, `clark2008cognitive`). Yates and Feldon count over 100 named CTA methods in
the literature and sort them from a sample of 1,065 studies [LIT] (`yates2011advancing`). Methods
combine interviews, observation, process tracing and document analysis. CTA output is used to
design training, job aids and systems.

### Key findings (with numbers at their original grain)
- **Why experts omit.** Automated knowledge "operates outside of conscious awareness" and is "not
  available for introspection", so "experts' unaided self-reports of their problem-solving
  processes are typically inaccurate or incomplete" [LIT] (`clark2008cognitive`, p. 583, citing
  Chao & Salvendy 1994 and Feldon's 2004 dissertation). Feldon develops the automaticity argument
  for curriculum and for teaching [LIT] (`feldon2007implications`, `feldon2007cognitive`).
  The mechanism is proceduralisation of skill (`anderson1982acquisition`; content not re-read).
- **Surgery, n = 3 experts, one procedure.** Three surgeons were videotaped teaching a
  cricothyrotomy. Against a CTA-built gold task list from three *other* surgeons, they omitted on
  average 71% (10/14) of clinical-knowledge steps, 51% (14/27) of action steps and 73% (3.6/5) of
  decision steps. They described "how to do it" for only 13% (3.6/27) of action steps. CTA
  prompting raised the share of steps described from 44% (20/46) to 66% (31/46) [LIT]
  (`sullivan2014use`, abstract).
- **Programming, n = 6 experts.** No single expert programmer reported more than 41% of diagnostic
  actions, 53% of debugging actions or 29% of interpretations, under any elicitation method.
  Pooling all six raised coverage to 87%, 88% and 62% [LIT] (as reported in `clark2008cognitive`,
  p. 585; the primary abstract, `chao1994percentage`, confirms the design and that coverage roughly
  doubled from one to six experts, with three experts as the best cost-benefit point).
- **Nursing, 17 NICU nurses.** CDM interviews elicited significantly more information than
  non-CDM interviews, and the elicited cues formed a sepsis-assessment guide with information "not
  available in the current literature" [LIT] (`crandall1993critical`, abstract). The often-quoted
  figure, 25 of 70 cues absent from the training literature of the time, is reported in
  `clark2008cognitive` (p. 584), not in the abstract.
- **Instructional value (the premise that matters).** CTA-based instruction versus other ways of
  identifying content: Hedges' g = 0.871, varying substantially by CTA method and context, from a
  "relatively small" number of studies [LIT] (`tofelgrehl2013cognitive`). In surgery, versus
  conventional training: SMD 1.36 (95% CI 0.67–2.05) for procedural knowledge and SMD 2.06
  (1.17–2.96) for technical performance of surgical trainees, from a 12-study review [LIT]
  (`edwards2021cognitive`). In an undergraduate biology lab course (n = 314, double-blind),
  CTA-derived instruction cut withdrawal from 8.1% to 1.4% of initial enrolment versus instruction
  by an award-winning instructor [LIT] (`feldon2010translating`).
- **A reusable elicitation product.** Interviews with 52 scientists and engineers, coded for
  decisions, gave a set of 29 problem-solving decisions shared across fields [LIT]
  (`price2021detailed`).

### Which primary study supports "experts omit about 70%"? (question from the task)
- The sentence in the CTA chapter reads: experts "are not fully aware of about 70% of their own
  decisions and mental analysis of tasks (Clark and Elen, 2006; Feldon and Clark, 2006)"
  (`clark2008cognitive`, p. 589, checked in the author-posted PDF). Both citations are review
  chapters by the same group, not new data. [LIT]
- **No single primary study measures "70%" as a general rate.** The nearest primary numbers are
  Sullivan et al. (73% of decision steps, 71% of clinical-knowledge steps; n = 3, one procedure)
  and Chao & Salvendy (at most 29% of interpretations reported by any one expert, i.e. at least 71%
  omitted; n = 6, one task family). [INT]
- **Clark & Estes (1996) is not an omission study.** It is a field cost comparison in one
  organisation (10,000+ employees; a safety course for about 500 managers): 1,087 training days
  with behavioural task analysis versus 590 with CTA, "only suggestive" by the chapter's own
  wording (`clark1996cognitive`, as tabulated in `clark2008cognitive`, Table 43.1, p. 586). [LIT]
- **Decision for the report.** Do not use "70%" as a parameter. Quote the grain-exact numbers with
  n and domain. This agrees with `REORIENTATION.md` §8.1. [INT]
- The "d = 1.72" often quoted for CTA is a within-group pre–post mean from an unpublished 2004
  dissertation (Lee), reported in `clark2008cognitive` (p. 586). It is not a CTA-versus-control
  effect and is not in the bib. [LIT]

### How it contributes to this system
- **The central premise.** Omission concentrates in decisions, interpretations and cues. This is
  why the gap map looks for those constructs rather than for sparse topics. [INT]
- **Knowledge types.** `decision`, `cue`, `interpretation`, `check` and `expectancy` in
  `KnowledgeType` are CTA categories. [PoC]
- **Pooling.** Pooling experts recovers much more than any one (Chao & Salvendy). This motivates
  the "union of experts plus trace" gold in `REORIENTATION.md` §14.1 and the rule that one
  independent source (RG-SINGLE) is a retrieval gap, not coverage. [INT]
- **Gold for evaluation.** Published CTA task lists (e.g. Sullivan's 46 steps) are candidate
  held-out golds for E-CTA. Because their structure is already known to the project, the
  anti-circularity rules of `REORIENTATION.md` §14.3 apply. [FUT]
- **Education path.** CTA-derived instruction is the evidenced route from recovered expert
  knowledge to teaching (g = 0.871; Feldon et al. 2010). [INT]

### Limits for our use
- Omission rates come from 3–6 experts per study, in one domain each, mostly from one group (USC).
  The gold lists are themselves built by CTA, so the rates are partly circular. [INT]
- Every CTA training result measures immediate or in-course performance; none found measures
  transfer (`research/falsify-decoding-the-disciplines.md`). [INT]
- CTA recovers what experts can be prompted to say. It does not tell us what *text* omits. That
  link is our hypothesis. [HYP]
- A brief physics intervention built on expert decisions (decision-based learning, two lessons,
  N = 390, quasi-experimental) had no direct effect on performance (`jeong2024effects`). Making
  expert decisions explicit is not sufficient on its own. [LIT]

---

## 2. Critical Decision Method (CDM)

### What it is
CDM is a CTA interview built on one real, recalled incident. The interviewer makes several passes
over the incident (timeline, then deepening probes, then "what if" questions) [LIT]
(`hoffman1998use`). It extends Flanagan's critical incident technique with probes for "perceptual
discriminations, conceptual discriminations, typicality judgments, and critical cues" [LIT]
(`klein1989critical`, abstract). ACTA is a streamlined practitioner version with three interview
methods [LIT] (`militello1998applied`).

### Key findings
- CDM was developed with fireground commanders, tank platoon leaders, engineers, paramedics and
  programmers [LIT] (`klein1989critical`).
- CDM elicited significantly more than non-CDM interviews with NICU nurses and yielded cues not in
  the literature [LIT] (`crandall1993critical`).
- CDM products include timelines, situation-assessment records and decision-requirement tables;
  Hoffman et al. discuss data quality, reliability and efficiency [LIT] (`hoffman1998use`).

### How it contributes to this system
- **DISC lens.** The CDM probe for discriminations and typicality becomes DISC's construct: a cue is
  a discrimination between contrasting cases. DISC fires when sources use a judgement term
  ("high risk", "abnormal", "stable") without a boundary [PoC] (spec §2.1).
- **DIAG, SEL, HEDGE, RESULT channels.** Each lens routes its question to CDM probes on a recalled
  case: options considered and the basis of choice (SEL), hypotheticals (HEDGE), what was noticed
  and what would have changed the action (RESULT) [PoC] (spec §2.2–2.8).
- **Question rules for all lenses.** Retrospective, incident-anchored, no yes/no, ask for a
  contrast between cases, one construct per question [PoC] (spec §2, "Question rules").
- **Evidence label.** A lens output is `inferred`. A CDM answer that a second expert or a trace
  corroborates would become `observed_human_evidence` in the future human path. [FUT]

### Limits for our use
- CDM is retrospective, so answers depend on memory and on the chosen incident. [LIT/INT]
- CDM needs a live expert. NOW uses none; the PoC only drafts CDM-style questions and has never
  asked them. [PoC]
- CDM probes were designed for time-pressured naturalistic work. Fit to normative domains (GDPR
  DPIA) is untested. [INT]

---

## 3. PARI (Precursor, Action, Result, Interpretation)

### What it is
PARI is a CTA procedure developed for U.S. Air Force troubleshooting training. For each step it
records why the action was taken (precursor), the action, its result, and what the result means
for the fault hypothesis (interpretation) [LIT] (`hall1995procedural`, abstract).

### Key findings
- The method was built for complex problem-solving tasks as part of an integrated technology for
  instruction [LIT] (`hall1995procedural`). No outcome statistics are cited here.
- Interpretations are where pooled expert coverage was lowest (62% even with six experts) [LIT]
  (`chao1994percentage` as reported in `clark2008cognitive`).

### How it contributes to this system
- **RESULT lens.** Sources prescribe a test but not how to read its result or which branch it
  selects. RESULT fires on a prescribed test (`procedure_step`, `check`, `strategy`, `decision`)
  with no result-to-interpretation mapping [PoC] (spec §2.8).
- **DIAG lens.** PARI's interpretation step, joined with ECD's alternative explanations (§12),
  gives DIAG's construct: rival causes of one effect with no sign that separates them [PoC]
  (spec §2.2).
- **Knowledge types.** `interpretation` and `expectancy` predictions; tacitness `relational`
  (+`perceptual` for inspect/observe) [PoC].

### Limits for our use
- PARI was built for equipment troubleshooting. Its fit to normative or conceptual domains is
  unknown. [INT]
- The report is a 1995 technical guide, not a validation study. [LIT]

---

## 4. Expert–novice differences

### What it is
Research comparing how experts and novices perceive, represent and solve problems.

### Key findings
- **Physics, representation.** In sorting tasks and protocols, experts categorised physics
  problems by the principle that solves them; novices used the problem's literal (surface)
  features [LIT] (`chi1981categorization`, abstract; four experiments).
- **Pattern-indexed knowledge.** Expert physics knowledge is indexed by large numbers of patterns
  that, once recognised, guide the solver [LIT] (`larkin1980expert`, abstract opening).
- **Chunking.** Chess masters perceive positions as meaningful chunks [LIT] (`chase1973perception`;
  content not re-read).
- **Perceptual expertise can be analysed and taught.** Experts sex chicks at over 98% accuracy.
  Naive participants, after a short instruction on one contrast in shape, rose "from slightly above
  chance" to expert-level accuracy; the item-level correlation with experts rose from .21 to .82
  [LIT] (`biederman1987sexing`, abstract).

### How it contributes to this system
- **DISC channel.** The chick-sexing result shows that a perceptual cue is a discrimination that
  contrasting cases can teach. DISC therefore routes to "contrasting-case classification", not to
  interviews alone [PoC] (spec §2.1; `REORIENTATION.md` §10.2 item 1).
- **Knowledge type `expert_novice_contrast`** and the planned bottleneck-hypothesis object
  ("expert has / novice lacks / novice substitutes") come from this line [PoC/FUT].
- **Education path.** Principle-based versus surface-based representation is the classic
  bottleneck for teaching (e.g. Track A's principle-selection K0 rule). [INT]

### Limits for our use
- These studies describe differences. They do not say what text leaves out. [INT]
- Expert–novice contrasts are learner-side facts. The PoC has only expert-voiced text, so it
  cannot observe them. [PoC]

---

## 5. Expert blind spot and the curse of expertise

### What it is
Experts misjudge what novices find hard, because their own knowledge is organised differently.

### Key findings
- **Mathematics teachers, N = 48.** Preservice teachers with more advanced mathematics were more
  likely to treat symbolic equations as a prerequisite for word and story problems, "in contrast
  with students' actual performance patterns"; the same pattern appeared across several subjects
  [LIT] (`nathan2003expert`).
- **Prediction of novice time.** In two studies, one with expertise experimentally manipulated,
  more expert participants predicted novice completion times worse and resisted debiasing;
  intermediates did best [LIT] (`hinds1999curse`).
- **Knowing wrong answers matters.** With 9,556 students of 181 middle-school physical-science
  teachers, teachers who could identify a popular wrong answer had larger class gains on those
  items than teachers who knew only the right answer [LIT] (`sadler2013influence`).

### How it contributes to this system
- **GUARD lens restriction.** GUARD never asserts a learner difficulty. It hypothesises the
  expert's guard against an error that an expert reported, and says so in the hypothesis text
  [PoC] (spec §2.5).
- **Gold choice.** Expert judgement is not the gold for "what is difficult". Learner response data
  are (`REORIENTATION.md` §8.2, §10.3). [INT]
- **Anchoring guard.** One human arm should be blind to the AI model (`REORIENTATION.md` §9). [FUT]

### Limits for our use
- Samples are small and domain-specific. Blind spot is a tendency, not a law. [INT]

---

## 6. Automaticity and the validity of verbal reports

### What it is
Research on when people can and cannot report their own thinking.

### Key findings
- **Think-aloud is non-reactive; explaining is not.** A meta-analysis of 94 studies (about 3,500
  participants) found the think-aloud effect indistinguishable from zero (r = −.03). Procedures
  that ask people to describe or explain were reactive and changed performance [LIT]
  (`fox2011procedures`; the model is `ericsson1980verbal`).
- **Self-report of causes is often wrong.** People often cannot report the causes of their own
  behaviour [LIT] (`nisbett1977telling`; content not re-read).
- **Automaticity.** See §1 (`clark2008cognitive`; `feldon2007implications`;
  `feldon2007cognitive`).

### How it contributes to this system
- **Tacitness `automated`** ("compiled procedure or self-check; not available to introspection")
  [PoC] (`residual/src/residual/vocab.py`).
- **GUARD channel.** Automated self-checks are behaviour-only, so GUARD routes first to observation
  or process tracing and flags a spoken answer as a weak channel [PoC] (spec §2.5).
- **Question wording.** Retrospective probes over a recalled case, not "explain what you do"
  [PoC] (spec §2 question rules, citing Fox et al.).

### Limits for our use
- Think-aloud surfaces only heeded information, so it misses automated steps [LIT]
  (`ericsson1980verbal`; `REORIENTATION.md` §10.3).

---

## 7. Expertise research: deliberate practice and valid intuition

### What it is
Research on how expert performance develops and when expert intuition can be trusted.

### Key findings
- Expert performance reflects extended, effortful practice with feedback [LIT]
  (`ericsson1993role`; content not re-read).
- The quality of an intuitive judgement depends on how predictable the environment is and whether
  the person had a chance to learn its regularities. "Subjective experience is not a reliable
  indicator of judgment accuracy" [LIT] (`kahneman2009conditions`, abstract).

### How it contributes to this system
- **Choice of human validators and golds.** Expert answers are credible where the domain gives
  fast, valid feedback (e.g. PLC fault diagnosis) and weaker where it does not (e.g. contested
  regulatory judgement). This is one reason DISC has an "institutionally indeterminate"
  alternative explanation [PoC] (spec §2.1) and why GRADE-like certainty is planned
  (`REORIENTATION.md` §10.2 item 4) [FUT].

### Limits for our use
- Neither source addresses written text or AI reconstruction. [INT]

---

## 8. Tacit knowledge

### What it is
Knowledge that people use but do not, or cannot, put into words. Polanyi's phrase is "we can know
more than we can tell" (`polanyi1966tacit`; content not re-read). Collins splits tacit knowledge
into relational (unsaid for contingent reasons, explicable in principle), somatic (tied to the
body) and collective (held in social practice) (`collins2010tacit`; content not re-read).

### Key findings
- **Transfer inside firms is sticky.** In 271 observations of 122 best-practice transfers in eight
  companies, the main barriers were knowledge-related (the recipient's absorptive capacity, causal
  ambiguity, an arduous relationship), not motivation [LIT] (`szulanski1996exploring`).
- **The SECI model is contested.** Nonaka's four modes of converting tacit to explicit knowledge
  (`nonaka1994dynamic`) are judged "flawed": three modes look plausible but none has evidence that
  a simpler account cannot explain, and the model omits inherently tacit knowledge [LIT]
  (`gourlay2006conceptualizing`, abstract).

### How it contributes to this system
- **Tacitness vocabulary.** `relational`, `somatic`, `collective` come from Collins; `automated`
  and `perceptual` come from §§1, 4 and 6 [PoC] (`residual/src/residual/vocab.py`).
- **Target of NOW.** Relational tacit knowledge is the part a gap map can hope to predict and a
  question can recover. Somatic and collective knowledge need observation or community presence
  (`REORIENTATION.md` §10.3). [INT]
- **WHY lens.** Szulanski's causal ambiguity is the construct behind WHY: a prohibition or
  contrast that sources prescribe without a reason [PoC] (spec §2.6).
- **Organisational path.** Stickiness is the reason the organisational wedge (knowledge-at-risk)
  targets missing rationale first (`REORIENTATION.md` §9, §21). [HYP]

### Limits for our use
- Collins's categories are conceptual, not measured; the PoC assigns tacitness by rule, as a
  prediction labelled `inferred` [PoC] (spec §2). [INT]
- SECI's "externalisation" should not be cited as evidence that tacit knowledge can be converted
  on demand. [INT]

---

## 9. Knowledge elicitation (knowledge engineering)

### What it is
The knowledge-engineering tradition that built expert systems studied which techniques elicit
which knowledge. Cooke reviews the varieties of elicitation techniques (`cooke1994varieties`;
content not re-read; the repo notes summarise three families: observation and interviews, process
tracing, and conceptual techniques such as sorting and repertory grids). Hoffman, Shadbolt, Burton
and Klein give a methodological analysis of eliciting knowledge from experts
(`hoffman1995eliciting`; content not re-read).

### Key findings
- Different techniques suit different knowledge types, and number of experts and task type change
  what is recovered [LIT] (`chao1994percentage`, abstract: task, method and number of experts all
  mattered).

### How it contributes to this system
- **"Knowledge type decides the channel."** The type → channel table in `REORIENTATION.md` §10.3
  and each lens's "Channel" field apply this idea [PoC] (spec §2). The full mapping is our
  synthesis, not a validated table [INT].

### Limits for our use
- These comparisons predate LLMs and measure elicitation from people, not from text. [INT]

---

## 10. Reporting bias in text

### What it is
People do not write down what is obvious to them, so text frequency does not track real-world
frequency.

### Key findings
- Gordon and Van Durme show that the frequency with which people write about actions, outcomes or
  properties is a distorted reflection of the world, and discuss the challenge for knowledge
  extraction [LIT] (`gordon2013reporting`, abstract).
- Language models inherit reporting bias: for object colour, text-only models' colour
  distributions diverge from human perception; the authors test multimodal training as a fix [LIT]
  (`paik2021world`, abstract; 521 objects in their CoDa dataset).

### How it contributes to this system
- **The bridge from CTA to text.** CTA shows experts omit the obvious when they talk; reporting
  bias shows writers omit it when they write. Together they predict that the residual lies in
  cues, expectancies and automated checks [INT] (`REORIENTATION.md` §1).
- **Gap-map prior.** "Boundary-text density" is a candidate feature in `REORIENTATION.md` §14.2.
  [HYP]
- **"Fire narrow, close wide."** Lenses fire on a claim's paraphrase but any verbatim source text
  can close a gap, so an obvious fact that happens to be written closes it [PoC] (spec §1.2).

### Limits for our use
- Reporting bias is shown for commonsense facts. Its size in expert technical text is unmeasured.
  [INT]

---

## 11. Pedagogical content knowledge (PCK)

### What it is
Shulman named the knowledge teachers need beyond subject knowledge: how to represent a topic so
that others understand it, and what makes it easy or hard, including students' preconceptions
(`shulman1986those`, `shulman1987knowledge`; content not re-read).

### Key findings
- See `sadler2013influence` in §5: knowing students' most common wrong answer predicted larger
  gains, over and above subject knowledge, on items with a popular wrong answer [LIT].

### How it contributes to this system
- **Education path.** PCK names the layer the gap map does not reach: knowledge about learners. It
  supports keeping `misconception` and learner difficulty as a separate L3 layer fed by learner
  data (`REORIENTATION.md` §10). [INT]
- **GUARD restriction.** Subject experts only partly know what students get wrong (§5), so GUARD
  stays on the expert side [PoC].

### Limits for our use
- PCK is about teachers and classrooms, not organisations. [INT]

---

## 12. Evidence-Centred Design (ECD)

### What it is
ECD treats assessment as an argument: from what students say, do or make in a few situations to
claims about what they know, through a "web of inference" [LIT] (`mislevy2003structure`,
abstract). Its student, evidence and task models separate the claim from the evidence and from the
task that produces it (content not re-read).

### How it contributes to this system
- **DIAG lens.** ECD's "additional knowledge, skills and abilities" name rival explanations of one
  observation. DIAG applies the idea to rival causes of one fault [PoC] (spec §2.2).
- **Bottleneck-hypothesis object.** A learner failure with named alternative explanations
  (missing prerequisite, misconception, execution) is ECD reasoning (`REORIENTATION.md` §10.2 item
  2) [FUT].
- **Education path.** The model → diagnostic item step for future work (`REORIENTATION.md` §9). [FUT]

### Limits for our use
- ECD designs assessments. It says nothing about which knowledge text omits. [INT]

---

## 13. Knowledge-Learning-Instruction (KLI) framework

### What it is
KLI gives three coordinated taxonomies (kinds of knowledge, learning processes and instructional
events) and uses the knowledge component (KC) as the unit of analysis [LIT]
(`koedinger2012knowledge`, abstract). A KC includes the condition under which it applies
(content not re-read; repo notes).

### How it contributes to this system
- **SEL and HEDGE lenses.** The KC condition part ("when, and when not, to apply") is the construct
  behind SEL (a named selection criterion without a situation-to-option mapping) and HEDGE (a
  hedged rule without its exception) [PoC] (spec §2.3, §2.4).
- **Layer L2** of the representation stores KCs with their conditions (`REORIENTATION.md` §10). [PoC/INT]

### Limits for our use
- KC models are validated on learner performance data, which NOW does not have. [INT]

---

## 14. Threshold concepts

### What it is
A threshold concept opens "a new way" of seeing a subject, as distinct from an ordinary core
concept, and often involves "troublesome knowledge" that is conceptually difficult, counter-
intuitive or alien [LIT] (`meyer2003threshold`, abstract). The framework is developed in
`meyer2005threshold` and `meyer2006overcoming`.

### How it contributes to this system
- **Education path.** A way to prioritise which bottleneck a gap-map question should serve first.
  [HYP]
- **Not a lens.** No lens is derived from threshold concepts. [PoC]

### Limits for our use
- Identifying threshold concepts relies on expert and teacher judgement, which the blind-spot
  evidence (§5) makes unreliable for learner difficulty (`research/explore-threshold-concepts.md`).
  [INT]

---

## 15. Conceptual change and misconceptions

### What it is
How learners replace or restructure prior ideas. The classical model (Posner et al.) asks for
dissatisfaction with the old idea and a new idea that is intelligible, plausible and fruitful
(`posner1982accommodation`; content not re-read). diSessa's "knowledge in pieces" treats intuitive
physics as many small context-bound elements (p-prims), not a coherent wrong theory
(`disessa1993toward`; content not re-read). Smith, diSessa and Roschelle argue that
misconceptions are knowledge in transition, not simply errors to replace
(`smith1994misconceptions`; content not re-read).

### Key findings
- The Force Concept Inventory is a multiple-choice test whose distractors encode common-sense
  beliefs about force and motion [LIT] (`hestenes1992force`; content not re-read).
- Bug libraries model procedural errors as systematic "bugs" in otherwise correct procedures [LIT]
  (`brown1978diagnostic`; title-level).

### How it contributes to this system
- **Misconceptions as hypotheses.** The representation stores a misconception as a hypothesis with
  evidence and confidence, which stays neutral between the misconceptions view and knowledge in
  pieces (`REORIENTATION.md` §10). The `misconception` knowledge type is defined as "a hypothesised
  erroneous belief or malrule, held with its evidence" [PoC] (`residual/src/residual/vocab.py`).
- **Public gold for difficulty.** Concept inventories with published response data are candidate
  golds for learner difficulty in physics. [FUT]
- **GUARD.** GUARD fires on claims typed `misconception` but frames them as expert-reported errors
  [PoC].

### Limits for our use
- The theoretical dispute is live, so no single misconception catalogue is ground truth. [INT]

---

## 16. Knowledge Space Theory (KST)

### What it is
KST models a domain as the set of feasible knowledge states and the order in which items can be
learned [LIT] (`doignon1985spaces`; content not re-read).

### How it contributes to this system
- Planned for layer L3 ("what should they learn next") and left until learner data exist
  (`REORIENTATION.md` §10, "Decisions"). Not used in NOW. [FUT]

---

## 17. Decoding the Disciplines (DtD)

### What it is
A teaching model for university instructors: find a bottleneck where many students get stuck,
uncover through a "decoding interview" what experts do at that point, then model it, give practice
and feedback, motivate, assess and share (`middendorf2004decoding`; step wording from the model as
summarised in `research/falsify-decoding-the-disciplines.md`, paper not re-read). The paradigm has
changed since 2004 ("Decoding 2.0") [LIT] (`pace2021beyond`; `pace2017decoding`).

### Key findings
- The strongest comparison found: introductory psychology, 46 DtD vs 45 control students; DtD
  students wrote better hypotheses and operational definitions and identified more variables
  [LIT] (`pinnow2016decoding`, abstract). The abstract does not report how students were allocated.
- No randomised trial of DtD, no physics study with a controlled outcome, and no retention or
  transfer outcome was found (`research/falsify-decoding-the-disciplines.md`). [INT]

### How it contributes to this system
- **Bottleneck framing only.** The spec uses DtD's bottleneck framing and states that "the decoding
  interview is not evidential" [PoC] (spec §2).

### Limits for our use
- See "Investigated but not central" below.

---

## 18. Investigated but not central

- **DtD's decoding interview as an elicitation method.** Falsified as a validity anchor: it has
  never been compared with another elicitation method, and the CTA evidence is stronger
  (`research/falsify-decoding-the-disciplines.md`, verdict "narrow"). **What survived:** step 1
  (pick a bottleneck from student data), steps 3–4 (model, practise, feedback) and step 6
  (assess) as the teaching frame, and the bottleneck idea as a framing for questions. [INT]
- **Knowledge tracing.** Bayesian knowledge tracing models mastery of procedural knowledge from
  learner responses (`corbett1995knowledge`; content not re-read). It needs learner response
  streams. NOW has none, so it belongs to the later L3 layer. [INT]
- **Intelligent tutoring systems.** A meta-analysis of 50 controlled evaluations found a median
  effect of 0.66 SD, larger on locally developed than standardised tests [LIT]
  (`kulik2016effectiveness`, abstract). ITS are a delivery channel, not a way to find what text
  omits. [INT]
- **Synthetic learners and synthetic respondents.** ChatGPT personas matched average survey scores
  but showed less variation than real respondents, and regression coefficients often differed from
  those in the real survey [LIT] (`bisbee2024synthetic`, abstract). This supports the project rule
  that synthetic output may be a predictor, never a criterion, and never feeds a gate (`CLAUDE.md`).
  The learner-specific studies cited in `REORIENTATION.md` §12 were not re-verified here. [INT]
- **Nonaka's SECI model.** Widely cited but judged conceptually flawed (§8). Not used. [INT]
- **Decision-based learning.** A brief two-lesson dose had no direct effect (§1). Not a basis for
  the education path. [LIT/INT]

---

## 19. Summary table: methodology → construct → system component → evidence status

| Methodology (key sources) | Construct used | Lens / system component | Evidence status of the construct |
|---|---|---|---|
| CTA (`clark2008cognitive`, `sullivan2014use`, `chao1994percentage`) | Experts omit decisions, cues, interpretations | Premise of the gap map; `KnowledgeType` decision/cue/interpretation/check/expectancy | Omission ESTABLISHED in direction; rates small-n (n = 3–6), one domain each |
| CTA-based instruction (`tofelgrehl2013cognitive`, `edwards2021cognitive`, `feldon2010translating`) | Recovered expert knowledge improves teaching | Education path | Positive in direction; few small studies; no transfer outcomes |
| CDM (`klein1989critical`, `hoffman1998use`, `crandall1993critical`) | Cues as discriminations; typicality; incident-based probes | DISC; question rules for all lenses; CDM channel for DIAG, SEL, HEDGE, RESULT | Method ESTABLISHED; no validation of our lens use |
| PARI (`hall1995procedural`) | Result → interpretation step | RESULT; DIAG | Method documented (1995 guide); lens unvalidated |
| ECD (`mislevy2003structure`) | Alternative explanations of one observation | DIAG; bottleneck-hypothesis object (future) | Framework ESTABLISHED; our mapping INT |
| KLI (`koedinger2012knowledge`) | KC with a condition part | SEL; HEDGE; layer L2 | Framework ESTABLISHED; our mapping INT |
| Tacit knowledge (`collins2010tacit`, `polanyi1966tacit`) | Relational / somatic / collective | `Tacitness` enum; channel routing | Conceptual framework, not empirical |
| Knowledge stickiness (`szulanski1996exploring`) | Causal ambiguity | WHY; organisational path | One large study (271 observations) |
| Automaticity, verbal reports (`fox2011procedures`, `feldon2007implications`) | Automated steps not reportable; think-aloud non-reactive, explaining reactive | `automated` tacitness; GUARD channel; question wording | Reactivity ESTABLISHED (94 studies); automaticity ESTABLISHED in direction |
| Perceptual learning (`biederman1987sexing`) | Cue taught by contrasting cases | DISC channel (contrasting-case classification); `perceptual` tacitness | One classic study |
| Expert blind spot (`nathan2003expert`, `hinds1999curse`, `sadler2013influence`) | Experts misjudge learner difficulty | GUARD restriction; learner data as gold | Replicated pattern, small samples |
| Expert–novice (`chi1981categorization`, `larkin1980expert`, `chase1973perception`) | Principle vs surface representation | `expert_novice_contrast` type; education path | ESTABLISHED |
| Knowledge elicitation (`cooke1994varieties`, `hoffman1995eliciting`) | Technique fits knowledge type | Type → channel table | Taxonomy ESTABLISHED; full mapping our synthesis |
| Reporting bias (`gordon2013reporting`, `paik2021world`) | Text omits the obvious | Gap-map prior feature (planned); "fire narrow, close wide" | Commonsense facts only; size in expert text unmeasured |
| Conceptual change (`posner1982accommodation`, `disessa1993toward`, `smith1994misconceptions`, `hestenes1992force`) | Misconception as context-bound hypothesis | `misconception` type stored as hypothesis; physics gold (future) | Live theoretical dispute |
| PCK (`shulman1986those`, `shulman1987knowledge`) | Knowledge of learners' difficulties | Education path; L3 layer | Construct ESTABLISHED |
| Threshold concepts (`meyer2003threshold`, `meyer2005threshold`) | Transformative, troublesome concepts | Education-path prioritisation (hypothesis) | Identification relies on expert judgement |
| KST (`doignon1985spaces`) | Feasible knowledge states | Layer L3, later | ESTABLISHED formalism; unused in NOW |
| DtD (`middendorf2004decoding`, `pinnow2016decoding`) | Bottleneck | Question framing only | Low–moderate; decoding interview not evidential |

The evidence label of every lens output is `inferred`. Only `literature_supported` claims attest an
explicit part or close a gap; `synthetic_extrapolation` never closes; `unknown` feeds only a
retrieval gap [PoC] (spec §1.1). A future answer from a person would enter as
`observed_human_evidence` only after corroboration [FUT].

---

## 20. Verification log (one line per bib key)

Method: OpenAlex (`resolve_references` by DOI, abstract via the OpenAlex API) and Crossref
(`api.crossref.org/works/<doi>`) for title, authors, year, venue, volume, pages. "Abstract read"
means numbers or claims above were checked against the abstract. "Content not re-read" means only
existence and metadata were checked; the content claim comes from standard summaries or repo notes.

- `anderson1982acquisition` — OpenAlex W2044754442 exact; Crossref Psych Rev 89(4):369–406. Content not re-read.
- `biederman1987sexing` — OpenAlex W2013352133 exact; Crossref JEP:LMC 13(4):640–645. Abstract read (98%, .21 → .82).
- `bisbee2024synthetic` — OpenAlex W4397011890 exact; Crossref Political Analysis 32(4):401–416. Abstract read.
- `brown1978diagnostic` — Crossref Cognitive Science 2(2):155–192. Title-level only.
- `chao1994percentage` — OpenAlex W2046788628 exact; Crossref IJHCI 6(3):221–233. Abstract read; 41/53/29% and 87/88/62% checked in `clark2008cognitive` p. 585 (secondary).
- `chase1973perception` — OpenAlex W2091785129 exact; Crossref Cogn Psych 4(1):55–81. Content not re-read.
- `chi1981categorization` — OpenAlex W2045300586 exact; Crossref Cognitive Science 5(2):121–152. Abstract read.
- `clark1996cognitive` — OpenAlex W2029473919 exact; Crossref IJER 25(5):403–417. No abstract; figures checked in `clark2008cognitive` Table 43.1.
- `clark2008cognitive` — Host book "Handbook of Research on Educational Communications and Technology" (Jonassen, Spector, Driscoll, Merrill, van Merriënboer, eds., Routledge 2008) verified by Crossref, DOI 10.4324/9780203880869; chapter authors, chapter 43, pp. 577–593 and quoted passages checked in the author-posted PDF (hpttreasures.wordpress.com, cta_chapter_2007-1.pdf). No chapter-level DOI found (a guessed ".ch43" suffix returns 404).
- `collins2010tacit` — OpenAlex W4300413483 exact; Crossref U Chicago Press monograph. Content not re-read.
- `cooke1994varieties` — OpenAlex W2050440709 exact; Crossref IJHCS 41(6):801–849. Content not re-read.
- `corbett1995knowledge` — OpenAlex W2015040676 exact; Crossref UMUAI 4(4):253–278, issued 1995 (often cited as 1994). Content not re-read.
- `crandall1993critical` — OpenAlex W2014940456 exact; Crossref Adv Nurs Sci 16(1):42–51. Abstract read; 17 nurses and 25/70 cues from `clark2008cognitive` pp. 583–584 (secondary).
- `crandall2006working` — OpenAlex W4230172260 exact; Crossref MIT Press 2006, authors Crandall, Klein, Hoffman. Content not re-read.
- `disessa1993toward` — OpenAlex W4239613992 exact; Crossref Cognition and Instruction 10(2–3):105–225, 1993 (the DOI string contains "1985" but resolves to the 1993 article). Content not re-read.
- `doignon1985spaces` — OpenAlex W2093869191 exact; Crossref IJMMS 23(2):175–196. Content not re-read.
- `edwards2021cognitive` — OpenAlex W4200531057 exact; Crossref BJS Open 5(6):zrab122. Abstract read (12 studies; SMD 1.36, 2.06 with CIs).
- `ericsson1980verbal` — OpenAlex W2041656211 exact; Crossref Psych Rev 87(3):215–251. Model as summarised in `fox2011procedures` abstract.
- `ericsson1993role` — OpenAlex W2137247190 exact; Crossref Psych Rev 100(3):363–406. Content not re-read.
- `feldon2007cognitive` — Crossref Educational Psychologist 42(3):123–137 (2007). OpenAlex mis-links this DOI to a 2004 USU record (W159125067) with a wrong co-author; Crossref metadata used. Abstract read (via that record's abstract, which matches the 2007 article's topic).
- `feldon2007implications` — OpenAlex W2115975686 (year 2006 = online date); Crossref Educ Psych Rev 19(2):91–110, print 2007. Content not re-read.
- `feldon2010translating` — OpenAlex W2129373075 exact; Crossref JRST 47(10):1165–1185. Abstract read (n = 314; 8.1% vs 1.4%).
- `fox2011procedures` — OpenAlex W2077979711 (year 2010 = online); Crossref Psych Bull 137(2):316–344, 2011. Abstract read (94 studies, ~3,500, r = −.03).
- `gordon2013reporting` — OpenAlex W2050482109 exact; Crossref AKBC 2013 workshop, pp. 25–30. Abstract read.
- `gourlay2006conceptualizing` — OpenAlex W2093047949; Crossref J Manag Studies 43(7):1415–1436. Abstract read.
- `hall1995procedural` — OpenAlex W15311681 exact; Crossref DTIC report 10.21236/ada303654 (Hall, Gott, Pokorny). Abstract read.
- `hestenes1992force` — OpenAlex W1985858077 exact; Crossref Phys Teach 30(3):141–158. Content not re-read.
- `hinds1999curse` — OpenAlex W2011381597 exact; Crossref JEP:Applied 5(2):205–221. Abstract read.
- `hoffman1995eliciting` — OpenAlex W1973007630 exact; Crossref OBHDP 62(2):129–158. Content not re-read.
- `hoffman1998use` — OpenAlex W2070841423 exact; Crossref Human Factors 40(2):254–276. Abstract read.
- `jeong2024effects` — OpenAlex W4401995203 exact; Crossref Educ Inf Technol 30(4):4413–4433 (online 2024, print 2025). Abstract read (N = 390); "no direct effect" from repo falsify note, not re-read.
- `kahneman2009conditions` — OpenAlex W2140543255; Crossref Am Psychol 64(6):515–526. Abstract read.
- `klein1989critical` — OpenAlex W2080862045 exact; Crossref IEEE SMC 19(3):462–472. Abstract read.
- `koedinger2012knowledge` — OpenAlex W2106779500 exact; Crossref Cognitive Science 36(5):757–798. Abstract read; KC condition part not re-read.
- `kulik2016effectiveness` — OpenAlex W1985824294 (year 2015 = online); Crossref RER 86(1):42–78, 2016. Abstract read (50 evaluations, 0.66 SD).
- `larkin1980expert` — OpenAlex W2048225703 exact; Crossref Science 208(4450):1335–1342. Abstract opening read.
- `meyer2003threshold` — OpenAlex W2108726499 (no DOI); University of Edinburgh research portal: ISL10 Improving Student Learning: Theory and Practice Ten Years On, Oxford Brookes University, pp. 412–424, ISBN 1873576682. Abstract read.
- `meyer2005threshold` — OpenAlex W2127773115 exact; Crossref Higher Education 49(3):373–388. Content not re-read.
- `meyer2006overcoming` — Crossref 10.4324/9780203966273, Routledge 2006. Content not re-read.
- `middendorf2004decoding` — OpenAlex W2163728131 exact; Crossref NDTL 2004(98):1–12. Content not re-read.
- `militello1998applied` — OpenAlex W2158441396 exact; Crossref Ergonomics 41(11):1618–1641. Abstract read.
- `mislevy2003structure` — OpenAlex W2039681496 exact; Crossref Measurement 1(1):3–62. Abstract read.
- `nathan2003expert` — OpenAlex W2108342609 exact; Crossref AERJ 40(4):905–928. Abstract read (N = 48).
- `nisbett1977telling` — OpenAlex W2164558494 exact; Crossref Psych Rev 84(3):231–259. Content not re-read.
- `nonaka1994dynamic` — OpenAlex W2132454116 exact; Crossref Org Sci 5(1):14–37. Content not re-read.
- `pace2017decoding` — Crossref 10.2307/j.ctt2005z1w, Indiana University Press 2017. Not read.
- `pace2021beyond` — OpenAlex W3200686411 exact; Crossref Teaching & Learning Inquiry 9(2). Title-level.
- `paik2021world` — Crossref EMNLP 2021 pp. 823–835; OpenAlex abstract read.
- `pinnow2016decoding` — OpenAlex W2314688064 exact; Crossref Psychology Learning & Teaching 15(1):94–101. Abstract read (46 vs 45).
- `polanyi1966tacit` — No DOI for the 1966 edition. University of Chicago Press page for the 2009 reissue (ISBN 9780226672984) resolves and names the book and author. OpenAlex W1606540910 is a 1997 reprint chapter only. Content not re-read.
- `posner1982accommodation` — OpenAlex W1989748540 exact; Crossref Sci Educ 66(2):211–227. Content not re-read.
- `price2021detailed` — OpenAlex W3111445027 exact; Crossref CBE-LSE 20(3):ar43. Abstract read (52 experts, 29 decisions).
- `sadler2013influence` — OpenAlex W2119740413 exact; Crossref AERJ 50(5):1020–1049. Abstract read (9,556 students, 181 teachers).
- `schraagen2000cognitive` — OpenAlex W1792756357 exact; Crossref Psychology Press 2000, editors Schraagen, Chipman, Shalin. Content not re-read.
- `shulman1986those` — OpenAlex W2140369176 exact; Crossref Educ Researcher 15(2):4–14. Content not re-read.
- `shulman1987knowledge` — OpenAlex W2153000380 exact; Crossref HER 57(1):1–23. Content not re-read.
- `smith1994misconceptions` — OpenAlex W2106713455 exact; Crossref JLS 3(2):115–163. Content not re-read.
- `sullivan2014use` — OpenAlex W1984195792 exact; Crossref Acad Med 89(5):811–816. Abstract read (all omission numbers).
- `szulanski1996exploring` — OpenAlex W2172157658 exact; Crossref SMJ 17(S2):27–43. Abstract read.
- `tofelgrehl2013cognitive` — OpenAlex W2170246441 exact; Crossref JCEDM 7(3):293–304. Abstract read (g = 0.871).
- `yates2011advancing` — OpenAlex W2073150831 (year 2010 = online); Crossref TIES 12(6):472–495, 2011. Abstract read (100+ methods, 1,065 studies).

### Checked but left out of the bib
- Lee (2004), USC dissertation, source of "d = 1.72": not retrieved; reported only in `clark2008cognitive`.
- Clark & Elen (2006); Feldon & Clark (2006): cited for "70%" in `clark2008cognitive`; not retrieved; review chapters, not data.
- Feldon (2004) dissertation: not retrieved.
- Verified but trimmed for length: Hinds, Patterson & Pfeffer 2001 (10.1037/0021-9010.86.6.1232);
  Burton et al. 1990 (10.1016/S1042-8143(05)80010-X); Yates, Sullivan & Clark 2012
  (10.1016/j.amjsurg.2011.07.011); Burkholder et al. 2020 (10.1103/physrevphyseducres.16.010123);
  Mohamed & Bayat 2022 (10.20853/36-1-4517); Collins 1974 (10.1177/030631277400400203); Kellman,
  Massey & Son 2010 (10.1111/j.1756-8765.2009.01053.x); Cen, Koedinger & Junker 2006
  (10.1007/11774303_17);
  Shadbolt & Smart 2015, "Knowledge Elicitation: Methods, Tools and Techniques" (10.1201/b18362-18), in Evaluation of Human Work; Crossref lists no authors, OpenAlex W1512412022 names Shadbolt and Smart;
  Cui, Li & Zhou 2025 (10.1038/s43588-025-00840-7, content not read).
- Metadata traps found: OpenAlex links Feldon (2007), "Cognitive Load and Classroom Teaching: The Double-Edged Sword of Automaticity" (10.1080/00461520701416173), to a wrong 2004 record; the
  diSessa 1993 DOI contains "1985"; several OpenAlex years are online-first dates (Feldon 2006,
  Fox 2010, Kulik 2015, Yates 2010). The `.bib` uses Crossref print years.
