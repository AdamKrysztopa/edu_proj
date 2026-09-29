# Review C — hostile grant reviewer, Round 2

Document: `draft2.pdf` (143 pp.), sources `report/sections/*.tex`. Checked against the repository at 754e2e6 (research/n3/*/gapmap.json, REORIENTATION.md) and OpenAlex.

**Verdict: Reject in current form. Fundable only as a small seed grant for V1 (the closure study), or on resubmission after V1 has run.**

The document is unusually honest about its own failures, and that is to its credit. But honesty is not evidence. After the PoC, the one step that makes this a *gap* map rather than a lens-firing counter does not work. The applicant already knows the cheapest decisive next study, which needs no grant and no participants (14_interpretation.tex:138), and has not run it. The EUR 0.3–0.7 M lean phase is, by the applicant's own forecast, "most likely inconclusive" (00_executive_summary.tex:105; 29_conclusion.tex:41). In a round with a few awards, this loses to any proposal that has one positive signal.

## Scores (1–5)

| Criterion | Score | Justification |
|---|---|---|
| Significance | 3 | The premise is real: experts omit decisions and cues (Sullivan 2014; Chao & Salvendy 1994). But the evidence is 3–17 experts in one domain per study, and the report admits the rate is not general (01_problem). The practical payoff is a proposed 1.25× gain in validated items per expert hour (H3). That is modest, untested, and for an activity (CTA) whose cost is never quantified. No cost figure is given for organizational loss (20_organizations, Table 22), which is honest but leaves the "why fund" case asserted rather than shown. |
| Novelty | 2 | The claim is the *chain*, not any step (04_approach.tex:119–131). Closely related work is missing from the report. Construct-driven completeness checking of GDPR text is established: Torre et al. 2020, RE, doi:10.1109/re48521.2020.00025, and the Luxembourg follow-ups. This is the PoC's own domain, and it is exactly "expected element absent" detection. Underspecification and missing information in instructional text are also studied (Anthonio, Bhat & Roth 2020, LRE; Anthonio, Sauer & Roth 2022, LREC). Rationale extraction from issue trackers exists (DRMiner, ASE 2024, doi:10.1145/3691620.3695019; Dhaouadi et al. ICPC 2024). So does turnover-to-quality work (Foucault et al. FSE 2015, doi:10.1145/2786805.2786870). The E-OSS "beyond authorship" question sits inside an active software-engineering literature. The novelty ledger's "potentially novel" rows are therefore weaker than stated. |
| Rigor | 3 | The design discipline is excellent: pre-registration, a two-step freeze, a fair control built into the code, strongest-baseline-in-resample, κ adoption rules, memorization probes, and blinding checks. But the deciding gate reads a construct-adjacent proxy. V1 validates the wrong unit. The absence judge is unvalidated on the text type of the primary study. And the map is collinear with its strongest baseline by construction (findings 2, 4, 5, 7). |
| Feasibility | 2 | There is no host institution and no named team. Gold availability is unconfirmed beyond Sullivan. The dated-corpus mode, the Git adapter, the code lenses and the area score do not exist. The departure count needed for a gate is unknown. The lean schedule puts 26–40 PM of WP4+WP5 into months 11–17 with about 2.5–3.5 FTE. V5b at the proposed δ needs about 300 areas against a budget sized for about 80. |
| Team | 1 | "Nothing in this section has been assembled" (24_team.tex). The roles are well reasoned (24.1), but a panel scores people, not a role map. The PoC was one owner plus AI agents (15.1; Appendix I), and the single-operator risk is rated H/H by the applicant (26_risks). No track record, no letters, no host. |
| Clarity | 3 | The evidence labels (LIT/OBS/INT/HYP/FUT) and the "claims we do not make" box are exemplary. But the report is 143 pages. The executive summary is dense with internal jargon (aU = 5/24, "Continue branch closed on the validity floor", MS1/MS2/V1/E-OSS in one paragraph). Several internal contradictions remain (findings 10–14). A panel reader reaches the proposal only at p. 48. |

## What the PoC actually shows (my reading)

- **Shown:** a provenance ledger whose 909 stored evidence items re-slice exactly from local snapshots (these are git-ignored, so the check cannot be repeated from a clone). Also shown: lenses fire, the pipeline replays byte-identically, and built-in controls expose failure.
- **Not shown:** anything about expert knowledge. The admissible output is 25 gap candidates (PLC 24 uncapped, GDPR v1 1). Precision is 3/19 strict, judged by one AI reviewer on pre-final maps, with no committed tally.
- **The judge is uninformative.** Repo check: `mismatched_evidence_control` gives own = control on every lens. `own_rate` is 1.0 on most lenses, and the "other-source-only" ablation still closes 0.67–0.71. The judge says "closed/partial" to almost anything topical.
- **The ranking is density.** On PLC, ρ = 0.91 with source density.
- **N2 is inconclusive.** Its gated arms were never scored.
- **A buried number.** The one decoy measurement on v1 shows a 35% false-accept rate on PLC (A_claims.tex:93). It appears only in the appendix.
- **Sales verdict.** Not oversold in the body. It is undersold in one respect: the negative-control machinery is a genuine methodological asset. It is mildly oversold in the executive summary: "The mechanism works end to end, and it is checkable" leads, although its central step fails.

## Findings

### CRITICAL

**C1. The central step fails, and the decisive cheap test was not run before asking for money.**
- Location: 14_interpretation.tex:136–140; 00_executive_summary.tex:60–70; 10_n3.tex (fair control).
- Problem: every gap candidate depends on closure, and closure ties its control on every lens in every ledger. The applicant names V1 on the 107 existing firings as "the cheapest informative next study … before any money is spent on gold". It needs no participants, one blind coder and a codebook. Yet the proposal asks the funder to pay for it inside a 15–18-month, EUR 0.3–0.7 M S1.
- Evidence: the repo gapmap.json `checks.mismatched_evidence_control`: PLC own/control 0.889/0.889, GDPR v1 0.961/0.961, GDPR v2 0.958/0.958.
- Fix: before submission, double-code at least 100 of the 107 units with a non-owner coder. Report human–human κ, the prevalence of "not stated", and whether any judge (including one frontier model) separates own from control. If human κ < 0.70, the construct is unreliable and the proposal should be rewritten around that finding. If a judge passes, lead the executive summary with it.

**C2. The deciding gate is decided by a proxy for a different construct, using components that do not exist.**
- Location: 17_validation.tex:88–107, 200–222; 16_residual.tex:73; 22_roadmap.tex:135.
- Problem: MS3 can read Stop only through V3 (E-OSS). The report itself says V3 "tests an organizational construct adjacent to the HKR, not the HKR itself". V3 uses lens rules rewritten for commit, issue and PR text, a Git adapter, and code-unit areas, and "None of this exists" (17_validation.tex:211). A V3 Stop therefore kills H2 (expert residual in procedural prose) on evidence from a different gap map and a different construct. A V3 Continue licenses expensive expert studies on the same proxy. The CTA arm, the only one aimed at the stated construct, "cannot stop H2" (17_validation.tex:91).
- Fix: either (a) make the expert-construct arm able to read Stop, by pre-registering at least 3 CTA golds pooled by random effects, or by making V5b the deciding gate at an affordable δ with a budget to match; or (b) state that the program's first funded decision is about artifact coverage in software, and retitle H2 accordingly. Do not let V3 decide H2 as defined in 02_question.

**C3. The gates do not control the budget.**
- Location: 23_workpackages.tex:145 ("WP6 onward are written to run either way") vs 25_resources.tex:161–162 ("A stop at … MS3 … cuts the remaining budget"); 17_validation.tex:99; 26_risks.tex:155–165.
- Problem: on Stop or a double-inconclusive reading, the program pivots to "interview-only", and S2–S5 keep their workbench, recruitment and budget. On an inconclusive reading, V5 still starts if the point estimate is ≥ δ and the lower bound is > −δ/2. So a null-ish, underpowered MS3 still releases human-study money. From a funder's view the EUR 1–2.8 M is spent under nearly every MS3 outcome, and "kill criteria" kill a *claim*, not *spending*. The two sections also contradict each other.
- Fix: state which WPs and how many euros are released only on MS3 Continue. Budget the pivot as a separate, smaller line, and state the money at risk if H2 fails. Remove or tighten the "pre-registered minimum" route into V5, or justify it with a value-of-information argument.

### MAJOR

**M1. Stop is unreachable at the budgeted sample sizes except by attrition.**
- Location: 17_validation.tex:74–90, 270–282; 25_resources.tex:138.
- Problem: with δ = 0.05, Stop needs the upper 90% bound below 0.05. At the planned sizes the only ways to Stop are the map being clearly *worse* than the baseline, or the double-inconclusive rule:
  - V2: ±0.14–0.20.
  - V3: "tens" of clustered departures, likely ≥ ±0.10.
  - V5b: the budget covers about 40 experts ≈ 80 areas ≈ ±0.10, against about 300 areas needed.

  V5b is then "an estimation study with no gate", so MS5 Stop is unreachable as budgeted. A true ΔAUROC of 0 reads inconclusive everywhere.
- Evidence: the applicant's own planning arithmetic (17_validation.tex:79–85) and Table 30.
- Fix: size V5b to the gate or raise δ to what the budget can decide (and justify it). Add to Table 19 the "best reachable outcome" per gate at the budgeted n. This is the lesson the report itself draws from E-PLANT (09_n2, §9.3).

**M2. V1 validates absence within a retrieved pool, not absence in the corpus.**
- Location: 17_validation.tex:142–152; 16_residual.tex (definition: "E does not contain").
- Problem: a V1 unit is (lens, seed, missing element, *evidence pool*), and coders "see the evidence pool". The HKR and the residual-present label require absence from the *whole dated corpus*. The PoC retriever is lexical, and the report concedes that lenses "cannot see a paraphrase" (14_interpretation). A judge can agree with humans on the pool while the pool misses the stating sentence. The retrieval-recall part of the absence check is never validated.
- Fix: add a corpus-level arm to V1. For a random subset, a coder searches the full ledger or snapshot corpus for the element. Report retrieval recall beside judge κ, and gate on both.

**M3. The closure judge adopted at MS2 is never validated on the text type of the primary study.**
- Location: 17_validation.tex:144–146 vs 200–212.
- Problem: V1 units come from PLC/GDPR prose plus one non-gold prose domain. V3 applies closure to commit messages, issues and review threads under new lens rules. The adoption rule (κ ≥ 0.70) is thus checked on a distribution the decisive study does not use.
- Fix: include commit/issue units from non-sample repositories in V1, or register V3 without closure (lens firing plus coverage only), stating the narrower claim.

**M4. The map is structurally collinear with its strongest baseline.**
- Location: 10_n3.tex:253; 14_interpretation (density); 10_n3 triage (k_topic ≥ 2 for HYP; single-source goes to a retrieval gap); record.py rubric (A = source buckets).
- Problem: candidacy and rank are built from source counts, and density is a headline baseline. PLC ρ = 0.91. A ΔAUROC over density is then close to testing the residual of a variable against itself, and a null is the design's expected result, not evidence against the lens idea.
- Fix: pre-register a conditional analysis: AUROC within density strata, or the map's incremental value in a model that already contains density and area size. Report the partial correlation before MS1, as 17_validation.tex:51 half-proposes.

**M5. Schedule contradictions in the lean path make S1 infeasible as written.**
- Location: 23_workpackages.tex:280 (MS1, M5, freezes "lenses with their code adaptation for V3") vs 23_workpackages.tex:132 (Git adapter delivered M8, pilot M11, V3 result M17); 24_team.tex:46–60; 25_resources Table 28.
- Problems:
  - The code-text lenses must be frozen three months before the adapter they need exists. They are also to be developed "on repositories outside the departure sample", which needs that adapter.
  - WP4 (12–18 PM) and WP5 (14–22 PM) are mostly post-MS2 (M11–M17). That is 26–40 PM in about 7 months against a lean team of 2.5–3.5 FTE (about 17–25 PM).
  - "Dated-corpus reconstructions for two to three golds (M11)" falls one month after MS2, for a mode that is not built.
- Fix: move the V3 freeze to a separate MS1b after the adapter exists. Re-cost the lean path by month, or cut V2 from the lean path.

**M5b. The dated-corpus assumption for E-CTA is unexamined.**
- Location: 17_validation.tex (V2 design); 21_domains D1.
- Problem: "Reconstruct from a corpus frozen at the gold's publication date" (2014 for Sullivan) implies an open-web corpus as of 2014. The pipeline uses a commercial live search API with no date guarantee. Surgical procedure text is largely paywalled. The models postdate the gold, and the planner (an LLM) picks areas and queries from priors that include post-2014 content. Per-item memorization probes do not cover planner priors.
- Fix: specify the archive source (e.g. Common Crawl snapshots or the Wayback CDX), the date-verification rule, the expected corpus size, and a pilot showing a 2014-dated corpus of usable size can be built for the gold domain. Otherwise drop "dated corpus" as a claim.

**M6. Gate governance was overridden at the first test.**
- Location: 08_evolution.tex:66–75.
- Problem: rule R13 says a NOW item without a passing gate blocks the next. N2 read INCONCLUSIVE, and the owner started N3 anyway by "a single, recorded exception". Recording an override is better than hiding it, but a funder buying "pre-registered kill criteria" sees the first criterion softened by the person whose grant depends on it. The independence rule (24.3) does not cover the PI's own gate decisions.
- Fix: name an external gate reader (statistician or advisory board) with authority at MS2/MS3/MS5. State that owner exceptions require their sign-off.

**M7. Novelty positioning omits the closest prior work.**
- Location: 03_foundations.tex:245–258; 04_approach.tex:105–131, 140–153.
- Problem: the report says requirements-engineering precedent "works on one document … at the level of terms … does not type the missing knowledge". But Torre et al. (RE 2020) check GDPR privacy policies for *typed* required elements from a conceptual model. That is construct-driven absence detection in the PoC's own domain. Other uncited neighbours:
  - underspecification in instructional text (Anthonio et al. 2020, 2022);
  - rationale mining from issues and commits (DRMiner 2024; Dhaouadi et al. 2024), which is exactly V3's WHY lens;
  - turnover-quality effects (Foucault et al. 2015).

  REORIENTATION.md:529 also lists knowledge-at-risk (KaR) as an E-OSS baseline. The V3 baseline list in 17_validation.tex omits it.
- Fix: add these works to Table 3 and 4.3. Downgrade "methodology lenses as absence detectors" to *adaptation*. Add KaR or degree-of-knowledge as a V3 baseline.

**M8. The executive summary frames a failed mechanism as the main result.**
- Location: 00_executive_summary.tex:~55–70, 83.
- Problem: "The mechanism works end to end, and it is checkable. Its most important step does not yet work" puts plumbing first. "A failed one gives the field its first bounded test of the idea" is grant-speak: no bounded test is funded to be reachable (see M1).
- Fix: lead with the result: "Closure ties its control; prediction is untested; the next €X buys a κ and a retrieval-recall number on 107 existing units." Move the build inventory to the second paragraph.

**M9. The decoy false-accept rate is hidden in the appendix.**
- Location: A_claims.tex:93 (E20: PLC 35%, GDPR 15%); absent from 09_n2.
- Problem: `literature_supported`, the label every lens depends on, rests on a verifier that accepted a third of mutated PLC decoys in the only measured run. R2 (Appendix D) notes that decoy validity is self-certified, which cuts both ways. The main text reports only 12–30% scope drift.
- Fix: report E20 in 09_n2 with its caveat, and add it to the H1 status in Table 1.

### MINOR

**m1. Contradiction on Maries & Singh.** 19_education.tex:18 says "only just above chance". 03_foundations §3.4 reports 65–68% vs 40% for random guessers, which is well above chance. Fix 19_education.

**m2. The organizational framing mischaracterizes the corpora.** 20_organizations.tex:7 describes the PoC domains as "a PLC troubleshooting forum and manual, and … WP248". The PLC ledger is 35 fetched web pages, including vendor blogs (42 promotional seeds excluded). GDPR v1 support is 80% UK ICO/statute (A_claims.tex:85, E16), with three independence keys. Describe them as they are.

**m3. The VanLehn overreach is labeled LIT.** 19_education.tex:27–30: "exactly the steps instructors do not think to state … exactly the kind of step a methodology lens is designed to flag". VanLehn et al. 2005 shows where tutoring gains concentrated, not what instructors omit. Relabel it INT or delete it.

**m4. Pytest-archon contradiction.** 06_architecture.tex:14 says the repository does not install pytest-archon. A_claims.tex:73 (E10) says "verified live in this audit's own pytest-archon collection". Fix E10.

**m5. Glossary contradicts the body.** F_glossary.tex:61 says E-CTA is "gated on a pre-registered stop rule", but it cannot stop H2. F_glossary.tex:68 defines E-OSS as "gold from open, documented expert practice", but it is developer departures. Align both with 17_validation.

**m6. A claim that future work exists.** G_method.tex:45 (Appendix I) says "The report was revised after each round. A final audit then checked … and the compiled PDF was inspected page by page", while Round 2 is in progress. Write it in the future tense, or fill it in only after it happens.

**m7. Figure 14 caption vs legend.** 22_roadmap.tex:17 says "Solid stages are built and evaluated in sequence", but only S0 is solid and the legend says solid = complete. Fix the caption.

**m8. Marketing.**
- "Autonomous research" (18_platform.tex:127) names a single-pass pipeline that 06_architecture says has "no agent loop"; rename it "Reconstruction pipeline".
- "The program has two pivots, not a single point of failure" (26_risks.tex:155) is grant-speak.
- "the defensible position is the validated ΔAUROC" (26_risks, 26.1) presupposes validation.

**m9. V1 unit counts are inconsistent.**
- 23_workpackages.tex:79: "about 200 units per arm type from the three PoC ledgers plus one new domain".
- 17_validation.tex:144, 167: "107 admissible (two ledgers) + about 150 new-domain units per arm"; GDPR v2 for codebook training only.

Pick one.

**m10. Unmotivated planning assumption.** The AUROC 0.70 vs 0.62 assumption (17_validation.tex:79) has no basis. Say so, and show the half-widths under a smaller gap.

**m11. Headline counts mix admissible and inadmissible ledgers.** "155 lens firings on three ledgers" and "24, 1 and 6 gap candidates" in the executive summary include GDPR v2, which is not admissible. State the admissible totals (107 firings; 25 candidates) first.

## Top reasons to reject (in order)

1. No positive signal after the PoC, and the free decisive test (V1 on 107 units) was not run (C1).
2. The deciding gate reads a construct-adjacent proxy built from components that do not exist, and the CTA arm cannot stop (C2).
3. Spending continues under nearly every gate outcome; the kill criteria kill claims, not budget (C3).
4. No host, no named team, and a single operator (Team score).
5. At the budgeted sizes, Stop is reachable only if the map is worse than its baseline; a true null reads inconclusive (M1).
6. Novelty is overstated against uncited, directly relevant prior work (M7).
7. The lean schedule is internally inconsistent and under-staffed for WP4+WP5 (M5).

## Minimum changes that would flip my vote to "fund the lean phase"

1. **Run V1 now** (C1, M2): at least 100 double-coded units by a non-owner coder, human–human κ, corpus-level retrieval recall, and a judge panel against the fair control. Put the numbers on page 1.
2. **Make MS3 decide H2 as defined** (C2, M1): pooled multiple CTA golds, or an affordably powered V5b as the deciding gate. V3 relabelled as a separate organizational hypothesis that cannot kill or license H2.
3. **Make the money contingent** (C3): a euro figure released only on Continue; the pivot costed separately; no "pre-registered minimum" route into V5 without a value-of-information justification.
4. **Name a host institution, the PI's record, a statistician and a CTA collaborator** with letters, and an external gate reader (M6).
5. **Fix the V3 freeze timing and re-cost the lean path by month** (M5); specify the dated-corpus source (M5b).
6. **Rewrite the novelty section** against Torre et al. 2020, Anthonio et al., DRMiner and Foucault et al. (M7).

With items 1–4, this becomes a credible, well-controlled, falsifiable EUR ~0.3–0.5 M methods grant. Its main value would be the closure benchmark and a clean test of whether text absence predicts expert residual. Without them, it is a well-written plan to find out whether a component that currently fails can be made to work.
