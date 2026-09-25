# Falsify: Decoding the Disciplines (DtD)

**Question:** Does DtD's evidence support its role as the P0 method for eliciting hidden expert reasoning and improving novice learning in university physics?

**Verdict: narrow.** Keep DtD as the instructional frame: pick a bottleneck, then model, practise and assess. Drop the decoding interview (step 2) as the elicitation method and use CTA (§5.2) for that step instead. Lower DtD's evidence rating from "Moderate / developing" to "Low–moderate".

**§9 kill criterion:** not met. Phase 1 has not yet produced bottleneck data, so it can't be tested.

Baseline moved: §4 DtD row (P0, "Moderate / developing"), §5.1 card, §12 notes 1–2, "Current recommendation". Serves §9 Phases 1–2 and §10 RQ1, RQ2, RQ4.

Search: OpenAlex REST API (the `openalex` MCP server was not loaded this session), which covered all works citing Mohamed & Bayat (2022) and all works with "decoding the disciplines" in the title or abstract (144 records). One WebSearch for critiques and null results. The Zotero library (1,026 items, read from a local copy of the database because the Zotero local API was unresponsive) has no items on DtD, CTA or expertise, so there are no reading notes to cite. Citations checked by the `citation-verifier` agent, and its corrections are applied.

## Evidence

### DtD itself

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Mohamed & Bayat (2022), https://doi.org/10.20853/36-1-4517 | Systematic review with CASP appraisal. The stated inclusion criterion was qualitative studies, but the included studies also contain quantitative comparisons (e.g. Pinnow 2016, Lee-Post 2019). | 33 studies, 2004–2020 | Mixed disciplines, mostly outside physics | Thematic synthesis; no pooled effect | Reports positive themes. The authors say the literature may not be saturated enough for an in-depth review, and that the seven steps were not applied holistically, so more research is needed on whether the steps are interconnected. |
| Pinnow (2016), https://doi.org/10.1177/1475725716637484 | Two-group comparison, DtD vs lecture and readings; the abstract does not report how students were allocated (full text paywalled) | 91 (46 / 45) | Intro psychology, university; **outside physics** | Immediate performance | DtD group wrote better hypotheses and operational definitions and identified more variables |
| Lee-Post (2019), https://doi.org/10.1108/jarhe-03-2018-0049 | Exam scores compared between classes with and without the interventions (non-equivalent groups), plus end-of-course survey | Not stated in abstract | Business analytics; **outside physics** | Immediate course performance plus attitudes | Higher exam scores in the intervention classes |
| Elliott & Middendorf (2024), https://doi.org/10.20429/ijsotl.2024.180112 | Single-group pre/post, no control (pre-experimental) | 3 semesters | Psychological statistics; **outside physics** | Immediate performance | Significant pre-to-final gain. Uninformative about DtD because there is no counterfactual. |
| Yaqoob et al. (2025), https://doi.org/10.1155/hbe2/9930449 | Student questionnaire | Large cohort | Algorithm design (CS); **outside physics** | Preference only | Students preferred DtD. Not a learning outcome. |
| Durisen & Pilachowski (2004), https://doi.org/10.1002/tl.145 | Descriptive practice account | — | Astronomy (closest to physics) | None | Describes a decoding process for light and scale |
| Niebler (2023), https://doi.org/10.23919/eaeeie55804.2023.10181773 | Descriptive design report | — | Intro electrical circuits (physics-adjacent) | None controlled | Decoding plus a game-design analysis of student behaviour produced a problem-solving flowchart |
| Pace (2021), https://doi.org/10.20343/teachlearninqu.9.2.3 | Theory / overview | — | — | — | The paradigm has changed substantially since 2004 ("Decoding 2.0"), so "DtD" does not name a single fixed intervention. |

What this shows: no randomized trial of DtD was found. There are two small non-randomized comparisons (Pinnow 2016; Lee-Post 2019). Neither is in physics, and both measure only immediate performance. No study found measures retention or transfer, and no physics study reports a controlled learning outcome.

### Other methods for the elicitation step

| Source | Design | N | Domain | Outcome | Finding |
|---|---|---|---|---|---|
| Tofel-Grehl & Feldon (2013), https://doi.org/10.1177/1555343412474821 | Meta-analysis of controlled studies | "Relatively small number of studies" | Mixed training domains; **outside physics** | Post-training performance | CTA-based instruction Hedges' g = 0.871, varying substantially by CTA method and training context |
| Edwards et al. (2021), https://doi.org/10.1093/bjsopen/zrab122 | Systematic review and meta-analysis (10 RCTs, 2 observational) | 12 studies reviewed, N = 327 | Surgery; **outside physics and outside academic university teaching** | Procedural knowledge, technical performance | Pooled SMD 1.36 for knowledge (k = 4). Pooled SMD 2.06 for technical performance (k = 4, surgical trainees only), or 1.58 with the medical-student study included. |
| Feldon et al. (2010), https://doi.org/10.1002/tea.20382 | Controlled, double-blind comparison | 314 | Undergraduate biology lab course (university STEM; **outside physics**) | Course withdrawal; lab-report quality among completers (in-course performance, not transfer) | Instruction derived from CTA with expert biologists beat instruction written and delivered by an award-winning biology instructor. Withdrawal was 1.4% vs 8.1% of initial enrolment, with better analysis, alternatives and limitations in the reports. |
| Price et al. (2021), https://doi.org/10.1187/cbe.20-12-0276 | Qualitative: informal plus semistructured retrospective interviews, coded for decisions | 52 experts | Science and engineering, multiple disciplines | None (descriptive) | Interviews coded for decisions produced a cross-discipline set of 29 expert problem-solving decisions. That is a reusable elicitation product that DtD interviews don't provide. |
| Burkholder et al. (2020), https://doi.org/10.1103/physrevphyseducres.16.010123 | Correlational (exam solutions) plus 7 think-aloud interviews | Two Physics 1 courses | **Intro university physics** | Immediate exam performance | A template of expert decisions is correlated with successful problem solving, depending on problem type and difficulty |

