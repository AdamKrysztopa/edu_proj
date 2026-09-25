# Explore: Knowledge Tracing / Mastery models

**Question:** Does knowledge tracing (KT) give the system a learner-state layer that improves learning, not just prediction, and what does the evidence say about knowledge components (KCs) for physics and about using DtD/CTA-derived operations as KCs?

**Verdict: no change to priority (P1); the "Moderate–high" rating is scoped to prediction.** KT models predict the next response within a tutor well, and simple, well-featured models (logistic regression, extended BKT, IRT variants) match or beat deep KT on moderate-sized data (Gervet et al. 2020: deep KT led on the largest datasets). The claim that matters for the system, that better tracing improves learning, rests on a few small, short classroom experiments:
- redesigning a tutor around a data-refined KC model improved learning in several high-school classroom experiments (e.g. d = 0.47 on an immediate post-test, Liu & Koedinger 2017; Koedinger et al. 2013; Huang et al. 2021, N = 129, one month);
- removing over-practice saved time (significant in one of six units) without a detected loss in another;
- a 2026 test of the redesign process on middle-school units chosen by topic found no difference in learning gains.

A review of 41 studies of model-driven sequencing found that none of the 8 in the cluster closest to KT (sequencing interdependent content) beat all baselines. No study found compares a KT-driven policy with a simple mastery rule on delayed or transfer outcomes. For the map, this adds one requirement for Phase 5: judge any learner model by a learning experiment against a simple mastery rule, not by predictive accuracy.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 row (P1, "Moderate–high", STEM fit High, humanities Medium, AI readiness Very high) and the §5.10 card. The §14 anchor "Corbett & Anderson — knowledge tracing / cognitive tutors" has no year or DOI. The branch serves §9 Phase 5 ("introduce knowledge tracing or another explicit learner model"), the §6 LEARNER DIAGNOSIS box ("assessment + knowledge tracing"), §10 RQ5 (explicit learner model vs conversational context) and §11 ("Do **not** assume higher predictive accuracy in a student model means better pedagogy").

Search: the OpenAlex REST API returned HTTP 429 on the one attempt; the `openalex` MCP server was not loaded. Search used the Crossref, Semantic Scholar, arXiv and ERIC APIs plus WebSearch. Full text was read for Cen, Koedinger & Junker (2007), Liu & Koedinger (2017), Doroudi, Aleven & Brunskill (2019, author version), Doroudi & Brunskill (2017), Gervet et al. (2020), Khajah, Lindsey & Mozer (2016), Piech et al. (2015), Pavlik, Cen & Koedinger (2009) and Lyu et al. (2026, arXiv 2603.29094). The rest come from abstracts or search summaries, marked below. The Kulik, Kulik & Bangert-Drowns (1990) PDF is a scanned image; the citation check OCR'd it and its figures below come from that. The Zotero local API returned no items for "knowledge tracing" or "mastery".

## Evidence

### Models and what they predict

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Corbett & Anderson (1995), https://doi.org/10.1007/BF01099821 | Series of tutor studies (abstract only) | Not in abstract | Programming (ACT Programming Tutor), university | Prediction of test performance | Defines BKT: the tutor keeps a probability that each production rule is learned and gives exercises until each is "mastered". "Currently the model is quite successful in predicting test performance." Doroudi et al. (2019) note that its mastery-remediation comparison was against no remediation, not against another sequencing rule. |
| Piech et al. (2015), arXiv 1506.05908 (NeurIPS) | Model comparison, 5-fold CV | ASSISTments 15,931 students; Khan Math 47,495 | School maths | Next-response AUC | Deep KT (LSTM) AUC 0.86 vs 0.69 for the best reported BKT on ASSISTments; 0.85 vs 0.68 on Khan. |
| Khajah, Lindsey & Mozer (2016), arXiv 1604.02416 (EDM) | Model comparison on DKT's data | ASSISTments and Synthetic from Piech et al., plus Spanish vocabulary and engineering Statics | School maths, Spanish, engineering statics | Next-response AUC | BKT extended with forgetting, skill discovery and individual ability reaches "a level of performance indistinguishable from that of DKT" (e.g. ASSISTments: classic BKT 0.73 when computed their way, BKT+F 0.83). DKT's gains "do not come from the discovery of novel representations". |
| Wilson et al. (2016), arXiv 1604.02336 (EDM) | Model comparison | 2 public + 1 proprietary dataset | Mixed | Next-response prediction | IRT-based methods "consistently matched or outperformed DKT"; a hierarchical IRT was best overall. |
| Gervet, Koedinger, Schneider & Mitchell (2020), https://doi.org/10.5281/zenodo.4143614 (JEDM 12(3)) | Model comparison | 9 real datasets | Mixed | Next-response AUC, calibration | Logistic regression with the right features (Best-LR) leads on moderate-sized datasets or those with many interactions per student; DKT leads on large datasets or where exact timing matters; Markov-process models such as BKT lag. Calibration is flagged as crucial for downstream use. |
| Pavlik, Cen & Koedinger (2009), https://doi.org/10.3233/978-1-60750-028-5-531 | Model comparison | Andes physics and Cognitive Tutor geometry datasets (grades 9–12), among others | **Physics** (high school, Andes) and geometry | Fit (LL, BIC), A′ | Performance Factors Analysis, a logistic model counting successes and failures per KC, fits slightly better than standard KT; "the differences are not large". |

