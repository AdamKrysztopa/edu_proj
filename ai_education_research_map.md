# Research Map: AI-Supported Learning That Makes Expert Knowledge Explicit

**Status:** starting map, not a final architecture  
**Primary use:** paste this file into a new research session and use it to decide what to investigate, validate, combine, or reject.  
**Project context:** an AI-supported educational system, initially relevant to university-level physics/STEM but intended to remain transferable across disciplines and potentially compatible with commercial learning-content partners.

---

## 1. Research question

> **How can an AI-supported learning system discover what experts fail to explain because it has become tacit or automatic, diagnose what a learner is actually missing, and turn that gap into effective instruction?**

This map deliberately separates three problems that are often conflated:

1. **Expert elicitation:** what does the expert know/do that they no longer verbalize?
2. **Learner diagnosis:** what exactly is blocking this learner?
3. **Instructional response:** what intervention should follow, and how should an AI system adapt it?

A good system will probably need methods from all three layers rather than one pedagogical framework alone.

---

## 2. Working hypothesis

The most promising starting point is not “build an LLM tutor.” It is:

**Decoding the Disciplines + Cognitive Task Analysis / Knowledge Elicitation + learner-state diagnosis + evidence-based tutoring.**

The proposed research path is therefore:

**hidden expert knowledge → explicit mental operations → learner bottleneck diagnosis → targeted modelling/practice/feedback → learner-state update → adaptation**

This is the main hypothesis to test, not an assumption to preserve.

---

## 3. Decision tree for future research

```text
START
 |
 |-- A. Are we trying to discover what the expert is omitting?
 |      |
 |      |-- Yes -> Decoding the Disciplines
 |      |          + Cognitive Task Analysis / Knowledge Elicitation
 |      |          + Expert–Novice research
 |      |          + Pedagogical Content Knowledge
 |      |
 |      `-- No -> go to B
 |
 |-- B. Is the learner blocked by a concept or mental model?
 |      |
 |      |-- Yes -> Conceptual Change
 |      |          + Concept Inventories / misconception diagnostics
 |      |          + Threshold Concepts (explore cautiously)
 |      |
 |      `-- No -> go to C
 |
 |-- C. Is the learner blocked by a procedure, strategy, or judgment process?
 |      |
 |      |-- Yes -> Cognitive Task Analysis
 |      |          + Cognitive Apprenticeship
 |      |          + Worked Examples / Self-Explanation
 |      |
 |      `-- No -> go to D
 |
 |-- D. Do we need to estimate what this individual learner currently knows?
 |      |
 |      |-- Yes -> Formative / diagnostic assessment
 |      |          + Knowledge Tracing
 |      |          + Mastery Learning
 |      |
 |      `-- No -> go to E
 |
 |-- E. Do we need scalable individualized instruction?
 |      |
 |      |-- Yes -> Intelligent Tutoring Systems
 |      |          + LLM-based tutoring
 |      |          + pedagogically constrained generation
 |      |
 |      `-- No -> traditional instructional design may be sufficient
 |
 `-- F. At every branch:
        validate learning outcomes, transfer, misconceptions,
        robustness across disciplines, and teacher/student acceptance.
```

---

## 4. Priority map

| Priority | Research family | Why it matters to this project | Evidence strength* | STEM fit | Humanities / social sciences fit | AI readiness |
|---|---|---|---|---|---|---|
| **P0** | **Decoding the Disciplines (DtD)** | Directly targets disciplinary bottlenecks and tacit expert mental operations; use as the instructional frame, elicitation via CTA | **Low–moderate**: mostly qualitative; two small non-randomized comparisons, none in physics, no transfer | High | High | **Very high** |
| **P0** | **Cognitive Task Analysis (CTA) / Knowledge Elicitation** | Gives concrete interview/probing methods for extracting expert cognition | **Moderate–high** for training outcomes outside physics; no physics or transfer outcomes | High | Medium–high | **Very high** |
| **P0** | **Expert–Novice research** | Explains why experts and beginners represent the same problem differently | **High as foundational evidence** for representation differences (a continuum, not two groups); instruction built on them helps immediate problem solving in small physics studies; one far-transfer RCT | **Very high** | High | High |
| **P0** | **Pedagogical Content Knowledge (PCK)** | Focuses on what teachers need to know about representations, difficulty and learner misconceptions | **Moderate**: correlational links to school achievement, weak and model-dependent (pooled r = .13 n.s. to .23, 11 studies; strongest in mathematics, mixed in physics); no experiment isolating PCK; no university or transfer outcomes | High | High | High |
| **P1** | **Conceptual Change + misconception research** | Addresses learners whose existing mental model conflicts with the target model | **High** that intuitive ideas persist and coexist with instruction (physics especially); **moderate** for interventions (refutation text g ≈ 0.4, holding at delay; physics curricula show larger gains that persist, in cohort studies; no university transfer outcomes); theory contested (coherent vs fragmented) | **Very high** | Medium | High |
| **P1** | **Concept Inventories / diagnostic instruments** | Makes hidden misconceptions measurable; physics is unusually mature here | **High for cohort/course evaluation** with well-validated instruments; weak for individual diagnosis (item answers unstable on retest, mixed models, some gender-biased items) | **Very high** | Low–medium | **Very high** |
| **P1** | **Cognitive Apprenticeship** | Converts expert cognition into modelling, coaching, scaffolding and fading | **Moderate** as a design framework: components have experimental support (worked examples, self-explanation, computer-based scaffolding g ≈ 0.46); no controlled test of the whole model in physics; fixed-schedule fading no better than none | High | High | **Very high** |
| **P1** | **Worked Examples + Self-Explanation** | Strong candidate for turning decoded expert operations into teachable interactions | **High** for immediate problem solving by novices (meta-analyses g ≈ 0.5); delayed and transfer effects smaller (g ≈ 0.35); little classroom or delayed physics evidence; reverses as prior knowledge grows | **Very high** | Medium | **Very high** |
| **P1** | **Intelligent Tutoring Systems (ITS)** | Mature evidence base for individualized step-level instruction and feedback | **High on tests aligned to the tutor** (median 0.66 SD; 0.73 on local vs 0.13 on standardized tests; step-based ≈ human tutoring); small at scale (≈ 0–0.2 SD); physics: one non-randomized university study, large hour-exam gains on enforced practices, d = 0.25 on an answer-only final | **Very high** | Medium–high | **Very high** |
| **P1** | **Knowledge Tracing / Mastery models** | Provides a computational learner-state layer rather than relying on LLM intuition | **Moderate–high for predicting performance** within a tutor (simple models match deep ones); for learning, a few small positive classroom studies of KC-model redesign on hand-picked units, one null on units chosen by topic, and no test against a simple mastery rule | High | Medium | **Very high** |
| **P2** | **Threshold Concepts** | Useful language for transformative/troublesome disciplinary ideas | **Low / contested**: definitions criticised as not empirically isolable; no reliability data for identification; small immediate-outcome studies test teaching the concept, not the "threshold" label | High | High | Medium–high |
| **P2** | **Formative assessment** | Essential feedback loop for checking whether the intervention actually worked | **High for feedback and quizzing as practices** (feedback d ≈ 0.48, over a third of feedback effects negative; classroom quizzing g ≈ 0.5); **low–moderate for formative assessment as a packaged intervention** (rigorous school estimates d ≈ 0.2–0.3; the quoted 0.4–0.7 has no source); little causal university evidence | High | High | High |
| **P2** | **LLM-based AI tutoring** | Potential delivery/orchestration layer; promising but evidence is newer than classic ITS | **Emerging / moderate**: one university-physics crossover RCT with a large immediate effect (AI bundled with self-pacing and pre-structured steps); elsewhere ≈ 0.1–0.4 SD on unassisted tests, nulls in lab RCTs, harm without guardrails; meta-analyses (g ≈ 0.6) rest on weak primary studies; no transfer evidence | High | High | N/A — implementation layer |

\*Evidence strength here is a **research-prioritization judgment**, not a formal GRADE score. It distinguishes mature replicated literatures from frameworks supported mainly by qualitative studies, case studies, or newer trials.

---

# 5. Method cards

## 5.1 Decoding the Disciplines (DtD) — **start here as framing; elicitation narrowed to CTA**

### What it is
A seven-step pedagogical framework developed around identifying **learning bottlenecks** and making the usually tacit mental operations of disciplinary experts explicit. Indiana University describes it specifically as a way of identifying bottlenecks and “decoding tacit disciplinary knowledge.”

Canonical cycle:

1. define a bottleneck;
2. uncover the expert mental task;
3. model it;
4. give practice and feedback;
5. address motivation/resistance;
6. assess mastery;
7. share what was learned.

### Why it is unusually relevant
It is almost a direct formulation of the project problem: **experts often do not know what they are failing to say because the reasoning has become automatic.**

### Where it has been used
Published work spans humanities and STEM/professional disciplines, including history, biology, astronomy/geoscience, psychology, structural mechanics, business/finance and computer science. A 2022 systematic review of 33 studies reported positive themes for making expert habits of mind explicit. It is a thematic synthesis with no pooled effect estimate, and it notes the literature was still largely qualitative and geographically concentrated.

### Evidence / limitations
**Promising, but do not treat DtD itself as strongly experimentally validated.** The 2022 review found mainly qualitative/case-study evidence, limited saturation of the literature, little direct investigation of students’ own mental blockages, and uncertainty about whether all seven steps are necessary.

Graded evidence (see `research/falsify-decoding-the-disciplines.md`):
- no RCT;
- two small non-randomized comparisons: introductory psychology (Pinnow 2016, N = 91) and business analytics (Lee-Post 2019);
- both measure immediate outcomes only;
- no physics study with a controlled outcome;
- no retention or transfer outcomes anywhere.

The decoding interview has never been compared with another elicitation method.

### Scope after falsification
Keep DtD steps 1 (bottleneck, selected from student data), 3–4 (model, practice and feedback) and 6 (assess) as the instructional frame. For step 2, use CTA (§5.2: CDM probes plus think-aloud on performed tasks) instead of the decoding interview. The decoding interview remains only as one arm of the §9 Phase 2 comparison.

### AI opportunity
Extremely high. AI could act as a **structured interviewer of experts**, repeatedly asking for cues, intermediate judgments, counterfactuals, hidden prerequisites and “what would a novice miss here?” It could then turn the interview into candidate mental operations for human validation.

### Questions to research next
- Can an LLM conduct a valid DtD interview, or does it merely produce plausible-sounding reconstructions?
- How much better is AI-assisted elicitation than a trained human interviewer or expert self-report?
- Can expert operations be validated by observing actual problem solving rather than relying only on retrospective explanation?
- Can multiple experts be compared to distinguish shared disciplinary knowledge from idiosyncratic technique?
- Which DtD steps are necessary for measurable learning gains?

### Minimum reading if this branch is selected
**David Pace, _The Decoding the Disciplines Paradigm: Seven Steps to Increased Student Learning_ (2017).**  
This is the **one mandatory book** in the entire map.

Start with the official Indiana University overview before reading the book.

