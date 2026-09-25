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
| **P0** | **Pedagogical Content Knowledge (PCK)** | Focuses on what teachers need to know about representations, difficulty and learner misconceptions | **Moderate–high** for correlational links to school achievement (strongest in mathematics, mixed in physics); no experiment isolating PCK; no university or transfer outcomes | High | High | High |
| **P1** | **Conceptual Change + misconception research** | Addresses learners whose existing mental model conflicts with the target model | **High, especially science education** | **Very high** | Medium | High |
| **P1** | **Concept Inventories / diagnostic instruments** | Makes hidden misconceptions measurable; physics is unusually mature here | **High for well-validated instruments** | **Very high** | Low–medium | **Very high** |
| **P1** | **Cognitive Apprenticeship** | Converts expert cognition into modelling, coaching, scaffolding and fading | **Moderate** | High | High | **Very high** |
| **P1** | **Worked Examples + Self-Explanation** | Strong candidate for turning decoded expert operations into teachable interactions | **High** | **Very high** | Medium | **Very high** |
| **P1** | **Intelligent Tutoring Systems (ITS)** | Mature evidence base for individualized step-level instruction and feedback | **High overall, heterogeneous** | **Very high** | Medium–high | **Very high** |
| **P1** | **Knowledge Tracing / Mastery models** | Provides a computational learner-state layer rather than relying on LLM intuition | **Moderate–high** | High | Medium | **Very high** |
| **P2** | **Threshold Concepts** | Useful language for transformative/troublesome disciplinary ideas | **Moderate / contested** | High | High | Medium–high |
| **P2** | **Formative assessment** | Essential feedback loop for checking whether the intervention actually worked | **High as a broad principle** | High | High | High |
| **P2** | **LLM-based AI tutoring** | Potential delivery/orchestration layer; promising but evidence is newer than classic ITS | **Emerging / moderate** | High | High | N/A — implementation layer |

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
- **No experiment isolates PCK:** too few intervention studies measure it separately (Gonzalez, Lynch & Hill 2022). A systematic review of 217 science-PCK studies found the student-outcome link inconclusive (Park & Chan 2025); a meta-analysis found it positive only under multilevel models (Fukaya et al. 2025).
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

Seed the misconception, misleading-cue and diagnostic-question entries from student response data (concept-inventory distractors, coded exam errors), not from expert or teacher prediction: TAs miss many common difficulties, and experienced instructors scored no better (Maries & Singh 2016). Teachers review these entries and contribute representations, analogies and explanation variants, the part student data cannot supply.

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

### AI opportunity
The tutor should identify a learner’s current model from explanations and predictions, then generate **discriminating cases** that separate the learner’s model from the target model.

### Questions to research next
- Can an LLM reliably infer a misconception from free-form reasoning?
- Should diagnosis be generative, inventory-based, or hybrid?
- How do we distinguish a slip/calculation error from a stable conceptual model?
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

### AI opportunity
Use concept inventories as:
- seed labels for misconception models;
- benchmark datasets for diagnostic dialogues;
- sources of contrastive questions;
- external validation for an AI’s inferred learner state.

Do **not** assume an individual concept-inventory score is a complete learner model; these instruments are generally designed for specific assessment purposes and have construct limitations.

### Questions to research next
- Which physics concept inventories are available for mechanics, E&M, quantum, thermodynamics, mathematics methods, etc.?
- Which are validated for individual diagnosis vs cohort/course evaluation?
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

### AI opportunity
An AI tutor can switch roles dynamically:
- demonstrate expert reasoning;
- coach the learner;
- provide partial scaffolds;
- request articulation;
- compare learner reasoning with expert reasoning;
- fade assistance as competence increases.

### Questions to research next
- How should scaffolding be faded automatically?
- What evidence shows when modelling should stop and productive struggle should begin?
- Which components have the strongest causal evidence?

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

