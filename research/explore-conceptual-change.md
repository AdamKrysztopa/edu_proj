# Explore: Conceptual Change + misconceptions

**Question:** How well supported is conceptual change as a theory and as a family of interventions, with delayed and transfer outcomes, and what does it say about diagnosing a misconception in one learner (the §5.5 AI questions)?

**Verdict: no change to priority (P1); the rating is scoped.** Two claims hide inside "High, especially science education", and they need separate ratings:
- **High** that intuitive ideas in mechanics are common, persist through conventional instruction and coexist with the scientific idea for years. The evidence is descriptive and replicated.
- **Moderate** for interventions. Refutation text has a moderate effect across 44 comparisons from 33 studies (g = 0.41), and it holds at delayed tests. The post-secondary estimate is g = 0.33 (k = 30; learner age did not significantly moderate the effect), dissertations show almost no effect (g = 0.11, k = 6), and transfer is not analysed separately. In university physics, research-based curricula built on eliciting and confronting student ideas give larger gains whose scores hold for months to years, though retention was equally high after traditional lecture in one comparison. The designs are cohort comparisons, and no university study measures transfer.

The theory itself is contested: coherent "framework theories" against fragmented "knowledge in pieces". That debate matters for the system. A misconception label for one learner is a context-bound hypothesis, not a stable state.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline:
- §4 row: P1, "High, especially science education", STEM fit Very high, humanities Medium, AI readiness High.
- §5.5 card.
- `explore-concept-inventories.md` left the coherent-theory vs knowledge-in-pieces debate to this branch.

It serves §9 Phase 3 (diagnosis) and Phase 4 (interventions; "misconception persistence" is an outcome) and §10 RQ3.

Search: the OpenAlex REST API returned HTTP 429 on the first call, and the `openalex` MCP server was not loaded. Search used:
- Crossref for metadata and DOI resolution;
- Semantic Scholar and the ERIC API for abstracts;
- Europe PMC for the full text of Schroeder & Kucera (2022);
- WebSearch;
- the author-hosted PDF of Crouch et al. (2004).

Guzzetti et al. (1993) is closed access, so its details come from the abstract. Clement (1993) was read in full by the citation check (text-layer PDF at csun.edu). The Zotero local API has no items on conceptual change, misconceptions or refutation text.

## Evidence

### Theory: what is a misconception?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Posner, Strike, Hewson & Gertzog (1982), https://doi.org/10.1002/sce.3730660207 | Theory | — | Science learning | — | The classical model: a learner accommodates a new conception when dissatisfied with the current one and the new one is intelligible, plausible and fruitful. |
| diSessa (1993), https://doi.org/10.1080/07370008.1985.9649008 | Theory with interview data | — | Physics | — | Knowledge in pieces: intuitive physics consists of many small, context-activated elements ("p-prims"), not a coherent theory. |
| Smith, diSessa & Roschelle (1994), https://doi.org/10.1207/s15327809jls0302_1 | Theoretical critique | — | Mathematics and science | — | Argues against treating misconceptions as flawed ideas to be replaced; novice ideas are resources that are refined and reorganised into expert knowledge. |
| Vosniadou & Brewer (1992), https://doi.org/10.1016/0010-0285%2892%2990018-W | Interview study | 60 children, grades 1, 3 and 5 | Astronomy (shape of the Earth) | Mental models | Framework theory: children form coherent "synthetic" models that combine intuition with instruction. |
| Chi, Slotta & de Leeuw (1994), https://doi.org/10.1016/0959-4752%2894%2990017-5 | Theory | — | Science concepts | — | Some misconceptions come from assigning a concept to the wrong ontological category (a process treated as a thing), and changing them needs re-categorisation, not repair. |
| diSessa, Gillespie & Esterly (2004), https://doi.org/10.1207/s15516709cog2806_1 | Theoretical analysis plus two empirical studies (a quasi-replication of Ioannides & Vosniadou 2002 and an extension study) | Not in abstract | Concept of force | Coherence of student ideas | "Coherence" and "fragmentation" are not well defined. They propose judging a concept by its contextuality (the range of contexts it applies in) and its relational structure, and their data strongly undermine Ioannides & Vosniadou's claim that ideas about force are coherent; students' ideas are "not random and chaotic; but neither are they simply described and strongly systematic". |
| Özdemir & Clark (2007), https://doi.org/10.12973/ejmste/75414 | Narrative review | — | Science | — | Two competing perspectives, knowledge-as-theory and knowledge-as-elements, "implicate radically different pathways for curricular design". The literature historically favoured knowledge-as-theory; the review sets out arguments and educational implications that "potentially favor" knowledge-as-elements. |

