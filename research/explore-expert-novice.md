# Explore: Expert–Novice research

**Question:** How strong is the evidence that experts and novices represent physics problems differently, and does instruction built on expert representations improve novice problem solving or transfer?

**Verdict: no change to priority (P0) or rating ("High as foundational evidence"); the rating is scoped.** The descriptive finding is well replicated in physics: experts sort and analyse problems by principle, novices by surface features. But it is a continuum, not two groups. Instruction built on expert representations (principle-first analyses) has helped novices in small controlled physics studies, a science meta-analysis and one randomized classroom study with a far-transfer outcome. Most of these outcomes are immediate, and no university-physics study shows delayed transfer.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 Expert–Novice row (P0, "High as foundational evidence", STEM fit Very high, humanities High, AI readiness High) and the §5.3 card. The branch serves §9 Phase 1 (the taxonomy entries "representation choice" and "decomposition strategy") and Phase 2 (the Stage A topic is principle selection, chosen because it is "the canonical expert–novice difference in physics"; see `experiment-ai-assisted-cta-physics.md`), and §10 RQ2 and RQ4.

Search: the `openalex` MCP server was not loaded, and the OpenAlex REST API refused requests this session (HTTP 429, daily credit limit reached). Search instead used the Crossref, Semantic Scholar and ERIC APIs plus WebSearch. Full text was read for the open-access PRST-PER papers (Mason & Singh 2011; Docktor et al. 2012, 2015; Docktor & Mestre 2014) and for the preprint of Singh et al. (2023). Dufresne et al. (1992), Hardiman et al. (1989) and Heller & Reif (1984) are closed access, and their details come from abstracts and secondary reviews. The Zotero local API holds Chi, Feltovich & Glaser (1981), added today with no notes, and no other expert–novice items.

## Evidence

### Do experts and novices represent physics problems differently?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Chi, Feltovich & Glaser (1981), https://doi.org/10.1207/s15516709cog0502_2 | Four lab studies: card sorts and protocols | Small; the main sort had 8 introductory students and 8 physics graduate students | **Physics** (mechanics) | Categorization, protocols | Experts begin a representation from the physics principle, novices from the problem's literal features. |
| Hardiman, Dufresne & Mestre (1989), https://doi.org/10.3758/bf03197085 | Two experiments: an expert–novice comparison, then novices grouped by how they reason (correlational) | Not in abstract | **Physics** (mechanics) | Similarity judgments; problem-solving score | Experts judged similarity mainly by deep structure but were still pulled by surface similarity. Novices who used principles more categorized more like experts **and scored higher in problem solving**. |
| de Jong & Ferguson-Hessler (1986), https://doi.org/10.1037/0022-0663.78.4.279 | Correlational card sort of 65 knowledge elements | 47 first-year students | **University physics** (E&M) | Knowledge organization vs problem-solving success | Good solvers sorted knowledge elements by problem type (principle-based); poor solvers did not (correlational). |
| Mason & Singh (2011), https://doi.org/10.1103/physrevstper.7.020110 | Cross-sectional categorization study | 3 introductory classes of >100 students each, plus graduate students and faculty | **University physics** (mechanics) | Categorization quality | There is a **large overlap** between calculus-based introductory students and graduate students on "good" categorization, which contrasts with Chi et al. Expertise is a wide distribution, and calculus-based students did better than algebra-based ones. |

This confirms the §5.3 mechanism, qualified by Mason & Singh. The categorization gap is real at the extremes. But in a large sample, the categorization gap does not cleanly separate calculus-based introductory students from graduate students. Categorization is a proxy for expertise, not a measure of it.