Prediction is a solved-enough problem at the level the system needs: interpretable logistic or extended-BKT models are as good as deep ones on moderate data. None of these papers measures learning.

### Is the learner state identifiable and fair?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Beck & Chang (2007), https://doi.org/10.1007/978-3-540-73078-1_17 | Analysis plus data (abstract / secondary summaries) | Not verified | Reading tutor | Parameter estimates | Different BKT parameter sets give the same performance predictions while implying different knowledge states; proposes Dirichlet priors. |
| Doroudi & Brunskill (2017), EDM, https://files.eric.ed.gov/fulltext/ED577166.pdf | Theory plus simulation | — | — | Identifiability, degeneracy | What Beck & Chang showed is not an identifiability problem: under mild conditions BKT is identifiable. The real problem is **semantic model degeneracy**, where the best-fitting parameters are implausible (e.g. higher chance of a correct answer when not knowing than when knowing). |
| Baker, Corbett & Aleven (2008), https://doi.org/10.1007/978-3-540-69132-7_44 | Model comparison (title and secondary summaries only) | Not verified | Cognitive Tutor data | Prediction | Estimating guess and slip from context rather than as fixed parameters per skill. The abstract states it "fits student performance data better than prior methods"; the size of the gain was not verified. |
| Doroudi & Brunskill (2019), https://doi.org/10.1145/3303772.3303838 | Simulation | — | — | Practice given to fast vs slow learners | Simulation. KT is much more equitable than fixed practice, but BKT fit to the whole population gives slow learners too little practice. When the model is misspecified, even individualized BKT leaves a gap (0.11 in P(correct) at mastery), and N-consecutive-correct shows a similar gap. AFM-based tracing was more equitable. |

The state estimate is only as meaningful as the constraints on the model. An unconstrained fit can predict well while saying something false about what the student knows, which is §11's concern in model form.

