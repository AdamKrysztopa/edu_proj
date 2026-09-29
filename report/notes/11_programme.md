# 11 — Future research program: domains, roadmap, work packages, team, resources, risks

Author: Grant / R&D Program Planner (worker note for the orchestrator). Date: 2026-09-29.
Feeds report sections 21 (domains), 22 (roadmap, Fig 12), 23 (work packages, Fig 13),
24 (team), 25 (resources), 26 (risks), 27 (contributions), 28 (impact), and the funding
paragraph of 29 (conclusion).

**Category tags.** **[LIT]** ESTABLISHED LITERATURE, **[POC]** OBSERVED IN THE PoC,
**[INT]** INTERPRETATION, **[HYP]** HYPOTHESIS, **[FW]** FUTURE WORK. Everything in this note
after section 0 is **[FW]** unless tagged otherwise: nothing in it has run. All numbers for
effort, money and time are **indicative planning ranges**, not estimates from data. Currency is
EUR unless a PoC figure was recorded in USD; USD figures are kept as recorded, not converted.

**Sources used.** `BRIEF.md`, `00_outline.md` (binding rulings), `01_evidence_audit.md`,
`04_results.md`, `06_platform.md`, `07_validation.md` (studies V0–V8, the spine of this plan),
`08_org.md`, `09_edu.md`, `REORIENTATION.md` §5, §7, §13–§22, `docs/lessons.md`.
**Citations.** Only keys already present and verified in `07_validation.bib`, `08_org.bib` and
`09_edu.bib` are used. No new literature is cited, so this note adds no `.bib` file.

---

## 0. Starting point (what the program inherits)

- **[POC]** The PoC is complete as engineering. N2 built a reconstruction pipeline with exact-span
  provenance (71/71 manual re-slices exact). N3 built a methodology-guided gap map that emits gap
  candidates and template-generated questions (`01_evidence_audit.md`; `04_results.md` §3).
- **[POC]** Hidden-knowledge prediction is not demonstrated. The absence check (closure) ties its
  fair control on every ledger: PLC 0.889 = 0.889, GDPR v1 0.961 = 0.961, GDPR v2 0.958 = 0.958
  (`research/n3/*/gapmap.json`, `checks.mismatched_evidence_control`). Precision 3 of 19 strict
  (8 of 19 lenient) is a *reported* figure from one adversarial AI review of the pre-final maps;
  its per-record tally is not committed.
- **[POC]** N2's research validation is deferred. The registered N2 gate reads INCONCLUSIVE. The
  recorded N2 spend is about $4.82 (E-LIVE $2.374, E-PLANT $1.953, E-ABST $0.495) against an
  OpenRouter key with a $5 weekly limit. The limit blocked E-LIVE v3 at its first call, with about
  $21 of registered caps unspent (`04_results.md` §1.5; `docs/lessons.md`). N3 could not afford a
  third domain ("the OpenRouter budget is $0", `research/n3/README.md`).
- **[POC]** The gap-map lexicons, denylist and stop-anchors were tuned in-sample on the three PoC
  ledgers (PLC, GDPR v1, GDPR v2; `config_sha256 35fd0af2…`). PLC and GDPR are therefore
  **development domains**, not test domains.
- **[INT]** So the program does not start from a working predictor. It starts from a pipeline, a
  set of checks that caught the pipeline's own failures, and one clear bottleneck: the absence
  check. The first money must buy a verdict on that bottleneck, not more features.

---

## 1. Domain strategy

### 1.1 Selection principles

Domains are chosen by **what generalization question they answer** and **what criterion exists**,
not by how easy the data are. Six axes matter:

| Axis | Why it matters |
|---|---|
| Knowledge type that dominates | Diagnostic craft (cues, checks), perceptual-motor procedure, normative-interpretive judgement (hedges, exceptions), design rationale ("why"), conceptual/learner difficulty. The lenses were derived from methodologies built for different types; each type is a separate test. |
| Documentation density | Text-rich domains flatter reconstruction (`REORIENTATION.md` §16 R3). A claim of generality needs a text-poor domain (RQ-I). |
| Human criterion | Retrospective published gold (CTA task lists), realised-loss outcomes (departures), or fresh blind elicitation. Without a criterion a domain can only debug the pipeline. |
| Learner data | Needed for any claim about learner difficulty (`09_edu.md` §3). Experts and expert-written text cannot answer "what is difficult" **[LIT]** (nathan2003expert; maries2016teaching). |
| Contamination risk | Old gold is in pretraining and has diffused into textbooks **[LIT]** (golchin2023time; sainz2023nlp). Post-cutoff or fresh criteria are the clean legs. |
| Validation purpose | **Scientific validation** asks "does the gap map predict the residual, beyond baselines?" **Commercial validation** asks "does a payer get value, legally, at acceptable cost?" A domain can serve one, both, or neither. Easy data is not a reason to include a domain. |

Three binding rules shape the set:
1. **Physics is the frozen Track A domain.** Introductory mechanics enters the program only through
   E-SEAL (sealed, script-generated, non-gating). NOW runs exclude conservation items. Anyone who
   has seen reconstructed conservation content is ineligible for any Track A human role
   (interviewer, corroborating coder, K1 "absent" coder, importance rater;
   `REORIENTATION.md` §18.1).
2. **Held-out gold domains are not reconstructed first.** No exploratory, debugging or tuning run
   touches a gold domain before the configuration is hash-frozen and the study is pre-registered.
   The first reconstruction of a gold domain *is* the test run, on a corpus dated before the gold.
   The notes already hold the structure of some golds (e.g. Sullivan's 46 steps split 14/27/5,
   `REORIENTATION.md` §14.3), so the pipeline is sandboxed from `research_notes/`.
3. **Development domains stay development domains.** PLC and GDPR tuned the lexicons. They may be
   used for debugging, for the V1 closure set (with a new non-gold domain added), and for a V5b
   *pilot* that is not analyzed for effect. They must not carry a decisive test.

### 1.2 The domain set (six domains, four decisive)