### Does instruction built on expert representations help novices?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Heller & Reif (1984), https://doi.org/10.1207/s1532690xci0102_2 | Controlled lab experiments with a prescriptive model | Undergraduate volunteers; N not verified | **University physics** (mechanics) | Immediate solution quality | Students guided through a model procedure for describing the problem in physics terms produced better descriptions and better solutions than groups following alternative or partial models. Most components of the model were necessary. |
| Dufresne et al. (1992), https://doi.org/10.1207/s15327809jls0203_3 | Three lab experiments (computer-based Hierarchical Analysis Tool vs traditional problem solving) | Not in abstract | **Physics novices** | Similarity judgments, reasoning, problem solving (immediate) | Principle-first, hierarchical analyses made novices' similarity judgments more expert-like by shifting attention to deep structure, and improved problem solving (Experiment 3). |
| Mestre et al. (1993), https://doi.org/10.1002/tea.3660300306 | Training study vs time-matched traditional problem-solving controls | 42 | **Beginning physics students** | Categorization and qualitative explanations (immediate) | After five one-hour sessions of hierarchical analysis, students relied more on principles in categorization and explanations; controls showed no consistent shift. Novices who carried out the analyses successfully improved in problem solving relative to self-directed novices (conditional result). |
| Leonard, Dufresne & Mestre (1996), https://doi.org/10.1119/1.18409 | Course implementation; design not controlled as far as the abstract shows | One calculus-based course | **University physics** | Principle identification; **recall of principles months later** | Written qualitative strategies (principle, justification, procedure) helped students identify applicable principles and recall the major principles months after the course. The retention outcome is recall, not problem solving. |
| Docktor, Mestre & Ross (2012), https://doi.org/10.1103/physrevstper.8.020102 | Randomized, two feedback conditions, one session | 26 | **University physics** (algebra-based, end of course) | Reasoning criteria in similarity judgments (immediate) | Elaborate, principle-linked feedback raised the share of principle-based reasoning (0.47 vs 0.16 of statements). Accuracy on the items stayed poor. |
| Docktor, Strand, Mestre & Ross (2015), https://doi.org/10.1103/physrevstper.11.020106 | Quasi-experimental, 3 schools, class-level assignment (random at one school only) | 84 (34 CPS, 50 control) | **High-school physics** (not university) | Post-instruction problem solving, concepts, categorization; one transfer test (2 schools) | Conceptual Problem Solving (identify principle, justify, plan) classes scored higher on problem solving at all three schools, by 10%, 15% and 16%; only the last was significant. On the transfer test almost all students in both arms scored zero, so it is uninformative. |
| Taconis, Ferguson-Hessler & Broekkamp (2001), https://doi.org/10.1002/tea.1013 | Meta-analysis, 22 articles, 40 experiments (1985–1995) | — | **Science problem solving** (not physics only) | Standardized learning effects | Effective treatments all attended to the structure of the knowledge base (schemata). Teaching strategy knowledge and plain practice had little effect. Guidelines for judging one's own solutions and immediate feedback mattered. |
| Nokes-Malach et al. (2013), https://doi.org/10.1007/s10212-012-0164-z | Randomized, 3 conditions, in class | Not in abstract | **University introductory physics** (rotational kinematics) | Near, intermediate and **far transfer** | Self-explaining how examples instantiate principles, and analogical comparison of examples, both beat reading examples on far transfer. Reading and self-explanation beat analogy on near-transfer problems during learning; this vanished on intermediate transfer at test. Whether the test was delayed is not verified. |

The pattern is consistent: making novices attend to principles first and to the principle–feature link improves how they categorize and analyse problems, and usually improves immediate problem solving. Nokes-Malach et al. (2013) is the only controlled university-physics study found here with a far-transfer outcome, and it tests principle-focused *study activities*, not expert-derived *content*.

### Secondary syntheses

- Docktor & Mestre (2014), https://doi.org/10.1103/PhysRevSTPER.10.020119, a synthesis of physics DBER, flags a limitation of the expert–novice literature: experts usually solve "exercises that are simple for them, not novel problems", and few studies look at the stages between novice and expert.
- Singh, Maries, Heller & Heller (2023), https://doi.org/10.1063/9780735425477_017, a handbook chapter, notes the procedural problems of the pioneering studies. The same question is a problem for the novice and an exercise for the expert, and deciding who counts as an expert (e.g., whether a graduate student is one) is itself unclear. Expertise runs on a continuum.

## Against

