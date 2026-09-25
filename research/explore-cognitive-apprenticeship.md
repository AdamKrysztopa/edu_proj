# Explore: Cognitive Apprenticeship

**Question:** Which parts of cognitive apprenticeship (modelling, coaching, scaffolding, articulation, reflection, exploration, fading) have causal evidence, how should scaffolding be faded, and when should modelling give way to the learner's own problem solving?

**Verdict: no change to priority (P1) or rating ("Moderate"); the rating is scoped.** No controlled test of the whole model in university physics was found, and whole-model work in health sciences is mostly design and perception studies. The components have experimental support in their own literatures: modelling through worked examples and articulation through self-explanation (§5.8), and computer-based scaffolding in STEM (g = 0.46 over 144 studies). Fading is the weakest part. Fixed-schedule fading did worse than no fading in the pilot meta-analysis (Belland et al. 2015), and the full meta-analysis found no moderation by whether or how scaffolds changed, including performance-adapted change (Belland et al. 2017); support for learner-adapted fading comes from two primary studies outside physics (Salden et al. 2010; Kalyuga & Sweller 2005). The order of modelling and struggle is contested. In university physics, problem solving before instruction improved conceptual scores in single-lesson randomized studies (DeCaro et al. 2023, N = 78; Bego et al. 2022, Experiment 1, N = 129, which also found higher transfer) and in two classroom studies (Weaver et al. 2018), all from one research group; a Bego et al. experiment without contrasting cases (N = 92) found no difference. Explicit instruction first won for young learners and high element interactivity.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 row (P1, "Moderate", STEM fit High, humanities High, AI readiness Very high) and the §5.7 card with its three open questions: how to fade automatically, when modelling should stop and productive struggle begin, and which components have the strongest causal evidence. The branch serves §9 Phase 4 ("expert modelling", "guided practice" and "Socratic questioning" are listed interventions), Phase 5 (tutoring policies) and §10 RQ4 and RQ8.

Search: the OpenAlex REST API returned HTTP 429 on the one attempt, and the `openalex` MCP server was not loaded. The Semantic Scholar API was also rate-limited for most queries. Search used the Crossref and ERIC APIs, one Semantic Scholar batch call, publisher pages and WebSearch. Full text was read for Ding et al. (2011), Schwartz et al. (2011) and DeCaro et al. (2023); the citation check later read Salden et al. (2010), Kapur (2008), Ashman et al. (2020, author preprint) and Belland et al. (2017, open access in PMC) in full. Weaver et al. (2018) comes from its abstract only (N and assignment not reached), and Heller, Keith & Anderson (1992) from its title only, so Heller is not used for a claim below. Dennen & Burner (2008), a handbook review of the model, has no DOI in Crossref and was not reached. The Zotero local API holds nothing on apprenticeship, scaffolding or fading.

## Evidence

### Is there causal evidence for the whole model?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Collins, Brown & Newman (1989; Routledge reissue 2018), https://doi.org/10.4324/9781315044408-14 | Theory, with three exemplar programmes (reciprocal teaching of reading, procedural facilitation of writing, Schoenfeld's mathematical problem solving) | — | Reading, writing, mathematics | — | Defines the model: content, methods (modelling, coaching, scaffolding, articulation, reflection, exploration), sequencing and sociology. Its evidence is the exemplar programmes, not a test of the model as a whole. |
| Lyons, McLaughlin, Khanova & Roth (2017; online 2016), https://doi.org/10.1007/s10459-016-9707-4 | Qualitative review | 104 articles, 26 synthesised in depth | Health sciences (nursing, medicine, veterinary) | — | Use of the theory concentrates on the methods dimension (coaching, mentoring, scaffolding); it mostly informs instructional design and instrument development. No pooled outcome. |
| Stalmeijer, Dolmans, Wolfhagen & Scherpbier (2009; online 2008), https://doi.org/10.1007/s10459-008-9136-0 | Focus groups | 21 sixth-year medical students | Clinical training | Perceptions | Students recognised the six teaching methods in clinical practice and judged them conducive to learning. Perception data only. |
| Etkina et al. (2010), https://doi.org/10.1080/10508400903452876 | Classroom comparison (design labs vs non-design labs within ISLE) | Not in abstract | **University introductory physics** labs, described as "cognitive apprenticeship enhanced by formative assessment" | Traditional exams; novel experimental tasks | Equal on traditional exams; the design group outperformed on novel experimental tasks in physics and biology. Not randomized as far as the abstract shows, and it tests design-plus-reflection labs, not the model's modelling-to-fading sequence. |

