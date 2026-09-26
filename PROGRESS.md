# Research progress

Tracks work against [`ai_education_research_map.md`](ai_education_research_map.md), which remains the single source of state. Each ticked branch links to its note in `research/`.

## Todo (you)
- [x] Download Fukaya et al. (2025): saved to `research/pdf/` (git-ignored). PCK–achievement r = .13 n.s. to .23 by model, 11 studies; PCK lowered to **Moderate**.
- [ ] Provide K0 data: past first-year mechanics exam scripts or error data (anonymized) for the conservation-principles topic.

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

### Experiment design
- [x] `/branch experiment`: gated two-stage design (K0 exam-error check → Stage A, 12 experts, AI vs human probes validated against the trace → K1 → Stage B, RCT with about 370 students on delayed transfer → K2). `methods-critic`: no fatal flaw; the six major fixes are applied. [note](research/experiment-ai-assisted-cta-physics.md)
- [x] Stage A instrument built: session app and coding pipeline in `instrument/` ([spec](docs/superpowers/specs/2026-09-26-stage-a-session-app-design.md)). Next: pilot on 1–2 physicists (`instrument/pilot-protocol.md`), then freeze.

## Reading (§8)
- [x] **Minimum:** [research/minimum-reading.md](research/minimum-reading.md), a synthesis of all branch notes and the experiment

### Deep dive
- [ ] Pace (2017), _The Decoding the Disciplines Paradigm_. **Read first:** controlled outcome data here could flip the DtD verdict back to keep.
- [ ] Shulman (1986), PCK
- [ ] Chi, Feltovich & Glaser (1981), expert–novice physics
- [ ] Clark et al. (2008), Cognitive Task Analysis
- [ ] Kulik & Fletcher (2016), ITS meta-analysis
- [ ] Kestin et al. (2025), AI tutoring RCT in physics
- [ ] _(optional)_ Hestenes, Wells & Swackhamer (1992), Force Concept Inventory

## Research phases (§9)
- [ ] **Phase 1**: validate the premise; taxonomy of hidden knowledge. Kill criterion not yet testable.
- [ ] **Phase 2**: expert-elicitation experiment (ordinary explanation vs human-led vs AI-led DtD/CTA vs think-aloud)
- [ ] **Phase 3**: learner-bottleneck diagnosis
- [ ] **Phase 4**: intervention experiment with transfer as the primary outcome
- [ ] **Phase 5**: adaptive system

## Open evidence gaps that would change a verdict
- [x] Full text of Fukaya et al. (2025): weak, model-dependent PCK–achievement link; PCK lowered to **Moderate** (a controlled study of difficulty-knowledge causing gains would restore Moderate–high)
- [ ] A controlled university-physics study of expert-representation instruction with **delayed** transfer
- [ ] A controlled comparison of the decoding interview against CTA (would move DtD back to **keep**)
- [ ] A CTA-derived instruction study in physics or university STEM with a **transfer** outcome
- [ ] A test of the provisional physics elicitation method: think-aloud while solving, then retrospective CDM probes

## Infrastructure
- [x] `/branch` and `/elicit` skills, `citation-verifier` and `methods-critic` agents, DOI hook
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
- [ ] DOI hook also checks that the resolved title matches the cited work. It only checks resolution now, so the Crandall et al. (2006) DOI in §14 passed while pointing to the wrong book (now corrected).
