# Explore: Worked Examples + Self-Explanation

**Question:** Is "High" warranted for worked examples and self-explanation when the outcome is transfer, not immediate performance, and what does the evidence imply for Stage B, whose arms are both built from worked examples with self-explanation prompts?

**Verdict: no change to priority (P1); the "High" rating is scoped.** Meta-analyses give a medium effect for worked examples (g = 0.48, mathematics) and for prompted self-explanation (g = 0.55, including g = 0.53 on transfer measures (a 2025 meta-analysis of digital environments finds g = 0.33 on transfer; Tan et al. 2025)). Most of it is immediate; delayed effects are smaller (g = 0.35, Tan et al. 2025). Evidence from real classrooms is limited, and the worked-example advantage reverses as learners gain knowledge. For Stage B, one change is forced. Explanations handed to learners add little to worked examples, while explanations learners generate add more. So the operations the treatment adds must be carried by self-explanation prompts, not only written into the steps; otherwise a K2 null would test the delivery format, not the operations.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 row (P1, "High", STEM fit Very high, humanities Medium, AI readiness Very high) and the §5.8 card. The branch serves §9 Phase 2 Stage B (both arms are worked examples with self-explanation prompts; see `experiment-ai-assisted-cta-physics.md`), Phase 4 (worked example and self-explanation are listed interventions) and §10 RQ4.

Search: the OpenAlex REST API refused requests this session (HTTP 429), and the `openalex` MCP server was not loaded. Search used the Crossref, ERIC, Semantic Scholar and Unpaywall APIs plus WebSearch. Full text was read for Bisra et al. (2018), Gjerde et al. (2022), Badeau et al. (2017) and Rittle-Johnson & Loehr (2017). Barbieri et al. (2023) and Wittwer & Renkl (2010) are closed access, so their details come from abstracts. The citation check later read Atkinson et al. (2003), van Gog & Kester (2012), Lin & Singh (2011, 2013) and Chen et al. (2026, arXiv 2604.00142) in full, and Hausmann & VanLehn (2010) via the authors' LearnLab project page. The Zotero local API holds nothing on worked examples, self-explanation or cognitive load.

## Evidence

### Meta-analyses

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Barbieri et al. (2023), https://doi.org/10.1007/s10648-023-09745-1 | Meta-analysis (RVE) of experimental and quasi-experimental studies | 55 studies, 181 effect sizes | Mathematics, elementary to postsecondary; **outside physics** | Mathematics performance | g = 0.48. Adding self-explanation prompts to worked examples **reduced** the effect relative to worked examples without prompts. Correct examples alone beat incorrect or mixed examples. |
| Bisra et al. (2018), https://doi.org/10.1007/s10648-018-9434-x | Meta-analysis (random effects) | 69 effect sizes from 64 reports, 5,917 participants | Mixed subjects and levels | Mixed; coded by outcome type | g = 0.55 [0.45, 0.65], with high heterogeneity. **Transfer measures: g = 0.53 (k = 17).** Undergraduate samples g = 0.61 (k = 42). Self-explanation beat instructional explanations (g = 0.35, k = 6). The effect was g = 0.41 when time on task was matched and 0.72 when self-explanation took longer (difference not significant). No moderator for delayed testing. |
| Tan et al. (2025), https://doi.org/10.1007/s10648-025-10001-x | Three-level meta-analysis | 56 studies | Self-explanation in digital learning environments, mixed domains | Immediate, **delayed**, transfer | Delayed tests g = 0.35 (k = 46), immediate g = 0.45 (k = 158), transfer g = 0.33 (k = 77) |
| Rittle-Johnson, Loehr & Durkin (2017), https://doi.org/10.1007/s11858-017-0834-z | Meta-analysis | Not extracted | Mathematics; **outside physics** | Procedural, conceptual knowledge, procedural transfer | Small to moderate gains, including procedural transfer, **when assessed immediately**. Evidence for classroom settings and for **retention over a delay is much more limited**. Effects were stronger when high-quality explanations were scaffolded. |
| Wittwer & Renkl (2010), https://doi.org/10.1007/s10648-010-9136-5 | Meta-analysis | 21 experiments | Example-based learning, mixed domains | Conceptual and procedural knowledge | Adding **instructional explanations** to worked examples gives minimal benefit on its own. It helps conceptual knowledge more than procedural, and is not necessarily better than prompting self-explanation. |

