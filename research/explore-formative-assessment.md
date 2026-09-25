# Explore: Formative assessment + feedback

**Question:** Does "High as a broad principle" hold for formative assessment once the headline effect sizes are traced to their sources, what does university STEM and physics evidence add, and which feedback properties have enough evidence to fix the AI tutor's feedback policy?

**Verdict: no change to priority (P2); the rating is split.** Two different claims sit under "formative assessment":
- **High** for feedback and low-stakes quizzing as *practices*. Feedback averages d = 0.48 across 435 studies, with high-information feedback (0.99) well above corrective feedback (0.46) and reinforcement (0.24). Classroom quizzing averages g = 0.50 across 222 studies. The effect depends heavily on the kind of feedback, and over a third of feedback interventions lowered performance (Kluger & DeNisi 1996).
- **Low–moderate** for formative assessment as a packaged classroom *intervention*. The widely quoted 0.4–0.7 SD has no quantitative source (Bennett 2011). Rigorous K–12 syntheses find d ≈ 0.20–0.29, and a methods critique says even that is uncertain. Causal evidence at university level is thin, and nothing found measures delayed transfer in a university classroom except a small engineering-course study on feedback timing.

Timing of feedback does not matter on average in computer-based studies (g = 0.03 across 51 studies, few with delays of a day or more), so "immediate feedback" is not a design principle by itself. One university engineering study found delayed feedback improved performance on new exam problems.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline:
- §4 row: P2, "Essential feedback loop for checking whether the intervention actually worked", "High as a broad principle", STEM fit High, humanities High, AI readiness High.
- There is **no §5 card** for formative assessment. The decision tree (§3 D) names "Formative / diagnostic assessment".
- §5.6 already cites Lichtenberger et al. (2024): diagnosis without a response did not help; a formative-assessment package did.

It serves §9 Phase 3 (instructional utility of diagnosis) and Phase 4 (every intervention arm gives feedback), and the tutor's feedback policy in §5.9 and §5.12.

Search: the OpenAlex REST API returned HTTP 429 on the one attempt, and the `openalex` MCP server was not loaded. Search used:
- the Crossref API for metadata and abstracts;
- the ERIC API;
- one Semantic Scholar call (rate-limited) and Semantic Scholar record pages;
- WebSearch;
- publisher pages.

Full text was read for Wisniewski, Zierer & Hattie (2020, Frontiers), Klute, Apthorp, Harlacher & Reale (2017, ERIC full text) and Mullet et al. (2014, author-hosted PDF). Everything else comes from abstracts, marked below. The Zotero local API returned no items for "formative" or "feedback".

## Evidence

### Where the famous effect sizes come from

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Black & Wiliam (1998), https://doi.org/10.1080/0969595980050102 | Narrative review | About 250 sources | Mixed, mostly school | Mixed | The founding review. It reports no meta-analysis or quantitative estimate of its own. |
| Bennett (2011), https://doi.org/10.1080/0969594X.2010.513678 | Critical review | — | — | — | The 0.4–0.7 SD often attributed to Black & Wiliam appears only in their pamphlet and position paper, with no source given; it is not a result of the 1998 review. Also flags a vague definition of formative assessment and weak causal designs in the underlying studies (abstract read via OpenAlex: claims derive "from untraceable, flawed, dated, or unpublished sources"; "no source for those values is ever given" is body text quoted in secondary sources; full text not read). |
| Kingston & Nash (2011), https://doi.org/10.1111/j.1745-3992.2011.00220.x | Meta-analysis | Over 300 studies screened; 13 usable, 42 effect sizes | K–12 | Achievement | "An effect size of about 0.70 (or 0.40–0.70) is often claimed … but is not supported". Weighted mean d = 0.20 (median 0.25). ELA 0.32, mathematics 0.17, science 0.09. Professional-development-based and computer-based formative systems did best (0.30, 0.28). |
| Briggs, Ruiz-Primo, Furtak, Shepard & Yin (2012), https://doi.org/10.1111/j.1745-3992.2012.00251.x | Methods critique | — | — | — | Study selection, inclusion criteria, biased effect sizes and outcome-measure characteristics make Kingston & Nash's 0.20 "somewhat equivocal"; "considerable uncertainty remains". |
| Klute, Apthorp, Harlacher & Reale (2017), ERIC ED572929 (REL Central) | Systematic review with WWC-style quality screen | 76 studies rated; 23 met standards; 19 gave effect sizes | Grades 1–6; **not university** | Achievement | Unweighted mean ES 0.26 (range −0.46 to 1.22). Mathematics 0.36, reading 0.22, writing 0.21. Formative assessment directed by a teacher or computer program beat student-directed formative assessment on average (0.29 vs 0.20), reversed in maths (student-directed 0.45 vs other-directed 0.30). |
| Lee, Chung, Zhang, Abedi & Warschauer (2020), https://doi.org/10.1080/08957347.2020.1732383 | Systematic review with meta-regression | 33 studies, 126 effect sizes | US K–12; **not university** | Learning | Overall d = 0.29. Student-initiated self-assessment (0.61), formal evidence such as written feedback on quizzes (0.40) and medium cycles within or between units (0.52) raised effects. |

