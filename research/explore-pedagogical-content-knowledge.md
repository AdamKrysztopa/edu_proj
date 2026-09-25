# Explore: Pedagogical Content Knowledge (PCK)

**Question:** Does measured teacher PCK, and in particular knowledge of student difficulties held separately from content knowledge, predict student learning, and does that justify a separate "PCK layer" in the §6 architecture elicited from experienced teachers rather than domain experts?

**Verdict: no change to priority (P0) or rating (Moderate–high); the rating is scoped, and the PCK layer's source changes.** Correlational studies link PCK to achievement gains in school mathematics and, less consistently, school physics. No experiment isolates PCK; the one meta-analysis of correlations finds a positive but model-dependent PCK–achievement association (Fukaya et al. 2025), and the latest systematic review calls the link inconclusive (Park & Chan 2025). There is nothing at university level with a learning outcome, nor any transfer outcome. The finding that matters most for the system: university physics TAs, and instructors who score no better, miss many of the common student difficulties that concept-inventory data reveal. The misconception part of the PCK layer should therefore be seeded from student response data, not elicited from teachers or experts.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 PCK row (P0, "Moderate–high", STEM fit High, humanities High, AI readiness High), §5.4 card, §6 "EXPERT ELICITATION: DtD + CTA + PCK" box. Serves §9 Phase 1 (taxonomy of hidden knowledge) and Phase 3, and §10 RQ3 and RQ7.

Search: the OpenAlex REST API was used for the first queries, then refused further requests (HTTP 429, the shared daily budget for this IP was exhausted). The rest used the Crossref API, the ERIC API, the Semantic Scholar API and WebSearch. The `openalex` MCP server was not loaded. Zotero, searched through its local API, holds Shulman (1986), added today with no notes, and nothing else on PCK or misconceptions.

## Evidence

### Does teacher PCK predict student learning?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Baumert et al. (2010), https://doi.org/10.3102/0002831209345157 | Longitudinal, correlational (multilevel SEM) | Representative sample of Grade 10 classes and their teachers (COACTIV) | School mathematics, Germany; **outside physics, not university** | Achievement gain over one school year | PCK was empirically distinguishable from content knowledge (CK) and had a substantial positive effect on learning gains, mediated by cognitive activation and individual learning support |
| Kunter et al. (2013), https://doi.org/10.1037/a0032583 | Longitudinal, correlational (two-level SEM), same programme | 194 classes | School mathematics, Germany; **outside physics, not university** | Achievement and motivation over one year | PCK, enthusiasm and self-regulation predicted instructional quality, which predicted student outcomes. General academic ability did not. |
| Hill, Rowan & Ball (2005), https://doi.org/10.3102/00028312042002371 | Correlational (linear mixed models) | US Grades 1 and 3 | School mathematics; **outside physics, not university** | Achievement gain over a year | Mathematical knowledge for teaching predicted gains after covariates. The measure is mainly specialised content knowledge, not knowledge of students. |
| Sadler et al. (2013), https://doi.org/10.3102/0002831213477680 | Correlational, teachers and students took the same items across the year | 181 teachers, 9,556 students | Middle-school physical science (**physics-adjacent, not university**) | Gains on the same items (immediate, not transfer) | On items with a popular wrong answer, students of teachers who could name that wrong answer gained much more than students of teachers who only knew the right answer. On items without a strong misconception, teacher subject knowledge alone predicted gains. |
| Keller et al. (2017), https://doi.org/10.1002/tea.21378 | Correlational (multilevel SEM), tests, questionnaires, video | 77 physics teachers and their classes | School physics, Germany and Switzerland; **not university** | Achievement and interest (immediate) | PCK predicted achievement, mediated by observer-rated cognitive activation. PCK did not predict interest. |
| Cauet et al. (2015), https://doi.org/10.24452/sjer.37.3.4963 | Correlational (multilevel) | 23 physics teachers | School physics, Grades 8–9 mechanics, Germany; **not university** | Learning gains over a mechanics sequence | **Null.** Neither CK nor PCK correlated with cognitive activation or explained variance in learning gains. The authors question the validity of the PCK test. |
| Liepertz & Borowski (2019), https://doi.org/10.1080/09500693.2018.1478165 | Correlational, tests plus one videotaped lesson per teacher | 35 physics teachers (ProwiN; includes the 23 teachers of Cauet et al. 2015) | School physics, Germany; **not university** | Student test outcomes | Teacher knowledge did not predict how interconnected the lesson content was. Interconnectedness and "certain aspects" of knowledge predicted student outcomes. |
| Wang et al. (2024), https://doi.org/10.1103/physrevphyseducres.20.020122 | Correlational, pre-post, two sections over two semesters | 92 students (mechanics, fall) and 84 (E&M, spring), about 27 in both; one university | **University** intro mechanics and E&M | Conceptual gain, critical thinking (immediate) | Learning assistants' PCK in questioning had a "significant but slight" effect on conceptual gain and little on critical thinking |
| She et al. (2025), https://doi.org/10.3102/00028312241278627 | Correlational (two-level HLM), text-based and video-based PCK tests | Not extracted | School science; **not university** | Student achievement | PCK was significantly and positively associated with achievement on both tests; the video-based test predicted better |