The debate is unresolved. Its practical consequence for this project is shared by both sides: whether a learner uses an intuitive idea depends on context. Under knowledge-in-pieces this is the core claim. Framework theory produces it through synthetic models that mix intuition with instruction.

### Do intuitive ideas persist?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Shtulman & Valcarcel (2012), https://doi.org/10.1016/j.cognition.2012.04.005 | Speeded verification experiment | Adults with many years of science education; N not in abstract | 10 domains including mechanics | Response time and accuracy | Statements where naive and scientific theories disagree were verified more slowly and less accurately. Naive theories "survive the acquisition of a mutually incompatible scientific theory, coexisting with that theory for many years". |
| Kim & Pak (2002), https://doi.org/10.1119/1.1484151 | Correlational | Korean students (level not stated in abstract); N not in abstract | Mechanics (student level not verified) | Conceptual test vs self-reported number of problems solved (average ~1,500) | Students kept the well-known conceptual difficulties; there was little correlation between problems solved and conceptual understanding. |
| Miller, Lasry, Chu & Mazur (2013), https://doi.org/10.1103/PhysRevSTPER.9.020113 | Prediction and recall study at two universities | Not in abstract | **University** mechanics and E&M | Observation and recall of lecture demonstrations, right after and weeks later | About one in five observations of a demonstration was inconsistent with the actual outcome. Students who understood the concept beforehand observed more correctly. Predicting first made a correct observation about 20% more likely, and learning depended on observing correctly. |
| Lasry et al. (2011), https://doi.org/10.1119/1.3602073 (already in the map) | Test–retest within a week | 100 | College | Item stability | 31% of FCI responses changed on retest. See `explore-concept-inventories.md`. |

A learner who answers correctly may still hold the intuitive idea and use it under time pressure or in another context. A learner who picks a distractor once may not hold it stably. Both points bear on §5.5's "slip vs stable conceptual model" question.

### Do conceptual change interventions work, and do they last?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Schroeder & Kucera (2022), https://doi.org/10.1007/s10648-021-09656-z | Random-effects meta-analysis of between-subjects experiments | 44 comparisons, n = 3,869 | Mathematics, science, social science; mostly post-secondary | Knowledge tests, most delayed test coded | g = 0.41 overall.<br>By domain: science g = 0.45 (k = 33).<br>By learner age (no significant difference, p = 0.25): post-secondary g = 0.33 (k = 30).<br>By test timing, no significant difference: same day 0.39 (k = 17); 2 days to 1 week 0.38 (k = 11); 8 days to 1 month 0.43 (k = 13); over 1 month 0.56 (k = 2).<br>By publication type (Qb(2) = 9.01, p = 0.01): dissertations g = 0.11 (k = 6, n.s.), journal articles 0.45 (k = 36), proceedings 0.73 (k = 2).<br>I² = 61. Egger's test showed no funnel asymmetry (p = 0.29); trim-and-fill gave g = 0.28. |
| Tippett (2010), https://doi.org/10.1007/s10763-010-9203-x | Narrative review with secondary analysis | Two decades of studies | Science and reading education | Various | Refutation text is described as one of the most effective text-based means of changing misconceptions. No developmental relationship was found. |
| Guzzetti, Snyder, Glass & Gamas (1993), https://doi.org/10.2307/747886 | Meta-analysis of experimental and quasi-experimental studies | Not in abstract | Reading and science education | Misconception measures | Effective interventions shared an element of conceptual conflict. |
| Guzzetti (2000), https://doi.org/10.1080/105735600277971 | Research synthesis | — | Text-based conceptual change | — | Refutational text alone is not sufficient, and discussion must be teacher-guided. Of the text-based strategies, only refutational text shows long-term effects. |
| Zengilowski, Schuetze, Nash & Schallert (2021), https://doi.org/10.1080/00461520.2020.1861948 | Critical review | — | Refutation text literature | — | The literature relies on a single topic or very few per study. It neglects the role of testing in conceptual change, and changes are rarely checked beyond an immediate posttest. |
| Limón (2001), https://doi.org/10.1016/S0959-4752%2800%2900037-2 | Critical review | — | Cognitive conflict | — | Studies applying cognitive conflict give controversial results. The review sets out the theoretical and practical problems of implementing conflict as a strategy. |

