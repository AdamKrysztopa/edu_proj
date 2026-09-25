# Explore: Cognitive Task Analysis (CTA) / Knowledge Elicitation

**Question:** What evidence supports CTA as the expert-elicitation step for university physics, which CTA method fits, and how does it plug into the §6 architecture?

**Verdict: no change to priority (P0) or rating (Moderate–high); the rating is scoped.** The meta-analytic support is real, but it comes from training outside physics and measures immediate or in-course performance, not transfer. The card should name a provisional method: non-directed think-aloud while the expert solves the problem, followed by probes over the recorded trace.

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data.

Baseline: §4 CTA row (P0, "Moderate–high", STEM fit High, humanities Medium–high, AI readiness Very high), §5.2 card, §12 note 2. Since `falsify-decoding-the-disciplines.md`, CTA also replaces DtD step 2 (§5.1 "Scope after falsification"). Serves §9 Phases 1–2 and §10 RQ1, RQ2.

Search: OpenAlex REST API (the `openalex` MCP server was not loaded this session), covering the card's anchors (Crandall, Klein & Hoffman 2006; Hoffman, Crandall & Shadbolt 1998), CTA meta-analyses, work on the validity of verbal reports, CTA method taxonomies, and CTA in university STEM. One WebSearch for LLM-conducted CTA. Zotero was searched through its local API and has no items on CTA, think-aloud, verbal reports or expertise.

## Evidence

### Does CTA-based instruction work?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Tofel-Grehl & Feldon (2013), https://doi.org/10.1177/1555343412474821 | Meta-analysis of controlled studies | "Relatively small number of studies" | Mixed training domains; **outside physics** | Post-training performance | Hedges' g = 0.871, varying substantially by CTA method and training context |
| Edwards et al. (2021), https://doi.org/10.1093/bjsopen/zrab122 | Systematic review and meta-analysis (10 RCTs, 2 observational) | 12 studies, N = 327 | Surgery; **outside physics and outside academic university teaching** | Procedural knowledge, technical performance | Pooled SMD 1.36 for knowledge (k = 4). Pooled SMD 2.06 for technical performance (k = 4, surgical trainees only), or 1.58 with the medical-student study included. |
| Feldon et al. (2010), https://doi.org/10.1002/tea.20382 | Controlled, double-blind comparison | 314 | Undergraduate biology lab course (university STEM; **outside physics**) | Course withdrawal; lab-report quality among completers (in-course, not transfer) | CTA-derived instruction beat instruction written and delivered by an award-winning instructor. Withdrawal was 1.4% vs 8.1% of initial enrolment, with better data analysis, alternative explanations and limitations in the reports. |

This is the strongest evidence for any elicitation method on the map. But no study measures transfer, and none is in physics.

### Do experts omit what they know?

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Sullivan et al. (2014), https://doi.org/10.1097/acm.0000000000000224 | Descriptive comparison against a CTA-derived gold-standard task list | 3 teaching experts (+3 for the gold standard) | Surgery (cricothyrotomy); **outside physics** | Knowledge coverage, not learning | While teaching, experts omitted on average 71% of clinical-knowledge steps, 51% of action steps and 73% of decision steps. Prompted CTA probes raised coverage from 44% to 66%. |

This supports §11's "do not assume an expert can accurately verbalize their own cognition". The N is very small, and the domain is procedural rather than conceptual. Even prompted CTA recovered only two thirds of the steps.

### Which method? Validity constraints

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Fox, Ericsson & Best (2011), https://doi.org/10.1037/a0021663 | Meta-analysis | 94 studies, ~3,500 participants | Laboratory cognitive tasks; **outside physics** | Reactivity (whether reporting changes task performance), not learning | Non-directed think-aloud does not change performance (r = −.03). Procedures that ask people to describe or explain their thoughts do change performance, raising it compared with silent controls. All verbal reporting tends to slow the task. |
| Yates & Feldon (2011), https://doi.org/10.1080/1463922x.2010.505269 | Methodological review: frequency count of CTA methods across 1,065 studies; the most-published methods (60% subsample) coded | — | Cross-domain | — | Over 100 CTA methods exist and are inconsistently matched to their applications. CTA is "more craft than technology", with no robust basis for choosing one method over another. |
| Klein, Calderwood & MacGregor (1989), https://doi.org/10.1109/21.31053 | Method paper | — | Fire command, military, paramedics, engineering, programming | — | The Critical Decision Method (CDM) was built for naturalistic, time-pressured, incident-based decisions, adapting the critical incident technique with probes for cues, discriminations and typicality. |
| Hoffman, Crandall & Shadbolt (1998), https://doi.org/10.1518/001872098779480442 | Method case study | — | Cross-domain | — | CDM is multiple-pass retrospection over a specific event, guided by probe questions. The paper addresses data quality, reliability, efficiency and utility, and says these become more critical as CTA moves into field use. |
| Militello & Hutton (1998), https://doi.org/10.1080/001401398186108 | Method paper plus evaluation study | — | Applied/professional | Usability and usefulness | Applied CTA (ACTA) is a streamlined toolkit of three interview methods. In an evaluation study it was found easy to use, flexible and clear, and training materials built from it were judged accurate and important. |

What this means for physics:
- CDM was designed for recalling real incidents, but physics problem solving can be observed directly, so there is no need to rely on memory of a past event.
- Fox et al. show that asking people to describe or explain *while* solving changes their performance, so it presumably alters the process being studied.
- A defensible order is: (1) the expert solves the problem while thinking aloud, without prompts, and the written or diagram work is captured alongside; (2) CDM-style multi-pass probes over the recorded trace (cues, alternatives rejected, what a novice would miss); (3) comparison across experts.

