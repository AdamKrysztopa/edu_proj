# Explore: Intelligent Tutoring Systems (ITS)

**Question:** How strong is the ITS evidence once test alignment, comparison condition and scale are separated out, what does it show in university physics, and which classical ITS design principles does it support for an LLM-based system (§5.9 questions, §6 architecture principle)?

**Verdict: no change to priority (P1); the rating "High overall, heterogeneous" is scoped.** The large effects are real but come from tests aligned to what the tutor teaches: a median 0.66 SD over conventional instruction (Kulik & Fletcher 2016), and step-based tutoring nearly as effective as human tutoring (d = 0.76 vs 0.79; VanLehn 2011). On standardized tests effects fall to 0.13 SD across 9 evaluations, against 0.73 on local tests (Kulik & Fletcher 2016), and in K–12 mathematics and at scale to about 0.0–0.2 SD (Steenbergen-Hu & Cooper 2013; Pane et al. 2014). In university physics the one long-running evaluation, Andes at the US Naval Academy, is non-randomized. Its hour-exam gain (d = 0.61) sits in the practices the tutor enforces (drawings, variable definitions), not in equations or the answer subscore; on the answer-only multiple-choice final exam the gain was d = 0.25, confined to majors other than engineering and science. For the architecture, the evidence supports step-level checking and an explicit pedagogical policy. No study found tests the §6 claim that separating domain, student and pedagogical models beats one integrated model, so that claim stays a design inference.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 ITS row (P1, "High overall, heterogeneous", STEM fit Very high, humanities Medium–high, AI readiness Very high), the §5.9 card, and the §6 "Important architectural principle" ("The LLM should probably be an interface/reasoning component, not the database of truth, the student model, the pedagogy model and the evaluator simultaneously"). The branch serves §9 Phase 5 (adaptive system) and §10 RQ5 and RQ8. It overlaps the P2 LLM-tutoring branch (§5.12); LLM studies appear here only where they bear on a classical ITS principle.

Search: the OpenAlex REST API returned HTTP 429 on the first request, and the `openalex` MCP server was not loaded. Search used the Crossref, Semantic Scholar and ERIC APIs and WebSearch. Full text was read for the Andes evaluation paper (VanLehn et al. 2005, "Five Years of Evaluations", OLI-hosted PDF) and Bastani et al. (2025, PMC). Ma et al. (2014) and Pane et al. (2014) come from ERIC or publisher abstracts. The citation check read Kulik & Fletcher (2016), the Andes IJAIED journal paper, VanLehn (2011), Steenbergen-Hu & Cooper (2013, 2014), Chi et al. (2011), Chi & VanLehn (2010), Pardos & Bhandari (2024) and the RAND addendum and brief for Pane et al. in full, and the figures below follow them. The Zotero local API holds Kulik & Fletcher (2016) and Kestin et al. (2025), both added today with no notes or attachments.

## Evidence

### How large is the effect, and on what kind of test?