### AI opportunity
Very high and comparatively easy to test experimentally:
- expert worked example;
- omitted step / completion problem;
- self-explanation prompt;
- AI diagnosis of explanation;
- progressively faded solution;
- transfer problem.

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
The evidence base is substantially stronger than for most generative-AI tutoring. Kulik & Fletcher’s meta-analysis of 50 controlled evaluations reported a median effect of **0.66 standard deviations over conventional instruction**, while emphasizing that outcomes depend strongly on assessment alignment and implementation quality. A 2025 systematic review of K–12 AI-driven ITS found generally positive effects, but advantages were smaller when compared with stronger non-intelligent tutoring systems.

### Domain fit
Very strong in mathematics/science and procedural domains; also used in reading, medicine, law and other areas.

### AI opportunity
Treat decades of ITS work as the **architecture and pedagogy prior** for LLM tutoring rather than starting from chatbot design.

### Questions to research next
- Which classical ITS design principles remain essential when generation becomes flexible?
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

### AI opportunity
Combine explicit knowledge tracing with qualitative evidence extracted from dialogue. The LLM becomes an **observation and explanation layer**, not the sole state estimator.

### Questions to research next
- What is the correct “knowledge component” for physics: concept, equation, representation, procedure, misconception, or expert mental operation?
- Can DtD-derived mental operations become knowledge components?
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

### AI opportunity
Use AI to propose candidate threshold concepts from expert interviews and learner data, but require empirical validation.

### Questions to research next
- Does “threshold concept” add predictive value beyond bottlenecks, misconceptions and prerequisite graphs?
- Can candidate thresholds be identified from longitudinal learning data?
- Are threshold concepts stable across instructors and curricula?

### Minimum reading if this branch is selected
Meyer & Land (2003/2005), **Threshold Concepts and Troublesome Knowledge.**  
Also read one critique before adopting the construct operationally.

---

## 5.12 LLM-Based Tutoring — **delivery layer, not the theory of learning**

### Current evidence signal
The field is promising but much younger than ITS. A 2025 randomized controlled trial in an undergraduate physics course reported substantially higher learning gains in less time with a carefully designed AI tutor than with the study’s in-class active-learning condition. Crucially, the tutor was **deliberately engineered around evidence-based pedagogical practices**; the result should not be generalized to arbitrary chatbots.

Recent systematic reviews also identify risks: over-reliance, technical unreliability, assessment problems, privacy, and lack of rigorous long-term evidence.

### Design implication
Do not ask “Which LLM should tutor students?” first. Ask:

1. What learner state is represented?
2. What bottleneck was diagnosed?
3. What evidence supports the chosen intervention?
4. What knowledge sources constrain factual content?
5. What does the model do when uncertain?
6. How do we measure transfer rather than immediate correctness?

### Questions to research next
- Can LLMs conduct expert elicitation as well as tutoring?
- Can a single model safely separate interviewer, diagnostician and tutor roles?
- What should be deterministic/rule-based vs generative?
- How much value comes from the LLM itself versus the instructional design wrapped around it?

### Minimum reading if this branch is selected
Kestin et al. (2025), **“AI tutoring outperforms in-class active learning: an RCT introducing a novel research-based design in an authentic educational setting.”**  
https://doi.org/10.1038/s41598-025-97652-6

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
The **LLM should probably be an interface/reasoning component, not the database of truth, the student model, the pedagogy model and the evaluator simultaneously.** Classical ITS research strongly suggests keeping these concerns conceptually separable even if one foundation model participates in several of them.

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
- **Stage B:** a two-arm RCT, about 370 students. The control is worked examples built from the experts' ordinary explanations. The treatment adds validated operations from the AI-assisted pipeline, length- and time-matched and delivered statically. The primary outcome is delayed transfer, scored for correctness only; SESOI d = 0.30. An arm × pretest interaction is prespecified as exploratory (expertise reversal).

