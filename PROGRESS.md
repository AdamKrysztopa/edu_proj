# Research progress

Tracks work against [`REORIENTATION.md`](REORIENTATION.md), the strategic plan adopted 2026-09-28, and the evidence in [`ai_education_research_map.md`](ai_education_research_map.md). Each ticked branch links to its note in `research/`.

**Visual PoC brief (Track A):** [What we plan to build, need and learn](docs/poc-explained.html) explains the frozen Track A route, not the project plan. Optional reading.

## Current priority — the NOW programme (`REORIENTATION.md` §22)

The project is reoriented: reconstruct what public and organisational evidence already says, predict where that reconstruction is missing human knowledge, and ask humans only about that residual. NOW needs zero participants, zero proprietary data, zero microphones and zero live expert interviews; its one human input is one blind second coder. Physics is one benchmark domain; the prepared physics study is frozen as Validation Track A (below).

**Next:** N2, the gated reconstruction pipeline v0 ([plan](docs/plans/n2-reconstruction-plan.md)). First, owner input: the E-ABST false-answer margin and the private objective. In parallel, fill in the rest of the threshold table and pre-register N3 (E-CTA, E-OSS) before acquiring any gold. N8 (E-SEAL) and N9 (cost ledger) can start at once.

| Item | What | Gate | Status |
|---|---|---|---|
| **N0** | Reset: DOI hook path fixed; Track A labelled frozen; `CLAUDE.md`, `PROGRESS.md` and map rewritten; domain-neutral package for reused components | DOI hook fires on a test edit | **Done 2026-09-28, gate passed.** `scripts/hook_tests/test_check_dois.py` runs the registered command offline, and a live Write of a made-up DOI was blocked. The test found that Drain 5 had stopped the hook reading `doi.org/` links; fixed, lesson queued. Package `residual/` created (pydantic only; own test hook); `instrument/` untouched |
| **N1** | Claim record, six evidence labels, knowledge-type vocabulary, gap-map fields | Every gold item expressible with ≤ 2 new field types | **Done 2026-09-28, gate: continue with 2 additions, at the registered limit** (`KnowledgeType.INTERPRETATION`, `ResponseDistribution`). Schema, feature set and label code hash-frozen in `residual/frozen/n1.json`. Record below |
| **N2** | Gated reconstruction pipeline v0; E-PLANT, E-ABST | Beats the ungated model on planted falsehoods and private objectives | Planned ([plan](docs/plans/n2-reconstruction-plan.md)); not started |
| **N3** | **Central test:** E-CTA (clinical, troubleshooting gold) and E-OSS | Pre-registered ΔAUROC stop/continue rule vs the strongest baseline | Not started; gold not yet acquired |
| **N4** | Behavioural validity: E-KC, E-DIST, E-MISC | Non-inferior KC fit; beats raw LLM likelihood; misconception recall | Not started |
| **N5** | Residual measurement against gold as an independent occasion | Unseen-item estimate matches the gold count within tolerance | Not started |
| **N6** | Question selection by expected information gain vs held-out gold oracles | Beats random, plain-LLM and expert-written lists | Not started |
| **N7** | Surrogates: labelling rule, validation tiers T1–T3 on public data | Uses licensed by tier reached | Not started |
| **N8** | E-SEAL: sealed Track A predictions | None (secondary, non-gating) | Not started |
| **N9** | Cost ledger | None | Not started |


### N0–N1 record (2026-09-28)

- **Decisions (owner).**
  - "A handful" means ≤ 2 new field types: a new field, model or vocabulary member.
  - The area partition and importance weights freeze with each experiment's pre-registration, still before gold.
  - Both are recorded in the `REORIENTATION.md` §22 threshold table. The N1 gate row was reworded to match. Its original text defined "continue" only for zero additions, and "change" only for more than a handful, which left 1–2 undecided. The wording now follows the ≤ 2 decision.
- **Decisions (design)** ([decision 0006](docs/architecture/decisions/0006-residual-accounting-core.md)):
  - Labels are computed from verified evidence, never set, and the generating model's family cannot verify its own output.
  - `@evidential_gate` reads only typed, labelled inputs and refuses a synthetic, unknown or inferred criterion. Synthetic *predictors* stay allowed, so N3 can gate a gap map built on them.
  - Gold, reconstruction and surrogate material live in separate ledgers.
  - Observed residual, estimated residual and gap-map prediction are separate types.
  - Published CTA lists are *literature-supported*, not observed (§6).
  - OSS artefacts are World B; public learner data are World A.