No randomized or quasi-experimental test of the full model in university physics was found. The model is used as a design vocabulary, and its evidence runs through the components.

### Scaffolding and fading

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Belland, Walker, Kim & Lefler (2017), https://doi.org/10.3102/0034654316670999 | Meta-analysis (random effects) of experimental studies | 144 studies, 333 outcomes | Computer-based scaffolding in problem-centred STEM curricula, primary to adult | Cognitive outcomes | g = 0.46, consistently positive across contexts. Effects were largest at the principles level and among adult learners. The effect **did not vary with the presence or absence of scaffolding change (fading or adding)**, nor with the logic of the change. |
| Belland, Walker, Olsen & Leary (2015), Educational Technology & Society 18(1), 183–197, no DOI; ERIC EJ1062484 | Pilot meta-analysis | Not in abstract | Computer-based scaffolding, STEM, secondary to adult | Cognitive outcomes | g = 0.53. Studies with **no fading had higher effects than studies with fixed fading**; fading explained 30% of the variance. Conceptual scaffolds beat metacognitive ones. |
| van de Pol, Volman & Beishuizen (2010), https://doi.org/10.1007/s10648-010-9127-6 | Narrative review | — | Teacher–student interaction | — | Contingency, fading and transfer of responsibility are the three defining features. Effectiveness studies were few; measurement is the main problem. |
| van de Pol, Volman, Oort & Beishuizen (2015), https://doi.org/10.1007/s11251-015-9351-z | Classroom experiment | 30 teachers, 768 students aged 12–15 | Social studies, pre-vocational; **outside physics and outside university** | Achievement, effort, appreciation | Contingent support helped achievement only when students had long independent working time; with frequent help, low-contingency support did better. "Scaffolding, thus, is not unequivocally effective." |
| Puntambekar & Hübscher (2005), https://doi.org/10.1207/s15326985ep4001_1 | Conceptual critique | — | Scaffolding tools | — | Software and curricula called "scaffolds" often drop ongoing diagnosis, calibrated support and fading, the features that made tutor scaffolding work. |
| Wood, Wood & Middleton (1978), https://doi.org/10.1177/016502547800100203 | Experiment, four tutoring strategies | Not in abstract | 3–4-year-olds, construction task; **far outside the target population** | Task mastery | The origin of "contingent" tutoring: more help after failure, less after success. |
| Renkl, Atkinson, Maier & Staley (2002), https://doi.org/10.1080/00220970209599510 | Quasi-experimental field study (two classes) and two lab experiments; fading vs example–problem pairs | Field: Grade 9 low-track German pupils (20 per ERIC; 15 + 20 per Renkl & Atkinson 2003); labs: 54 and 45 US college students | Field: **school physics (electricity)**; labs: probability | Near and far transfer; field posttest 2 days later | Fading fostered near transfer; "the far transfer issue is less clear". |
| Salden, Aleven, Schwonke & Renkl (2010), https://doi.org/10.1007/s11251-009-9107-8 | Lab experiment (randomized) and classroom experiment (assigned from a list sorted by prior grade) | Lab: 57 German 9th–10th graders; classroom: 51 US 9th graders, heavy attrition (20 completed all tests) | Geometry Cognitive Tutor (angles), secondary; **outside physics and outside university** | Immediate and delayed posttests (1 week lab; 3 weeks classroom) | Lab: adaptive fading beat fixed fading and problem solving on the immediate (d = 0.49) and delayed (d = 0.59) posttests. Classroom: no immediate differences; adaptive fading beat both on the delayed posttest. Fixed fading did not differ from tutored problem solving in either experiment. |
| Kalyuga & Sweller (2005), https://doi.org/10.1007/BF02504800 | Experiment, yoked control | Not in abstract | Elementary algebra tutor; **outside physics** | Knowledge gain, efficiency | Instruction adapted with rapid knowledge tests and cognitive-load measures gave higher knowledge and efficiency gains than the same sequence without adaptation. |

