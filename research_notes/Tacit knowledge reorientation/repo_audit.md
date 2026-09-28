# Repository audit for the tacit-knowledge reorientation

**Scope.** Read-only audit of the 147 tracked files in `/Users/adamkrysztopa/projects/edu_proj` at `fbc104e` (2026-09-28), plus the git history (47 commits, 2026-09-25 to 2026-09-28). Not read: any `.env`, `sessions/`, `instrument/sessions/`, `research/pdf/`. Large generated or executed files (`instrument/uv.lock`, `docs/superpowers/plans/*.md`, `instrument/calibration/items.csv`) were skimmed, not read line by line.

**Bottom line.** The repository has two layers of very different value for the new direction. The **intellectual layer** is largely domain-agnostic and usable with zero participants: 13 graded literature syntheses, a nine-type taxonomy of hidden expert knowledge, a provenance-like status scheme for elicited operations (performed / reported only / contradicted), and a strict validity discipline (pre-registration, computed gates, blind coding, decoys, citation verification, lessons loop). The **operational layer** is a physics-specific, participant-bound study: 12 physicists, about 370 first-year students, a course offering, a tablet with a microphone, and a transcription pipeline. Every open milestone (M1–M8) now waits on people. The code also contains a small surrogate expert (`probe_app/simulate.py`). It was built only as a test double, and a registered rule forbids its output from ever counting as data.

---

## 1. Original motivation as stated in the repo

The earliest framing is in the first commit, `7aee199` ("Baseline research map and Claude Code research tooling", 2026-09-25), in `ai_education_research_map.md`:

> **Project context:** an AI-supported educational system, initially relevant to university-level physics/STEM but intended to remain transferable across disciplines and potentially compatible with commercial learning-content partners.

> **How can an AI-supported learning system discover what experts fail to explain because it has become tacit or automatic, diagnose what a learner is actually missing, and turn that gap into effective instruction?**

The same commit split this into three layers: "Expert elicitation: what does the expert know/do that they no longer verbalize? · Learner diagnosis · Instructional response". It stated the working hypothesis as "hidden expert knowledge → explicit mental operations → learner bottleneck diagnosis → targeted modelling/practice/feedback → learner-state update → adaptation … the main hypothesis to test, not an assumption to preserve."

In the §5.1 DtD card of the first commit, the tacit-omission motive is explicit: "experts often do not know what they are failing to say because the reasoning has become automatic." The same card named the AI opportunity: AI as "a **structured interviewer of experts**, repeatedly asking for cues, intermediate judgments, counterfactuals, hidden prerequisites and 'what would a novice miss here?'", then turning interviews into "candidate mental operations for human validation."

The Phase 1 deliverable of the first commit is the hidden-knowledge taxonomy that still underlies the codebook: omitted prerequisite; perceptual cue; representation choice; decomposition strategy; decision criterion; conceptual model; error-checking routine; metacognitive judgment; disciplinary norm / epistemic standard. Its kill criterion: "if bottlenecks are explained mostly by ordinary prerequisite knowledge or practice quantity, do not over-engineer expert elicitation."

The first commit's closing recommendation: "The first prototype should be a **research instrument for expert elicitation and learner diagnosis**, not yet a complete tutoring platform."

From the start, the framing was education-only and learner-facing. Organisational or company knowledge appears nowhere. The only non-education hint is "commercial learning-content partners" (map line 6). The map's §7 "Medicine / professional judgment" notes CTA's "exceptional relevance because experts use tacit cues and decisions."

The current `CLAUDE.md` restates the motive as: "Research on how AI can elicit hidden expert knowledge, diagnose learner bottlenecks, and turn those gaps into effective instruction. Physics is the initial setting; transfer across disciplines remains part of the question."

---

## 2. Research questions, assumptions, architecture, milestones, experiments, status

### 2.1 Research questions (map §10, unchanged since `7aee199`)

- **RQ1 Expert elicitation:** Can an AI interviewer recover tacit expert mental operations that are absent from ordinary lectures, textbooks and expert self-explanations?
- **RQ2 Validity:** Are the recovered operations reproducible across multiple experts and observable in actual expert task performance?
- **RQ3 Learner diagnosis:** Can AI distinguish missing knowledge, misconception, representation error, procedural error and metacognitive failure?
- **RQ4 Instructional causality:** Does teaching the decoded operation improve transfer, or merely performance on the original problem?
- **RQ5 Personalization:** Does an explicit learner model outperform an LLM that adapts only from conversational context?
- **RQ6 Cross-disciplinary generalization:** Which parts of the pipeline are domain-general and which require discipline-specific models/instruments?
- **RQ7 Teacher augmentation:** Does the system improve teachers' own PCK by exposing recurrent learner bottlenecks?
- **RQ8 AI role separation:** Should expert interviewer, learner diagnostician, tutor and evaluator be separate agents/models/policies?

Research phases (map §9): Phase 1 validate the premise; Phase 2 elicitation experiment (ordinary explanation vs human-led vs AI-led DtD/CTA vs think-aloud); Phase 3 learner-bottleneck diagnosis comparison; Phase 4 intervention experiment with transfer primary; Phase 5 adaptive system. All five are unchecked in `PROGRESS.md`.

### 2.2 Assumptions register (`research/roadmap.md`, "Assumptions register")

| # | Assumption | Tested at | If it fails |
|---|---|---|---|
| A1 | At least 30% of first errors on the registered K0 items are principle selection or representation | M1 (early K0); pretest K0 in M6 | Stage B stops; next module targets prerequisites/practice |
| A2 | AI retrospective probes are no worse than a trained human's on the contradicted rate | M4 (K1(c)) | Stage B does not run; a human-led design needs new pre-registration |
| A3 | At least 3 of the 12 experts share operations that the trace corroborates and ordinary materials omit | M4 (K1(a)) | Stage B does not run |
| A4 | Operations can be taught as structured, checkable steps with pre-authored feedback | M3 | Free-response prompts coded offline |
| A5 | A cohort-level diagnosis suffices for the first version | M1 (form agreement) | Test per-student routing |
| A6 | Static, expert-checked feedback teaches as well as live generation | M8 | Add live generation where it wins |
| A7 | A simple mastery rule stops practice about where knowledge tracing would | M7 | Randomize stopping rules |
| A8 | Worked examples first suit novices on this material | Later powered experiment | Switch default order |
| A9 | Teaching the operations improves delayed transfer by at least the SESOI | M6 (K2) | Stop this use for this topic |
| A10 | LLM-assisted coding matches the adjudicated human codes | M1 | Human coding only |

All ten require human data. None is testable with zero participants as written.

### 2.3 Architecture