Why the switch: the only designs at or above quasi-experimental that bear on the elicitation step come from CTA. Feldon et al. (2010) is the closest analogue to the §9 Phase 2 comparison: university STEM, with instruction written by an expert instructor as the control. The decoding interview itself has never been tested against another elicitation method.

## Against

These are the strongest points against *narrowing*, meaning in favour of keeping DtD's full P0 elicitation role:

- DtD is the only framework here that is **designed for university teachers in every discipline**. Much of the CTA training evidence comes from professional and procedural training (surgery, per Edwards et al. 2021), so its effect sizes may not carry over to conceptual and mathematical physics reasoning. Tofel-Grehl & Feldon (2013) themselves report large variation by method and context.
- Pinnow (2016) and Lee-Post (2019) are positive comparison-group results for DtD, and nothing shows the decoding interview is *worse* than CTA. The narrowing rests on missing DtD evidence, not on a negative head-to-head result.

These are the strongest points against the broader premise the map relies on for both DtD and CTA:

- Jeong et al. (2024), https://doi.org/10.1007/s10639-024-12962-y. Quasi-experimental, N = 390, two self-selected sections (180 vs 210), an online introductory physical-science course that the authors frame as introductory physics, immediate course performance. Decision-based learning, which teaches students expert decision sequences, was used for two lessons and had **no direct effect** on performance. A positive indirect path ran through self-testing. The dose was small, so this is not a null result for DtD or CTA. But it gives no evidence that briefly making expert decisions explicit improves physics learning (§11; §10 RQ4).
- Every CTA result above measures immediate or in-course performance. None measures transfer, so CTA also has not yet cleared §11's "include retention and transfer".

**No null DtD finding and no methodological critique of DtD were found** after a title and abstract sweep of all 144 DtD records in OpenAlex and a targeted web search. The published critiques are theoretical, for example about scope (bias and colonialism, the "disrupting" literature) and how theory is integrated, not about efficacy. The lack of nulls in a literature with almost no controlled designs is not evidence that DtD works.

## Implications for the map

1. **§4 DtD row.** Change the evidence strength to "**Low–moderate**: mostly qualitative; two small non-randomized comparisons, none in physics, no transfer". Append to "Why it matters": "use as the instructional frame; elicitation via CTA".
2. **§5.1 heading.** Change "**start here**" to "**start here as framing; elicitation narrowed to CTA**".
3. **§5.1 "Where it has been used".** Correct the review's description: it is a thematic synthesis with no pooled effect estimate.
4. **§5.1 "Evidence / limitations".** Add the graded summary: no RCT; two small non-randomized comparisons (introductory psychology and business analytics) with immediate outcomes; no physics study with a controlled outcome; no retention or transfer outcomes.
5. **§5.1 new subsection "Scope after falsification".** Keep steps 1 (bottleneck, selected from student data), 3–4 (model, practise and give feedback) and 6 (assess). Replace the decoding interview in step 2 with CTA (§5.2: CDM probes plus think-aloud on performed tasks). The decoding interview stays only as one arm of the §9 Phase 2 comparison.
6. **§12 note 1.** Change it to say that DtD is kept as the framing, and that its interview step is not evidential without CTA-style validation against performed tasks.
7. **§14.** Add Pinnow (2016), Feldon et al. (2010), Tofel-Grehl & Feldon (2013).
8. **Current recommendation.** Change "DtD → CTA" to "DtD (bottleneck framing) + CTA (elicitation)".

§5.2 (CTA) is not edited. The CTA evidence found here belongs to a separate `/branch explore "Cognitive Task Analysis"`.

## Open questions

These are only the ones that would change the verdict:

- Is there any controlled comparison of a decoding interview against a CTA method (CDM, think-aloud) on the number or validity of expert operations recovered, or on novice learning? A result where decoding matched or beat CTA would move the verdict back to **keep**. None was found, and this is the §9 Phase 2 experiment.
- Does Pace (2017), the mandatory book, report controlled outcome data not indexed as separate papers? The book has not been read. If it contains a quasi-experiment in physics or with a transfer outcome, the rating downgrade should be reconsidered.