### Does better tracing produce better learning?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Kulik, Kulik & Bangert-Drowns (1990), https://doi.org/10.3102/00346543060002265 | Meta-analysis of controlled evaluations | 108 evaluations | College, high school, upper elementary; mastery learning in general, **not KT** | Examination performance, attitudes, time | Mean ES 0.52 on exams (103 studies). 0.57 on local tests (n = 88) vs 0.29 on standardized tests (n = 11), and trivially small on standardized tests in group-paced LFM studies. Follow-up exams (~8 weeks, 11 studies): 0.71. |
| Slavin (1987), https://doi.org/10.3102/00346543057002175 | Best-evidence synthesis | Not in abstract | Group-based mastery learning, elementary and secondary; **not KT** | Standardized achievement | "No evidence to support the claim that mastery learning improves student performance on standardized achievement measures" (ERIC abstract). |
| Pane et al. (2014), https://doi.org/10.3102/0162373713507480 | Cluster RCT, matched school pairs, 2 years | Schools in 7 states | Cognitive Tutor Algebra I (mastery-based curriculum), middle and high school | Algebra proficiency exam | No effect in year 1; positive in year 2 (significant in high schools only), about eight percentile points for the median student. It tests the whole curriculum, not the tracing component. |
| Cen, Koedinger & Junker (2007), AIED 2007 (no DOI in Crossref), http://pact.cs.cmu.edu/koedinger/pubs/Cen%20&%20Koedinger%20AIED07.pdf | RCT, individual assignment, one teacher | 110 enrolled; 73 with valid pre and post; 64 with a retention test | High-school geometry Cognitive Tutor | Immediate post-test and **2-week retention**, including transfer items | KC parameters re-estimated with Learning Factors Analysis to cut over-practice (58% of practices had come after mastery). The optimized group spent less time in 5 of 6 units, about 12% of total time (not tested). Only one unit's saving was significant (30%, one-tailed p = .01; time data from 62 students). Post-test and retention did not differ (p = .77, p = .60). "No difference" here is non-significance in a small sample, not shown equivalence. |
| Koedinger, Stamper, McLaughlin & Nixon (2013), https://doi.org/10.1007/978-3-642-39112-5_43 | Classroom experiment (abstract only) | Not verified | High-school geometry (area) | Mastery efficiency, learning of targeted skills | A redesign based on a KC split separating problem-decomposition planning from execution got students to mastery faster and improved learning on the planning skills. |
| Liu & Koedinger (2017), JEDM 9(1), https://files.eric.ed.gov/fulltext/EJ1155896.pdf | RCT, individual assignment | 115 enrolled, 91 analysed | High-school geometry (area), 3 days of tutor use | Immediate post-test (same problems, different numbers) | A KC-model refinement found by Learning Factors Analysis (a hidden "find radius from area" skill) was used to redesign the tutor. The redesigned tutor gave higher post-tests (d = 0.47 from raw post-test; ANCOVA β = 0.09, p = .027; the redesign also added hints and interface scaffolding), driven by the three targeted items; time on tutor did not explain it. |
| Huang et al. (2021), https://doi.org/10.1145/3448139.3448155 | Classroom experiment, one month | 129 | High-school maths ITS | Learning outcomes, over- and under-practice | A multi-method data-driven redesign gave significantly higher learning outcomes and less over- and under-practice (per Lyu et al. 2026 and the abstract). |
| Lyu, Borchers et al. (2026), https://doi.org/10.1007/978-3-032-29760-0_12 (arXiv 2603.29094) | Randomized within-subjects crossover, preregistered | 123 | Grades 7–8 maths ITS (5 schools), 4 units chosen by topic; ~3 × 20–25 min per condition | Learning gains, time on task, mastery | Applying Huang et al.'s (2021) multi-method redesign process to units not selected for redesign potential produced **no difference in learning gains** (p = .76). Exploratory process measures favoured the redesigned units (more productive time, more skills practised, more KCs mastered). |
| Doroudi, Aleven & Brunskill (2019), https://doi.org/10.1007/s40593-019-00187-x | Systematic review of experiments comparing model-derived (RL) instructional policies with baselines | 41 studies in 34 papers | Mixed; lab and classroom | Mostly post-test or time to mastery | Counts from Table 2 (the author-version text says "21 of the 36" and "Ten studies … no significant difference", which do not match the table). 21 studies found an RL-induced policy beat all baselines. In the "sequencing interdependent content" cluster, the one closest to KT-driven curriculum sequencing, **0 of 8** did (2 mixed, 6 not significant). Only 3 of 15 classroom studies found a significant advantage. 71% (17 of 24 studies with a significant or ATI result) compared against random or weak baselines. The review includes two university-physics RL studies of activity-type sequencing (Chi et al. 2009, 2010). Success was greatest where models came from cognitive psychology. The review excludes Corbett & Anderson (1995) because it compared tracing with no remediation. |
| Pelánek & Řihák (2017), https://doi.org/10.1145/3079628.3079667 | Simulated and real data | Not in abstract | Adaptive practice systems | Mastery decisions (not learning) | The data used for the mastery decision and the threshold matter more than the choice of learner model; a simple exponential moving average is a suitable mastery criterion (abstract and search summary). |
| Ritter, Yudelson, Fancsali & Berman (2016), https://doi.org/10.1145/2876034.2876039 | Observational log analysis | ~11,000 students, 49 middle schools, one district | Middle-school maths (Cognitive Tutor/MATHia) | In-tutor error rates over the year | Median 21% of work violated mastery. Students moved on without mastery made more errors, rising over time, and lower performers were hurt most (correlational; no external outcome). |

