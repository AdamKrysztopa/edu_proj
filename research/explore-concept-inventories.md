# Explore: Concept Inventories / diagnostic instruments

**Question:** Which physics concept inventories are validated for individual diagnosis rather than cohort or course evaluation, does a distractor choice reliably indicate a stable misconception in one student, and are the map's two current uses (seeding the §5.4 PCK layer, and EMCS items in the Phase 2 Stage B) defensible?

**Verdict: no change to priority (P1) or rating ("High for well-validated instruments"); the rating is scoped to cohort-level use.** The major physics inventories have strong validity evidence for class-level evaluation: reliable total scores, replicated factor structures, large multi-institution datasets. The evidence does not support using them to diagnose an individual student. About a third of FCI responses (31%, pooled over 100 college students) changed on a retest within a week. Students hold mixed, context-dependent models. Some items are biased by gender. Published best-practice guidance says the instruments assess instruction, not individual mastery (Madsen, McKagan & Sayre 2017), even though the FCI's developers also proposed diagnostic and college-placement uses (Hestenes et al. 1992). Both current uses are cohort-level, so both are defensible. The PCK layer should add coded open-ended answers, because distractors miss student ideas. Stage B should drop the three EMCS items flagged in the largest psychometric analysis.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 Concept Inventories row (P1, "High for well-validated instruments", STEM fit Very high, humanities Low–medium, AI readiness Very high) and the §5.6 card, whose second research question is exactly "Which are validated for individual diagnosis vs cohort/course evaluation?". Since `explore-pedagogical-content-knowledge.md`, §5.4 also seeds the PCK layer from "concept-inventory distractors, coded exam errors". `experiment-ai-assisted-cta-physics.md` uses selected EMCS items as an exploratory arm-level secondary measure in Stage B. The branch serves §9 Phase 3 (diagnosis methods) and Phase 2 Stage B, and §10 RQ3.

Search: the OpenAlex REST API returned HTTP 429 (daily limit) throughout, and the `openalex` MCP server was not loaded. Search used the Crossref, Semantic Scholar and ERIC APIs, PhysPort, arXiv and WebSearch. Full text was read for Lasry et al. (2011), Rebello & Zollman (2004), Singh & Rosengrant (2003, arXiv), Madsen, McKagan & Sayre (2017, arXiv), Bao & Redish (2006) and Lichtenberger et al. (2024). Everything else comes from abstracts. Huffman & Heller (1995) and Heller & Huffman (1995) are closed access and come from ERIC descriptions and later papers' summaries; Hestenes & Halloun (1995) was read from an archived copy. The Zotero local API holds one relevant item, "Force concept inventory" (Hestenes et al. 1992), with no notes.

## Evidence

### What the instruments were built and validated for