Sources:  
- Indiana University CITL: https://citl.indiana.edu/teaching-resources/course-design/decoding-disciplines/index.html  
- Mohamed & Bayat (2022), systematic review: https://doi.org/10.20853/36-1-4517

---

## 5.2 Cognitive Task Analysis (CTA) / Knowledge Elicitation — **likely the strongest complement to DtD**

### What it is
A family of methods designed to elicit the **cognitive processes, cues, decisions, knowledge structures and strategies** underlying expert performance. Methods include structured interviews, observation, think-aloud protocols and the **Critical Decision Method (CDM)**.

### Relationship to DtD
DtD gives the educational framing: *find the bottleneck and reveal disciplinary thinking.*  
CTA provides a richer toolbox for the difficult middle step: *how exactly do we extract expert cognition without accepting shallow self-report?*

### Domain fit
Originally especially strong in complex professional domains—aviation, military, medicine, engineering, emergency response and other judgment-heavy work—but conceptually applicable to academic reasoning as well.

### Evidence / limitations
CTA is much more mature as an elicitation family than DtD, although there is no single standardized CTA procedure. The key problem is that expert verbalization is incomplete and can be distorted by retrospective reconstruction; therefore interviews should ideally be combined with task performance and artifacts.

Graded evidence (see `research/explore-cognitive-task-analysis.md`):
- **Meta-analyses of CTA-based training:** g = 0.871 across training domains (Tofel-Grehl & Feldon 2013); surgery SMD 1.36 for knowledge and 2.06 for technical performance (Edwards et al. 2021). All are outside physics and measure immediate or in-course performance, with high heterogeneity.
- **Closest university-STEM study:** Feldon et al. (2010), in which CTA-derived instruction beat an award-winning instructor's in an undergraduate biology course, on withdrawal and lab-report quality.
- **Expert omission:** experts teaching a procedure omitted about 70% of knowledge and decision steps (Sullivan et al. 2014, surgery, 3 experts).
- **Method choice:** there are over 100 CTA methods, and CTA is "more craft than technology" with no validated basis for choosing one (Yates & Feldon 2011).
- **Transfer:** no study found measures it.

### Provisional method for physics
1. The expert solves the problem while thinking aloud, without prompts. Written and diagram work is captured alongside. Non-directed think-aloud does not change performance; being asked to describe or explain does (Fox, Ericsson & Best 2011).
2. After the task, CDM-style multi-pass probes over the recorded trace. CDM was built for recalling real incidents (Klein, Calderwood & MacGregor 1989), and physics solving can be observed directly instead.
3. Compare across experts.

This is a hypothesis, not a validated protocol.

### AI opportunity
Very high, but unevaluated: no study of LLM-conducted CTA was found. AI probes should run after the task, over the recorded trace, never during solving. Probes of the describe/explain kind are reactive when used mid-task. An AI interviewer can dynamically probe:
- cues noticed;
- alternatives rejected;
- expectations;
- anomalies;
- mental simulations;
- prerequisite knowledge;
- confidence;
- counterfactuals (“what would change your decision?”).

This could produce a structured **expert reasoning graph** rather than a transcript.

### Questions to research next
- Which CTA method best maps onto university physics problem solving?
- Can CDM-style probes be adapted from high-stakes professional decisions to conceptual/mathematical reasoning?
- What is the minimum expert sample needed to identify stable shared mental operations?
- Can multimodal traces—writing, diagrams, equations, gaze, screen actions—improve elicitation?

### Minimum reading if this branch is selected
Clark, Feldon, van Merriënboer, Yates & Early (2008), **“Cognitive Task Analysis”**.  
Optional practical reference only if needed later: Crandall, Klein & Hoffman, _Working Minds_ (2006).

---

## 5.3 Expert–Novice Differences — **foundational mechanism**

### What it is
Research comparing how experts and novices perceive, categorize and solve problems. A classic result in physics is that novices tend to group problems by **surface features**, while experts organize them according to **deep physical principles**.

### Why it matters
This may explain *why* expert explanations omit important steps. The missing item is not always a fact—it may be an entire **representation of the problem** that the expert constructs automatically.

### STEM fit
Exceptional. Physics is one of the canonical research domains for expert–novice studies.

### Non-STEM fit
Strong conceptually, with large literatures in medicine, chess, history, writing and professional judgment, although the exact expert structures are discipline-specific.

### Evidence / limitations
Graded evidence (see `research/explore-expert-novice.md`):
- The representation difference replicates in physics (Chi et al. 1981; Hardiman et al. 1989; de Jong & Ferguson-Hessler 1986). Novices who categorize by principle also solve better, but the link is correlational.
- Expertise is a continuum: calculus-based introductory and graduate students overlap widely on categorization (Mason & Singh 2011). Categorization is a proxy, not a measure.
- Principle-first instruction helps novices on immediate outcomes (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015, high school), consistent with a science meta-analysis favouring attention to knowledge structure plus guidelines and feedback (Taconis et al. 2001).
- Transfer: one randomized university-physics study found far-transfer gains from self-explanation and analogical comparison (Nokes-Malach et al. 2013). No study shows delayed transfer.
- In most studies experts solve exercises that are routine for them (Docktor & Mestre 2014).

### AI opportunity
Use paired expert/novice solutions to detect differences in:
- problem representation;
- decomposition;
- cue selection;
- principle selection;
- abstraction level;
- checking/verification;
- error recovery.

### Questions to research next
- Can we automatically infer where a novice representation diverges from an expert representation?
- Is the important unit a “concept,” a procedural skill, a decision rule, or a representation transformation?
- How transferable are expert representations across superficially different problems?
- Does teaching an expert representation help strong novices as much as weak ones (expertise reversal)?

### Minimum reading if this branch is selected
Chi, Feltovich & Glaser (1981), **“Categorization and Representation of Physics Problems by Experts and Novices.”**  
https://doi.org/10.1207/s15516709cog0502_2

---

## 5.4 Pedagogical Content Knowledge (PCK) — **teacher-side model**

### What it is
Shulman’s concept that knowing a subject is not the same as knowing **how that subject becomes learnable**. PCK includes useful representations, analogies, examples and explanations, plus knowledge of what makes specific topics difficult and which preconceptions learners commonly bring.

### Why it matters
DtD asks experts to expose hidden reasoning. PCK asks a complementary question:

> **What does an effective teacher know about how learners misunderstand this particular content?**

A domain expert and an excellent teacher are therefore not interchangeable training sources.

### Evidence / limitations
Graded evidence (see `research/explore-pedagogical-content-knowledge.md`):
- **Correlational links to achievement gains:** Baumert et al. (2010) in school mathematics; in school physics, Keller et al. (2017) positive and Cauet et al. (2015) null. All immediate or within-year, none at university.
- **Knowledge of student difficulties:** teachers who could name students' most common wrong answer had much larger gains on those items than teachers who knew only the right answer (Sadler et al. 2013, middle-school physical science, 181 teachers, same-item gains).
- **No experiment isolates PCK:** too few intervention studies measure it separately (Gonzalez, Lynch & Hill 2022). A systematic review of 217 science-PCK studies found the student-outcome link inconclusive (Park & Chan 2025); a meta-analysis found r = .13 (n.s.) under random effects and r = .23 only under a three-level model, with a prediction interval of −.40 to .72 (Fukaya et al. 2025, 11 studies).
- **Content experts hold it only partly:** university physics TAs and instructors scored 65% and 68% of the maximum when predicting students' most common wrong FCI answers (chance: 40%), and the TAs missed many common difficulties (Maries & Singh 2016).
- **Transfer:** no study found measures it.

### Domain fit
Very broad. Especially developed in teacher education and science/mathematics education, but applicable to essentially any discipline.

### AI opportunity
Create a **PCK layer** separate from the raw domain knowledge base:
- common misconceptions;
- good/bad analogies;
- prerequisite gaps;
- typical misleading cues;
- explanation variants;
- diagnostic questions.

Seed the misconception, misleading-cue and diagnostic-question entries from student response data (cohort-level concept-inventory distractor frequencies, plus coded open-ended answers and exam errors, since distractors miss some student ideas), not from expert or teacher prediction: TAs miss many common difficulties, and experienced instructors scored no better (Maries & Singh 2016). Teachers review these entries and contribute representations, analogies and explanation variants, the part student data cannot supply.

### Questions to research next
- Should the system learn separately from domain experts and experienced teachers?
- How can PCK be represented computationally?
- Can student interaction logs grow the PCK layer over time?
- Do teacher-contributed representations and explanation variants improve learning beyond difficulty knowledge taken from student data?

### Minimum reading if this branch is selected
Shulman (1986), **“Those Who Understand: Knowledge Growth in Teaching.”**  
It is short and remains the canonical starting point.

---

## 5.5 Conceptual Change + Misconceptions — **learner mental-model branch**

### What it is
A learner often does not lack information; they possess an **existing model that explains the world differently**. Learning then requires restructuring rather than adding a missing fact.

### Why it matters for physics
Physics education contains unusually rich evidence on persistent intuitive models—force and motion are the classic example. Telling a learner the correct equation can leave the incorrect underlying model untouched.

### Evidence / limitations
Graded evidence (see `research/explore-conceptual-change.md`):
- **Persistence:** naive intuitions survive science education and coexist with the scientific idea for years (Shtulman & Valcarcel 2012). Solving many traditional problems leaves conceptual difficulties intact (Kim & Pak 2002).
- **Theory contested:** coherent framework theories (Vosniadou & Brewer 1992) against knowledge in pieces (diSessa 1993; diSessa, Gillespie & Esterly 2004). Both imply that whether a learner uses an intuitive idea depends on context.
- **Refutation text:** g = 0.41 across 44 comparisons (33 studies), stable across test delays up to a month and beyond (k = 2 beyond); post-secondary g = 0.33 (age not a significant moderator); dissertations g = 0.11 (Schroeder & Kucera 2022). Not sufficient on its own (Guzzetti 2000).
- **Conflict needs commitment:** passively observed demonstrations did not improve end-of-semester explanations; predicting first did, modestly (Crouch et al. 2004). Cognitive conflict alone gives inconsistent results (Limón 2001).
- **Physics curricula:** elicit–confront–resolve tutorials and interactive engagement give larger conceptual gains whose scores hold for months to years (Pollock 2009; Deslauriers & Wieman 2011, where retention was equally high after traditional lecture), from cohort comparisons, not randomized trials. No university study measures transfer; a high-school bridging-analogies study included near- and far-transfer items with a two-month delay (Clement 1993).

### AI opportunity
The tutor should identify a learner’s current model from explanations and predictions, then generate **discriminating cases** that separate the learner’s model from the target model.

Treat a diagnosed misconception as a context-bound hypothesis, not a stable state: confirm it in a second surface context before acting on it, and re-check it after instruction, since a correct answer can coexist with the intuition (Shtulman & Valcarcel 2012). A discriminating case works better when the learner commits to a prediction before seeing the outcome (Crouch et al. 2004; Miller et al. 2013). No study has validated an LLM's misconception diagnosis for an individual learner; the studies found work at item level (Smart, Bos & Bos 2024; Savage & Rebello 2025).