So there is causal evidence that the KC model behind the tracing can matter. A refined KC model improved learning in several small classroom studies on hand-picked units, and removing over-practice saved time without a detected loss. The one test on units chosen by topic found no learning difference. Mastery learning in general has positive effects on local examinations (ES ≈ 0.57) and about half that on standardized tests (0.29). No study found tests a KT-driven policy against a simple rule such as N-correct-in-a-row or a moving average, with a delayed or transfer outcome.

### Knowledge components for physics, and CTA operations as KCs

- **Physics data exist and fit the same models.** Andes physics data (high school, from PSLC DataShop) were used alongside geometry to compare PFA with KT (Pavlik, Cen & Koedinger 2009). The Andes student model was a Bayesian network over problem-solution steps (Conati, Gertner & VanLehn 2002, https://doi.org/10.1023/A:1021258506583; title and secondary summary only), used to manage uncertainty about which knowledge the student applied.
- **KCs are an empirical question, answered with learning curves.** The KC model is refined until error rates fall smoothly with practice opportunities (Learning Factors Analysis: Cen, Koedinger & Junker 2006, https://doi.org/10.1007/11774303_17). The KLI framework treats a KC as any acquired unit of cognitive function inferable from performance (Koedinger, Corbett & Perfetti 2012, https://doi.org/10.1111/j.1551-6709.2012.01245.x).
- **CTA operations as KCs.** No study was found that uses CTA-elicited expert operations as KCs. The closest case is Liu & Koedinger (2017): a hidden sub-skill discovered from student data was split into its own KC, and teaching it improved the targeted items. That is a data-side counterpart to what CTA does on the expert side. An elicited operation (for example "choose conservation of momentum because the collision time is short") could be a KC if it is (a) observable as a step in student work and (b) gives a smooth learning curve when coded. Both are testable once Stage B produces logs. This is a hypothesis.
- **Single responses are weak evidence.** 31% of FCI item responses changed on a retest within a week (Lasry et al. 2011, https://doi.org/10.1119/1.3602073). BKT's guess and slip parameters absorb some of this kind of noise, which is one reason mastery is inferred over several opportunities and never from one answer.

## Against

- **Prediction is not learning.** Every model comparison above (Piech; Khajah; Wilson; Gervet; Pavlik) scores next-response prediction within the tutor. None tests whether the better predictor teaches better. This is §11 verbatim.
- **Closed-loop evidence is small and short.** A few positive closing-the-loop studies (largest N = 129, one month; Liu & Koedinger d = 0.47, N = 91, immediate, same items), one efficiency result without a powered equivalence test, and one null on units chosen by topic (Lyu et al. 2026). The redesigns bundle new tasks, hints and scaffolding with the KC change. None is in university physics, and none has a delayed transfer outcome.
- **Model-driven sequencing of interdependent content has not beaten baselines.** 0 of 8 studies in that cluster, and 3 of 15 classroom studies overall (Doroudi et al. 2019). Many positive results used weak baselines.
- **Mastery learning's standardized-test effects are small.** Slavin (1987) found no support on standardized measures; the larger effects in Kulik et al. (1990) are mostly on local examinations (0.57 local vs 0.29 standardized).
- **State estimates can be wrong while predictions are right.** Semantic degeneracy (Doroudi & Brunskill 2017) and population-level parameters that under-practise slow learners (Doroudi & Brunskill 2019; simulation; N-correct-in-a-row is susceptible too).
- **Whole-curriculum effects are not tracing effects.** Cognitive Tutor Algebra's year-2 effect (Pane et al. 2014) bundles curriculum, teacher practice and mastery learning.

Held against §11: the strong evidence here is about predictive accuracy, which §11 already says does not establish better pedagogy. The learning evidence supports only that the KC model can matter, in small immediate-outcome studies.

## Implications for the map

1. **§4 Knowledge Tracing row, evidence cell.** Replace "**Moderate–high**" with:
   > **Moderate–high for predicting performance** within a tutor (simple models match deep ones); for learning, a few small positive classroom studies of KC-model redesign on hand-picked units, one null on units chosen by topic, and no test against a simple mastery rule

   Keep the other cells.

2. **§5.10, new subsection "Evidence / limitations"** after "Domain fit":
   > Graded evidence (see `research/explore-knowledge-tracing.md`):
   > - **Prediction:** deep KT beat classic BKT (Piech et al. 2015), but extended BKT, IRT variants and well-featured logistic regression match or beat it on moderate-sized data; deep KT led on the largest (Khajah, Lindsey & Mozer 2016; Wilson et al. 2016; Gervet et al. 2020).
   > - **Learning:** redesigning a tutor around a data-refined KC model improved learning in several small high-school classroom studies on hand-picked units (d = 0.47 immediate, Liu & Koedinger 2017; Koedinger et al. 2013; Huang et al. 2021), and cutting over-practice saved time (significant in one of six units) without a detected loss (Cen, Koedinger & Junker 2007). Applied to middle-school units chosen by topic, the redesign process gave no difference in learning gains (Lyu et al. 2026). Liu & Koedinger and Cen et al. are high-school geometry; Lyu et al. is middle-school maths. Outcomes are immediate, 2-week or one-month.
   > - **Sequencing policies:** of 8 experiments sequencing interdependent content with a learner model, none beat all baselines (Doroudi, Aleven & Brunskill 2019).
   > - **State validity:** best-fitting BKT parameters can be implausible (Doroudi & Brunskill 2017), and population-level parameters under-practise slow learners (Doroudi & Brunskill 2019; simulation; N-correct-in-a-row is susceptible too).
   > - **Transfer:** no study found tests a KT-driven policy against a simple mastery rule on delayed or transfer outcomes.

3. **§5.10 "AI opportunity".** Append:
   > Prefer an interpretable model (logistic/PFA-style or constrained BKT) with a KC model checked against learning curves. Infer mastery from several opportunities, never one answer (§5.6). Whether a mastery rule beats a simple heuristic such as N-correct-in-a-row is an experiment to run, not an assumption.

4. **§5.10 "Questions to research next".** Replace "Can DtD-derived mental operations become knowledge components?" with:
   > Can CTA-elicited operations become knowledge components, i.e. are they observable as steps in student work and do they give smooth learning curves?

   Add:
   > Does a KT-driven mastery policy beat N-correct-in-a-row on delayed transfer?

5. **§9 Phase 5.** After "- introduce knowledge tracing or another explicit learner model;", add:
   > - judge it by a learning experiment against a simple mastery rule (N-correct-in-a-row or a moving average), with delayed transfer as the outcome, not by predictive accuracy;

   This is the only §9 edit. It is forced because the only closed-loop evidence is small, immediate and mixed, and §11 already rules out predictive accuracy as the criterion. No §6 change: the LEARNER DIAGNOSIS box already names knowledge tracing as one input among several.

6. **§12.** No change.

7. **§14.** Replace "Corbett & Anderson — knowledge tracing / cognitive tutors" with:
   - Corbett & Anderson (1995) — knowledge tracing: https://doi.org/10.1007/BF01099821

   And add:
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

## Open questions

These are only the ones that would change the verdict:

- Is there an experiment, in any domain, comparing a KT-driven mastery policy with N-correct-in-a-row (or a moving average) on a delayed or transfer outcome? A positive result would lift the "no test against a simple rule" qualifier; a null would narrow KT to an efficiency tool.
- Does data-driven KC redesign improve learning on units not hand-picked for it? Lyu et al. (2026) found no difference in gains when Huang et al.'s (2021) process was applied to units chosen by topic; a second test on non-selected units would settle it. Kelly, Wang, Thompson & Heffernan (EDM 2015, "Defining mastery: KT versus N-consecutive correct") compares mastery rules observationally and was not read.
- Do CTA-elicited operations, coded in Stage B logs, give smooth learning curves? If yes, they can be the physics KCs for Phase 5; if not, the KC model has to come from student data.
