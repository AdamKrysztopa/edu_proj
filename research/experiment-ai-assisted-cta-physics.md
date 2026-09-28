# Experiment: AI-assisted CTA elicitation → novice transfer, one physics topic

**Status (2026-09-28): part of the chosen route.** `research/roadmap.md` uses this study's registered rules unchanged: early K0 is milestone M1, Stage A is M4 and Stage B is M6, with a feasibility run (M5) before Stage B in its own offering. Additions in the roadmap (component items and a second form in early K0, a guard rule applied in both arms) are secondary and cannot change what K0, K1 or K2 decide. Stage A serves Phase 2; Stage B is one Phase 4 intervention comparison. This design does not replace Phase 3's learner-diagnosis comparison or commit the project to an adaptive system. Its numerical gates are specific to this topic and design.

**Question:** What is the smallest defensible study showing that AI-assisted CTA elicits expert knowledge that improves novice transfer in one university physics topic?

**Verdict:** a gated two-stage design. Stage A runs only if early K0, a student-error check on an earlier offering, does not stop the study; it is a within-expert elicitation study with 12 physicists, comparing ordinary explanation, think-aloud trace alone, AI-led probes and human-led probes. Stage B runs only if the Stage A gate (K1) and the pretest-error check (K0) pass: a two-arm individually randomized trial with about 370 first-year students and **delayed transfer** as the primary outcome. No rating on the map changes; this adds a design to §9 Phase 2. The `methods-critic` review found no fatal flaw and six major threats; the fixes are applied below (see "Review").

**§9 kill criteria:** none met yet. Phase 1 has no bottleneck data, and no past exam scripts are available. The design therefore includes a small Phase 1 check (K0 below) run twice on new items: early K0, on an earlier offering, can stop the study before experts are recruited; K0 on the Stage B cohort's pretest can stop Stage B.

Baseline allowed to move:
- **§9 Phase 2** lists four elicitation arms and four measures, including "whether novices actually benefit from the recovered operations".
- **§10 RQ1** (can an AI interviewer recover tacit operations absent from ordinary materials), **RQ2** (reproducible across experts, observable in performance) and **RQ4** (does teaching the operation improve transfer).
- **§5.2 "Provisional method for physics":** think-aloud while solving, then retrospective CDM-style probes over the trace, then comparison across experts. AI probes run after the task, never during it.
- **§11**: no fluency-only or immediate-only evidence; expert verbalization and LLM reconstructions are not trusted without validation.

Search: OpenAlex REST API (the `openalex` MCP server is not loaded in this session), Unpaywall and publisher full text for effect sizes. Zotero's local API responded but holds no items on physics education, think-aloud, worked examples, CTA or AI interviewing.

## Design

### Topic
Introductory university mechanics: **selecting and combining conservation principles** (energy, momentum, and energy plus momentum in multi-stage problems such as collisions followed by motion). Reasons:
- principle-based versus surface-based problem representation is a classic expert–novice difference in physics (Chi, Feltovich & Glaser 1981);
- instruction that targets it has precedents to compare against (Dufresne et al. 1992; Docktor et al. 2015);
- a misconception instrument exists for the topic (EMCS; Singh & Rosengrant 2003).

### K0: Phase 1 check (before Stage B)
No past exam scripts are available, so K0 uses new data from the Stage B cohort.
- **Items.** The topic pretest carries 2 open-response problems (about 15 minutes) with the same principle structure as the Stage A problems (collision followed by energy conservation) and different surface features. No K0 item repeats, or is isomorphic to (same principle sequence and same unknown), a delayed-test item; the delayed-test authors receive the K0 items to check this.
- **Timing.** The pretest is given after the course's lectures and problem sets on energy and momentum conservation, at least 7 days before the module opens, and carries completion credit. It precedes randomization, so coders cannot know a student's arm, and both arms sit the same items.
- **Unit and sample.** Consenting students are sampled at random and one randomly chosen K0 item is coded per student, until 100 solutions containing an error are coded. The unit is the first substantive error (the earliest step that departs from a correct solution), one code per solution: prerequisite or maths; principle selection or representation; other. Blank and correct solutions are counted and reported but are not in the denominator.
- **Coding.** Codebook with anchor examples, sampling rule, unit and decision rule are pre-registered with Stage B before the pretest is given, citing the early-K0 record unchanged; all Stage B materials, prompts and the delayed test are frozen at that point, and K0 results cannot change them. Two coders, neither the instructional designer nor the PI, double-code all 100 solutions. Target κ ≥ 0.70; below that, they retrain and recode once. K0 is decided on the adjudicated codes.