- **The dichotomy does not hold in large samples.** Mason & Singh (2011) found large overlap between calculus-based introductory students and graduate students. Chi et al.'s contrast came from small samples at the extremes.
- **Categorization is a noisy proxy.** A short intervention shifted students' stated criteria without improving their accuracy (Docktor et al. 2012). In Docktor et al. (2015) all groups, treatment included, chose the superficially similar problem more often than the one that shared a principle.
- **Transfer is thin.** Apart from Nokes-Malach et al. (2013), outcomes are immediate; Docktor et al. (2015) report one marginal post-course gain on an independent district test (one high-school class, p < .10). Docktor et al.'s (2015) transfer test hit the floor. Leonard et al.'s (1996) "months later" result measures recall of principles, not solving new problems. Under §11 this does not show that teaching expert representations produces transfer.
- **Null in physics for teaching expert decisions.** Jeong et al. (2024), https://doi.org/10.1007/s10639-024-12962-y, found no direct performance effect (quasi-experimental, N = 390, two lessons, in an online introductory physical-science course framed as introductory physics). See `explore-cognitive-task-analysis.md`.
- **Small samples, old studies.** The instructional studies of the 1980s and 1990s are laboratory or small-class work, several with N not reported in the abstract. The meta-analysis covers 1985–1995 and all of science.
- **Expertise reversal.** Instruction that helps novices can become redundant or harmful for more knowledgeable learners (Kalyuga 2007, https://doi.org/10.1007/s10648-007-9054-3; review, mostly outside physics). Expert-derived content added statically may help weak students and not strong ones.

## Implications for the map

1. **§4 Expert–Novice row, evidence cell.** Replace "**High as foundational evidence**" with:
   > **High as foundational evidence** for representation differences (a continuum, not two groups); instruction built on them helps immediate problem solving in small physics studies; one far-transfer RCT

   Keep the other cells.
2. **§5.3, new subsection "Evidence / limitations"** after "Non-STEM fit":
   - The descriptive finding replicates in physics (Chi et al. 1981; Hardiman et al. 1989; de Jong & Ferguson-Hessler 1986). Novices who categorize by principle also solve better (correlational).
   - Expertise is a continuum: calculus-based introductory and graduate students overlap widely on categorization (Mason & Singh 2011). Categorization is a proxy, not a measure.
   - Principle-first instruction helps novices on immediate outcomes (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015, high school), consistent with a science meta-analysis favouring attention to knowledge structure plus guidelines and feedback (Taconis et al. 2001).
   - Transfer: one randomized university-physics study (Nokes-Malach et al. 2013) found far-transfer gains from self-explanation and analogical comparison against principles; no study shows delayed transfer.
   - In most studies experts solve exercises that are routine for them (Docktor & Mestre 2014).
3. **§5.3 "Questions to research next".** Add:
   > Does teaching an expert representation help strong novices as much as weak ones (expertise reversal)?
4. **§9 Phase 2, Stage A bullet.** After "'Absent' is judged against expert explanations plus textbook and lecture notes.", add:
   > Operations are also tagged if they already appear in published physics problem-solving frameworks (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015), so that "new" is not confused with "absent from this course".

   This does not change K1, which is defined against the course's material. It prevents Stage A from reporting known PER principle-first moves as AI discoveries. The experiment note already acknowledges this confound for Stage B ("Explicitness" confound); this item applies it to Stage A reporting.
5. **§9 Phase 2, Stage B bullet.** Append:
   > An arm × pretest interaction is prespecified as exploratory (expertise reversal).

   The design already stratifies by pretest, so this is a reporting line, not a new arm. The Chi-style categorization task stays secondary: it is a noisy proxy (Mason & Singh 2011; Docktor et al. 2012) and must not be reported as transfer.
6. **§12 note 3.** Append:
   > Expert–novice differences are well replicated but form a continuum; instruction built on them has immediate, not yet delayed-transfer, evidence.
7. **§14.** Add Hardiman, Dufresne & Mestre (1989); de Jong & Ferguson-Hessler (1986); Mason & Singh (2011); Heller & Reif (1984); Mestre et al. (1993); Leonard, Dufresne & Mestre (1996); Docktor, Mestre & Ross (2012); Taconis, Ferguson-Hessler & Broekkamp (2001); Nokes-Malach et al. (2013); Docktor & Mestre (2014); Singh, Maries, Heller & Heller (2023); Kalyuga (2007). Dufresne et al. (1992), Docktor et al. (2015) and Chi et al. (1981) are already listed.

## Open questions

These are only the ones that would change the verdict:

- Is there a controlled university-physics study where instruction built on expert representations is tested against **delayed** transfer? A positive result would let the §4 cell drop "immediate"; a null would narrow the instructional claim to immediate performance.
- Does the Nokes-Malach et al. (2013) far-transfer effect replicate, and was its test delayed? The full text was not reached.
- Does principle-first instruction still help once students' pretest level is controlled, or only weak students (expertise reversal in physics)?