| Source | Design | N | Domain | Test type and timing | Finding |
|---|---|---|---|---|---|
| Kulik & Fletcher (2016), https://doi.org/10.3102/0034654315581420 | Meta-analysis of controlled evaluations | 50 evaluations | Mixed domains and levels | Mixed; locally developed vs standardized; immediate or end of course | Median effect 0.66 SD over conventional instruction. The size "depended to a great extent" on locally developed vs standardized tests, so alignment of test and objectives is "a critical determinant". Evaluations with non-conventional controls (6) or flawed implementations (4) showed small effects. Across all 50 evaluations the average ES was 0.73 on locally developed tests (38 evaluations), 0.13 on standardized tests (9) and 0.45 on both (3) (Table 3; Hedges's g 0.62 vs 0.09). In the 15 Cognitive Tutor evaluations the mean was 0.76 on local and 0.12 on standardized tests (medians 0.86 and 0.16; Table 4); Cognitive Tutor "neither helped nor hindered" standardized-test performance. |
| VanLehn (2011), https://doi.org/10.1080/00461520.2011.611369 | Review of experiments comparing human, computer and no tutoring | 87 comparisons (human vs no tutoring 10; step-based 28; substep-based 26) | STEM only (inclusion criterion), mixed levels | Mixed | Against no tutoring, human tutoring gave d = 0.79 and step-based tutoring d = 0.76 (substep-based 0.40), so step-based ITS are "nearly as effective as human tutoring"; in 10 direct comparisons human tutoring led step-based by d = 0.21. The believed ordering (answer-based 0.3, ITS 1.0, human 2.0) was not confirmed. |
| Ma, Adesope, Nesbit & Liu (2014), https://doi.org/10.1037/a0037123 | Meta-analysis | 107 effect sizes, 14,321 participants | Mixed domains, all levels | Mixed | ITS beat teacher-led large-group instruction (g = 0.42), non-ITS computer instruction (0.57) and textbooks (0.35). No difference from individual human tutoring (g = −0.11) or small-group instruction (0.05). |
| Steenbergen-Hu & Cooper (2014), https://doi.org/10.1037/a0034752 | Meta-analysis | 39 studies, 22 ITS | **College**, mixed domains | Mixed | g = 0.32–0.37. Less effective than human tutoring, better than all other comparisons. No difference by domain. Earlier studies showed larger effects than recent ones. |
| Steenbergen-Hu & Cooper (2013), https://doi.org/10.1037/a0032447 | Meta-analysis | 34 samples (26 reports, 1997–2010) | K–12 mathematics; **not university** | Mostly regular classroom comparison | g = 0.01–0.09: "no negative and perhaps a small positive effect"; 0.19 on course-related measures and 0.02 on standardized tests. Kulik & Fletcher (2016) contest it, finding 0.40 across 18 K–12 mathematics evaluations (0.10 on standardized tests). Effects were larger for interventions shorter than a school year, and larger for general students than for low achievers. |
| Pane, Griffin, McCaffrey & Karam (2014), https://doi.org/10.3102/0162373713507480 | Cluster RCT, matched school pairs, 7 US states, 2 years | 147 schools (73 high, 74 middle) in 51 districts; about 18,700 high-school and 6,800 middle-school students (RAND RB9746) | Algebra I, middle and high school; **not university** | Standardized algebra proficiency exam | No effect in year 1. In year 2, about +8 percentile points; significant in high schools only (0.20 SD in RAND's brief; 0.21 SD in the addendum's fully adjusted model, p = .04, ERIC ED559621; less-adjusted models 0.12–0.17, n.s.). |
| Létourneau et al. (2025), https://doi.org/10.1038/s41539-025-00320-7 | Systematic review | 28 studies, 4,597 students, all quasi-experimental | K–12; **not university** | Mixed | Effects "generally positive" but "mitigated when compared to non-intelligent tutoring systems". Calls for longer interventions and larger samples. |

The pattern is consistent across the syntheses. Effects shrink when the test is standardized rather than aligned to the tutor, when the control is another tutoring system rather than a lecture, and when the tutor runs at scale in schools. None of the syntheses reports delayed retention or transfer as a separate outcome (Ma et al. 2014 not checked in full text).

### University physics