So the rigorous estimates for formative assessment as an intervention cluster around 0.2–0.3 SD in schools, with wide spread and contested methods. That is a small-to-moderate effect by education benchmarks, not "high".

### Feedback as a practice

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Kluger & DeNisi (1996), https://doi.org/10.1037/0033-2909.119.2.254 | Meta-analysis | 607 effect sizes, 23,663 observations | Mixed laboratory and field tasks, education and work settings | Task performance | Feedback interventions improved performance on average (d = 0.41), but over one-third of them **lowered** performance. Effectiveness fell as feedback moved attention from the task towards the self. |
| Hattie & Timperley (2007), https://doi.org/10.3102/003465430298487 | Conceptual review and meta-synthesis | — | Education | Achievement | Feedback "is among the major influences", but its impact "can be either positive or negative". Proposes four levels: task, process, self-regulation and self. The meta-synthesis average (0.79) was later re-estimated at 0.48 from the primary studies; Wisniewski et al. (2020) attribute the gap to double-counted studies and unweighted, fixed-effect synthesis. |
| Wisniewski, Zierer & Hattie (2020), https://doi.org/10.3389/fpsyg.2019.03087 | Meta-analysis of primary studies drawn from earlier meta-analyses | 435 studies, 994 effect sizes, N > 61,000 | Kindergarten to university | Cognitive, motivational, physical, behavioural | d = 0.48 after removing extreme values; I² = 83%. Controlled studies 0.42, pre–post studies 0.63; journals 0.49, dissertations 0.36. By type: reinforcement or punishment 0.24 (k = 39), corrective feedback 0.46 (k = 238), **high-information feedback 0.99** (k = 42). Cognitive outcomes 0.51, motivational 0.33. |
| Shute (2008), https://doi.org/10.3102/0034654307313795 | Narrative review | — | Mixed | — | Formative feedback should be "nonevaluative, supportive, timely, and specific"; effects interact with learner characteristics and the task. |

### Computer-based feedback: content and timing

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Van der Kleij, Feskens & Eggen (2015), https://doi.org/10.3102/0034654314564881 | Meta-analysis | 40 studies, 70 effect sizes | Computer-based, mixed levels | Learning outcomes, lower vs higher order | Elaborated feedback (an explanation) 0.49; correct answer shown 0.32; right/wrong only **0.05**. Elaborated feedback was especially better for higher-order outcomes. Delayed timing had a negative effect overall; no significant timing × outcome-level interaction. |
| Mertens, Finn & Lindner (2022), https://doi.org/10.1037/edu0000764 | Network meta-analysis | 77 studies, 163 effect sizes (secondary summaries; not verified from the paper) | Computer-based feedback | Lower- and higher-order performance | Ranked elaborated feedback above answer-until-correct feedback; both beat no feedback (abstract not retrieved; secondary summaries only). |
| Heckler & Mikula (2016), https://doi.org/10.1103/PhysRevPhysEducRes.12.010134 | Full factorial experiments | Over 450 university students | **University introductory physics** (vector maths) | Immediate post-training scores; training time | Elaborated feedback (a general explanation) was the most effective, especially for students with low prior knowledge and low course grades. Correct-answer feedback was less effective for low performers, and adding it to elaborated feedback gained nothing. Elaborated feedback took longer, so the learning rate was at best marginally higher. |
| Kandemir, Esposito, Gurgand & Ramus (2026), https://doi.org/10.1007/s10648-026-10117-8 | Meta-analysis (robust variance estimation) | 51 studies, 160 effect sizes, 1988–2024 | Computer-assisted learning | Learning outcomes | Immediate vs delayed feedback: **g = 0.03**, 95% CI [−0.08, 0.13]. Educational level, domain and response-time limits moderate it. Few studies used delays of a day or more. |
| Mullet, Butler, Verdin, von Borries & Marsh (2014), https://doi.org/10.1016/j.jarmac.2014.05.001 | Two classroom experiments: between sections (Exp. 1), within students across materials (Exp. 2) | 26 consented, 24 analysed (Exp. 1); 50 consented, 36 analysed (Exp. 2) | **University** upper-level engineering (signals and systems) | Course exams with **new problems** on the same concepts | Homework feedback delayed by one week beat feedback released at the deadline on later exams (Exp. 1: 0.92 vs 0.84, d = 0.75, p = .04). Students believed immediate feedback helped them more. Exp. 1 assigned by section (quasi-experimental); Exp. 2 replicated the delay benefit with timing alternated within students across weekly topics (F(1, 34) = 4.79, p = .036). |

