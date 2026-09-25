# Explore: LLM-based AI tutoring

**Question:** How strong is the evidence that LLM tutoring improves learning once the outcome is unassisted (the AI removed), the comparison controls for the pedagogical design, and the timing is delayed, and what does it say about what should be generative versus fixed (§5.12 questions)?

**Verdict: no change to priority (P2); the rating "Emerging / moderate" is scoped.** The one university-physics trial (Kestin et al. 2025) found a large immediate effect, but it changes several things at once: the AI tutor, self-pacing, working at home, and a platform that walked students through each part in order with pre-written solutions. Outside it, controlled studies with unassisted tests find:
- small-to-moderate gains when the tutor is constrained or used for explanations (about 0.2–0.4 SD);
- nulls in two preregistered lab experiments;
- harm when an unconstrained chatbot gives answers during practice;
- about 0.06–0.08 SD per school year at scale, where students seldom used the tutor for substantive dialogue.

Across these studies, how students use the model (asking for explanations vs asking for solutions) moves outcomes as much as whether it is available. The meta-analyses (g ≈ 0.6) rest on primary studies that mostly fail basic design checks, and one widely cited meta-analysis has been retracted. Only one study measures retention after a delay (one week, Contractor & Reyes 2026, preprint); a few measure at the end of a longer intervention (8 months to a school year), and the only transfer measure (Fan et al. 2025) found no difference.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline:
- §4 row: P2, "Emerging / moderate", STEM fit High, humanities High, AI readiness "N/A — implementation layer".
- The §5.12 card and its four questions:
  - Can LLMs conduct expert elicitation as well as tutoring?
  - Can one model separate interviewer, diagnostician and tutor?
  - What should be deterministic vs generative?
  - How much value comes from the LLM versus the instructional design?
- §12 note 5: "Strong results have come from carefully engineered pedagogical systems".
- Overlap: `explore-intelligent-tutoring-systems.md` already covers Bastani et al. (2025) and Pardos & Bhandari (2024) as evidence for classical ITS principles. They are cited here only where they bear on the §5.12 questions.

The branch serves §9 Phase 2 Stage B (static delivery), Phases 4–5, and §10 RQ5 and RQ8.

Search:
- OpenAlex REST returned HTTP 429 on both attempts. The Semantic Scholar batch endpoint also returned 429; its single-paper endpoint worked for some abstracts.
- Also used: Crossref, the arXiv API and WebSearch.
- Full text read: Kestin et al. (2025, Scientific Reports HTML), Henkel et al. (2024, arXiv PDF), Lehmann, Cornelius & Sting (arXiv PDF), Oreopoulos & Low (2026, EdWorkingPaper PDF) and Fischer, Rau & Rilke (2025, IZA PDF).
- Abstracts or search summaries only, marked below: Stadler et al., Darvishi et al., Deng et al. The citation check read De Simone et al. (WB PRWP 11125), Nie et al., Contractor & Reyes and Tutor CoPilot (EdWorkingPaper 24-1054) in full.
- Zotero: the local API holds Kestin et al. (2025) and Kulik & Fletcher (2016), with no notes.

## Evidence

### The anchor study: Kestin et al. (2025)

| Source | Design | N | Domain | Outcome and timing | Finding |
|---|---|---|---|---|---|
| Kestin, Miller, Klales, Milbourne & Ponti (2025), https://doi.org/10.1038/s41598-025-97652-6 | Crossover, two consecutive weeks, one lesson each (surface tension, fluid flow). Randomized by peer-instruction group (2–3 students), not by individual. | 233 enrolled; 194 eligible. The post-test comparison reports 142 AI and 174 in-class observations. | **University introductory physics** for life-science students (Harvard PS2) | Short pre- and post-lesson quizzes written from the learning goals by a team member who did not design the tutor. **Immediate**, same session. The paper does not say where or under what supervision the AI group took its post-test; since the AI lesson was done at home, it was presumably unsupervised (not stated). | Median post-test 4.5 (AI) vs 3.5 (in-class), against a pooled pretest median of 2.75, so "over double" the median gain. Mann–Whitney p < 10⁻⁸. The regression effect is 0.63, and 0.73–1.3 SD from a quantile regression that corrects the ceiling. Median time on task was 49 min vs an assumed 60 min in class, and time did not correlate with the post-test. |