### Syntheses

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Park & Chan (2025), https://doi.org/10.3102/00346543251394404 | Systematic review | 217 empirical studies, 1986–2023 | Science teachers | Mixed | PCK is strongly connected with CK and teaching practice, but relationships with student outcomes are **inconclusive**. Divergent conceptualisation, operationalisation and measurement hinder accumulation. |
| Fukaya et al. (2025), https://doi.org/10.1016/j.tate.2024.104881 | Systematic review and meta-analysis of correlations | 298 effect sizes from 56 papers | Primary and secondary mathematics and science | Associations | PCK was positively associated with CK and teacher efficacy, not with gender. For instructional quality and student achievement, results differed by model; the multilevel (three-level) analyses gave positive correlations (abstract). Pooled r not extracted: the article is open access but could not be retrieved by script. |
| Gonzalez, Lynch & Hill (2022), https://doi.org/10.26300/d9kc-4264; published as Lynch et al. (2025), https://doi.org/10.1177/23328584251335302 | Meta-analysis of experimental studies of STEM PD and curriculum interventions | 37 studies (working paper); 46 (published) | PreK–12 mathematics and science | Teacher knowledge, instruction, student achievement | Interventions improved teacher outcomes (+0.56 SD working paper; +0.52 SD published). In the working paper, impacts on instruction predicted impacts on achievement (0.27 SD per SD), and impacts on teacher knowledge did not reach significance. Only 9 studies reported PCK separately, too few to model PCK on its own. |
| Depaepe, Verschaffel & Kelchtermans (2013), https://doi.org/10.1016/j.tate.2013.03.001 | Systematic review | Not extracted | Mathematics education | Conceptual | PCK is conceptualised differently across studies. Large-scale studies measure it with paper-and-pencil tests, small-scale studies with multiple qualitative sources. |
| Sarkar et al. (2024), https://doi.org/10.1016/j.tate.2024.104608 | Systematic scoping review | Not extracted | **Higher education**, all disciplines | Conceptual | PCK research in higher education is disparate across countries and disciplines, with significant variation in which components are included, making comparisons hard. No learning-outcome synthesis. |

### Do content experts know what students get wrong?

This is the question that decides whether a separate PCK layer is needed.

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Maries & Singh (2016), https://doi.org/10.1103/physrevphyseducres.12.010131 | Descriptive: participants predicted the most common wrong FCI answer per item, scored against pre/post data from ~900 intro students; think-aloud interviews | 25 TAs, 30 physics instructors, 24 simulated random guessers | **University** intro mechanics | Knowledge of student difficulties, not learning | TAs and instructors beat random guessing (65% and 68% of the maximum score vs 40%) but missed many common difficulties that persist after traditional instruction. Instructors did not differ significantly from TAs. |
| Maries & Singh (2013), https://doi.org/10.1103/physrevstper.9.020120 | Same task on the TUG-K | First-year physics graduate students in a TA course | **University** kinematics graphs | As above | Better than chance, but many common difficulties were missed; performance was context-dependent |
| Karim, Maries & Singh (2018), https://doi.org/10.1103/physrevphyseducres.14.010117 | Same task on the CSEM | TAs | **University** E&M | As above | TAs struggled to identify many common difficulties that persist after traditional instruction |
| Nathan & Petrosino (2003), https://doi.org/10.3102/00028312040004905 | Judgement task vs actual student performance | 48 preservice secondary teachers | Algebra; **outside physics** | Accuracy of difficulty judgements | "Expert blind spot": more advanced mathematics education predicted ranking symbolic equations as easier than word problems, the reverse of students' actual performance |

Taken with Sadler et al. (2013), these point one way. Knowing students' common wrong answers is distinct from knowing the subject; it predicts gains on misconception-laden items; and physics content experts, including experienced instructors, hold only part of it. The part they lack is visible in student response data.

### Construct and models

- Shulman (1986), https://doi.org/10.3102/0013189x015002004, is the canonical definition: representations, analogies and examples, plus knowledge of what makes topics easy or hard and of learners' preconceptions. Theory.
- Carlson et al. (2019), https://doi.org/10.1007/978-981-13-5898-2_2: the Refined Consensus Model separates collective PCK (held by a professional community), personal PCK and enacted PCK. Theory. A PCK layer in the system is collective PCK, the kind that can be written down and shared, so the personal-to-enacted gap the model describes does not transfer directly to it.
- Kulgemeyer & Riese (2018), https://doi.org/10.1002/tea.21457: 109 preservice physics teachers explained phenomena to trained, standardised high-school "students". PCK mediated the effect of CK on explaining performance. It measures teaching performance, not student learning.
- Kind (2009), https://doi.org/10.1080/03057260903142285, and Kind & Chan (2019), https://doi.org/10.1080/09500693.2019.1584931: reviews of competing PCK models and of how PCK relates to CK and pedagogical knowledge. Theory.

## Against