### Low-stakes quizzing (retrieval practice) as formative assessment

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Yang, Luo, Vadillo, Yu & Shanks (2021), https://doi.org/10.1037/bul0000309 | Meta-analysis of classroom studies | 222 studies, 48,478 students | Classrooms, all levels | Academic achievement | g = 0.50. Moderated by the control condition, format match between quiz and test, material match, corrective feedback, repetitions and timing. |
| Adesope, Trevisan & Sundararajan (2017), https://doi.org/10.3102/0034654316689306 | Meta-analysis | 272 effect sizes, 188 experiments; g = 0.51 vs restudy, 0.93 vs filler or no activity (secondary summary) | Mixed | Final-test performance | Practice tests beat restudying and all other comparison conditions; effects moderated by test features, participants and outcome construct (abstract; numbers not extracted). |
| Pan & Rickard (2018), https://doi.org/10.1037/bul0000151 | Meta-analysis | 192 transfer effect sizes, 122 experiments, N = 10,382 | Mixed, mostly lab | **Transfer** | d = 0.40 [0.31, 0.50] for transfer from testing. Weakest for problems involving worked examples. After PET-PEESE and selection-model corrections, intercepts often indicated **no positive transfer** unless specific conditions (response congruency, elaborated retrieval) held. |
| Wooldridge, Bugg, McDaniel & Liu (2014), https://doi.org/10.1016/j.jarmac.2014.07.001 | Instructor survey plus two experiments | Not extracted | College biology textbook material | Final test with identical vs related items | Quizzing gave the usual benefit on repeated items but **no significant benefit on topically related items**, which is how instructors usually quiz (abstract via search summary). |

### University STEM and physics: peer instruction and formative questions

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Crouch & Mazur (2001), https://doi.org/10.1119/1.1374249 | Ten-year cohort comparison, not randomized | Harvard cohorts 1990–2000, 117–246 per year (1,624 total); traditional comparison cohorts only 1990 (N = 121, no pretest) and 1999 (N = 129) | **University physics** | Conceptual (FCI) and quantitative problem solving, end of course | Peer Instruction (in-class ConcepTests, vote, discuss, revote) increased conceptual mastery and quantitative problem solving; later refinements added further gains. |
| Lasry, Mazur & Watkins (2008), https://doi.org/10.1119/1.2978182 | Cohort comparison, two institutions | Not verified (full text paywalled) | **University** and two-year college physics | FCI, problem solving, attrition | Replicated better conceptual learning and similar problem solving; PI students with less background gained as much as better-prepared students under traditional teaching; attrition fell. |
| Smith, Wood, Adams, Wieman et al. (2009), https://doi.org/10.1126/science.1165919 | Within-class design with an isomorphic follow-up question | About 350 students (secondary summaries; full text not read) | **University** genetics | Isomorphic question answered individually (immediate) | Peer discussion improved answers on a new, isomorphic question, even when no one in the group had first answered correctly: the gain is understanding, not copying. |
| Vickrey, Rosploch, Rahmanian, Pilarz & Stains (2015), https://doi.org/10.1187/cbe.14-11-0198 | Literature review | — | Physics, biology, chemistry, computer science (university) | — | Summarises PI research and a research-based implementation model; instructors often adapt the practice in ways that compromise it. |
| Morris, Perry & Wardle (2021), https://doi.org/10.1002/rev3.3292 | Systematic review of trials | Not extracted | **Higher education** | Learning | "The evidence base is currently limited". Low-stakes quizzing is "particularly powerful"; peer and tutor feedback help depending on implementation; evidence for praise, grading and technology-based feedback is mixed. |
| Lichtenberger et al. (2024), https://doi.org/10.1007/s11092-024-09445-6 (already in the map) | Cluster RCT | 29 teachers, 604 students | Upper-secondary kinematics; **not university** | Concept test, immediate and 3 months | Teachers who used the same concept questions without the formative-assessment training and tools did not significantly beat traditional teaching; the formative-assessment package did (at 3 months, d = 0.39 vs concept questions alone, d = 0.62 vs traditional teaching). See `explore-concept-inventories.md`. |