- **Conceptual (map §6, "hypothesis to test"):** Domain/curriculum → Expert elicitation (DtD + CTA) → Expert reasoning model (operations, cues, representations, traps) → Learner diagnosis (PCK layer from student data + dialogue + assessment + KT) → Pedagogical decision → AI tutor interaction (constrained generation) → Assess + update → repeat.
  - Principle: "The LLM should probably be an interface/reasoning component, not the database of truth, the student model, the pedagogy model and the evaluator simultaneously." The map rates this principle as supported only indirectly.
- **First-version route (`research/roadmap.md` step 3–5):** "Student errors locate the bottleneck. Trace-based expert elicitation recovers the operations behind it. Those operations are taught through a static module … LLMs work behind the scenes … They do not face learners."
  - Delivery separates a domain model (problems, steps, operations, error categories), a learner record, and a policy (fixed sequence + three-in-a-row mastery rule).
- **Instrument (`instrument/`, built):** a FastAPI app served from a laptop, with a researcher console on loopback and an expert tablet page over HTTPS.
  - `Session` state machine (`probe_app/session.py`, 562 lines) with append-only `events.jsonl` on one monotonic clock.
  - AI arm: `ProbeEngine` (`engine.py`). Each turn is one stateless structured call (`llm.py`), then a deterministic turn contract (`contract.py`), then an LLM leading-question guard; one regeneration, then fallback to the bare stem.
  - Transcription through ElevenLabs Scribe v2 / OpenAI whisper (`transcribe.py`).
  - `FrozenConfig` hashes checked against `prereg.json` (`config.py`).
  - Coding CLI `probe-code` for blind exports, corroboration with decoys, α/κ, guard audit, calibration, freeze baseline and K0.
  - Model choice lives only in `instrument/models.json`: interviewer `claude-opus-5` (effort medium), guard `claude-haiku-4-5` (temperature 0), simulated expert `claude-sonnet-5` (effort low), transcriber `scribe_v2`.

### 2.4 Milestones and gates (`research/roadmap.md` step 6)

| Milestone | Content | Gate / decision | Needs |
|---|---|---|---|
| **M1** Bottleneck check (early K0) | 2 registered K0 items + component items + parallel Form 2; two coders; LLM coding secondary | **K0**: stop before recruiting experts if <30% of first errors are principle selection/representation; decisive only with ≥100 errored solutions; κ ≥ 0.70 | Course offering, ethics, 2 coders |
| **M2** Elicitation tool and pilot | Freeze hardening, codebook, HTTPS, backup, leading rule in both arms | `/preflight pilot` GO; 1–2 physicists; only a safety failure (an AI turn reaching the expert without contract and guard) removes the AI arm | Pilot physicists |
| **M3** Module v0 | Module format and validator, static player, logging, mastery rule; matched ordinary version | Physicist check; 5–8 students' think-aloud; ±10% word match | Students |
| **M4** Stage A | Freeze, pre-register, 12 experts | **K1**: (a) ≥3 performed, shared (≥3/12 experts) operations absent from ordinary material; (b) ≥2 of them AI-probe-added; (c) upper 95% CI of AI-minus-human contradicted rate ≤15 pp. If (a) or (c) fails, RQ1 is negative and Stage B does not run. If only (b) fails, Stage B tests "trace-based CTA" | 12 physicists, human interviewer, coders |
| **M5** Feasibility run | Both versions in one section | ≥70% compliance/arm; time within 10%; delayed test runs | Own course offering |
| **M6** Stage B | Two-arm RCT, ~370 students, delayed transfer 2–3 weeks | Pretest **K0** first, then **K2**: with ≥70% compliance per arm, kill if the upper 90% ITT CI < d = 0.30 (futility); inconclusive zone d ≈ 0.12–0.21 → one replication | ~370 first-year students |
| **M7** Offline learner-model check | KT vs three-in-a-row on logs | Disagreement threshold (project choice) | M5/M6 logs |
| **M8** Live generation arm | Static vs live LLM feedback | Keep generation only if it beats static by ≥ SESOI | After K2 passes |

### 2.5 Experiments (`research/experiment-ai-assisted-cta-physics.md`)

- **Early K0:** the same 2 items as a quiz in an earlier offering, registered before the quiz (`instrument/k0/prereg-early-k0.md`, draft with *to confirm* fields).
- **Pilot:** 1–2 physicists, about 75 minutes each, following `instrument/pilot-protocol.md`: ordinary explanation (paper) → think-aloud on tablet → trace review → AI probes on one set, human probes on the other → debrief. It builds codebook v0 and never counts as data.
- **Stage A:** 12 physicists, within-expert, with 4 counterbalanced sequences × 3 experts and a 20-minute cap per set.
  - Operations are coded blind to interviewer.
  - "Absent" is judged against the expert's explanations plus the textbook and lecture notes.
  - A published-framework tag (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015) marks operations that are already published.
  - Saturation is checked (Hennink & Kaiser 2022; Guest et al. 2020), with an extension to 16 experts.
- **Stage B:** individually randomized, both arms static worked examples with matched self-explanation prompts and locked answers. The control uses experts' ordinary explanations; the treatment adds the validated operations. SESOI d = 0.30, ≈183 per arm.
- `methods-critic` reviewed the design four times. It found no fatal flaw; all majors were fixed.

### 2.6 Completed vs planned

**Completed, all with zero participant data:**
- 13 branch notes (`research/explore-*.md`, `research/falsify-decoding-the-disciplines.md`), `route-comparison.md`, `decision-gaps.md`, `roadmap.md`, the experiment design and its four reviews.
- `probe-app` and `probe-code`: `CLAUDE.md` reports 306 tests; 256 `def test_` functions are defined.
- The M1 kit (`instrument/k0/`).
- The M2 build: HTTPS verified in Playwright, freeze covering model-facing code, codebook v0, encrypted backup, loopback-only console.
- 3 current-configuration simulated sessions and the freeze baseline (`docs/freeze-baseline.md`, rule outcome "accept").
- Guard-calibration items (60), with the protocol in `docs/guard-calibration.md`. The items are **not yet labelled**.
- Stage A pre-registration additions (`docs/stage-a-prereg-additions.md`).
- Five architecture decisions: 0001, 0002, 0004 and 0005 active; 0003 proposed.
- Four lesson drains, 24 archived rules (L1.1–L4.3), plus one open queue entry.

**Not done:** any pilot; early-K0 registration; guard labelling; `probe-app freeze`; `instrument/prereg.json` (does not exist); the recording-module extraction (0003); any expert, student, course or proprietary data; Zotero seeding. `PROGRESS.md` line 17 states: "Everything that needs no participants is built; both now wait on people (course, ethics, physicists)."

---