Fading has two findings, and they do not fully agree. In the pilot meta-analysis, fading on a fixed schedule did worse than leaving scaffolds in place (Belland et al. 2015); in the full meta-analysis, neither the presence of scaffold change nor its logic (none, fixed, performance-adapted, self-selected) moderated the effect (Belland et al. 2017). Two primary studies favour fading tied to the individual learner: adaptive fading beat fixed fading in a Geometry Cognitive Tutor on 1- and 3-week delayed posttests, though the classroom replication showed no immediate difference and had heavy attrition (Salden et al. 2010), and an algebra tutor adapted by rapid knowledge tests beat a yoked, non-adapted sequence (Kalyuga & Sweller 2005). Both are outside physics.

### When should modelling give way to struggle?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Kirschner, Sweller & Clark (2006), https://doi.org/10.1207/s15326985ep4102_1 | Argument and review | — | General | — | Minimally guided instruction is less effective than strongly guided instruction; the advantage of guidance recedes only with high prior knowledge. |
| Hmelo-Silver, Duncan & Chinn (2007), https://doi.org/10.1080/00461520701263368 | Response | — | Problem-based and inquiry learning | — | PBL and inquiry learning are heavily scaffolded and should not be grouped with unguided discovery. |
| Alfieri, Brooks, Aldrich & Tenenbaum (2011), https://doi.org/10.1037/a0021017 | Two meta-analyses | 164 studies (580 and 360 comparisons) | Mixed | Mixed | Unassisted discovery lost to explicit instruction (d = −0.38). Enhanced or assisted discovery beat other instruction (d = 0.30). |
| Lazonder & Harmsen (2016), https://doi.org/10.3102/0034654315627366 | Meta-analysis | 72 studies | Inquiry-based learning, mixed ages | Learning activities, performance, learning outcomes | Guidance helped learning outcomes (d = 0.50); type of guidance moderated performance success but not learning outcomes. |
| Sinha & Kapur (2021), https://doi.org/10.3102/00346543211019105 | Meta-analysis | 53 studies, 166 comparisons | Mixed, mostly mathematics and science | Mixed | Problem solving then instruction (PS-I) beat instruction then problem solving (I-PS), g = 0.36 [0.20, 0.51]; 0.37–0.58 with high fidelity to Productive Failure; 0.87 after publication-bias adjustment. I-PS was favoured for Grades 2–5 and for domain-general skills. |
| Loibl, Roll & Rummel (2017), https://doi.org/10.1007/s10648-016-9379-x | Review and theory | — | PS-I studies | — | PS-I helps only when it uses contrasting cases or instruction that builds on students' own solutions. |
| Darabi, Arrington & Sayilir (2018), https://doi.org/10.1007/s11423-018-9579-9 | Meta-analysis | 12 experimental studies | Productive failure and failure-driven memory | Mixed | Moderately positive; the small number of experiments is itself a finding. |
| Kapur (2008), https://doi.org/10.1080/07370000802212669 | Randomized at group level: 103 triads, randomized within each of 7 schools | 309 | **Grade 11 physics** (Newtonian kinematics), India, text-chat collaboration; the unit had already been taught | Individual well-structured (near) and ill-structured (far, within kinematics) post-tests, same study period | Groups given ill-structured problems produced poorer group solutions but outperformed well-structured groups on both individual post-tests. The manipulation is problem structure after instruction, not instruction order. |
| Schwartz, Chase, Oppezzo & Chin (2011), https://doi.org/10.1037/a0025140 | Two experiments | 128 and 120 | **Grade 8 physics** (density, speed; ratio structure) | Word problems; transfer to unrelated ratio phenomena | Tell-then-practise and invent-with-contrasting-cases were equal on word problems. Inventing first produced better learning of the ratio structure and more transfer (e.g. to spring constant), for low and high achievers. Transfer tests were delayed (21 days in Experiment 1, 1 week in Experiment 2). |
| Weaver, Chastain, DeCaro & DeCaro (2018), https://doi.org/10.1016/j.cedpsych.2017.12.003 | Two classroom studies (different semesters, courses, instructors), explore-first vs instruct-first; assignment not reached | Not reached | **University physics** | Instructor-made quiz, conceptual and procedural items | Explore-first students struggled as much or more on the activity but showed better conceptual and equal procedural knowledge (abstract). |
| Bego, Chastain & DeCaro (2022), https://doi.org/10.1111/bjep.12555 | Two experiments, explore-first vs instruct-first (random assignment stated for Experiment 1 by DeCaro et al. 2023) | 129; 92 | **University physics** | Procedural, conceptual and transfer items (timing not verified) | Experiment 1, activity with contrasting cases: equal procedural knowledge, higher conceptual knowledge and transfer. Experiment 2, activity with a rich dataset instead: no difference. |
| DeCaro, Isaacs, Bego & Chastain (2023), https://doi.org/10.3389/feduc.2023.1215975 | Randomized to condition (conditions on separate class days), same materials in reverse order | 78 | **University physics** (gravitational field, synchronous online) | Posttest taken online after class, before the next class, graded for effort; no transfer measure | Explore-first scored lower on the activity but higher on the posttest (76% vs 66%, ηp² = 0.07). The condition × subscale interaction was not significant (p = .164); the conceptual subscale alone was 69% vs 63% with overlapping intervals. |
| Ashman, Kalyuga & Sweller (2020), https://doi.org/10.1007/s10648-019-09500-5 | Two fully randomized experiments | 64 and 71 | Year 5 (primary), light energy efficiency; **not university** | Similar and transfer problems | Explicit instruction first was better on similar problems (both experiments) and, when element interactivity was raised, on transfer too. |