| # | Domain | Generalization question it tests | Gold / human criterion | Text density | Learner data | Main risks | Purpose |
|---|---|---|---|---|---|---|---|
| D1 | **Clinical procedural skill** (surgical airway; NICU cue recognition as fallback) | Does the gap map find omitted steps and cues in a **perceptual-motor, decision-heavy procedure**? | Retrospective CTA gold: Sullivan et al. cricothyrotomy task list, 46 items, 44% unprompted / 66% prompted recall **[LIT]** (sullivan2014use). Fallback golds: Crandall & Getchell-Reiter NICU cues (crandall1993critical; itemised list availability **unverified**). | Medium: concepts rich, cues poor | Few public | Contamination (2014 gold, diffused into guidelines); one gold gives only ±0.14–0.20 on ΔAUROC (`07_validation.md` §2) | **Scientific** (V2, primary gold) |
| D2 | **Open-source software maintenance** (knowledge-at-risk after developer departure) | Does **artefact coverage of design rationale** predict realised knowledge loss beyond authorship concentration? (RQ-H) | Realised-loss outcome: blind-coded rationale-seeking issues and defect-fix commits after a truck-factor developer leaves **[LIT]** for the risk (avelino2016novel; avelino2019abandonment; rigby2016quantifying; nassif2017revisiting) | Medium; rationale poor | None | Repositories in pretraining (mitigate with post-cutoff outcome windows); authorship metrics may break after agentic coding (`REORIENTATION.md` R8); effective n ≈ number of departures | **Scientific** (V3, the best-powered retrospective test) and **commercial precursor** for the software wedge (V7) |
| D3 | **Industrial fault diagnosis** (maintenance troubleshooting; PLC/SCADA as the development subdomain) | Does the method hold where **diagnostic craft** dominates and text is **poor**? (RQ-I) | Retrospective: Chao & Salvendy troubleshooting data **[LIT]** (chao1994percentage); PARI aircraft-maintenance task list (hall1995procedural; availability **unverified**). Prospective: blind elicitation with technicians (V5b). Narrative, community-held diagnostic knowledge is documented **[LIT]** (orr1996talking) | Low (terse, jargon-heavy) | Apprentices (V8c) | PLC ledger is in-sample; low reconstruction support; recruiting technicians; no clean natural experiment | **Scientific** (text-poor falsification target; V5b decisive domain) and **commercial** (second-wave maintenance partner) |
| D4 | **Regulatory judgement** (a held-out regulation; GDPR/DPIA as development subdomain) | Does the method work on **normative-interpretive judgement**, where the residual sits in hedges and exception boundaries ("in most cases")? | No public itemised gold. Criterion: prospective blind elicitation of practitioners (V5b), expert raters (V5a). Work-as-imagined vs work-as-done frame **[LIT]** (hollnagel2018safety) | High for rules, low for case judgement | None | GDPR ledger is in-sample (and GDPR v2 is not N3-admissible); practitioners may disagree legitimately, so "residual" and "opinion" must be separated by corroboration | **Scientific** (V5b second decisive domain); **commercial** only later (audit defensibility has no benchmark, `08_org.md` §4) |
| D5 | **School mathematics** (middle school) | Does an expert-text residual relate to **learner difficulty**, or are they different constructs? (V8a; RQ-E) | Learner response data: Eedi misconception data and NeurIPS 2020 responses (wang2020neuripschallenge; licence **unverified**), DataShop logs (stamper2011datashop; terms **unverified**) | High | Rich, public | Licences (NC datasets unusable commercially); gap map reads expert-voiced text, so a null is likely and informative | **Scientific only** (learner link; not a calibration set for other domains) |
| D6 | **Introductory mechanics** (Track A) | Best-case ceiling; the only place where expert residual, learner error and a learning RCT meet in one topic | Track A's own registered K0/K1/K2; E-SEAL sealed predictions scored after K1 is locked | Very high | Track A cohort (≈ 370) | Contamination (FCI in pretraining); eligibility rule; must not change any registered rule | **Scientific, secondary and non-gating** (V8b) |

**[INT]** D1–D4 are the four decisive domains. They span four knowledge types (procedural-
perceptual, design rationale, diagnostic craft, normative judgement) and the full density range.
D5 and D6 test the learner link and the ceiling. No domain was included because its data are
convenient: mathematics has the easiest data but is scientific-only, because it measures learner
difficulty, not the expert residual (`REORIENTATION.md` §19).

### 1.3 Choice for the prospective study (V5b)

`07_validation.md` suggests PLC as V5b's diagnostic domain because it is already reconstructed.
That conflicts with rule 3 above: the lexicons were tuned on the PLC ledger.

- **Option A (Recommended): V5b pilot in PLC, V5b main in two held-out subdomains** — a fresh
  maintenance-diagnosis task (D3) and a held-out regulation (D4), each reconstructed once, after
  the freeze, on a dated corpus. Evidence: `config_sha256 35fd0af2…` was tuned on the PLC and GDPR
  ledgers (`research/n3/README.md`, Limitations), so any PLC effect is optimistic. The pilot is not
  analyzed for effect, so in-sample tuning does not bias it. Cost: one extra reconstruction per
  domain (tens of euros of API) and a new area partition.
- Option B: V5b main in PLC and GDPR. Cheaper by one partition each, but the decisive human study
  would test a configuration on its own tuning data.
- What would change the recommendation: if no reachable expert pool exists for a fresh maintenance
  subdomain, keep PLC but re-tune nothing, state the in-sample status in the pre-registration, and
  treat the PLC result as supporting, not decisive.

### 1.4 Order of entry

