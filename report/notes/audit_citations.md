# Citation claim-support audit (citation-verifier agent; saved by orchestrator)

Scope: 183 citation commands in 01, 03, 04, 09, 17, 19, 20. SUPPORTED 161; PARTLY 11; NOT SUPPORTED 3;
UNVERIFIABLE 9; UNSOURCED 2; bib metadata wrong 2 (+3 minor). All 17_validation methodological anchors
SUPPORTED. Full texts downloaded by the verifier: scratchpad/pdf/ (aghajani, andes, andes5, andesLL,
avelino16/19, clasheval, …). Also check research/pdf/ (local, git-ignored, read-only).

| file:line | key | claim | verdict | evidence | suggested fix |
|---|---|---|---|---|---|
| 03:186-189 | gourlay2006conceptualizing | SECI "three of its four modes have no evidence…" | NOT SUPPORTED | Abstract: "Three of the modes appear plausible but none are supported by evidence that cannot be explained more simply." | "…none of its four modes (three of which appear plausible) is supported by evidence that a simpler account cannot explain…" |
| 19:117-119 | cui2025large | LLM survey simulations under-disperse and over-detect nulls in 68–83% of replications | NOT SUPPORTED | 156 scenario-based psychology/management experiments; 68–83% = share of originally-null studies where LLMs gave significant results; under-dispersion is Bisbee's finding. | "LLM replications of 156 scenario-based psychology experiments produced significant results in 68–83% of the studies whose original finding was null, and larger effect sizes overall \parencite{cui2025large}." + bisbee2024synthetic for under-dispersion. |
| 19:77-78 | corbett1995knowledge | interpretable models (extended BKT, logistic regression) solve next-response prediction well enough | NOT SUPPORTED | 1995 paper cannot show later comparisons. | Cite a verified later comparison, or cut to "Bayesian knowledge tracing models mastery from graded responses \parencite{corbett1995knowledge}". |
| 20:123-125 | rigby2016quantifying | worst-case turnover losses >3× expected in two large projects | PARTLY | ES95 (mean of worst 5% quarterly losses, abandoned files) = 3.8× (Avaya), 3.6× (Chrome); simulations >5×. | "In Chrome and a project at Avaya, the mean of the worst 5% of quarterly knowledge losses (abandoned files) was 3.6–3.8 times the expected loss, and historical simulations of departures gave losses over five times the expected loss \parencite{rigby2016quantifying}." |
| 09:132-137 | wu2024clasheval | >60% expectation from ClashEval; ClashEval did not test multiple documents | PARTLY | >60% only GPT-4o (60.8%) and GPT-3.5 (62.6%) on prior-correct items; others 31–53% (Claude Opus 31.3%); §4.2 tested 5 documents and found LOWER context bias. | "ClashEval's >60% is GPT-4o's and GPT-3.5's rate on prior-correct items with the modified document as sole context (other models 31–53%); its own multi-document test lowered adoption; it did not test true-value pages alongside the plant." |
| 19:80-81 | lyu2026redesign | 2026 replication found no difference | PARTLY + bib | No difference in learning gains (N=123); process measures favored redesign. Real title "Evaluating a Data-Driven Redesign Process for Intelligent Tutoring Systems" (Lyu, Qianru; Borchers; Xia; Xiao; Carvalho; Koedinger; Aleven; AIED 2026). | "…found no difference in learning gains (N = 123), though process measures favored the redesign." Fix bib. |
| 19:79-80 | liu2017closing | gains "real, small, short…" (d=0.47, N=91) | PARTLY | d = 0.47 not small. | "real but shown only on an immediate post-test in one selected unit (d = 0.47, N = 91)" |
| 19:102-103 | vanlehn2011relative | ITS wide-CI effect over classroom instruction | PARTLY | d = 0.76 vs no tutoring, close to human tutoring 0.79. | "(d = 0.76 over no tutoring, close to human tutoring's 0.79)" |
| 19:113-115 | kieser2023chatgpt | human-like variance only once told which misconception to hold | PARTLY | Variance approximates human responses "in some regards". | "…produced variance that approximated human responses in some respects only once told which preconception to hold." |
| 01:40-44 | crandall1993critical | CDM elicited significantly more cues than unstructured interviews | PARTLY | "significantly more information … than in non-CDM interviews"; N=17 not in abstract. | "…significantly more information than non-CDM interviews…"; verify N = 17. |
| 03:109-113 | nathan2003expert | 48 preservice secondary mathematics teachers | PARTLY | 48 preservice secondary teachers with varying mathematics education. | "48 preservice secondary teachers; those with more advanced mathematics education…" |
| 01:87-90 | maries2016teaching, hinds1999curse | experts misjudged which steps novices find hard; more expertise did not help | PARTLY | Maries: 65%/68% vs 40% chance (above chance). Hinds measured completion times. | "…predicted novice difficulty only partly (well above chance, far from complete), and more expertise did not improve the predictions." |
| 20:59-61 | gao2023retrieval, es2024ragas | no existing enterprise RAG evaluation scores access-scoped retrieval… | PARTLY | Absence claim. | "…the standard RAG evaluation frameworks we found \parencite{…} do not score…" |
| 04:131 | argyle2023out | precedent for synthetic-as-predictor-only | PARTLY | Argyle argues pro-proxy. | Cite Argyle as the proxy method, Bisbee/Cui as the reason for the restriction. |
| 19:25-28 | vanlehn2005andes | Andes gains concentrated in diagram/variables, not equations | UNVERIFIABLE + bib | DOI = "Lessons Learned" IJAIED 15(3) 2005. | Check the rubric subscores in the paper's evaluation section (andesLL.pdf in scratchpad/pdf); keep or cut accordingly. |
| 01:36-40 | chao1994percentage | no expert >41/53/29%; six pooled 87/88/62% | UNVERIFIABLE | Abstract: coverage roughly doubled from one to six experts; three experts optimal. | Verify in paper tables or cut to "coverage roughly doubled from one to six experts". |
| 19:66-68 | bisra2018selfexplanation | g = 0.35 vs instructional explanation, k = 6 | UNVERIFIABLE | Abstract: 69 effect sizes, overall g = .55. | Verify moderator table or report overall g = .55 (k = 69). |
| 01:15,45,52 | clark2008cognitive | p.583 quote; p.584 25 of 70; p.589 70% | UNVERIFIABLE | Chapter PDF unreachable. | Check page numbers if a PDF is available; else drop page pins. |
| 03:29-30 | pinnow2016decoding | allocation not reported | UNVERIFIABLE (allocation only) | Ns/domain confirmed. | Keep only if method section checked; else drop the allocation clause. |
| 19:151-152 | kraft2020interpreting | typical effects 0.1–0.2 SD | UNVERIFIABLE | Abstract gives no numbers. | Quote Kraft's benchmark from the paper or soften. |
| 20:205-207 | aghajani2019software | outdated/incomplete/inconsistent info "dominant" failure modes | UNVERIFIABLE | Taxonomy of 878 artifacts, no ranking in abstract (aghajani.pdf in scratchpad/pdf). | Verify frequencies or say "prominent categories". |
| 20:115-116 | — | documentation problems a named barrier for OSS newcomers | UNSOURCED | — | Add verified Steinmacher et al. source or cut. |
| 20:138-140 | — | conformance checking "mature"; no public SOP+log corpus | UNSOURCED | — | Cite a verified conformance-checking reference; mark corpus absence as our search result. |