**Kill criteria:**
- **K1 (gate to Stage B):** at least 3 performed, shared operations absent from ordinary material, at least 2 of them added by AI probes, and the AI-minus-human contradicted rate (95% CI upper bound) no more than 15 points. If only the AI-added condition fails, Stage B tests trace-based CTA instead.
- **K2 (after Stage B):** with compliance of at least 70%, an upper bound of the 90% CI for delayed transfer below d = 0.30 stops the use of elicited operations as instruction for this topic.

---

## Phase 3 — diagnose learner bottlenecks
For the same topic, compare:
- conventional test;
- concept-inventory style items;
- open-ended explanation;
- AI Socratic diagnostic dialogue;
- hybrid diagnosis.

Measure not only classification accuracy but **instructional utility**: does the diagnosis lead to a better next intervention?

---

## Phase 4 — intervention experiment
Convert decoded operations into several interventions:
- direct explanation;
- expert modelling;
- worked example;
- self-explanation;
- guided practice;
- Socratic questioning.

Randomize or counterbalance where feasible.

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
- define tutoring policies;
- then optimize personalization.

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
- Do **not** use concept inventories outside their validated purpose without checking validity.
- Do **not** assume higher predictive accuracy in a student model means better pedagogy.
- Do **not** assume an unconstrained chatbot inherits the evidence base of intelligent tutoring systems.
- Do **not** evaluate only immediate post-test performance; include retention and transfer.
- Do **not** assume experts or instructors know which difficulties are common; check against student response data.

---

# 12. Evidence notes that should shape the project

1. **DtD is directly aligned with the problem, but its empirical base is less mature than its conceptual fit suggests.** Keep it as the pedagogical framing (bottleneck → model → practice → assess). Its interview step is not evidential without CTA-style validation against performed tasks.
2. **CTA offers a more mature toolkit for extracting expert cognition.** Combining it with DtD is likely more defensible than using DtD interviewing alone. No physics or transfer evidence yet; start with think-aloud on performed tasks plus retrospective CDM probes.
3. **Physics is a strategically strong first domain.** It offers classic expert–novice findings, validated misconception instruments, structured problems and objective checks. Expert–novice differences are well replicated but form a continuum; instruction built on them has immediate, not yet delayed-transfer, evidence.
4. **Classical ITS research should be treated as required prior art.** Meta-analytic evidence for ITS is much stronger than the current evidence for generic LLM tutors.
5. **Recent AI-tutoring evidence is encouraging but narrow.** Strong results have come from carefully engineered pedagogical systems, not generic “ask an LLM” interactions.
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
- Collins, Brown & Newman (1989) — cognitive apprenticeship
- Posner et al. (1982) — conceptual change
- Hestenes, Wells & Swackhamer (1992) — Force Concept Inventory: https://doi.org/10.1119/1.2343497
- Chi et al. (1989) — self-explanation: https://doi.org/10.1207/s15516709cog1302_1
- Corbett & Anderson — knowledge tracing / cognitive tutors
- Kulik & Fletcher (2016) — ITS meta-analysis: https://doi.org/10.3102/0034654315581420
- Létourneau et al. (2025) — systematic review of AI-driven K–12 ITS: https://doi.org/10.1038/s41539-025-00320-7
- Kestin et al. (2025) — AI tutoring RCT in undergraduate physics: https://doi.org/10.1038/s41598-025-97652-6
- Lovett et al. (2023), _How Learning Works: Eight Research-Based Principles for Smart Teaching_, 2nd ed. — useful umbrella reference, **optional**, not part of the mandatory reading pack.

---

## Current recommendation

**Research first:** DtD (bottleneck framing) + CTA (elicitation) → Expert–Novice → PCK.  
**Then connect learner diagnosis:** conceptual change / concept inventories.  
**Then connect instructional mechanisms:** cognitive apprenticeship + worked examples/self-explanation.  
**Only then formalize the AI system:** explicit student model / knowledge tracing + ITS architecture + LLM interaction layer.

The first prototype should be a **research instrument for expert elicitation and learner diagnosis**, not yet a complete tutoring platform.