- **No experiment isolates PCK.** Every positive study is correlational. The experimental meta-analysis could not separate PCK (k = 9), and in its working-paper version teacher-knowledge impacts did not significantly predict achievement impacts (Gonzalez, Lynch & Hill 2022).
- **Inconclusive link to student outcomes.** The largest synthesis, 217 studies, calls the relationships with student outcomes inconclusive and the measurement divergent (Park & Chan 2025).
- **Physics replication is mixed.** Keller et al. (2017) is positive, Cauet et al. (2015) is null, and Liepertz & Borowski (2019) is partial. The null and partial studies are not independent: Cauet et al.'s 23 teachers are a subset of Liepertz & Borowski's 35 (both ProwiN, Germany).
- **No university evidence with a learning outcome** beyond one small correlational study of learning assistants (Wang et al. 2024). Higher-education PCK research is disparate (Sarkar et al. 2024).
- **No retention or transfer outcomes.** Every student outcome here is achievement over a unit or year, or gains on the same items.
- **Measurement validity.** Cauet et al. (2015) question whether a normatively set PCK test measures what matters. Depaepe et al. (2013) and Park & Chan (2025) report inconsistent operationalisation.

Held against §11: the positive studies show that PCK predicts gains on achievement tests, not transfer. Sadler et al. (2013) measured gains on the same items the teachers answered.

## Implications for the map

1. **§4 PCK row.** Keep P0 and "Moderate–high", and qualify it: "**Moderate–high** for correlational links to school achievement (strongest in mathematics, mixed in physics); no experiment isolating PCK; no university or transfer outcomes". Keep the other cells.
2. **§5.4 new subsection "Evidence / limitations"** (after "Why it matters"), in the style of §5.2:
   - correlational links to achievement gains: Baumert et al. (2010) in mathematics; Keller et al. (2017) positive and Cauet et al. (2015) null in school physics;
   - knowing students' common wrong answers predicted gains on misconception items beyond subject knowledge (Sadler et al. 2013, middle-school physical science, same-item gains);
   - no experiment isolates PCK (only 9 studies in Gonzalez, Lynch & Hill 2022 reported it separately), a systematic review of 217 science-PCK studies found the student-outcome link inconclusive (Park & Chan 2025), while a meta-analysis found it positive only under multilevel models (Fukaya et al. 2025);
   - university physics TAs and instructors scored 65% and 68% of the maximum on a task predicting students' most common wrong FCI answers (random guessing: 40%), and the TAs missed many common difficulties (Maries & Singh 2016);
   - no university learning outcomes and no transfer outcomes.
3. **§5.4 "AI opportunity".** Add: "Seed the misconception, typical misleading cue and diagnostic question entries from student response data (concept-inventory distractors, coded exam errors), not from expert or teacher prediction. TAs miss many common difficulties, and experienced instructors scored no better (Maries & Singh 2016). Teachers review these entries and contribute representations, analogies and explanation variants, the part student data cannot supply." The coded-error step overlaps with §9 Phase 2 K0 (coding existing exam errors) and with the P1 Concept Inventories branch, which owns instrument validity.
4. **§5.4 "Questions to research next".** Keep the existing three and add one: "Do teacher-contributed representations and explanation variants improve learning beyond difficulty knowledge taken from student data?"
5. **§6 diagram.** In the EXPERT ELICITATION box, "DtD + CTA + PCK" becomes "DtD + CTA", and the LEARNER DIAGNOSIS box reads "misconceptions (PCK layer, from student data) + dialogue + assessment + knowledge tracing". This is optional: it moves PCK to where its evidence says its content comes from.
6. **§11.** Add: "Do **not** assume experts or instructors know which difficulties are common; check against student response data."
7. **§12.** Add a note 7: "**Knowledge of student difficulties is only partly held by content experts.** University physics TAs miss many common difficulties that concept-inventory data reveal, and instructors score no better (about two-thirds of the maximum, against 40% for chance). Knowing students' common wrong answers predicts gains beyond subject knowledge, though only correlationally. Seed the PCK layer from student data and let teachers review it."
8. **§14.** Add Baumert et al. (2010), Sadler et al. (2013), Keller et al. (2017), Cauet et al. (2015), Maries & Singh (2016), Nathan & Petrosino (2003), Park & Chan (2025), Carlson et al. (2019), Gonzalez, Lynch & Hill (2022). The Shulman (1986) DOI in §14 resolves correctly.

## Open questions

These are only the ones that would change the verdict:

- Fukaya et al. (2025) report that the PCK–achievement association depends on the model and is positive only in the multilevel analyses (abstract). How large the pooled r is, and whether it holds for science alone, still needs the full text (open access; download manually). A model-dependent estimate together with Park & Chan (2025) supports considering "Moderate"; the rating is left unchanged because both are correlational syntheses and the /branch stop rule requires quasi-experimental evidence or better to move it.
- Is there any experimental or quasi-experimental study, at university level, where giving instructors student-difficulty data (for example, concept-inventory distractor results) changed student learning, ideally transfer? A positive result would support the student-data-seeded PCK layer causally. None was found.