1. D1 and D2 first (Research Validation; V2, V3). They decide the N3 program gate.
2. D5 in parallel (V8a; public data; no participants).
3. D3 and D4 after the gate (V5, V6), with PLC/GDPR only as pilot and debugging domains.
4. D6 whenever Track A's own preconditions are met; never scheduled by this program.
5. A **new, non-gold development domain** (for V1's out-of-sample closure units) is picked at V0
   and never used as a test domain. Candidate kind: a second maintenance or regulatory task.

---

## 2. Roadmap: gated stages

Each stage names the hypothesis it tests, what gets built (only what the stage's evidence needs),
the evidence required, and continue / stop criteria. Gates read experiment results, not builds
(`REORIENTATION.md` §16 R13). Durations are indicative.

| Stage | Hypothesis tested | What gets built | Evidence required | Continue if | Stop / pivot if | Duration |
|---|---|---|---|---|---|---|
| **S0 PoC — COMPLETE** | H1 partly (reconstruction with provenance is feasible); H2 mechanism only | `residual/`, `reconstruct/`, `gapmap/`; three gap maps | **[POC]** Engineering complete; N2 INCONCLUSIVE; N3 "pipeline complete, prediction not demonstrated" | — | — | Done (Sept 2026) |
| **S1 Research Validation** (V0–V4, V8a) | L0 trustworthy inputs; L1 absence check is informative; L2 gap map beats the strongest baseline on retrospective gold; L3 residual measurable | Frozen config and area partitions; admissibility as code; dated-corpus mode with gold blocklist and memorization probes; closure codebook and judge panel; World B Git adapter (public repositories only) | V1: judge–human κ; V2: ΔAUROC on ≥ 1 CTA gold; V3: clustered ΔAUROC over departures; V4: known-truth check | **N3 program gate:** lower 90% bound of ΔAUROC > 0 and point ≥ δ on the primary test (V3 carries most power; V2 may read "inconclusive by design") | Upper 90% bound < δ → **pivot to H3** (elicitation efficiency, no reconstruction prior). V1 fails → closure coded by humans or dropped (V2 still runs, narrower claim). V4 fails → drop residual as an objective | 15–18 months |
| **S2 Research Prototype / MVP** (V5a, V5b pilot) | Experts can tell real gap candidates from decoys; blinded prospective elicitation is feasible and measurable | Elicitation workbench: question service, blind-arm separation, World C records, segmentation and coding tools, residual accounting (`ObservedResidual`), cost per validated item. Track A components reused **by copy** | V5a real-vs-decoy AUROC of ratings; pilot base rate of "residual present", intra-expert correlation, coding α, blinding leakage | Rater discrimination above chance; pilot yields a required sample size the budget can buy; α ≥ 0.667 | Raters at chance → revise candidate generation once, then stop H1 targeting; required n unaffordable → V5b becomes an estimation study (no gate) | 6–8 months (build overlaps S1) |
| **S3 Multi-domain Validation** (V5b main, V6) | L4 predictions hold on fresh blind elicitation in held-out domains; L5a targeting saves expert time | Workbench hardened for two domains; leave-one-domain-out runs; EIG question selection (N6) | Prospective ΔAUROC per domain (clustered by expert and area); validated items per expert hour, targeted vs untargeted | V5b: lower 90% > 0 and point ≥ δ; V6: lower bound of ratio > 1 and point ≥ SESOI (proposed 1.25×) | V5b upper 90% < δ → **stop the H1 claim** (publish as negative result; keep H3 tool if V6-H3 passes). V6 upper bound < SESOI → stop the efficiency claim | 12–16 months |
| **S4 Organizational Pilot** (V7) | L5b: predicted gaps match what staff add and where departures or onboarding cause trouble in one partner | World B ingestion for one tenant: ACL-respecting retrieval, on-prem judge stack (three model families), artefact-coverage mode, pseudonymization, audit trail | DPIA done; works agreement where required; retrospective hit rate or ΔAUROC; prospective G vs D/R hit rate | G beats D and R in both parts; legal route workable | DPIA or works council blocks; outcome not measurable from records; G ≤ D or R | 8–14 months (legal prep overlaps S3) |
| **S5 Education Pilot** (V8c, education materials pilot) | L5c: confirmed residual areas carry more novice errors; teaching validated residual items changes a delayed outcome | Materials built **only from validated items** (criterion-labelled); novice task set; manipulation-check logging | V8c error excess at matched difficulty; pilot compliance and manipulation checks | Error excess with CI > 0; compliance ≥ 70% | No excess → expert residual ≠ learner difficulty (report; do not build learner features on it). A later powered RCT uses K2-style futility at a pre-set SESOI | 9–15 months; RCT later |
| **S6 Full Platform** | Commercial: the validated primitive (residual accounting per unit) is usable, legal and worth paying for | Multi-tenant platform, connectors, compliance defaults in the core, residual corpus with tenant isolation | Validated ΔAUROC per domain and type (from S3), a working partner pilot (S4), cost per validated item | ≥ 2 partners renew or pay; legal review clean | S3 stop → no platform on H1; S4 legal block repeated → no organizational product | 18–36 months after S3/S4 |

**Parallel streams.**
- Inside S1: V1 (closure set) runs in parallel with the V3 pilot and the Git adapter; V8a (public
  learner data) runs independently; V2 waits for V1's verdict; V4 runs on V2 data.
- S2's engineering starts during S1 (month 10), but **no expert is recruited for new tracks before
  the S1 gate** (`REORIENTATION.md` §20).
- S4's partner scouting and legal preparation run in parallel with S3; S4's data work waits for
  V3's reading and N2's deferred validation (E-PLANT, E-ABST), because partner documents raise the
  injection and false-support stakes.
- S5's V8c runs alongside late S3 in a V5 domain.
- Track A runs on its own preconditions at any time. It is never scheduled or blocked by a gate
  here.

**The H3 branch.** If the S1 gate fires the stop rule, V5 is not run in its H1 form. S2 builds
the same workbench without the reconstruction prior, and V6 runs as the H3 test ("EIG without the
reconstruction prior vs untargeted CTA"). S4 and S6 then target an elicitation-efficiency tool,
not a residual predictor.

---

## 3. Work packages

WPs follow the program's logic chain (L0–L5c), not a generic template. Months are counted from
program start (M1). The plan assumes a 48-month grant-scale program; the lean variant (section 4)
funds WP1–WP5 and WP9a only.

### WP1 — Pre-registration, governance and data protection
- **Objective.** Every gate is fixed before its data exist, and every human-data step is legal.
- **Key tasks.** Fill the §22 threshold table (δ = 0.05 recommended in `07_validation.md`; SESOI for
  V6; tolerances for V4). Hash-commit each study's pre-registration after a `methods-critic`
  review. Ethics approvals for V5/V6/V8c. Licence checks before any dataset download. DPIA and
  works-council preparation for V7. Budget-headroom rule (section 5.2). Staff eligibility registers
  (Track A roster; per-domain advisor vs participant lists).
- **Dependencies.** None; starts at M1.
- **Deliverables.** D1.1 threshold table and V1–V4 pre-registrations (M5); D1.2 ethics approval
  for V5/V6 (M18); D1.3 V5b/V6 pre-registrations (M20, M28); D1.4 DPIA and data agreement for V7
  (M28); D1.5 final data-management and open-data report (M48).
- **Milestones.** MS1 (M5): V1–V4 pre-registered and hash-committed.
- **Expertise.** PI, statistician/methodologist, data-protection counsel, project manager.
- **Risks.** Thresholds set after data are seen; ethics delay pushes S2; legal cost of V7.

### WP2 — Freeze, admissibility and deferred N2 validation (V0)
- **Objective.** Make pipeline outputs admissible as inputs to a gold test (L0).
- **Key tasks.** Hash-freeze `gapmap/src/gapmap/config.py` and the feature set. Admissibility as
  code (every located extraction has a verdict; cross-verify and decoys ran; `complete` derived from
  `failed_calls_by_task`). Report live vs dead features. Dated-corpus mode with DOI/title gold
  blocklist. Run the deferred N2 protocols as registered (E-LIVE v3, E-PLANT run 2, E-ABST run 2
  with second coding), after a baseline-calibration pilot that prints the best reachable outcome.
- **Dependencies.** WP1 (budget rule, prereg).
- **Deliverables.** D2.1 frozen config and admissibility checker (M4); D2.2 N2 deferred-validation
  report (M8).
- **Milestones.** MS1 (shared, M5): no hash, no gold.
- **Expertise.** Research engineer, LLM/retrieval engineer; one blind second coder (E-ABST).
- **Risks.** Live runs expose new defects (they did in N2); provider limits; N2 reads Stop (then
  V7 does not start).

### WP3 — Absence-check validation (V1)
- **Objective.** Decide whether "is this element really unsaid?" can be judged reliably (L1).
- **Key tasks.** Closure codebook with anchors per lens. Build about 200 units per arm type (own vs
  swapped evidence) from the three PoC ledgers plus one new non-gold domain. Double-code blind.
  Score a judge panel (local 7B, a stronger open-weight judge, other-family judges). Rerun the fair
  control with the best judge.
- **Dependencies.** WP2 (frozen config), WP1 (codebook fixed before coding).
- **Deliverables.** D3.1 closure codebook (M5); D3.2 human-labelled closure set, released (M9);
  D3.3 closure verdict report (M10).
- **Milestones.** MS2 (M10): closure verdict — automated judge adopted / human-coded closure /
  closure feature dropped.
- **Expertise.** Cognitive psychologist (CTA practitioner) for the codebook; statistician; two
  coders (non-owner for the gating κ); LLM engineer.
- **Risks.** Human–human κ < 0.70 (construct unreliable); coder drift; judge overfits the codebook.

### WP4 — Retrospective CTA gold test and residual check (V2, V4)
- **Objective.** First test of RQ-B against published human-revealed gold (L2), and of whether the
  residual can be measured (L3).
- **Key tasks.** Check itemised gold availability by metadata only. Build area partitions from a
  dated pre-gold source. Reconstruct on a corpus frozen at each gold's date (first and only
  reconstruction of the gold domain). Acquire gold, sealed. Per-item memorization probes, exclusion
  of probe-positive items. Map gold to areas (blind double coding). Score ΔAUROC against the
  strongest §14.3 baseline, chosen inside each bootstrap resample. V4 known-truth check on V2 data.
- **Dependencies.** WP2 (freeze, dated corpus), WP3 (closure verdict decides what V2 tests).
- **Deliverables.** D4.1 dated-corpus reconstructions for 2–3 golds (M11); D4.2 V2 result per gold
  and pooled (M15); D4.3 V4 residual known-truth report (M17); D4.4 public reconstruct-vs-CTA
  benchmark release (M20).
- **Milestones.** MS3 input (M15).
- **Expertise.** LLM/retrieval engineer; statistician; CTA practitioner; clinical advisor (not a
  coder, not a participant); two coders.
- **Risks.** Gold unobtainable; one gold underpowered (±0.14–0.20); contamination; unmappable items.

### WP5 — Developer-departure natural experiment (V3)
- **Objective.** Test RQ-B in the organizational family with realised loss as the outcome (L2).
- **Key tasks.** World B Git adapter (commits, blame at *t*, issues, PRs, reviews, dated docs), public
  repositories only. Pilot on 5 departures: base rate, intra-repository correlation, coding time.
  Compute the number of departures giving a 90% ΔAUROC half-width ≤ δ. Main study if obtainable,
  else pre-register as descriptive. Blind double coding of rationale-seeking issues and defect-fix
  commits; staggered-adoption difference-in-differences **[LIT]** (callaway2021difference).
- **Dependencies.** WP2 (freeze); WP1 (legitimate-interest record, pseudonymization).
- **Deliverables.** D5.1 Git adapter with provenance (M8); D5.2 pilot report and power decision
  (M11); D5.3 V3 result (M17); D5.4 coded post-departure dataset, pseudonymized (M20).
- **Milestones.** MS3 input (M17).
- **Expertise.** Data/backend engineer; mining-software-repositories researcher (AI/ML role);
  statistician; two coders with software literacy.
- **Risks.** Too few departures with enough post-departure activity; authorship metrics after
  agentic coding; repositories in pretraining.

**MS3 (M18): N3 program gate.** Reads V2 and V3 under the §22 rule. Continue H1 / inconclusive
(one fallback gold) / pivot to H3.

### WP6 — Elicitation workbench (research prototype)
- **Objective.** The minimum software that V5 and V6 need to run blind, logged and codable.
- **Key tasks.** Question service (template questions now; EIG later, N6) with an
  unknown-unknowns fraction. Blind-arm separation (the interviewer view never shows scores or
  strata). World C records into the ledger. Segmentation and coding tool with blinding checks.
  Residual accounting and cost per validated item. Copy the Track A turn contract, leading-question
  guard and corroboration code into the new package; never import `instrument/`.
- **Dependencies.** WP2 (ledger contract). Engineering starts M10; human use only after MS3.
- **Deliverables.** D6.1 workbench v1, tested on simulated, labelled sessions (M20); D6.2 v2 for two
  domains with EIG selection (M26).
- **Milestones.** MS4 (M24) uses it.
- **Expertise.** Research software engineer, frontend/HCI (interviewer and coder views), LLM
  engineer, CTA practitioner (script and channel design).
- **Risks.** Tooling drift (building before the gate reads; `REORIENTATION.md` R13); leakage of
  scores into interviewer or coder views.

### WP7 — Prospective expert validation (V5a, V5b, V6)
- **Objective.** Test whether predictions hold on fresh, blind human elicitation (L4) and save
  expert time (L5a).
- **Key tasks.** V5a expert raters with decoys (6–10 per domain). V5b pilot in PLC (6 experts × 12
  areas, not analyzed for effect). V5b main in two held-out subdomains (D3, D4) with strata G/D/L/R,
  neutral CDM probes **[LIT]** (klein1989critical), 3 experts per area **[LIT]** (chao1994percentage).
  V6 crossover, targeted vs untargeted, with question-seeded coding **[LIT]** (loftus1975leading).
- **Dependencies.** MS3 (continue or H3), WP6, D1.2 ethics.
- **Deliverables.** D7.1 V5a report (M22); D7.2 V5b pilot report and sample-size decision (M24);
  D7.3 V5b main result (M34); D7.4 V6 result (M40); D7.5 residual corpus v1 (M40).
- **Milestones.** MS4 (M24) prototype gate; MS5 (M34) prospective gate; MS6 (M40) efficiency gate.
- **Expertise.** CTA practitioner (interviewer training), trained interviewers per domain,
  statistician, coders, domain advisors (independent of participants), HCI.
- **Risks.** Expert recruitment; fatigue; interviewer effects; required n above budget.

### WP8 — Organizational pilot (V7)
- **Objective.** Test transfer to one partner (L5b) and whether the legal route is workable.
- **Key tasks.** Partner selection (software organization first, `08_org.md` §5). DPIA,
  legitimate-interest balancing test, works agreement where German co-determination applies, data
  agreement (no training on partner data; on-prem or equivalent). Retrospective part (departures
  or onboarding tickets as outcome). Prospective part (V5b design, 1–2 critical units).
- **Dependencies.** V3 reading (WP5), N2 deferred validation (WP2), WP10 on-prem stack, WP1 legal.
- **Deliverables.** D8.1 signed partner and data agreements (M26); D8.2 retrospective result (M34);
  D8.3 prospective result and feasibility report (M42).
- **Milestones.** MS7 (M42) organizational gate.
- **Expertise.** Data-protection counsel, project manager, data/backend engineer, security
  engineer, CTA practitioner, statistician.
- **Risks.** Partner access; works-council veto; surveillance framing; prompt injection through
  internal documents **[LIT]** (greshake2023not).

### WP9 — Learner link and education pilot (N4, V8a, V8c, education pilot, E-SEAL interface)
- **Objective.** Test whether expert residual relates to learner difficulty, and whether teaching
  validated residual items changes anything measurable.
- **Key tasks.** (a) V8a and N4 on public mathematics data (E-KC, E-DIST, E-MISC) after licence
  checks. (b) E-SEAL interface to Track A: sealed gap-map scores, if the owner approves adding them
  before Stage A. (c) V8c novices (30–60) in a V5 domain, with a 10-novice pilot. (d) Education
  materials pilot built from validated items only, run as a manipulation check (one course section
  or apprentice cohort), not a powered RCT.
- **Dependencies.** (a) WP2 only; (c) and (d) need D7.3.
- **Deliverables.** D9.1 V8a/N4 report (M16); D9.2 V8c result (M44); D9.3 education pilot
  feasibility report and RCT pre-registration draft (M48).
- **Milestones.** MS8 (M44) learner-link gate.
- **Expertise.** Learning scientist, educational data scientist, statistician; a partner teaching
  institution or training provider.
- **Risks.** Licences (non-commercial terms); null learner link (likely and informative); learner
  data protection; Annex III(3)(b) if individual outcomes are evaluated.

### WP10 — Platform groundwork and World B infrastructure
- **Objective.** Turn PoC properties into the platform's core without building features ahead of
  evidence.
- **Key tasks.** Typed run-status record (replace the untyped sidecar). Ledger storage that scales
  beyond one JSON per run. ACL propagation to labels (a claim inherits its evidence's most
  restrictive ACL). Erasure design (pseudonym key outside the ledger; `source_withdrawn`). On-prem
  stack with three model families (generator, verifier, closure judge from different families).
  Hash-chained audit trail. Compliance defaults in the core (artefact-coverage mode).
- **Dependencies.** Decisions from WP3 (judge choice) and WP5 (World B adapter).
- **Deliverables.** D10.1 typed run status and scalable ledger (M18); D10.2 on-prem judge stack
  (M26); D10.3 ACL, erasure and audit design, implemented for the V7 tenant (M30); D10.4 platform
  architecture decision record for S6 (M46).
- **Milestones.** Supports MS7.
- **Expertise.** Data/backend/platform engineer, security engineer, MLOps, legal input.
- **Risks.** Building for customers before S3 reads; on-prem judges weaker than hosted ones.

### WP11 — Open benchmark, residual corpus and dissemination
- **Objective.** Make the program's outputs reusable whatever the verdicts are.
- **Key tasks.** Release the closure set (D3.2), the reconstruct-vs-CTA benchmark (D4.4), the
  coded departure dataset (D5.4), a residual corpus subset under consent (D7.5), and all
  pre-registrations and negative results. Papers per gate.
- **Dependencies.** WP3–WP9 outputs; licences and consent from WP1.
- **Deliverables.** Releases at M12, M20, M40, M48; papers after MS2, MS3, MS5, MS6, MS7.
- **Expertise.** PI, research engineer (packaging), all study leads.
- **Risks.** Gold licences forbid redistribution (release mappings and code, not gold text).

### 3.1 Gantt specification (one figure, Fig 13)

Horizontal axis M1–M48, quarters marked. One bar per WP. Diamonds are gates; a diamond with a
fork icon marks a stop/pivot point. Bars after MS3 are drawn hatched with the note "only if MS3
reads continue or H3".

| Bar | Start | End | Notes on the bar |
|---|---|---|---|
| WP1 Pre-registration, governance, data protection | M1 | M48 | Tick marks at D1.1 (M5), D1.2 (M18), D1.4 (M28) |
| WP2 Freeze, admissibility, deferred N2 validation (V0) | M1 | M8 | |
| WP3 Absence-check validation (V1) | M3 | M10 | |
| WP4 CTA gold test + residual check (V2, V4) | M3 | M20 | Light segment M3–M5 "metadata check"; M11 "gold unsealed" tick |
| WP5 Departure natural experiment (V3) | M3 | M20 | Tick at M11 "power decision" |
| WP9a Public learner data (V8a, N4) | M6 | M16 | Separate short bar |
| WP10 Platform groundwork | M10 | M48 | |
| WP6 Elicitation workbench | M10 | M26 | Segment M10–M18 "engineering only, no recruitment" |
| WP7 Prospective expert validation (V5a, V5b, V6) | M19 | M40 | Hatched (conditional) |
| WP8 Organizational pilot (V7) | M14 | M42 | Segment M14–M26 "scouting + legal"; data from M27; hatched after M27 |
| WP9b Novices + education pilot (V8c, materials) | M32 | M48 | Hatched |
| WP11 Open benchmark and dissemination | M10 | M48 | |
| Track A (frozen; own preconditions) | — | — | Separate dashed rail below the chart, no dates, arrow "E-SEAL: sealed, non-gating" |

| Milestone | Month | Gate rule (few words) |
|---|---|---|
| MS1 | M5 | Config hash-frozen; V1–V4 pre-registered |
| MS2 | M10 | Closure: judge κ ≥ 0.70 and own–control gap within ±0.10 of humans' |
| MS3 | M18 | **N3 program gate**: ΔAUROC vs strongest baseline; continue / inconclusive / pivot H3 |
| MS4 | M24 | Raters above chance; pilot-derived n affordable |
| MS5 | M34 | Prospective ΔAUROC ≥ δ (lower 90% > 0) |
| MS6 | M40 | Items per expert hour ≥ SESOI |
| MS7 | M42 | Org pilot: G beats D and R; legal route workable |
| MS8 | M44 | Novice error excess in confirmed residual areas |

---

## 4. Team

### 4.1 Three configurations

- **Lean research team (S1 only; 15–18 months; about 2.5–3.5 FTE).** PI/research lead (0.8–1.0),
  research engineer with LLM/retrieval skills (1.0), statistician/methodologist (0.2–0.3), CTA
  practitioner as consultant (0.1–0.2), two coders paid by the hour (a few hundred hours in total),
  data-protection/licence advice ad hoc. **[INT]** This is enough to read the N3 program gate.
  It removes the PoC's largest structural risk: one operator who is also the only coder.
- **Grant-scale team (S1–S5; 48 months; about 5–7 people, 3.5–5 FTE on average).** The lean team
  plus a cognitive psychologist/CTA researcher (postdoc), a data/backend engineer, a learning
  scientist (from S2/S5), HCI (part-time, WP6–WP7), a project manager (part-time) and legal counsel
  for V7.
- **Product/platform team (S6; only after S3 and S4 read continue).** Product manager, 2–4
  backend/platform engineers, frontend engineer, security engineer, MLOps, implementation/customer
  engineer, compliance and data-protection officer, plus the research core (PI, statistician,
  CTA researcher) to keep calibration and validation running per domain.

### 4.2 Roles

| Role | Why the competence is needed | When (stage / WP) | FTE (grant-scale) | Permanent or consultant |
|---|---|---|---|---|
| PI / research lead | Owns hypotheses, gates and pre-registrations; resists tooling drift; signs off every threshold before data | S0–S6; WP1, all gates | 0.5–1.0 | Permanent |
| AI/ML researcher (evaluation, mining software repositories) | ΔAUROC designs, baselines, memorization probes, V3 repository mining | S1–S3; WP4, WP5 | 1.0 | Permanent |
| LLM / retrieval engineer | Dated-corpus mode, judge panel, cross-family verification, EIG selection, on-prem models | S1–S4; WP2–WP4, WP6, WP10 | 0.5–1.0 (can merge with the research engineer in the lean team) | Permanent |
| Research software engineer / data-backend-platform | Admissibility as code, Git adapter, ledger at scale, typed run records, audit trail | S1–S6; WP2, WP5, WP6, WP10 | 1.0 | Permanent |
| Frontend / product engineer | Interviewer and coder views that cannot leak scores; later product UI | S2–S6; WP6, S6 | 0.3–0.5 in the grant; 1.0 in S6 | Permanent in S6; contract before |
| Cognitive psychologist / expertise researcher (CTA practitioner) | Closure codebook, elicitation scripts, channel-per-type design, interviewer training, corroboration rules. This is the core human-science skill the PoC lacked | S1 (codebook) → S3; WP3, WP6, WP7, WP8 | 0.5 (S1) → 1.0 (S2–S3) | Permanent (postdoc) |
| Learning scientist | V8a/N4 analyses, novice study, instructional materials from validated items, RCT design later | S1 (V8a, small) and S5; WP9 | 0.2 → 0.5 | Permanent part-time or partner institution |
| HCI / human factors | Blinding in the interfaces; expert fatigue; how experts use ranked questions; usability for partner staff | S2–S4; WP6–WP8 | 0.3–0.5 | Consultant or part-time |
| Statistician / methodologist | Threshold table, clustered ROC, min-over-baselines bootstrap, power decisions from pilots, equivalence logic; holds analysis code before unblinding | S1–S5; WP1, WP3–WP9 | 0.3–0.5 | Permanent part-time |
| Coders / research assistants | Blind double coding in V1–V8; the gating κ must not depend on the owner | S1–S5 | Hourly; about 1,000–2,000 h over the program | Hourly contracts |
| Domain experts as **advisors** | Area partitions, scope decompositions, plausibility of materials, recruitment networks | Per domain, before the domain's freeze | 0.05–0.1 per domain | Consultant, domain-specific |
| Domain experts as **participants** | V5a raters, V5b/V6 interviewees, importance raters | S2–S3; WP7 (and WP8 staff) | Honoraria per hour | Participants, domain-specific |
| Project / product manager | Schedules, reporting, partner contracts, budget headroom checks | S1 (light) → S6 | 0.2–0.5; 1.0 in S6 | Permanent part-time |
| Security / privacy / legal | GDPR (DPIA, legitimate interest, erasure), works councils, AI Act classification, dataset licences, TDM rights | S1 (licences), S4 (DPIA, works council), S6 | 0.1–0.2 plus external counsel for V7 | Consultant; permanent DPO in S6 |

**Independence requirements (binding for staffing).**
1. **Advisor vs participant.** A domain advisor who helped build an area partition, saw the gap map
   or saw candidate content may not be a V5a rater, V5b/V6 interviewee, importance rater, coder or
   corroborator in that domain. Keep a per-domain eligibility register (WP1).
2. **Track A roster.** Anyone who has seen reconstructed conservation content is ineligible for any
   Track A human role (`REORIENTATION.md` §18.1). Program staff who handle mechanics runs are
   therefore excluded from Track A roles; E-SEAL predictions are generated by script without display.
3. **Owner cannot be blind.** The PI built the lenses. Gating κ values come from non-owner coders;
   owner codes only under origin blinding, reported as such.
4. **Interviewers and coders never see scores or strata.** A guess-the-stratum check on 20% of
   areas measures leakage (`07_validation.md` V5b).
5. **Analysis independence.** The statistician commits the analysis script before unsealing gold or
   unblinding strata. AI agents may draft code and text, but agent agreement is not evidence and
   no agent is a coder of record.

---

## 5. Resources and indicative timeline

All figures are **indicative**. They are planning ranges for a grant proposal, not estimates from
data. Personnel cost per person-month varies by a factor of two or more across European
countries and institution types; the range used below is EUR 6,000–10,000 per person-month fully
loaded. Replace it with the host institution's rate.

### 5.1 Person-months per WP (grant-scale, 48 months)

| WP | Person-months | Main roles |
|---|---|---|
| WP1 Pre-registration, governance, data protection | 18–26 | PI, PM, statistician, counsel |
| WP2 Freeze, admissibility, deferred N2 (V0) | 5–8 | Research engineer, LLM engineer |
| WP3 Absence-check validation (V1) | 6–9 | CTA researcher, statistician, LLM engineer |
| WP4 CTA gold test + residual check (V2, V4) | 12–18 | AI/ML researcher, LLM engineer, statistician |
| WP5 Departure natural experiment (V3) | 14–22 | AI/ML researcher, backend engineer, statistician |
| WP6 Elicitation workbench | 16–26 | Research software engineer, frontend/HCI, CTA researcher |
| WP7 Prospective expert validation (V5, V6) | 30–44 | CTA researcher, interviewers, statistician |
| WP8 Organizational pilot (V7) | 12–20 | PM, backend/security, counsel, CTA researcher |
| WP9 Learner link and education pilot | 14–22 | Learning scientist, statistician |
| WP10 Platform groundwork | 20–34 | Platform/backend, security, MLOps |
| WP11 Open benchmark and dissemination | 6–10 | PI, research engineer |
| **Total** | **≈ 150–240** | ≈ 3.2–5.0 FTE on average |

Coder hours are counted under participant costs (5.3), not in the table.
**Lean variant (S1 only):** WP1 (light), WP2–WP5 and WP9a ≈ 40–60 person-months over 15–18
months.

### 5.2 Compute and API budgets (orders of magnitude)

**What the PoC tells us.** **[POC]** One E-LIVE v1 domain run cost $0.68 (PLC) and $0.50 (GDPR)
with the models then used (`04_results.md` §1.2). The whole of N2 cost about $4.82. That money was
not the constraint; **headroom** was. A $5 weekly key limit, set below the roughly $21 of
registered caps, stopped E-LIVE v3 at its first call and left N2 inconclusive on budget, not on
evidence (`docs/lessons.md`). **[INT]** The lesson is about limits and planning, not price.

**Why later stages cost more per run.** Research validation needs, per gold or domain, at least
three reruns (retrieval variance dominated cross-run instability, `04_results.md` §4), two or three
model families (generator, verifier and judge must differ), stronger models than the PoC's
defaults, plain-LLM baselines, memorization probes per gold item, and larger corpora (repository
histories in V3).

| Stage | Driver | Order of magnitude |
|---|---|---|
| S1 hosted API | Roughly 50–300 reconstruction-scale runs (golds, V1 new domain, V3 repositories, reruns, families) at a few euros to a few tens of euros each, plus baselines and probes | EUR 10³–10⁴ (plan EUR 3,000–15,000) |
| S1 local inference | Stronger open-weight closure judges and memorization probes on open-weight models with documented cutoffs: one GPU workstation, or rented GPU hours | EUR 5,000–20,000 one-off, or EUR 2,000–10,000 per year rented |
| S2–S3 | Workbench question service, EIG selection, local speech-to-text for interview audio, re-runs in two new domains | EUR 10³–10⁴ |
| S4 | On-prem stack with three model families for one tenant (may be partner-provided) | EUR 10⁴ (hardware or partner in-kind) |
| S6 | Multi-tenant inference and storage | EUR 10⁴–10⁵ per year; depends on tenants and on-prem share |

**Budget rules (proposed here, from the PoC failure).**
1. Provider limits must be at least 3× the sum of registered caps for the stage, on a monthly, not
   weekly, window. Read and record both numbers in each protocol before the first run.
2. The headroom check runs as code before a run sequence starts, not as a note.
3. One key per experiment, so one study cannot exhaust another's budget.
4. Report cost per validated item (E-COST), not cost per claim.

### 5.3 Participant, coder and learner costs

Planning units come from `07_validation.md`. Hourly rates vary widely by country and profession;
the ranges below are honoraria or wages, not market consulting rates.

| Item | Volume (planning range) | Rate range | Cost range |
|---|---|---|---|
| V5a expert raters | 2 domains × 6–10 experts × 0.5–1 h ≈ 6–20 h | EUR 60–200/h | EUR 0.5k–4k |
| V5b pilot | 6 experts × 1–1.5 h ≈ 6–9 h | EUR 60–200/h | EUR 0.4k–2k |
| V5b main + importance raters | ≈ 40 experts × 1–1.5 h + 10–16 raters × 2–3 h ≈ 60–110 h | EUR 60–200/h (technicians and compliance staff at the low end, clinicians at the high end) | EUR 4k–22k |
| V6 efficiency study | 2 domains × 20–30 experts × 1.5–2 h ≈ 60–120 h | EUR 60–200/h | EUR 4k–24k |
| Recruitment overhead | Agencies, professional bodies, scheduling | +20–50% of honoraria | EUR 2k–25k |
| V7 partner staff | 6–12 staff × 1–2 h | Usually partner in-kind | EUR 0–5k |
| Coders, all studies | ≈ 1,000–2,000 h (V1 30–50; V2 40–180; V3 150–500; V5 330–550; V6 300–500; V7 50–150; V8c 50–150) | EUR 20–45/h | EUR 20k–90k |
| V8c novices | 30–60 × 1.5–2 h (+10 pilot) | EUR 15–30/h, or apprentice partner in-kind | EUR 1k–4k |
| Education pilot | One course section or cohort, 100–150 learners, course-embedded | Small incentives or none | EUR 0–3k plus instructor time |
| Gold acquisition | Library access, author contact, licences | — | EUR 0–5k |

Participant, coder and learner costs together: **roughly EUR 30k–185k.** Other direct costs
(legal counsel for V7, open-access fees, travel, ethics fees): **roughly EUR 30k–100k.**

### 5.4 Indicative totals and timeline

| Configuration | Duration | Personnel | Other direct costs | Indicative total |
|---|---|---|---|---|
| Lean (S1: reads the N3 program gate) | 15–18 months | 40–60 PM | EUR 20k–60k | **≈ EUR 0.3–0.7 M** |
| Grant-scale (S1–S5 up to the education pilot) | 48 months | 150–240 PM | EUR 80k–370k (participants, coders, compute, legal, other) | **≈ EUR 1–2.8 M** |
| Product (S6) | 18–36 months after S3/S4 | Team of 8–15 | Hosting, sales, compliance | Not a research-grant cost; outside this estimate |

**Uncertainty.** The largest unknowns are (1) the V5 sample size, which comes from the pilot and can
move WP7 by a factor of two; (2) the number of usable departures in V3; (3) whether V7's legal
work is weeks or many months; (4) host-institution rates. A stop at MS3 or MS5 cuts the remaining
budget; the program is designed so that a stop is a result, not a waste.

---

## 6. Risks, kill criteria and pivots

Likelihood and impact are qualitative (L/M/H). "Kill/pivot" states the pre-registered or proposed
rule.

| Risk | Likelihood / impact | Early signal | Mitigation | Kill / pivot criterion |
|---|---|---|---|---|
| **Central scientific kill: the gap map does not beat the strongest baseline** (R1) | M / H | V2 point estimate near 0; PLC score already tracks density (ρ = 0.91, **[POC]**) | Density and area size as headline baselines; min-over-baselines inside the bootstrap; δ fixed before gold | Upper 90% bound of ΔAUROC < δ on the decisive retrospective tests (V2/V3) → **pivot to H3**. Upper bound < δ in V5b → **stop the H1 claim** entirely |
| **Absence check (closure) cannot be made informative** | H / H | **[POC]** own = control on every ledger; V1 human–human κ < 0.70 | Codebook with anchors; stronger and other-family judges; human-coded closure as fallback | No judge meets κ ≥ 0.70 and human-bound rule → human closure or drop the feature. Human–human κ < 0.70 twice → construct unreliable; V2 tests lens firing plus density only (narrow claim). If closure passes and the map still does not beat density and size → the methodology layer adds nothing (stricter kill, to register) |
| **Gold unavailable or too small** | M / H | Metadata check finds no itemised list; < 15 missed areas per gold | Fallback golds pre-registered; pooled random-effects ΔAUROC; "inconclusive by design" rule | No primary or fallback gold obtainable → V3 and V5b carry L2; state that the retrospective clinical test did not run |
| **Contamination / memorization** (R2) | H / M | Probe-positive share high; recall on old gold far above post-cutoff | Corpus dated at gold date; per-item probes and exclusion; open-weight models with known cutoffs; post-cutoff and fresh-elicitation legs | Probe-positive items dominate a gold → report recall as upper bound, drop that gold from the gate |
| **In-sample tuning leaks into tests** | M / H | Tuning request after gold seen | Hash-freeze before gold; leave-one-gold-out and leave-one-domain-out; PLC/GDPR as development only | Any change to frozen config after gold → result reported as exploratory, not as a gate reading |
| **Retrieval noise masks the signal** | H / M | **[POC]** GDPR v1 vs v2 share only 3 of 13 and 3 of 9 candidates | Dated frozen corpus; ≥ 3 reruns; report stability | Cross-run agreement stays low under a frozen corpus → gap map not reproducible; stop before human spend |
| **Residual not measurable** (R4) | M / M | V4 simulation shows estimator bias under dependence | Known-truth check with fixed tolerance | Out of tolerance → drop residual as objective; report observed counts only |
| **Too few OSS departures** | M / M | V3 pilot base rate low; high intra-repository correlation | Power decision after pilot; review-weighted concentration; pre-agent histories | Required departures unobtainable → V3 descriptive; organizational L2 moves to V5b/V7 |
| **Partner access** (S4) | M / H | No letter of intent by M20 | Start scouting at M14; software partner first; offer artefact-coverage mode only | No partner by M28 → run V7 on a second public OSS setting and report organizational transfer as untested |
| **Expert recruitment** (S2–S3) | M / H | V5a fills slowly; no-shows | Professional bodies, honoraria, short sessions (≤ 75 min), 3 experts per area | Pilot-implied n unaffordable → V5b as estimation study, no gate claim |
| **Ethical / legal** (R10) | M / H | DPIA finds high residual risk; works council objects | Artefact-coverage mode; pseudonymized concentration; no evaluation use; on-prem; AI Act Annex III watch | DPIA or works council blocks → stop V7 at that partner; product design reconsidered before S6 |
| **Surveillance framing and Goodhart** | M / M | Staff see outputs as monitoring; coverage becomes a KPI | Aggregate by default; consent for naming; contract bans evaluation use | Partner uses outputs for evaluation → terminate pilot |
| **Prompt injection via internal documents** (R11) | M / M | Retrieved spans acting as instructions | Retrieved text is data; ACL-enforced retrieval; flagged spans held PENDING | Unresolved injection path → no World B deployment |
| **Budget exhaustion mid-study** | L–M / M | Key limit below sum of caps | Section 5.2 rules | A study stopped by budget reads inconclusive and is rerun, never re-interpreted |
| **Track A contamination** | L / H | Program staff assigned to Track A roles | Eligibility register; script-only E-SEAL | Any breach → that person removed from Track A role; logged |
| **Team: single operator and key-person risk** | H (lean) / H | One person codes, builds and decides | Non-owner coders; statistician; second engineer | Key person lost in S1 → pause at the last gate; no unreviewed gate readings |
| **Tooling drift** (R13) | M / M | A stage ends with software and no gate reading | Gates read results; WP6 human use only after MS3 | Any stage ending without a reading is recorded as a plan failure |
| **Incumbents fold coverage accounting into platforms** (R9) | M / M (commercial only) | Vendor ships "undocumented knowledge" features | Differentiate on validated ΔAUROC and the residual corpus | Commercial pivot: license the benchmark and method rather than build S6 |

---

## 7. Expected contributions and impact

### 7.1 Scientific contributions, graded

| Contribution | If the hypothesis holds | Even if it fails |
|---|---|---|
| Human-labelled closure (absence-check) set with a codebook and fair control | A validated way to judge "unsaid in this evidence" | A measured answer to whether LLM judges can decide absence; a benchmark for others |
| Public reconstruct-vs-CTA benchmark (dated corpora, area partitions, gold mappings, probes) | First measured ΔAUROC of residual prediction on CTA gold | A reusable test for any reconstruction or "what's missing" system, with contamination controls |
| Coded post-departure dataset (OSS) | Evidence that artefact coverage adds to authorship concentration | Evidence that it does not; a public outcome set for knowledge-loss research |
| Residual corpus (validated expert-added items, type, channel, prior score) | Training and calibration data for gap maps | The first typed record of what experts add beyond text, useful to CTA research regardless |
| Pre-registered negative results | — | A falsification of "text reconstruction locates the human residual" with bounded effect sizes, which the field lacks |
| Elicitation-efficiency evidence (V6) | Targeted elicitation saves expert time by a measured ratio | Bounds on the gain; the H3 tool tested on its own terms |
| Learner link (V8a, V8c) | Residual areas predict learner and novice errors | Evidence that expert residual and learner difficulty are different constructs, as the expert-blind-spot work suggests **[LIT]** (nathan2003expert) |
| Methods | Provenance ledger with epistemic labels; gates computed by code; min-over-baselines bootstrap | Same; they do not depend on the verdict |

### 7.2 Practical impact (conditional and sober)

- **[HYP]** If V5b and V6 pass: CTA practitioners start interviews with a ranked list of likely
  gaps and spend less expert time per validated item. The size of that saving is unknown until V6;
  the proposed SESOI is 25% more yield per hour.
- **[HYP]** If V3 and V7 pass: organizations get a knowledge-at-risk view per component that adds
  artefact coverage to authorship concentration, in artefact-coverage mode. The risk is real and
  measured in software **[LIT]** (avelino2016novel; rigby2016quantifying); whether our score adds
  value is the open question. No credible cost-of-knowledge-loss figure was found, and none is
  claimed (`08_org.md` §4).
- **[HYP]** If V8c and an RCT pass: instruction that states validated hidden steps. Field effects
  of education interventions are usually small **[LIT]** (kraft2020interpreting), so expected
  gains are modest even on success.
- **[INT]** If the central hypothesis fails, the practical output is an elicitation tool (H3) and
  public benchmarks, not a residual predictor.

---

## 8. Funding instrument fit (types only)

No specific call or deadline is named. Eligibility depends on a host institution, which the
program needs in any case (ethics approval, employment of coders, data protection).

| Stage | Type of instrument | Why it fits |
|---|---|---|
| S1 (lean) | National science foundation grants for basic or early-career research (cognitive science, learning sciences, computer science panels) | Zero participants, method-focused, clear falsification test, small budget |
| S1–S3 | Investigator-driven frontier research grants (if the PI profile fits) | High-risk, high-gain question with pre-registered kill criteria |
| S1–S5 | EU Horizon Europe collaborative projects, in clusters on education and inclusive society, or on digital technology and AI | Multi-partner (university, training provider, industrial partner), cross-domain validation, open benchmarks |
| S4 | Industry–academia collaborative R&D (national or regional innovation agencies; co-funded industrial research) | One partner's artefacts, legal work, on-prem deployment; partner in-kind contribution |
| S5 | Education research funders and teaching-innovation programs at the host institution | Course-embedded pilots, learner data under ethics approval |
| S6 | Innovation or deployment instruments and private investment | Product build; not research. Only after S3 and S4 read continue |

**[INT]** The strongest fit for the next step is a single-institution grant that funds S1 alone.
It buys the N3 program gate, the closure verdict and three public datasets at the lowest cost,
and every later instrument can cite its result, positive or negative.

---

## 9. Findings that matter most (for the orchestrator)

1. **[INT]** Six domains, four decisive (clinical procedure, OSS departures, industrial diagnosis,
   regulatory judgement), chosen by knowledge type, density and criterion. Mathematics and mechanics
   serve the learner link and the ceiling only.
2. **[INT] Conflict flagged:** `07_validation.md` suggests PLC as a V5b main domain, but PLC and
   GDPR tuned the lexicons. Recommended: PLC for the V5b pilot only; held-out subdomains for the main.
3. **[INT] Conflict flagged:** `09_edu.md` §5 proposes teaching *inferred* candidates;
   `06_platform.md` §2.12 says only criterion-labelled claims may enter instruction. This plan
   follows 06: the education pilot uses V5-validated items only.
4. **[POC → INT]** The PoC's money lesson is headroom, not cost: $4.82 spent, $5/week limit,
   about $21 of caps. Rule: limits ≥ 3× registered caps, checked in code.
5. **[FW]** Grant-scale: 48 months, ≈ 150–240 PM, ≈ EUR 1–2.8 M; lean S1: 15–18 months,
   ≈ EUR 0.3–0.7 M. MS3 (M18) is the program's decisive gate.
6. **[INT]** Staffing must enforce independence: advisors ≠ participants per domain; the Track A
   roster stays separate; gating κ from non-owner coders.