**Stop** Stage B if fewer than 30% of errors are principle selection or representation, judged on the point estimate and reported with its Wilson 95% CI (about ±9 pp at n = 100). That meets the §9 Phase 1 kill criterion for this topic ("bottlenecks explained mostly by ordinary prerequisite knowledge"). The 30% threshold is a judgment carried over from the exam-script design and not calibrated for a pretest, so the pretest's full error profile is reported next to it. Stage A's results still stand as RQ1 evidence; no RQ4 claim is made for this topic. Stage B reports which K0 error codes each added operation addresses.

**Early K0 (before the Stage A data sessions).** The same 2 items run as a quiz in an earlier offering, in a different cohort from Stage B, at the same point relative to the topic's lectures and under that cohort's own research consent; non-consenters' scripts are not kept.
- **Registration.** The 2 items, codebook with anchors, unit, sampling and decision rule are registered before the quiz. The Stage B pre-registration cites that record unchanged. Any later change to an item or code is a logged deviation, and early K0 is not recoded under it.
- **Effort.** The quiz carries the pretest's completion credit where the course allows it. A solution enters the denominator if it contains at least one step beyond restating the givens (an equation or a diagram with quantities); one that stops after that point is coded at its first substantive error. Attempt and attendance rates are reported.
- **Leakage.** Scripts are collected and no item-specific solutions are released; feedback is given on the topic only. Stage B records whether each student sat early K0; those students are left out of the pretest K0 sample and flagged in the covariate analysis.
- **Decision.** **Stop before recruiting the 12 experts** if fewer than 30% of errors are principle selection or representation. Early K0 can stop the study only if it reaches 100 errored solutions; with fewer it is reported as inconclusive and Stage A proceeds on the literature premise. A new topic needs its own early K0 on its own items before experts are recruited. A pass does not replace K0: the pretest check runs on the analysed cohort and alone decides Stage B. If the two checks fall on opposite sides of 30%, both are reported with their Wilson CIs and attempt rates, and the difference is discussed as a cohort or effort effect.
- **Use in Stage B.** Early-K0 codes may choose the four worked-example problems and which steps carry prompts, applied identically to both arms. They do not add, drop or rank operations: the treatment carries every operation that passed K1. The mapping from operations to early-K0 error codes is registered with the Stage B freeze; the report of which K0 error codes each operation addresses uses the pretest codes and is checked against that mapping.

The 1–2 pilots may run before early K0, since they only build the Stage A operation codebook and use no data-session experts.