This is a provisional choice. Yates & Feldon mean no study establishes the best method, and nothing here tests this order in physics.

### CTA-like work in university physics

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Price et al. (2021), https://doi.org/10.1187/cbe.20-12-0276 | Qualitative: informal plus semistructured retrospective interviews, coded for decisions | 52 experts | Science and engineering, multiple disciplines | None (descriptive) | Produced 29 expert problem-solving decisions that are shared across disciplines. The decisions rely on domain-specific predictive models. |
| Burkholder et al. (2020), https://doi.org/10.1103/physrevphyseducres.16.010123 | Correlational (exam solutions) plus 7 think-aloud interviews | Two Physics 1 courses | **Intro university physics** | Immediate exam performance | Using a template built from the expert decisions correlated with successful problem solving, depending on problem type and difficulty |

These are the nearest physics-domain applications. They show that the product of CTA-like elicitation (a set of decisions) can be used in physics instruction and assessment. Neither shows a causal effect on learning.

### AI opportunity (§5.2): LLM-conducted CTA

No study was found that evaluates an LLM conducting CTA interviews against a human interviewer or against observed expert performance. That included a targeted OpenAlex search for LLM interviewers and knowledge elicitation, and a WebSearch. Brown, Power & Gore (2024), https://doi.org/10.1177/10944281241271216, is a methods paper recommending CDM and ACTA for interview research. It is outside education and does not evaluate or propose AI-conducted CTA. The claim in §5.2 that an "AI interviewer can dynamically probe" has no evidence yet. It is the Phase 2 question.

## Against

- **Nothing in physics and nothing on transfer.** Every controlled CTA result measures immediate or in-course performance, and the large effects come from surgery and professional training (Edwards et al. 2021; Tofel-Grehl & Feldon 2013). Under §11 these do not show that CTA-derived physics instruction improves transfer.
- **Heterogeneity.** Tofel-Grehl & Feldon (2013) report large variation by method and context. The surgery pool for technical performance has I² = 87% before the medical-student study is excluded, and 61% after (Edwards et al. 2021, full text). A pooled g ≈ 0.9 should not be carried over to physics.
- **Physics null for teaching expert decisions.** Jeong et al. (2024), https://doi.org/10.1007/s10639-024-12962-y, was quasi-experimental with N = 390 across two self-selected sections of an online introductory physical-science course framed as introductory physics. Decision-based learning, which exposes students to expert decision sequences, was used for two lessons and had no direct effect on performance. A positive indirect path ran through self-testing. The dose was small, but it is the closest physics test of teaching an elicited set of expert decisions, and it found no direct gain.
- **CTA is "craft".** No method is validated as best (Yates & Feldon 2011). Even prompted CTA missed about a third of the steps (Sullivan et al. 2014).
- **Reactivity.** The probes listed in §5.2 (confidence, counterfactuals, "what would change your decision") fall into the describe/explain class that Fox et al. (2011) found reactive when used during the task.

## Implications for the map

1. **§4 CTA row.** Keep P0 and "Moderate–high", and qualify it: "**Moderate–high** for training outcomes outside physics; no physics or transfer outcomes". Keep the other cells.
2. **§5.2 "Evidence / limitations".** Add a short graded summary with:
   - the meta-analytic effects (g = 0.871; surgery SMD 1.36/2.06) and that they are immediate, in-course and outside physics;
   - Feldon et al. (2010) as the closest university-STEM study;
   - evidence that experts omit steps (Sullivan et al. 2014, small N);
   - the absence of transfer outcomes;
   - "more craft than technology" (Yates & Feldon 2011).
3. **§5.2 new subsection "Provisional method for physics".**
   1. Non-directed concurrent think-aloud while the expert solves the problem, with the written or diagram work captured alongside.
   2. After the task, CDM-style multi-pass probes over the recorded trace.
   3. Comparison across experts.

   Give the reasons in one line each: Fox et al. (2011) on reactivity; Klein et al. (1989) on CDM being designed for recalling incidents; Yates & Feldon (2011) on method choice.
4. **§5.2 "AI opportunity".** Add the constraint that AI probes run after the task, over the recorded trace, and never during solving. Add that no evaluation of LLM-conducted CTA was found.
5. **§5.2 "Questions to research next".** Leave the existing questions. The provisional method answers the first two only as hypotheses.
6. **§12 note 2.** Append: "no physics or transfer evidence yet; start with think-aloud on performed tasks plus retrospective CDM probes".
7. **§14.** Correct the Crandall, Klein & Hoffman (2006) DOI. The map gives `10.7551/mitpress/7301.001.0001`, which resolves in OpenAlex to a book titled "Workflow Management"; *Working Minds* is `10.7551/mitpress/7304.001.0001`. Add Fox, Ericsson & Best (2011), Sullivan et al. (2014), Yates & Feldon (2011) and Klein, Calderwood & MacGregor (1989).

## Open questions

These are only the ones that would change the verdict:

- Is there a controlled study, in physics or university STEM, of CTA-derived instruction with a **transfer** outcome? If it was positive, the scope qualifier could be removed. If it was null, the rating should drop.
- Does any study compare concurrent think-aloud plus retrospective probes against CDM interviews alone, measured by the number or validity of the operations recovered? That would confirm or overturn the provisional method.