The effect is real and medium-sized for immediate outcomes. The two meta-analyses do not agree on adding prompts to examples (Barbieri: studies whose example conditions included prompts showed smaller effects, a between-study moderator in mathematics; Bisra: positive for studying worked problems, g = 0.36, k = 8, the smallest main task-type estimate), so the combination should not be assumed to add up.

### Transfer and delay

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Atkinson, Renkl & Merrill (2003), https://doi.org/10.1037/0022-0663.95.4.774 | Two experiments | 78 university students (Exp. 1, lab, 2 × 2) and 40 high-school students (Exp. 2, school, prompts vs no prompts with fading) | Probability; **outside physics** | Near and **far transfer** (immediate) | Fading worked-out steps combined with prompts to name the principle behind each step gave medium to large effects on near and far transfer, with no extra time on task |
| Kissane et al. (2008), https://doi.org/10.1080/01443410802322069 | Classroom experiment | Not in abstract | Financial-services employees; **outside physics and outside university** | Immediate, **delayed** and transfer | Fading beat example–problem pairs and pure problem solving; the advantage was larger on the delayed and transfer tests |
| van Gog & Kester (2012), https://doi.org/10.1111/cogs.12002 | Experiment | 40 | Electrical-circuit troubleshooting (parallel circuits); 40 Dutch university students without upper-secondary science | Immediate and **1-week delayed** retention | Studying only worked examples equalled example–problem pairs at 5 minutes and beat them after 1 week |

Transfer benefits exist, mostly as immediate far-transfer tests in single-session laboratory studies. Delayed evidence is thin, and immediate and delayed results can diverge.

### University physics

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Chi et al. (1989), https://doi.org/10.1207/s15516709cog1302_1 | Think-aloud, correlational | 8 | Mechanics (participants had no college physics) | Problem solving after studying examples | Good solvers generated more self-explanations while studying examples. It is the origin of the self-explanation effect, and correlational. |
| Nokes-Malach et al. (2013), https://doi.org/10.1007/s10212-012-0164-z | Randomized, 3 conditions, in class | Not in abstract | **University introductory physics** (rotational kinematics) | Near, intermediate and **far transfer** | Self-explanation and analogical comparison beat reading examples on far transfer, with no loss on problem solving |
| Hausmann & VanLehn (2010), https://doi.org/10.3233/jai-2010-010 | In vivo experiment, 2 × 2 (self-explaining vs paraphrasing × complete vs incomplete examples) | 104 analysed (106 of 113 volunteered) | **University physics** (electrodynamics, US Naval Academy) | Immediate (assistance scores during training), ~1-week mid-term exam problem, later homework transfer | Results favoured the **generation** account: explaining helps because learners produce the content, not because the content is there. The authors conclude that examples should push learners to generate missing content. |
| Badeau et al. (2017), https://doi.org/10.1103/physrevphyseducres.13.020112 | Three randomized experiments | 196, 254 and 232 | **University introductory physics** (calculus-based, Ohio State) | One target synthesis problem after 10–15 min of unrelated tasks (immediate) | Self-explaining worked examples, and analogical comparison between synthesis examples, improved performance on multi-concept problems and recognition of the relevant concepts. On the harder problem, self-explanation beat comparison. |
| Gjerde et al. (2022), https://doi.org/10.1103/physrevphyseducres.18.010136 | Correlational (n = 18); randomized trial (N = 54) and quasi-experiment (N = 57) on retrieval practice before self-explanation | See design | **University introductory mechanics** (Bergen) | Post-test problem solving and conceptual items (short-term) | Self-explanations that named the principle, how it is set up and why its conditions of application hold predicted post-test scores (r = 0.30–0.50). Retrieval practice of principles and their conditions had no significant effect in the randomized study alone; pooled with the earlier study, d = 0.51 on problem solving and d = 0.16 (n.s.) on conceptual items. |
| Lin & Singh (2011), https://doi.org/10.1103/physrevstper.7.020104; (2013), https://doi.org/10.1103/physrevstper.9.020114 | Recitation quiz with scaffolding variants plus think-alouds | 362; 382 | **University introductory physics** | Solving an isomorphic problem after a solved one (immediate) | Students learned from the solved problem enough to invoke the right principles, but often did not apply them correctly, mapping principles superficially without checking their conditions |
| Heckler (2010), https://doi.org/10.1080/09500690903199556 | Experiments | 891 | **University introductory physics** | Correct solutions (immediate) | Prompting students to draw a force diagram **lowered** the rate of correct solutions and led to more incorrect forces; the authors suggest novices switched from intuitive to newly taught formal methods they could not yet use |