| Source | Design | N | Domain | Validity shown | Finding |
|---|---|---|---|---|---|
| Hestenes, Wells & Swackhamer (1992), https://doi.org/10.1119/1.2343497 | Instrument development | Not in abstract | High-school and university mechanics | Content design; comparison with the Mechanics Baseline | FCI: rationale, design, validation and uses of an instrument that assesses students' beliefs about force, with distractors built from common-sense conceptions (ERIC description). |
| Madsen, McKagan & Sayre (2017), https://doi.org/10.1119/1.5011826 | Guidance built from interviews with 24 physics faculty plus the literature | 24 faculty | Physics and astronomy inventories, university | — | Inventories "are meant to assess the effectiveness of instruction and not individual students' concept mastery". The authors advise against high-stakes use and warn that individual scores carry "systematic biases that disadvantage certain students". |
| Henderson (2002), https://doi.org/10.1119/1.1534822 (findings via Madsen et al. 2017) | Comparison of graded vs ungraded administration | 2,178 | University mechanics | Administration effects | At most 2.8% of students failed to take the ungraded FCI seriously. Some students with very low pretest scores still earned an A, so the FCI does not work as a placement test. |
| Hake (1998), https://doi.org/10.1119/1.18809 | Survey of pre/post data, not controlled | 62 courses, 6,542 students | High school, college, university mechanics | Class-level sensitivity to instruction | Interactive-engagement courses averaged a normalized gain of 0.48, traditional courses 0.23. This is the canonical class-level use. |
| Singh & Rosengrant (2003), https://doi.org/10.1119/1.1571832 | Instrument development: 25 items, 34 one-hour interviews, item analysis | >3,000 students in about 30 courses | Intro university physics (energy and momentum) | Content validity from interviews; internal consistency | EMCS. α slightly above 0.75 for calculus-based classes (1,170 students) and 0.68 for algebra-based classes (186 students). |
| Ding, Chabay, Sherwood & Beichner (2006), https://doi.org/10.1103/physrevstper.2.010105 | Classical item and test statistics | Not in abstract | Calculus-based intro E&M, university | Reliability, discrimination | BEMA judged a reliable assessment tool. |
| Maloney et al. (2001), https://doi.org/10.1119/1.1371296 | Instrument development | >5,000 students, 30 institutions | Intro E&M, university | Content | CSEM. It reports student difficulties across E&M topics. |
| Beichner (1994), https://doi.org/10.1119/1.17449 | Instrument development | 895 high-school and college students | Kinematics graphs | Content; diagnostic design | TUG-K. It proposes a model for building multiple-choice tests usable as diagnostic tools. |
| Thornton & Sokoloff (1998), https://doi.org/10.1119/1.18863 | Instrument plus curriculum evaluation | Not extracted | Force and motion, university | Class-level sensitivity to curricula | FMCE, introduced alongside an evaluation of active-learning curricula. The claims were not extracted. |

Each instrument's reported validity evidence is at class or course level, even where the developers proposed diagnostic use (the FCI "as a diagnostic tool … to identify and classify misconceptions"). None reports individual-level classification accuracy, such as agreement between a distractor-based diagnosis and an interview-based diagnosis of the same student.

### Is the total score reliable and structurally valid?

| Source | Design | N | Domain | Validity shown | Finding |
|---|---|---|---|---|---|
| Huffman & Heller (1995), https://doi.org/10.1119/1.2344171; replies Hestenes & Halloun (1995), https://doi.org/10.1119/1.2344278, and Heller & Huffman (1995), https://doi.org/10.1119/1.2344279 | Exploratory factor analysis, then published exchange | Not verified | High school and university | Structure | Huffman & Heller questioned whether FCI responses show the six intended dimensions of the Newtonian force concept (as quoted in Hestenes & Halloun 1995). Hestenes & Halloun defended the total score as a measure of basic Newtonian concepts and of instructional effectiveness. Heller & Huffman urged caution in interpreting scores (ERIC descriptions). |
| Eaton & Willoughby (2018), https://doi.org/10.1103/physrevphyseducres.14.010124 | Confirmatory factor analysis | 20,822 post-instruction responses | University | Structure, replication | Three factor models fit the full sample. On smaller samples the Scott et al. (2012) and Eaton & Willoughby models stayed stable and the Hestenes et al. model did not. The FCI can be scored on factors that are not unique to one class. |
| Stewart et al. (2018), https://doi.org/10.1103/physrevphyseducres.14.010137 | Multidimensional IRT | 4,716 post-tests | University | Structure | A 9-factor solution, much of it produced by problem blocks and pairs of similar items. With those items removed, the 6 factors "had little relation" to the structure of Newtonian mechanics. A constrained model built from expert solutions was needed to recover interpretable concepts. |
| Wang & Bao (2010), https://doi.org/10.1119/1.3443565 | IRT | Not in abstract | University | Item parameters | IRT gives difficulty, discrimination and guessing for each FCI item and a scaled proficiency score beyond classical statistics. |
| Lasry et al. (2011), https://doi.org/10.1119/1.3602073 | Test–retest within one week, no mechanics review in between | 100 students (3 cohorts, same instructor) | Start of an E&M course, college | Internal consistency; test–retest | KR-20 was high and total-score test–retest r = 0.89. But **31% of individual responses changed** between test and retest, neither consistently nor completely at random. The authors conclude that the total score is highly reliable while individual responses are not. The paper cites KR-20 > 0.80 as the usual threshold for comparing individuals and > 0.70 for comparing groups. |
| Traxler et al. (2018), https://doi.org/10.1103/physrevphyseducres.14.010103 | CTT, IRT and differential item functioning | 5,391 pre, 5,769 post (3 samples) | University | Fairness across genders | Six items appeared substantially unfair to women and two favoured women. Removing all the unfair items halved the gender gap in the main sample. The authors recommend reporting a reduced-instrument score and **not assigning credit to students using the biased items**. |
| Nissen et al. (2018), https://doi.org/10.1103/physrevphyseducres.14.010115 | Secondary analysis of the LASSO database | 4,551 students, 89 courses, 17 institutions | Physics, chemistry, biology and maths inventories, university | Choice of gain metric | Normalized gain and Cohen's d led to different conclusions about learning and equity. Normalized gain is biased in favour of groups with high pretest scores. |