### Physics-specific interventions

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Crouch, Fagen, Callan & Mazur (2004), https://doi.org/10.1119/1.1707018 | Within-course design with the demonstration mode rotated across sections weekly; free-response test at end of semester | 122 students (133 enrolled); 7 demonstrations; absent students counted as controls; p-values pool ~854 student-by-demonstration responses as independent | **University physics** (Harvard Physics 1a) | **End-of-semester** outcome and explanation | Correct explanations:<br>- no demo 22%;<br>- passive observation 24% (p = 0.64);<br>- predicting first 30% (p = 0.04);<br>- predicting plus discussion 32% (p = 0.02).<br>Predicting added about 2 minutes. Fully correct explanations stayed low in every mode. |
| Clement (1993), https://doi.org/10.1002/tea.3660301007 | Quasi-experimental; experimental vs control classes, not randomized | 205 high-school students (150 experimental, 55 control; 5 teachers, 4 schools) | **High-school mechanics** (normal force, friction, Newton's third law) | 15-item test with near- and far-transfer items; posttest 2 months or more after the lessons | Experimental gains exceeded control by 27.5 points on average (about 1.5 SD, t = 8.41, p < .0001), significant in all three areas; experimental pretest scores were somewhat higher. |
| Finkelstein & Pollock (2005), https://doi.org/10.1103/PhysRevSTPER.1.010101 | Implementation study over two semesters, no randomized control | N = 336 | **University** intro mechanics | FMCE, immediate | Tutorials in Introductory Physics, built on eliciting, confronting and resolving student ideas, gave a median normalized gain of 0.77. This replicates the original tutorial studies. |
| Pollock (2009), https://doi.org/10.1103/PhysRevSTPER.5.020110 | Longitudinal cohort comparison over 8 semesters | Not in abstract | **University** E&M | BEMA scores **years later** (juniors) | Individual BEMA scores did not change significantly after the introductory course. Juniors who had taken a non-tutorial freshman course scored significantly lower than those from the tutorial course. |
| Francis, Adams & Noonan (1998), https://doi.org/10.1119/1.879933 | Follow-up of three classes | Not in abstract | **University** non-major intro mechanics | FCI up to **four years** later | High FCI gains from an inquiry-based tutorial approach persisted up to four years after instruction (abstract and later citations; full text not read). |
| Deslauriers & Wieman (2011), https://doi.org/10.1103/physrevstper.7.010101 | Two equivalent cohorts, different teaching | 57 and 67 enrolled; 48 and 62 tested at course end; 29 and 44 retested (consecutive years, different instructors) | **University** modern physics (quantum) | QMCS at course end, **6 and 18 months** later | The cohort taught by a highly rated traditional lecturer scored 19% lower (67% vs 85% on the QMCS) than the interactive-engagement cohort. Retention was high in both: a few percent decrease at 18 months (lecture cohort, N = 29) and at 6 months (IE cohort, N = 44). |

Taken together, the effects are real. Refutation text works in controlled experiments, including at delayed tests. Scores from research-based physics curricula hold up over months to years (Pollock 2009; Francis et al. 1998), but retention was equally high after traditional lecture (Deslauriers & Wieman 2011); what lasts is the larger initial gain. The physics evidence compares cohorts or rotates demonstrations within one course, and the university outcomes are concept-inventory items, not transfer to new problems (the one study with near- and far-transfer items, Clement 1993, is high school). Crouch et al. (2004) is the closest result to the §5.5 idea of "discriminating cases", though its seven demonstrations were standard lecture demonstrations, not designed to discriminate between models. Passive observation modestly raised correct outcome predictions on the end-of-semester test (61% to 70%, p = 0.03) but not correct explanations (22% to 24%, p = 0.64); predicting first raised explanations to 30% (p = 0.04), and even then most explanations stayed wrong.

### AI opportunity (§5.5): LLM diagnosis of misconceptions

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Smart, Bos & Bos (2024), https://doi.org/10.1007/978-3-031-60609-0_21 | Benchmark: LLM answers compared with student answer distributions; LLM vs one teacher explaining wrong answers | 388 NAEP items | Grades 4, 8, 12 mathematics and science; **not university** | Agreement | LLMs found the same items difficult as students to a statistically significant but small degree, varying by model; under minimal prompts they often chose the same wrong answers as students, less so with chain-of-thought prompting. GPT-4's explanations of frequently chosen wrong answers agreed fully or partly with an experienced science teacher's in 81% of cases. |
| Savage & Rebello (2025), https://doi.org/10.1119/perc.2025.pr.Savage (already in the map) | LLM coding of written explanations | 1,131 | 3 EMCS items, university | Correct/incorrect agreement | Matched human graders on correct/incorrect; the categories of wrong ideas were not checked against human coders. |
| Parker & Zavala-Cerna (2026), arXiv 2605.00294 (preprint, not peer reviewed) | Quiz analytics plus LLM characterisation | 3,802 enrolments | Online medical courses; **outside physics** | Descriptive | LLMs were used to characterise misconceptions behind hard, central quiz topics. There was no validation against individual students. |