In university physics, prompted self-explanation of worked examples improved immediate multi-concept problem solving (Badeau et al. 2017) and far transfer without loss on problem solving (Nokes-Malach et al. 2013), both in randomized studies. Only one physics study found measured learning after a delay: Hausmann & VanLehn (2010) scored a mid-term exam problem about a week after a two-hour session, plus later homework. The self-explanation advantage there was marginal (exam) or small (homework, p = .05). No physics study has a planned delayed transfer test.

### Expertise reversal and boundary conditions

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Kalyuga et al. (2001), https://doi.org/10.1037/0022-0663.93.3.579 | Experiments | 24 trade apprentices per experiment (2 experiments; per Kalyuga 2007 review, Table 1) | Trade apprentices; **outside physics and outside university** | Test performance, mental load | Worked examples helped inexperienced trainees; with more experience, problem solving was superior |
| Chen, Kalyuga & Sweller (2015), https://doi.org/10.1037/edu0000018 | Two experiments | Not in abstract | Geometry; school students (China); **outside physics** | Test performance | The worked-example effect held for material high in element interactivity; for low-interactivity material, and for all material once learners knew more, generating answers beat studying them |
| Rey & Fischer (2013), https://doi.org/10.1007/s11251-012-9237-2 | Randomized 2 × 2 (induced expertise × explanations) | 93 | Statistics; **outside physics** | Retention and transfer | Instructional explanations showed an expertise reversal on transfer, not on retention |

### Critiques and alternatives

- Rittle-Johnson & Loehr (2017; online 2016), https://doi.org/10.3758/s13423-016-1079-5, a review of constraints: prompts draw effort to what they target and away from other content, so they must be aligned with the target outcome; explaining one's own, possibly wrong, ideas can reduce learning; alternatives such as extra non-routine problems sometimes match self-explanation on transfer.
- Sinha & Kapur (2021), https://doi.org/10.3102/00346543211019105: across 53 studies, problem solving *before* instruction beat instruction first (g = 0.36), except for young children and domain-general skills. This limits the claim that worked examples should always come first. It is not a comparison with worked examples as such.
- de Jong (2010), https://doi.org/10.1007/s11251-009-9110-0, sets out conceptual, methodological and application problems with cognitive load theory, the main explanation of the worked-example effect. The effect itself is not in dispute; its explanation and boundaries are.

### AI opportunity (§5.8): LLM feedback on self-explanations

One controlled study was found. Chen et al. (2026), https://doi.org/10.1007/978-3-032-29763-1_42, a conference paper with N = 92 in calculus, compared no self-explanation, menu-based self-explanation and open-ended self-explanation with LLM feedback. All conditions gained, with no post-test difference between them. Participants were adults recruited on Prolific (n = 28–35 per arm). Open-ended explanations were better than control only on 'not enough information' transfer items (β = +11.9 points, p = .030; across all post-test explanations p = .057), and that arm completed fewer practice problems in the same time. Abstract and arXiv full text (2604.00142) checked. On the §5.8 question "transfer or merely fluency?", the only evidence so far shows explanation quality, not transfer.

## Against

- **Delayed effects are smaller and less studied.** In digital learning environments, self-explanation gave g = 0.35 on delayed tests (k = 46) against 0.45 immediately (k = 158), and g = 0.33 on transfer (k = 77) (Tan et al. 2025). In mathematics, classroom and delayed-retention evidence is "much more limited" (Rittle-Johnson et al. 2017). Bisra et al. (2018) and Barbieri et al. (2023) did not code test delay. Under §11, the "High" rating is firmest for immediate performance.
- **Prompts plus examples do not reliably add.** In Barbieri et al.'s (2023) mathematics meta-analysis, studies whose example conditions included self-explanation prompts showed smaller worked-example effects (a between-study moderator). Prompts can also pull attention from other content (Rittle-Johnson & Loehr 2017).
- **Told explanations add little.** Instructional explanations in examples give minimal benefit (Wittwer & Renkl 2010), and self-explanation beats them (g = 0.35, k = 6, Bisra et al. 2018). In one physics in-vivo study the results favoured generation over content, though delayed effects were marginal (Hausmann & VanLehn 2010).
- **Expertise reversal.** The worked-example advantage turns into a disadvantage as knowledge grows (Kalyuga et al. 2001; Chen et al. 2015; Rey & Fischer 2013 for explanations, on transfer).
- **Formal methods can hurt novices.** Prompting a taught formal step reduced correct solutions among 891 physics students (Heckler 2010).
- **Order.** Problem solving before instruction can beat instruction first (Sinha & Kapur 2021).

## Implications for the map

