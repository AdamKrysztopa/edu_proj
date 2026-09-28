# Approach comparison: the 13 research families (roadmap step 1)

**Question:** what does each family contribute to the pipeline, expert elicitation → learner diagnosis → instruction → delivery and adaptation, how strong is that contribution, and where do the families overlap?

**Verdict:** the 13 families are not 13 alternatives. After overlaps are removed, one candidate remains per layer, plus shared constraints. Evidence is strongest for instruction (worked examples with self-explanation, elaborated feedback). It is moderate–high for elicitation, but only outside physics. It is good for cohort-level diagnosis, weak for individual diagnosis, and weakest for adaptation. The gap shared by every family is delayed transfer in university physics.

**Sources:** the graded cards in map §4–§5 and the branch notes they cite. No new search was made for this note; ratings are the map's. This note compares; it does not select. Selection is step 3.

## By layer

### Expert elicitation

| Family | Role in the pipeline | Strongest evidence | Main limit for this project | Overlaps |
|---|---|---|---|---|
| **Decoding the Disciplines** | Instructional frame: bottleneck → model → practice → assess | Low–moderate: two small non-randomized comparisons, immediate outcomes, none in physics | The decoding interview has never been compared with any other elicitation method | CTA (step 2), Cognitive Apprenticeship (steps 3–4), formative assessment (step 6), Threshold Concepts (step 1) |
| **Cognitive Task Analysis** | Elicitation method: think-aloud on a performed task, then retrospective probes over the trace | Moderate–high: CTA-based training g = 0.87 across domains; experts omit about 70% of knowledge and decision steps when teaching (surgery, 3 experts) | No physics study, no transfer outcome, no evaluation of an LLM conducting CTA; over 100 methods and no validated basis for choosing one | DtD step 2; Expert–Novice supplies what to look for |
| **Expert–Novice research** | Theory of what hidden knowledge looks like (representation, principle selection), and a frame for tagging operations that are already published | High as description: experts represent physics problems by principle, novices by surface features; principle-first instruction helps immediate problem solving in small physics studies; one far-transfer RCT | Expertise is a continuum and categorization is only a proxy; no delayed transfer | CTA coding frame; worked examples (principle-first); Knowledge Tracing (candidate KCs) |
| **Pedagogical Content Knowledge** | Now a diagnosis input: difficulty knowledge taken from student data, with teachers adding representations and analogies | Moderate, correlational only (pooled r = .13 n.s. to .23) | Content experts hold it only partly: physics TAs and instructors scored 65% and 68% of the maximum when predicting students' most common wrong FCI answers (chance 40%); no experiment isolates PCK | Concept Inventories (seed data), Conceptual Change |

### Learner diagnosis

| Family | Role in the pipeline | Strongest evidence | Main limit for this project | Overlaps |
|---|---|---|---|---|
| **Conceptual Change** | Theory of learner models, and two interventions: refutation, and predict-then-observe | High that intuitive ideas persist alongside instruction; moderate for interventions (refutation g = 0.41, holding at delay) | Theory contested (coherent vs in pieces); an individual misconception label is bound to its context | Concept Inventories; formative assessment (predict first); worked examples |
| **Concept Inventories** | Cohort-level measurement; distractor frequencies seed the difficulty layer; external validation | High for class-level evaluation (FCI total score test–retest r = 0.89) | Weak for one student: 31% of FCI item answers changed on retest within a week; distractors miss student ideas | PCK, Conceptual Change, the evaluation layer |
| **Threshold Concepts** | At most vocabulary for naming a candidate bottleneck | Low / contested: no inter-rater or cross-institution agreement statistic for identifying one (Delphi studies report only percentage agreement) | Adds nothing tested beyond DtD step 1 plus Conceptual Change | DtD step 1 |
| **Knowledge Tracing** | Explicit learner state | Moderate–high for predicting the next answer; on moderate-sized data simple models match or beat deep ones, which lead only on the largest datasets | For learning: a few small studies on hand-picked units, one null on units chosen by topic, and no test against an N-correct-in-a-row rule | ITS student model; Cognitive Apprenticeship fading depends on it |

### Instruction

| Family | Role in the pipeline | Strongest evidence | Main limit for this project | Overlaps |
|---|---|---|---|---|
| **Worked Examples + Self-Explanation** | Carrier for an elicited operation: a worked step plus a prompt to justify or apply it | High: g ≈ 0.5 immediate, ≈ 0.35 delayed, 0.33–0.53 on transfer (meta-analyses, mostly outside physics); randomized physics studies for immediate performance and one far transfer | Expertise reversal; explanations handed to the learner add little; the one LLM self-explanation-feedback RCT found no post-test difference | Cognitive Apprenticeship (modelling, articulation); Expert–Novice (principle-first) |
| **Cognitive Apprenticeship** | Sequencing frame: model, coach, scaffold, fade | Moderate: components supported (computer-based scaffolding g = 0.46) | Whole model untested in physics; fixed-schedule fading no better than none; exploring first wins on average (g = 0.36) and in university physics when the activity has contrasting cases, but not without them; instruction first won only for primary pupils at high element interactivity | Worked examples + self-explanation, ITS, Knowledge Tracing |
| **Formative assessment + feedback** | Feedback policy and low-stakes checks | High for practices: feedback d = 0.48 (elaborated ≫ right/wrong), quizzing g = 0.50; packaged interventions d ≈ 0.2–0.3 | Over a third of feedback interventions lowered performance; little causal university evidence; no delayed-transfer study in physics | ITS step feedback; Concept Inventories (diagnosis helps only when it drives a response) |