So the FCI total score is reliable and is structurally usable at scale. Item-level answers are not stable for one student, and part of the item set is not fair across genders. Both limits bear on individual diagnosis and neither bears much on class-level evaluation.

### Does a distractor choice mean a stable misconception in one student?

| Source | Design | N | Domain | Validity shown | Finding |
|---|---|---|---|---|---|
| Bao & Redish (2006), https://doi.org/10.1103/physrevstper.2.010103 | Method paper (model analysis) with example data | — | University mechanics | Theory of response patterns | Students "can each have multiple models and use these models inconsistently", so they are in **mixed model states** that shift with context. Scoring only right or wrong discards this; model analysis estimates it as probabilities, summarised as a class model density matrix. |
| Scott & Schumayer (2018), https://doi.org/10.1103/physrevphyseducres.14.010106 | Network analysis of distractor co-selection | ~1,500 students a year over two years, one algebra-based course | FCI data | Structure of wrong answers | Distractors form groupings, the two largest associated with an "impetus" worldview, linked by central and connector items. The authors take as background that non-Newtonian worldviews are "coherent and robust"; their own data are distractor co-selection in one algebra-based course. This is a population-level pattern of co-selection. |
| Segado, Adair, Stewart & Pritchard (2026), arXiv 2606.08986 (preprint, not peer reviewed) | Multidimensional IRT in which distractors have their own directions | ~34,000 FCI administrations | Mechanics | Structure of wrong answers | 22 robust, partly overlapping misconception dimensions, two of them apparently new. Remediation patterns vary: some misconceptions persist unchanged after instruction. The authors propose per-student and per-class "misconception scores" and offer them for **class-level** formative assessment. |
| Rebello & Zollman (2004), https://doi.org/10.1119/1.1629091 | Four FCI items given as multiple-choice vs equivalent open-ended versions, counterbalanced across two questionnaire forms; then revised multiple choice | 238 algebra-based students, then 234 | University mechanics | Coverage of distractors | The percentage correct agreed across formats. But "a significant percentage" of open-ended answers fell into categories **not among the FCI choices**, and when those were added as distractors a significant percentage of students chose them. |
| Savage & Rebello (2025), https://doi.org/10.1119/perc.2025.pr.Savage (conference proceedings) | GPT-4o classification of written explanations, validated against human graders | 1,131 | 3 EMCS questions, university | Agreement with humans on correct/incorrect; coverage | GPT-4o's correct/incorrect judgments differed from human graders' by 0–3% in overall percentage correct (mean κ = 0.77 on a 20% subsample). Its emergent categories of incorrect explanations **differed from the multiple-choice distractors**; they were checked for stability across runs, not against human coders. |

Distractor data are strong evidence of which wrong ideas are common in a population. They are weak evidence of what one student believes: a single answer flips often on retest, students hold mixed models, and the distractor set misses ideas that open-ended answers reveal. The only LLM study found reports that GPT-4o matched human graders in judging open-ended answers correct or incorrect on three items; its categories of wrong ideas were not checked against human coders. It does not compare the diagnostic accuracy of dialogue against multiple choice for individual students.