### Questions to research next
- Can an LLM reliably infer a misconception from free-form reasoning?
- Should diagnosis be generative, inventory-based, or hybrid?
- Does a misconception label for one learner predict their answers in a second context and on retest, or only on the item it came from?
- Can the system deliberately choose examples where competing mental models predict different outcomes?

### Minimum reading if this branch is selected
Posner, Strike, Hewson & Gertzog (1982), **“Accommodation of a Scientific Conception: Toward a Theory of Conceptual Change.”**

---

## 5.6 Concept Inventories — **high-value physics branch**

### What they are
Validated diagnostic instruments designed around core concepts and common incorrect alternatives. The **Force Concept Inventory (FCI)** is the canonical physics example.

### Why they matter
They offer something extremely useful for AI research: **known misconception structures and distractors grounded in education research**, rather than diagnoses invented by an LLM.

### Domain fit
Very strong in physics and several STEM fields; much weaker as a generic tool across disciplines.

### Evidence / limitations
Graded evidence (see `research/explore-concept-inventories.md`):
- **Validated for class-level use.** FCI, FMCE, CSEM, BEMA, TUG-K and EMCS have class-level validity evidence, and published best-practice guidance says they assess instruction, not individual mastery (Madsen, McKagan & Sayre 2017). The FCI total score is reliable (test–retest r = 0.89) and its factor structure replicates at scale (Eaton & Willoughby 2018).
- **Weak for individual diagnosis.** 31% of FCI responses changed on a retest within a week, although total scores correlated at r = 0.89 (Lasry et al. 2011; one college, N = 100). Students hold mixed, context-dependent models (Bao & Redish 2006). Six FCI items are biased against women and two in their favour (Traxler et al. 2018). EMCS α is 0.68–0.76 (Singh & Rosengrant 2003; Wu, Li & Rebello 2025), below the 0.80 usually cited for comparing individuals (Lasry et al. 2011).
- **Distractors miss student ideas.** Open-ended versions reveal categories that are not among the choices (Rebello & Zollman 2004; Savage & Rebello 2025).
- **Diagnosis helps only when it drives a response.** In a cluster RCT, concept questions and a diagnostic test without feedback did not significantly beat traditional teaching, while a formative-assessment package built on the diagnosis did (d ≈ 0.4 at 3 months; Lichtenberger et al. 2024, upper-secondary kinematics). No study measures transfer.

### AI opportunity
Use concept inventories as:
- seed labels for misconception models;
- benchmark datasets for diagnostic dialogues;
- sources of contrastive questions;
- external validation for an AI’s inferred learner state **at class level**, or for one student only when several items probe the same concept (single item answers are unstable on retest).

Do **not** assume an individual concept-inventory score is a complete learner model; these instruments are generally designed for specific assessment purposes and have construct limitations.

### Questions to research next
- Which physics concept inventories are available for mechanics, E&M, quantum, thermodynamics, mathematics methods, etc.?
- How many items per concept are needed before a misconception score is stable for one student on retest?
- Does diagnosis-targeted instruction beat untargeted instruction of equal time, and does it improve transfer?
- Can open-ended AI dialogue outperform multiple-choice diagnostics without losing reliability?

### Minimum reading if this branch is selected
Hestenes, Wells & Swackhamer (1992), **“Force Concept Inventory.”**  
https://doi.org/10.1119/1.2343497

---

## 5.7 Cognitive Apprenticeship — **bridge from elicitation to teaching**

### What it is
An instructional model aimed at making otherwise invisible cognitive and metacognitive processes visible. Common components include **modelling, coaching, scaffolding, articulation, reflection and exploration**, with support gradually faded.

### Why it matters
CTA/DtD can reveal expert cognition; cognitive apprenticeship provides a plausible way to **teach that cognition explicitly** rather than simply displaying the final answer.

### Domain fit
Broad; particularly natural for complex problem solving, professional practice and STEM.

### Evidence / limitations
Graded evidence (see `research/explore-cognitive-apprenticeship.md`):
- **Whole model:** no controlled test in university physics was found; health-sciences use is mostly design and perception work (Lyons et al. 2017).
- **Components:** modelling via worked examples and articulation via self-explanation (§5.8); computer-based scaffolding in STEM, g = 0.46 over 144 studies, largest at the principles level and for adults (Belland et al. 2017).
- **Fading:** in computer-based STEM scaffolding, fixed-schedule fading did worse than no fading in a pilot meta-analysis (Belland et al. 2015), and the full meta-analysis found no difference by whether or how scaffolds changed, including performance-adapted change (Belland et al. 2017). In single studies, per-learner fading beat fixed fading on delayed tests in a Geometry Cognitive Tutor (Salden et al. 2010), and adapted instruction beat a yoked non-adapted sequence in an algebra tutor (Kalyuga & Sweller 2005); both are outside physics.
- **Order:** problem solving before instruction beat instruction first on average (g = 0.36; Sinha & Kapur 2021), when it used contrasting cases or built instruction on students' attempts (Loibl et al. 2017). In university physics, exploring first beat instructing first on conceptual scores in one group's studies (Weaver et al. 2018; Bego et al. 2022, Experiment 1; DeCaro et al. 2023, N = 78), but not when the activity lacked contrasting cases (Bego et al. 2022, Experiment 2). Explicit instruction first won for primary pupils when element interactivity was high (Ashman et al. 2020).
- **Physics scaffold-then-remove:** conceptual questions before synthesis problems during training improved an unscaffolded, cross-topic exam problem 4 days later (Ding et al. 2011; class-level assignment).
- **Transfer:** one university-physics study measured transfer, with mixed results across two experiments (Bego et al. 2022); none has a verified delayed transfer test.

### AI opportunity
An AI tutor can switch roles dynamically:
- demonstrate expert reasoning;
- coach the learner;
- provide partial scaffolds;
- request articulation;
- compare learner reasoning with expert reasoning;
- fade assistance as measured competence increases, per learner, not on a fixed schedule (fixed-schedule fading did worse than no fading in a pilot meta-analysis, Belland et al. 2015; per-learner fading beat fixed fading in single studies outside physics, Salden et al. 2010; the full meta-analysis found no moderation by fading logic, Belland et al. 2017).

Fading needs a per-learner estimate of the targeted skill, so it depends on the explicit learner model (§5.10), not on conversation alone. Whether the tutor models first or lets the learner explore first is a design choice with evidence on both sides; for conceptual goals, exploration with contrasting cases before modelling is the better-supported default beyond early primary school (Sinha & Kapur 2021; Loibl et al. 2017).

### Questions to research next
- How should scaffolding be faded automatically?
- What evidence shows when modelling should stop and productive struggle should begin?
- Which components have the strongest causal evidence?
- In university mechanics, does exploring with contrasting cases before expert modelling beat modelling first on **delayed** transfer, and does the answer change with element interactivity (Ashman et al. 2020)?
- Does adaptive fading beat fixed fading on delayed transfer in physics?

### Minimum reading if this branch is selected
Collins, Brown & Newman (1989), **“Cognitive Apprenticeship: Teaching the Crafts of Reading, Writing, and Mathematics.”**

---

## 5.8 Worked Examples + Self-Explanation — **strong implementation candidate**

### What it is
Worked examples reduce unnecessary search during early skill acquisition. Self-explanation prompts learners to explain **why each step follows**, helping them extract principles rather than memorize solutions.

### Why it matters
Decoded expert operations can become **worked reasoning traces**, while the AI asks the learner to explain transitions rather than passively consume them.

### Domain fit
Especially strong for mathematics, physics, programming and procedural STEM. Some principles transfer beyond STEM, but the literature is strongest for structured problem solving.

### Evidence / limitations
Graded evidence (see `research/explore-worked-examples-self-explanation.md`):
- Worked examples: g = 0.48 in mathematics (Barbieri et al. 2023). Prompted self-explanation: g = 0.55, and g = 0.53 on transfer measures (Bisra et al. 2018); in digital learning environments, g = 0.45 immediate, 0.35 delayed and 0.33 on transfer (Tan et al. 2025).
- Classroom and delayed-retention evidence is "much more limited" in mathematics (Rittle-Johnson et al. 2017).
- University physics: prompted self-explanation of worked examples improved immediate multi-concept problem solving (Badeau et al. 2017) and far transfer (Nokes-Malach et al. 2013), both randomized. The only delayed physics measure found a marginal or small advantage (Hausmann & VanLehn 2010).
- Learner-generated explanations beat provided ones (g = 0.35, k = 6; Bisra et al. 2018). Instructional explanations added to examples give minimal benefit (Wittwer & Renkl 2010). One physics in-vivo study favoured generation over content (Hausmann & VanLehn 2010).
- Boundary conditions: expertise reversal (Kalyuga et al. 2001; Chen, Kalyuga & Sweller 2015). Mathematics studies whose example conditions included self-explanation prompts showed smaller worked-example effects, a between-study moderator (Barbieri et al. 2023). Prompts must target the intended outcome (Rittle-Johnson & Loehr 2017).

### AI opportunity
Very high and comparatively easy to test experimentally:
- expert worked example;
- omitted step / completion problem;
- self-explanation prompt;
- AI diagnosis of explanation;
- progressively faded solution;
- transfer problem.

Decoded operations should reach the learner as prompts to generate or apply them, not only as added text: provided explanations add little to worked examples (Wittwer & Renkl 2010). In physics, self-explanations that state the principle, how it is set up and how its conditions of application are met predicted post-test scores (r = 0.30–0.50; Gjerde et al. 2022). The one controlled study of LLM feedback on self-explanations (calculus; 92 adults online; one session) found no post-test difference between conditions (Chen et al. 2026).

### Questions to research next
- Does LLM-generated self-explanation feedback improve transfer or merely fluency?
- When should the tutor show a worked example vs force retrieval/problem solving?
- Can decoded expert reasoning provide better examples than textbook solution steps?

### Minimum reading if this branch is selected
Chi et al. (1989), **“Self-Explanations: How Students Study and Use Examples in Learning to Solve Problems.”**

---

## 5.9 Intelligent Tutoring Systems (ITS) — **mature system-level foundation**

### What it is
Classic ITS research separates at least three concerns:
- **domain model** — what is being taught;
- **student model** — what the learner knows/does;
- **tutoring/pedagogical model** — what intervention to choose next.

This separation is extremely important for an LLM system: the language model should not silently collapse all three into one prompt.

