# Test-suite review: `instrument/` (2026-09-27)

## Evidence portfolio

**System context:** a single-researcher lab instrument. It records expert think-aloud sessions, runs AI-led and human-led probe sessions over them, and exports blinded coding material. A failure during a data session is irreversible: lost audio, or a leading AI question, cannot be re-collected from the same expert. Validity rests on the AI-versus-human comparison being fair.

**Assumptions:** CI is a PostToolUse hook (`.claude/hooks/run-instrument-tests.sh`) plus `/preflight`; there is no hosted CI. The runtime and coverage below were measured on 2026-09-27. Escaped-defect data come from `docs/lessons.md`. No live pilot data exist yet, so every statement about stochastic quality is provisional.

**Critical failure surfaces:**
1. A leading AI question reaches the expert.
2. The guard's flag rate differs between arms because of the guard, not the interviewers.
3. Think-aloud or probe audio is lost silently.
4. Blinded exports leak interviewer text or arm.
5. A frozen-config drift is not refused.
6. A CLI entry point is broken while the suite stays green.
7. The configured model refuses the frozen prompts live.

| Risk or claim | Selected evidence | Why it belongs | Cost accepted | Evidence deliberately omitted | Reopen when |
|---|---|---|---|---|---|
| Contract rules (stems, one follow-up, quoted span, cap, fallback) | Unit tests with scripted fakes (`test_contract.py` 11, `test_engine.py` 10) | Deterministic wiring; the oracle is the spec's contract, written by hand | About 2 s; fakes to maintain | Live-LLM tests in the suite | A contract rule changes without a matching test |
| Frozen config refused on drift | Unit tests (`test_config.py` 12, `test_session.py`) | Deterministic; the oracle is the pre-registration rule | Negligible | None | A new frozen field is added |
| Blind export and agreement statistics | Unit tests on synthetic sessions with hand-computed α and κ (`test_analysis.py`, `test_export.py`) | An independent oracle: toy values computed by hand | Negligible | Property-based tests | A codebook change allows several codes per unit (already queued in `docs/lessons.md`) |
| HTTP and state machine wiring | In-process integration via FastAPI TestClient (`test_server.py` 9, `test_session.py` 24) | Covers phase transitions and routes without a browser | About 1 s | Browser E2E in the suite (one headless Playwright run exists from the build, not in the suite) | Tablet-side audio bugs recur that TestClient cannot see |
| **Guard classifies "leading" correctly** | **Nothing calibrated.** The guard is exercised only for parsing (`test_llm.py:75`, `:102`, `:109`) and by a scripted `FlagHuman` (`test_analysis.py:53`) | The guard is an LLM judge used as a measuring instrument: it gates AI turns and its flag rate is compared across arms | — | — | **Buy now** (see the primary recommendation) |
| Live refusals and outages | `/preflight`: one live simulated session with the 1-in-10 refusal and fallback rules | Fakes cannot refuse (`docs/lessons.md`, "Model switch broke the simulator…") | About 7 min and API spend per preflight | A repeated-run refusal estimate | The refusal rate in preflight lands near 1 in 10: one session gives too few turns to separate 5% from 15% |
| Audio stream integrity | Unit tests on `Session` chunk handling | Silent loss is irreversible | Negligible | A stream-module invariant suite (decision 0003) | Before `probe-app freeze` (decision 0003) |
| CLI entry points | 3 tests in `test_cli.py` | — | — | Smoke tests for every subcommand | Already reopened (secondary 1) |

**Deterministic tests vs stochastic evaluations:**
- **Asserted:** contract checks, fallback rules, cap, parsing, refusal and outage mapping, exports, statistics, config drift.
- **Needs evaluation:** whether the guard's "leading" verdict matches human judgment; whether the interviewer asks non-leading, answerable questions; refusal rates on the frozen prompts.

Today the evaluated half has only preflight's refusal count and the planned pilot measures. None of those measure the guard's accuracy.

**Generated-test oracle assessment:** the tests are hand-written from the spec. The expected values are spec rules or hand-computed statistics (`test_analysis.py:14-24`), not outputs captured from the implementation, and there are no snapshot or golden files. Sound.

**Primary recommendation:** before `probe-app freeze`, calibrate the leading-question guard against a human-labelled set, and freeze the set, its results and the guard prompt together.

