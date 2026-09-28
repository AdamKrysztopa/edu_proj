# Locate the residual before asking anyone

**Status:** strategic research map, 2026-09-28. Synthesised from the eight notes in `research_notes/Tacit knowledge reorientation/`. It proposes a reorientation; it does not enact one. `ai_education_research_map.md` remains the single source of state until the owner accepts or rejects this document, and nothing here changes a registered rule of the prepared study.

**Claim tags.** ESTABLISHED = replicated, meta-analytic, or a foundational result not seriously contested. PROMISING = one or a few credible studies, a strong preprint, or a documented but unevaluated capability. SPECULATIVE = argument, position paper, single small study, or an inference in the notes. OUR HYPOTHESIS = a proposal of this document, untested. Bracketed numbers are references (section 26). "Not found" means the notes' searches did not find it, not that it does not exist.

---

## 1. Executive summary: the evidence qualifies reconstruct-first and moves the target

**Verdict.** The evidence **qualifies** the reorientation. Reconstructing a domain from public and organisational evidence before asking humans is supported as a way to **locate gaps, cut expert time and generate candidate claims, tasks and questions**. It is contradicted as a way to produce **authoritative expertise models**, **learner error frequencies**, or **independent expert perspectives**. LLM search and deep-research systems leave large shares of statements unsupported by their own citations (about 23–48% in most audits [34][35][61], up to 75–98% for some deep-research modes [35]) (ESTABLISHED as a pattern). Simulated learners drop a misconception under any feedback [67] (PROMISING), LLM-simulated participants inflate effects [72] (PROMISING), and simulated expert panels reach consensus more often than human experts [74] (PROMISING).

**The decisive twist.** Three independent lines of evidence point the same way. Text under-reports what is obvious to its writers (reporting bias [25], ESTABLISHED; LMs inherit it, shown for object colour [26], PROMISING). Experts omit much of what they do when they explain: no single one of six programmers reported more than 41% of diagnostic actions or 29% of interpretations (as reported in [3]) [2], and three surgeons omitted on average 73% of decision steps [1] (both PROMISING: n = 3–6, one domain each). A third of the cues that 17 NICU nurses used (25 of 70) were absent from the training literature of the time (as reported in [3]) [4] (PROMISING, 1993). So the human residual concentrates **exactly in the obvious-to-experts steps this project exists to recover**: cue→decision bindings, expectancies, automated checks. Reconstruction is structurally worst where it matters most.

The central research question is therefore **not** "can AI reconstruct a domain?" (plausibly yes for concepts and taxonomy in well-documented domains [41]) but **"can AI reconstruct what is written and predict where its own reconstruction is thin, locating the residual before any human is asked?"** (OUR HYPOTHESIS). Nothing in the notes answers it. No study was found that scores LLM public-text reconstruction against a CTA gold standard [notes: tacit §9, reconstruction §5], and no product was found that computes "what documents already cover versus what only experts know" [notes: organisational §5].