### Evidence
Graded evidence (see `research/explore-intelligent-tutoring-systems.md`):
- **Aligned tests carry the effect.** Median 0.66 SD over conventional instruction across 50 evaluations, depending "to a great extent" on locally developed vs standardized tests: 0.73 vs 0.13 (Kulik & Fletcher 2016). Step-based ITS are nearly as effective as human tutoring (d = 0.76 vs 0.79; VanLehn 2011). College: g = 0.32–0.37 (Steenbergen-Hu & Cooper 2014).
- **Small at scale and against strong controls.** K–12 mathematics g = 0.01–0.09, 0.02 on standardized tests (Steenbergen-Hu & Cooper 2013; Kulik & Fletcher 2016 report 0.10 on standardized tests). Cognitive Tutor Algebra at scale: no effect in year 1, about 0.2 SD in year 2 in high schools (Pane et al. 2014). No advantage over individual human tutoring (Ma et al. 2014); smaller effects against non-intelligent tutoring systems (Létourneau et al. 2025).
- **University physics.** Andes, replacing paper homework at the US Naval Academy (non-randomized): hour exams d = 0.61, concentrated in drawings (1.21) and variable definitions (0.69), with no gain on the answer subscore; answer-only final exam d = 0.25, confined to majors other than engineering and science (VanLehn et al. 2005).
- **Transfer and delay:** not reported in the syntheses.

### Domain fit
Very strong in mathematics/science and procedural domains; also used in reading, medicine, law and other areas.

### AI opportunity
Treat decades of ITS work as the **architecture and pedagogy prior** for LLM tutoring rather than starting from chatbot design.

The evidence supports three classical principles for an LLM tutor: step-level feedback checked against an explicit solution representation (VanLehn 2011; VanLehn et al. 2005); an explicit pedagogical policy, which changed learning with content held constant (Chi et al. 2011, college physics); and withholding answers, since an unconstrained GPT-4 tutor lowered unassisted exam scores while a hint-only version did not (Bastani et al. 2025, high school; overlap with §5.12).

### Questions to research next
- Does an LLM tutor with step-level checking against an explicit solution model beat the same tutor without it, on a test not aligned to the tutor?
- Does an ITS in university physics improve correct answers and transfer, not only the practices it enforces?
- Which student-model variables should be explicit rather than left in conversation context?
- How should correctness and pedagogical quality be verified independently of the LLM?

### Minimum reading if this branch is selected
Kulik & Fletcher (2016), **“Effectiveness of Intelligent Tutoring Systems: A Meta-Analytic Review.”**  
https://doi.org/10.3102/0034654315581420

---

## 5.10 Knowledge Tracing + Mastery Models — **computational learner-state branch**

### What it is
Knowledge Tracing estimates a learner’s evolving mastery of skills from interaction history. Classical Bayesian Knowledge Tracing models latent mastery using interpretable parameters; newer approaches add richer predictive models.

### Why it matters
Without an explicit student model, an LLM tutor can confuse:
- fluent language with understanding;
- one correct answer with mastery;
- short conversation context with stable knowledge state.

### Domain fit
Best when knowledge can be decomposed into skills/concepts and learner interactions are observable. Harder for open-ended interpretation, research judgment and other poorly discretized expertise.

### Evidence / limitations
Graded evidence (see `research/explore-knowledge-tracing.md`):
- **Prediction:** deep KT beat classic BKT (Piech et al. 2015), but extended BKT, IRT variants and well-featured logistic regression match or beat it on moderate-sized data; deep KT led on the largest (Khajah, Lindsey & Mozer 2016; Wilson et al. 2016; Gervet et al. 2020).
- **Learning:** redesigning a tutor around a data-refined KC model improved learning in several small high-school classroom studies on hand-picked units (d = 0.47 immediate, Liu & Koedinger 2017; Koedinger et al. 2013; Huang et al. 2021), and cutting over-practice saved time (significant in one of six units) without a detected loss (Cen, Koedinger & Junker 2007). Applied to middle-school units chosen by topic, the redesign process gave no difference in learning gains (Lyu et al. 2026). Liu & Koedinger and Cen et al. are high-school geometry; Lyu et al. is middle-school maths. Outcomes are immediate, 2-week or one-month.
- **Sequencing policies:** of 8 experiments sequencing interdependent content with a learner model, none beat all baselines (Doroudi, Aleven & Brunskill 2019).
- **State validity:** best-fitting BKT parameters can be implausible (Doroudi & Brunskill 2017), and population-level parameters under-practise slow learners (Doroudi & Brunskill 2019; simulation; N-correct-in-a-row is susceptible too).
- **Transfer:** no study found tests a KT-driven policy against a simple mastery rule on delayed or transfer outcomes.

### AI opportunity
Combine explicit knowledge tracing with qualitative evidence extracted from dialogue. The LLM becomes an **observation and explanation layer**, not the sole state estimator.

Prefer an interpretable model (logistic/PFA-style or constrained BKT) with a KC model checked against learning curves. Infer mastery from several opportunities, never one answer (§5.6). Whether a mastery rule beats a simple heuristic such as N-correct-in-a-row is an experiment to run, not an assumption.

### Questions to research next
- What is the correct “knowledge component” for physics: concept, equation, representation, procedure, misconception, or expert mental operation?
- Can CTA-elicited operations become knowledge components, i.e. are they observable as steps in student work and do they give smooth learning curves?
- Does a KT-driven mastery policy beat N-correct-in-a-row on delayed transfer?
- How should uncertainty and contradictory evidence be represented?

### Minimum reading if this branch is selected
Corbett & Anderson (1995 / original APT work), **Knowledge Tracing: Modeling the Acquisition of Procedural Knowledge.**

---

## 5.11 Threshold Concepts — **useful, but do not overcommit early**

### What it is
A threshold concept is proposed to act like a conceptual portal: after grasping it, the learner sees the discipline differently. The literature emphasizes properties such as transformative, integrative and troublesome.

### Why it could help
It provides a language for identifying **high-leverage conceptual transitions** rather than treating every course topic as equally important.

### Why it is P2 rather than P0
There are substantial methodological questions about how threshold concepts are reliably identified and whether the defining properties can be operationalized without circular reasoning. It is better treated as a **hypothesis-generation framework** than as the main diagnostic engine.