1. **§4 row, evidence cell.** Replace "**High**" with:
   > **High** for immediate problem solving by novices (meta-analyses g ≈ 0.5); delayed and transfer effects smaller (g ≈ 0.35); little classroom or delayed physics evidence; reverses as prior knowledge grows

   Keep the other cells.
2. **§5.8, new subsection "Evidence / limitations"** after "Domain fit":
   - Worked examples: g = 0.48 in mathematics (Barbieri et al. 2023). Prompted self-explanation: g = 0.55, and g = 0.53 on transfer measures (Bisra et al. 2018); in digital learning environments, g = 0.45 immediate, 0.35 delayed and 0.33 on transfer (Tan et al. 2025).
   - Classroom and delayed-retention evidence is "much more limited" in mathematics (Rittle-Johnson et al. 2017).
   - University physics: prompted self-explanation of worked examples improved immediate multi-concept problem solving (Badeau et al. 2017) and far transfer (Nokes-Malach et al. 2013), both randomized. The only delayed physics measure found a marginal or small advantage (Hausmann & VanLehn 2010).
   - Learner-generated explanations beat provided ones (g = 0.35, k = 6; Bisra et al. 2018). Instructional explanations added to examples give minimal benefit (Wittwer & Renkl 2010). One physics in-vivo study favoured generation over content (Hausmann & VanLehn 2010).
   - Boundary conditions: expertise reversal (Kalyuga et al. 2001; Chen, Kalyuga & Sweller 2015). Mathematics studies whose example conditions included self-explanation prompts showed smaller worked-example effects, a between-study moderator (Barbieri et al. 2023). Prompts must target the intended outcome (Rittle-Johnson & Loehr 2017).
3. **§5.8 "AI opportunity".** Append after the list:
   > Decoded operations should reach the learner as prompts to generate or apply them, not only as added text: provided explanations add little to worked examples (Wittwer & Renkl 2010). In physics, self-explanations that state the principle, how it is set up and how its conditions of application are met predicted post-test scores (r = 0.30–0.50; Gjerde et al. 2022). The one controlled study of LLM feedback on self-explanations (calculus; 92 adults online; one session) found no post-test difference between conditions (Chen et al. 2026).
4. **§9 Phase 2, Stage B bullet.** After "The treatment adds validated operations from the AI-assisted pipeline, length- and time-matched and delivered statically.", add:
   > Each added operation is carried by at least one self-explanation prompt that asks the student to state or apply it, with a model answer shown after; both arms have the same number of prompts. Operations given only as text would test the delivery format, not the operations (Wittwer & Renkl 2010; Hausmann & VanLehn 2010).

   The experiment note says the operations are "written into the steps and self-explanation prompts", without fixing either detail. K1, K2 and the expertise-reversal line are unchanged. Keeping prompts in the control arm is right: it holds the prompt effect constant, so Barbieri et al.'s negative moderator lowers the expected absolute gain in both arms rather than biasing the contrast.
5. **§14.** Add Tan et al. (2025); Barbieri et al. (2023); Bisra et al. (2018); Rittle-Johnson, Loehr & Durkin (2017); Rittle-Johnson & Loehr (2017); Wittwer & Renkl (2010); Atkinson, Renkl & Merrill (2003); Kissane et al. (2008); van Gog & Kester (2012); Hausmann & VanLehn (2010); Badeau et al. (2017); Gjerde et al. (2022); Heckler (2010); Kalyuga et al. (2001); Chen, Kalyuga & Sweller (2015); Rey & Fischer (2013); Sinha & Kapur (2021); Chen et al. (2026). Chi et al. (1989), Nokes-Malach et al. (2013) and Kalyuga (2007) are already listed.

No §12 change: note 5 already says the strong results come from carefully engineered pedagogy, and this branch does not alter that.

## Open questions

These are only the ones that would change the verdict:

- Is there a university-physics study of worked examples or prompted self-explanation with a planned **delayed** transfer test (Hausmann & VanLehn 2010 measured a week later, but not transfer by design)? A positive result would let the §4 cell drop "delayed evidence limited"; a null would narrow the rating to immediate performance.
- What drives Barbieri et al.'s (2023) negative moderator for self-explanation prompts: prompt type, time on task, or learner level? If it holds for undergraduates, Stage B's absolute effects would be smaller than the meta-analytic g suggests, which matters for the SESOI.
- Does the Chen et al. (2026) result, no post-test difference and better explanations only on some transfer items, hold in physics with students and a delayed test? That is the §5.8 "transfer or fluency" question.