The physics evidence for Peer Instruction comes from cohort comparisons on concept inventories and course measures. The only university classroom study found with a delayed, new-problem outcome from a formative practice is Mullet et al. (2014), in engineering, on feedback *timing*; Smith et al. (2009) shows immediate near transfer to an isomorphic question (genetics), and Wooldridge et al. (2014) found no quizzing benefit on related items with college textbook material.

## Against

- **The headline number has no source.** The 0.4–0.7 SD is not a meta-analytic result (Bennett 2011). Rigorous school estimates are 0.20–0.29 (Kingston & Nash 2011; Klute et al. 2017; Lee et al. 2020), and even those are contested (Briggs et al. 2012). Science was the weakest subject in Kingston & Nash (0.09).
- **Feedback can hurt.** More than a third of feedback interventions lowered performance (Kluger & DeNisi 1996). Reinforcement-type feedback averages 0.24 and right/wrong feedback on computer 0.05 (Wisniewski et al. 2020; Van der Kleij et al. 2015).
- **Inflation by design.** Pre–post studies give larger feedback effects than controlled ones (0.63 vs 0.42), and journals larger than dissertations (0.49 vs 0.36) (Wisniewski et al. 2020).
- **Quizzing transfers weakly.** Transfer from retrieval practice shrinks towards zero after publication-bias correction unless specific conditions hold, and is weakest for worked-example problems (Pan & Rickard 2018); related-item benefits were not found with authentic materials (Wooldridge et al. 2014).
- **Timing is not a lever by itself.** No average difference between immediate and delayed feedback in computer-assisted learning, where few studies used delays of a day or more (Kandemir et al. 2026). The one university classroom result favours a one-week *delay*, in a small engineering course: between sections in Exp. 1 (n = 24) and within students in Exp. 2 (n = 36) (Mullet et al. 2014).
- **University causal evidence is thin.** The higher-education review calls the base "limited" (Morris et al. 2021). Peer Instruction evidence is cohort comparisons (Crouch & Mazur 2001; Lasry et al. 2008).

Held against §11: the strong numbers are for feedback and quizzing on immediate or same-item outcomes. Only one small university classroom study measured performance on new problems after a delay (Mullet et al. 2014); the other near-transfer evidence is immediate (Smith et al. 2009) or null (Wooldridge et al. 2014). Diagnosis without a response did not help (Lichtenberger et al. 2024), which matches §9 Phase 3's focus on instructional utility.

## Implications for the map

1. **§4 Formative assessment row, evidence cell.** Replace "**High as a broad principle**" with:
   > **High for feedback and quizzing as practices** (feedback d ≈ 0.48, over a third of feedback effects negative; classroom quizzing g ≈ 0.5); **low–moderate for formative assessment as a packaged intervention** (rigorous school estimates d ≈ 0.2–0.3; the quoted 0.4–0.7 has no source); little causal university evidence

   Keep the other cells.