No study was found that checks an LLM's misconception diagnosis for an individual student against an interview, a retest or behaviour in a second context. The studies found work at item or population level: which wrong ideas are common and why a distractor attracts students.

## Against

- **The construct is contested.** Knowledge in pieces (diSessa 1993; diSessa et al. 2004; Smith et al. 1994) disputes that learners hold stable misconceptions at all. If that view is right, "the learner's model" in §5.5 is a context-bound pattern, not a state to be diagnosed once.
- **Suppression, not replacement.** Scientific knowledge suppresses naive intuitions but does not replace them (Shtulman & Valcarcel 2012). A correct answer after instruction does not show that the misconception is gone, and a speeded test brings it back.
- **Refutation text is thin on physics-specific and transfer evidence.** Most comparisons are post-secondary (k = 30 of 44, g = 0.33; learner age did not significantly moderate the effect), but transfer is not analysed separately and only 2 comparisons test beyond a month (Schroeder & Kucera 2022). Dissertations average g = 0.11 (k = 6) against 0.45 for journal articles, although Egger's test found no funnel asymmetry and trim-and-fill still gave g = 0.28. Critics note single-topic designs and little follow-up (Zengilowski et al. 2021). Refutation text alone is not sufficient (Guzzetti 2000).
- **Conflict alone is unreliable.** Cognitive conflict has controversial results (Limón 2001). Passively watching a standard lecture demonstration did not improve end-of-semester explanations (22% vs 24%, p = 0.64), though it modestly improved outcome predictions (61% vs 70%, p = 0.03) (Crouch et al. 2004), and about one in five observations was inconsistent with the actual outcome (Miller et al. 2013).
- **The physics curriculum evidence is not randomized.** Tutorials and interactive engagement are supported by cohort comparisons and follow-ups (Finkelstein & Pollock 2005; Pollock 2009; Francis et al. 1998; Deslauriers & Wieman 2011), none randomized and none measuring transfer to new problems; retention was equally high after traditional lecture in Deslauriers & Wieman (2011).
- **No individual-level LLM diagnosis evidence.** Agreement with one teacher on why a distractor is popular (Smart et al. 2024) is item-level, not a diagnosis of one student.

Held against §11: the intervention evidence measures misconception items, mostly immediately or within a month, not transfer. The persistence evidence shows that correct answers do not equal understanding, which is the §11 point already on the map.

## Implications for the map

1. **§4 Conceptual Change row, evidence cell.** Replace "**High, especially science education**" with:
   > **High** that intuitive ideas persist and coexist with instruction (physics especially); **moderate** for interventions (refutation text g ≈ 0.4, holding at delay; physics curricula show larger gains that persist, in cohort studies; no university transfer outcomes); theory contested (coherent vs fragmented)

   Keep the other cells.

2. **§5.5, new subsection "Evidence / limitations"** after "Why it matters for physics":
   > Graded evidence (see `research/explore-conceptual-change.md`):
   > - **Persistence:** naive intuitions survive science education and coexist with the scientific idea for years (Shtulman & Valcarcel 2012). Solving many traditional problems leaves conceptual difficulties intact (Kim & Pak 2002).
   > - **Theory contested:** coherent framework theories (Vosniadou & Brewer 1992) against knowledge in pieces (diSessa 1993; diSessa, Gillespie & Esterly 2004). Both imply that whether a learner uses an intuitive idea depends on context.
   > - **Refutation text:** g = 0.41 across 44 comparisons (33 studies), stable across test delays up to a month and beyond (k = 2 beyond); post-secondary g = 0.33 (age not a significant moderator); dissertations g = 0.11 (Schroeder & Kucera 2022). Not sufficient on its own (Guzzetti 2000).
   > - **Conflict needs commitment:** passively observed demonstrations did not improve end-of-semester explanations; predicting first did, modestly (Crouch et al. 2004). Cognitive conflict alone gives inconsistent results (Limón 2001).
   > - **Physics curricula:** elicit–confront–resolve tutorials and interactive engagement give larger conceptual gains whose scores hold for months to years (Pollock 2009; Deslauriers & Wieman 2011, where retention was equally high after traditional lecture), from cohort comparisons, not randomized trials. No university study measures transfer; a high-school bridging-analogies study included near- and far-transfer items with a two-month delay (Clement 1993).