## 3. Artefact inventory

### 3.1 Root and state files
- `CLAUDE.md`: project instructions: priority (M1/M2), Stage A/B and gates, off-limits paths, tests, agents, skills, definition of done.
- `PROGRESS.md`: step table 1–18, M1/M2 checklists, branch verdicts, open evidence gaps, infrastructure checklist.
- `ai_education_research_map.md` (1168 lines): single source of state. §1 question; §2 hypothesis; §3 decision tree; §4 graded priority map; §5.1–5.13 method cards; §6 architecture; §7 disciplines; §8 reading; §9 phases and prepared design; §10 RQs; §11 "What not to assume"; §12 evidence notes; §13 prompts; §14 about 200 source anchors with DOIs.
- `.mcp.json`: openalex (HTTP), zotero (local), playwright. `.gitignore`: secrets, sessions, PDFs, `*.pem`, arch-crew runtime.

### 3.2 Research notes (`research/`) and their main conclusions
- `falsify-decoding-the-disciplines.md`: **narrow**. DtD is kept as the frame (bottleneck → model → practice → assess). The decoding interview is dropped as the elicitation method in favour of CTA. Rating lowered to Low–moderate: no RCT, two small non-randomized comparisons, none in physics, no transfer. The decoding interview has never been compared with another method.
- `explore-cognitive-task-analysis.md`: rating kept Moderate–high, scoped to training outcomes outside physics.
  - CTA-based training g = 0.871 (Tofel-Grehl & Feldon 2013); surgery SMD 1.36/2.06 (Edwards et al. 2021); Feldon et al. (2010), N = 314, biology.
  - Experts omit about 71% of knowledge, 51% of action and 73% of decision steps when teaching (Sullivan et al. 2014, 3 experts). Prompted CTA raised coverage only from 44% to 66%.
  - Over 100 methods; CTA is "more craft than technology" (Yates & Feldon 2011).
  - Non-directed think-aloud is non-reactive; describe/explain prompts are reactive (Fox, Ericsson & Best 2011).
  - Price et al. (2021): 29 cross-disciplinary expert problem-solving decisions from 52 experts. Burkholder et al. (2020) built a physics template from them.
  - "No study was found that evaluates an LLM conducting CTA interviews."
- `explore-expert-novice.md`: kept High, scoped. The representation difference (principle vs surface) replicates but is a continuum (Mason & Singh 2011). Principle-first instruction helps immediately in small physics studies. One far-transfer RCT (Nokes-Malach et al. 2013); no delayed transfer.
- `explore-pedagogical-content-knowledge.md`: lowered to Moderate. PCK–achievement r = .13 n.s. to .23 (Fukaya et al. 2025). TAs and instructors miss common FCI difficulties (Maries & Singh), so difficulty knowledge is seeded from student data, not from experts.
- `explore-conceptual-change.md`: rating split.
  - High that intuitions persist alongside instruction; Moderate for interventions (refutation text g ≈ 0.41, holds at delay); theory contested (knowledge in pieces).
  - LLM misconception evidence is item- or population-level only (Smart, Bos & Bos 2024; Savage & Rebello 2025).
- `explore-concept-inventories.md`: High for cohort use, weak for individuals. 31% of FCI item answers change on retest; mixed models; gender-biased items; distractors miss ideas. EMCS drops Q16, Q22 and Q23.
- `explore-cognitive-apprenticeship.md`: Moderate. Components are supported (scaffolding g = 0.46); fixed-schedule fading is no better than none; explore-first vs model-first is split.
- `explore-worked-examples-self-explanation.md`: High for immediate outcomes (g ≈ 0.5), g ≈ 0.35 delayed; expertise reversal. Explanations handed to learners add little, so operations must be carried by self-explanation prompts.
- `explore-intelligent-tutoring-systems.md`: 0.73 SD on local tests vs 0.13 on standardized tests; ≈0–0.2 SD at scale. Andes physics is non-randomized. Supports step checking and an explicit policy; the separation principle is untested.
- `explore-knowledge-tracing.md`: Moderate–high for prediction only. Simple models match deep KT (Gervet et al. 2020). Public datasets are named: ASSISTments, Khan, DataShop Andes. No test against an N-in-a-row rule.
- `explore-threshold-concepts.md`: lowered to Low/contested. No reliability data for identifying threshold concepts.
- `explore-formative-assessment.md`: split. Feedback d = 0.48 (elaborated ≫ right/wrong), more than a third of effects negative; quizzing g = 0.50; packaged formative assessment d ≈ 0.2–0.3.
- `explore-llm-tutoring.md`: Emerging. Kestin et al. (2025) is large but immediate and bundled. With the AI removed at test, 0.1–0.4 SD or null. Harm without guardrails (Bastani et al. 2025); weak syntheses.
- `route-comparison.md`: the 13 families collapse to five independent choices (elicitation method; diagnosis source and grain; instructional carrier and feedback; delivery; learner model). Evidence weakens along the pipeline. The AI-specific roles are the least tested.
- `decision-gaps.md`: six targeted searches; nothing settled. Gap 2, the AI interviewer, collects the only AI-interviewing evidence (Chopra & Haaland; Wuttke et al.; Chan et al.). Defaults: static delivery, simple mastery rule, worked examples first.
- `roadmap.md`: route, a hypothetical worked physics case with the hidden-knowledge taxonomy, first-version scope, M1–M8, A1–A10.
- `experiment-ai-assisted-cta-physics.md`: the gated Stage A/B design (§2.5).
- `minimum-reading.md`: one-page orientation that points to the physics route.

### 3.3 Instrument (`instrument/`)
- `probe_app/`:
  - `session.py`: state machine for think-aloud, trace review and AI/human probe arms, including audio streams.
  - `server.py`: HTTP API, loopback-only console.
  - `engine.py`: generate → contract → guard → regenerate once → bare-stem fallback.
  - `llm.py`: interviewer and guard clients, structured output, full logging.
  - `backends.py`: Anthropic and OpenAI-compatible backends; `LLMRefused` vs `LLMUnavailable`.
  - `contract.py`: known stem, at most one follow-up, quoted span must occur in the expert's words, stem coverage.
  - `models.py`: Pydantic `InterviewerTurn`, `GuardVerdict`, `Segment`, `Anchor`, `DialogueTurn`.
  - `config.py`: `models.json` loading, `FrozenConfig` hashes, `check_preregistered`, `freeze`.
  - `storage.py`: append-only store with monotonic and wall clocks.
  - `trace.py`: segments and corrections.
  - `transcribe.py`: Scribe/whisper with retry.
  - `human.py`: human-arm turn attribution from I/E markers.
  - `simulate.py`: the surrogate expert (§8).
  - `backup.py`: openssl-encrypted, verified backup and restore.
  - `cli.py`: `serve`, `hashes`, `transcribe`, `freeze`, `simulate`, `backup`, `restore`.