### The EMCS specifically (Stage B secondary measure)

| Source | Design | N | Domain | Validity shown | Finding |
|---|---|---|---|---|---|
| Wu, Guthrie, Scanlon & Li (2023), https://doi.org/10.1119/perc.2023.pr.Wu | IRT dimensionality (bootstrap parallel analysis) | 253 pre, 201 post | University intro mechanics | Structure | Not unidimensional; a 2- or 3-dimensional model fits best. Grouping items by their designated concepts did not improve fit: "students may interpret the items differently than intended". |
| Wu, Li & Rebello (2025), https://doi.org/10.1103/kvph-l899 | CTT, IRT and EFA | 6,343 pre / 5,996 post administrations (abstract: "over 10 000 students"), 5 semesters, one US university | University intro mechanics | Item quality; structure | Several items showed weak discrimination, low reliability or guessing. A four-factor model **excluding Q16, Q22 and Q23** (item–total correlations below 0.20; removing them raised α) was the most interpretable. The design-intent two-factor model (energy vs momentum) was robust across model variations. |
| Brundage, Maries & Singh (2023), https://doi.org/10.1103/PhysRevPhysEducRes.19.020132 | Cross-sectional pre/post | 352 pre / 336 post introductory; 68 pre / 42 post upper-level; one university | Introductory and upper-level undergraduates | Sensitivity across levels | On every item that fewer than 50% of introductory students answered correctly after traditional instruction, fewer than two thirds of upper-level students answered correctly; upper-level students were below two thirds on 13 of 25 items. |

The experiment note's open question, "does an item-level validation of EMCS exist?", now has a partial answer. There is item-level psychometric evidence from one large university, and it flags three items. There is still no validation of any item subset, and the full test's α (0.68–0.76 across Singh & Rosengrant 2003 and Wu, Li & Rebello 2025) is below the 0.80 threshold for comparing individuals. The arm-level, exploratory use the experiment note already specifies is the defensible one.

### Does inventory-based diagnosis feeding an instructional response improve learning?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Lichtenberger, Hofer, Stern & Vaterlaus (2024), https://doi.org/10.1007/s11092-024-09445-6 | Cluster-randomized trial, 3 arms (formative assessment / same concept questions without formative assessment / traditional) | 29 teachers, 604 students analysed (561 at 3-month follow-up) | Swiss upper-secondary kinematics; **not university** | Kinematics Concept Test (49 items, α 0.88–0.92) immediately and **3 months later**; quantitative problem solving | Formative assessment (clicker concept questions, a diagnostic multiple-choice test with distractors from interviews, a monitoring tool and a reflective lesson targeting the diagnosed deficits) beat the same concept questions without it (d = 0.37 post, 0.39 at 3 months) and traditional teaching (d = 0.68, 0.62). **Concept questions alone did not beat traditional teaching.** No cost to problem solving. |
| Weijers et al. (2025), arXiv 2504.00408 (preprint, not peer reviewed) | RCT, one lab session | 165 enrolled, 141 analysed; one North American R1 university | Intro mechanics | Standard FCI post-test in the same session (students had taken it ~2 months earlier; a modified FCI served as pretest) | A GPT-4o "peer", prompted with each student's modified-FCI errors, raised post-test scores by 10.5 percentage points over a control that chatted about physics history. The control is not an equal-time physics activity, so this does not show that the targeting itself helped. |

Diagnosis without feedback did not help significantly: the frequent-testing arm took the same concept questions and diagnostic test without feedback and did not beat traditional teaching (p = 0.084 post, 0.323 at 3 months). The gain came from a package of teacher training, peer-discussion clicker sessions, a monitoring tool and a reflective lesson built on the diagnosis. Neither study isolates targeting from time on physics, and neither measures transfer.

## Against