The pooled evidence favours a structured exploration phase before instruction for conceptual and transfer outcomes, with conditions: contrasting cases or instruction built on students' attempts (Loibl et al. 2017), learners beyond early primary school, and not for domain-general skills (Sinha & Kapur 2021). The university-physics evidence comes from one research group: two classroom studies (Weaver et al. 2018; higher conceptual, equal procedural scores), two experiments (Bego et al. 2022; with contrasting cases, higher conceptual knowledge and transfer, N = 129; with a rich dataset instead, no difference, N = 92) and one small online randomized lesson with an end-of-class posttest (DeCaro et al. 2023, N = 78). The counter-result (Ashman et al. 2020) is primary-school and ties the reversal to element interactivity, which is high in multi-principle mechanics problems.

### Scaffolding in university physics problem solving

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Ding, Reay, Lee & Bao (2011), https://doi.org/10.1103/physrevstper.7.020109 | Study 2: groups formed by recitation section (cluster); Study 3: three parallel classes assigned to treatments | Study 2: 360 (143 / 109 / 108); Study 3: 92 / 82 / 90 | **University** calculus-based mechanics | Study 2: one scaffolded test (immediate). Study 3: final-exam synthesis problem 4 days after a 2-week training, no scaffolding | Two conceptual questions before a two-concept "synthesis" problem helped students search for and apply the right principles. In Study 3 the scaffolded class did better on the exam problem's **untrained** topic (linear momentum; consideration p = 0.002, expansion p = 0.04) than the control; unscaffolded synthesis practice did not. Classes had different instructors, so Study 3 is quasi-experimental, and its p-values are student-level χ² tests with one class per arm, ignoring clustering. |
| Pol, Harskamp, Suhre & Goedhart (2008), https://doi.org/10.1007/s10956-008-9110-x | Qualitative analysis of an earlier experiment | Not in abstract | Secondary physics, student-controlled hint program | Strategic knowledge | Gains came from more effective practice time and systematic use of episode-related hints. |
| Ryan, Frodermann, Heller, Hsu & Mason (2016), https://doi.org/10.1103/physrevphyseducres.12.010105 | Design and usability studies | — | **University** introductory physics, computer coaches built on a cognitive-apprenticeship framework | Usability | Design paper; no learning-outcome comparison. |

Ding et al. (2011) is the closest physics evidence for scaffold-then-remove: a brief conceptual scaffold during training, then an unscaffolded exam problem days later with a cross-topic gain. It is one course, class-level assignment and one exam item.

## Against