3. **§5.5 "AI opportunity".** Append:
   > Treat a diagnosed misconception as a context-bound hypothesis, not a stable state: confirm it in a second surface context before acting on it, and re-check it after instruction, since a correct answer can coexist with the intuition (Shtulman & Valcarcel 2012). A discriminating case works better when the learner commits to a prediction before seeing the outcome (Crouch et al. 2004; Miller et al. 2013). No study has validated an LLM's misconception diagnosis for an individual learner; the studies found work at item level (Smart, Bos & Bos 2024; Savage & Rebello 2025).

4. **§5.5 "Questions to research next".** Replace "How do we distinguish a slip/calculation error from a stable conceptual model?" with:
   > Does a misconception label for one learner predict their answers in a second context and on retest, or only on the item it came from?

5. **§9 Phase 3.** After "Also measure each method's test–retest stability for the same student; …", add:
   > and its cross-context consistency: whether the same diagnosed idea shows up when the concept is probed in a second surface context (diSessa, Gillespie & Esterly 2004).

   This follows from the evidence rather than preference: both theories predict that intuitive ideas are context-dependent, and Phase 3 compares diagnoses as if they were learner states.

6. **§9 Phase 4.** Add to the list of interventions:
   > - refutation (state the likely wrong idea, then refute it);
   > - predict-then-observe discriminating cases.

   Both have controlled evidence (Schroeder & Kucera 2022; Crouch et al. 2004) and neither is on the list. "Misconception persistence" is already an outcome. No change to Stage B follows: its primary outcome is already delayed transfer, and the operations it teaches are principle-selection moves, not refutations.

7. **§11.** Add:
   > - Do **not** assume a misconception is gone because a learner now answers correctly; naive intuitions persist alongside the scientific idea.

8. **§12.** No change.

9. **§14.** Replace "Posner et al. (1982) — conceptual change" with "Posner et al. (1982) — conceptual change: https://doi.org/10.1002/sce.3730660207", and add:
   - Schroeder & Kucera (2022): https://doi.org/10.1007/s10648-021-09656-z
   - Guzzetti et al. (1993): https://doi.org/10.2307/747886
   - Guzzetti (2000): https://doi.org/10.1080/105735600277971
   - Zengilowski, Schuetze, Nash & Schallert (2021): https://doi.org/10.1080/00461520.2020.1861948
   - Limón (2001): https://doi.org/10.1016/S0959-4752%2800%2900037-2
   - Shtulman & Valcarcel (2012): https://doi.org/10.1016/j.cognition.2012.04.005
   - diSessa (1993): https://doi.org/10.1080/07370008.1985.9649008
   - diSessa, Gillespie & Esterly (2004): https://doi.org/10.1207/s15516709cog2806_1
   - Vosniadou & Brewer (1992): https://doi.org/10.1016/0010-0285%2892%2990018-W
   - Kim & Pak (2002): https://doi.org/10.1119/1.1484151
   - Clement (1993): https://doi.org/10.1002/tea.3660301007
   - Crouch et al. (2004): https://doi.org/10.1119/1.1707018
   - Miller et al. (2013): https://doi.org/10.1103/PhysRevSTPER.9.020113
   - Pollock (2009): https://doi.org/10.1103/PhysRevSTPER.5.020110
   - Deslauriers & Wieman (2011): https://doi.org/10.1103/physrevstper.7.010101
   - Smart, Bos & Bos (2024): https://doi.org/10.1007/978-3-031-60609-0_21

## Open questions

These are only the ones that would change the verdict:

- Is there a randomized university-physics study of a conceptual change intervention (refutation, predict–observe–explain, bridging analogies) with a **transfer** outcome to new problems? A positive result would raise the intervention rating from moderate; a null would narrow it to misconception items.
- Do refutation effects hold for post-secondary physics specifically, beyond a month? The meta-analysis has only 2 studies beyond a month, across all domains.
- Does any study show that a misconception diagnosed in one context predicts the same learner's reasoning in another? If not, individual misconception diagnosis should be dropped from Phase 3 in favour of item-level difficulty data.