- `probe_code/`:
  - `export.py`: blind unit export, trace export, leading export.
  - `corroboration.py`: corroboration sheet with decoys.
  - `agreement.py`: nominal α, Cohen κ, MASI α, per-code κ, decoy false rate, guess rate.
  - `guard_audit.py`: guard over both arms, config drift, leading rates.
  - `calibration.py`: guard sensitivity and specificity against human labels.
  - `baseline.py`: Wilson intervals, pooled metrics, computed freeze rule.
  - `k0.py`: registered K0 decision, sampling plan, κ, component share, form agreement, bootstrap κ.
  - `loader.py`: loads sessions and rejects simulated ones.
  - `cli.py`: subcommands for all of the above.
- `web/`: `console.html`, `console.js` (researcher console); `expert.html`, `expert.js` (tablet canvas and microphone streaming); `app.css`.
- `codebook/v0.md`: operation codebook (§7.3).
- `prompts/`: `interviewer_system.md`, `guard_system.md`, `stems.json` (§7.4).
- `problems/`: `problems.json` (A1–B2 conservation problems), `explanation-problems.md` (E_A/E_B), `simulated_think_aloud.json` (hand-written fixture transcript).
- `k0/`: `items.md` (Form 1, Form 2, components), `codebook-k0.md` (PM/SR/OT codes and sub-codes), `prereg-early-k0.md`.
- `calibration/items.csv`: 60 guard-calibration items. 30 are unaltered candidates from the simulated sessions' 172 generated questions; 30 are authored leading variants (15 explicit, 15 subtle).
- `pilot-protocol.md`, `human-script.md`, `consent-pilot.md`, `models.json`, `pyproject.toml`, `uv.lock`.
- `tests/`: 25 test modules plus `fakes.py` (the fakes "never refuse").

### 3.4 Docs
- `docs/architecture/decisions/`:
  - 0001: validity guarantees (frozen config refuses data sessions; AI turn passes contract and guard; no silent model substitution; full session log; blind coding material; **simulated sessions rejected**; session data outside the repo).
  - 0002: model choice in one file, two backends, uniform refusal mapping.
  - 0003 (proposed): extract audio recording.
  - 0004: freeze covers model-facing code; guard calibrated before freeze; freeze by computed rule; **rules, not agents, decide gates**.
  - 0005: console loopback-only, full uuid4.
- `docs/architecture/constitution.md` and `migration-report.md`: generated by arch-crew.
- `docs/agentic-review-`, `design-pattern-review-`, `security-review-`, `test-suite-review-2026-09-27.md`: four lens reviews of the instrument.
- `docs/freeze-baseline.md`, `docs/guard-calibration.md`, `docs/stage-a-prereg-additions.md`.
- `docs/superpowers/specs/` (2 specs) and `docs/superpowers/plans/` (2 executed plans, 170 KB and 39 KB).
- `docs/poc-explained.html`: offline visual brief of the physics PoC. Its "What we need" table lists physics collaborators, a course partner, coders, a microphone and ethics.
- `docs/lessons.md` (queue; one open entry on a route-surface test that filtered by type) and `docs/LESSONS-ARCHIVE.md` (drains 1–4).

### 3.5 Claude tooling and scripts
- **Agents:**
  - `citation-verifier`: resolves each claim–source pair and checks support, scope creep and qualifier drift.
  - `methods-critic`: adversarial review of study designs; ranked fatal/major/minor.
  - `validity-reviewer`: instrument validity threats.
  - `codebook-stress-tester`: applies the codebook to simulated exports; refuses non-simulated data.
- **Skills:**
  - `/branch explore|compare|falsify|experiment`: graded literature investigation with verification.
  - `/elicit`: an interactive DtD/CDM interview with a human expert "on one physics problem".
  - `/preflight`, `/session-report`: Stage A session gates and summaries.
  - `lessons`, `implement-ll`: capture and drain.
- **Hooks:**
  - `check-dois.py`: DOI must resolve to the cited work.
  - `guard-secrets.sh`, `guard-user-email.sh`, `guard-nested-repo.sh`.
  - `guard-frozen-prompts.sh`, `guard-session-data.sh`, `run-instrument-tests.sh`, `live-smoke-reminder.sh`.
  - `session_start_lessons.py`: injects the archive at session start.