What the treatment was, from the paper:
- GPT-4 with a system prompt for active engagement, cognitive-load management and growth mindset.
- Expert-written, question-specific prompts with **pre-written step-by-step solutions**; the authors "avoided relying solely on GPT-4 to generate solutions".
- A platform that **guided students sequentially through each part of each problem**, because "a system prompt could not reliably provide enough structure".
- Pre-recorded introductory videos, self-paced, at home.

The control was the same worksheet in an in-person peer-instruction class.

**Assessment.** It is a well-built trial with authentic content, a strong active-learning control and separate test authorship. But the contrast bundles four changes at once: the AI, self-pacing, the home setting (the AI group's post-test conditions are not reported and were presumably unsupervised), and the video delivery. The authors' own limitations section says the gains "may also depend on" high-quality videos, expert question-specific prompts and a carefully structured framework. They also do not presume the result extends to tasks "requiring complex synthesis of multiple concepts". The outcome is immediate and covers one lesson per condition; there is no retention or transfer test. The post-test comparison reports 142 AI and 174 in-class observations (316, not the 388 implied by 194 eligible students who completed all tests). Neither the paper nor the Supplementary Information explains the gap or why the AI arm lost more observations.

### Controlled studies with an unassisted learning outcome

| Source | Design | N | Domain | Outcome and timing | Finding |
|---|---|---|---|---|---|
| Bastani et al. (2025), https://doi.org/10.1073/pnas.2422633122 | Field RCT, three arms. The model is fixed (GPT-4); only the wrapper differs. | ~1,000 | High-school mathematics, Turkey; **not university** | Unassisted exam, same session | "GPT Base" raised practice scores but lowered the unassisted exam by 17%. "GPT Tutor" (hints only, teacher-written solutions and common mistakes in the prompt) largely removed the harm, with no positive exam effect. Details in `explore-intelligent-tutoring-systems.md`. |
| Lehmann, Cornelius & Sting (2024), arXiv 2409.09047 (SSRN https://doi.org/10.2139/ssrn.4941259) | Two preregistered, incentivized lab RCTs plus a quasi-experimental field study (ChatGPT outages as an instrument) | Lab: 107 and 69; field: 113 students, 6,594 answers | Introductory Python; lab subjects from a German university's participant pool, field study in two graduate programming courses at a Dutch university; **outside physics** | Post-test without the LLM, same session (about 90 min in total) | **No effect of LLM access on overall learning in either experiment.** In exploratory analyses, using the LLM for solutions widened topic coverage but lowered understanding, and using it for explanations raised understanding. The LLM widened the gap between students with low and high prior knowledge. |
| Contractor & Reyes (2026), arXiv 2607.08849 (preprint, not peer reviewed) | Randomized, proctored, in-person | 211 undergraduates (204 at one week), Middlebury College | Undergraduates, an unfamiliar topic plus an analytical essay; **outside physics** | Unaided knowledge test **immediately and one week later**, plus an unaided essay | Off-the-shelf AI access raised immediate test scores by 0.27 SD, and **the gain persisted a week later**. Essay quality improved one week later mainly among "augmentation" users (explaining concepts), while "automation" users' essay gains vanished once the AI was removed. Gains were larger in the upper GPA/SAT quartiles. |
| Fischer, Rau & Rilke (2025), IZA DP 18338, https://docs.iza.org/dp18338.pdf | Lab RCT, three arms: textbook only; AI tutor after 10 min of reading; AI tutor throughout | 334 university students | Economics textbook excerpt, 25-min study phase, TU Berlin; **outside physics** | Incentivized test without textbook or AI, same session | AI tutor access raised the test by 0.23 SD (p < 0.05), driven by unrestricted access (+0.34 SD vs control); restricted access did not differ significantly from control. **Unrestricted beat forced reading-first by 0.21 SD (marginal, p = 0.066)**; the authors attribute this to bursts of prompting once access opened. Suggestive (unadjusted subgroup) gains for low prior knowledge and strong self-regulation. IZA working paper, not peer reviewed. |
| Kumar, Rothschild, Goldstein & Hofman (2025), https://doi.org/10.1007/978-3-031-98459-4_5 | Two preregistered online experiments | 1,818 US adults (search summary) | High-school-level mathematics; **not students in a course** | New, similar test questions without assistance, same session | LLM explanations beat seeing only the correct answer, **most for those who attempted the problem first**. Explanations containing arithmetic errors fell between correct explanations and answer-only. |
| Fan et al. (2025; online 2024), https://doi.org/10.1111/bjet.13544 | Randomized, four support conditions (ChatGPT, human expert, writing analytics, none) | 117 university students | Writing task; **outside STEM** | Essay score; knowledge gain and transfer | ChatGPT improved the essay score, but **knowledge gain and transfer did not differ** between groups. The authors warn of "metacognitive laziness". |
| Stadler, Bannert & Sailer (2024), https://doi.org/10.1016/j.chb.2024.108386 | Randomized, ChatGPT-3.5 vs Google Search (abstract read) | 91 university students | Scientific inquiry task; **outside physics** | Cognitive load; quality of the task's final recommendation and justification (task output, not an unassisted learning test) | The LLM lowered cognitive load but produced lower-quality reasoning than web search. |
| Melumad & Yun (2025), https://doi.org/10.1093/pnasnexus/pgaf316 | Seven online and lab experiments | 10,462 | General-knowledge topics, adults; **not a course** | Self-reported depth of knowledge; quality of written advice | Learning from LLM syntheses gave shallower knowledge and sparser, less original advice than web links, even when the core facts were the same. |
| Darvishi et al. (2024), https://doi.org/10.1016/j.compedu.2023.104967 | Randomized controlled experiment in ten courses: four weeks of AI prompts during peer review, then four weeks in four arms (AI prompts continued; no prompts; self-monitoring checklist; checklist plus AI). The AI was rule-based and semantic-similarity feedback, **not an LLM** (abstract read) | 1,625 students, 16,007 reviews | Peer review of learning resources, university | Review quality with and without AI | "Students tended to rely on rather than learn from AI assistance." Self-monitoring checklists partly filled the gap when AI was removed but were less effective; checklist plus AI was no better than AI alone. |

### Field trials at scale

| Source | Design | N | Domain | Outcome and timing | Finding |
|---|---|---|---|---|---|
| Oreopoulos & Low (2026), EdWorkingPaper 26-1551, https://doi.org/10.26300/kner-hv33 | Cluster RCT, two years, 18 Tennessee middle schools; grades randomized within schools (53 clusters: 28 treated, 25 control). Control: business-as-usual remedial maths, often with non-AI adaptive practice software. | 2,708 ever-scheduled students; 6,902 student-term observations | Remedial middle-school mathematics; **not university** | Standardized mathematics achievement, **per term and over a school year** | Khanmigo, configured to coach rather than give answers, raised achievement by 1.3 national percentile ranks per term, **about 0.06–0.08 SD per school year** (0.14 SD implied for a full year of active use). The authors say this "resemble[s]" Khan Academy practice without AI (a comparison with other studies, not an arm here). The median student messaged the tutor on a third of practice days and in 17% of sessions with a mistake. Messages were mostly bare answers or clicks on suggested prompts. "The binding constraint appears to be engagement." Year 1: 0.02 SD (n.s.); Year 2: 0.084 SD; stacked 0.062 SD per year (p < 0.10). The authors attribute the gains mainly to structured mastery-based practice and say the design cannot isolate the tutor. |
| Henkel, Horne-Robinson, Kozhakhmetova & Lee (2024), https://doi.org/10.1007/978-3-031-64315-6_34 (arXiv 2402.09809) | Cluster-randomized by school: 11 schools, 5 treatment and 6 control | 637 at baseline, 477 analysed (241 control / 236 treatment). The arXiv listing abstract says "approximately 1,000", the paper's own abstract "approximately 500". | Grades 3–8 mathematics, Ghana, via WhatsApp; **not university** | 35-item test of grade 3–5 numeracy and algebra, baseline and endline over **8 months** | Two 30-min sessions a week during study hall, on top of regular instruction, gave d = 0.36 (0.37 in the arXiv listing abstract), p < 0.001 from a student-level t-test on growth scores that ignores clustering by school (5 vs 6 schools), so the p-value is overstated. The control had no Rori during study hall. |
| De Simone et al. (2025), https://doi.org/10.1596/1813-9450-11125 (WB Policy Research WP 11125, full text) | RCT, six-week after-school programme | 1,328 randomized among volunteers (657 treatment / 671 control); 759 analysed (422 / 337), with differential attrition (Lee bounds still positive) | English, first-year senior secondary, Nigeria; **not university** | Pen-and-paper endline; end-of-year curricular exam | 0.31 SD overall and 0.24 SD on English (primary) at the end of the programme; 0.21 SD on the third-term curricular exam. Control got no programme. The effect grew with attendance (≈0.031 SD per day) and was larger for students with higher prior scores. Microsoft Copilot (GPT-4) with teacher guidance. |
| Nie et al. (2025), https://doi.org/10.1145/3698205.3733960 (arXiv 2407.09975) | RCT of offering GPT-4 chat in a MOOC (abstract only) | 5,831 students, 146 countries | Introductory programming (Code in Place); **outside physics** | Exam participation and score, end of course | Offering GPT-4 **lowered exam participation** and other engagement on average. Adopters scored higher, but adoption is self-selected. The published title softens the preprint's "Increased" to "May Increase". |
| Wang, Ribeiro, Robinson, Loeb & Demszky (2025), EdWorkingPaper 24-1054, https://doi.org/10.26300/81nh-8262 (arXiv 2410.03017) | Preregistered RCT; the LLM advises **human tutors**, not students | 700+ tutors, 1,000 students (Nov 2025 version; arXiv v2: 900 and 1,800) | K–12 mathematics tutoring, under-served US communities | Exit-ticket pass rate per session (proximal); end-of-year NWEA MAP, the originally preregistered outcome | Students of tutors given Tutor CoPilot were 4 percentage points more likely to pass session exit tickets (62% → 66%; 9 points for students of lower-rated tutors). No significant effect on end-of-year MAP, the originally preregistered outcome. Treatment tutors prompted students to explain more and gave generic praise less. |

### Meta-analyses and their quality

| Source | Design | N | Finding | Quality note |
|---|---|---|---|---|
| Deng, Jiang, Yu, Lu & Liu (2025), https://doi.org/10.1016/j.compedu.2024.105224 | Meta-analysis of experimental studies of ChatGPT | 69 publications; 51 effect sizes for academic performance | Improves academic performance, affect and higher-order thinking propensities; reduces mental effort (g = −0.68); no effect on self-efficacy. | Publication bias detected for academic performance (Kendall's τ = 0.321, p < .001); pooled g ≈ 0.7 from 21 primary studies (51 effect sizes), per Weidlich et al.; the mental-effort estimate (g = −0.68) rests on 4 effect sizes. The authors themselves flag missing power analyses and weak post-intervention assessments. |
| Weidlich, Gašević, Drachsler & Kirschner (2025), https://doi.org/10.1111/jcal.70105 | Conceptual critique plus an audit of Deng et al.'s primary studies | Subset of Deng et al. | "Only a small minority" of audited studies described the treatment precisely, described the control's activities, and used outcomes that validly indicate durable learning. | Applies the media-versus-method confound from earlier media-comparison research to ChatGPT studies. |
| Wang & Fan (2025), https://doi.org/10.1057/s41599-025-04787-y | Meta-analysis | — | **Retracted** (retraction note https://doi.org/10.1057/s41599-026-07310-z, April 2026) over "discrepancies in the meta-analysis". | Do not cite as evidence. |
| Liu, Zuo & Lu (2025), https://doi.org/10.1111/jcal.70096 | Meta-analysis | 37 studies | g = 0.577 [0.395, 0.759] on academic achievement; larger effects in studies with 21–40 participants than in other sample-size bands. | A sample-size moderator is a possible sign of small-study effects; publication bias not examined here. |
| Wu et al. (2026), https://doi.org/10.1057/s41599-026-07019-z | Meta-analysis | 35 studies, 4,193 participants | g = 0.670 | Overlapping primary literature (ChatGPT experiments published 2022–2024). |
| Strohmaier et al. (2026), arXiv 2601.18685v5 (Sep 2026; living meta-analysis, preprint) | Bayesian multilevel meta-regression, updated every two months | 34 studies | g = 0.57 [0.36, 0.79] (CrI) for generative AI in mathematics learning; larger when AI supplemented teacher instruction and in longer interventions. | No evidence of publication bias reported. |

The pooled estimates of about 0.6 are roughly 1.5 to 10 times the effects seen in the controlled studies above that remove the AI at test (about 0.06–0.4 SD, where the low end is a per-school-year effect at scale). This matches the ITS pattern already on the map: large effects on aligned, assisted or researcher-made measures, and small ones on independent, unassisted measures.

### What the evidence says about the §5.12 design questions

**"How much value comes from the LLM versus the instructional design?"** Several studies vary the design while holding the model fixed, and the design moves the outcome:
- Bastani et al. (2025): the same GPT-4 with and without hints-only guardrails and teacher solutions. Harm vs no harm.
- Fischer et al. (2025): the same tutor with and without forced reading first. 0.21 SD in favour of unrestricted access (marginal, p = 0.066).
- Kumar et al. (2025): LLM explanations helped most after an own attempt.
- Lehmann et al. (2024) and Contractor & Reyes (2026): how students use the model is associated with the outcome (observational within the experiments). In Lehmann et al., solution-seeking lowered understanding and explanation-seeking raised it; in Contractor & Reyes, gains persisted a week later for explanation-seeking ("augmentation") users, while automation users' essay gains vanished once the AI was removed.
- Kestin et al. (2025): the authors had to move sequencing out of the prompt into the platform, and supplied solutions to prevent errors.
- Oreopoulos & Low (2026): Khan Academy with a coaching tutor gave gains similar to those predicted for Khan Academy practice without AI (a quasi-experimental benchmark, not an arm here). The authors attribute them mainly to structured practice, since students seldom used the tutor, and say the design cannot isolate its contribution.

No study found holds the pedagogical design fixed and swaps the LLM for a non-generative implementation of the same design. So how much of any effect is attributable to the model itself is unknown.

**"What should be deterministic/rule-based vs generative?"** In these studies, the parts that worked were fixed or pre-authored:
- the problem sequence and step order (Kestin et al.);
- correct step-by-step solutions supplied in the prompt (Kestin et al.; Bastani et al.), plus common student mistakes (Bastani et al.);
- a rule not to give answers (Bastani et al.; in Kestin et al. a softer rule: one step at a time, the answer only if the student demands it); structured, individually placed practice paths, which Oreopoulos & Low credit for their gains rather than the tutor dialogue.

The generative part was the dialogue around them. This matches the ITS finding that step checking needs an explicit solution model (§5.9).

## Against

- **The anchor effect is confounded and immediate.** Kestin et al. bundle AI, self-pacing, home setting and video delivery, with one lesson per condition and a same-session quiz. It is not evidence about retention or transfer, and not about generic chatbots.
- **Assisted performance is not learning.** Practice scores rise with AI while unassisted exams fall (Bastani et al. 2025). Essays improve while knowledge gain and transfer do not (Fan et al. 2025). Review quality drops when AI is withdrawn (Darvishi et al. 2024). This is §11's "learner correctness is not understanding" in AI form.
- **Nulls and small effects in the stronger designs.** Two preregistered lab experiments found no overall effect (Lehmann et al.). A two-year cluster RCT found about 0.06–0.08 SD per year (Oreopoulos & Low 2026).
- **Engagement is a binding constraint.** Offering GPT-4 reduced exam participation in a MOOC (Nie et al. 2025). Students rarely engaged a coaching tutor in substantive dialogue (Oreopoulos & Low 2026).
- **LLMs can widen gaps.** Gains concentrate among students with more prior knowledge (Lehmann et al.) or higher GPA/SAT (Contractor & Reyes 2026), and, in suggestive subgroup splits, stronger self-regulation (Fischer et al.), though Fischer et al. also found larger gains at low prior knowledge.
- **The synthesis literature is weak.** Only a small minority of audited primary studies meet basic interpretability criteria (Weidlich et al. 2025), one meta-analysis was retracted, and publication bias was detected in another (Deng et al. 2025).
- **Transfer and delay are almost absent.** One study has a one-week unaided test (Contractor & Reyes 2026, preprint). Several measure at the end of a longer intervention: a school year (Oreopoulos & Low 2026), 8 months (Henkel et al. 2024), an end-of-year curricular exam (De Simone et al. 2025, 0.21 SD), or end-of-year MAP (Tutor CoPilot, null). Fan et al. report a transfer measure (null). None tests retention after tutoring stops, and none is in university physics.

Held against §11: most positive LLM-tutoring evidence is immediate, much of it on researcher-made tests, and some of it measured with the AI still available. It does not show that LLM tutors produce transfer.

## Implications for the map

1. **§4 LLM tutoring row, evidence cell.** Replace "**Emerging / moderate**" with:
   > **Emerging / moderate**: one university-physics crossover RCT with a large immediate effect (AI bundled with self-pacing and pre-structured steps); elsewhere ≈ 0.1–0.4 SD on unassisted tests, nulls in lab RCTs, harm without guardrails; meta-analyses (g ≈ 0.6) rest on weak primary studies; no transfer evidence

   Keep the other cells.

2. **§5.12 "Current evidence signal".** Replace both paragraphs with:
   > Graded evidence (see `research/explore-llm-tutoring.md`):
   > - **University physics:** one crossover RCT (194 eligible students, randomized by peer-instruction group; 142 AI vs 174 in-class post-test observations) found higher immediate post-test scores than in-class active learning: a standardized regression coefficient of 0.63, and 0.73–1.3 SD from a quantile regression that corrects for the ceiling. The median time on task was 49 min, against an assumed 60 min in class (Kestin et al. 2025). The AI condition also changed pacing, setting and delivery, used pre-written solutions and a platform that stepped students through each part, and was tested in the same session.
   > - **Unassisted outcomes elsewhere:** 0.23–0.27 SD in university lab RCTs (Fischer et al. 2025; Contractor & Reyes 2026, preprint, gain held at one week); no overall effect in two preregistered lab RCTs (Lehmann et al. 2024); about 0.06–0.08 SD per school year for a coaching tutor at scale (Oreopoulos & Low 2026); 0.24 SD in English (0.31 SD overall) in an individually randomized after-school trial with differential attrition (De Simone et al. 2025) and d = 0.36 in an 11-school trial analysed without clustering (Henkel et al. 2024), both with added learning time.
   > - **Harm without guardrails:** an unconstrained GPT-4 raised practice scores but lowered the unassisted exam (Bastani et al. 2025); ChatGPT raised essay scores without knowledge gain or transfer (Fan et al. 2025).
   > - **Use pattern matters:** asking for explanations helps; asking for solutions lowered understanding in one study (Lehmann et al. 2024) and left gains that did not persist in another (Contractor & Reyes 2026); explanations help most after an own attempt (Kumar et al. 2025).
   > - **Syntheses are weak:** pooled g ≈ 0.6 (Liu et al. 2025; Wu et al. 2026; Strohmaier et al. 2026, preprint), but in an audit of primary studies from one such meta-analysis (Deng et al. 2025), only a small minority described the treatment precisely, described the control's activities and used a valid learning outcome (Weidlich et al. 2025); one meta-analysis has been retracted (Wang & Fan 2025).
   > - **Transfer and delay:** one one-week unaided test (preprint) and a few end-of-intervention outcomes; the one transfer measure was null; no university-physics study.

3. **§5.12 "Design implication".** Append after the six questions:
   > In the studies that worked, the sequence, the correct solutions, the common mistakes and the rule against giving answers were largely fixed in advance (Bastani et al. 2025; in Kestin et al. 2025 the sequence and solutions, with a softer answer rule), and the LLM generated the dialogue around them. Measure learning with the AI removed; practice or assisted performance can rise while learning falls.

4. **§5.12 "Questions to research next".** Replace "How much value comes from the LLM itself versus the instructional design wrapped around it?" with:
   > With the pedagogical design held fixed, does an LLM tutor beat a non-generative implementation of the same design (static or rule-based hints) on an unassisted, delayed test?

   Add:
   > How can a tutor get students to use it for explanation rather than solutions, given low engagement at scale (Oreopoulos & Low 2026)?

5. **§9 Phase 5.** After the Knowledge Tracing line ("judge it by a learning experiment against a simple mastery rule …"), add:
   > - if an LLM delivers the tutoring, compare it with the same design delivered without generation (static or rule-based), on an unassisted, delayed test, and report uptake; LLM effects shrink or vanish once the AI is removed at test, pacing is matched or students must choose to use it (Bastani et al. 2025; Lehmann et al. 2024; Oreopoulos & Low 2026).

   Stage B needs no change. Its static delivery is the design-held-fixed baseline this evidence asks for, and its test is unassisted and delayed.

6. **§11.** Add:
   > - Do **not** measure learning while the AI is still available; assisted or practice performance can rise while unassisted performance falls.

7. **§12 note 5.** Append:
   > The large result (Kestin et al. 2025) is immediate and bundles the AI with self-pacing and pre-structured steps; at scale and with the AI removed at test, effects are small or null, and syntheses of ChatGPT studies rest on weak designs.

8. **§14.** Add:
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

   Kestin et al. (2025) and Bastani et al. (2025) are already listed. The retracted Wang & Fan (2025) is deliberately not added.

## Open questions

These are only the ones that would change the verdict:

- Is there a university-physics RCT of an LLM tutor with a **delayed or transfer** outcome measured without the AI? A positive result would lift the "no transfer evidence" qualifier; a null would narrow the rating to immediate performance.
- Does any study hold the pedagogical design fixed and compare an LLM with a non-generative implementation of it? This answers the §5.12 "LLM vs design" question directly, and decides whether Phase 5 needs a generative tutor at all.
- Does Kestin et al.'s effect replicate when pacing and setting are matched (both arms self-paced at home, or both in class)?