2. **New §5.13 card**, after §5.12 (so no other card is renumbered):
   > ## 5.13 Formative Assessment + Feedback — **the loop that checks whether instruction worked**
   >
   > ### What it is
   > Gathering evidence of what a learner currently understands during instruction and using it to adjust the next step, for the teacher, the tutor or the learner. Feedback is the learner-facing part; low-stakes quizzing and in-class concept questions are common vehicles.
   >
   > ### Why it matters
   > Diagnosis only helps when it drives a response (§5.6, Lichtenberger et al. 2024). This card is about what that response should look like.
   >
   > ### Evidence / limitations
   > Graded evidence (see `research/explore-formative-assessment.md`):
   > - **Packaged formative assessment is smaller than its reputation.** The quoted 0.4–0.7 SD has no quantitative source (Bennett 2011). Rigorous school estimates are d = 0.20 (Kingston & Nash 2011; science 0.09), 0.26 (Klute et al. 2017) and 0.29 (Lee et al. 2020), with contested methods (Briggs et al. 2012).
   > - **Feedback works when it carries information.** d = 0.48 overall; reinforcement 0.24, corrective 0.46, high-information 0.99 (Wisniewski et al. 2020). On computers, elaborated feedback 0.49 vs right/wrong 0.05 (Van der Kleij et al. 2015). In university physics, elaborated feedback helped most for low-prior-knowledge students (Heckler & Mikula 2016). More than a third of feedback interventions lowered performance (Kluger & DeNisi 1996).
   > - **Timing is not a lever by itself.** Immediate vs delayed: g = 0.03 across 51 computer-based studies, few with delays of a day or more (Kandemir et al. 2026). Delayed homework feedback improved exam performance on new problems in one small university engineering course, in two experiments (Mullet et al. 2014).
   > - **Low-stakes quizzing helps in classrooms** (g = 0.50, 222 studies; Yang et al. 2021), but transfer is weak once publication bias is corrected (Pan & Rickard 2018) and may not reach related items (Wooldridge et al. 2014).
   > - **University physics:** Peer Instruction improves conceptual scores in cohort comparisons (Crouch & Mazur 2001; Lasry et al. 2008); discussion improves answers to new isomorphic questions (Smith et al. 2009, genetics). Causal higher-education evidence is limited (Morris et al. 2021).
   > - **Transfer:** one small university classroom study with new exam problems (Mullet et al. 2014, engineering); immediate near transfer to isomorphic questions in genetics (Smith et al. 2009); no delayed-transfer study in physics.
   >
   > ### AI opportunity
   > The tutor's feedback policy has better evidence than most of its other choices:
   > - elaborated, task- and process-level feedback that explains why, not right/wrong alone and not praise or comments about the person;
   > - more explanation for learners with low prior knowledge, less for strong ones (Heckler & Mikula 2016; cf. expertise reversal, §5.8);
   > - an attempt before any feedback, with answers withheld until then (§5.9, Bastani et al. 2025);
   > - timing chosen by design and tested, not assumed to be "as fast as possible";
   > - quizzes with varied items, not only repeats of practised ones, and judged on transfer.
   >
   > ### Questions to research next
   > - Does elaborated feedback from an LLM tutor improve delayed transfer in physics, or only the next answer?
   > - Does delaying feedback on physics homework improve transfer, as it did in engineering (Mullet et al. 2014)?
   > - Which feedback content (principle, condition check, worked step) best carries a decoded expert operation to the learner?
   >
   > ### Deep-dive reading if this branch is selected
   > Wisniewski, Zierer & Hattie (2020), **"The Power of Feedback Revisited."** https://doi.org/10.3389/fpsyg.2019.03087

3. **§9 Phase 4.** After "Randomize or counterbalance where feasible. …", add:
   > Hold feedback constant across arms (elaborated, same timing) and report it; average effects of computer-based feedback range from 0.05 (right/wrong) to 0.49 (elaborated) across studies (Van der Kleij et al. 2015), so arms that differ in feedback would confound the comparison.

   This is forced: Phase 4 compares interventions that each give feedback, and the size of the feedback-type moderator is comparable to the effects Phase 4 is trying to detect. Stage B already meets it: both arms show equal-length model answers after a locked attempt, which is elaborated feedback on the same schedule.

4. **§11.** Add:
   > - Do **not** assume more or faster feedback is better; over a third of feedback interventions lowered performance, and in computer-based studies immediate vs delayed feedback makes no difference on average (few used delays of a day or more).

5. **§12.** No change.

6. **§14.** Add:
   - Black & Wiliam (1998) — assessment and classroom learning: https://doi.org/10.1080/0969595980050102
   - Bennett (2011) — formative assessment, a critical review: https://doi.org/10.1080/0969594X.2010.513678
   - Kingston & Nash (2011) — formative assessment meta-analysis: https://doi.org/10.1111/j.1745-3992.2011.00220.x
   - Briggs et al. (2012) — critique of the Kingston & Nash meta-analysis: https://doi.org/10.1111/j.1745-3992.2012.00251.x
   - Klute et al. (2017) — formative assessment in elementary grades, REL Central: ERIC ED572929
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

## Open questions

These are only the ones that would change the verdict:

- Is there a randomized university-physics study of a formative-assessment or feedback intervention with a **delayed transfer** outcome? A positive result would lift "little causal university evidence"; a null would narrow the card to immediate performance.
- Does elaborated feedback beat correctness-only feedback on delayed transfer, not only on immediate scores? The meta-analyses mix outcome timings (Van der Kleij et al. 2015 did not separate delayed transfer).
- Does the Mullet et al. (2014) delayed-feedback benefit replicate with randomized assignment in a physics course? If so, the tutor's default timing should change.