- **No whole-model test.** Nothing found compares cognitive apprenticeship as a sequence against a matched alternative in university physics, with any outcome. The health-sciences literature is design and perception work (Lyons et al. 2017; Stalmeijer et al. 2009).
- **Fixed fading of computer-based scaffolds does not beat leaving them in place.** Scheduled fading did worse than unfaded scaffolds in the pilot (Belland et al. 2015); in the full meta-analysis neither the presence nor the logic of scaffold change (fixed, performance-adapted, self-selected) moderated the effect (Belland et al. 2017). Fixed fading of worked-example steps differs: backward fading beat example–problem pairs on near transfer, including in a Grade 9 physics field study (Renkl et al. 2002), but fixed fading did not beat tutored problem solving (Salden et al. 2010). The "fade assistance as competence increases" bullet in §5.7 rests on two primary studies of per-learner fading outside physics (Salden et al. 2010; Kalyuga & Sweller 2005).
- **Contingency is conditional.** Contingent teacher support helped only with long independent working time (van de Pol et al. 2015, school social studies).
- **Modelling first is not a safe default for conceptual outcomes.** PS-I beat I-PS on average (Sinha & Kapur 2021). In physics, inventing before being told improved transfer at Grade 8 (Schwartz et al. 2011), and exploring first improved conceptual scores in undergraduate physics (Weaver et al. 2018; Bego et al. 2022, Experiment 1; DeCaro et al. 2023), though a Bego et al. experiment without contrasting cases found no difference. Explicit instruction first won with Year 5 pupils when element interactivity was high (Ashman et al. 2020), and PS-I needs specific design features (Loibl et al. 2017). Kapur (2008) supports unstructured struggle after instruction, not problem solving before it.
- **Exploration length matters.** In randomized university chemistry studies, a 15-minute exploration before instruction gave *lower* conceptual scores (N = 168), while a 20-minute one gave higher conceptual and transfer scores (N = 357) (DeCaro et al. 2025, https://doi.org/10.1111/bjep.70007).
- **Transfer and delay are thin.** At school level, Kapur (2008), Schwartz et al. (2011; delayed 1–3 weeks) and Ashman et al. (2020) measured transfer; in university physics only Bego et al. (2022) did, with mixed results across two experiments (timing not verified). Ding et al. (2011) measured a cross-topic exam item 4 days later.
- **"Scaffold" is used loosely.** Many tools labelled scaffolds lack diagnosis and calibration (Puntambekar & Hübscher 2005), so pooled scaffolding effects mix different interventions.

Held against §11: most supporting outcomes are immediate. The component evidence does not show that an AI tutor switching between modelling, coaching and fading produces transfer.

## Implications for the map

1. **§4 Cognitive Apprenticeship row, evidence cell.** Replace "**Moderate**" with:
   > **Moderate** as a design framework: components have experimental support (worked examples, self-explanation, computer-based scaffolding g ≈ 0.46); no controlled test of the whole model in physics; fixed-schedule fading no better than none

   Keep the other cells.

2. **§5.7, new subsection "Evidence / limitations"** after "Domain fit":
   > Graded evidence (see `research/explore-cognitive-apprenticeship.md`):
   > - **Whole model:** no controlled test in university physics was found; health-sciences use is mostly design and perception work (Lyons et al. 2017).
   > - **Components:** modelling via worked examples and articulation via self-explanation (§5.8); computer-based scaffolding in STEM, g = 0.46 over 144 studies, largest at the principles level and for adults (Belland et al. 2017).
   > - **Fading:** in computer-based STEM scaffolding, fixed-schedule fading did worse than no fading in a pilot meta-analysis (Belland et al. 2015), and the full meta-analysis found no difference by whether or how scaffolds changed, including performance-adapted change (Belland et al. 2017). In single studies, per-learner fading beat fixed fading on delayed tests in a Geometry Cognitive Tutor (Salden et al. 2010), and adapted instruction beat a yoked non-adapted sequence in an algebra tutor (Kalyuga & Sweller 2005); both are outside physics.
   > - **Order:** problem solving before instruction beat instruction first on average (g = 0.36; Sinha & Kapur 2021), when it used contrasting cases or built instruction on students' attempts (Loibl et al. 2017). In university physics, exploring first beat instructing first on conceptual scores in one group's studies (Weaver et al. 2018; Bego et al. 2022, Experiment 1; DeCaro et al. 2023, N = 78), but not when the activity lacked contrasting cases (Bego et al. 2022, Experiment 2). Explicit instruction first won for primary pupils when element interactivity was high (Ashman et al. 2020).
   > - **Physics scaffold-then-remove:** conceptual questions before synthesis problems during training improved an unscaffolded, cross-topic exam problem 4 days later (Ding et al. 2011; class-level assignment).
   > - **Transfer:** one university-physics study measured transfer, with mixed results across two experiments (Bego et al. 2022); none has a verified delayed transfer test.

3. **§5.7 "AI opportunity".** Replace "fade assistance as competence increases." with:
   > fade assistance as measured competence increases, per learner, not on a fixed schedule (fixed-schedule fading did worse than no fading in a pilot meta-analysis, Belland et al. 2015; per-learner fading beat fixed fading in single studies outside physics, Salden et al. 2010; the full meta-analysis found no moderation by fading logic, Belland et al. 2017).

   Append after the list:
   > Fading needs a per-learner estimate of the targeted skill, so it depends on the explicit learner model (§5.10), not on conversation alone. Whether the tutor models first or lets the learner explore first is a design choice with evidence on both sides; for conceptual goals, exploration with contrasting cases before modelling is the better-supported default beyond early primary school (Sinha & Kapur 2021; Loibl et al. 2017).

4. **§5.7 "Questions to research next".** Keep the three questions and add:
   > - In university mechanics, does exploring with contrasting cases before expert modelling beat modelling first on **delayed** transfer, and does the answer change with element interactivity (Ashman et al. 2020)?
   > - Does adaptive fading beat fixed fading on delayed transfer in physics?

5. **§9 Phase 4.** Add to the intervention list:
   > - problem solving before instruction (contrasting cases, then instruction built on students' attempts);

   and after "Randomize or counterbalance where feasible.", add:
   > Treat order (explore first vs model first) as a factor, not a fixed default; the evidence is split by learner level and element interactivity (Sinha & Kapur 2021; Ashman et al. 2020).

   This is forced because Phase 4 lists "expert modelling" and "guided practice" without an order, and the order alone changes conceptual outcomes in randomized physics lessons (DeCaro et al. 2023; Bego et al. 2022; Schwartz et al. 2011). Stage B is not affected: both arms share the same order, so order cannot bias its contrast.

6. **§11, §12.** No change.

7. **§14.** Add:
   - Collins, Brown & Newman (1989): https://doi.org/10.4324/9781315044408-14 (replaces the undated §14 entry "Collins, Brown & Newman (1989) — cognitive apprenticeship")
   - Lyons et al. (2017): https://doi.org/10.1007/s10459-016-9707-4
   - Belland et al. (2017): https://doi.org/10.3102/0034654316670999
   - Belland, Walker, Olsen & Leary (2015): Educational Technology & Society 18(1), 183–197, no DOI (ERIC EJ1062484)
   - van de Pol, Volman & Beishuizen (2010): https://doi.org/10.1007/s10648-010-9127-6
   - van de Pol et al. (2015): https://doi.org/10.1007/s11251-015-9351-z
   - Puntambekar & Hübscher (2005): https://doi.org/10.1207/s15326985ep4001_1
   - Salden et al. (2010): https://doi.org/10.1007/s11251-009-9107-8
   - Kalyuga & Sweller (2005): https://doi.org/10.1007/BF02504800
   - Kirschner, Sweller & Clark (2006): https://doi.org/10.1207/s15326985ep4102_1
   - Hmelo-Silver, Duncan & Chinn (2007): https://doi.org/10.1080/00461520701263368
   - Alfieri et al. (2011): https://doi.org/10.1037/a0021017
   - Loibl, Roll & Rummel (2017): https://doi.org/10.1007/s10648-016-9379-x
   - Kapur (2008): https://doi.org/10.1080/07370000802212669
   - Schwartz et al. (2011): https://doi.org/10.1037/a0025140
   - Weaver et al. (2018): https://doi.org/10.1016/j.cedpsych.2017.12.003
   - Bego, Chastain & DeCaro (2022): https://doi.org/10.1111/bjep.12555
   - DeCaro et al. (2025): https://doi.org/10.1111/bjep.70007
   - Renkl et al. (2002): https://doi.org/10.1080/00220970209599510
   - DeCaro et al. (2023): https://doi.org/10.3389/feduc.2023.1215975
   - Ashman, Kalyuga & Sweller (2020): https://doi.org/10.1007/s10648-019-09500-5
   - Ding et al. (2011): https://doi.org/10.1103/physrevstper.7.020109

   Sinha & Kapur (2021) is already listed.

## Open questions

These are only the ones that would change the verdict:

- Is there a controlled university-physics comparison of the full modelling-coaching-fading sequence against a matched alternative, with a transfer outcome? A positive result would lift the "no whole-model test" qualifier; a null would narrow the card to its components.
- Does adaptive fading beat fixed fading in physics on a delayed test? If yes, §5.7's fading bullet has direct support; if fixed and adaptive tie, fading drops out of the tutor design.
- In university mechanics with multi-principle problems (high element interactivity), does explore-first still beat model-first, and does it hold at delay? This decides the default order for Phase 4 and the tutor.