| Source | Design | N | Domain | Test type and timing | Finding |
|---|---|---|---|---|---|
| VanLehn et al. (2005a), "Five Years of Evaluations", AIED 2005, https://oli.cmu.edu/wp-content/uploads/2012/05/VanLehn_2005_Andes_Five_Years_of_Evaluations.pdf; journal account VanLehn et al. (2005b), https://doi.org/10.3233/irg-2005-15%283%2902 | Non-randomized field comparison: sections of the Andes instructors (who are co-authors) vs recruited control sections doing paper homework graded for effort | Hour exams 2000–2003: 455 Andes, 276 control. Final exam 2003: 89 Andes, 823 non-Andes | **University introductory physics**, US Naval Academy | Hour exams written by the instructors, scored with a rubric (end of each unit); a common multiple-choice final exam (end of semester) | Hour exams: d = 0.61 overall (2000–2003). By rubric component: drawings d = 1.21, variable definitions 0.69, equations 0.11, correct answers −0.08. Final exam (2003 only, residualized on GPA and major): d = 0.25 (p = .028), carried by majors other than engineering and science (0.52; engineers 0.22 and science majors 0.18, both n.s.). Andes replaced only paper homework; lectures, text and labs were unchanged. |
| Chi, VanLehn, Litman & Jordan (2011), https://doi.org/10.3233/jai-2011-014 | Experiment: two pedagogical policies induced by reinforcement learning, same content | 64 paid college students randomized; 57 completed (29 vs 28) | Physics work–energy, **college students without college physics**, lab study; NL tutor with a human language-understanding wizard | Pre/post (immediate) | With content held the same, the policy induced to enhance learning beat the one induced to do the opposite. "Content exposure and practice opportunities can help students to learn even when tutors have poor pedagogical tutorial tactics", but effective tactics add to it. Posttest d = 0.65, adjusted posttest 0.86, normalized gain 0.81. |
| Chi & VanLehn (2010), ERIC EJ880072 (Educational Technology & Society 13(1); no DOI found) | Experiment with transfer across domains | 44 paid college students randomized; 42 analysed (10–12 per ability × condition cell) | Probability, then **physics** (college) | Transfer to a second domain | An ITS teaching a domain-independent strategy in probability closed the gap between high and low learners in probability and in physics, where it was not taught. The authors attribute transfer to the "principle-emphasis" skill (attending to each principle's characteristics), not to the backward-chaining strategy. |

The Andes result is the one most relevant to the map. On the hour exams the gain appears in the practices the tutor makes students perform, with no gain on the answer subscore (−0.08); on the answer-only multiple-choice final exam the gain was smaller (d = 0.25) and confined to majors other than engineering and science. Under §11 ("do not treat learner correctness as equivalent to understanding", and its converse) this is an alignment effect of the kind Kulik & Fletcher describe. It supports Stage B's decision to score the primary outcome for correctness only.

### Which classical design principles does the evidence support?

- **Step-level interaction.** VanLehn (2011) found step-based tutoring nearly as effective as human tutoring (0.76 vs 0.79 against no tutoring) and no advantage for finer, substep granularity (0.40), though Kulik & Fletcher (2016) attribute the low substep figure to nonconventional control groups. Andes' distinguishing feature is feedback on each step of a derivation (VanLehn et al. 2005b). Checking steps requires a representation of valid solutions that is independent of the language that describes them.
- **An inner loop and an outer loop.** VanLehn (2006), https://doi.org/10.3233/irg-2006-16%283%2902, describes tutoring as an outer loop that chooses the next task and an inner loop that gives feedback and hints within a task. This is a descriptive framework, not an evaluation.
- **An explicit pedagogical policy matters beyond content.** Chi et al. (2011) is the direct evidence: with content identical, the policy changed learning. It is a single lab study (N = 57) against a policy induced to be poor, and its outcome is immediate.
- **Withholding answers.** Overlap with §5.12: in a field RCT with nearly 1,000 high-school students in Turkey, an unconstrained GPT-4 tutor raised practice scores by 48% but lowered the unassisted exam score by 17%. A version prompted to give teacher-designed hints and not answers raised practice by 127% and largely removed the harm, without a positive exam effect (Bastani et al. 2025, https://doi.org/10.1073/pnas.2422633122; the correction, https://doi.org/10.1073/pnas.2518204122, fixes one author's affiliation only). The exam was immediate and closed-book, in the same session.
- **Independent verification of content.** Overlap with §5.12: ChatGPT-generated hints produced learning gains not significantly different from human-authored hints for Mechanical Turk adults on OpenStax algebra and statistics problems (N = 274; online, immediate post-test), but failed quality checks on 32% of problems before a self-consistency filter (Pardos & Bhandari 2024, https://doi.org/10.1371/journal.pone.0304013).

No study found compares a system with separate domain, student and pedagogical models against one integrated model on learning. The §6 principle is therefore supported only indirectly: step checking needs a domain model, the pedagogical policy has independent effects (Chi et al. 2011), and generated content needs checking (Pardos & Bhandari 2024).

## Against

- **Alignment inflates effects.** The headline 0.66 SD is a median over locally developed and standardized tests, and the tests aligned to the tutor carry it (Kulik & Fletcher 2016). Andes' hour-exam gains are in the rubric components it enforces, not in the answer subscore; on its answer-only final exam the gain was d = 0.25.
- **Small at scale.** In K–12 mathematics Steenbergen-Hu & Cooper (2013) found g ≈ 0.01–0.09 overall (0.19 on course-related measures, 0.02 on standardized tests); Kulik & Fletcher (2016) found 0.40 across 18 K–12 mathematics evaluations, but 0.10 on standardized tests only. The largest RCT found nothing in year 1 and about 0.2 SD in year 2, statistically significant only in high schools (similar magnitude in middle schools) (Pane et al. 2014).
- **Weaker against strong controls.** ITS do not beat individual human tutoring or small-group instruction (Ma et al. 2014), and effects are smaller against non-intelligent tutoring systems (Létourneau et al. 2025).
- **Declining over time.** Earlier college studies show larger effects than recent ones (Steenbergen-Hu & Cooper 2014).
- **Physics evidence is non-randomized.** Andes sections were those of the co-author instructors, who also set the hour exams that their recruited Control sections sat. The final-exam result is one year, residualized on GPA and major rather than randomized, and driven by majors other than engineering and science.
- **No delayed or transfer outcomes** in the syntheses. The only transfer result found is cross-domain transfer of a strategy (Chi & VanLehn 2010), with 42 students analysed (about 10 per cell).
- **The §6 separation principle is untested** as an architectural comparison.

Held against §11: most ITS evidence is immediate or end-of-course performance, much of it on tests aligned to the tutor. It does not show that ITS produce transfer.

## Implications for the map

1. **§4 ITS row, evidence cell.** Replace "**High overall, heterogeneous**" with:
   > **High on tests aligned to the tutor** (median 0.66 SD; 0.73 on local vs 0.13 on standardized tests; step-based ≈ human tutoring); small at scale (≈ 0–0.2 SD); physics: one non-randomized university study, large hour-exam gains on enforced practices, d = 0.25 on an answer-only final

   Keep the other cells.

2. **§5.9 "Evidence".** Replace the paragraph with:
   > Graded evidence (see `research/explore-intelligent-tutoring-systems.md`):
   > - **Aligned tests carry the effect.** Median 0.66 SD over conventional instruction across 50 evaluations, depending "to a great extent" on locally developed vs standardized tests: 0.73 vs 0.13 (Kulik & Fletcher 2016). Step-based ITS are nearly as effective as human tutoring (d = 0.76 vs 0.79; VanLehn 2011). College: g = 0.32–0.37 (Steenbergen-Hu & Cooper 2014).
   > - **Small at scale and against strong controls.** K–12 mathematics g = 0.01–0.09, 0.02 on standardized tests (Steenbergen-Hu & Cooper 2013; Kulik & Fletcher 2016 report 0.10 on standardized tests). Cognitive Tutor Algebra at scale: no effect in year 1, about 0.2 SD in year 2 in high schools (Pane et al. 2014). No advantage over individual human tutoring (Ma et al. 2014); smaller effects against non-intelligent tutoring systems (Létourneau et al. 2025).
   > - **University physics.** Andes, replacing paper homework at the US Naval Academy (non-randomized): hour exams d = 0.61, concentrated in drawings (1.21) and variable definitions (0.69), with no gain on the answer subscore; answer-only final exam d = 0.25, confined to majors other than engineering and science (VanLehn et al. 2005).
   > - **Transfer and delay:** not reported in the syntheses.

3. **§5.9 "AI opportunity".** Append:
   > The evidence supports three classical principles for an LLM tutor: step-level feedback checked against an explicit solution representation (VanLehn 2011; VanLehn et al. 2005); an explicit pedagogical policy, which changed learning with content held constant (Chi et al. 2011, college physics); and withholding answers, since an unconstrained GPT-4 tutor lowered unassisted exam scores while a hint-only version did not (Bastani et al. 2025, high school; overlap with §5.12).

4. **§5.9 "Questions to research next".** Replace "Which classical ITS design principles remain essential when generation becomes flexible?" with:
   > Does an LLM tutor with step-level checking against an explicit solution model beat the same tutor without it, on a test not aligned to the tutor?

   Add:
   > Does an ITS in university physics improve correct answers and transfer, not only the practices it enforces?

5. **§6 "Important architectural principle".** Append:
   > No study compares separated domain, student and pedagogical models against one integrated model; the principle rests on indirect evidence (step checking needs a domain model; pedagogical policy has effects of its own, Chi et al. 2011; generated hints fail quality checks without verification, Pardos & Bhandari 2024).

6. **§9 Phase 5.** Add after "then optimize personalization.":
   > Evaluate any adaptive system on a test not written around the system's own tasks, and over more than one term: ITS effects shrink on standardized tests (Kulik & Fletcher 2016) and appeared only in the second year at scale (Pane et al. 2014).

7. **§12 note 4.** Append:
   > Its large effects are on tests aligned to the tutor; on standardized tests and at scale they are about 0–0.2 SD.

8. **Stage B:** no change. The Andes finding supports the existing correctness-only scoring of the primary outcome.

9. **§14.** Add:
   - VanLehn (2011): https://doi.org/10.1080/00461520.2011.611369
   - Ma, Adesope, Nesbit & Liu (2014): https://doi.org/10.1037/a0037123
   - Steenbergen-Hu & Cooper (2013): https://doi.org/10.1037/a0032447
   - Steenbergen-Hu & Cooper (2014): https://doi.org/10.1037/a0034752
   - Pane, Griffin, McCaffrey & Karam (2014): https://doi.org/10.3102/0162373713507480
   - VanLehn et al. (2005), Andes: https://doi.org/10.3233/irg-2005-15%283%2902
   - VanLehn (2006), the behavior of tutoring systems: https://doi.org/10.3233/irg-2006-16%283%2902
   - Chi, VanLehn, Litman & Jordan (2011): https://doi.org/10.3233/jai-2011-014
   - Bastani et al. (2025): https://doi.org/10.1073/pnas.2422633122
   - Pardos & Bhandari (2024): https://doi.org/10.1371/journal.pone.0304013

   Kulik & Fletcher (2016) and Létourneau et al. (2025) are already listed.

## Open questions

These are only the ones that would change the verdict:

- Is there a randomized university-physics ITS study with a standardized or independently written test, or a delayed transfer test? A positive result would let the §4 cell drop the physics qualifier; a null would narrow ITS to aligned-test gains.
- Does any study compare a separated-model architecture with an integrated LLM tutor on learning? That would turn the §6 principle from inference into evidence, or overturn it.