**The core primitive is residual accounting**: a provenance-typed expertise model plus a calibrated **gap map** recording, per claim or area, evidence status, knowledge type (Collins's relational / somatic / collective [15]; automated procedure; perceptual cue) and the predicted likelihood that important knowledge is missing. It outputs a **ranked list of residual questions chosen by expected information gain** [147][148], and across domains accumulates a corpus of what humans added that text never contained. That pair is the smallest useful primitive and the defensible core (OUR HYPOTHESIS).

**What changes.** The physics study and its tablet-and-microphone instrument become **Validation Track A**: frozen, intact, registered rules unchanged, started only on its own registered preconditions (course, ethics, physicists) and not scheduled by the NOW gates. Physics becomes one benchmark domain. The NOW programme uses zero participants, zero proprietary data and zero microphones — its one human input is a blind second coder, a labeller rather than a participant — and runs eleven experiments with public ground truth, led by CTA replay against published gold and an open-source-software departure natural experiment (§18).

**The falsifier.** The central hypothesis is about targeting, so recall does not decide it. On a pre-registered primary gold, model and baseline, the test statistic is ΔAUROC: the gap map's AUROC for missed areas minus that of the **strongest** pre-specified baseline. If the upper 90% confidence bound of ΔAUROC falls below a pre-registered smallest effect of interest δ, reconstruct-first adds no targeting value, whatever the recall, and the project becomes an **elicitation-efficiency tool**: World C first, behavioural traces over text. Results between the stop and continue rules are inconclusive and trigger one pre-registered fallback gold, as Stage B's K2 does. The hypothesis is also falsified if the residual cannot be measured: if a known-truth check of the unseen-item estimate against published gold fails its pre-registered tolerance (§14, §22). Recall decides only whether reconstruction survives as a draft for experts to correct.

**Commercial direction.** The first wedge is likely **organisational knowledge-at-risk** (retiring-expert capture, platform onboarding), with education as the research testbed with the best public gold (OUR HYPOTHESIS; §21).

**Decisions.** Adopt the qualified reorientation. Freeze Track A without editing it. Make residual accounting the first build. Run E-CTA and E-OSS, with their ΔAUROC tests, before anything else, because they decide whether the thesis survives.

---

## 2. Original problem: why experts leave knowledge out, and six questions that must stay separate

The first commit (`7aee199`) asked: "How can an AI-supported learning system discover what experts fail to explain because it has become tacit or automatic, diagnose what a learner is actually missing, and turn that gap into effective instruction?" — and called its pipeline "the main hypothesis to test, not an assumption to preserve" [repo_audit §1]. The mechanism named was automaticity: "experts often do not know what they are failing to say because the reasoning has become automatic."

The literature splits that mechanism in two, and the split governs every later design choice [notes: tacit §1 Inferences]:

1. **Automated procedural and perceptual steps.** The expert has the knowledge but cannot verbalise it. Knowledge compilation removes declarative retrieval from practised skill [7] (ESTABLISHED as theory). Automated processes are "not available for introspection" [3][8] (ESTABLISHED in direction, uncertain in size); self-reports often echo shared theories of the task rather than introspection [10], and only heeded information surfaces in concurrent verbalisation [11]. Attending to automated skill degraded experts' sensorimotor performance [174] (PROMISING, one study). Concurrent think-aloud is non-reactive (r = −.03 across 94 studies, about 3,500 participants), while requests to explain are reactive [9] (ESTABLISHED). **This source needs behaviour: traces, observation or process-tracing, in World B or World C.**
2. **Mis-modelled novice difficulty.** The expert cannot see which steps are hard. Preservice teachers with more mathematics mis-ranked student difficulty against real performance (N = 48) [12], and more expert participants were worse at predicting novice task times and resisted debiasing [13] (ESTABLISHED/PROMISING). LLMs show the same blind spot: across 20+ models they converge on a "machine consensus" on item difficulty and "fail to predict their own limitations" [48] (PROMISING). **This source is a fact about learners. It needs learner data, not experts and not text written by experts.**

Collins adds a third axis, why knowledge is tacit [15] (ESTABLISHED as a framework): *relational* (unwritten for contingent reasons; explicable in principle; most of what CTA calls "omitted"), *somatic* (tied to bodies; explanation does not confer skill) and *collective* (social practice; inexplicable for Collins).

The six questions the system must keep apart have different primary sources; conflating them is the drift's root error.

| Question | Primary evidence | World that can answer it | What cannot answer it |
|---|---|---|---|
| **What is the domain?** (concepts, principles, taxonomy) | Textbooks, standards, literature | A. LLMs classified balanced is-a pairs at F1 0.68–0.78 on GeoNames, UMLS and schema.org [41] (PROMISING; one 2023 paper, not full taxonomy construction) | — |
| **What does competent performance look like?** | Published procedures (work-as-imagined); traces of real work (work-as-done); CTA of decisions and cues | A partly; B (traces, logs, review threads); C for cues and expectancies [19][4] | Documents alone: they are work-as-imagined by construction [19] |
| **What is difficult?** | Learner response data, error logs | Public learner data (Eedi, AAAS, DataShop) [137]–[140]; later own learners | Experts [12][13]; LLMs [48]; text written by experts |
| **What does this person know?** | That person's responses over time | Only individual learner data (C) | Public data (cohort-level only); synthetic learners |
| **What should they learn next?** | Prerequisite structure plus that person's state | Structure from A (knowledge-space theory [91]); state from C | Structure alone |
| **How should it be taught?** | Instructional-design evidence; outcome data | A for candidate designs (4C/ID [88], worked examples); C for effects | Synthetic participants: simulated effects inflate [72] |

**Decisions.** Every node in the future model is typed by which of these six questions it answers and by which omission mechanism threatens it. Learner difficulty is never inferred from expert or LLM judgement alone.

---

## 3. Diagnosis of current project drift: rigour without participants became instrument-building

The repository was written in four days (47 commits), so "drift" names a sequence of commits, each coherent [repo_audit §4]:

1. **Physics and university were chosen as the first case** for good reasons (expert–novice literature, concept inventories, checkable steps). The `/branch` skill then hard-coded physics, and every note graded evidence by "outside physics / not university".
2. **Falsifying Decoding the Disciplines [33] moved elicitation to CTA over observed performance.** RQ2 made the human trace the validity anchor, which required audio, written-work capture and transcription.
3. **The experiment fixed people and one topic.** `6f228c2` introduced 12 physicists, about 370 first-year students, conservation principles and a tablet.
4. **The instrument absorbed the effort**: a session app, HTTPS for a tablet microphone, transcription, four review lenses, five architecture decisions, four lesson drains. Instrument artefacts are roughly half the repository's non-lockfile bytes.
5. **Missing data showed early** ("K0 without exam scripts", `30a2b8e`), but the replacement premise test also needs a cohort.
6. **The owner's correction** (`4e790e2`) added L1.11 ("A built instrument or designed study is preparation, not progress on a research phase") and re-broadened `CLAUDE.md`, yet the roadmap chosen in the same commit still routed through physics, courses and experts. `PROGRESS.md` now reads: "Everything that needs no participants is built; both now wait on people."

**Root causes** (inferred in [repo_audit §4.8]; this document agrees). The falsification discipline demanded validation against observed human performance; with no participants, it had nowhere to go except building the instrument ever more carefully. **Public-evidence reconstruction, organisational knowledge and evidence-grounded surrogates never appeared as design options**, and the grading scheme had no category for organisational, synthetic or reconstructed evidence [repo_audit §9], so work of that kind could not register as progress.

**What the drift got right**, and the reorientation needs: a falsifiable design whose "absent from ordinary material" check is a proto-definition of the residual; a provenance discipline (pre-registration, hash freezing, computed gates, decoy-blinded exports, citation verification); and a refusal, enforced in code, to let simulated sessions count as data.

**Decisions.** Diagnose the drift as a **scope** error, not a quality error: change what counts as the next milestone, not the instrument. The lesson: when the only admissible evidence needs unavailable people, the plan must name a zero-participant route or it defaults to tooling.

---

## 4. What existing work should be preserved (KEEP and REUSE)

This section and section 5 classify every significant component, starting from repo_audit §6 and correcting it where the new direction warrants. **KEEP** = central under the new direction. **REUSE** = a useful component, usually copied or generalised rather than edited in place, so that Track A stays intact.

| Component | Class | Why |
|---|---|---|
| `ai_education_research_map.md` | KEEP | The question, the three layers, §11 "What not to assume" and the graded cards are the evidence base. §1, §7 and §9 need reframing once the owner accepts this document. |
| The 13 graded literature notes in `research/` | KEEP (CTA, DtD, expert–novice, PCK, conceptual change, concept inventories) / REUSE (KT, instructional notes) | DOI-verified syntheses holding the omission evidence, "seed difficulty from response data", "cohort, not individual", and the public datasets. The instructional notes serve the later "how to teach" layer. |
| `research/route-comparison.md`, `decision-gaps.md` | REUSE | The five-choice decomposition and the AI-interviewer evidence are domain-general. |
| Map evidence discipline (scoped and split ratings, *(project choice)* marks, L2.1 on grain) | KEEP | Exactly what residual accounting needs, extended with new evidence classes (§10). |
| Lessons loop (`docs/lessons.md`, archive, `lessons_graph.py`, `lessons` / `implement-ll`, session-start hook) | KEEP | Domain-agnostic process memory; L1.1, L1.11, L1.12, L2.1, L2.3, L3.1, L3.6 and L4.1 carry over directly. |
| `citation-verifier` agent; `check-dois.py`; `guard-secrets`, `guard-user-email`, `guard-nested-repo` hooks | KEEP | Provenance of literature claims. **Confirmed defect:** `.claude/settings.json` line 9 calls `check-dois.sh`, but only `check-dois.py` exists, so the DOI hook probably never fires (file listing checked; hook not executed). |
| `methods-critic` agent | REUSE | Rewrite its checklist for zero-participant and surrogate designs; it currently treats human transfer outcomes as mandatory. |
| `codebook-stress-tester` agent | REUSE | The nearest existing tool to known-truth surrogate testing. |
| `/branch` skill | REUSE | Strip the physics hard-coding from the compare and experiment modes. |
| `.mcp.json` (OpenAlex, Zotero, Playwright) | KEEP | OpenAlex and Zotero are the World A literature pipeline. |
| Nine-type hidden-knowledge taxonomy and codebook operation types (`instrument/codebook/v0.md`) | REUSE (copy) | The gap map's **knowledge-type vocabulary**; the operation form "in situation S, do A (because C)" maps onto a KLI component with a condition part [86]. |
| Operation status tags: trace-only, probe-added performed, reported only, contradicted; plus source tags | REUSE | These become **provenance classes** for claims about expert cognition (§10). |
| "Absent from ordinary material" judgement and the `published=yes` framework tag | REUSE | A **proto-residual**: an operation that is performed, shared, not in ordinary material and not in published frameworks. Generalised, it is the residual definition in §14. |
| Cross-expert matching rule ("the same if a novice taught either would perform the same action in the same situation") | REUSE | The matching criterion for recall against a gold list; it fixes grain before matching (§14 pitfall 4). |
| `probe_code/agreement.py` (α, κ, MASI, decoy false rate, guess rate) | KEEP | Needed for every matching step in §18: human–human κ versus LLM-matcher κ. |
| `probe_code/calibration.py`, `baseline.py` (Wilson intervals, computed rules), `export.py` (blinding), `corroboration.py` (decoys) | REUSE | Calibrating an LLM judge against human labels, pre-stated computed gates, and decoy-mixed checks of whether a claim is grounded. `k0.py`'s `wilson` and `bootstrap_kappa` helpers are reusable. |
| Interviewer turn contract and leading-question guard (`contract.py`, `engine.py`, `llm.py`, prompts, stems) | REUSE (copy, de-physics) | One question per turn, quoted-span follow-ups checked in code, a guard against naming what the respondent has not said: the right control for probing surrogates without planting content, and for later residual interviews. Copy rather than edit, because `instrument/prompts/` freezes with Track A. |
| `backends.py`, `models.json` pattern, decision 0002 | REUSE | Provider-neutral backends and the refused-versus-unavailable split. Refusal is model- and role-specific: Opus 5 refused expert role-play under `reasoning_extraction` and none of 86 interviewer turns [repo_audit §8.3]. |
| `FrozenConfig` hashing; `storage.py` append-only log; decision 0004 (`rules-not-agents-decide`, `freeze-by-computed-rule`) and 0001 (`full-session-log`, `blind-coding-material`) | REUSE (patterns and principles) | Provenance of machine-generated claims; gates are code, not model judgement. The Track A instances stay frozen. |
| `docs/guard-calibration.md`; `instrument/calibration/items.csv` (60 unlabelled items) | REUSE | A protocol for validating an LLM judge against human labels; a seed set for a leading-probe detector. |
| K0 error-category scheme (`codebook-k0.md`) and its rule that a difficulty is a "candidate hidden operation" only when components pass but synthesis fails | REUSE (copy) | A **gold-coding scheme for public error data** (AAAS, Eedi, DataShop) and the operational test separating a missing prerequisite from a hidden operation. The registered copy is untouched. |

**Decisions.** Reuse by copying into a new, domain-neutral package, so that nothing under `instrument/` changes and Track A's future freeze stays valid. Fix the `check-dois` path first.

---

## 5. What should be frozen or demoted (FREEZE and RETIRE): Validation Track A

**Validation Track A — Physics / Human Expert Elicitation** is the prepared study, kept whole. It holds Stage A (12 physicists, within-expert, AI versus human retrospective probes), K1, the early and pretest K0, Stage B (a two-arm RCT with about 370 students and delayed transfer), and K2. **Its registered rules stay exactly as written: K0, K1, K2, Stage B arm matching and the 2–3-week delay.** The reorientation demotes the track's priority; it does not reopen its design. Track A starts only on its own registered preconditions (a course offering, ethics, physicists); no NOW gate schedules or blocks it. Two additions are allowed inside it, both secondary and non-gating per `CLAUDE.md`: sealed predictions (§18, E-SEAL) and a later post-hoc residual comparison (§20). Neither can change what a registered rule decides.

**FREEZE** means valuable, internally sound, and blocked on humans. Frozen items are not deleted or edited; they resume as a unit when Track A's registered preconditions are met.

| Component | Class | Explanation |
|---|---|---|
| `research/experiment-ai-assisted-cta-physics.md` (Stage A/B, K0/K1/K2) | FREEZE | A reviewed World C design (four `methods-critic` passes, no fatal flaw) needing 12 physicists, a human interviewer, coders and about 370 students. Track A's charter. |
| `research/roadmap.md` (M1–M8, A1–A10) | FREEZE as the Track A plan — **corrects audit's RETIRE** | Still the right plan *for Track A*; only its role as the governing plan is retired. A1–A10 stay "untested". |
| Early K0 kit (`instrument/k0/*`, `probe_code/k0.py`) | FREEZE | Needs a course, ethics and two coders; the prereg draft has *to confirm* fields. |
| Pilot materials (`pilot-protocol.md`, `human-script.md`, `consent-pilot.md`, `problems/*`) | FREEZE | Live sessions with physicists. |
| Session instrument (`session.py`, `server.py`, `human.py`, `trace.py`, `transcribe.py`, `backup.py`, `cli.py`, `instrument/web/*`, stream and server tests) | FREEZE | Tablet, microphone, transcription and console exist to record live expert sessions; there is nothing to record. |
| Freeze and prereg instances (`probe-app freeze`, planned `prereg.json`, `freeze-baseline.md` thresholds, `stage-a-prereg-additions.md`); `guard_audit.py` | FREEZE | They gate or audit Stage A sessions. The patterns are reused (§4); the baseline's "Limits" section is reused as evidence about surrogates. |
| `probe_code/loader.py` (rejects simulated sessions) | FREEZE unchanged — **corrects audit's "REUSE (invert)"** | Inverting it would break decision 0001 inside Track A. New tracks get their own loader that **admits labelled synthetic material and never pools it with human data**. |
| `probe_app/simulate.py` ("Dr. Lee" surrogate) | FREEZE as a Track A test double — **corrects audit's "KEEP (rebuild)"** | It did its job: exercising the app and codebook. New-track surrogates are built separately and labelled (§12), and in elicitation experiments the "expert" is a **held-out gold source**, not a persona. |
| Architecture decisions 0001–0005, `constitution.md`, `migration-report.md` | FREEZE, scoped to Track A — **corrects audit's RETIRE of `simulated-sessions-rejected`** | The instrument's validity constitution. Decision 0001's rejection of simulated sessions **stays in force inside Track A**; new tracks replace rejection with labelling, and synthetic material may never reach a gate or be pooled with human data. |
| `validity-reviewer`; `/elicit`, `/preflight`, `/session-report`; `guard-frozen-prompts`, `guard-session-data`, `run-instrument-tests`, `live-smoke-reminder` | FREEZE, kept active | Instrument-specific; they must keep firing on any edit under `instrument/`. |
| Instrument reviews, `docs/superpowers/specs/*` and `plans/*` | FREEZE | Historical build records. |
| `docs/poc-explained.html`; `research/minimum-reading.md` | FREEZE — **corrects audit's RETIRE** | Accurate briefs of Track A, wrong only if read as the project's plan. The project minimum becomes §25 once this document is accepted. |

**RETIRE** means the item rests on an assumption the evidence or the owner's situation no longer supports. Retired items are not deleted; they stop governing.

| Item | Explanation |
|---|---|
| **Physics and university level as the project's defining scope** | The original question was cross-disciplinary [repo_audit §1]. Physics mechanics is close to a *best case* for reconstruction because it is unusually text-rich at the expert–novice boundary [notes: adjacent Q2(d)], so success there would not show generality. Physics stays as one benchmark domain and as Track A. |
| **"12 physicists plus about 370 students" as the next milestone** (`PROGRESS.md` "Next: M1 … M2", `CLAUDE.md` "Current priority and scope") | The owner has no participants, possibly for months. A next milestone that cannot start is not a plan. The **text of both files must be updated if the owner accepts this document**; this document does not edit them. |
| **The roadmap as the governing plan** | It presumes cohort-first bottleneck data and experts. Replaced by §22. |
| **`PROGRESS.md`'s current content** (audit said RETIRE the file) | **Corrected:** keep the file as the progress tracker the project's method requires; retire its current priority and NEXT lines. The M1–M8 rows move under a "Track A (frozen)" heading. |
| **`instrument/problems/simulated_think_aloud.json` as evidence of any kind** | A hand-written, unsourced expert transcript, whose "tacit" content the builder authored [repo_audit §8.3]. It stays as a test fixture only, and it is the model of what a provenance-first design must not produce. |
| **The implicit assumption that only human-observed evidence counts** | Replaced by typed evidence classes (§10). Human observation remains the strongest class, not the only admissible one. |

**Decisions.** Freeze Track A as a unit and label it. Retire only scope and priority, not artefacts. Put the owner-facing edits (`CLAUDE.md` scope section, `PROGRESS.md` NEXT, the map's §1/§7/§9, the `check-dois` path) on a list for the owner to approve.

---

## 6. Reframed research problem: reconstruct what is written, predict where it is thin

**Reframed problem** (OUR HYPOTHESIS). Given a role, task or domain and evidence in three tiers — World A (public), World B (organisational artefacts and traces), World C (humans) — build a model of the domain and of competent performance in which **every claim carries its evidence class**. The system then **estimates, per area, how likely it is that important knowledge is missing**, and emits the **smallest set of human questions** expected to close the most important gaps. Success is measured by how much held-out, human-revealed knowledge the questions recover per unit of human time, not by how complete the model looks.

Three findings support the reframing. **Reconstruction is one more elicitation technique with its own access profile**: knowledge-acquisition techniques are complementary, and no single one captured the full range [14] (PROMISING; n = 16 and the claim unverified, paywalled); LLMs are strong at structuring and at inferring policy from observed decisions, weak at completeness against a human reference [27][28] (PROMISING). **CTA already begins with document analysis** [3], so reconstruct-first strengthens CTA's first phase rather than breaking with it. **"Externalisation" is contested** [29] (ESTABLISHED as a critique), so the system promises to **locate and scope** tacit knowledge, not to convert it.

**Two omission mechanisms, two routes.** Automated steps (mechanism 1) need behaviour: World B traces or World C observation. The strongest precedent is Cho et al.: an LLM given **320 student–tutor conversations paired with expert tutors' alternative responses** produced knowledge whose LLM+Conversation arm beat a CTA-derived expert-articulated model, and novices trained on it narrowed the expert–novice gap (85–99 per arm, math tutoring, preprint) [27] (PROMISING). That study used **behavioural traces, not public text**, so it supports "traces first" more than "public text first". Mis-modelled difficulty (mechanism 2) needs learner data. Public response datasets supply it at cohort grain with zero participants (§19).

**"I do not have enough evidence to assert this" must be architectural.** Verbalised confidence is overconfident [notes: reconstruction §7]. Reasoning fine-tuning degrades abstention by 24% on average [53], and strong models answer instead of abstaining when context is insufficient [54] (PROMISING). Conformal factuality gives 80–90% guarantees but needs a labelled calibration set from the target distribution [55] (PROMISING). So a claim with no verifying source span gets status *unsupported* whatever the model says, and "insufficient evidence" is a first-class output, not a refusal.

**Epistemic labels (extended from the brief).** Every claim carries exactly one primary label:

| Label | Meaning | May feed a gate? |
|---|---|---|
| Observed human evidence | Direct record of human performance or response: trace, think-aloud, learner response, logged action | Yes |
| Literature-supported | A resolvable source span from published work supports it; verifier verdict recorded | Yes, at its graded certainty |
| Organisational-artefact-supported | A resolvable span in an organisation's artefact (doc, ticket, commit, ADR, log) supports it | Yes, within that organisation |
| Inferred | Derived by the system from supported claims; the derivation is recorded | Only as a hypothesis |
| Synthetic extrapolation | Produced by a simulated learner or expert, or by parametric model recall with no span | **Never** as a criterion; may serve as a gap-map *predictor* (§14.2) |
| Unknown | Evidence was sought and not found (insufficient evidence) | No; it feeds the gap map |

Each label also carries source type, date, corroboration count and independence, contradiction links, knowledge type, and the world it came from (§10).

**Decisions.** Adopt the reframed problem. Treat "can AI reconstruct a domain?" as plausible for concepts and taxonomy in text-rich domains, and as the wrong question. Treat "does the gap map predict the residual?" as the project's central, falsifiable question.

---

## 7. Education and organisational knowledge: two families, one primitive

Both families face expert knowledge the artefacts do not contain and a recipient who needs it; evidence, payer, legal exposure and where the residual concentrates differ.

| Dimension | Education | Knowledge inside companies |
|---|---|---|
| Who lacks the knowledge | Learners | Newcomers (documentation is a known onboarding barrier [136]), successors, adjacent teams |
| Where the residual sits | Cue→principle bindings and checking habits [notes: tacit §7]; mis-modelled difficulty [12][13] | Rationale ("why"), work-as-done deviations, knowledge concentrated in few people, and the "who knows what" directory itself [117][110][118]; leavers may remain reachable [113] |
| Strongest public gold | Misconception catalogues with prevalence (Eedi graph, CC BY 4.0 [137]), option-level responses [138], KC-labelled logs [140], published CTA task lists [1] | OSS departures with post-departure outcomes [111][112]; rationale datasets [59]; documentation-issue taxonomy [116] |
| What text contains | Work-as-imagined: textbooks, worked solutions [19] | Work-as-imagined: SOPs, CONTRIBUTING files, wikis [19][124] |
| What traces contain | Learner logs; tutoring conversations with expert responses [27] | Git history, review threads, tickets, work orders, incident timelines |
| Zero-participant validation | Retrodiction of real response data; AFM fit on logs; CTA replay | Retrospective departure natural experiment on OSS |
| Payer | Institutions and publishers; weak, slow | Operations, engineering and HR leaders facing retirements and turnover; TVA saw about 35% of its nuclear workforce retire over six years [121] (unverified) |
| Legal exposure | AI Act Annex III(3)(b) if individual learning outcomes are evaluated [129] | GDPR employee data; German co-determination; Annex III(4) if outputs feed task allocation or performance evaluation [129][131] |

**The shared primitive** is residual accounting over a provenance-typed model (OUR HYPOTHESIS). In education the "unit" is a KC, decision point or misconception. In a company it is a component, process step, decision or SOP section. The organisational literature already has two of three needed axes, measured separately and never joined [notes: organisational §3 Inferences]. *Concentration* comes from authorship-based truck factor and Knowledge-at-Risk [109][110]; *criticality* comes from TVA/IAEA-style position risk [121]. The missing axis is **artefact coverage**: does any artefact explain what, how and why? Adding it is the organisational form of the gap map.

**Why the two families help each other** (OUR HYPOTHESIS). Education has the best public gold for *what humans add*; organisations have the best natural experiments for *what is lost when a knower leaves*. A gap map that predicts residuals in both is evidence of a universal *procedure*. The notes are clear that a universal *model* or universal validation is not plausible: expertise and PCK are domain-specific [23][168][161], and ITS authoring tools traded generality for depth [169], so every domain needs its own calibration set (ESTABLISHED for domain specificity).

**Decisions.** Build one primitive with two adapters. Use education to validate *residual prediction against human-revealed knowledge*, and OSS to validate *residual prediction against realised loss*. Claim universality only for the procedure, and only after a text-poor domain passes; that cannot happen NOW (§19).

---

## 8. Evidence landscape: strong on omission, weak on reconstruction completeness, negative on synthetic learners

### 8.1 The "70% omission" figure is a slogan, not a parameter

The map and the CTA note carry "experts omit about 70%". The data trail is narrower than that [notes: tacit §1].

- **Chao & Salvendy 1994** [2] (as reported in [3]): six expert programmers doing troubleshooting. No single expert reported more than 41% of diagnostic actions, 53% of debugging actions or 29% of interpretations; pooling all six reached 87%, 88% and 62%. PROMISING (n = 6, one domain).
- **Sullivan et al. 2014** [1]: three surgeons videotaped teaching cricothyrotomy, scored against a CTA-built task list. They omitted on average 71% (10/14) of clinical-knowledge steps, 51% (14/27) of action steps and 73% (3.6/5) of decision steps. CTA probing raised coverage from 44% (20/46) to 66% (31/46). PROMISING: n = 3, one procedure, and the gold list is CTA-derived and so partly circular.
- **The round "70%"** traces to review chapters by the same USC group citing each other [3]. The data trail ends at these studies and an unretrieved dissertation.
- **Take away three things:** omission is real (ESTABLISHED); pooling experts recovers much more than any one (PROMISING); the pooled ceiling is lowest for *interpretations and decisions*.
- **The premise that matters is instructional value.** CTA-based instruction beats other or conventional instructional-design methods: Hedges g = 0.871 against "other means" of identifying content, in a meta-analysis of few, small studies [5]; in surgery, against conventional training, SMD 1.36 (procedural knowledge) and 2.06 (technical performance, surgical-trainee subgroup; 1.58, 95% CI 0.31–2.85, with the medical-student study), each pooled from 4 RCTs within a 12-study review [6] (PROMISING→ESTABLISHED in direction). The oft-quoted d = 1.72 is a within-group pre–post effect from an unpublished dissertation and must not be cited as CTA's added value [notes: tacit §3].

### 8.2 The strand-by-strand picture

| Strand | Strongest finding, at its original grain | Tag | Implication |
|---|---|---|---|
| Text is incomplete at the boundary | 25 of 70 NICU nurse cues absent from training literature (17 nurses, 1993; as reported in [3]) [4]; reporting bias in a teraword corpus [25] and its transfer to LMs, for object colour [26] | PROMISING / ESTABLISHED / PROMISING | Expect the residual in cues and "obvious" steps |
| Published text does not transfer capability | TEA laser [20] and Q-of-sapphire [176] replication needed personal contact; lapsed practices need "reinvention" [21] | ESTABLISHED (qualitative cases) | Limits *capability* transfer, not *description*; a domain-dependent answer, physics near the favourable end [notes: tacit §8] |
| Tacit ≠ unarticulable | Chick-sexing cue was analysed and taught with a short instruction sheet [24]; perceptual expertise is trained by classification practice [22] | ESTABLISHED | Perceptual residual needs contrasting cases, not interviews |
| Declared policy ≠ practice | Physicians' diagnoses driven by 1–4 symptoms despite long self-reported lists; the same physicians' diagnoses of identical symptoms at different times correlated only r ≈ .40–.50 [3] | ESTABLISHED as a family | Self-report is not the gold; traces are |
| Work-as-imagined ≠ work-as-done | Protocols deviate systematically in practice [19] | ESTABLISHED as a phenomenon | Documents (World A/B) are imagined work |
| LLM deep research | Citation links valid above 94%, factual accuracy 39–77%, falling about 42% from 2 to 150 tool calls [36]; 3–13% hallucinated URLs [37]; no system above 75% rubric coverage [38] | ESTABLISHED pattern / PROMISING numbers | Every claim needs span-level verification; more retrieval is not more accuracy |
| Curated-corpus agents | PaperQA2 answer precision 85.2% on LitQA2 multiple-choice questions; WikiCrow 13.5% cited-and-unsupported versus 24.9% for human Wikipedia [39] | PROMISING | Restrict World A to curated full text where possible |
| Ontology/KG building | Balanced is-a pair classification F1 0.68–0.78; non-taxonomic relations F1 49.5% on UMLS (2023) [41]; GraphRAG quality only LLM-judged [42] | PROMISING | Concepts: draft; prerequisites and causal edges: hypotheses |
| KCs and misconceptions | GPT-4 KCs matched human KCs for 56% (chemistry) and 35% (e-learning) of items [43]; distractor preferences only moderately correlated with students [46]; LLM errors converge on one distractor while students spread [47] | PROMISING | Catalogues are reconstructable; prevalence is not |
| Rationale recovery | Precision 0.267–0.278, recall 0.627–0.715; 64–69% of the LLM arguments experts had not mentioned were judged helpful [59] | PROMISING | Recovered "why" is a hypothesis to confirm, not coverage |
| Traces beat articulation | LLM given 320 student–tutor conversations with expert responses beat a CTA-derived expert-articulated model; novices improved [27] | PROMISING (one domain, preprint) | World B traces are the highest-value input |
| LLM as stand-in expert | Answering in place of experts it was faster (~10 vs 35 min) and more structured, but its ontologies had 19–32% hallucinated classes (one game domain, n = 2) [28] | SPECULATIVE (small n; venue unverified) | LLM answers for speed; humans for model authority |
| Abstention | Unsolved; reasoning tuning degrades it 24% [53] | PROMISING | Abstention must be architectural |
| Surrogate learners and experts | Near-zero misconception faithfulness [67]; under-dispersion and false positives on nulls in simulated participants [71][72]; over-consensus [74] (details in §12) | PROMISING / ESTABLISHED | Hypothesis generation and debugging only |
| Learner data beat experts on structure | Learner data reveal difficulty factors experts did not list [162]; LFA models beat the best human KC model on at least 10 of 11 DataShop datasets (all 11 under item-stratified CV) [103]; a discovered KC split drove a redesign with d = 0.47 in one RCT (115 randomised, 91 completed) [102] | PROMISING (one group) | Learner data are the gold for "what is difficult" |
| Organisational loss | 65% of 133 popular GitHub projects have truck factor ≤ 2 [109] (PROMISING, one study); losses over 3× expected [110], replicated with more severe extremes [111] (ESTABLISHED) | See cells | OSS is a zero-participant organisational testbed |

### 8.3 Where the evidence contradicts the original proposal

The notes' red team found three contradictions [notes: adjacent Q4], and this document adopts them:

1. **A synthetic cohort cannot stand in for learners before any real learner data exist.** Agents grounded in real per-person interviews and surveys reached 86% of participants' test–retest consistency on held-out General Social Survey items, against 74% for demographics-only agents (1,052 US adults, not learners) [73] (PROMISING). That this argues for real learner errors *early* is the notes' inference (SPECULATIVE). With no learners available, public response data must play that role.
2. **Surrogate expert perspectives are not independent** [48][75][74].
3. **Validity does not transfer across domains without per-domain human calibration** — the notes' inference from evidence that expertise is domain-specific [23][168].

**Decisions.** Cite only grain-exact figures. Drop "70%" as a parameter, including in the map when next edited. Treat instructional value (g = 0.871; SMD 1.36/2.06) as the premise and omission rates as illustrations.

---

## 9. Missing research areas the project has not used

A grep of `research/` and the map found no hits for most of these [notes: adjacent, coverage check].

| Area | What it contributes | How the project should use it |
|---|---|---|
| Requirements-engineering elicitation [158] | Separates unarticulated "unknown knowns" from true unknowns, with a technique for each | Source for the type → channel table (§10.3) |
| Cooke's classical model [159] | Performance weighting on seed questions won on combined accuracy × informativeness in 26 of 33 studies, though out-of-sample statistical accuracy alone was lower than equal weighting (PROMISING) | Calibrate **both** surrogate and human experts |
| Prelec's "surprisingly popular" / truth serum [160] | Recovers the answer an informed minority holds (PROMISING–ESTABLISHED) | Stops minority knowledge being averaged away by aggregation or LLM consensus |
| Safety-II (work-as-imagined versus done) [19] | Procedures describe imagined work | SOP-derived claims stay "imagined" until a trace corroborates them |
| Process mining, conformance checking [124] | Log versus reference model: skipped, extra, reordered steps (ESTABLISHED) | The rigorous doc-versus-practice signal where event logs exist |
| Learnersourcing [165] | A majority of learners' subgoal labels were comparable to expert labels, on four videos (PROMISING) | Learners as producers, not only test subjects (LATER) |
| Knowledge space theory [91] | Surmise relations; the "outer fringe" is what to learn next (ESTABLISHED) | The "what next" layer |
| Evidence-centred design [87]; automatic item generation [171] | Student → evidence → task; "additional KSAs" name alternative explanations (ESTABLISHED) | Model → diagnostic items; competing bottleneck hypotheses |
| Job and practice analysis [163]; entrustable professional activities [164] | Role → tasks → knowledge → exam specification, validated by SME panels and surveys | Precedent for a universal *procedure* with domain-specific human validation |
| Knowledge stickiness [117]; knowledge hiding [120]; codification versus personalisation [119] | Transfer fails on absorptive capacity and causal ambiguity more than motivation (PROMISING, one large study); hiding is separate and measurable | Missing rationale is the highest-value gap; low expert burden and credit attribution |
| Truck factor, Knowledge-at-Risk [109][110] | Concentration (one study) and loss (replicated) from Git with no participants | Concentration axis of the organisational gap map |
| Reporting bias [25][26] | Text under-reports the obvious (ESTABLISHED); LMs inherit it (PROMISING) | A gap-map prior feature |
| Think-aloud reactivity [9] | Think-aloud non-reactive; explanation requests reactive (ESTABLISHED) | Human channels use think-aloud, not "explain", for verbalisable content; traces and observation for automated steps (§10.3) |
| Abstention, conformal factuality [53][55] | Guarantees need labelled target-domain calibration data | Conformal layer is LATER |
| Declining public novice–expert Q&A [135] | Stack Overflow activity fell about 25% within six months of ChatGPT relative to comparison platforms, a lower bound (PROMISING) | World A boundary sources shrink; World B matters more over time |
| AI-generated code [115] | Authorship-equals-knowledge fails when agents write code (SPECULATIVE) | Weight by review and discussion [114]; validate on pre-agent histories |
| Anchoring on the AI model | Size not quantified (SPECULATIVE) | **One human arm blind to the AI model** |
| Knowledge type → channel | Methods map to knowledge types [3]; the full mapping is the notes' synthesis (SPECULATIVE) | Route every gap to its channel (§10.3) |
| Epistemic network analysis [107] | Models expertise as co-occurrence structure (PROMISING; the source is a methods tutorial, no expert–novice result checked) | A later check on cue–decision–principle links |

**Decisions.** Import Cooke calibration, surprisingly-popular scoring, ECD, the Safety-II/process-mining lens and typed channels now; add a map branch only when a §18 experiment needs it.

---

## 10. Proposed domain and expertise representation: reuse a layered composite, invent four objects

**Do not invent an ontology.** A plain knowledge graph cannot natively represent condition→action rules, ordered procedures, perceptual cues, probabilistic learner state or argumentative status [100] (ESTABLISHED structurally). The strongest tutoring results come from production-rule and constraint representations with statistical learner models layered on top [89][102]; no controlled comparison with graph models was found. The composite below reuses mature standards layer by layer [notes: representation §8]. Each mapping is the notes' design inference (SPECULATIVE), not a validated integration.

| Layer | Content | Reused standard |
|---|---|---|
| L0 Terminology | Concepts, labels, cross-scheme mappings (e.g. to ESCO for organisations) | SKOS [94] |
| L1 Domain structure | **Index and glue only**; means–ends and causal structure | RDF/OWL graph [100]; CWA abstraction hierarchy |
| L2 Performance and expertise | KC as the unit **with its condition part** ("when (not) to apply"); recurrent rules versus non-recurrent strategies and mental models; applicability and violation constraints; decisions, cues, strategies, common errors; troubleshooting steps | KLI [86]; 4C/ID [88]; constraint-based modelling [89]; CDM/ACTA decision-requirement rows [16][17]; PARI [106]; bug libraries [90] |
| L3 Learner and difficulty | Item→attribute mapping; prerequisite states; per-KC mastery; malrules; learning-progression levels | Q-matrix and G-DINA [92]; KST [91]; BKT/AFM; LFA on DataShop for validation [101][140] |
| L4 Diagnosis and assessment | Claim→evidence→task; alternative explanations; hypothesis testing | ECD [87]; CommonKADS diagnosis template [93] |
| L5 Instruction | Whole tasks, supportive and procedural information, part-task practice | 4C/ID [88]; KLI instructional principles [86] |
| L6 Epistemics | Provenance; claim with support and challenge; contradictions; open issues; graded certainty | PROV-O [95]; nanopublications [96]; micropublications [97]; Dung/AIF argumentation [98]; IBIS; GRADE-like certainty [99] |

Misconceptions are stored as **hypotheses with evidence and confidence, not fixed entities**. That keeps the model neutral in the live dispute between the misconceptions view and knowledge-in-pieces [105] (ESTABLISHED as a dispute). Procedures that resist graphs are held as solution-path libraries; perceptual cues as contrasting-case sets; collective and troubleshooting knowledge as narrative cases. The graph indexes these assets rather than containing them [notes: adjacent Q2(e)].

### 10.1 The claim record (the unit of residual accounting)

Every assertion in L1–L5 is a claim with these fields (OUR HYPOTHESIS, assembled from the notes' pieces):

- **Assertion**, **layer**, and which of the six questions (§2) it answers.
- **Epistemic label** (§6).
- **Evidence spans**: source identifier, span, retrieval date, verifier verdict and verifier model family.
- **Source type** (study, textbook, standard, forum answer, SOP, ticket, commit, review thread, trace), **date**, and a **work-as-imagined versus work-as-done** flag.
- **Corroboration** by *independent* sources (same authors or derived sources count once), and **contradiction** links computed by claim clustering plus NLI, not left to the synthesiser, because models flatten conflicts [52].
- **Status tags** reused from the codebook: trace-only / probe-added performed / reported only / contradicted.
- **Knowledge type**: the nine codebook types, Collins's relational / somatic / collective, "automated procedure" and "perceptual cue".
- **Certainty**: a GRADE-like level; **no test for elicited knowledge was found** [99].
- **Residual prior**: predicted probability that important knowledge is missing here, with its features (§14).

### 10.2 The four objects that do not exist yet

The notes found four gaps no mature framework fills [notes: representation §8]:

1. **Perceptual cue representation.** CDM/ACTA cues are free text with no link to evidence. Represent a cue as a discrimination: contrasting cases plus the feature that separates them, following the chick-sexing analysis [24].
2. **A bottleneck-hypothesis object.** It links a learner failure (observation), the focal knowledge claimed missing, named alternative explanations (ECD "additional KSAs": missing prerequisite, misconception, execution), their evidence, and the **expert–novice contrast** ("expert has / novice lacks / novice substitutes"). The K0 rule "components pass, synthesis fails" is its operational test.
3. **A crosswalk between framework units**: KC ↔ ECD KSA ↔ CDM decision ↔ 4C/ID constituent skill ↔ codebook operation.
4. **Validated certainty for elicited knowledge.** Adapting GRADE's downgrading domains is plausible — one expert versus several (inconsistency), a claim moved across domains (indirectness), small elicitation samples (imprecision) — but no test was found.

### 10.3 Knowledge type decides the channel

| Knowledge type | Where it can come from | Matched channel (later, for humans) |
|---|---|---|
| Declarative concepts, principles, taxonomy | World A text | Documents; interviews; concept maps |
| Relational tacit (unwritten, explicable) | A partly (pooled sources); C | CDM-style probes; residual questions |
| Automated procedure and self-checks | B traces; C observation | Observation and process tracing first; think-aloud is non-reactive [9] but surfaces only heeded information [11], so it is a weak channel here (inference) |
| Perceptual cues | C | Contrasting-case classification tasks [24][22]; not interviews |
| Somatic | C | Observation of performance |
| Collective (norms, what counts as good work) | B review threads and postmortems, partly; C | Narrative capture; community presence [32] |
| Learner difficulty | Learner data (public now, own later) | Response data; error coding; KC-model fit |
| Rationale ("why") in organisations | B (ADRs, PRs, commits), partly | Targeted confirmation questions [59] |

**Decisions.** Build the claim record and the six labels first, then L2 and L6, then L3 over public data. Leave G-DINA, KST semantics and argumentation solvers until data demand them. Build the four new objects only as far as the §18 experiments need them.

---

## 11. Autonomous domain reconstruction: what to automate, and the gates that make it safe

**What an autonomous pipeline can do now** [notes: reconstruction Implications]: draft a broad concept inventory and taxonomy for well-documented domains [41]; retrieve real sources once a liveness and bibliographic-resolution filter removes the 3–13% hallucinated URLs [37]; assemble catalogued misconceptions into candidate distractors, though LLMs are less adept at anticipating real students' errors [45]; and represent claim-level provenance with automatic claim verification [62] (ESTABLISHED as methods). Verifiers' agreement with human judges ranged from about 72% to 96% across the tools the notes reviewed, so the verifier's false-accept rate is measured on decoys (reusing `corroboration.py`); verifier error is how parametric content gets mislabelled literature-supported.

**What it cannot do reliably now:** guarantee that cited claims are supported; recover prerequisite, causal and procedural edges (prerequisite benchmarks still use soft similarity metrics [44]); represent disagreement (models adopt wrong retrieved content over correct priors more than 60% of the time [51]); know what real learners get wrong or how often (generated physics items needed human oversight or student interviews for distractors aligned with real difficulties [155]); produce CTA-grade tacit knowledge from public sources (untested; every positive result found used expert behaviour data [27]); abstain reliably; or cover niche and organisational knowledge, since accuracy tracks pretraining frequency [56] and hallucination is bounded below by the share of facts seen once [57].

**Pipeline** (OUR HYPOTHESIS; stages taken from the notes' designs):

1. **Scope.** Task decomposition drafted with HTA/CommonKADS templates, marked *inferred*, and hash-frozen before any gold is acquired.
2. **World A, curated first.** Retrieve from curated full-text corpora before the open web; restricting to curated full text gives the best measured claim support [39][40]. Prioritise **boundary texts** where a novice's error forces an expert to articulate. The notes rank them: expert–novice and CTA research; discipline-based education research on errors; novice-asks-expert-answers forums; examiner reports; instructor guides and PCK documents [161]; incident reports; narrated demonstrations; design-rationale artefacts [notes: adjacent Q3] (SPECULATIVE ranking).
3. **Extract claims.** Atomic claims, each bound to a source span.
4. **Mechanical gates, not prompts:** bibliographic resolution; span verification by a different-family verifier [152]; parametric-only content labelled *synthetic extrapolation*; contradictions computed separately; staleness checked against source dates.
5. **World B, when available.** Traces before prose. SOP claims stay *imagined* until corroborated by logs, tickets or reviews [19][124].
6. **Gap map.** Compute the residual prior per area (§14) and emit ranked questions (§14.4).
7. **Ledger.** Log model identifiers, dates, prompt hashes, tokens, dollars and tool calls per run; rerun several times and report the stability of concept and edge sets [notes: reconstruction, evaluation design]. Accuracy must be reported jointly with research depth, because depth reduced accuracy [36].

**The LLM summariser is itself an unreliable layer.** In 2023, 55% of GPT-3.5 and 18% of GPT-4 citations in literature-review prompts were fabricated [58]. During this research a fetch summariser reported a "63% distractor match" figure for Acquaye et al. that does not exist in the paper [notes: adjacent Q2(a)]. Every number entering the model is checked against the source text, not against a summary of it.

**Decisions.** Build the gates before the generator. Treat citation-verifier-style checking as code. Restrict World A to curated and boundary sources in v0. No claim reaches a gate on parametric recall alone.

---

## 12. Evidence-grounded surrogate cohorts: demoted to hypothesis generation and debugging

### 12.1 Synthetic learners

**The record** [notes: synthetic §1–§3]. A simulator predicted an adaptive fractions-tutor policy would win; with real students there was no significant difference [63] (PROMISING, one study). Simulated learner models agreed on the top policy about 27% of the time, and all-criteria certification succeeded in 3.75% of 1,280 settings [80] (single-author preprint); and almost half of 2010–19 simulated-learner studies gave no validity evidence [64]. LLM students cannot reliably be less competent in a controlled way [66], drop a misconception on any feedback (Selective Flip Score near zero) [67], reach role-play fidelity F 0.23 against 0.51 for a trained simulator in chess [69], need re-prompting per model [85], and prompting performs poorly on real tutoring dialogues [70] (all PROMISING). Even the strongest positive silicon-sampling result predicts treatment effects of 70 nationally representative survey experiments — while overestimating effects and doing worse on megastudies — not learner errors [82].

**Legitimate uses, strongest first** (adopted from [notes: synthetic Implications]):

1. **Known-truth pipeline and instrument debugging.** Generate data from an explicit specification — a KC list plus a misconception→answer map — and check that coding and export recover what was put in [83] (ESTABLISHED use class).
2. **Logical discriminability of diagnostic items.** Does item Y have some response that profile X would give and a correct learner would not? This says nothing about prevalence.
3. **Hypothesis and candidate generation**: candidate misconceptions, distractors and probe questions [68].
4. **Interviewer rehearsal.** Practising a protocol, where plausibility matters more than fidelity [84].
5. **Coarse difficulty ranking, only after passing T2 below.** The positive results share four features: aggregate item correctness, an induced proficiency spread, often weaker models, and validation against existing real data [65][49].

**Never:** K0, K1 or K2 numbers, Stage B arm matching or the delay; power or sample-size planning (synthetic survey responses had SD 16.1 versus 31.4, and a power analysis on them suggested 33 respondents, almost an order of magnitude too few, reflecting under-dispersion and a larger simulated effect [71]); prevalence of any error or profile; intervention effects or policy choice; standing in for experts; any unlabelled figure. LLM-simulated participants in 156 psychology and management experiments produced significant effects on 68–83% of human nulls [72], so a synthetic cohort is **biased toward passing gates**.

**Labelling rule.** Every surrogate artefact carries `SYNTHETIC — not evidence about learners or experts`, the model identifier and version, the date, the prompt or spec hash, the profile spec and the validation tier reached. Surrogate artefacts live apart from study data and are never merged into `sessions/`.

**Validation tiers on public data only** (from [notes: synthetic §6]; thresholds must be pre-registered and are **our choice** — the notes found no agreed numerical standard). Each tier licenses only the uses listed.

| Tier | Test | Pass condition | Licenses |
|---|---|---|---|
| T1 | IRT on real plus simulated responses (NAEP released statistics) | Simulated ability covers the real 10th–90th percentile; SD ratio ≥ about 0.7 (the notes' proposal; 16.1/31.4 ≈ 0.5 on one ANES measure [71], our derivation) | Nothing alone |
| T2 | Item difficulty on held-out items | Spearman ρ ≥ a pre-set value (best reported r = 0.72–0.82 on aggregate item correctness [65][49]; the top end is an ensemble) **and** beats a text-feature regressor and a direct "rate the difficulty" prompt | Use 5 |
| T3 | Distractor distributions (Eedi) | Jensen–Shannon divergence and top-distractor agreement beat uniform and "most plausible distractor" baselines; dual-property test per profile [68] | Calling a profile "realistic" |
| T4 | Interaction faithfulness | Selective Flip Score above a pre-set margin over 0 [67] | Rehearsal beyond practice |
| All tiers | Population and stability checks | ≥ 3 seeds, ≥ 2 model families, ≥ 2 independently built surrogate models (Robust Evaluation Matrix [63]) | Any conclusion is otherwise "model-dependent" |

**Default expectation** from the literature: a prompted cohort passes T1 only with ensembling, may pass T2, and fails T3 at profile level and T4. Data-grounded personas are the likeliest to improve: latent classes learned from Eedi logs raised IRT-difficulty R² from 0.525 to 0.686 [81] (PROMISING).

### 12.2 Surrogate experts

**Machine consensus means surrogates are not independent samples** [48]. Persona prompts collapse to stereotype-level variation [75], models defer to stated user beliefs [173], and generative AI homogenises collective output [170]; LLM Delphi panels reached consensus more often than human experts (93.3% versus 81.5%), including on most statements humans did not agree on [74]; debate gains are mostly majority voting [76]. Cross-model ensembles do give independent-error benefits: 12 LLMs were statistically indistinguishable from 925 human forecasters on 31 questions [77] (PROMISING).

**Design** (OUR HYPOTHESIS, extending the notes):

- Surrogate experts are **corpus-partitioned retrieval agents**, STORM-style [78], over *disjoint* source families (textbooks, research papers, forums, standards).
- Each runs on a different model family and votes independently, with no debate.
- **Their disagreements are hypotheses whose value must itself be tested.** Test: do surrogate disagreements fall where planted contradictions and known real controversies are (E-PLANT)? Do they predict where held-out gold items are missed (E-CTA)? The notes found no study testing whether disjoint-corpus agents reproduce real inter-expert disagreement [notes: synthetic §4 Gaps].
- Seed questions with known answers calibrate surrogate "experts" Cooke-style [159] before their weights mean anything.

**In simulated elicitation experiments the "expert" is a held-out gold source, not an LLM persona.** The oracle is deterministic: it returns only verbatim gold item IDs (from a CTA task list, a cue list, a misconception catalogue or a departed developer's later record) matched by the frozen matcher, and never volunteers items. A perfectly cooperative oracle lacks omission behaviour, so its efficiency results are upper bounds. That removes synthetic circularity: the system is scored on recovering knowledge that humans actually produced. The cautionary case is an agent that reached 94.9% knowledge recall interviewing simulated employees — in 864 synthetic companies only [60] (SPECULATIVE for real organisations).

**Decisions.** Build the labelling rule and T1–T3 on public data NOW. Build no prompted persona cohort beyond what debugging and discriminability checks need. Use held-out gold oracles, never personas, for every elicitation-efficiency claim.

---

## 13. Public → organisation → human: the progression, reordered by evidence

The evidence supports the A→B→C order for **cost**, but changes what goes first within each world and when learner data enter.

| World | Yields reliably | Yields as hypotheses only | Cannot yield |
|---|---|---|---|
| **A: public** | Concepts, taxonomy, canonical schemas, taught heuristics, already-explicated relational knowledge, catalogued misconceptions; **cohort-level learner difficulty from public response data** | Prerequisite and causal edges; rationales; decision cues found in boundary texts | Prevalence in *your* cohort; episode-specific cues; perceptual discriminations; organisation-specific knowledge |
| **B: organisational** | Work-as-done from logs, tickets, reviews and work orders; concentration (truck factor, KaR); cue→decision policy from expert responses to recorded work [27]; which representation experts actually use | Rationale recovered from commits, PRs and design-rationale artefacts [59][172]; doc-versus-practice divergence from prose | Why the expert did it, when nothing records it; somatic and collective knowledge |
| **C: human** | Validation of residual items; episode cues via CDM [4]; perceptual discriminations via contrasting cases; individual learner state; instructional effects | — | Nothing is excluded, but it is the most expensive per item |

**Four reorderings the evidence forces** [notes: adjacent Q4; tacit Implications]:

1. **Learner errors come second, not fourth.** Real error data should precede any synthetic cohort, because grounding drives surrogate fidelity [73]. With no own learners, **public response data (Eedi, AAAS, DataShop) are World A's learner layer NOW**; if early K0 runs, it runs exactly as registered, and any use of its data for surrogate calibration is secondary.
2. **In the company track, traces come before prose.** Compare SOPs (imagined) with process-mined logs and ticket or chat histories (done); the divergence *is* the residual map there [19][124]. An AI assistant trained on a firm's customer-support conversations raised productivity 15% on average, most for less-experienced agents; that it transferred top performers' practice is suggestive [134] (PROMISING, one study).
3. **The human step is targeted and short.** The gap map names the items and knowledge types. The channel follows the type (§10.3). Experts correct rather than dictate, which attacks Szulanski's "arduous relationship" barrier [117] (SPECULATIVE until measured).
4. **Anchoring guard.** At least one human elicitation arm stays **blind to the reconstruction**. Otherwise experts anchored on the AI model will shrink the measured residual [notes: adjacent Q4 change 5].

**Decisions.** Keep A→B→C as the cost order. Treat public learner-response data as part of World A NOW. Treat traces as the first input of World B. Require a blind human arm in every later residual measurement.

---

## 14. The human knowledge residual: define it, estimate it, predict it

"Human knowledge residual" was not found as an established term. Its close analogues are CTA omission rates against a union-of-experts gold [1]; interview saturation (about 70% of themes within 6 interviews and 92% within 12, as restated in Guest et al. 2020 [143]); capture–recapture and species-richness estimation (predicted theme counts within 1–3% in simulations and under 2% on a real 1,053-participant survey [157]) [144], used in software inspection to estimate total defects from independent inspectors [145]; and Knowledge-at-Risk [110] and knowledge-loss risk assessment [121].

### 14.1 Operational definition

This definition is adopted from the notes' proposal (SPECULATIVE there, OUR HYPOTHESIS here). For a task scope *D*:

- **U(D)** is the set of *important* items, typed as concept/KC, prerequisite edge, misconception, decision cue or rule, rationale, or expert–novice contrast. Each item has an importance weight *wᵢ*, grounded in behaviour where possible: misconception prevalence, KC error rate or learning-curve slope, decision criticality in a CTA list, or post-departure incident or defect load for an organisational unit. Otherwise the weight is a panel rating recorded before comparison. **NOW uses unweighted counts as the primary analysis**; weights arrive LATER, with expert raters.
- **R** is the set of items the reconstruction produced from existing evidence (World A, or A+B), each with its label.
- **H** is the set of items humans supplied and that were **validated**: corroborated by a second expert or by a trace, as Stage A already requires.
- **Observed residual:** Res_obs = Σ_{i∈H∖R} wᵢ / Σ_{i∈H∪R_valid} wᵢ, stratified by knowledge type, with its converse R∖H (valid items the experts did not say, which Sullivan's omission result predicts). R_valid needs a validity judgement that NOW can obtain from neither an LLM judge (forbidden as criterion) nor experts (LATER), so **NOW reports recall of H plus an unvalidated R∖H count**; Res_obs proper starts when expert raters join.
- **Estimated unseen items, with a known-truth check.** Capture–recapture over text occasions (source families, model families) estimates the *written* universe, not the residual: never-written items have near-zero catchability in every World A occasion, model families share pretraining [48], source families share authors, and with 3 occasions a log-linear dependence model is saturated. Dependent occasions give *stable underestimates*, so stability proves nothing. The check that replaces it: estimate the items unseen by text from the text occasions (heterogeneity-robust Mh, jackknife, Chao1 as lower bound [144][145]), then compare with the count of published-gold items no text occasion captured, using the gold as an independent occasion (Lincoln–Petersen), against a pre-registered tolerance. A labelled synthetic simulation with planted dependence (known-truth use 1, §12) tests the estimators first.

**Pre-registered pitfalls** [notes: evaluation Implications B]: (1) **source dependence** — literature is written by experts, which biases capture–recapture low (hence the known-truth check above); (2) **unequal catchability** — stratify by type; (3) **adaptive questioning** breaks equal catchability [146], so estimate from the non-adaptive portion; (4) **granularity** — fix the codebook grain before matching; (5) **LLM matching** — only a different-family matcher meeting the §18 adoption rule, blind to P(missing) and to item origin; (6) **H is not gold** — the union of experts plus trace corroboration is; (7) **multiple saturation plateaus** [146] — never declare the residual zero from a stopping rule.

### 14.2 The gap map: predicting the residual before any human is asked

The definition above measures the residual *after* humans are asked. The project's distinctive claim is that the residual can be **predicted beforehand** (OUR HYPOTHESIS).

For each area *a* of the reconstructed model (task step, decision point, KC, component, SOP section), the gap map outputs P(important knowledge missing | a). Candidate features, each traceable to the notes: **knowledge type** (interpretations have the lowest pooled coverage [2] and decisions the highest per-expert omission [1]; perceptual and automated steps are behaviour-only); **boundary-text density** (reporting bias predicts "obvious" steps are absent from expert-to-expert text [25]); **support profile** (imagined-only support with no trace [19]; once-documented support, where hallucination pressure is highest [57]); **instability** (cross-model or cross-corpus disagreement, semantic entropy [150]); **rationale gap** ("why" absent — Szulanski's causal ambiguity [117]); and **organisational concentration**, weighted by review participation rather than raw authorship [114][115]. Surrogate disagreement and cross-model instability are synthetic outputs: they may be gap-map **predictors**, never **criteria**.

**The unknown-unknowns guard.** High-confidence errors are invisible to uncertainty sampling [149]. A fixed fraction of questions — the fraction is our choice and must be pre-registered — therefore goes to **confident-but-unverified** areas sampled by partition, not by uncertainty.

### 14.3 How the gap map is scored (zero participants)

Against a held-out gold (a CTA task list, a cue list, a misconception catalogue, or a post-departure outcome record).

**Anti-circularity rules** (pre-registration requirements). Several golds are already known to this project — their structure (46 steps split 14/27/5; 25 of 70 cues) sits in the notes — and the type feature was derived from them. So: hash-freeze the feature set, weights, scope decomposition and area partition **before acquiring any gold**; run leave-one-gold-out, so no source is both a feature source and a test gold; sandbox the pipeline from `research_notes/`; count gold items that map to no area as missed areas at a pre-registered floor score, since they are the most important unknown unknowns; keep matchers blind to P(missing); use origin-free, model-family-free item IDs.

**Scoring.** Label an area *missed* if it contains at least one important gold item the reconstruction lacks, and score P(missing) with **AUROC** at area level; score the ranked questions by gold-residual hits per question. The comparison is **ΔAUROC against the strongest** of: random; the naive type rule ("every procedural or decision area is a gap" — nearly constant on Sullivan's list, where most items are action or decision steps, so it ties heavily and is easy to beat); verbalised confidence; area size or gold items per area; retrieval-support density (the ablation of the map's best single feature); corpus frequency of area terms [56]; a plain-LLM prompt ("where would text omit expert knowledge?"); and a type prior with rates estimated on the *other* golds.

### 14.4 From gap map to questions

Question selection maximises **expected information gain** over contested model elements [147]. LM-driven elicitation surfaced considerations users had not anticipated [156], and EIG-based questioning from LLM predictive distributions beat prompting-only questioning on 20 Questions and preference-elicitation tasks [148] (PROMISING), and information-gain rewards raised task success by 38.1% on average across medical diagnosis, troubleshooting and 20 Questions [175] (PROMISING). **No study was found applying EIG to expert or CTA interviews** [notes: evaluation §4 Gaps]. Each question carries its target claim, the knowledge type, the matched channel, and a concrete probe. An organisational example from the notes: "Commit a1b2 changed the retry limit from 3 to 7; no issue, PR or ADR says why."

### 14.5 The residual corpus

Every validated item in H∖R is stored with its domain, type, the channel that revealed it, and the gap-map score it had before elicitation. Across domains this becomes a dataset of **what humans add that text never contained**. It is the training and calibration set for the gap map and, commercially, the asset competitors cannot download (OUR HYPOTHESIS; §21).

**Decisions.** Make ΔAUROC against the strongest baseline the headline metric. In NOW, report unweighted recall of H, the unvalidated R∖H count and the known-truth-checked unseen estimate, stratified by type. Never report a residual of zero.

---

## 15. Competing architectural hypotheses

These are the rival bets. Each §18 experiment is chosen to discriminate between them.

| # | Hypothesis | Predicts | Discriminating experiment | Current evidence |
|---|---|---|---|---|
| **H1** | **Reconstruct-and-locate** (this document's thesis): public/artefact reconstruction plus a calibrated gap map targets human time better than untargeted elicitation | Gap-map ΔAUROC against the strongest baseline reaches δ; EIG questions recover gold faster than baselines | E-CTA, E-OSS, E-EIG | Untested; components PROMISING [27][148] |
| **H2** | **Traces-first**: behavioural traces carry the residual; public text adds little once traces exist | Trace-based reconstruction recovers far more held-out gold than text-only; the gap map adds little over "no trace" | E-CTA with a traces arm where traces exist (Cho-style data; OSS reviews); E-DVP | Cho et al. favour it [27]: LLM+Conversation beat the no-conversation Baseline (Study 1, p < .001), and the Baseline did not differ from the expert-articulated arm (p = .502 Study 1; p = .664 Study 2) |
| **H3** | **Elicitation-efficiency first** (the fallback): skip reconstruction; make human elicitation faster and better targeted by live question selection | H1's gap map adds nothing over live EIG with a human oracle | E-EIG with and without the reconstruction prior | An LLM answering as a stand-in expert was faster but hallucinated 19–32% of ontology classes [28]; no human-oracle test possible NOW |
| **H4** | **Learner-data-first**: difficulty structure from learner logs beats both text and experts | Data-discovered KC models beat text-reconstructed and expert models on fit | E-KC | PROMISING for LFA over human models (one group) [103] and for LLM-assisted KCluster [104] |
| **H5** | **Monolithic LLM**: one model as database of truth, learner model, pedagogy and evaluator | Separated components add nothing measurable | Planted-source and abstention tests (E-PLANT, E-ABST) on the monolith versus the gated pipeline | The map rated the separation principle "supported only indirectly"; ClashEval and abstention results favour separation [51][53] |
| **H6** | **KG-centric model** versus the layered composite | A graph-only model loses nothing on behavioural tests | E-KC and E-DIST with graph-only versus KC-with-conditions representations | No controlled comparison found [notes: representation §7 Gaps] |

**The notes favour a combination:** H1 for targeting, H2 for inputs, H4 for the difficulty layer. H5 and H6 are the defaults to beat.

**Decisions.** Keep H1 as the working bet. Instrument every experiment so that H2 and H4 can win. If they do, reorder inputs; do not rescue H1. Adopt H3 wholesale if the N3 stop rule fires (§22).

---

## 16. Critical risks and reasons this may fail

| Risk | Mechanism and evidence | Kill or change signal | Mitigation |
|---|---|---|---|
| **R1 The residual is where reconstruction is blind, and the gap map is blind there too** | Reporting bias plus omission put the residual in obvious steps [25][1]; model confidence is miscalibrated off-distribution [notes: reconstruction §7] | Upper 90% bound of ΔAUROC against the strongest baseline below δ | Pivot to H3 (the N3 stop rule, §22) |
| **R2 Contamination makes World A look better than it is** | Old gold (FCI 1992, NICU 1993, Sullivan 2014) is almost certainly in pretraining, and its content has diffused into textbooks that do not cite it [151] | Probe-positive items dominate; results hold only with gold-era sources retrievable | Corpus frozen at each gold's own date, per-item memorisation probes with exclusion (§18.2) |
| **R3 Physics and maths are best cases** | Boundary-text density is highest there [notes: adjacent Q2(d), Q3] | Success in text-rich domains, failure in maintenance or OSS | Include a deliberately text-poor domain (§19); claim nothing universal before it passes |
| **R4 The residual cannot be measured reliably** | Never-written items are invisible to text occasions; dependent occasions give stable underestimates | Known-truth check against gold fails its tolerance | Planted-dependence simulation first; if the check fails, drop the residual as an objective (falsifier part 2) |
| **R5 The judge becomes the gold** | LLM judges show self-preference [152]; expert item ratings had ICC 0.07–0.18 [154] | Matcher fails the §18 adoption rule | Different-family matcher panel; one blind second coder in NOW (§18); behavioural tests preferred |
| **R6 Synthetic material leaks into conclusions** | Illusions of understanding and exploratory breadth [79] | Any gate or map entry fed by an unlabelled synthetic number | Label rule (§12); separate storage; gates refuse synthetic labels in code |
| **R7 Public boundary sources shrink** | Stack Overflow activity fell about 25% after ChatGPT, relative to comparison platforms (a lower bound) [135] | Declining yield of new boundary texts per domain | Weight World B and learnersourcing more over time |
| **R8 Authorship metrics break** | AI-generated code invalidates authorship-equals-knowledge (SPECULATIVE) [115] | Truck-factor baselines stop predicting departures in agent-era histories | Use pre-agent histories; review- and discussion-weighted concentration [114] |
| **R9 Incumbents fold it in** | People Skills already infers expertise inside Copilot | An incumbent ships coverage accounting | Differentiate on validated residual prediction and the residual corpus |
| **R10 Legal friction blocks the company wedge** | Employee-data processing, co-determination, AI Act Annex III(4) [129][131] | Pilot blocked by a works council or DPIA | Compliance defaults of §21 |
| **R11 Prompt injection through ingested documents** | Demonstrated attack class [133] | Any retrieved text acting as an instruction | Treat retrieved text as data; ACL-enforced retrieval; provenance on every claim |
| **R12 Repeating the expert-systems deletion** | Knowledge engineers deleted the situated and tacit parts of expertise [31] | Gap map blind to collective and situated types | Never score collective types as "covered" by text |
| **R13 Tooling drift, again** | The same failure as §3 | A NOW phase ends with infrastructure and no experiment result | Every NOW item ends in a gate reading an experiment result, not a build |

**Decisions.** R1, R2 and R4 are fatal-class and are tested first. R6 and R11 are controlled in code before any run. R13 is policed by the phase gates in §22.

---

## 17. Research questions

The original RQ1–RQ8 remain valid inside Track A. The reoriented programme asks:

- **RQ-A (reconstruction yield).** For a task scope, what share of held-out, human-revealed important knowledge can a gated pipeline recover from World A, and from A+B, stratified by knowledge type? (Extends RQ1 and RQ6.)
- **RQ-B (residual prediction — central).** Can the gap map predict, before any human is asked, which areas contain residual knowledge, better than the strongest pre-specified baseline, by at least a pre-registered δ?
- **RQ-C (targeting).** Do EIG-selected questions recover held-out gold per question faster than random, plain-LLM and expert-written question lists?
- **RQ-D (measurement).** Does an unseen-item estimate from text occasions match, within a pre-registered tolerance, the count of published-gold items no text occasion captured?
- **RQ-E (behavioural validity).** Do reconstructed KC and misconception models predict real learner behaviour (AFM fit, distractor choice) better than the raw LM prior and the dataset's default models? (Extends RQ3 at cohort grain.)
- **RQ-F (surrogate licence).** Which validation tier (T1–T4) can a surrogate learner reach on public data, and which uses does that license?
- **RQ-G (provenance robustness).** Does the gated pipeline resist planted false sources, surface planted contradictions and abstain on non-public objectives better than an ungated model? (Tests H5; extends RQ8.)
- **RQ-H (organisational transfer).** Does artefact coverage add predictive value for realised knowledge loss beyond authorship-only concentration (truck factor, KaR)?
- **RQ-I (generality).** Does the procedure's performance hold in a text-poor domain? (Extends RQ6.) Not answerable NOW: every residual-prediction test available is text-medium or text-rich, unless the itemised PARI task list in [106] can be obtained.
- **RQ-J (cost).** What is the cost per validated item of reconstruction versus published CTA effort?

**Central hypothesis (the object of the falsification test).** Reconstruction from public and artefact evidence, together with a calibrated gap map, locates the human knowledge residual well enough that targeted elicitation recovers more validated knowledge per human hour than untargeted elicitation.

**Decisions.** RQ-B is the project's primary question. RQ-A and RQ-D are necessary conditions for it. RQ-E through RQ-J run in parallel because they share infrastructure.

---

## 18. Experiments requiring zero participants

**Common rules.** Public ground truth only; no LLM judge as the criterion. Where matching or classification is needed: a fixed codebook, blind double coding of a sample (the notes propose at least 20%) by the owner plus **one blind second coder** — a trained labeller, not a participant, expert or interviewee — and an LLM matcher from a *different* family, adopted only if its κ against the human coders is ≥ 0.70 and not below the lower confidence bound of the human–human κ *(our choice)* [notes: evaluation Implications A]. The owner cannot be blind (they built the map and will see gold), so owner codes are made under origin blinding: no gold or reconstruction origin, no model family, no P(missing) visible. If no second coder is available, the owner codes pairs under that blinding and the report states it as a limitation. Pre-register metric, primary gold, primary model, primary baseline and threshold (§22 threshold table); log cost per validated item. Every N3 pre-registration is conditional on acquiring its gold, with pre-specified fallback golds and minimum items and missed areas.

| ID | Experiment | Public ground truth | Metric | Falsifying result | Threshold source |
|---|---|---|---|---|---|
| **E-CTA** | CTA replay: reconstruct the task before looking at the gold, then score by type and score the gap map | Sullivan et al. cricothyrotomy task list [1]; Crandall & Getchell-Reiter NICU cue categories [4]; Chao & Salvendy troubleshooting [2]; further CTA-based studies reported in [3] (e.g. Velmahos, Schaafstal; whether task lists are published is unchecked) — itemised availability of all of these is unconfirmed | Recall by step type and cues, described against the average unprompted expert (44%, 20/46; Wilson CI roughly 30–59%) and prompted CTA (66%) [1]; **ΔAUROC for the misses** (§14.3); per-item memorisation probes | Upper 90% bound of ΔAUROC below δ. Recall is descriptive only | Comparators evidence-derived [1]; δ, primary gold and minimum missed areas are our choice |
| **E-MISC** | Misconception catalogue recall, weighted by prevalence | Eedi Misconception Graph (8,000+ misconceptions, CC BY 4.0) [137] with selection rates from NeurIPS 2020 data [138]; FCI [108] and AAAS [139] for mechanics, excluding conservation items (§18.1, E-SEAL) | Recall and precision at matched grain; prevalence-weighted recall; pre- versus post-cutoff recall where a post-cutoff subset exists | Prevalence-weighted recall below 0.6 (the note's example value); **or** recall collapses post-cutoff. Eedi-derived sources are excluded from the corpus; state the graph's release date against each model's cutoff, and if it predates them all, the post-cutoff falsifier is dropped and probes carry contamination control | 0.6 is the note's example, our choice |
| **E-DIST** | Distractor-choice retrodiction from item stems only | NeurIPS 2020 option-level responses [138]; AAAS national distributions [139]; Eedi-derived sources (graph, Kaggle labels) excluded from the corpus, since they link misconceptions to these distractors | Rank correlation and KL divergence over wrong options; top-1 popular-distractor accuracy | The reconstructed misconception model does not beat raw LLM likelihood (moderate correlation [46]) | Evidence-derived baseline |
| **E-KC** | KC-model fit on real logs | DataShop datasets with expert KC models [140], and some of the ~60% of 4,639 with no KC model better than the Single-KC/Unique-step defaults [104] | AFM item-stratified CV RMSE, AIC/BIC, learning slope; versus expert model and best LFA | Not non-inferior to the expert KC model within a pre-set ΔRMSE margin on most datasets (beating Single-KC is trivial) | Baselines evidence-derived [103]; margin our choice |
| **E-OSS** | Departure natural experiment: freeze the repository at *t* before a truck-factor developer leaves; compute coverage **only from artefacts dated ≤ t**; score code units existing at *t* (git blame at *t*) | Departures from the 1,932-project corpus [112] and Chromium plus 7 [111]; truck-factor estimates [109]. Outcome: blind double-coded rationale-seeking issues and defect-fix commits per unit of post-*t* activity, as a difference-in-differences against the same units' pre-*t* rate; abandoned files only as a covariate, since they are defined by authorship | ΔAUROC or rank-correlation gain of the gap map over the strongest of prior trouble, size, churn, doc-link/comment density, truck factor and KaR | Upper 90% bound of the gain below δ | Our choice. Departures counted from a power calculation (tens, not 3–5) with a minimum post-departure activity; contamination via (a) low-visibility repositories plus memorisation probes on post-*t* issue titles, excluding hits, or (b) outcome windows after every model's cutoff with review-weighted concentration [114]; developers pseudonymised in all outputs, legitimate-interest basis recorded. No validation of KLRA against realised loss was found [notes: organisational §7] |
| **E-DVP** | Doc-versus-practice divergence in OSS | Gap map computed from docs and reviews before *t*; scored on norms enforced after *t* in review comments, rejected PRs and maintainer corrections (blind double-coded); documentation-issue taxonomy as labels [116] | Share of review-enforced norms absent from docs; ΔAUROC over the E-OSS baselines | Upper 90% bound of the gain below δ | Our choice. No public SOP-plus-execution-log pair was found [notes: organisational §4]; OSS is the proxy |
| **E-PLANT** | Planted contradictions and planted false sources | A known-false plausible source (ClashEval-style [51]) and real conflicts (WikiContradict-style [52]) injected into the corpus | Adoption rate of planted falsehoods; contradiction-flag recall; whether surrogate disagreements fall on planted conflicts | Gated pipeline adopts planted falsehoods at a rate not below the ungated model (baseline over 60% [51]) | Evidence-derived baseline |
| **E-ABST** | Abstention probes | Real-but-private objectives, e.g. the owner's own code conventions (fictional objectives are trivially detectable) | False-answer rate; share of "insufficient evidence" outputs | The pipeline's false-answer rate is not below the raw model's by the pre-set margin | Our choice (AbstentionBench logic [53]) |
| **E-EIG** | Question selection against a held-out gold oracle | E-CTA or E-MISC gold, or a departed developer's later record, behind the deterministic oracle of §12.2 (upper bound) | Gold items recovered per question (area under the curve); questions to reach 90% of recoverable gold | EIG does not beat random, plain-LLM and expert-written question lists; **EIG without the reconstruction prior** is the H1-versus-H3 discriminator [notes: evaluation E8] | Evidence-derived baselines; the 90% target is the note's |
| **E-SYN** | Synthetic-learner validation tiers | NAEP released statistics [66][49]; Eedi responses; DataShop and ASSISTments logs | T1–T4 as in §12 | Fails T2 and T3: surrogates are restricted to uses 1–4 | Our choice (no agreed standard found) |
| **E-COST** | Cost ledger | All runs; published CTA effort for comparison | Tokens, dollars and wall-clock per validated item; cost–accuracy frontier [153] | — (informs, does not falsify) | — |

### 18.1 Supporting and follow-on experiments

- **E-HOLD (temporal holdout; secondary).** *T* must post-date the cutoff of **every** model in the chain (generator, other-family verifier, matcher, instability-feature models). With frontier cutoffs around mid-2026, the window is a few months and post-cutoff published CTA task lists may not exist, so E-HOLD is secondary; misconception, CTA and inventory papers after *T* (PRPER, JRST, Acad. Med., EDM/LAK) are scored on topics matched to pre-*T* papers, with the post-versus-pre recall drop that counts as "far below" fixed in advance.
- **E-NOV (expert–novice contrast recovery).** Can the model predict which problem pairs experts versus novices group together [23]? Falsified if its predictions sit at surface-feature level.
- **E-DIFF (sanity only).** Item difficulty on the BEA 2024 USMLE items. The best known system reached RMSE 0.299 against a dummy baseline of 0.311 [141], so this is near floor for everyone and is not a gate.
- **E-SEAL (sealed predictions for Track A).** Generate two predictions **by script, straight into an encrypted file, without display**, and hash-commit them: the early-K0 error-category distribution (only after the early-K0 items are frozen in their registration) and the reconstructed operation list for the Stage A problems, from public sources only. Unseal only after K1 adjudication is locked, and match them with coders who hold no Track A role. NOW mechanics runs exclude conservation items; anyone who has seen reconstructed conservation content is ineligible for any Track A human role (interviewer, corroborating coder, K1 "absent" coder, importance rater), otherwise K1's AI-versus-human contrast is confounded. Comparisons are secondary and non-gating [notes: adjacent Q4 change 6] and cannot change what K0 or K1 decides.

### 18.2 Contamination handling for E-CTA

The CTA gold papers predate every frontier model, and their content has diffused into textbooks and guidelines that do not cite them, so removing the gold paper and its citing works does not remove it. Instead: **freeze the retrieval corpus at each gold's own publication date** using dated sources (OpenAlex `publication_date` earlier than the gold; Wayback snapshots), which directly measures "was this written before experts revealed it?"; run guided-completion memorisation probes per gold item [151] and **exclude probe-positive items from the primary analysis**; prefer open-weight models with documented cutoffs. Parametric memory cannot be removed, so recall remains an upper bound.

**Decisions.** Run E-CTA and E-OSS first: together they decide the central hypothesis. E-MISC, E-DIST and E-KC run next, on shared infrastructure. E-PLANT and E-ABST gate the pipeline itself before its outputs are trusted. E-SYN and E-SEAL are cheap and can start at once.

---

## 19. Cross-domain benchmark strategy: choose domains by gold, and spread text-richness on purpose

The notes recommend choosing domains by which of three test families have public gold, not by topical breadth. The families are coverage against a gold list, behavioural fit and response retrodiction. Only mathematics has all three at scale [notes: evaluation §6]. The red team adds that physics and mathematics are best cases and that a text-poor domain is needed as a falsification target [notes: adjacent Q2(d)]. The panel spans both axes.

| Domain | Role | Public gold | Tests possible | Text-richness | Licence and access constraints |
|---|---|---|---|---|---|
| **Middle-school mathematics** | Strongest learner-difficulty gold (it measures learner misconceptions, not the expert residual); not a calibration set for other domains | Eedi Misconception Graph [137]; NeurIPS 2020 responses [138]; DataShop and ASSISTments logs [140]; Kaggle Eedi competition | All three | High | Graph CC BY 4.0; NeurIPS 2020 data, DataShop and ASSISTments terms **not verified**; Kaggle competition terms **not verified**; EdNet (CC BY-NC) and Junyi (CC BY-NC-SA) are **non-commercial** |
| **Introductory mechanics** | Best case; reconnects to Track A | FCI distractor taxonomy [108] (GPT-4 scored 83% on it, so contamination is likely [50]); AAAS item distributions [139]; Chi-style contrasts [23]; DataShop physics logs (availability **not verified**) | Coverage and retrodiction; KC fit if logs exist | Very high (best case) | FCI access terms on PhysPort **not verified**; AAAS licence **not verified**; the original AAAS host did not respond, a mirror resolves |
| **Clinical procedural (surgery, NICU)** | Direct CTA gold for residual measurement | Sullivan task list [1]; Crandall & Getchell-Reiter cue categories [4] — **availability of the itemised 70-cue list not verified**; BEA 2024 USMLE items [141]; AAMC EPAs | Coverage against CTA gold; difficulty sanity check | Medium: concepts rich, cues poor | AAMC, USMLE outline licences **not verified** |
| **OSS onboarding and knowledge-at-risk** | Organisational family; realised-loss outcomes | Truck-factor corpora [109][112]; Chromium plus 7 [111]; rationale datasets (Linux OOM-killer; 100 Stack Overflow/GitHub problems; 30 developer-written ADDs) [59]; documentation-issue taxonomy [116]; DeepWiki pages as a baseline to beat [126] | Coverage; retrospective prediction of loss (E-OSS); doc-versus-practice (E-DVP) | Medium; rationale poor | Repository licences per project; the Stack Exchange dump bars LLM-training use, and evaluation use appears within its terms — the note author's reading, not legal advice [notes: evaluation §1]; authorship threat after agentic coding [115] |
| **Industrial maintenance troubleshooting** | Deliberately text-poor; long-tail and abstention stress | MaintIE schema and benchmark [123]; MaintNet logbooks [123]; O*NET task lists (CC BY 4.0) [142]; excavator dataset of 5,485 work orders for 5 excavators [123][177] | Coverage and abstention; residual prediction only if the itemised PARI list in [106] is obtainable | Low (terse, jargon-heavy [122]) | The UWA host failed DNS in the notes' session; ISO/IEC standards are paywalled and need a licence |

**A qualification.** The notes found no public human-revealed residual gold for maintenance (nor for IT operations or OSS onboarding [notes: evaluation §6 Gaps]), and no paired SOP-plus-execution-log corpus. Maintenance therefore tests **abstention, long-tail decay and schema coverage**. A candidate text-poor residual gold does exist: [106] is a PARI analysis of aircraft-maintenance troubleshooting (200+ technicians), but whether its itemised task list is public is unchecked. Until it is obtained, **generality (RQ-I) cannot be tested NOW**: every residual-prediction test is text-medium or text-rich. OSS carries the organisational residual test through realised-loss outcomes. The gap map is frozen before each new domain (leave-one-domain-out); mathematics does not calibrate it for clinical or OSS.

**Contamination and popularity.** Apply §18.2 in every domain, report memorisation probes next to every recall figure [151], and stratify every metric by the concept's corpus frequency to expose long-tail decay [56].

**Decisions.** Run mathematics and clinical first: they give the best gold for recall and residual prediction. Run OSS in parallel as the organisational falsification test. Use mechanics to connect to Track A and as the best-case ceiling. Use maintenance for abstention and long-tail only, until the [106] task list is obtained. Check every licence marked "not verified" before downloading, and exclude NC/ND material from anything that could become commercial.

---

## 20. Later human validation strategy

New-track human validation comes in increasing order of cost, each step triggered by a NOW gate, not by calendar. Track A is the exception: it starts only on its own registered preconditions.

1. **More labellers** (beyond NOW's one blind second coder): guard calibration (the 60 items exist); a conformal-factuality calibration set in the target domain [55].
2. **Experts as raters, in minutes**, drawn from high-validity environments with feedback, where intuition can be trusted [18]. Written scenario tests with expert-rated response options predicted job performance in several studies [30], so expert judgement of reconstructed claims is cheap to collect. Their independence from general ability is contested [30], so ratings validate content, not people. Cooke seed questions calibrate each rater [159]; surprisingly-popular prompts protect minority knowledge [160].
3. **Targeted residual interviews**, driven by the gap map's ranked questions, using the reused turn contract and leading-question guard, with **one arm blind to the reconstruction**, and channels matched to type: observation and traces for automated procedure (think-aloud only as a non-reactive supplement [9][11]), contrasting-case classification for perceptual cues [24], CDM probes for episode-specific cues [16].
4. **Minimal real learner data**: a small error sample to calibrate surrogates. If early K0 runs, it runs exactly as registered (at least 100 errored solutions, items registered before the quiz); surrogate calibration and the E-SEAL comparison are secondary uses of its data.
5. **Track A as prepared**, all registered rules unchanged, on its own preconditions. Two secondary, non-gating additions are allowed if pre-registered before Stage A, subject to E-SEAL's eligibility and unsealing rules: the sealed reconstruction's coverage of K1's new shared operations, and Res_obs on Stage A's validated operations. Stage A's coding already supplies trace corroboration, the "absent from ordinary material" check and the published-framework tag.
6. **Organisational pilot**: one partner's artefacts in artefact-coverage mode, pseudonymised concentration, a DPIA, a works agreement where German co-determination applies, no evaluation use.

Neither experts nor learners are needed to test whether the gap map predicts held-out, human-revealed knowledge; that is the NOW programme (what each is needed for: Final Test Q4–Q5).

**Decisions.** Recruit no one for the new tracks until E-CTA and E-OSS have read out; Track A is unaffected. If the gap map passes, the first human spend is expert raters (step 2), not interviews. If it fails, the first human spend is H3: live EIG-driven elicitation with a blind arm.

---

## 21. Commercial product implications: the primitive is residual accounting, the wedge is knowledge-at-risk

**The primitive, not a UI.** Per critical unit, the system returns what the evidence covers (with provenance), what it contradicts, what is decided without rationale, who — with consent — is the only evidence, how likely important knowledge is missing, and the short ranked list of questions that would close the biggest gaps (OUR HYPOTHESIS).

**White space** [notes: organisational §5]. The market has split three ways: retrieval and answer engines (Glean, Copilot, Rovo, Guru — Glean reported $200M ARR in December 2025 and a $7.2B valuation in June 2025 [127]); frontline capture tools (Dozuki, Augmentir, Tulip), which record what experts choose to show; and code-understanding tools (DeepWiki, Swimm) that generate documentation from code [126]. **None found computes "what the documents already cover versus what only experts know" as a first-class output.** Interloom raised $16.5M in March 2026 to capture tacit "corporate memory", its CEO arguing that outside software "the evaluation has to come from a human expert" [128] (grey, funding signal). Microsoft retired Viva Topics on 22 February 2025, citing a shift to Copilot-based knowledge experiences [125]. That is **weak evidence** of KM product failure — no adoption figures were found and the stated reason was strategic — and expert inference moved into People Skills, so incumbents will fold expertise inference into platforms.

**First wedge** (OUR HYPOTHESIS):

- **What.** Organisational knowledge-at-risk: retiring-expert capture in operations-heavy firms, and platform or service onboarding in software organisations.
- **Why.** A clear payer. A measurable outcome (realised loss after departures, which E-OSS validates on public data first). Existing practices already accept a person-level risk score — TVA/IAEA's attrition × position-criticality factor [121] — whose criticality term the coverage axis can replace with a measurement.
- **Education's role.** The **research testbed**; as a first market it is slower and carries Annex III(3)(b) exposure once individual learning outcomes are evaluated.

**Defensibility** (OUR HYPOTHESIS): a **validated residual predictor** (measured ΔAUROC per domain and knowledge type), the **accumulating residual corpus** (§14.5) that an incumbent cannot scrape, and calibrated **elicitation protocols** per knowledge type. Search, wikis and item generation already exist.

**Legal constraints (information, not legal advice):**

- **EU AI Act Annex III** covers education (evaluating learning outcomes, including steering learning) and employment (allocating tasks by individual behaviour; monitoring and evaluating performance) [129]. Stand-alone Annex III obligations apply from **2 December 2027** under the Digital Omnibus on AI, per secondary sources [130]; its reported number, Regulation (EU) 2026/1744, was **not verified** on EUR-Lex. The Art. 6(3) derogation covers systems that detect patterns without replacing or influencing the previously completed human assessment without proper review, but Annex III systems that profile natural persons are always high-risk [129] — which bears directly on person-level expertise inference.
- **GDPR.** Mining employees' messages and Git history to infer who knows what is processing personal data: legitimate interest under Art. 6(1)(f) with a balancing test is the usual basis, consent is weak in employment, systematic monitoring triggers a DPIA (Art. 35), and Art. 88 allows national employment rules (via secondary sources).
- **Germany, § 87(1) no. 6 BetrVG.** A system *objectively capable* of monitoring behaviour or performance needs works-council co-determination, even when that is not its purpose [131].
- **Copyright.** EU DSM Art. 4 permits commercial text-and-data mining unless the rightholder has reserved it in an appropriate, for example machine-readable, way [132]. CC NC and ND material, paywalled standards (ISO/IEC) and non-commercial datasets (EdNet, Junyi) need separate licences.
- **Security.** Indirect prompt injection through ingested documents is demonstrated [133]; retrieval must enforce per-user ACLs and treat retrieved text as data.

**Product design consequences.** Default to **artefact-coverage mode** ("this subsystem's rationale is undocumented"); person-attributed concentration only pseudonymised or with consent to be named; no use of outputs for evaluating or allocating people; cohort-level, not individual, diagnosis in education.

**Decisions.** Pursue no customer data until E-OSS reads out. Build the compliance defaults into the core, not as an enterprise add-on. Do not claim to "convert tacit knowledge" — the evidence supports locating and scoping it [29].

---

## 22. Revised project phases: NOW, LATER, MUCH LATER

**NOW** means zero participants, zero proprietary customer data, zero microphones and zero live expert interviews. It is dominated by autonomous research, domain reconstruction, provenance, cohort construction, evaluation, cross-domain experiments and falsification. Every NOW item ends in a continue / change / stop decision.

**The one human input NOW uses is one blind second coder**: a trained labeller with no domain expertise required, who codes matches and OSS outcomes blind to origin. That is labelling, not participation — no one is studied, interviewed or asked for expertise — but it is a person, and **the owner should confirm it is acceptable**. Fallback: the owner codes pairs under origin blinding (§18), reported as a limitation.

**Threshold key.** *(evidence)* = derived from a baseline or figure in the notes. *(our choice)* = a judgement to pre-register before the data it judges, as the project already does with *(project choice)*.

**Thresholds to fix before gold acquisition** (all *our choice*; a default is given only where the notes or reviewers supply one):

| Threshold | Used in | Proposed default |
|---|---|---|
| ΔAUROC smallest effect of interest δ | N3, E-CTA, E-OSS, E-DVP | to set |
| Primary gold, primary model, primary baseline; multiplicity rule | N3 | to set; Holm correction, or pooled random-effects ΔAUROC across golds |
| Minimum items and missed areas per gold (precision/power calculation); fallback golds | N3 | to set |
| Floor score for unmappable gold items | §14.3 | to set |
| E-OSS departures and minimum post-departure activity | E-OSS | to set by power calculation (tens of departures, not 3–5) |
| "Dominate" for a change to H2 (OSS only) | N3 | to set |
| E-HOLD "far below" (post- versus pre-*T* recall drop) | E-HOLD | to set |
| "A handful" of ad-hoc fields | N1 | to set |
| False-answer margin versus the raw model | N2, E-ABST | to set |
| Known-truth tolerance and numeric "stable" for the unseen estimate | N5 | to set |
| LLM-matcher adoption κ | §18 | ≥ 0.70 and not below the human–human κ lower CI bound |
| E-KC non-inferiority ΔRMSE margin | E-KC, N4 | to set |
| E-MISC prevalence-weighted recall | E-MISC, N4 | 0.6 (the note's example) |
| T1 SD ratio | E-SYN | about 0.7 (the notes' proposal) |
| T2 ρ | E-SYN | to set (best reported r = 0.72–0.82 [65][49]) |
| T4 Selective Flip Score margin over 0 | E-SYN | to set |
| Unknown-unknowns question fraction | §14.2 | to set |

| # | NOW item | Output | Gate: continue / change / stop |
|---|---|---|---|
| N0 | Reset and housekeeping (owner-approved edits only) | `check-dois` path fixed; Track A labelled frozen; `CLAUDE.md` scope and `PROGRESS.md` NEXT rewritten; new domain-neutral package created for reused components | Continue when the DOI hook demonstrably fires on a test edit. No experiment waits on the rest |
| N1 | Claim record, six epistemic labels, knowledge-type vocabulary, gap-map fields | Schema plus validators; labels enforced in code; synthetic labels refused by any gate function | **Continue** if every gold item from mathematics, clinical and OSS sources can be expressed without new field types. **Change** the schema if more than "a handful" (threshold table) need ad-hoc fields. No stop condition. The schema, features and area partition are hash-frozen here, before any gold is acquired (§14.3) |
| N2 | Gated reconstruction pipeline v0 plus pipeline robustness tests (E-PLANT, E-ABST) | Pipeline over curated and boundary sources; ledger | **Continue** if planted-falsehood adoption is below the ungated model's (baseline over 60% [51]) *(evidence baseline)*, and the false-answer rate on real-but-private objectives is below the raw model's by the pre-set margin *(our choice)*. **Change**: add verifier stages or restrict corpora. **Stop** building on it if gating does not beat the ungated model at all |
| N3 | **Central test**: E-CTA (clinical and troubleshooting gold) and E-OSS, pre-registered conditional on gold acquisition | ΔAUROC against the strongest baseline on the primary gold and model; recall by type (descriptive) | **Stop H1 targeting and pivot to H3** if the upper 90% bound of ΔAUROC is below δ, regardless of recall. **Continue H1** if the lower 90% bound exceeds 0 and the point estimate is at least δ. **Otherwise inconclusive**: run the next pre-registered fallback gold once, then apply the same rule. **Change to H2** (traces first) only from E-OSS, where traces exist, if trace-based inputs "dominate" (threshold table); E-CTA has no public traces. Recall, against the 44% average-unprompted-expert comparator (Wilson CI roughly 30–59%) [1], decides only whether reconstruction survives as a draft for experts to correct. All thresholds *(our choice)* |
| N4 | Behavioural validity: E-KC, E-DIST, E-MISC | Fit, retrodiction and prevalence-weighted recall | **Continue** if E-KC is non-inferior to the expert KC model within the pre-set margin and E-DIST beats raw LLM likelihood *(evidence baselines)*, and E-MISC prevalence-weighted recall ≥ 0.6 *(the note's example; our choice)*. **Change**: move the difficulty layer to learner-data-first (H4) if data-driven models dominate. **Stop** using reconstructed misconception models for diagnosis if E-DIST fails |
| N5 | Residual measurement on the N3 and N4 gold, stratified by type | Unweighted recall of H; unvalidated R∖H count; unseen-item estimate; planted-dependence simulation | **Continue** if the text-occasion estimate of unseen items matches the gold-as-occasion count within the pre-set tolerance *(our choice)*. **Stop** using the residual as an objective if it does not (falsifier part 2) |
| N6 | Question selection: E-EIG against held-out gold oracles | Recovery curves for EIG, EIG without the reconstruction prior, partition sampling, plain-LLM, expert-written lists and random (deterministic oracle; upper bounds) | **Continue** if EIG beats random, plain-LLM and expert-written lists *(evidence baselines)*; if EIG without the prior matches it, that favours H3. **Change** to partition-plus-uncertainty sampling if that wins. **Stop** the active-acquisition claim if neither beats random |
| N7 | Surrogates: labelling rule, E-SYN tiers T1–T3, known-truth pipeline tests | Tier reached per model family; licensed uses | **Continue** uses 1–4 regardless. **Change**: license use 5 only on a T2 pass (threshold table). **Stop** any profile-level use on a T3 failure — the expected default |
| N8 | E-SEAL: sealed Track A predictions | Encrypted, undisplayed, hash-committed predictions | No gate: secondary and non-gating; eligibility and unsealing rules in §18.1 |
| N9 | E-COST ledger (continuous) | Cost per validated item; frontier | Informs N3–N6 decisions; no gate of its own |

**Order.** N0–N2 first, briefly. N3 is the critical path. N4–N7 run in parallel on shared infrastructure. N8 and N9 start immediately.

**Programme gate.** If N3 fires the stop rule, the reorientation's central hypothesis is falsified and the project becomes an elicitation-efficiency tool (H3), keeping N1, N2 and N6 as its core. N3 gates only **new-track** human spending; it neither schedules nor blocks Track A.

**LATER** (a few humans, no cohort study, no customer data by default), beginning only after N3 continues or pivots to H3: further labellers for guard and conformal calibration; importance weights for Res_obs; expert raters (§20 step 2); targeted residual interviews with a blind arm (§20 step 3); a small real learner error sample; one organisational pilot in artefact-coverage mode under a DPIA and works agreement; learnersourcing experiments; the post-hoc Track A comparisons if Track A has started.

**MUCH LATER for the new tracks** (Track A runs on its own registered preconditions, whenever they are met, not on this schedule): learner-facing modules and adaptive policy; live LLM generation facing learners, with pedagogy-matched design [167] and guardrails (unguarded GPT-4 raised practice performance 48% and lowered unassisted exam performance 17% [166]); instructional RCTs; per-student diagnosis (Annex III exposure); commercial deployment beyond pilots.

**Decisions.** Adopt this phase table as the replacement for the roadmap's governing role. Treat any NOW item that ends in infrastructure without a gate reading as a failure of the plan (R13).

---

## 23. What NOT to build yet

- **No new session, audio, tablet or transcription work**; the instrument is frozen with Track A.
- **No prompted persona cohort** beyond debugging and discriminability checks, and **no LLM-persona oracle**; nothing that produces prevalence, effect sizes or power estimates.
- **No learner-facing tutor, adaptive policy or knowledge-tracing layer.** "How to teach" and "what this person knows" need learners.
- **No UI** beyond what an experiment needs to be inspected. The primitive is an output, not a front end.
- **No GraphRAG-style graph as the domain model.** Its quality evidence is LLM-judged preference [42]; a graph is index only.
- **No new ontology** beyond the four missing objects (§10.2).
- **No conformal-factuality layer** until a human-labelled calibration set exists [55].
- **No ingestion of customer or employee data**, and no person-attributed expertise inference.
- **No threshold-concept or "stable misconception" node types** without an operational test [notes: adjacent Q1].
- **No edits under `instrument/`**, including `instrument/prompts/` (frozen once `prereg.json` exists) and the Track A codebooks. Reuse by copying.

**Decisions.** Enforce the last item mechanically: the existing `guard-frozen-prompts` and `run-instrument-tests` hooks stay active.

---

## 24. Immediate next steps

For the owner to approve, in order:

1. **Decide on this document.** If accepted, approve these edits:
   - rewrite `CLAUDE.md` "Current priority and scope" and "Prepared experiment branch" to point at NOW and label Track A frozen;
   - rewrite `PROGRESS.md` "Current priority" and NEXT;
   - reframe map §1, §7 and §9;
   - fix `.claude/settings.json` to call `check-dois.py`.
2. **Drain the lessons queue** with `implement-ll`. The drift lesson (a plan whose only admissible evidence needs unavailable people defaults to tooling) is already queued in `docs/lessons.md`.
3. **Create the domain-neutral package.** Copy the taxonomy, status tags, turn contract and guard, the `agreement`, `calibration`, `baseline` and `corroboration` statistics, and the `FrozenConfig` pattern. Add the claim record and the six labels (N1).
4. **Fix the threshold table (§22) and pre-register E-CTA and E-OSS** before acquiring gold: primary gold, model and baseline, δ, minimum missed areas and fallback golds, the frozen feature set and area partition, the full baseline sets (§14.3, E-OSS), dated-corpus and memorisation-probe rules, model identifiers and cutoffs. Confirm the blind second coder with the owner.
5. **Collect gold.** Obtain the Sullivan task list and the Crandall & Getchell-Reiter cue material (verify that an itemised list exists); two to three further CTA task lists (candidates in [3]; availability unchecked); and the OSS departures the power calculation requires (tens, not 3–5), under the contamination option chosen in E-OSS.
6. **Verify licences** for the Eedi NeurIPS 2020 data, DataShop, ASSISTments, AAAS items and the FCI before downloading.
7. **Generate E-SEAL's predictions by script into an encrypted file**, without display, and commit only their hashes; the K0 prediction waits until the early-K0 items are frozen in their registration.
8. **Build N2's gates**: resolution, span verification, contradiction clustering, label enforcement. Then run E-PLANT and E-ABST.
9. **Rewrite `methods-critic`'s checklist** for zero-participant and surrogate designs, and run it on the E-CTA and E-OSS pre-registrations.
10. **Run `citation-verifier` on this document.** Several references are flagged unverified, from memory or secondary.

**Decisions.** Steps 1–2 are owner decisions. Steps 3–10 need no participants and can start the day the owner accepts.

---

## 25. Minimal reading list

Optional, as all reading in this project is; nothing here is a prerequisite. Eight items cover the argument.

1. Sullivan et al. 2014 [1] — what expert omission looks like when measured, and why the gold is circular.
2. Crandall & Getchell-Reiter 1993 [4] — the one quantified "text lacks the cues" datum.
3. Collins 2010, or its reviews [15] — which tacit knowledge is explicable in principle.
4. Cho et al. 2026 [27] — traces beat articulation; the strongest precedent, and why it is about World B.
5. Gordon & Van Durme 2013 [25] — reporting bias, the mechanism behind the twist.
6. Doroudi et al. 2017 [63] and Cui et al. 2025 [72] — why simulated learners and participants cannot decide anything.
7. Rigby et al. 2016 [110] — Knowledge-at-Risk, the organisational measurement precedent.
8. Mislevy & Riconscente 2005 [87] with Koedinger et al. 2012 (KLI) [86] — the representation backbone.

---

## 26. References

Identifiers are as given in the notes. **Flags:** *unverified* = the notes could not confirm the identifier or content; *memory* = figures recalled by the note author; *secondary* = figures via a secondary source; *grey* = vendor, press or blog source; *preprint* = not peer reviewed.

1. Sullivan ME et al. 2014. Acad Med 89(5):811–816. doi:10.1097/ACM.0000000000000224
2. Chao C-J, Salvendy G 1994. IJHCI 6(2). doi:10.1080/10447319409526093 (figures as reported in [3])
3. Clark RE, Feldon DF, van Merriënboer JJG, Yates KA, Early S 2008. Cognitive task analysis (chapter). https://hpttreasures.wordpress.com/wp-content/uploads/2025/11/cta_chapter_2007-1.pdf
4. Crandall B, Getchell-Reiter K 1993. Adv Nurs Sci 16(1):42. doi:10.1097/00012272-199309000-00006 (numbers as reported in [3])
5. Tofel-Grehl C, Feldon DF 2013. JCEDM 7(3):293–304. doi:10.1177/1555343412474821 (full text not accessed; per-method effects unverified)
6. Edwards TC et al. 2021. BJS Open 5(6):zrab122. doi:10.1093/bjsopen/zrab122
7. Anderson JR 1982. Psych Rev 89(4):369. doi:10.1037/0033-295X.89.4.369
8. Feldon DF 2007. Educ Psych Rev 19:91. doi:10.1007/s10648-006-9009-0
9. Fox MC, Ericsson KA, Best R 2011. Psych Bull 137(2):316. doi:10.1037/a0021663
10. Nisbett RE, Wilson TD 1977. Psych Rev 84(3):231. doi:10.1037/0033-295X.84.3.231
11. Ericsson KA, Simon HA 1980. Psych Rev 87(3):215. doi:10.1037/0033-295X.87.3.215
12. Nathan MJ, Petrosino A 2003. AERJ 40(4):905. doi:10.3102/00028312040004905
13. Hinds PJ 1999. JEP: Applied 5(2):205. doi:10.1037/1076-898X.5.2.205
14. Burton AM, Shadbolt NR, Rugg G, Hedgecock AP 1990. Knowledge Acquisition 2(2):167. doi:10.1016/S1042-8143(05)80010-X
15. Collins H 2010. Tacit and Explicit Knowledge. U Chicago Press. doi:10.7208/chicago/9780226113821.001.0001
16. Klein GA, Calderwood R, MacGregor D 1989. IEEE Trans SMC 19(3):462. doi:10.1109/21.31053
17. Militello LG, Hutton RJB 1998. Ergonomics 41(11):1618. doi:10.1080/001401398186108
18. Kahneman D, Klein G 2009. Am Psychologist 64(6):515. doi:10.1037/a0016755
19. Hollnagel E 2017. Why is work-as-imagined different from work-as-done? doi:10.1201/9781315605739-24; Hollnagel E, Safety-I and Safety-II. doi:10.1201/9781315607511
20. Collins HM 1974. Science Studies 4(2):165. doi:10.1177/030631277400400203
21. MacKenzie D, Spinardi G 1995. Am J Sociology 101(1):44. doi:10.1086/230699
22. Kellman PJ, Massey CM, Son JY 2010. Topics Cogn Sci 2(2):285. doi:10.1111/j.1756-8765.2009.01053.x; Kellman PJ, Garrigan P 2009. Phys Life Rev 6(2):53. doi:10.1016/j.plrev.2008.12.001
23. Chi MTH, Feltovich PJ, Glaser R 1981. Cognitive Science 5(2):121. doi:10.1207/s15516709cog0502_2
24. Biederman I, Shiffrar MM 1987. JEP: LMC 13(4):640. doi:10.1037/0278-7393.13.4.640
25. Gordon J, Van Durme B 2013. Reporting bias and knowledge acquisition. doi:10.1145/2509558.2509563
26. Paik C et al. 2021. EMNLP. arXiv:2110.08182
27. Cho, Funk, Gupta, Yang 2026. Large Language Models Explain Experts Better Than Experts Themselves. arXiv:2608.07488 (preprint)
28. van den Bent, Pernisch, Schlobach. Investigating Knowledge Elicitation Automation with LLMs. https://www.semantic-web-journal.net/system/files/swj3868.pdf (listed as a Semantic Web Journal submission; PDF header says Transportation Research Record 2025; venue unverified)
29. Gourlay S 2006. J Mgmt Studies 43(7):1415. doi:10.1111/j.1467-6486.2006.00637.x; Nonaka I 1994. Org Sci 5(1):14. doi:10.1287/orsc.5.1.14
30. Wagner RK, Sternberg RJ 1985. JPSP 49(2):436. doi:10.1037/0022-3514.49.2.436; Gottfredson LS 2003. Intelligence 31(4):343. doi:10.1016/S0160-2896(02)00085-5
31. Forsythe DE 1993. Social Studies of Science. doi:10.1177/0306312793023003002
32. Orr J 1996, review record doi:10.2307/2655659; Brown JS, Duguid P 1991. Org Sci. doi:10.1287/orsc.2.1.40
33. Middendorf J, Pace D 2004. New Dir Teach Learn 2004(98):1. doi:10.1002/tl.142
34. Liu NF, Zhang T, Liang P 2023. arXiv:2304.09848
35. Venkit et al. 2025. DeepTRACE. arXiv:2509.04499
36. Onweller et al. 2026. arXiv:2605.06635 (preprint)
37. Rao et al. 2026. arXiv:2604.03173 (preprint)
38. Yifei et al. 2025. ResearchQA. arXiv:2509.00496
39. Skarlinski et al. 2024. PaperQA2. arXiv:2409.13740
40. Asai et al. 2026. Nature 650:857–863 (OpenScholar). doi:10.1038/s41586-025-10072-4; arXiv:2411.14199
41. Babaei Giglou H et al. 2023. LLMs4OL. arXiv:2307.16648
42. Edge D et al. 2024. GraphRAG. arXiv:2404.16130; Xiang et al. 2025. GraphRAG-Bench. arXiv:2506.05690
43. Moore S et al. 2024. L@S. arXiv:2405.20526
44. Le et al. 2025. ESCO-PrereqSkill. arXiv:2507.18479
45. Feng W et al. 2024. NAACL Findings. arXiv:2404.02124
46. Liu, Sonkar, Baraniuk 2025. arXiv:2502.15140
47. Tufino et al. 2026. arXiv:2605.09602 (preprint)
48. Li et al. 2025. arXiv:2512.18880
49. Acquaye et al. 2026. arXiv:2601.09953 (preprint; reports top-distractor match of about 31–47%; no "63%" figure exists in it)
50. Kieser F, Wulff P, Kuhn J, Küchemann S 2023. Phys Rev PER 19:020150. doi:10.1103/PhysRevPhysEducRes.19.020150
51. Wu K et al. 2024. ClashEval. arXiv:2404.10198
52. Hou Y et al. 2024. WikiContradict. arXiv:2406.13805
53. Kirichenko P et al. 2025. AbstentionBench. arXiv:2506.09038
54. Joren H et al. 2025. Sufficient context. arXiv:2411.06037
55. Mohri C, Hashimoto T 2024. Conformal factuality. arXiv:2402.10978
56. Kandpal N et al. 2023. arXiv:2211.08411
57. Kalai AT, Vempala SS 2024. arXiv:2311.14648; Kalai AT et al. 2025. arXiv:2509.04664
58. Walters WH, Wilder EI 2023. Sci Rep. doi:10.1038/s41598-023-41032-5
59. Zhou X et al. 2025. arXiv:2504.20781; Dhaouadi, Oakes, Famelis 2024. doi:10.1145/3643916.3644413; Karan, Dhar, Soliman 2026. arXiv:2609.03721 (preprint)
60. Zuin et al. 2025. arXiv:2507.03811 (synthetic companies only)
61. Wu KZL et al. 2025. SourceCheckup. Nat Commun. doi:10.1038/s41467-025-58551-6
62. Min S et al. 2023. FActScore. arXiv:2305.14251
63. Doroudi S, Aleven V, Brunskill E 2017. L@S. ERIC ED577159. https://files.eric.ed.gov/fulltext/ED577159.pdf
64. Käser T, Alexandron G 2023/24. IJAIED. doi:10.1007/s40593-023-00337-2
65. Lu X, Wang X 2024. Generative Students. L@S. doi:10.1145/3657604.3662031
66. Srivatsa, Maurya, Kochmar 2025. BEA@ACL. arXiv:2507.08232
67. Do, Sonkar, Sachan 2026. arXiv:2605.12748 (preprint)
68. Sonkar S et al. 2024. MalAlgoPy. arXiv:2410.12294
69. Yang et al. 2026. StudentSim. arXiv:2609.01591 (preprint)
70. Scarlatos A, Lee, Woodhead, Lan 2026. arXiv:2601.04025
71. Bisbee J et al. 2024. Political Analysis. doi:10.1017/pan.2024.5
72. Cui Z, Li N, Zhou H 2025. Nat Comput Sci. doi:10.1038/s43588-025-00840-7
73. Park JS et al. 2024/2026. arXiv:2411.10109
74. Park, Jeon et al. 2025. Int J Surgery. doi:10.1097/JS9.0000000000003631
75. Xiao et al. 2026. Persona collapse. arXiv:2604.24698 (preprint)
76. Choi et al. 2025. NeurIPS. arXiv:2508.17536
77. Schoenegger P et al. 2024. Science Advances. doi:10.1126/sciadv.adp1528
78. Shao Y et al. 2024. STORM. arXiv:2402.14207
79. Messeri L, Crockett MJ 2024. Nature. doi:10.1038/s41586-024-07146-0
80. Kadir 2026. RankCert. arXiv:2609.26069 (preprint)
81. Krishnan, Savelka 2026. arXiv:2605.16290 (preprint)
82. Ashokkumar A et al. 2026. Nature. doi:10.1038/s41586-026-10742-x
83. Morris TP, White IR, Crowther MJ 2019. Stat Med. doi:10.1002/sim.8086
84. Markel JM et al. 2023. GPTeach. L@S. doi:10.1145/3573051.3593393
85. Benedetto L et al. 2024. Findings of EMNLP. https://aclanthology.org/2024.findings-emnlp.663/
86. Koedinger KR, Corbett AT, Perfetti C 2012. Cognitive Science (KLI). doi:10.1111/j.1551-6709.2012.01245.x
87. Mislevy RJ, Steinberg LS, Almond RG 2003. Measurement. doi:10.1207/s15366359mea0101_02; Mislevy RJ, Riconscente MM 2005. https://padi.sri.com/downloads/aera/2005/symposium2/papers/MislevyRicLayers.pdf
88. van Merriënboer JJG, Clark RE, de Croock MBM 2002. ETR&D. doi:10.1007/bf02504993
89. Mitrovic A 2012. UMUAI. doi:10.1007/s11257-011-9105-9; Ohlsson S 1994. doi:10.1007/978-3-662-03037-0_7
90. Brown JS, Burton RR 1978. Cognitive Science. doi:10.1016/s0364-0213(78)80004-4
91. Doignon J-P, Falmagne J-C 1985. IJMMS. doi:10.1016/s0020-7373(85)80031-6; Heller J et al. 2015. Psychometrika. doi:10.1007/s11336-015-9457-x
92. de la Torre J 2011. Psychometrika. doi:10.1007/s11336-011-9207-7
93. Schreiber G et al. 1994. IEEE Expert (CommonKADS). doi:10.1109/64.363263
94. Miles A, Bechhofer S 2009. SKOS Reference. https://www.w3.org/TR/skos-reference/
95. W3C 2013. PROV-O. https://www.w3.org/TR/prov-o/
96. Groth P, Gibson A, Velterop J 2010. Information Services & Use. doi:10.3233/ISU-2010-0613
97. Clark T, Ciccarese PN, Goble CA 2014. J Biomed Semantics. doi:10.1186/2041-1480-5-28
98. Dung PM 1995. Artificial Intelligence. doi:10.1016/0004-3702(94)00041-x
99. Guyatt GH et al. 2008. BMJ (GRADE). doi:10.1136/bmj.39489.470347.ad
100. Hogan A et al. 2021. ACM Computing Surveys. doi:10.1145/3447772
101. Cen H, Koedinger K, Junker B 2006. LFA. doi:10.1007/11774303_17
102. Liu R, Koedinger KR 2017. JEDM. https://jedm.educationaldatamining.org/index.php/JEDM/article/view/212
103. Koedinger KR, McLaughlin EA, Stamper JC 2012. EDM. ERIC ED537201. https://files.eric.ed.gov/fulltext/ED537201.pdf
104. Wei, Carvalho, Stamper 2025. KCluster. EDM 2025. arXiv:2505.06469 (fit metrics not read)
105. Smith JP, diSessa AA, Roschelle J 1994. JLS. doi:10.1207/s15327809jls0302_1
106. Hall EP, Gott SP, Pokorny RA 1995. PARI. AFHRL report. doi:10.21236/ada303654
107. Shaffer DW, Collier W, Ruis AR 2016. JLA. doi:10.18608/jla.2016.33.3
108. Hestenes D, Wells M, Swackhamer G 1992. Phys Teach 30:141. doi:10.1119/1.2343497
109. Avelino G, Passos L, Hora A, Valente MT 2016. ICPC. doi:10.1109/icpc.2016.7503718; arXiv:1604.06766
110. Rigby PC, Zhu YC, Donadelli SM, Mockus A 2016. ICSE. doi:10.1145/2884781.2884851
111. Nassif M, Robillard MP 2017. ICSME. doi:10.1109/icsme.2017.64
112. Avelino G, Constantinou E, Valente MT, Serebrenik A 2019. arXiv:1906.08058
113. Robillard MP 2021. ESEC/FSE. doi:10.1145/3468264.3473923
114. Jabrayilzade E et al. 2022. ICSE-SEIP. doi:10.1109/icse-seip55303.2022.9793985
115. Wheeler 2026. The Substrate Collapse. arXiv:2606.20882 (single-author position paper)
116. Aghajani E et al. 2019. ICSE. doi:10.1109/icse.2019.00122
117. Szulanski G 1996. Strategic Mgmt J. doi:10.1002/smj.4250171105
118. Wegner DM 1987. Transactive memory. doi:10.1007/978-1-4612-4634-3_9
119. Hansen MT, Nohria N, Tierney T 1999. HBR. https://hbr.org/1999/03/whats-your-strategy-for-managing-knowledge
120. Connelly CE et al. 2012. J Org Behav. doi:10.1002/job.737
121. TVA nuclear knowledge retention (OSTI/ETDEWEB). https://www.osti.gov/etdeweb/biblio/20842949 (summary from search; the 35% figure unverified); IAEA 2017, Knowledge Loss Risk Management in Nuclear Organizations, Nuclear Energy Series NG-T-6.11. https://www.iaea.org/publications/10921/knowledge-loss-risk-management-in-nuclear-organizations
122. Brundage MP et al. 2021. Manufacturing Letters. doi:10.1016/j.mfglet.2020.11.001
123. Bikaun T et al. 2024. MaintIE. doi:10.63317/3cuvz8qfmako; MaintNet. arXiv:2005.12443; NIST nestor datasets (excavator work orders). https://pages.nist.gov/nestor/nestor/datasets/
124. van der Aalst W 2016. Process Mining. doi:10.1007/978-3-662-49851-4
125. Microsoft Learn. Changes coming to Topics. https://learn.microsoft.com/en-us/microsoft-365/topics/changes-coming-to-topics?view=o365-worldwide
126. Cognition 2025. DeepWiki. https://cognition.com/blog/deepwiki (grey)
127. Glean press releases. https://www.glean.com/press/glean-surpasses-200m-in-arr-for-enterprise-ai-doubling-revenue-in-nine-months; https://www.glean.com/press/glean-raises-150m-series-f-at-7-2b-valuation-to-accelerate-enterprise-ai-agent-innovation-globally; (grey)
128. Fortune via Yahoo Finance, 23 Mar 2026 (Interloom). https://finance.yahoo.com/sectors/technology/articles/exclusive-interloom-startup-capturing-tacit-070000121.html (grey)
129. EU AI Act Annex III. https://artificialintelligenceact.eu/annex/3/; Article 6. https://artificialintelligenceact.eu/article/6/; Regulation (EU) 2024/1689. https://eur-lex.europa.eu/eli/reg/2024/1689/oj (not fetched)
130. CSA Labs research note on the Digital Omnibus. https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/; Gibson Dunn. https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/ (secondary; regulation number unverified)
131. Orrick 2024. AI and German Co-Determination. https://www.orrick.com/en/Insights/2024/09/AI-and-German-Co-Determination-What-Employers-Need-to-Know (secondary)
132. Directive (EU) 2019/790. https://eur-lex.europa.eu/eli/dir/2019/790/oj/eng; Kluwer Copyright Blog. https://legalblogs.wolterskluwer.com/copyright-blog/the-new-copyright-directive-text-and-data-mining-articles-3-and-4/ (secondary)
133. Greshake K et al. 2023. AISec. doi:10.1145/3605764.3623985; arXiv:2302.12173
134. Brynjolfsson E, Li D, Raymond L 2025. QJE. doi:10.1093/qje/qjae044 (15% average; the novice figure was not accessible)
135. del Rio-Chanona RM et al. 2024. PNAS Nexus. doi:10.1093/pnasnexus/pgae400
136. Steinmacher I et al. 2015. IST. doi:10.1016/j.infsof.2014.11.001
137. Eedi Misconception Graph via Learning Commons. https://learningcommons.org/news/ai-platform-launch/; Eedi news. https://www.eedi.com/news/from-wrong-answers-to-real-insights-how-we-used-a-kaggle-challenge-to-map-student-misconceptions
138. Wang Z et al. 2020. NeurIPS Education Challenge. arXiv:2007.12061; results arXiv:2104.04034 (licence unverified)
139. AAAS Project 2061 assessment. https://www.aaas.org/news/new-testing-feature-aaas-web-site-helps-teachers-find-gaps-students-science-knowledge; mirror http://assess.bscs.org/science/pages/about (licence unverified)
140. PSLC DataShop. https://pslcdatashop.web.cmu.edu/; Stamper J, Koedinger KR 2011. doi:10.1007/978-3-642-21869-9_46 (terms unverified)
141. Yaneva V et al. 2024. BEA 2024 shared task findings. https://aclanthology.org/2024.bea-1.39/
142. O*NET database licence (CC BY 4.0). https://www.onetcenter.org/license_db.html
143. Guest G, Bunce A, Johnson L 2006. Field Methods. doi:10.1177/1525822X05279903; Guest G, Namey E, Chen M 2020. PLOS ONE. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7200005/
144. Chao A 1984 (OpenAlex W1558982506); Chao A 1987. Biometrics. doi:10.2307/2531532; Chao A, Jost L 2012. Ecology. doi:10.1890/11-1952.1
145. Eick SG et al. 1992. ICSE. doi:10.1145/143062.143090; Briand LC et al. 2000. IEEE TSE. doi:10.1109/32.852741
146. Barker 2023. arXiv:2301.04760
147. Lindley DV 1956. doi:10.1214/aoms/1177728069; Rainforth T et al. 2024. Stat Sci. doi:10.1214/23-STS915
148. Choudhury et al. 2025. BED-LLM. arXiv:2508.21184; Handa K et al. 2024. OPEN. arXiv:2403.05534; Piriyakulkij T, Kuleshov V, Ellis K 2023. arXiv:2312.12009
149. Lakkaraju H, Kamar E, Caruana R, Horvitz E 2017. AAAI. doi:10.1609/aaai.v31i1.10821
150. Kuhn L, Gal Y, Farquhar S 2023. Semantic entropy. arXiv:2302.09664
151. Golchin S, Surdeanu M 2023. arXiv:2308.08493; Sainz O et al. 2023. doi:10.18653/v1/2023.findings-emnlp.722
152. Panickssery A, Bowman SR, Feng S 2024. arXiv:2404.13076; Verga P et al. 2024. PoLL. arXiv:2404.18796
153. Kapoor S et al. 2024. arXiv:2407.01502
154. Linde P et al. 2026. npj Digital Medicine. GPT-4o versus human items. doi:10.1038/s41746-025-02313-7
155. Küchemann S et al. 2024. Front Psychol. doi:10.3389/fpsyg.2024.1426209
156. Li BZ, Tamkin A, Goodman N, Andreas J 2023. GATE. arXiv:2310.11589
157. Tran V-T et al. 2017. J Clin Epidemiol. doi:10.1016/j.jclinepi.2016.10.001
158. Gervasi V et al. 2013. doi:10.1007/978-3-642-34419-0_2; Zowghi D, Coulin C 2005. doi:10.1007/3-540-28244-0_2
159. Colson AR, Cooke RM 2017. Reliab Eng Syst Saf. doi:10.1016/j.ress.2017.02.003
160. Prelec D, Seung HS, McCoy J 2017. Nature. doi:10.1038/nature21054; Prelec D 2004. Science. doi:10.1126/science.1102081
161. Shulman LS 1986. Educ Researcher. doi:10.3102/0013189x015002004; Loughran J, Mulhall P, Berry A 2004. JRST. doi:10.1002/tea.20007
162. Koedinger KR et al. 2013. AI Magazine. doi:10.1609/aimag.v34i3.2484
163. NCCA Standards (Institute for Credentialing Excellence), draft 2021 revision. https://www.credentialingexcellence.org/Portals/0/NCCA%20Standards%202021%20DRAFT%20REVISIONS_Sept%202021.pdf
164. ten Cate O 2005. Med Educ. doi:10.1111/j.1365-2929.2005.02341.x
165. Weir S, Kim J, Gajos KZ, Miller RC 2015. CSCW. doi:10.1145/2675133.2675219
166. Bastani H et al. 2025. PNAS. doi:10.1073/pnas.2422633122
167. Kestin G et al. 2025. Sci Rep. doi:10.1038/s41598-025-97652-6
168. Tricot A, Sweller J 2014. Educ Psych Rev. doi:10.1007/s10648-013-9243-1
169. Murray T 2003. ITS authoring tools. doi:10.1007/978-94-017-0819-7_17
170. Doshi AR, Hauser OP 2024. Sci Adv. doi:10.1126/sciadv.adn5290; Kleinberg J, Raghavan M 2021. PNAS. doi:10.1073/pnas.2018340118
171. Gierl MJ, Lai H, Turner SR 2012. Med Educ. doi:10.1111/j.1365-2923.2012.04289.x
172. Burge JE et al. 2008. Rationale-Based Software Engineering. doi:10.1007/978-3-540-77583-6
173. Sharma M et al. 2023. Sycophancy. arXiv:2310.13548
174. Beilock SL, Carr TH, MacMahon C, Starkes JL 2002. JEP: Applied 8(1):6. doi:10.1037/1076-898X.8.1.6
175. Hu Z et al. 2024. Uncertainty of Thoughts. arXiv:2402.03271
176. Collins HM 2001. Tacit knowledge, trust and the Q of sapphire. Social Studies of Science 31(1):71–85. doi:10.1177/030631201031001004 (content not re-read)
177. Löwenmark et al. 2022. PHM Society European Conference. doi:10.36001/phme.2022.v7i1.3356 (source of the 5,485 work-order count)

---

## Final test

1. **What is this project actually trying to discover?** Whether a machine can reconstruct what is written about a domain *and predict where that reconstruction is missing important human knowledge*, so that expensive human elicitation targets only the human knowledge residual. Physics was the first setting, not the question.
2. **What is the smallest useful product/research primitive?** Residual accounting: a provenance-typed claim model plus a calibrated gap map. Per area it gives evidence status, knowledge type and P(important knowledge missing), and it emits a ranked list of residual questions chosen by expected information gain.
3. **What can we build and scientifically test TODAY with no participants?**
   - The claim record, labels and gates.
   - A gated reconstruction pipeline.
   - E-CTA against published CTA gold, with dated-corpus contamination controls and ΔAUROC against the strongest baseline.
   - E-OSS on public repository departures.
   - E-MISC, E-DIST and E-KC on Eedi, AAAS and DataShop.
   - E-PLANT, E-ABST, E-EIG against held-out gold oracles.
   - Synthetic-learner tiers T1–T3.
   - Sealed Track A predictions.
   - The cost ledger.

   The one human input is a blind second coder — labelling, not participation — subject to the owner's confirmation.
4. **What do we genuinely need experts for?**
   - Validating residual items.
   - Episode-specific cues and expectancies.
   - Automated procedures (via traces and observation).
   - Perceptual discriminations (via contrasting cases).
   - Collective norms.
   - Importance weights with no behavioural proxy.

   Experts are not needed to test whether the gap map works; published human-revealed gold does that.
5. **What do we genuinely need learners for?** Prevalence in a real cohort, individual state ("what this person knows", "what next"), and instructional effects and transfer. Mis-modelled difficulty is a fact about learners; public response data answer it only at cohort grain.
6. **What does proprietary organisational data add?** Work-as-done: traces, logs, tickets, reviews and work orders, which carry cue→decision policy and doc-versus-practice divergence that public text lacks [27][19]. It also adds the long-tail, organisation-specific knowledge that is absent from public corpora by construction [56], and the concentration and outcome data needed to weight criticality.
7. **Which current repository components are premature?**
   - Stage A and Stage B execution.
   - Early K0 fielding.
   - The pilot.
   - The session instrument (tablet, microphone, transcription, console).
   - Freeze and pre-registration instances.
   - `/elicit`, `/preflight`, `/session-report`.

   All are frozen as Validation Track A, not retired.
8. **What would falsify the central hypothesis?**
   - On the pre-registered primary gold, the upper 90% bound of ΔAUROC — the gap map against the **strongest** pre-specified baseline (random, the naive type rule, confidence, area size, retrieval density, term frequency, a plain-LLM prompt, a cross-gold type prior) — falls below the smallest effect of interest δ (E-CTA, E-OSS), **regardless of recall**.
   - **Or** the residual cannot be measured: the text-based unseen-item estimate misses the gold-as-occasion count by more than the pre-registered tolerance.

   Then the project becomes an elicitation-efficiency tool: World C first, traces over text. Results between the stop and continue rules are inconclusive and trigger one fallback gold. Recall only decides whether reconstruction survives as a draft for experts to correct. Track A is unaffected either way.
9. **What is potentially novel here versus already solved elsewhere?**
   - **Already exists:** deep research, GraphRAG, codebase wikis, enterprise search, LLM item generation, simulated students, truck factor and KaR, CTA, capture–recapture.
   - **Not found in the notes' searches** (not proven absent):
     - a test of LLM public-text reconstruction against a CTA gold standard;
     - a product or study computing artefact coverage versus expert-only knowledge;
     - EIG question selection applied to expert or CTA interviews;
     - a validated predictor of where the human residual lies.
   - "Human knowledge residual" was not found as an established term, but it has close analogues: CTA omission rates, saturation, capture–recapture, Knowledge-at-Risk and knowledge-loss risk assessment.
10. **If this becomes a company/product, what is the defensible core capability?** A residual predictor validated per domain and knowledge type, plus targeted elicitation protocols, over a provenance-typed expertise model. Behind it sits the accumulating cross-domain corpus of residuals — what humans added that artefacts never contained — which competitors cannot scrape. Search, generated wikis and item generation are commodities.