- `scripts/lessons_graph.py`: detects oscillation, recurrence and dangling edges in the archive. `scripts/lessons_loop_tests/`: its fixtures and tests.
- **Defect found during the audit:** `.claude/settings.json` still invokes `.claude/hooks/check-dois.sh`, but commit `4e790e2` deleted that file and added `check-dois.py`. The DOI-verification hook (lesson L1.1's home) therefore probably never fires. This was not executed to confirm.

---

## 4. Where the project drifted

The whole repository was written in four days, so "drift" means a sequence of commits, not months.

1. **Physics and university level were chosen at the start, as a first case.** At `7aee199` the map already said "initially relevant to university-level physics/STEM". §7 declared physics the "best research environment for an initial prototype" for six reasons: expert–novice literature, structured problems, concept inventories, checkable intermediate states, ITS literature, LLM-tutoring trials. Phase 2 said "Take **one narrow physics topic**". The `/elicit` skill was written "on one physics problem". The `/branch` skill hard-codes physics in two modes ("compare … for eliciting hidden expert reasoning in university physics"; "experiment … one physics topic"). Every branch note consequently grades evidence by "outside physics / not university".
2. **Falsifying DtD pushed elicitation toward observed performance, and so toward recording.** `b678289` moved elicitation from the decoding interview to CTA. `ec0ca25` fixed the "provisional physics method": non-directed think-aloud while solving, then retrospective CDM probes over the recorded trace. Observed human performance became the validity anchor for RQ2 ("observable in actual expert task performance"). That is what later required audio, written-work capture and transcription.
3. **The experiment design fixed people, sample sizes and a single topic.** `6f228c2` (2026-09-25) is titled "gated two-stage design — AI-assisted CTA elicitation (12 experts) gating a transfer RCT (~370 students)". It introduced conservation principles, 12 physicists, about 370 first-year students and "written and diagram work captured on a tablet". A human-interviewer arm is intrinsic to K1(c).
4. **Microphone and tablet instrumentation.** `b7acea0` specified the session app. `3a4bcf2` added "HTTPS for tablet mic". `c17fe5d` (3,934-line plan) picked Scribe v2 transcription. `027bb9b` … `4e9b5ae` built the app in about 10 commits on 2026-09-26. Then came review fixes for audio loss (`9ce748a`, `737aa8e`), a security review and decisions 0003/0005 (`ce2bc6a`). Later work (`3010fa9` stream invariants, `fbc104e` loopback-only) continued to harden audio and network handling after the owner's scope correction.
5. **Peak narrowing of the project identity.** `CLAUDE.md` at `a84c4a0` opened with: "Research on eliciting the hidden reasoning of expert physicists and testing whether teaching it improves novice transfer (topic: selecting and combining conservation principles in first-year mechanics)." Its K0 line read "Waiting on exam data from the user."
6. **The first sign that participant data were not available.** `30a2b8e` ("K0 without exam scripts") rebuilt K0 because "no past exam scripts are available". The replacement moved the premise test onto a course quiz and a Stage B pretest, which also need a cohort.
7. **Owner correction, 2026-09-27, recorded at `4e790e2`.**
   - The map gained a "Scope alignment" note: "The conservation-topic experiment and its existing session app are preparation for one branch, not a replacement for the map. Literature reviews and working software do not establish the premise."
   - It also gained a "User clarification": "the immediate goal is to work out the approach and roadmap, then implement it".
   - Lesson L1.11: "A built instrument or designed study is preparation, not progress on a research phase". L1.12: "Choosing an evidence-informed route is separate from proving it works".
   - `CLAUDE.md` was re-broadened ("Physics is the initial setting").
   - The roadmap chosen in the same commit still routes through physics, courses and experts. M1 and M2 both need people, and `PROGRESS.md` now reads "both now wait on people".
8. **Why the narrowing happened (inferred from the texts):**
   - Physics maximised the available evidence and checkability (§7).
   - The falsification discipline demanded validation against observed human performance and against a human interviewer (§11: "Do not assume the LLM's reconstruction … is valid because it sounds plausible"; K1(c)).
   - The `/branch experiment` template asks for "the smallest defensible study … in one physics topic".
   - Validity rigour on the instrument (four reviews, five decisions, four lesson drains) generated work that could be done without people. Instrument-side artefacts (`instrument/`, the instrument docs, the plans) are roughly half the non-lockfile bytes of the repository.
   - Organisational knowledge, public-data-first reconstruction and surrogates never appear as design options. The simulator was built only to test the app.

---

## 5. Dependency map

**Needs expert participants (physicists):** Stage A, pilot, M4, K1; `instrument/pilot-protocol.md`, `human-script.md`, `consent-pilot.md`; `problems/explanation-problems.md` (physicist check); `/elicit`; `/preflight`; `/session-report`; `docs/stage-a-prereg-additions.md`; decision 0001's human-arm rules; the codebook's final (non-SIM) anchors; the M1 item physicist check.

**Needs a learner cohort or course:** early K0, pretest K0 and form agreement (`instrument/k0/*`, `probe_code/k0.py` inputs); M3 usability; M5; Stage B/M6, K2; M7 logs; M8; A1 and A4–A10; course lecture notes as the "absent" baseline.

**Needs microphone, tablet or audio:** `probe_app/session.py` audio streams, `transcribe.py`, `web/js/expert.js`, the HTTPS/mkcert setup, decisions 0003 and 0005, `docs/security-review-2026-09-27.md`, the `live-smoke-reminder` hook's transcriber part, and the audio invariant tests (`tests/test_streams.py`).

**Needs proprietary or institutional data:** past exam scripts (already abandoned, `30a2b8e`), the course pretest, the course textbook chapter and lecture notes (Stage A baseline), ethics approval.

**Needs non-participant humans (labellers or coders, not subjects):**
- guard calibration: two labellers who are not the author, the PI or a Stage A coder;
- two K0 coders;
- leading-content coders;
- a physicist item check.

**Domain-agnostic, usable with zero participants:**
- all literature notes and the map's §1–§4, §6, §11 and §12;
- the hidden-knowledge taxonomy;
- the codebook type table and status scheme;
- the interviewer turn contract, stems and leading rule (probing text or surrogates);
- `probe_code/agreement.py`, `baseline.py` (Wilson and computed-rule pattern), `calibration.py` (classifier vs human labels), `export.py` blinding logic, the `corroboration.py` decoy method;
- `llm.py`, `backends.py`, `engine.py`, `contract.py`, the `models.json` pattern, the `FrozenConfig` hashing;
- `simulate.py` (the surrogate harness);
- the lessons loop, hooks, `citation-verifier`, `methods-critic` (after de-physicsing), `/branch` (likewise), the OpenAlex/Zotero MCP setup.

---

## 6. Classification of every significant artefact

Legend: **KEEP** = central under the new direction; **REUSE** = useful component; **FREEZE** = valuable but needs humans; **RETIRE** = rests on an assumption no longer supported.

### State and planning
- `ai_education_research_map.md` — **KEEP**: the question, three layers, §11 and graded cards are the evidence base. §1/§7/§9 need reframing so that physics becomes one case and organisational knowledge is added.
- `CLAUDE.md` — **REUSE**: the off-limits, tests, agents and definition-of-done sections carry over. "Current priority and scope" and "Prepared experiment branch" must be rewritten.
- `PROGRESS.md` — **RETIRE**: every open row waits on a course, ethics or physicists.
- `research/roadmap.md` — **RETIRE** as the governing plan. Its route presumes cohort-first bottleneck data and experts. Salvage the step-4 taxonomy and "Candidate hidden-knowledge categories" (missing prerequisite / misconception / practice vs hidden operation).
- `research/experiment-ai-assisted-cta-physics.md` — **FREEZE**: a reviewed World C design (Stage A/B, K0/K1/K2), ready if experts and a cohort appear.
- `research/route-comparison.md` — **REUSE**: the five-choice decomposition and evidence gradient hold. The physics framing of the gaps does not.
- `research/decision-gaps.md` — **REUSE**: the gap-2 AI-interviewer evidence and gaps 3–5 are domain-general. Gap 1 is physics-specific.
- `research/minimum-reading.md` — **RETIRE**: it summarises the physics route. Rewrite for the new direction.
- `docs/poc-explained.html` — **RETIRE**: a visual brief of the physics PoC whose dependencies are people.

### Literature notes
- `explore-cognitive-task-analysis.md` — **KEEP**: the core evidence on elicitation, expert omission (≈70%), method craft, and the absence of LLM-CTA evidence.
- `falsify-decoding-the-disciplines.md` — **KEEP**: it defines what DtD contributes (bottleneck framing) and what it does not.
- `explore-expert-novice.md` — **KEEP**: the theory of what hidden knowledge looks like (representation, principle selection). Transferable to organisational experts.
- `explore-pedagogical-content-knowledge.md` — **KEEP**: "experts do not know what learners miss; seed from response data" is central for surrogate learners.
- `explore-conceptual-change.md` — **KEEP**: knowledge in pieces is a constraint on surrogate-learner validity. It holds the only LLM-vs-student-distribution evidence (Smart et al. 2024).
- `explore-concept-inventories.md` — **KEEP**: public, validated item banks and distractor data are World A evidence. Cohort-not-individual grain applies to surrogates.
- `explore-knowledge-tracing.md` — **REUSE**: it names public learner datasets (ASSISTments, DataShop). Learner-model evidence is for later.
- `explore-worked-examples-self-explanation.md`, `explore-cognitive-apprenticeship.md`, `explore-formative-assessment.md`, `explore-intelligent-tutoring-systems.md`, `explore-llm-tutoring.md` — **REUSE**: the instructional and delivery layer, needed when the residual is turned into instruction (World C). The §11-style cautions apply to surrogate evaluation.
- `explore-threshold-concepts.md` — **REUSE** (low priority): it documents why that construct is not operational.

### Instrument code
- `probe_app/simulate.py` — **KEEP** (rebuild): the only surrogate-expert harness. It currently role-plays "Dr. Lee" from an invented fixture and must become evidence-grounded, with provenance.
- `probe_app/engine.py`, `contract.py`, `llm.py`, `models.py` — **REUSE**: the generator + deterministic contract + LLM guard + bounded retry pattern suits probing surrogates and later humans.
- `probe_app/backends.py` — **REUSE**: provider-neutral, and the refusal/outage split matters for surrogate runs.
- `probe_app/config.py` (`FrozenConfig`, `freeze`) — **REUSE**: hash-based configuration freezing is provenance of generation settings.
- `probe_app/storage.py` — **REUSE**: an append-only event log with dual timestamps, a provenance substrate.
- `probe_app/session.py`, `server.py`, `human.py`, `trace.py`, `transcribe.py`, `backup.py`, `cli.py`; `instrument/web/*` — **FREEZE**: they serve live human sessions with audio and a tablet.
- `probe_code/agreement.py` — **KEEP**: α/κ/MASI, decoy false rate and guess rate are needed to compare surrogate output with sources and with human coders.
- `probe_code/calibration.py`, `baseline.py` — **REUSE**: calibrating an LLM classifier against human labels with CIs, and pre-stated computed decision rules.
- `probe_code/export.py`, `corroboration.py` — **REUSE**: blinding and decoy-mixed corroboration generalise to "is this claim grounded in the evidence".
- `probe_code/loader.py` — **REUSE (invert)**: it rejects simulated sessions. Under the new direction, surrogate data must be admitted with an explicit provenance label.
- `probe_code/guard_audit.py` — **FREEZE**: a human-arm audit.
- `probe_code/k0.py` — **FREEZE**: course-specific K0. Its `wilson`/`bootstrap_kappa` helpers are reusable.
- `instrument/tests/` — **REUSE** for the modules above; **FREEZE** for session, stream and server tests.

### Instrument content
- `instrument/codebook/v0.md` — **KEEP**: the operation representation, statuses, cross-expert matching and framework tag.
- `instrument/prompts/interviewer_system.md`, `stems.json`, `guard_system.md` — **REUSE**: domain-neutral apart from the words "physicist", "physics" and "first-year student". Frozen status does not bind them yet (no `prereg.json`).
- `instrument/calibration/items.csv` — **REUSE**: 60 leading-question items built from simulated sessions, a seed benchmark for a leading-probe detector. Unlabelled and physics-bound.
- `instrument/models.json` — **REUSE**: the single-file model-choice pattern. Update the roles for surrogates.
- `instrument/problems/problems.json`, `explanation-problems.md` — **FREEZE**: physics tasks for Stage A.
- `instrument/problems/simulated_think_aloud.json` — **RETIRE** as evidence, keep as a test fixture: an invented expert transcript with no source, the opposite of evidence-grounded.
- `instrument/k0/*` — **FREEZE**: World C premise check.
- `instrument/pilot-protocol.md`, `human-script.md`, `consent-pilot.md` — **FREEZE**: human sessions.

### Docs and decisions
- Decision 0001 — **FREEZE**, except `full-session-log` and `blind-coding-material`, which are **REUSE**. `simulated-sessions-rejected` is **RETIRE** under the new direction; replace it with "surrogate data labelled, never pooled with human data".
- Decision 0002 — **REUSE**: one model file, uniform refusal mapping.
- Decision 0003 — **FREEZE**: audio.
- Decision 0004 — **REUSE**: `rules-not-agents-decide` and `freeze-by-computed-rule` are central to autonomous reconstruction. Guard calibration is reusable.
- Decision 0005 — **FREEZE**: tablet network.
- `docs/architecture/constitution.md`, `migration-report.md` — **FREEZE** (generated from the decisions).
- `docs/freeze-baseline.md` — **FREEZE**: Stage A thresholds. Its "Limits" section is **REUSE** as evidence on surrogates.
- `docs/guard-calibration.md` — **REUSE**: a protocol for validating an LLM judge against human labels.
- `docs/stage-a-prereg-additions.md` — **FREEZE**.
- The four `docs/*-review-2026-09-27.md` — **FREEZE**: historical instrument reviews.
- `docs/superpowers/specs/*`, `plans/*` — **FREEZE**: executed build records.
- `docs/lessons.md`, `docs/LESSONS-ARCHIVE.md`, `scripts/lessons_graph.py`, `scripts/lessons_loop_tests/` — **KEEP**: a domain-agnostic process memory. About half the rules (L1.1, L1.11, L1.12, L2.1, L2.3, L3.1, L3.6, L4.1) carry over directly.

### Claude tooling
- `citation-verifier` — **KEEP**: provenance of every literature claim.
- `methods-critic` — **REUSE**: rewrite its checklist for zero-participant and surrogate designs (it treats human transfer outcomes as mandatory).
- `codebook-stress-tester` — **REUSE**: it already applies the codebook to simulated sessions, the closest existing tool to surrogate-cohort analysis.
- `validity-reviewer` — **FREEZE**: specific to the instrument.
- `/branch` — **REUSE**: strip the physics hard-coding in the compare and experiment modes.
- `/elicit` — **FREEZE**: a live human interview.
- `/preflight`, `/session-report` — **FREEZE**.
- `lessons`, `implement-ll`, `session_start_lessons.py` — **KEEP**.
- Hooks: `guard-secrets`, `guard-user-email`, `guard-nested-repo`, `check-dois.py` — **KEEP**; fix the `settings.json` path. `guard-frozen-prompts`, `guard-session-data`, `run-instrument-tests`, `live-smoke-reminder` — **FREEZE/REUSE** with the instrument. The live-smoke rule ("fakes never refuse") stays relevant to surrogate runs.
- `.mcp.json` — **KEEP**: OpenAlex and Zotero are the World A literature pipeline.

---

## 7. Reusable intellectual assets

### 7.1 Literature syntheses
The CTA, DtD, expert–novice, PCK, conceptual-change, concept-inventory and KT notes are graded, DOI-verified syntheses. Each has an Evidence table (Source | Design | N | Domain | Outcome | Finding), an Against section and Open questions. They remain valid and are about 290 KB of work. Items that bear directly on the new direction:
- **Expert omission:** Sullivan et al. (2014); CTA recovers only about two thirds of steps.
- **Cross-disciplinary expert decisions:** Price et al. (2021) found 29 decisions shared across science and engineering. This is a public, domain-general seed list, and a precedent that expert decision structures transfer across disciplines.
- **Published problem-solving frameworks** as a "not new" reference: Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015; the Docktor et al. 2016 rubric.
- **Experts misjudge learner difficulty:** Maries & Singh; `explore-pedagogical-content-knowledge.md`.
- **Public learner-response data:** concept inventories and PhysPort; ASSISTments, Khan and DataShop (Andes) in `explore-knowledge-tracing.md`; NAEP items in Smart et al. (2024).
- **Instructional carriers** for eventually teaching the residual: worked examples with prompted self-explanation; elaborated, error-keyed feedback.

### 7.2 Hidden-knowledge taxonomy and codebook codes (`instrument/codebook/v0.md`)
- **Nine types, multi-label per unit:** Omitted prerequisite · Perceptual cue · Representation choice · Decomposition strategy · Decision criterion · Conceptual model · Error-checking routine · Metacognitive judgment · Disciplinary norm / epistemic standard. Each has Definition, Include, Exclude and an example. The examples are marked (SIM) because they come from Sonnet role-play.
- **Operation statement form:** "in situation S, do A (because C)", with an `op_id` and source units. This is a ready representation for expert operations in any domain.
- **Source tags:** explanation · trace-only · AI probe · human probe.
- **Status tags:** trace-only · probe-added performed (corroborated by a blind third coder, with decoys) · reported only · contradicted. These are provenance and evidence-strength classes for a claim about expert cognition, and they map onto "grounded in evidence / asserted only / contradicted by evidence".
- **Cross-expert matching rule:** "the same if a novice taught either would perform the same action in the same situation", with κ. **Shared** = ≥3 of 12 experts.
- **Framework tag** (`published=yes`) and the **"absent from ordinary material"** judgment against explanations plus textbook plus lecture notes. Together these are a proto-definition of a **human knowledge residual**: an operation that is performed, shared, not in ordinary material and not in the published frameworks.
- **K0 learner-error codes** (`instrument/k0/codebook-k0.md`): PM.prereq, PM.math, SR.decompose, SR.criterion, SR.misconception, SR.representation, OT, BLANK, CORRECT. The roadmap's three "ordinary explanations" to rule out first are missing prerequisite (component also fails), misconception, and practice/execution. A difficulty is a "candidate hidden operation" only when components pass but the synthesis fails.

### 7.3 Interviewer turn contract and leading guard (`instrument/prompts/`, `contract.py`, `engine.py`)
- **Five stems:** cues, alternatives, checks, anomalies, novice_miss.
- **Rules:** one question per turn; anchored to specific transcript segments or written work; every stem used once per problem; at most one follow-up, which must quote the expert's exact words (checked in code); no evaluation, praise or explanation; `end_session` only after full coverage.
- **Guard rule:** "A question is leading if it names or implies a specific … principle, quantity, relation, representation, strategy or check that the expert has not said … Words that appear in the problem statements are not leading." The same rule is applied to the human interviewer and audited post hoc.
- **Pipeline:** generate, then contract, then guard, then one regeneration, then a bare-stem fallback; rejections are logged, never shown.
- **Reuse:** the design is directly reusable for probing surrogate experts without contaminating them with the interviewer's hypotheses. This is the key risk when a model interviews a model: the interviewer planting content the "expert" then echoes. It is also reusable for later human elicitation. Remove the physics nouns first.

### 7.4 Provenance and validity discipline
- Pre-registration before data; registered numbers held as constants checked against the registered text (L3.1, `tests/test_registered.py`).
- Computed gates: "rules, not agents, decide" (decision 0004). Thresholds marked *(project choice)* are set before the data they judge.
- Hash-freezing of everything that reaches a model (L1.9).
- Full request/response logging, because current models accept no temperature.
- Blind exports with keys held apart; decoy-based corroboration with a reported false-corroboration rate; arm-guess rate to measure residual unblinding.
- Classifier calibration against independent human labels with sensitivity and specificity CIs, sampled upstream of the classifier (L4.1).
- Citation verification of every claim, including qualifier drift (L2.1). The DOI must match the cited work (L1.1).
- The lessons loop with oscillation detection.
- The "simulated" flag on every session manifest.

### 7.5 Zero-participant work already planned
Almost none. Planned items without participants are all instrument hardening:
- 3–5 more simulated sessions before the pilot;
- the freeze baseline;
- the recording-module extraction.

M7 is offline, but it needs logs from M5/M6. No public-data analysis, no organisational-knowledge work and no surrogate-cohort study is planned anywhere.

---

## 8. Evidence in the repo bearing on the new direction's feasibility

### 8.1 On LLMs conducting CTA or interviews
- "No study was found that evaluates an LLM conducting CTA interviews against a human interviewer or against observed expert performance" (`explore-cognitive-task-analysis.md`; also map §5.2).
- **AI interviewers with lay respondents** (`decision-gaps.md` gap 2; experiment note):
  - Chopra & Haaland: about 95% of AI questions were rated open and non-leading, with richer answers than surveys; there was no human-interviewer arm.
  - Geiecke & Jaravel: high quality ratings.
  - Wuttke et al. (2025): the AI caused 88% of failures to follow up on surprising answers.
  - Chan et al. (2024, preprint): a generative chatbot produced more than three times as many false memories, persisting at one week. This is the suggestion risk that motivated the guard.
- The experiment note concludes: none of these "tests an AI interviewer against observed task performance, and none elicits expert problem-solving cognition."

### 8.2 On surrogate learners
- **Smart, Bos & Bos (2024), 388 NAEP items, grades 4/8/12:** LLMs found the same items difficult as students "to a statistically significant but small degree, varying by model". Under minimal prompts they often chose the same wrong answers as students, less so with chain-of-thought. GPT-4's explanations of popular wrong answers agreed with an experienced teacher's in 81% of cases. The repo rates this item- or population-level only: "No study was found that checks an LLM's misconception diagnosis for an individual student" (`explore-conceptual-change.md`).
- LLM grading matches humans on binary correctness: Chen & Wan (2025), 70–80% with a 5-run majority; Savage & Rebello (2025), where the wrong-idea categories were not validated.
- ChatGPT hints were not significantly different from human hints (Pardos & Bhandari 2024), but generated hints fail quality checks without verification (map §6).
- Knowledge in pieces and the 31% FCI retest instability mean that a "learner state" is context-bound. A surrogate learner calibrated to single items would inherit this instability.

### 8.3 The repo's own surrogate expert (`instrument/src/probe_app/simulate.py`)
- **What it does:**
  - It prompts a model to "Role-play Dr. Lee, a human physics lecturer taking part in an education research interview … Reply … as Dr. Lee would say it aloud: two to five sentences, first person, consistent with the transcript."
  - Its only grounding is `instrument/problems/simulated_think_aloud.json`, a hand-written, unsourced think-aloud fixture for A1–B2 (e.g. "Then they stick, so that part isn't energy, it's momentum, the collision loses energy.").
  - A `FixtureTranscriber` replays that fixture in place of audio.
  - The AI interviewer (Opus 5) then probes the surrogate through the real contract and guard.
  - Sessions are marked `simulated`, and `probe_code/loader.py` plus decision 0001 (`simulated-sessions-rejected`) bar them from coding.
- **The refusal observation:** commit `098eaee`: "Simulator: role-play prompt on Sonnet 5 — Opus 5 refuses expert role-play under reasoning_extraction". `instrument/pilot-protocol.md`, "Refusals": "Claude Opus 5 runs a `reasoning_extraction` safety classifier. It refused every attempt to have Opus 5 role-play the expert (which is why the simulator uses Sonnet 5)."
  - In the same sessions, Opus 5 as *interviewer* had 0/86 refusals (`docs/freeze-baseline.md`).
  - The refusal thus attached to impersonating a human expert and verbalising their reasoning, not to asking about reasoning.
  - Implication for surrogate cohorts: refusal behaviour is model-specific and must be measured per model and role. `backends.py` already separates `LLMRefused` from `LLMUnavailable` so that these rates can be counted.
- **What the simulated runs showed:**
  - 3 current-configuration sessions: 86 AI turns, 95 generated, fallback 1.2%, guard rejection 4.5%, contract rejection 0/95, refusals 0/86, median latency 5.0 s.
  - 172 generated questions over the simulated sessions feed the calibration set.
  - The recorded limits: "Sonnet role-play, not physicists. Simulated answers are fluent, on topic and typed; real answers are spoken, transcribed, hesitant and sometimes off topic." "The guard rejections look like guard errors" (all on the `alternatives` stem).
  - The codebook's (SIM) examples and `codebook-stress-tester` ("Simulated experts are Sonnet role-play, so say which findings may not survive real data") show the surrogate was useful for exercising the codebook and pipeline. It was never treated as evidence of expert cognition.
- **Caveat:** the surrogate is grounded in text the project itself wrote. Under a provenance-first design it is an example of what to avoid: no source, no citation, and its "tacit" content was authored by the builder.

### 8.4 On the residual concept
- Expert omission of about 70% (Sullivan et al. 2014) and TA/instructor blind spots (Maries & Singh) support the existence of a residual on both sides: what experts do not say, and what experts do not know learners lack.
- Stage A's "absent from ordinary material" and "published framework" tags already separate course-absent from literature-absent. This is the distinction a public-evidence reconstruction would need in order to claim a residual.
- `explore-conceptual-change.md` and `explore-concept-inventories.md` warn that population-level public data cannot be read as individual states.

### 8.5 On validity threats a surrogate programme inherits (map §11)
The relevant entries of "What not to assume":
- "Do not assume the LLM's reconstruction of expert reasoning is valid because it sounds plausible";
- "Do not assume an expert can accurately verbalize their own cognition";
- "Do not assume experts or instructors know which difficulties are common; check against student response data".

The first is the central risk of surrogates. The repo's answer so far has been corroboration against an observed human trace, which zero-participant work cannot supply; public performance traces (worked solutions, think-aloud corpora, error datasets) would be the analogue.

---

## 9. Evidence grades in the map

- **Scheme (map §4 footnote):** "Evidence strength here is a **research-prioritization judgment**, not a formal GRADE score. It distinguishes mature replicated literatures from frameworks supported mainly by qualitative studies, case studies, or newer trials."
- **Vocabulary:** High · Moderate–high · Moderate · Low–moderate · Low / contested · Emerging / moderate. Ratings are routinely **scoped** (e.g. "High for cohort/course evaluation", "Moderate–high for predicting performance", "for training outcomes outside physics") or **split** into two claims (conceptual change: High for persistence, Moderate for interventions; formative assessment: High for feedback and quizzing as practices, low–moderate for packaged interventions).
- **Per-source grading rule (`/branch` step 4):** design (meta-analysis / RCT / quasi-experiment / qualitative / theory), N, domain, and outcome type (transfer / retention / immediate). Evidence outside physics or university level is labelled as such. Each note's Evidence table carries these columns. "Abstract" marks sources read only in abstract; preprints and secondhand reports are marked.
- **Change rules:** "No source at or above quasi-experimental design supports a change → leave the rating as it is" (`/branch` stop conditions). Two downgrades were made "by the user's decision, departing from the stop rule": PCK Moderate–high → Moderate, and Threshold Concepts Moderate/contested → Low/contested. DtD fell from "Moderate / developing" to "Low–moderate" by falsification.
- **Supporting marks:**
  - Decision-gap status: settled / partly settled / open.
  - *(project choice)* marks a threshold that is a judgment, not a sourced value.
  - L2.1 requires syntheses to preserve each claim's "rating word, domain, timing, grain (item vs total, cohort vs individual) and comparison".
  - `citation-verifier` verdicts: supported / overstated / wrong / unresolvable / unsourced.
- **Current §4 ratings:**
  - DtD Low–moderate; CTA Moderate–high (outside physics); Expert–Novice High (foundational); PCK Moderate.
  - Conceptual Change High (persistence) / moderate (interventions); Concept Inventories High for cohorts, weak for individuals; Cognitive Apprenticeship Moderate.
  - Worked Examples + Self-Explanation High (immediate); ITS High on aligned tests, small at scale; KT Moderate–high for prediction.
  - Threshold Concepts Low/contested; Formative Assessment split; LLM tutoring Emerging/moderate.
- The scheme grades education-intervention evidence against a university-physics transfer target. It has no grade for evidence from organisational settings, for synthetic or surrogate data, or for public-corpus reconstruction. Those would need new categories.