- **Gate evidence.** [`docs/n1-gold-shapes.md`](docs/n1-gold-shapes.md) is a schema-blind inventory of 16 gold shapes, committed before the claim model. [`docs/n1-schema-validation.md`](docs/n1-schema-validation.md) maps every attribute, and `residual/tests/test_cross_domain.py` checks the mapping.
- **Schema changes forced by validation.**
  - `interpretation` knowledge type (Chao & Salvendy, PARI).
  - `ResponseDistribution` model: E-DIST computes on per-option shares. Review caught these first sitting in locator text.
  - The allowance is used up. Anything more (E-KC's L3 log tables at N4, or Sullivan per-step capture histories if published) needs a re-freeze and a new owner decision.
  - Prevalence weights use the existing `Measurement` type through `recall(weights=)`, which is not a field type.
- **Reviews.**
  - A test-writing agent found 5 defects.
  - A type-design review found 7 gate bypasses, via pydantic's unvalidated `model_copy` among others.
  - A skeptical-maintainer review found 10 more issues:
    - self-verification slipped through with the generator unrecorded;
    - a surrogate ledger reached a gate;
    - verified simulation output was labelled "supported";
    - OSS newcomer evidence could not answer "what is difficult";
    - `as_of` ignored `valid_from`, and drops came without reasons;
    - a numeric key could hide in a dict passed to a gate;
    - a matcher could share the generator's model family;
    - the DOI test lacked a fixture for the bare form;
    - the E-DIST distributions sat in text.
  - All are fixed, each with a regression test, and the schema was re-frozen afterwards (before any gold).
  - The citation check corrected reference [2]'s volume and issue.
- **Limitations.**
  - The items are illustrative. Real gold is re-checked on acquisition, and any field it forces counts against the same threshold and needs a re-freeze.
  - E-KC and E-DIST need learner-response tables (L3), deferred to N4.
  - Sullivan per-step coverage, if published, would need a capture-history record (would be the 2nd addition).
  - The gate checks expressiveness, not prediction (R13).
  - A `Measurement` certifies which claims it was scored against, not the arithmetic behind its value. `Threshold.registered_in` is free text. Python cannot stop deliberate forgery; the rules stop accidents, and code review plus N2's run log cover the rest.
  - No schema was committed before the inventory, so the addition count rests on the validation record, not on git.
- **Tests.** `uv run --directory residual pytest -q` (268); `python3 scripts/hook_tests/test_check_dois.py` (14); the instrument suite is unchanged (311). `git diff 520d8fd -- instrument/` and the Track A design, roadmap and decisions 0001–0005 are empty.

**LATER** begins only after N3 continues or pivots: labellers, expert raters, targeted residual interviews with a blind arm, a small learner error sample, one organisational pilot under a DPIA. **MUCH LATER:** learner-facing modules, live generation, instructional RCTs, per-student diagnosis.

## Validation Track A (frozen) — roadmap steps

**Frozen 2026-09-28 as a unit; starts only on its own registered preconditions (course, ethics, physicists), independent of the NOW programme. Registered rules unchanged.** Steps 1–6 worked out the Track A route; steps 7 onward are its milestones (M1–M8 in `research/roadmap.md`), in execution order. Steps 7 and 8 wait on people.

**Size:** S = small task; M = several focused tasks; L = substantial work; XL = participant study with external scheduling. These are rough effort categories, not calendar estimates.

**Priority:** P0 = essential; P1 = follows core validation; P2 = conditional extension. Dependencies refer to numbered steps in this table. Research-family priorities in the branch inventory below are separate from execution priorities.

| Name | What introduces / what does? | Size | Priority | Blocked by |
|---|---|---|---|---|
| **1. Consolidate existing research — done** ([comparison](research/route-comparison.md)) | All 13 research families compared by role, evidence, limits and overlap; they reduce to five independent choices. | M | P0 | — |
| **2. Resolve decision-critical gaps — done** ([gaps](research/decision-gaps.md)) | Six targeted searches; none settles a gap; three give first-version defaults. | M | P0 | 1 |
| **3–6. Route, physics case, first version, roadmap — done** ([roadmap](research/roadmap.md)) | Selected approach; hypothetical worked case with the hidden-knowledge taxonomy; first-version scope and reuse; milestones, cohorts and assumptions register. Reviewed by `methods-critic` and `citation-verifier`. | M | P0 | 1–2 |
| **7. M1 — Bottleneck check (early K0) — kit built; waiting on course, physicist check and registration** | Registered K0 items plus component items and a second form; two-coder coding; K0 decision on form 1. Tests A1, A5, A10. | L | P0 | Course offering and ethics (logistics below) |
| **8. M2 — Elicitation tool and pilot — tool built and verified; waiting on 3–5 simulated sessions, preflight and pilot physicists** | The pre-pilot instrument items below; `/preflight pilot`; 1–2 physicists; codebook checked. | M–L | P0 | Pilot physicists |
| **9. M3 — Module v0** | Module format and validator, static player, logging, mastery rule; provisional conservation module and its matched ordinary version; usability with 5–8 students. Tests A4. | L | P0 | 7 not stopped; 8 |
| **10. M4 — Validated operations (Stage A)** | Freeze, pre-register, 12 experts; K1. Tests A2, A3. | XL | P0 | 7 not stopped; 8 |
| **11. M5 — Feasibility run** | Both module versions in one section; compliance, time match, delayed-test logistics. | L | P0 | 9; its own offering |
| **12. M6 — Learning and transfer (Stage B)** | Registered two-arm RCT; pretest K0, then K2. Tests A1, A9. | XL | P0 | 10 with K1 passed; 11 |
| **13. M7 — Offline learner-model check** | Knowledge tracing fitted to logs against the three-in-a-row rule. Tests A7. | S | P1 | Logs from 11 or 12 |
| **14. M8 — Live generation arm** | Static vs live LLM feedback on the same prompts, delayed unassisted test. Tests A6. | L | P1 | 12 with K2 passed |
| **15. Refine the approach** | Continue, change or stop components from M1–M8; update requirements. | M–L | P0 | 12 |
| **16. Later experiments** | Powered order experiment (A8); Phase 3 diagnosis comparison; per-student routing if M1's form agreement supports it. | L–XL | P1 | 15 |
| **17. Polish the frontend** | Navigation, presentation and usability of the established workflow. | L | P1 | 15 supports continuing |
| **18. Extend beyond the initial case** | A second topic, other disciplines, teacher-facing uses; adaptive personalization only with useful signals. | XL | P2 | A supported initial approach |

**Reading is not a blocker:** the short summary is the entire minimum; every book, paper and branch note is optional reading for the user.

### Course logistics — needed for M1 and M6

- [ ] Confirm the Stage B course's pretest can carry 2 open-response conservation problems after the topic's lectures (K0 data; no past exam scripts are available).
- [ ] Name the course offering for early K0 and confirm its ethics cover a research quiz. Credit follows the experiment protocol and the course's rules.
- [ ] Allocate distinct offerings to early K0 (M1), the feasibility run (M5) and Stage B (M6), and freeze the lecture notes that serve as Stage A's baseline (roadmap, "Cohorts").

## Method branches (§4, §5)

### P0
- [x] **Decoding the Disciplines**: `falsify` → **narrow**. Kept as the instructional frame; elicitation (step 2) moves to CTA; evidence rating Low–moderate. [note](research/falsify-decoding-the-disciplines.md)
- [x] **Cognitive Task Analysis**: `explore` → **no rating change, scoped**. Moderate–high for training outcomes outside physics; no physics or transfer data. Provisional physics method: think-aloud while solving, then retrospective CDM probes; §14 DOI for Crandall et al. (2006) corrected. [note](research/explore-cognitive-task-analysis.md)
- [x] **Expert–Novice research**: `explore` → **no rating change, scoped**. Representation differences replicate but form a continuum; principle-first instruction helps immediate problem solving in small physics studies; one far-transfer RCT (Nokes-Malach et al. 2013), no delayed transfer. Adds a published-framework tag to Stage A and an exploratory arm × pretest interaction to Stage B. [note](research/explore-expert-novice.md)
- [x] **Pedagogical Content Knowledge**: `explore` → **downgraded to Moderate; PCK layer re-sourced**. Correlational links to school achievement only (mixed in physics), no experiment isolating PCK, no university or transfer outcomes. Physics TAs and instructors miss many common FCI difficulties, so misconception entries are seeded from student response data and teachers review them; §6 moves PCK from expert elicitation to learner diagnosis. [note](research/explore-pedagogical-content-knowledge.md)

### P1
- [x] **Conceptual Change + misconceptions**: `explore` → **rating split**. High that intuitive ideas persist alongside instruction; Moderate for interventions (refutation text g = 0.41, holds at delay; physics curricula from cohort studies; no university transfer outcomes); theory contested. Phase 3 adds cross-context consistency; Phase 4 adds refutation and predict-then-observe. [note](research/explore-conceptual-change.md)
- [x] **Concept Inventories**: `explore` → **no rating change, scoped to cohort-level use**. Strong class-level validity; weak for individual diagnosis (31% of FCI responses change on retest, mixed models, gender-biased items). PCK-layer seeding and Stage B EMCS use are cohort-level, so defensible; Phase 3 adds test–retest stability; EMCS drops Q16, Q22, Q23. [note](research/explore-concept-inventories.md)
- [x] **Cognitive Apprenticeship**: `explore` → **no rating change, scoped**. Components have experimental support (scaffolding g = 0.46); no whole-model test in physics; fixed-schedule fading no better than none, per-learner fading supported only outside physics. Explore-first vs model-first is split; Phase 4 now treats order as a factor. [note](research/explore-cognitive-apprenticeship.md)
- [x] **Worked Examples + Self-Explanation**: `explore` → **no rating change, scoped**. High for immediate novice problem solving (g ≈ 0.5); delayed and transfer effects smaller (g ≈ 0.35); reverses with prior knowledge. Forced Stage B change: each added operation is carried by a self-explanation prompt, equal prompt counts in both arms. [note](research/explore-worked-examples-self-explanation.md)
- [x] **Intelligent Tutoring Systems**: `explore` → **no rating change, scoped to aligned tests**. 0.73 on local vs 0.13 on standardized tests (Kulik & Fletcher 2016); ≈ 0–0.2 SD at scale. Andes physics: non-randomized, gains on enforced practices, d = 0.25 on an answer-only final. §6 separation principle untested; Phase 5 must evaluate on non-aligned tests over more than one term. [note](research/explore-intelligent-tutoring-systems.md)
- [x] **Knowledge Tracing / Mastery models**: `explore` → **no rating change, scoped to prediction**. Simple models match deep KT; learning evidence is a few small KC-redesign studies on hand-picked units plus one null; no test against a simple mastery rule. Phase 5 must judge a learner model by a learning experiment against N-correct-in-a-row with delayed transfer. [note](research/explore-knowledge-tracing.md)

### P2
- [x] **Threshold Concepts**: `explore` → **downgraded to Low / contested** (user decision, as for PCK). Definitions criticised as not empirically isolable; no agreement statistic for identifying threshold concepts; physics papers relabel known PER difficulties; small immediate-outcome studies test teaching a concept, not the label. [note](research/explore-threshold-concepts.md)
- [x] **Formative assessment**: `explore` → **rating split**. High for feedback and quizzing as practices (feedback d = 0.48, over a third of effects negative; quizzing g = 0.50); low–moderate for packaged formative assessment (d ≈ 0.2–0.3; the quoted 0.4–0.7 has no source). New §5.13 card; Phase 4 holds feedback constant across arms. [note](research/explore-formative-assessment.md)
- [x] **LLM-based AI tutoring**: `explore` → **no rating change, scoped**. Kestin et al. (2025) is large but immediate and bundles AI with self-pacing and pre-structured steps; with the AI removed at test, effects elsewhere are ≈ 0.1–0.4 SD, null in preregistered lab RCTs, or harmful without guardrails; syntheses weak, one retracted. Phase 5 compares any LLM tutor with the same design without generation; §11 adds "do not measure learning while the AI is available". [note](research/explore-llm-tutoring.md)

### Instrument and study — M1 kit, M2 build, later gates

Stage A is M4 and Stage B is M6 in the roadmap. Stage A addresses Phase 2; Stage B addresses one Phase 4 comparison.

**M1 kit — built (2026-09-28), waiting on the course:**
- [x] Items (Form 1 = registered K0 pair, Form 2, components), answer key, K0 codebook and pre-registration draft in `instrument/k0/`; `probe-code k0-sample`, `k0`, `k0-kappa`, `form-agreement` enforce the registered rule and the plan. Reviewed by `methods-critic` (majors fixed); physics checked by Codex (all answers confirmed).
- [ ] A physicist checks the items and their timing; the user completes the *to confirm* fields in `instrument/k0/prereg-early-k0.md` (course offering, ethics, coders, seed) and registers it before the quiz.

**M2 build — done (2026-09-28):**
- [x] HTTPS tablet setup verified end to end in the browser: console create → tablet link (now the LAN address, carrying the session code) → join with microphone → think-aloud → audio stored; LAN access to console routes refused. Two defects found and fixed: the console linked the tablet to 127.0.0.1, and a refused microphone failed silently.
- [x] `FrozenConfig` hashes the model-facing code, `problems.json`, `human-script.md` and the expert page (decision 0004, rule 1).
- [x] Codebook v0: trace and probe units, per-code multi-label agreement (`--multi`), Include/Exclude cells filled; stress-tested.
- [x] Every CLI subcommand smoke-tested; `UNRUN` is empty.
- [x] E_A and E_B drafted as a paper handout (`instrument/problems/explanation-problems.md`), kept out of `problems.json` so the guard's non-leading vocabulary does not grow.
- [x] Freeze baseline and computed freeze rule (`probe-code freeze-baseline`, `docs/freeze-baseline.md`); proposed thresholds from the simulated baseline.
- [x] Decision 0005: console routes loopback-only, full uuid4 session IDs.
- [x] Encrypted backup and restore of sessions (`probe-app backup`/`restore`, passphrase from `PROBE_BACKUP_PASSPHRASE`).
- [x] Leading-probe rule applied identically in both arms: `human-script.md` states the guard's rule verbatim; `guard-audit` (refuses config drift) and blind `export-leading` cover both arms.
- [ ] Before the pilot: 3–5 more simulated sessions (`probe-app simulate`), then recompute the baseline thresholds (`docs/freeze-baseline.md`); `/preflight pilot`; a physicist checks A1–B2 and E_A/E_B.

**Before `probe-app freeze` (gate for M4; decisions 0003, 0004):**
- [x] Guard calibration built: `probe-code guard-calibration-sheet`, `guard-calibrate`, `calibration-report`; 60 items in `instrument/calibration/items.csv` (all 9 guard-rejected candidates, 21 accepted, 30 authored leading variants); protocol and decision rule in `docs/guard-calibration.md` (reviewed by `methods-critic`, fatal and majors fixed).
- [ ] Two labellers label the 60 items (not the item author, the PI, or any Stage A coder); adjudicate; run the guard; register the report with the guard prompt hash.
- [x] Stage A pre-registration additions drafted (`docs/stage-a-prereg-additions.md`): separate leading-content coders, two-sided arm-guess rule, unmarked-speech handling, leading human questions; K1 decided on the registered analysis alone.
- [x] Human-arm speech before the first I/E marker is marked `unmarked`, kept off coder sheets, counted in the leading key and guard audit, and warned on the console.
- [x] Stream-invariant tests (decision 0003); missing part files, chunk gaps and reload holes now hold the problem or warn the console; console "Accept audio gap" action (wiring checked in the browser; the success path is covered only by unit tests until a dry run with real speech).
- [x] Output schemas tied to their Pydantic models; `extra="forbid"` on `GuardVerdict`; one `make_guard()`/`make_interviewer()` used by the app and `probe-code`.
- [ ] Recording module extraction (decision 0003: after the pilots, under the invariant tests). Known leftovers: a failed save can duplicate a chunk; truncated part files are not detected; the pilot checks the tablet's real chunk rate.
- [ ] After the last change to a frozen file and before the pilot: 3 simulated sessions on that configuration (the baseline sessions are now a superseded configuration; the thresholds were fixed in advance and stand).
- [x] `/branch experiment`: gated two-stage design; `methods-critic` reviews applied. [note](research/experiment-ai-assisted-cta-physics.md)
- [x] Stage A instrument built ([spec](docs/superpowers/specs/2026-09-26-stage-a-session-app-design.md)).

## Reading

**Entire minimum:** `REORIENTATION.md` §1. [research/minimum-reading.md](research/minimum-reading.md) is the Track A brief. This does not assert that the user has read either.

**All further reading is optional**, including Pace, Shulman, Chi et al., Clark et al., Kulik & Fletcher, Kestin et al., the FCI paper and every branch note. The optional source selection remains in map §8. There is no extra reading checklist to complete before continuing.

## Research phases (§9)

These track the map's research questions inside Track A; the reoriented questions are RQ-A to RQ-J in `REORIENTATION.md` §17.

- [ ] **Phase 1** (roadmap 7, M1): validate the premise. Taxonomy drafted in the roadmap's step 4; learner evidence not collected, so the kill criterion has not been evaluated.
- [ ] **Phase 2** (roadmap 8 and 10): expert-elicitation experiment (ordinary explanation vs human-led vs AI-led DtD/CTA vs think-aloud)
- [ ] **Phase 3** (roadmap 16): learner-bottleneck diagnosis; cohort-level diagnosis is used until then
- [ ] **Phase 4** (roadmap 9, 11–12): intervention experiment with transfer as the primary outcome
- [ ] **Phase 5** (roadmap 13–14, 18): adaptive system

## Open evidence gaps that would change a verdict
- [x] Full text of Fukaya et al. (2025): weak, model-dependent PCK–achievement link; PCK lowered to **Moderate** (a controlled study of difficulty-knowledge causing gains would restore Moderate–high)
- [ ] A controlled university-physics study of expert-representation instruction with **delayed** transfer
- [ ] A controlled comparison of the decoding interview against CTA (would move DtD back to **keep**)
- [ ] A CTA-derived instruction study in physics or university STEM with a **transfer** outcome
- [ ] A test of the provisional physics elicitation method: think-aloud while solving, then retrospective CDM probes

## Infrastructure
- [x] `/branch` and `/elicit` skills, `citation-verifier` and `methods-critic` agents, DOI hook (settings path fixed 2026-09-28; it had called a deleted `.sh`)
- [x] `/session-report` skill, `validity-reviewer` agent, hooks guarding `.env` and the frozen prompts
- [x] Lessons loop: queue `docs/lessons.md`, archive `docs/LESSONS-ARCHIVE.md`, `lessons` and `implement-ll` skills, SessionStart hook, checker `scripts/lessons_graph.py`. Capture is step 9 of `/branch`; the drain runs before `probe-app freeze` (`instrument/pilot-protocol.md`)
- [x] Zotero local API responding
- [x] `openalex` MCP server loaded
- [x] `zotero` MCP server loaded
- [x] `guard-session-data.sh`: denies file-tool writes to `sessions/` and `instrument/sessions/`, and asks before Bash `rm`/`mv`/`sed -i`/redirects into them or `git clean -x`
- [x] `run-instrument-tests.sh`: reruns the instrument suite after edits under `instrument/{src,tests,web,prompts,problems}` and blocks on failure
- [x] `/preflight pilot|data`: clean tree, `prereg.json` match (data), tests, live transcriber and simulated session, `validity-reviewer` since the last real session; step 5 of the pilot protocol
- [x] Project `CLAUDE.md`: the experiment's gates and stages, off-limits paths, tests, when to use each agent and skill, definition of done
- [x] `codebook-stress-tester` agent: applies `instrument/codebook/v0.md` to simulated exports and reports codes that overlap, go unused or are applied with low confidence; before pilots only, never as a coder of record
- [x] Add `.claude/worktrees/` to `.gitignore`
- [ ] Zotero library seeded with this project's reading (currently no items in this area)
- [x] DOI hook also checks that the resolved title matches the cited work (`check-dois.py`: first author or two title words on the line).
- [x] DOI hook reads any DOI form (`doi.org` links, `doi:10.…`, bare) and reports unreachable DOIs as unverified (L5.1)
- [x] SessionStart hook warns when a registered hook script is missing or not executable (L5.1)
- [ ] `methods-critic` checklist rewritten for zero-participant and surrogate designs
- [x] DOI hook proven to fire by a deterministic test of the registered command (`scripts/hook_tests/test_check_dois.py`); `doi.org/` links read again (2026-09-28)
- [x] `run-residual-tests.sh`: reruns the `residual/` suite after edits under `residual/`