**Consequences and trade-offs:**
- About 60 labelled utterances to build, which is a few researcher hours.
- One labelled run costs about 60 small Haiku calls.
- Re-running is owed on any change to the guard's model or prompt, which after the freeze means a new pre-registration anyway.
- Interviewer question quality is still left to the pilots and the debrief. That is proportionate at 1–2 pilots.

**The smallest-portfolio check:**
- Nothing broader is added: no browser E2E in the suite, no mutation testing, no LLM judge on interviewer quality.
- The one added item is a calibration of a judge the study already relies on.

## Review sections

**Observed current portfolio:**
- **Unit:** about 105 tests (contract, engine, llm, backends, config, trace, storage, analysis, export).
- **In-process integration:** about 26 tests (session, server, human, cli, simulate), all on fakes.
- **E2E:** 0 in the suite.
- **Evaluations:** 0. The live simulated session in `/preflight` is a smoke check, not an evaluation.
- **Totals (measured):** 131 tests pass in 2.10 s. Line coverage is 94% overall. The CLIs are lowest: `probe_app/cli.py` 72%, `probe_code/cli.py` 78%.

### Evidence-placement problems

1. **The LLM judge is uncalibrated.** `prompts/guard_system.md` defines "leading". Code trusts its verdict to regenerate or replace AI turns (`engine.py`), and `probe-code guard-audit` reports its flag rate for both arms as a comparison. No test or evaluation measures its false-negative rate (leading questions that pass) or its false-positive rate (neutral probes blocked).
   - A high false-negative rate lets the AI arm lead, which inflates "reported only" operations. That is the §11 threat the design's K1(c) contradicted-rate bound exists to catch.
   - A false-positive rate that differs by question style would bias the cross-arm flag comparison.
2. **CLI branches are the escaped-defect class the suite has already missed.**
   - `probe_app/cli.py:51-64` (`serve`, `simulate`) and `probe_code/cli.py:77-89` (`corroboration`, `alpha`/`kappa`, `decoys`, `guesses`) are unexecuted.
   - `docs/lessons.md`, "A constructor change broke a CLI command the suite never ran", records exactly this happening once, with every test passing.
3. **The error paths of the audio stream are uncovered.**
   - `session.py:156`, `:160`, `:173` and `:200`: a stream opened in the wrong phase, an unknown part, and a missing part file skipped silently.
   - Line 200 (`if not path.exists(): continue`) is the same silent-skip shape as the two audio-loss paths in `docs/lessons.md`, which were found only by review.

**The single highest-leverage move:** build and freeze a guard calibration set, then measure the guard against it before `probe-app freeze`.
- **The set:** about 60 candidate probe utterances, each with its trace context. Include clearly neutral stems, restatements of the expert's own words, questions that name an unsaid principle, and near-misses (synonyms, problem-statement words).
- **Labelling:** two researchers label each utterance leading or not leading using the guard prompt's own definition, report κ, and adjudicate disagreements.
- **Measurement:** run `Guard` over the set and report sensitivity and specificity with their CIs.
- **Acceptance threshold:** pre-registered, for example sensitivity ≥ 0.9 on leading items.

**Expected benefit:** it turns the guard from an assumed oracle into a measured instrument, and gives the cross-arm flag-rate comparison and K1(c) a known error rate.

**Migration scope:** a labelled CSV under `instrument/` and a `probe-code guard-eval` command (or a marked live test outside the default suite) that prints the confusion matrix. Smallest first step: label the 30 human-arm and AI-arm turns from the first pilot, run `guard-audit` over them, and compare.

**Indicators the change worked:**
- κ between the two labellers is at least 0.7.
- Guard sensitivity and specificity are reported in the pre-registration.
- A later guard-prompt edit re-runs the evaluation before re-freezing.

**Then, in order:**
1. Add a smoke test per CLI subcommand that drives `main([...])` with fakes and asserts it runs to output. This is cheap and closes the recorded escaped-defect class.
2. Write stream-invariant tests (wrong-phase open, unknown part, missing part file must be reported, not skipped) as the first step of decision 0003.
3. If preflight's refusal count lands near 1 in 10, run the simulated session 3–5 times before freezing, to get a refusal estimate with a usable interval.

**Sound as-is:**
- The contract and engine tests.
- The hand-computed statistics oracles.
- Frozen-config refusal coverage.
- The fast in-process integration layer.
- Keeping live API calls out of the default suite and in `/preflight`.
- Not having browser E2E or mutation testing.