- **Individual answers are unstable.** 31% of FCI answers changed on retest within a week, 13 points of them from one wrong answer to another (Lasry et al. 2011, one college, N = 100). A Comment (Wallace 2012, https://doi.org/10.1119/1.3660663) and the authors' Reply (https://doi.org/10.1119/1.3660664) exist; both are closed access and were not read. A misconception label from one item is not a stable learner-state fact.
- **Students hold mixed models** (Bao & Redish 2006). The competing view, that the underlying worldviews are "coherent and robust" (Scott & Schumayer 2018), rests on population-level co-selection of distractors, not on the stability of individual students. This is the knowledge-in-pieces vs coherent-theory debate, which belongs to the Conceptual Change branch. It is not settled here.
- **Structure is contested and partly an artefact.** Much of the FCI factor structure comes from item blocks and similar item pairs (Stewart et al. 2018). The EMCS does not split cleanly by its intended concepts (Wu et al. 2023).
- **Counterpoint from the developers.** Hestenes & Halloun (1995) wrote that "a negative response is nearly always a reliable indicator of some deficiency in the student's understanding", while also saying their categories do not "describe conceptual structures of individual students".
- **Fairness.** Eight FCI items function differently by gender (Traxler et al. 2018). Individual-level decisions based on them would be biased.
- **Distractors miss student ideas** (Rebello & Zollman 2004; Savage & Rebello 2025). An inventory-only misconception list is incomplete by construction.
- **The metric affects the conclusion.** Normalized gain favours high-pretest groups (Nissen et al. 2018). Stage B already uses effect sizes, not normalized gain.
- **Instructional utility is thin.** The one cluster RCT is upper-secondary and measured the developers' own concept test. The one university RCT is a preprint with a no-physics control. No study measures transfer. No study compares LLM dialogue with multiple choice on the accuracy of diagnosing individual students.

Held against §11: the class-level validity evidence is strong. But "a student chose distractor C" is correctness-style evidence from one item, and it does not show that the student holds a stable model.

## Implications for the map

1. **§4 Concept Inventories row, evidence cell.** Replace "**High for well-validated instruments**" with:
   > **High for cohort/course evaluation** with well-validated instruments; weak for individual diagnosis (item answers unstable on retest, mixed models, some gender-biased items)

   Keep the other cells.

2. **§5.6, new subsection "Evidence / limitations"** after "Domain fit":
   > Graded evidence (see `research/explore-concept-inventories.md`):
   > - **Built and validated for class-level use.** FCI, FMCE, CSEM, BEMA, TUG-K and EMCS have class-level validity evidence, and published best-practice guidance says they assess instruction, not individual mastery (Madsen, McKagan & Sayre 2017). The FCI total score is reliable (test–retest r = 0.89) and its factor structure replicates at scale (Eaton & Willoughby 2018).
   > - **Weak for individual diagnosis.** 31% of FCI responses changed on a retest within a week, although total scores correlated at r = 0.89 (Lasry et al. 2011; one Canadian two-year college, N = 100). Students hold mixed, context-dependent models (Bao & Redish 2006). Six FCI items are biased against women and two in their favour (Traxler et al. 2018). EMCS α is 0.68–0.76 (Singh & Rosengrant 2003; Wu, Li & Rebello 2025), below the 0.80 usually cited for comparing individuals (Lasry et al. 2011).
   > - **Distractors miss student ideas.** Open-ended versions reveal categories that are not among the choices (Rebello & Zollman 2004; Savage & Rebello 2025).
   > - **Diagnosis helps only when it drives a response.** In a cluster RCT, concept questions and a diagnostic test without feedback did not significantly beat traditional teaching, while a formative-assessment package built on the diagnosis did (d ≈ 0.4 at 3 months; Lichtenberger et al. 2024, upper-secondary kinematics). No study measures transfer.

3. **§5.6 "AI opportunity".** Replace the last list item "external validation for an AI's inferred learner state." with:
   > external validation for an AI's inferred learner state **at class level**, or for one student only when several items probe the same concept (single item answers are unstable on retest).

   Append after the "Do **not** assume…" paragraph:
   > Add coded open-ended answers to the distractor labels, because distractors miss some student ideas. An LLM can grade open-ended answers as correct or incorrect close to human graders on a few items (Savage & Rebello 2025). Its misconception categories have not been validated against human coding, and this is not evidence that it can diagnose individual students.

4. **§5.6 "Questions to research next".** Replace "Which are validated for individual diagnosis vs cohort/course evaluation?" with:
   > How many items per concept are needed before a misconception score is stable for one student on retest?

   Add:
   > Does diagnosis-targeted instruction beat untargeted instruction of equal time, and does it improve transfer?

5. **§5.4 "AI opportunity".** In the sentence beginning "Seed the misconception, misleading-cue and diagnostic-question entries from student response data", replace "(concept-inventory distractors, coded exam errors)" with:
   > (cohort-level concept-inventory distractor frequencies, plus coded open-ended answers and exam errors, since distractors miss some student ideas)

6. **§9 Phase 3.** After "Measure not only classification accuracy but **instructional utility**: does the diagnosis lead to a better next intervention?", add:
   > Also measure each method's test–retest stability for the same student; 31% of FCI item responses changed on a retest within a week, 13 points of them from one wrong answer to another (Lasry et al. 2011).

   This is the only §9 edit. It is forced because Phase 3 scores classification accuracy, and a label that flips on retest cannot be scored against one administration. Stage B in §9 does not mention EMCS, so no §9 edit follows from the EMCS findings.

7. **`research/experiment-ai-assisted-cta-physics.md`** (not the map). In the EMCS secondary-measure bullet, add "excluding Q16, Q22 and Q23, which had item–total correlations below 0.20 and lowered α in the largest analysis (Wu, Li & Rebello 2025)". Answer the open question "Does an item-level validation of EMCS exist?" with: partial; there is item-level evidence from one university and no validated subsets, so EMCS stays exploratory.

8. **§11.** Replace "Do **not** use concept inventories outside their validated purpose without checking validity." with:
   > Do **not** use concept inventories outside their validated purpose without checking validity; most are validated for class-level evaluation, not for diagnosing or grading individual students.

9. **§14.** Add:
   - Lasry et al. (2011): https://doi.org/10.1119/1.3602073
   - Traxler et al. (2018): https://doi.org/10.1103/physrevphyseducres.14.010103
   - Eaton & Willoughby (2018): https://doi.org/10.1103/physrevphyseducres.14.010124
   - Stewart et al. (2018): https://doi.org/10.1103/physrevphyseducres.14.010137
   - Bao & Redish (2006): https://doi.org/10.1103/physrevstper.2.010103
   - Rebello & Zollman (2004): https://doi.org/10.1119/1.1629091
   - Madsen, McKagan & Sayre (2017): https://doi.org/10.1119/1.5011826
   - Nissen et al. (2018): https://doi.org/10.1103/physrevphyseducres.14.010115
   - Hake (1998): https://doi.org/10.1119/1.18809
   - Wu, Li & Rebello (2025): https://doi.org/10.1103/kvph-l899
   - Savage & Rebello (2025): https://doi.org/10.1119/perc.2025.pr.Savage
   - Lichtenberger et al. (2024): https://doi.org/10.1007/s11092-024-09445-6

   Hestenes, Wells & Swackhamer (1992) and Singh & Rosengrant (2003) are already listed.

## Open questions

These are only the ones that would change the verdict:

- Is there a study measuring how accurately a physics inventory classifies an individual student's misconception against an interview or repeated-measures standard? A positive result would lift the "weak for individual diagnosis" qualifier for that instrument.
- Is there a controlled university-physics study in which inventory-based diagnosis feeds targeted instruction, compared against untargeted instruction of equal time, with a transfer outcome? A positive result would give the §5.4 and §5.6 diagnostic uses causal support. None was found.
- Does an LLM coding open-ended answers identify an individual's misconception more stably on retest than multiple choice does? This is the Phase 3 comparison, and no study was found.