### Delivery and adaptation

| Family | Role in the pipeline | Strongest evidence | Main limit for this project | Overlaps |
|---|---|---|---|---|
| **Intelligent Tutoring Systems** | Architecture prior: separate domain, student and pedagogy models; step-level checking; explicit policy; answers withheld until an attempt | High on tests aligned to the tutor (0.73 SD) | 0.13 SD on standardized tests and about 0–0.2 SD at scale; the one university-physics field evaluation (Andes) is non-randomized, with d = 0.25 on an answer-only final | LLM tutoring, Knowledge Tracing, formative feedback |
| **LLM-based tutoring** | Dialogue generation inside a fixed design; also the candidate AI interviewer for elicitation | Emerging: a large immediate effect in one university-physics trial that bundled the AI with self-pacing and pre-structured steps | With the AI removed at test, ≈ 0.1–0.4 SD, null in preregistered lab RCTs, harmful without guardrails; the one transfer measure was null | ITS (delivery); CTA (AI interviewer) |

## What collapses

1. **DtD step 2 is CTA.** CTA is the elicitation method, with DtD's other steps as the frame; the decoding interview survives only as a comparison arm in Phase 2.
2. **Cognitive Apprenticeship's modelling and articulation are worked examples with self-explanation.** What it adds is sequencing and fading, and fading needs a learner model.
3. **Threshold Concepts add nothing tested to DtD step 1 and Conceptual Change,** since there are no reliability data for identifying one.
4. **PCK's difficulty knowledge is student response data:** inventory distractors plus coded open answers. What remains unique to PCK is teacher-contributed representations, which are untested.
5. **The ITS student model is Knowledge Tracing, ITS feedback is formative feedback, and LLM tutoring is ITS delivery with generation.** The one delivery question unique to LLMs is whether generation adds anything over the same design delivered statically.
6. **Expert–Novice research is not a method.** It is the theory that tells elicitation what to look for and instruction what to target.

Five independent choices remain for step 3:
- an elicitation method;
- a source of diagnosis, and its grain (cohort or individual);
- an instructional carrier and feedback policy;
- a delivery architecture, including whether generation is learner-facing;
- a learner model, or a simple rule instead.

## Evidence gradient

Evidence falls along the pipeline. Instruction has meta-analytic support at delay, mostly outside physics; the one delayed physics measure found a marginal or small advantage. Elicitation has meta-analytic support only outside physics and for immediate outcomes. Diagnosis is sound at cohort level; for individuals, total scores are stable on retest but item answers and misconception labels are not. Adaptation has the least: no study tests a KT policy against a simple mastery rule on delayed or transfer outcomes; fading logic did not moderate scaffolding effects in the meta-analysis, though per-learner adaptation won in two single studies outside physics; and none of 8 sequencing experiments with a learner model beat all baselines. The AI-specific roles (interviewer, individual diagnostician, self-explanation feedback) are the least tested of all.

## Decision-critical gaps (input to step 2)

Only gaps whose answer could change the route, not just a rating:

1. **Premise.** Do hidden expert operations, rather than missing prerequisites or too little practice, cause a meaningful share of errors on the target topic? This decides whether elicitation is the front end at all (Phase 1 kill criterion). No study answers it for this topic; K0 is the prepared check.
2. **AI as interviewer.** Do AI-led retrospective probes recover valid operations beyond the trace and a human interviewer? This decides whether AI sits in elicitation or only in delivery. No study exists; it is Stage A's question.
3. **Individual diagnosis.** Does any method (multi-item, LLM-coded open answers, hybrid) give a diagnosis that is stable on retest and across contexts? This decides cohort-level versus per-learner diagnosis in the first version (Phase 3).
4. **Generation.** With the design held fixed, does an LLM beat a static or rule-based version on an unassisted, delayed test? This decides whether an LLM faces learners in the first version.
5. **Learner model.** Does a KT-driven policy beat N-correct-in-a-row on delayed transfer? This decides whether the first version needs KT.
6. **Order.** In multi-principle mechanics, does exploring first beat modelling first at delay? This decides the default sequence.

A seventh gap, delayed transfer for worked examples with self-explanation in university physics, changes the expected effect size and the SESOI, not the choice.

Step 2 checks whether the literature already settles any of these. The rest become explicit assumptions, each tied to a milestone test in step 6.