### Evidence / limitations
Graded evidence (see `research/explore-threshold-concepts.md`):
- **Definitions:** critiques argue threshold concepts are defined so that they cannot be isolated empirically (Rowbottom 2007; Salwén 2021), and that being "threshold" depends on the learner (Rowbottom 2007).
- **Identification:** no settled method. Participants disagree about which concepts are thresholds (Barradell 2013), and results depend on who is asked and how (Quinlan et al. 2013). No inter-rater (e.g. kappa) or cross-institution agreement statistic was found; Delphi studies report percentage agreement and between-round stability, which reflect convergence toward consensus, not reliability.
- **Physics:** the physics papers found (Harrison & Serbanescu 2017; Serbanescu 2017) reframe difficulties already established by physics education research (Newton's first law; measurement uncertainty, the latter already proposed by Wilson et al. 2010) as threshold concepts, and find them "too many to count".
- **Interventions:** a few small, immediate-outcome studies show that teaching a hard concept helps (Aptyka et al. 2025, Grade 10 biology; Ma et al. 2025, N = 30, clinical medicine). None compares a "threshold" concept with a comparable non-threshold one, and none measures transfer.

### AI opportunity
Use AI to propose candidate threshold concepts from expert interviews and learner data, but require empirical validation. Treat an AI-proposed threshold concept as a candidate bottleneck and test it with the same instruments as any other (§5.5, §5.6, Phase 3). "Threshold" status adds value only if crossing it predicts later performance on integrated problems beyond what prerequisite mastery predicts.

### Questions to research next
- Does mastering a candidate threshold concept predict later performance on integrated problems better than mastering an equally difficult non-threshold concept, controlling for prerequisite knowledge?
- Can candidate thresholds be identified from longitudinal learning data?
- Are threshold concepts stable across instructors and curricula?

### Minimum reading if this branch is selected
Meyer & Land (2003/2005), **Threshold Concepts and Troublesome Knowledge.**  
Also read one critique before adopting the construct operationally.

---

## 5.12 LLM-Based Tutoring — **delivery layer, not the theory of learning**

### Current evidence signal
Graded evidence (see `research/explore-llm-tutoring.md`):
- **University physics:** one crossover RCT (194 eligible students, randomized by peer-instruction group; 142 AI vs 174 in-class post-test observations) found higher immediate post-test scores than in-class active learning: a standardized regression coefficient of 0.63, and 0.73–1.3 SD from a quantile regression that corrects for the ceiling. The median time on task was 49 min, against an assumed 60 min in class (Kestin et al. 2025). The AI condition also changed pacing, setting and delivery, used pre-written solutions and a platform that stepped students through each part, and was tested in the same session.
- **Unassisted outcomes elsewhere:** 0.23–0.27 SD in university lab RCTs (Fischer et al. 2025; Contractor & Reyes 2026, preprint, gain held at one week); no overall effect in two preregistered lab RCTs (Lehmann et al. 2024); about 0.06–0.08 SD per school year for a coaching tutor at scale (Oreopoulos & Low 2026); 0.24 SD in English (0.31 SD overall) in an individually randomized after-school trial with differential attrition (De Simone et al. 2025) and d = 0.36 in an 11-school trial analysed without clustering (Henkel et al. 2024), both with added learning time.
- **Harm without guardrails:** an unconstrained GPT-4 raised practice scores but lowered the unassisted exam (Bastani et al. 2025); ChatGPT raised essay scores without knowledge gain or transfer (Fan et al. 2025).
- **Use pattern matters:** asking for explanations helps; asking for solutions lowered understanding in one study (Lehmann et al. 2024) and left gains that did not persist in another (Contractor & Reyes 2026); explanations help most after an own attempt (Kumar et al. 2025).
- **Syntheses are weak:** pooled g ≈ 0.6 (Liu et al. 2025; Wu et al. 2026; Strohmaier et al. 2026, preprint), but in an audit of primary studies from one such meta-analysis (Deng et al. 2025), only a small minority described the treatment precisely, described the control's activities and used a valid learning outcome (Weidlich et al. 2025); one meta-analysis has been retracted (Wang & Fan 2025).
- **Transfer and delay:** one one-week unaided test (preprint) and a few end-of-intervention outcomes; the one transfer measure was null; no university-physics study.

### Design implication
Do not ask “Which LLM should tutor students?” first. Ask:

1. What learner state is represented?
2. What bottleneck was diagnosed?
3. What evidence supports the chosen intervention?
4. What knowledge sources constrain factual content?
5. What does the model do when uncertain?
6. How do we measure transfer rather than immediate correctness?

In the studies that worked, the sequence, the correct solutions, the common mistakes and the rule against giving answers were largely fixed in advance (Bastani et al. 2025; in Kestin et al. 2025 the sequence and solutions, with a softer answer rule), and the LLM generated the dialogue around them. Measure learning with the AI removed; practice or assisted performance can rise while learning falls.

### Questions to research next
- Can LLMs conduct expert elicitation as well as tutoring?
- Can a single model safely separate interviewer, diagnostician and tutor roles?
- What should be deterministic/rule-based vs generative?
- With the pedagogical design held fixed, does an LLM tutor beat a non-generative implementation of the same design (static or rule-based hints) on an unassisted, delayed test?
- How can a tutor get students to use it for explanation rather than solutions, given low engagement at scale (Oreopoulos & Low 2026)?

### Minimum reading if this branch is selected
Kestin et al. (2025), **“AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting.”**  
https://doi.org/10.1038/s41598-025-97652-6

---

## 5.13 Formative Assessment + Feedback — **the loop that checks whether instruction worked**

### What it is
Gathering evidence of what a learner currently understands during instruction and using it to adjust the next step, for the teacher, the tutor or the learner. Feedback is the learner-facing part; low-stakes quizzing and in-class concept questions are common vehicles.

### Why it matters
Diagnosis only helps when it drives a response (§5.6, Lichtenberger et al. 2024). This card is about what that response should look like.

### Evidence / limitations
Graded evidence (see `research/explore-formative-assessment.md`):
- **Packaged formative assessment is smaller than its reputation.** The quoted 0.4–0.7 SD has no quantitative source (Bennett 2011). Rigorous school estimates are d = 0.20 (Kingston & Nash 2011; science 0.09), 0.26 (Klute et al. 2017) and 0.29 (Lee et al. 2020), with contested methods (Briggs et al. 2012).
- **Feedback works when it carries information.** d = 0.48 overall; reinforcement 0.24, corrective 0.46, high-information 0.99 (Wisniewski et al. 2020). On computers, elaborated feedback 0.49 vs right/wrong 0.05 (Van der Kleij et al. 2015). In university physics, elaborated feedback helped most for low-prior-knowledge students (Heckler & Mikula 2016). More than a third of feedback interventions lowered performance (Kluger & DeNisi 1996).
- **Timing is not a lever by itself.** Immediate vs delayed: g = 0.03 across 51 computer-based studies, few with delays of a day or more (Kandemir et al. 2026). Delayed homework feedback improved exam performance on new problems in one small university engineering course, in two experiments (Mullet et al. 2014).
- **Low-stakes quizzing helps in classrooms** (g = 0.50, 222 studies; Yang et al. 2021), but transfer is weak once publication bias is corrected (Pan & Rickard 2018) and may not reach related items (Wooldridge et al. 2014).
- **University physics:** Peer Instruction improves conceptual scores in cohort comparisons (Crouch & Mazur 2001; Lasry et al. 2008); discussion improves answers to new isomorphic questions (Smith et al. 2009, genetics). Causal higher-education evidence is limited (Morris et al. 2021).
- **Transfer:** one small university classroom study with new exam problems (Mullet et al. 2014, engineering); immediate near transfer to isomorphic questions in genetics (Smith et al. 2009); no delayed-transfer study in physics.

### AI opportunity
The tutor's feedback policy has better evidence than most of its other choices:
- elaborated, task- and process-level feedback that explains why, not right/wrong alone and not praise or comments about the person;
- more explanation for learners with low prior knowledge, less for strong ones (Heckler & Mikula 2016; cf. expertise reversal, §5.8);
- an attempt before any feedback, with answers withheld until then (§5.9, Bastani et al. 2025);
- timing chosen by design and tested, not assumed to be "as fast as possible";
- quizzes with varied items, not only repeats of practised ones, and judged on transfer.

### Questions to research next
- Does elaborated feedback from an LLM tutor improve delayed transfer in physics, or only the next answer?
- Does delaying feedback on physics homework improve transfer, as it did in engineering (Mullet et al. 2014)?
- Which feedback content (principle, condition check, worked step) best carries a decoded expert operation to the learner?

### Minimum reading if this branch is selected
Wisniewski, Zierer & Hattie (2020), **"The Power of Feedback Revisited."** https://doi.org/10.3389/fpsyg.2019.03087

---

# 6. Proposed combined research architecture — **hypothesis to test**

```text
                  ┌──────────────────────────┐
                  │   DOMAIN / CURRICULUM    │
                  │ concepts, tasks, sources │
                  └────────────┬─────────────┘
                               │
                   ┌───────────▼───────────┐
                   │  EXPERT ELICITATION  │
                   │ DtD + CTA            │
                   └───────────┬───────────┘
                               │
                   ┌───────────▼────────────┐
                   │ EXPERT REASONING MODEL │
                   │ operations, cues,      │
                   │ representations, traps │
                   └───────────┬────────────┘
                               │
        ┌──────────────────────▼──────────────────────┐
        │              LEARNER DIAGNOSIS             │
        │ PCK layer (student data) + dialogue +      │
        │ assessment + knowledge tracing             │
        └──────────────────────┬──────────────────────┘
                               │
                   ┌───────────▼────────────┐
                   │ PEDAGOGICAL DECISION   │
                   │ model / practice /     │
                   │ scaffold / challenge   │
                   └───────────┬────────────┘
                               │
                   ┌───────────▼────────────┐
                   │  AI TUTOR INTERACTION  │
                   │ constrained generation │
                   └───────────┬────────────┘
                               │
                   ┌───────────▼────────────┐
                   │ ASSESS + UPDATE MODEL  │
                   │ mastery + transfer     │
                   └───────────┬────────────┘
                               │
                               └──────► repeat
```

### Important architectural principle
The **LLM should probably be an interface/reasoning component, not the database of truth, the student model, the pedagogy model and the evaluator simultaneously.** Classical ITS research strongly suggests keeping these concerns conceptually separable even if one foundation model participates in several of them. No study compares separated domain, student and pedagogical models against one integrated model; the principle rests on indirect evidence (step checking needs a domain model; pedagogical policy has effects of its own, Chi et al. 2011; generated hints fail quality checks without verification, Pardos & Bhandari 2024).

---

# 7. Applicability by discipline

## Physics / mathematics / engineering
**Best research environment for an initial prototype.** Reasons:
- strong expert–novice literature;
- structured problem solving;
- existing misconception research and concept inventories;
- objectively checkable intermediate states in many tasks;
- mature worked-example and ITS literature;
- recent LLM-tutoring experiments in physics.

This makes physics unusually suitable for determining whether AI-assisted decoding works before attempting less structured domains.

## Natural sciences beyond physics
Likely high applicability. Conceptual bottlenecks, representations, scale, causal models and procedural reasoning make DtD/CTA natural fits.

## Computer science
Likely high applicability, especially algorithms, debugging and code reasoning. Fine-grained procedural traces are available, but “correct output” must not be confused with expert reasoning.

## Medicine / professional judgment
CTA has exceptional relevance because experts use tacit cues and decisions. Safety and evaluation requirements are much higher.

## Humanities / history / law
DtD and PCK remain highly relevant because expert reading, source evaluation, argumentation and interpretation contain tacit disciplinary moves. Knowledge tracing and fixed skill decomposition may be less natural and require different representations.

## Languages / writing
Strong opportunities for tutoring and feedback, but “expert solution traces” are less deterministic. Rubrics, exemplars and discourse-level representations may matter more than concept inventories.

---

# 8. Minimum reading pack — deliberately small

**Do not read everything above before starting.** The initial pack is intentionally limited to **one book + five papers**.

### One book
1. **David Pace (2017), _The Decoding the Disciplines Paradigm: Seven Steps to Increased Student Learning_.**  
   Purpose: understand the core framework that directly motivates the project.

### Five papers
2. **Shulman (1986), “Those Who Understand: Knowledge Growth in Teaching.”**  
   Purpose: distinguish domain expertise from knowledge of how learners understand/misunderstand content.

3. **Chi, Feltovich & Glaser (1981), “Categorization and Representation of Physics Problems by Experts and Novices.”**  
   Purpose: foundational evidence for the expert–novice representation gap in physics.

4. **Clark et al. (2008), “Cognitive Task Analysis.”**  
   Purpose: methods for eliciting hidden expert cognition.

5. **Kulik & Fletcher (2016), “Effectiveness of Intelligent Tutoring Systems: A Meta-Analytic Review.”**  
   Purpose: avoid reinventing decades of tutoring-system research.

6. **Kestin et al. (2025), “AI tutoring outperforms in-class active learning...”**  
   Purpose: current empirical signal for carefully designed LLM/AI tutoring in university physics.

### Optional seventh item only if misconception diagnosis becomes central
7. **Hestenes, Wells & Swackhamer (1992), “Force Concept Inventory.”**

---

# 9. Research sequence — recommended order

## Phase 1 — validate the premise
**Question:** Is “hidden expert cognition” actually a major source of the learning bottlenecks we care about?

Explore:
- DtD;
- expert–novice differences;
- PCK;
- CTA.

Deliverable: a taxonomy of candidate hidden knowledge:
- omitted prerequisite;
- perceptual cue;
- representation choice;
- decomposition strategy;
- decision criterion;
- conceptual model;
- error-checking routine;
- metacognitive judgment;
- disciplinary norm / epistemic standard.

**Kill criterion:** if bottlenecks are explained mostly by ordinary prerequisite knowledge or practice quantity, do not over-engineer expert elicitation.

---

## Phase 2 — build an expert-elicitation experiment
Take **one narrow physics topic** and compare:

1. ordinary expert explanation;
2. human-led DtD/CTA interview;
3. AI-led DtD/CTA interview;
4. expert solving problems with think-aloud / artifact capture.

Measure:
- number of distinct actionable mental operations recovered;
- agreement across experts;
- expert rating of importance;
- whether novices actually benefit from the recovered operations.

**Key research question:** Does AI uncover useful expert knowledge that ordinary teaching materials omit?

**Minimal first design** (see `research/experiment-ai-assisted-cta-physics.md`; reviewed by `methods-critic`):
- **Topic:** selecting and combining conservation principles in first-year university mechanics.
- **K0:** code existing exam errors first. Stop if fewer than 30% are principle selection or representation (the Phase 1 kill criterion).
- **Stage A:** 12 experts, within-expert. Order: ordinary explanation → non-directed think-aloud → retrospective probes, AI-led on one problem set and human-led on the other (counterbalanced, time-capped). Operations are coded blind to interviewer and validated against the trace, with decoys. "Absent" is judged against expert explanations plus textbook and lecture notes. Operations are also tagged if they already appear in published physics problem-solving frameworks (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015), so that "new" is not confused with "absent from this course". The decoding-interview arm is deferred.
- **Stage B:** a two-arm RCT, about 370 students. The control is worked examples built from the experts' ordinary explanations. The treatment adds validated operations from the AI-assisted pipeline, length- and time-matched and delivered statically. Each added operation is performed in a worked step and carried by self-explanation prompts that ask the student to justify or apply it; the answer is locked before a model answer is shown. Both arms have the same number of prompts, from the same fixed stems and with equal-length model answers; the control's prompts go to steps already present, so the arms differ in the operations, not in the kind of prompting. Operations given only as text would test the delivery format, not the operations (Wittwer & Renkl 2010; Hausmann & VanLehn 2010). The primary outcome is delayed transfer, scored for correctness only. The SESOI of d = 0.30 is a cost judgment above the likely effect (self-explanation against none gives g ≈ 0.35 at delay; Tan et al. 2025), so Stage B is built to rule out d ≥ 0.30. If treatment time exceeds control by more than 10%, the claim becomes "operations plus time". An arm × pretest interaction is prespecified as exploratory (expertise reversal) and cannot overturn K2.

**Kill criteria:**
- **K1 (gate to Stage B):** at least 3 performed, shared operations absent from ordinary material, at least 2 of them added by AI probes, and the AI-minus-human contradicted rate (95% CI upper bound) no more than 15 points. If only the AI-added condition fails, Stage B tests trace-based CTA instead.
- **K2 (after Stage B):** with compliance of at least 70% in each arm, an upper bound of the 90% CI for delayed transfer below d = 0.30 stops the use of elicited operations as instruction for this topic, and is recorded as an effect below the SESOI, not a null. A compliance failure allows one re-run; a second failure is a kill.

---

## Phase 3 — diagnose learner bottlenecks
For the same topic, compare:
- conventional test;
- concept-inventory style items;
- open-ended explanation;
- AI Socratic diagnostic dialogue;
- hybrid diagnosis.

Measure not only classification accuracy but **instructional utility**: does the diagnosis lead to a better next intervention? Also measure, for each method, the same student's test–retest stability (31% of FCI item responses changed on a retest within a week; Lasry et al. 2011) and cross-context consistency: whether the same diagnosed idea shows up when the concept is probed in a second surface context (diSessa, Gillespie & Esterly 2004).

---

## Phase 4 — intervention experiment
Convert decoded operations into several interventions:
- direct explanation;
- expert modelling;
- worked example;
- self-explanation;
- guided practice;
- Socratic questioning;
- refutation (state the likely wrong idea, then refute it);
- predict-then-observe discriminating cases;
- problem solving before instruction (contrasting cases, then instruction built on students' attempts).

Randomize or counterbalance where feasible. Treat order (explore first vs model first) as a factor, not a fixed default; the evidence is split by learner level and element interactivity (Sinha & Kapur 2021; Ashman et al. 2020). Hold feedback constant across arms (elaborated, same timing) and report it; average effects of computer-based feedback range from 0.05 (right/wrong) to 0.49 (elaborated) across studies (Van der Kleij et al. 2015), so arms that differ in feedback would confound the comparison.

Measure:
- immediate performance;
- delayed retention;
- **transfer to structurally similar but superficially different problems**;
- misconception persistence;
- time on task.

Transfer should be a primary outcome because expert-like representation is the real target.

---

## Phase 5 — adaptive system
Only after Phases 1–4 identify useful signals:
- formalize knowledge components / mental operations;
- introduce knowledge tracing or another explicit learner model;
- judge it by a learning experiment against a simple mastery rule (N-correct-in-a-row or a moving average), with delayed transfer as the outcome, not by predictive accuracy;
- if an LLM delivers the tutoring, compare it with the same design delivered without generation (static or rule-based), on an unassisted, delayed test, and report uptake; LLM effects shrink or vanish once the AI is removed at test, pacing is matched or students must choose to use it (Bastani et al. 2025; Lehmann et al. 2024; Oreopoulos & Low 2026).
- define tutoring policies;
- then optimize personalization.

Evaluate any adaptive system on a test not written around the system's own tasks, and over more than one term: ITS effects shrink on standardized tests (Kulik & Fletcher 2016) and appeared only in the second year at scale (Pane et al. 2014).

Do not start with a complex adaptive model before validating what should be represented.

---

# 10. Research questions with highest expected value

### RQ1 — Expert elicitation
**Can an AI interviewer recover tacit expert mental operations that are absent from ordinary lectures, textbooks and expert self-explanations?**

### RQ2 — Validity
**Are the recovered operations reproducible across multiple experts and observable in actual expert task performance?**

### RQ3 — Learner diagnosis
**Can AI distinguish missing knowledge, misconception, representation error, procedural error and metacognitive failure?**

### RQ4 — Instructional causality
**Does teaching the decoded operation improve transfer, or merely performance on the original problem?**

### RQ5 — Personalization
**Does an explicit learner model outperform an LLM that adapts only from conversational context?**

### RQ6 — Cross-disciplinary generalization
**Which parts of the pipeline are domain-general and which require discipline-specific models/instruments?**

### RQ7 — Teacher augmentation
**Does the system improve teachers’ own PCK by exposing recurrent learner bottlenecks?**

### RQ8 — AI role separation
**Should expert interviewer, learner diagnostician, tutor and evaluator be separate agents/models/policies?**

---

# 11. What not to assume

- Do **not** assume every learning difficulty is a hidden expert step.
- Do **not** assume an expert can accurately verbalize their own cognition.
- Do **not** assume the LLM’s reconstruction of expert reasoning is valid because it sounds plausible.
- Do **not** assume every bottleneck is a “threshold concept.”
- Do **not** treat learner correctness as equivalent to understanding.
- Do **not** assume a misconception is gone because a learner now answers correctly; naive intuitions persist alongside the scientific idea.
- Do **not** use concept inventories outside their validated purpose without checking validity; most are validated for class-level evaluation, not for diagnosing or grading individual students.
- Do **not** assume higher predictive accuracy in a student model means better pedagogy.
- Do **not** assume an unconstrained chatbot inherits the evidence base of intelligent tutoring systems.
- Do **not** measure learning while the AI is still available; assisted or practice performance can rise while unassisted performance falls.
- Do **not** evaluate only immediate post-test performance; include retention and transfer.
- Do **not** assume more or faster feedback is better; over a third of feedback interventions lowered performance, and in computer-based studies immediate vs delayed feedback makes no difference on average (few used delays of a day or more).
- Do **not** assume experts or instructors know which difficulties are common; check against student response data.

---

# 12. Evidence notes that should shape the project

1. **DtD is directly aligned with the problem, but its empirical base is less mature than its conceptual fit suggests.** Keep it as the pedagogical framing (bottleneck → model → practice → assess). Its interview step is not evidential without CTA-style validation against performed tasks.
2. **CTA offers a more mature toolkit for extracting expert cognition.** Combining it with DtD is likely more defensible than using DtD interviewing alone. No physics or transfer evidence yet; start with think-aloud on performed tasks plus retrospective CDM probes.
3. **Physics is a strategically strong first domain.** It offers classic expert–novice findings, validated misconception instruments, structured problems and objective checks. Expert–novice differences are well replicated but form a continuum; instruction built on them has immediate, not yet delayed-transfer, evidence.
4. **Classical ITS research should be treated as required prior art.** Meta-analytic evidence for ITS is much stronger than the current evidence for generic LLM tutors. Its large effects are on tests aligned to the tutor; on standardized tests and at scale they are about 0–0.2 SD.
5. **Recent AI-tutoring evidence is encouraging but narrow.** Strong results have come from carefully engineered pedagogical systems, not generic “ask an LLM” interactions. The large result (Kestin et al. 2025) is immediate and bundles the AI with self-pacing and pre-structured steps; at scale and with the AI removed at test, effects are small or null, and syntheses of ChatGPT studies rest on weak designs.
6. **A learner model should be explicit enough to inspect and test.** Conversational memory alone is a weak scientific foundation for claims of personalization.
7. **Knowledge of student difficulties is only partly held by content experts.** University physics TAs miss many common difficulties that concept-inventory data reveal, and instructors score no better. Knowing students' common wrong answers predicts gains beyond subject knowledge, though only correlationally. Seed the PCK layer from student data and let teachers review it.

---

# 13. How to use this file in the next research session

Paste this file and give the research agent one of the following instructions:

### Explore one branch
> Using the attached Research Map as the current project state, deeply investigate **[METHOD]**. Focus on empirical evidence, criticisms, domain applicability, operational methods, and how it could integrate with the proposed AI system. Update the map only where evidence justifies a change. Do not expand unrelated branches.

### Compare methods
> Using the attached Research Map, compare **[METHOD A]** and **[METHOD B]** specifically for eliciting hidden expert reasoning in university physics. Identify overlap, differences, evidence quality, implementation requirements, and a minimal experiment that could discriminate between them.

### Eliminate a branch
> Attempt to falsify the usefulness of **[METHOD]** for this project. Search for critiques, null findings, validity problems, and more suitable alternatives. Recommend **keep / narrow / park / reject**, with evidence.

### Design the first experiment
> Using the Research Map as constraints, design the smallest scientifically defensible experiment testing whether AI-assisted DtD/CTA elicits expert knowledge that improves novice learning in one physics topic. Prioritize measurable transfer and avoid unnecessary system complexity.

---

# 14. Source anchors

These are starting anchors, not a complete bibliography.

- Indiana University — Decoding the Disciplines: https://citl.indiana.edu/teaching-resources/course-design/decoding-disciplines/index.html
- Mohamed & Bayat (2022) — systematic review of DtD: https://doi.org/10.20853/36-1-4517
- Pace (2017) — _The Decoding the Disciplines Paradigm: Seven Steps to Increased Student Learning_
- Pinnow (2016) — DtD two-group comparison, introductory psychology: https://doi.org/10.1177/1475725716637484
- Feldon et al. (2010) — CTA-derived vs expert-authored instruction, undergraduate biology: https://doi.org/10.1002/tea.20382
- Tofel-Grehl & Feldon (2013) — meta-analysis of CTA-based training: https://doi.org/10.1177/1555343412474821
- Shulman (1986) — PCK: https://doi.org/10.3102/0013189X015002004
- Baumert et al. (2010) — teachers' PCK and student progress in mathematics (COACTIV): https://doi.org/10.3102/0002831209345157
- Sadler, Sonnert & Coyle (2013) — teacher knowledge of student misconceptions and learning gains: https://doi.org/10.3102/0002831213477680
- Keller et al. (2017) — physics teachers' PCK and student outcomes: https://doi.org/10.1002/tea.21378
- Cauet et al. (2015) — physics teachers' CK and PCK, null for learning gains: https://doi.org/10.24452/sjer.37.3.4963
- She et al. (2025) — science teachers' PCK and student achievement: https://doi.org/10.3102/00028312241278627
- Maries & Singh (2016) — TAs' and instructors' knowledge of common FCI difficulties: https://doi.org/10.1103/physrevphyseducres.12.010131
- Nathan & Petrosino (2003) — expert blind spot: https://doi.org/10.3102/00028312040004905
- Park & Chan (2025) — systematic review of science-teacher PCK: https://doi.org/10.3102/00346543251394404
- Fukaya et al. (2025) — meta-analysis of PCK correlates: https://doi.org/10.1016/j.tate.2024.104881
- Carlson et al. (2019) — Refined Consensus Model of PCK: https://doi.org/10.1007/978-981-13-5898-2_2
- Gonzalez, Lynch & Hill (2022) — meta-analysis of STEM teacher-PD experiments: https://doi.org/10.26300/d9kc-4264
- Chi, Feltovich & Glaser (1981) — expert/novice physics: https://doi.org/10.1207/s15516709cog0502_2
- Hardiman, Dufresne & Mestre (1989) — expert/novice similarity judgments in physics: https://doi.org/10.3758/bf03197085
- de Jong & Ferguson-Hessler (1986) — knowledge organization of good and poor physics solvers: https://doi.org/10.1037/0022-0663.78.4.279
- Mason & Singh (2011) — categorization across introductory and graduate students: https://doi.org/10.1103/physrevstper.7.020110
- Heller & Reif (1984) — prescriptive model for describing physics problems: https://doi.org/10.1207/s1532690xci0102_2
- Mestre et al. (1993) — hierarchical-analysis training for beginning physics students: https://doi.org/10.1002/tea.3660300306
- Leonard, Dufresne & Mestre (1996) — written qualitative problem-solving strategies: https://doi.org/10.1119/1.18409
- Docktor, Mestre & Ross (2012) — principle-linked feedback on categorization: https://doi.org/10.1103/physrevstper.8.020102
- Taconis, Ferguson-Hessler & Broekkamp (2001) — meta-analysis of science problem-solving instruction: https://doi.org/10.1002/tea.1013
- Nokes-Malach et al. (2013) — self-explanation and analogical comparison, far transfer in physics: https://doi.org/10.1007/s10212-012-0164-z
- Docktor & Mestre (2014) — synthesis of physics education research: https://doi.org/10.1103/PhysRevSTPER.10.020119
- Singh, Maries, Heller & Heller (2023) — physics problem-solving research, handbook chapter: https://doi.org/10.1063/9780735425477_017
- Kalyuga (2007) — expertise reversal effect: https://doi.org/10.1007/s10648-007-9054-3
- Crandall, Klein & Hoffman (2006) — _Working Minds: A Practitioner’s Guide to Cognitive Task Analysis_: https://doi.org/10.7551/mitpress/7304.001.0001
- Hoffman, Crandall & Shadbolt (1998) — Critical Decision Method: https://doi.org/10.1518/001872098779480442
- Klein, Calderwood & MacGregor (1989) — Critical Decision Method, original: https://doi.org/10.1109/21.31053
- Fox, Ericsson & Best (2011) — reactivity of verbal reports, meta-analysis: https://doi.org/10.1037/a0021663
- Sullivan et al. (2014) — expert omissions revealed by CTA: https://doi.org/10.1097/acm.0000000000000224
- Yates & Feldon (2011) — CTA method taxonomy: https://doi.org/10.1080/1463922x.2010.505269
- Hennink & Kaiser (2022) — sample sizes for saturation, systematic review: https://doi.org/10.1016/j.socscimed.2021.114523
- Guest, Namey & Chen (2020) — assessing thematic saturation: https://doi.org/10.1371/journal.pone.0232076
- Lortie-Forgues & Inglis (2019) — effect sizes of large educational RCTs: https://doi.org/10.3102/0013189X19832850
- Kraft (2020) — interpreting effect sizes of education interventions: https://doi.org/10.3102/0013189X20912798
- Dufresne et al. (1992) — expert-like problem analyses for physics novices: https://doi.org/10.1207/s15327809jls0203_3
- Docktor et al. (2015) — Conceptual Problem Solving in high-school physics: https://doi.org/10.1103/PhysRevSTPER.11.020106
- Docktor et al. (2016) — physics problem-solving rubric: https://doi.org/10.1103/physrevphyseducres.12.010130
- Singh & Rosengrant (2003) — energy and momentum concepts test (EMCS): https://doi.org/10.1119/1.1571832
- Chopra & Haaland (2026) — AI-led qualitative interviews: https://doi.org/10.65864/ch6grwpore
- Geiecke & Jaravel — robust AI-led interviews (2024 preprint; forthcoming, _Review of Economic Studies_): https://doi.org/10.2139/ssrn.4974382
- Wuttke et al. (2025) — AI vs human conversational interviewing: https://doi.org/10.18653/v1/2025.latechclfl-1.17
- Collins, Brown & Newman (1989; Routledge reissue 2018) — cognitive apprenticeship: https://doi.org/10.4324/9781315044408-14
- Lyons et al. (2017) — cognitive apprenticeship in health sciences, review: https://doi.org/10.1007/s10459-016-9707-4
- Belland et al. (2017) — computer-based scaffolding in STEM, meta-analysis: https://doi.org/10.3102/0034654316670999
- Belland, Walker, Olsen & Leary (2015) — scaffolding pilot meta-analysis: Educational Technology & Society 18(1), 183–197, no DOI (ERIC EJ1062484)
- van de Pol, Volman & Beishuizen (2010) — scaffolding in teacher–student interaction: https://doi.org/10.1007/s10648-010-9127-6
- van de Pol et al. (2015) — contingent scaffolding classroom experiment: https://doi.org/10.1007/s11251-015-9351-z
- Puntambekar & Hübscher (2005) — critique of "scaffolding": https://doi.org/10.1207/s15326985ep4001_1
- Renkl et al. (2002) — fading worked-example steps: https://doi.org/10.1080/00220970209599510
- Salden et al. (2010) — adaptive vs fixed fading: https://doi.org/10.1007/s11251-009-9107-8
- Kalyuga & Sweller (2005) — rapid-test adaptive instruction: https://doi.org/10.1007/BF02504800
- Kirschner, Sweller & Clark (2006) — against minimal guidance: https://doi.org/10.1207/s15326985ep4102_1
- Hmelo-Silver, Duncan & Chinn (2007) — reply on scaffolded inquiry: https://doi.org/10.1080/00461520701263368
- Alfieri et al. (2011) — discovery learning meta-analyses: https://doi.org/10.1037/a0021017
- Loibl, Roll & Rummel (2017) — when problem solving before instruction works: https://doi.org/10.1007/s10648-016-9379-x
- Kapur (2008) — productive failure, Grade 11 kinematics: https://doi.org/10.1080/07370000802212669
- Schwartz et al. (2011) — inventing before being told, Grade 8 physics: https://doi.org/10.1037/a0025140
- Weaver et al. (2018) — explore-first in university physics: https://doi.org/10.1016/j.cedpsych.2017.12.003
- Bego, Chastain & DeCaro (2022) — contrasting cases before instruction, university physics: https://doi.org/10.1111/bjep.12555
- DeCaro et al. (2023) — explore-first randomized lesson, university physics: https://doi.org/10.3389/feduc.2023.1215975
- DeCaro et al. (2025) — exploration length before instruction, university chemistry: https://doi.org/10.1111/bjep.70007
- Ashman, Kalyuga & Sweller (2020) — explicit instruction first at high element interactivity: https://doi.org/10.1007/s10648-019-09500-5
- Ding et al. (2011) — conceptual scaffolding for synthesis problems in mechanics: https://doi.org/10.1103/physrevstper.7.020109
- Posner et al. (1982) — conceptual change: https://doi.org/10.1002/sce.3730660207
- Schroeder & Kucera (2022) — meta-analysis of refutation texts: https://doi.org/10.1007/s10648-021-09656-z
- Guzzetti et al. (1993) — meta-analysis of conceptual change interventions: https://doi.org/10.2307/747886
- Guzzetti (2000) — synthesis of text-based conceptual change: https://doi.org/10.1080/105735600277971
- Zengilowski, Schuetze, Nash & Schallert (2021) — critical review of refutation-text research: https://doi.org/10.1080/00461520.2020.1861948
- Limón (2001) — critique of cognitive conflict: https://doi.org/10.1016/S0959-4752%2800%2900037-2
- Shtulman & Valcarcel (2012) — naive theories coexist with scientific ones: https://doi.org/10.1016/j.cognition.2012.04.005
- diSessa (1993) — knowledge in pieces: https://doi.org/10.1080/07370008.1985.9649008
- diSessa, Gillespie & Esterly (2004) — coherence vs fragmentation for force: https://doi.org/10.1207/s15516709cog2806_1
- Vosniadou & Brewer (1992) — framework theory, mental models of the Earth: https://doi.org/10.1016/0010-0285%2892%2990018-W
- Kim & Pak (2002) — problems solved vs conceptual understanding: https://doi.org/10.1119/1.1484151
- Clement (1993) — bridging analogies in mechanics: https://doi.org/10.1002/tea.3660301007
- Crouch et al. (2004) — predicting before lecture demonstrations: https://doi.org/10.1119/1.1707018
- Miller et al. (2013) — observation and recall of demonstrations: https://doi.org/10.1103/PhysRevSTPER.9.020113
- Pollock (2009) — long-term retention after tutorials, E&M: https://doi.org/10.1103/PhysRevSTPER.5.020110
- Deslauriers & Wieman (2011) — retention after interactive engagement, quantum: https://doi.org/10.1103/physrevstper.7.010101
- Smart, Bos & Bos (2024) — LLM answers vs student misconceptions: https://doi.org/10.1007/978-3-031-60609-0_21
- Hestenes, Wells & Swackhamer (1992) — Force Concept Inventory: https://doi.org/10.1119/1.2343497
- Lasry et al. (2011) — FCI test–retest reliability of individual responses: https://doi.org/10.1119/1.3602073
- Traxler et al. (2018) — gender fairness of FCI items: https://doi.org/10.1103/physrevphyseducres.14.010103
- Eaton & Willoughby (2018) — confirmatory factor analysis of the FCI: https://doi.org/10.1103/physrevphyseducres.14.010124
- Stewart et al. (2018) — multidimensional IRT of the FCI: https://doi.org/10.1103/physrevphyseducres.14.010137
- Bao & Redish (2006) — model analysis, mixed model states: https://doi.org/10.1103/physrevstper.2.010103
- Rebello & Zollman (2004) — open-ended vs multiple-choice FCI items: https://doi.org/10.1119/1.1629091
- Madsen, McKagan & Sayre (2017) — best practices for administering concept inventories: https://doi.org/10.1119/1.5011826
- Nissen et al. (2018) — normalized gain vs Cohen's d: https://doi.org/10.1103/physrevphyseducres.14.010115
- Hake (1998) — interactive engagement vs traditional courses: https://doi.org/10.1119/1.18809
- Wu, Li & Rebello (2025) — EMCS item analysis: https://doi.org/10.1103/kvph-l899
- Savage & Rebello (2025) — GPT-4o coding of open-ended EMCS answers: https://doi.org/10.1119/perc.2025.pr.Savage
- Lichtenberger et al. (2024) — cluster RCT of formative assessment in kinematics: https://doi.org/10.1007/s11092-024-09445-6
- Chi et al. (1989) — self-explanation: https://doi.org/10.1207/s15516709cog1302_1
- Tan et al. (2025) — three-level meta-analysis of self-explanation in digital environments: https://doi.org/10.1007/s10648-025-10001-x
- Barbieri et al. (2023) — meta-analysis of worked examples in mathematics: https://doi.org/10.1007/s10648-023-09745-1
- Bisra et al. (2018) — meta-analysis of self-explanation: https://doi.org/10.1007/s10648-018-9434-x
- Rittle-Johnson, Loehr & Durkin (2017) — self-explanation meta-analysis, mathematics: https://doi.org/10.1007/s11858-017-0834-z
- Rittle-Johnson & Loehr (2017) — constraints on self-explanation prompts: https://doi.org/10.3758/s13423-016-1079-5
- Wittwer & Renkl (2010) — instructional explanations in example-based learning: https://doi.org/10.1007/s10648-010-9136-5
- Atkinson, Renkl & Merrill (2003) — fading plus self-explanation prompts: https://doi.org/10.1037/0022-0663.95.4.774
- Kissane et al. (2008) — fading in a workplace classroom: https://doi.org/10.1080/01443410802322069
- van Gog & Kester (2012) — worked examples, delayed retention: https://doi.org/10.1111/cogs.12002
- Hausmann & VanLehn (2010) — generation vs content in physics self-explanation: https://doi.org/10.3233/jai-2010-010
- Badeau et al. (2017) — self-explanation and analogical comparison, physics synthesis problems: https://doi.org/10.1103/physrevphyseducres.13.020112
- Gjerde et al. (2022) — quality of self-explanations in introductory mechanics: https://doi.org/10.1103/physrevphyseducres.18.010136
- Heckler (2010) — prompted force diagrams lowered novice performance: https://doi.org/10.1080/09500690903199556
- Kalyuga et al. (2001) — expertise reversal with worked examples: https://doi.org/10.1037/0022-0663.93.3.579
- Chen, Kalyuga & Sweller (2015) — element interactivity and the worked-example effect: https://doi.org/10.1037/edu0000018
- Rey & Fischer (2013) — expertise reversal for instructional explanations: https://doi.org/10.1007/s11251-012-9237-2
- Sinha & Kapur (2021) — problem solving before instruction, meta-analysis: https://doi.org/10.3102/00346543211019105
- Chen et al. (2026) — LLM feedback on self-explanations, calculus: https://doi.org/10.1007/978-3-032-29763-1_42
- Corbett & Anderson (1995) — knowledge tracing: https://doi.org/10.1007/BF01099821
- Piech et al. (2015) — deep knowledge tracing: arXiv 1506.05908
- Khajah, Lindsey & Mozer (2016) — extended BKT matches deep KT: arXiv 1604.02416
- Gervet et al. (2020) — when deep learning is best for knowledge tracing: https://doi.org/10.5281/zenodo.4143614
- Pavlik, Cen & Koedinger (2009) — Performance Factors Analysis: https://doi.org/10.3233/978-1-60750-028-5-531
- Doroudi & Brunskill (2017) — BKT identifiability and semantic degeneracy: https://files.eric.ed.gov/fulltext/ED577166.pdf
- Doroudi & Brunskill (2019) — equitability of knowledge tracing: https://doi.org/10.1145/3303772.3303838
- Doroudi, Aleven & Brunskill (2019) — review of RL for instructional sequencing: https://doi.org/10.1007/s40593-019-00187-x
- Cen, Koedinger & Junker (2007) — over-practice in the Cognitive Tutor (AIED 2007, no DOI): http://pact.cs.cmu.edu/koedinger/pubs/Cen%20&%20Koedinger%20AIED07.pdf
- Liu & Koedinger (2017) — closing the loop on a KC-model discovery: https://files.eric.ed.gov/fulltext/EJ1155896.pdf
- Lyu et al. (2026) — data-driven redesign on units chosen by topic: https://doi.org/10.1007/978-3-032-29760-0_12
- Kulik, Kulik & Bangert-Drowns (1990) — mastery learning meta-analysis: https://doi.org/10.3102/00346543060002265
- Koedinger, Stamper, McLaughlin & Nixon (2013) — KC-based tutor redesign: https://doi.org/10.1007/978-3-642-39112-5_43
- Huang et al. (2021) — multi-method data-driven tutor redesign: https://doi.org/10.1145/3448139.3448155
- Slavin (1987) — mastery learning reconsidered: https://doi.org/10.3102/00346543057002175
- Black & Wiliam (1998) — assessment and classroom learning: https://doi.org/10.1080/0969595980050102
- Bennett (2011) — formative assessment, a critical review: https://doi.org/10.1080/0969594X.2010.513678
- Kingston & Nash (2011) — formative assessment meta-analysis: https://doi.org/10.1111/j.1745-3992.2011.00220.x
- Briggs et al. (2012) — critique of the Kingston & Nash meta-analysis: https://doi.org/10.1111/j.1745-3992.2012.00251.x
- Klute et al. (2017) — formative assessment in elementary grades, REL Central (ERIC ED572929)
- Lee et al. (2020) — formative assessment in US K–12, systematic review: https://doi.org/10.1080/08957347.2020.1732383
- Adesope, Trevisan & Sundararajan (2017) — practice-test meta-analysis: https://doi.org/10.3102/0034654316689306
- Kluger & DeNisi (1996) — feedback intervention meta-analysis: https://doi.org/10.1037/0033-2909.119.2.254
- Hattie & Timperley (2007) — the power of feedback: https://doi.org/10.3102/003465430298487
- Wisniewski, Zierer & Hattie (2020) — feedback meta-analysis: https://doi.org/10.3389/fpsyg.2019.03087
- Van der Kleij, Feskens & Eggen (2015) — computer-based feedback meta-analysis: https://doi.org/10.3102/0034654314564881
- Heckler & Mikula (2016) — feedback complexity in physics practice: https://doi.org/10.1103/PhysRevPhysEducRes.12.010134
- Kandemir et al. (2026) — feedback timing meta-analysis: https://doi.org/10.1007/s10648-026-10117-8
- Mullet et al. (2014) — delayed feedback and transfer in engineering: https://doi.org/10.1016/j.jarmac.2014.05.001
- Yang et al. (2021) — classroom quizzing meta-analysis: https://doi.org/10.1037/bul0000309
- Pan & Rickard (2018) — transfer of test-enhanced learning: https://doi.org/10.1037/bul0000151
- Crouch & Mazur (2001) — Peer Instruction, ten years: https://doi.org/10.1119/1.1374249
- Smith et al. (2009) — peer discussion and isomorphic questions: https://doi.org/10.1126/science.1165919
- Morris, Perry & Wardle (2021) — feedback in higher education, systematic review: https://doi.org/10.1002/rev3.3292
- Kulik & Fletcher (2016) — ITS meta-analysis: https://doi.org/10.3102/0034654315581420
- VanLehn (2011) — human, step-based and answer-based tutoring compared: https://doi.org/10.1080/00461520.2011.611369
- Ma, Adesope, Nesbit & Liu (2014) — ITS meta-analysis: https://doi.org/10.1037/a0037123
- Steenbergen-Hu & Cooper (2013) — ITS in K–12 mathematics, meta-analysis: https://doi.org/10.1037/a0032447
- Steenbergen-Hu & Cooper (2014) — ITS in college, meta-analysis: https://doi.org/10.1037/a0034752
- Pane, Griffin, McCaffrey & Karam (2014) — Cognitive Tutor Algebra at scale, cluster RCT: https://doi.org/10.3102/0162373713507480
- VanLehn et al. (2005) — Andes physics tutor evaluations: https://doi.org/10.3233/irg-2005-15%283%2902
- VanLehn (2006) — inner and outer loop: https://doi.org/10.3233/irg-2006-16%283%2902
- Chi, VanLehn, Litman & Jordan (2011) — RL-induced pedagogical policies, physics: https://doi.org/10.3233/jai-2011-014
- Bastani et al. (2025) — GPT-4 tutoring and unassisted exam performance, field RCT: https://doi.org/10.1073/pnas.2422633122
- Pardos & Bhandari (2024) — ChatGPT vs human hints: https://doi.org/10.1371/journal.pone.0304013
- Létourneau et al. (2025) — systematic review of AI-driven K–12 ITS: https://doi.org/10.1038/s41539-025-00320-7
- Lehmann, Cornelius & Sting (2024) — LLM use and learning in programming, lab RCTs: arXiv 2409.09047
- Contractor & Reyes (2026) — generative AI access and unaided learning, randomized: arXiv 2607.08849
- Fischer, Rau & Rilke (2025) — AI tutor access and timing, lab RCT: https://docs.iza.org/dp18338.pdf
- Kumar, Rothschild, Goldstein & Hofman (2025) — LLM explanations in math learning: https://doi.org/10.1007/978-3-031-98459-4_5
- Fan et al. (2025) — "metacognitive laziness", ChatGPT in writing: https://doi.org/10.1111/bjet.13544
- Stadler, Bannert & Sailer (2024) — LLM vs web search in scientific inquiry: https://doi.org/10.1016/j.chb.2024.108386
- Melumad & Yun (2025) — LLM syntheses vs web search and depth of learning: https://doi.org/10.1093/pnasnexus/pgaf316
- Darvishi et al. (2024) — AI assistance and student agency: https://doi.org/10.1016/j.compedu.2023.104967
- Oreopoulos & Low (2026) — Khanmigo two-year cluster RCT: https://doi.org/10.26300/kner-hv33
- Henkel et al. (2024) — AI math tutor in Ghana: https://doi.org/10.1007/978-3-031-64315-6_34
- De Simone et al. (2025) — GPT-4 after-school programme in Nigeria: https://doi.org/10.1596/1813-9450-11125
- Nie et al. (2025) — offering GPT-4 in a massive coding course: https://doi.org/10.1145/3698205.3733960
- Wang et al. (2025) — Tutor CoPilot RCT: https://doi.org/10.26300/81nh-8262
- Deng et al. (2025) — ChatGPT meta-analysis: https://doi.org/10.1016/j.compedu.2024.105224
- Weidlich, Gašević, Drachsler & Kirschner (2025) — critique of ChatGPT efficacy studies: https://doi.org/10.1111/jcal.70105
- Kestin et al. (2025) — AI tutoring RCT in undergraduate physics: https://doi.org/10.1038/s41598-025-97652-6
- Meyer & Land (2005) — threshold concepts and troublesome knowledge (2): https://doi.org/10.1007/s10734-004-6779-5
- Meyer & Land (2006) — *Overcoming Barriers to Student Understanding*: https://doi.org/10.4324/9780203966273
- Rowbottom (2007) — demystifying threshold concepts: https://doi.org/10.1111/j.1467-9752.2007.00554.x
- Salwén (2021) — threshold concepts, obstacles or scientific dead ends?: https://doi.org/10.1080/13562517.2019.1632828
- Barradell (2013) — identifying threshold concepts, methods review: https://doi.org/10.1007/s10734-012-9542-3
- Quinlan et al. (2013) — methodological challenges in threshold-concept research: https://doi.org/10.1007/s10734-013-9623-y
- Nicola-Richmond et al. (2018) — measuring threshold crossing, synthesis: https://doi.org/10.1080/07294360.2017.1339181
- Aptyka, Fiedler & Großschedl (2025) — threshold-concept instruction in evolution: https://doi.org/10.1002/sce.21977
- Ma et al. (2025) — threshold concepts in clinical simulation, randomized: https://doi.org/10.3389/fmed.2025.1690297
- Lovett et al. (2023), _How Learning Works: Eight Research-Based Principles for Smart Teaching_, 2nd ed. — useful umbrella reference, **optional**, not part of the mandatory reading pack.

---

## Current recommendation

**Research first:** DtD (bottleneck framing) + CTA (elicitation) → Expert–Novice → PCK.  
**Then connect learner diagnosis:** conceptual change / concept inventories.  
**Then connect instructional mechanisms:** cognitive apprenticeship + worked examples/self-explanation.  
**Only then formalize the AI system:** explicit student model / knowledge tracing + ITS architecture + LLM interaction layer.

The first prototype should be a **research instrument for expert elicitation and learner diagnosis**, not yet a complete tutoring platform.