Until K0 runs, the topic rests on indirect evidence: experts categorize and represent mechanics problems by principle and novices by surface features (Chi, Feltovich & Glaser 1981), though a larger replication found wide overlap between calculus-based first-year and graduate students (Mason & Singh 2011, https://doi.org/10.1103/PhysRevSTPER.7.020110). No cited study measures how often first-year errors on conservation problems are principle selection; K0 does. Early K0 keeps the stop before experts are recruited. Without it, Stage A would run on this premise alone; K1 tests elicitation, which does not depend on student errors, so that risks only expert time on a topic Stage B may drop. The Stage A problems are standard multi-stage conservation problems checked by a physicist, not selected by error rate; K0 confirms the bottleneck on items of the same structure before Stage B. The two ordinary-explanation problems (E_A, E_B) are listed with the four think-aloud problems and checked with them, since the "absent" judgment depends on which problems were explained.

### Stage A: elicitation (within-expert)

**Participants.** 12 physicists who have taught or examined the course topic, plus 2 pilot experts used only to build the codebook. Twelve lies in the 9–17 range at which code saturation was reached in homogeneous interview samples (Hennink & Kaiser 2022, outside physics). Saturation is checked with the Guest, Namey & Chen (2020) run-length method. Recruitment extends to 16 if the last 3 experts still add more than 5% new operations.

**Session order per expert** (fixed, so that the baseline is not contaminated):
1. **Ordinary explanation** (§9 arm 1). Before anything else, the expert writes a worked explanation of two problems, one from each problem set and not used later, "for a first-year student".
2. **Think-aloud solving** (§9 arm 4). Non-directed think-aloud instructions only, on four new problems (sets A and B, two each), with the written and diagram work captured on a tablet. No probing, because describe/explain prompts during the task are reactive (Fox, Ericsson & Best 2011).
3. **Retrospective CDM-style probes** over the transcript and captured work: set A by one interviewer and set B by the other (§9 arms 2 and 3). The AI interviewer is an LLM running a fixed probe script. The human is a trained interviewer running the same script. Probes cover cues noticed, alternatives rejected, checks, anomalies and "what would a novice miss here?". Both see the same transcript and scans, and both get a hard cap of 20 minutes per problem set, so that the AI cannot win by simply asking more.
   - Interviewer × problem set × order is counterbalanced: 4 sequences × 3 experts. Session order is a term in the estimate, because the second probe session is primed by the first.
   - The model ID, effort setting and prompt hashes are frozen, and the app refuses a data session if they differ from the pre-registered values. Current models do not accept a sampling temperature, so every request and response is logged in full instead. Both interviewers follow the same rule for unscripted follow-ups: at most one follow-up per scripted probe, restating the expert's own words; for the AI the app checks that the quoted words occur in the expert's speech. Both interviewers use the same session app (`instrument/`). With one human interviewer, the claim is scoped to "vs this interviewer".

The decoding interview (§5.1) is **not** an arm. It is deferred to a follow-up comparison (PROGRESS.md "open evidence gaps").

**Coding.**
- Unit: a *mental operation*, meaning a cue, decision, representation choice, check or heuristic that a novice could be taught.
- Before coding, interviewer turns are removed and expert utterances segmented, so that coders cannot tell from question style which interviewer ran a session. Blinding will not be complete (expert replies may echo the question) and is checked: coders guess the condition for 20 sessions, and the guess rate is reported.
- Two coders double-code 25% of sessions before single-coding the rest, with a target of ≥ 0.70 on each agreement statistic:
  - Krippendorff's α for identifying and segmenting operations;
  - κ for the status tags below;
  - κ for matching operations across experts ("is this the same operation?").
- The ordinary-material baseline is the experts' explanations **plus** the course textbook chapter and lecture notes. An operation counts as *absent* only if coders judge that it applies to the explained problems and appears in none of these.
- Each operation is tagged by **source** (explanation / trace-only / AI probe / human probe) and by **status**:
  - *trace-only*: extracted from the think-aloud and written work by a coder who has not seen the probe transcripts;
  - *probe-added, performed*: named first in a probe, then corroborated in the trace by a third coder. That coder is blind to interviewer. Their list is mixed with decoy operations taken from other experts and other problems, and the false-corroboration rate on the decoys is reported;
  - *reported only*: named in a probe, with no corroboration in the trace;
  - *contradicted*: the trace shows the expert doing something else.
- **Shared** means an operation is present in at least 3 of the 12 experts.
- Each operation is also tagged if it already appears in a published physics problem-solving framework (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015), so that "new" is not confused with "absent from this course". The tag does not change K1; Stage B reports how many added operations carry it.

**Outcomes.**
1. Per expert and interviewer: the number of *performed, shared* operations that are absent from the ordinary explanations.
2. The *contradicted* and *reported-only* rates among probe-elicited operations, per interviewer. This is the §11 check for plausible-but-false reconstruction.
3. Importance ratings, given one week later by *other* experts who are blind to each operation's source.

With 12 experts, the AI–human difference is **estimated** (paired means with 95% CI), not tested. Stage A is an estimation and gating study.

**K1: Stage A gate (pre-registered).**
- (a) The AI-assisted pipeline (trace plus AI probes) yields **at least 3** performed, shared operations that are absent from the ordinary material.
- (b) **At least 2** of those are *probe-added by the AI*, not trace-only.
- (c) The upper bound of the 95% CI for the AI-minus-human contradicted rate is **no more than 15 percentage points**.

Outcomes:
- If (a) or (c) fails, RQ1 is answered negatively for this topic and Stage B does not run.
- If only (b) fails, Stage B may still run. Its claim is then restated as "trace-based CTA", and the AI question counts as a null.

The thresholds are judgment calls. They are fixed before data collection, not derived from literature.

### Stage B: learning (two-arm RCT)

**Participants.** First-year students in the university mechanics course, randomized individually and stratified on the pretest's closed-response score (or the midterm score; the open-response K0 items are scored afterwards and enter the analysis as covariates only), in a graded-for-completion online module run before the topic's exam.

**Conditions.** Both arms get the same four worked examples with self-explanation prompts, delivered as a **static** module with no LLM tutor, so that §5.12 delivery effects cannot confound the result. The two arms are matched for word count (±10%, prompts and model answers included) and allotted time (2 × 40 min).
- **Control (strong):** worked examples built from the experts' *ordinary explanations* in Stage A, edited by the same instructional designer. This is the expert-authored baseline of Feldon et al. (2010), not a lecture baseline.
- **Treatment:** the same examples, plus the performed, shared operations recovered by the **AI-assisted pipeline** that are absent from the ordinary explanations. Each added operation is performed in a worked step and carried by a self-explanation prompt in at least two of the four examples, asking the student to justify that step or apply the operation to the next, faded step; operations given only as text would test the delivery format, not the operations (see `explore-worked-examples-self-explanation.md`). The answer is submitted and locked before a model answer is shown; a blank answer does not count as answered.
- **Prompts in both arms.** Both arms have the same number of prompts, drawn in the same proportions from one fixed list of stems (which principle this step uses and why its conditions hold; apply it to the next step; what check confirms the result), with model answers of equal length. Prompts on steps present in both arms are identical. Only the prompts carrying added operations differ; in the control, the same stems go to steps already present. Prompts are piloted on non-participants until median time per prompt differs by no more than 10% between arms.

**Measures.**
- **Covariate:** a topic pretest (including the K0 open-response problems) and the student's prior midterm score.
- **Primary: delayed transfer, 2–3 weeks after the module.** Problems that share the principle structure of the training problems but differ in surface context, plus problems that need the same principles in a new combination.
  - Written by two physics instructors who took no part in Stage A or the materials. They work from a specification of target principles only, never from the operations list, which guards against assessment alignment (§5.9, Kulik & Fletcher 2016).
  - **Scored for correctness only:** the correct principle set, correct equations and correct answer. The rubric does not reward write-up steps that the treatment teaches, which also keeps scorers blind to arm.
  - Items are piloted on non-participants, targeting 30–70% correct, and reliability is reported.
  - The delayed test is a credited course activity. The missing-data rule (multiple imputation under missing at random, plus a worst-case bound) is fixed in advance.
- **Secondary:**
  - a score on the published problem-solving rubric of Docktor et al. (2016), https://doi.org/10.1103/physrevphyseducres.12.010130, which is *not* blind to arm;
  - immediate and delayed performance on near problems;
  - the same selected EMCS items at pretest and delayed test, excluding Q16, Q22 and Q23, which had item–total correlations below 0.20 and lowered α in the largest analysis (Wu, Li & Rebello 2025), analysed at arm level and labelled exploratory. The full test has α ≈ 0.75 in calculus-based courses (Singh & Rosengrant 2003), but no validation exists for item subsets;
  - a Chi-style problem-categorization task, given *after* the transfer test so it cannot prime it;
  - logged time on task per arm and prompts answered. A random 10% of answers per arm are scored, by a coder who did not write the materials, for whether they attempt the targeted step. If median logged time in the treatment exceeds the control by more than 10%, the claim is restated as "operations plus extra time";
  - at the delayed test, "did you see the other version?".

**Analysis and power.**
- ANCOVA on delayed transfer, pre-registered.
- **Smallest effect size of interest (SESOI): d = 0.30.** This is a pre-registered judgment of the smallest effect worth the elicitation cost, not an estimate of the likely effect.
- **Expected effect: probably below the SESOI.** Prompted self-explanation against no prompts gives g = 0.35 on delayed tests and 0.33 on transfer (Tan et al. 2025, https://doi.org/10.1007/s10648-025-10001-x). Both arms here are prompted, so the contrast is the added operations alone, and the closest physics test of teaching expert decisions found no direct effect (Jeong et al. 2024). Stage B is therefore built to rule out d ≥ 0.30 (K2), not to detect a small effect: at the planned N, power for a true d = 0.15 is about 0.3. Barbieri et al.'s (2023) negative moderator compares examples with and without prompts across studies; both arms here have prompts, so it does not bias the contrast.
- **Exploratory: arm × pretest** (continuous pretest; expertise reversal, Kalyuga 2007, https://doi.org/10.1007/s10648-007-9054-3). Reported with its CI. It is not powered and cannot overturn K2.
- For α = .05 two-sided, power .80, a conservative pretest r = .4 (no source for this population) and 20% attrition: **≈ 183 per arm, ≈ 370 randomized.**
- A single course of 200 students gives a minimum detectable effect (MDE) of about d = 0.41. If enrolment is below 370, pool two semesters or two sites; do not proceed underpowered.
- **Compliance** is fixed in advance: at least 60 of the 80 minutes logged, and at least 75% of self-explanation prompts answered. The intention-to-treat (ITT) estimate is primary. A per-protocol estimate among compliers in both arms is a secondary sensitivity analysis (both arms can take partial doses, so a CACE is not cleanly identified).

**K2: Stage B kill criterion.** Applies only if at least 70% of students in each arm meet the compliance threshold. Otherwise the run counts as a failed dose, not a null. One re-run with re-piloted prompts is allowed; a second compliance failure is a kill (the material cannot be delivered at this dose in a static module).
- **Kill:** the upper bound of the 90% ITT CI for delayed transfer is below d = 0.30 (observed d ≲ 0.12 at the planned N). Stop using elicited operations as instructional content for this topic, and record this in the map on RQ4 as "effect below the SESOI d = 0.30", not as a null.
- **Inconclusive** (observed d between about 0.12 and 0.21): run one replication semester and decide once on the pooled estimate: kill if the pooled 90% upper bound is below 0.30, otherwise report a positive effect.

**Ethics.**
- The control arm is ordinary, good-quality expert material, so it is no weaker than current teaching.
- After the delayed test, every student gets the treatment materials before the exam.
- The module is earned by completion, not score. Research consent is separate from credit: non-consenters do the same module and their data are not used. The instructor does not learn who consented.
- K0 codes pretest responses under the Stage B research consent, which is collected before the pretest; non-consenters' pretests are not coded. The consent rate is reported, and K0 describes consenters, who are also the analysed population. If K0 stops Stage B, the module runs as ordinary teaching with the control materials, no research data beyond K0 are analysed, and consenters are told.
- Students' and experts' consent, pseudonymized data and recording consent for experts.
- Transcripts sent to an LLM provider need a data-processing agreement or a locally hosted model.

## Evidence

### Anchors for design choices

| Source | Design | N | Domain | Outcome type | Used for |
|---|---|---|---|---|---|
| Hennink & Kaiser (2022), https://doi.org/10.1016/j.socscimed.2021.114523 | Systematic review of 23 empirical and modelling tests of saturation | 23 studies | Qualitative health and social research; **outside physics and education** | Saturation, not learning | Code saturation was reached at 9–17 interviews in homogeneous samples with narrow aims; "meaning" saturation needed more. Sets expert N = 12, extendable to 16. |
| Guest, Namey & Chen (2020), https://doi.org/10.1371/journal.pone.0232076 | Methods paper, validated by bootstrapping 3 datasets | 3 datasets | Qualitative interviews; **outside physics** | Saturation | Stopping rule (base size, run length, new-information threshold). |
| Fox, Ericsson & Best (2011), https://doi.org/10.1037/a0021663 | Meta-analysis | 94 studies | Lab cognitive tasks; **outside physics** | Reactivity of concurrent reports | Non-directed think-aloud leaves accuracy unchanged but adds time. Describe/explain prompts change (improve) performance, so there is no probing during solving. Retrospective probing was not tested. |
| Lortie-Forgues & Inglis (2019), https://doi.org/10.3102/0013189X19832850 | Review of RCT effect sizes | 141 RCTs, 1,222,024 students | K–12; **not university, not physics** | Standardized achievement | Mean effect 0.06 SD, mean CI width 0.30 SD. Reason not to power for a large effect. |
| Kraft (2020), https://doi.org/10.3102/0013189X20912798 | Methodological review with empirical benchmarks | 747 RCTs, 1,942 effect sizes | Pre-K–12; **not university, not physics** | Standardized achievement only | Cohen's benchmarks are miscalibrated for field education effects, and cost should be weighed. Consistent with a cost-based SESOI; on Kraft's schema d = 0.30 is already "large". |
| Kestin et al. (2025), https://doi.org/10.1038/s41598-025-97652-6 | Crossover RCT, randomized by 2–3-student peer group | 194 | **University physics** | Immediate post-test | Effect 0.63 SD (0.73–1.3 by quantile regression) for a pedagogy-engineered AI tutor over in-class active learning. Immediate only, and a different manipulation: an upper reference, not a power anchor. |
| Feldon et al. (2010), https://doi.org/10.1002/tea.20382 | Controlled, double-blind comparison | 314 | Undergraduate biology; **outside physics** | Withdrawal, lab-report quality (in-course) | Precedent for a CTA-derived vs expert-authored instruction contrast; the control arm here copies it. |

### Physics precedents for teaching principle selection

| Source | Design | N | Domain | Outcome type | Finding |
|---|---|---|---|---|---|
| Dufresne et al. (1992), https://doi.org/10.1207/s15327809jls0203_3 | Three laboratory experiments | Not in abstract | **Physics novices** (population not checked; closed access) | Similarity judgments; problem solving (immediate) | Constraining novices to expert-like, hierarchical, principle-first analyses made their similarity judgments more expert-like and improved problem solving. |
| Heller & Reif (1984), https://doi.org/10.1207/s1532690xci0102_2 | Controlled lab experiments with a prescriptive model | N not verified | **University physics** (mechanics) | Immediate solution quality | Students guided through a model procedure for describing problems in physics terms produced better descriptions and solutions than groups following alternative or partial models (see `explore-expert-novice.md`). |
| Docktor et al. (2015), https://doi.org/10.1103/PhysRevSTPER.11.020106 | Quasi-experiment, 3 schools, class-level assignment | 84 students | **High-school physics** (not university) | Post-instruction tests | Conceptual Problem Solving classes outscored controls by 10–20% on problem-solving and conceptual tests, significant at some schools only. On problem categorization, all groups chose the superficially similar problem more often than the one sharing a principle. |
| Chi, Feltovich & Glaser (1981), https://doi.org/10.1207/s15516709cog0502_2 | Lab studies, expert–novice | Small | **Physics** | Categorization | Novices sort by surface features, experts by principle. Basis for the topic choice and the mechanism check. |
| Singh & Rosengrant (2003), https://doi.org/10.1119/1.1571832 | Instrument development: 25 items plus interviews | Intro physics students | **Physics** | Conceptual understanding | EMCS, a test of energy and momentum concepts; α ≈ 0.75 (calculus-based), 0.68 (algebra-based). Secondary, exploratory. |

### AI-led interviewing (for §9 arm 3)

| Source | Design | N | Domain | Outcome type | Finding |
|---|---|---|---|---|---|
| Chopra & Haaland (2026), https://doi.org/10.65864/ch6grwpore | Working paper (CESifo); multiple interview studies | Not in abstract | Economics respondents; **not experts, not physics** | Interview quality metrics; prediction of behaviour at 6 months | AI-led interviews were thematically richer than other at-scale qualitative methods, mainly because of dynamic probing, and predicted behaviour six months later. |
| Geiecke & Jaravel (2026), https://doi.org/10.2139/ssrn.4974382 | Methods paper with comparison to human experts; DOI is the 2024 SSRN preprint, forthcoming in *Review of Economic Studies* per the 2026 replication package (https://doi.org/10.5281/zenodo.21702419) | Not in abstract | Economics and policy; **not physics** | Quality ratings | AI-led interviews received high ratings across decision-factor, political-view, mental-state and mental-model applications. |
| Wuttke et al. (2025), https://doi.org/10.18653/v1/2025.latechclfl-1.17 | Small randomized comparison, AI vs human interviewer | Small (students) | Political opinion; **not physics** | Guideline adherence, response quality | Data quality was comparable. Error rates were similar, but the kinds of errors differed. |

None of these tests an AI interviewer against **observed task performance**, and none elicits expert problem-solving cognition. They support only feasibility and interview quality. That is why Stage A validates operations against the think-aloud trace rather than against interview richness.

## Against

- **The learning effect may be small.** Large commissioned K–12 RCTs average 0.06 SD on standardized achievement (Lortie-Forgues & Inglis 2019). The closest physics test of teaching expert decision models (instructor-built, not CTA-elicited) found no direct effect (Jeong et al. 2024, https://doi.org/10.1007/s10639-024-12962-y; quasi-experimental, N = 390, small dose; see `explore-cognitive-task-analysis.md`). In Docktor et al. (2015), a 9-item categorization test (each item: pick which of two problems is solved like a model problem) showed no significant advantage for Conceptual Problem Solving (2 schools, n = 54; +2% and +11%), and all groups still favoured surface matches. The authors attribute this to test difficulty, so the Chi-style mechanism check here may be insensitive. Stage B can therefore come back inconclusive even at N ≈ 370. K2 is stated so that a clear null still ends the branch.
- **"Explicitness" confound.** The treatment adds principle-focused content. Principle-first scaffolds have helped novices in two physics studies (Dufresne et al. 1992; Docktor et al. 2015, high school), so a positive Stage B shows that the *elicited* operations help relative to ordinary expert material. It does not show that they beat a *published* strategy template. A third arm with a published template (Docktor-style CPS, or the expert decisions of Burkholder et al. 2020, https://doi.org/10.1103/physrevphyseducres.16.010123) would answer that at about 1.5× N. It is left out as not the smallest test of the stated question; see Open questions.
- **AI-interviewer evidence is off-domain.** All of it comes from opinion and economic interviews, with outcomes of richness and ratings (Chopra & Haaland; Geiecke & Jaravel; Wuttke et al.). None comes from expert cognition or from validation against *task* performance. It justifies trying the arm, not expecting it to work.
- **Known strategies.** If every added operation carries the published-framework tag, a positive Stage B shows that recovering known strategies this course omits helps; it shows nothing new about elicitation.
- **Stage A is small.** With 12 experts the AI–human difference is only estimated. Blinding coders to the interviewer is partial.
- **Transfer is a researcher-written test.** Independent authors and a principles-only specification reduce the alignment problem, but this is not a standardized measure.

## Review (`methods-critic`)

Verdict before fixes: no fatal flaw, six major threats, would not run as designed; with fixes 1–6, would run. All 14 issues were applied above:

1. **Rubric rewarded the taught write-up.** The primary score is now correctness only, and the rubric score is secondary.
2. **K1 could pass without the AI contributing.** Added K1(b): at least 2 AI-probe-added operations, otherwise the claim is restated as trace-based CTA.
3. **Circular "performed" check.** Added decoy operations and a reported false-corroboration rate; the coder is blind to interviewer.
4. **No reliability check on "shared" or on the status tags.** Agreement statistics are now given for segmentation (α), the status tags (κ) and cross-expert matching (κ).
5. **Baseline was narrow and uneven.** The baseline now includes the textbook and lecture notes, and an operation must apply to the explained problems to count as absent.
6. **Dose and contamination could produce a false null.** Added a compliance threshold and a CACE estimate, made K2 conditional on at least 70% compliance, added a contamination question and made the delayed test credited, with a pre-set missing-data rule.

The minor issues were also addressed:
- EMCS is now given at pretest and delayed test and labelled exploratory.
- The K1 contradicted-rate gate uses the CI bound.
- K2 has a defined inconclusive zone.
- The interviewer settings are frozen, both follow the same follow-up rule, and session order is a term in the estimate.
- The transfer items are piloted against a floor effect.
- Power is recomputed with r = .4, giving N ≈ 370.
- Ethics lines were added.
- The categorization task moves after the transfer test.

### Re-review after the P1 branches

Stage B changed after `explore-worked-examples-self-explanation.md` (operations carried by self-explanation prompts), `explore-concept-inventories.md` (EMCS items excluded) and `explore-expert-novice.md` (framework tag, arm × pretest). Verdict: no fatal flaw, five major issues; would run with them fixed. All were applied above:

1. **Prompt type differed between arms.** Both arms now draw from one fixed list of stems in the same proportions; only the steps they attach to differ.
2. **Model answers could turn prompts back into provided explanations.** The operation is performed in a worked step, the prompt asks to justify or apply it, answers are locked before the model answer, blanks do not count, and a 10% sample is scored for attempting the targeted step.
3. **Time and compliance would diverge.** Prompts are piloted to within 10% median time, logged time is a manipulation check, and a compliance failure allows one re-run only.
4. **No expected effect stated; K2 recorded a kill as a null.** The expected effect is stated as likely below the SESOI, Stage B is named a futility test at d = 0.30, the kill is recorded as "below the SESOI", and the pooled rule is stated.
5. **Framework tag and arm × pretest were missing from this note.** Both added, with scope limits.

Minor: dose raised to prompts in at least two of four examples; prompts and model answers count toward the word match; CACE relabelled per-protocol; a "known strategies" caveat added under Against; Heller & Reif (1984) added to the precedents. Still open: list the selected EMCS items in the pre-registration before any data are collected.

### Re-review after the K0 amendment

No past exam scripts will be available, so K0 moved from exam scripts before Stage A to open-response pretest items before Stage B. Verdict: no fatal flaw, five major issues; would run with them fixed. All were applied above:

1. **Pretest timing was unspecified**, so errors from not yet knowing the principle could fail K0. The pretest now follows the course's lectures on the topic and carries completion credit; the uncalibrated threshold is reported with the full error profile.
2. **The 30% had no unit or denominator.** One code per solution on the first substantive error; blank and correct solutions are outside the denominator.
3. **K0 now follows the sunk cost.** Codebook, sampling and decision rule are pre-registered, Stage B materials frozen before the pretest, coders independent of the designer and PI, κ ≥ 0.70.
4. **Stratifying on open-response items would not fit the one-week window.** Randomization stratifies on the closed-response score or midterm.
5. **K0 could test different problems from Stage A's.** K0 items share Stage A's principle structure, and map §5.1 now says the bottleneck is set from the literature and confirmed by K0.

Minor: clustered sampling replaced by one item per student with a Wilson CI; pretest length and delayed-test overlap fixed; consent timing and the fallback if K0 stops; the ordinary-explanation problems named; the premise citation narrowed (also flagged by `citation-verifier`).

### Review of early K0

Early K0 runs the K0 items as a quiz in an earlier offering, so that student data can again stop the study before experts are recruited. Verdict: no fatal flaw, three major issues; would run with them fixed. All were applied above:

1. **An ungraded quiz is weak ground for a stop.** Completion credit where allowed, a defined attempt threshold, attempt and attendance rates reported, and no stop below 100 errored solutions.
2. **Items were not frozen across the two checks.** Items and codebook are registered before the quiz; the Stage B pre-registration cites that record, and later changes are logged deviations.
3. **Items could leak to the Stage B cohort.** Different cohorts, scripts collected, no item solutions released, early-K0 sitters excluded from the pretest K0 sample.

Minor: early-K0 codes may shape examples and prompt placement only, never which operations the treatment carries; a new topic needs its own early K0; disagreement between the checks is reported; stale lines on what K0 can stop corrected.

## Implications for the map

1. **§9 Phase 2.** Under "Measure", add a "Minimal first design" paragraph:
   - early K0 on quiz errors in an earlier offering; Stage A with 12 experts, blind operation coding and validation against the trace; K1 gate; K0 check on pretest errors; Stage B, a two-arm RCT on delayed transfer with SESOI d = 0.30 and about 370 students; K2 with its compliance condition and inconclusive zone.
   - Note that the decoding interview arm is deferred.
   - Link this note.
2. **§9 Phase 2.** Add a **kill criterion** line matching K1, K0 and K2 (Phase 2 has none today).
3. **§14.** Add: Hennink & Kaiser (2022); Guest, Namey & Chen (2020); Lortie-Forgues & Inglis (2019); Kraft (2020); Dufresne et al. (1992); Docktor et al. (2015); Docktor et al. (2016); Singh & Rosengrant (2003); Chopra & Haaland (2026); Geiecke & Jaravel (2026); Wuttke et al. (2025).
4. **No change** to any §4 rating, to §5.1 or to §5.2. The design uses the §5.2 provisional method unchanged.

## Open questions

These are only the ones that would change the design:
- Is the course enrolment at one site at least 370 per offering? If not, Stage B needs two semesters or two sites, and that decides feasibility.
- Should Stage B add a published-strategy arm? That would turn the claim from "better than ordinary expert material" into "better than the best known material" at about 1.5× N.
- Does an item-level validation of EMCS for this population exist? Partly: item-level evidence from one university flags three items, and no item subset is validated, so EMCS stays exploratory (see `explore-concept-inventories.md`).
- Which course offering runs early K0, and does its ethics approval cover a research quiz? Without one, Stage A runs on the literature premise alone.