Minor bib: `schraagen2000cognitive` lacks editors (Schraagen, Chipman, Shalin); `jeong2024effects` key 2024 vs year 2025 (online Aug 2024) — fine to keep key, check year field.

## Resolution (2026-09-29)

Scratch build (`cfix/`, latexmk): 150 pages, 0 undefined citations, biber clean.

| row | key | action |
|---|---|---|
| 03 SECI | gourlay2006conceptualizing | Rewritten to the abstract: three modes appear plausible, none of the four supported by evidence a simpler account cannot explain; model omits inherently tacit knowledge. |
| 19 synthetic | cui2025large | Rewritten: 156 scenario-based psychology and management experiments; larger effects; significant in 68–83% of originally-null cases (verified in full text). Under-dispersion now cited to bisbee2024synthetic (abstract: "less variation"). |
| 19 adaptive practice | corbett1995knowledge | Cut to "BKT models mastery from graded responses". Prediction comparison now cited to added khajah2016deep (extended BKT indistinguishable from DKT, abstract) and gervet2020deep (logistic regression leads on moderate-size data, abstract). |
| 20 org table | rigby2016quantifying | Rewritten per suggested fix; 3.8×/3.6× (Avaya/Chrome) and >5× simulations verified in full text. |
| 09 E-PLANT | wu2024clasheval | Rewritten: >60% only GPT-4o (60.8%) and GPT-3.5 (62.6%), prior-correct items, sole context; others 31.3–52.9%; §4.2 multi-document test lowered context bias (all verified in full text). |
| 19 adaptive practice | lyu2026redesign | Now "no difference in learning gains (N = 123), though process measures favored the redesign" (verified, arXiv 2603.29094). Bib: full author list (7 authors); title/venue/DOI already correct. |
| 19 adaptive practice | liu2017closing | "real but shown only on an immediate post-test in one selected unit (d = 0.47, N = 91)". |
| 19 comparison class | vanlehn2011relative | "d = 0.76 over no tutoring, close to human tutoring's 0.79" (verified in full text). |
| 19 synthetic | kieser2023chatgpt | "variance that approximated human responses in some respects only once told which preconception to hold" (abstract wording). |
| 01 nursing | crandall1993critical | "significantly more information than non-CDM interviews" (abstract). N = 17 moved to its verified secondary source, clark2008cognitive p. 584. |
| 03 blind spot | nathan2003expert | "48 preservice secondary teachers" (abstract). |
| 01 principle selection | maries2016teaching, hinds1999curse | "predictions of what novices find hard were well above chance but far from complete, and more expertise did not improve them". |
| 20 World B | gao2023retrieval, es2024ragas | Marked as our search: "the standard RAG evaluation frameworks we found … do not score …". |
| 04 table | argyle2023out | Split: Argyle cited as the proxy method; Bisbee and Cui as the limits motivating the restriction. |
| 19 worked example | vanlehn2005andes | VERIFIED in "Lessons Learned" (IJAIED 15(3), local preprint; Table 5): hour-exam subscores Drawings 1.21, Variable definitions 0.69, Equations 0.11, Answers −0.08 (averages). Claim rewritten with these numbers and pinned to Table 5. Bib: full nine authors, vol. 15(3), pp. 147–204; DOI matches this paper. |
| 01 programming | chao1994percentage | 41/53/29% and 87/88/62% verified only in the secondary source (clark2008cognitive p. 585). Primary citation now carries only the abstract claim (coverage roughly doubled from one to six experts); the numbers are cited to Clark p. 585. |
| 19 instructional material | bisra2018selfexplanation | VERIFIED in full text, Table 1: instructional explanation k = 6, g = .354. Kept, pinned to Table 1. Bib: first name Kiran (was Kanwal), added 30(3):703–725. |
| 01 | clark2008cognitive | Page pins checked against the typeset chapter (pp. 577–593): "not available for introspection" p. 584 (was 583); "25 out of 70" p. 585 (was 584); "about 70%" p. 591, Conclusion (was 589). Pins corrected. |
| 03 DtD | pinnow2016decoding | Method section not available; allocation clause dropped. Following absence claim reworded as "We found no …". |
| 19 pilot | kraft2020interpreting | Verified in the working-paper full text: median 0.10 SD across 1,942 effect sizes from 747 RCTs with standardized achievement outcomes. "0.1–0.2 SD" replaced by that figure. |
| 20 org table + risks | aghajani2019software | Full text not obtainable (local file is an HTML page). "Dominant failure modes" and "common" cut; both passages now state only what the abstract supports (taxonomy from 878 artifacts in four sources; issues arise without scoring pressure). |
| 20 org table | — (newcomers) | Added steinmacher2014barriers (IFIP OSS 2014, open HAL copy read): documentation problems are one of five barrier categories for OSS newcomers. "No study of onboarding speed" marked as our search. |
| 20 org table | — (conformance) | "Mature" dropped. Added carmona2018conformance (Springer 2018) for conformance checking comparing event logs with process models; corpus absence and benchmark absence marked "our search found no / we found no". |
| bib | schraagen2000cognitive | Editors already present (Schraagen, Chipman, Shalin); no change. |
| bib | jeong2024effects | Year 2025 is correct for the issue (vol. 30(4), 4413–4433; online 29 Aug 2024). Author list completed (Lawler, Mike; Plummer, Kenneth J.). Key kept. |

Out of scope (files not assigned): the same Chao and Crandall figures are also cited in 17_validation, 21_domains, 23_workpackages and 27_contributions; they should use the same secondary-source attribution.
