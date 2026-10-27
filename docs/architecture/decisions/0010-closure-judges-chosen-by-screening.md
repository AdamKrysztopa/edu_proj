---
id: 0010
status: active
skill: decide-architecture
date: 2026-10-27
commit: ee1744a
rules:
  - id: screen-free-gates-before-paid
    statement: gapmap.screen starts a paid screening run (G1, G2) only when every earlier step of the sequence, the $0 fixture gate and, for a same-family candidate, the parallel-arm gate, is satisfied under the current fixture hash; it starts at most one paid run per invocation and never two on one candidate at once.
    scope: ["gapmap/src/gapmap/screen.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_a_paid_step_is_refused_while_the_free_fixture_gate_fails
  - id: screen-same-family-after-other-family
    statement: A candidate whose family is a target ledger's generator or verifier family gets no paid screening run until an other-family candidate is eligible on the same fixture hash, and a usable judge pair needs an eligible cheap other-family arm and an eligible top-tier arm on one hash.
    scope: ["gapmap/src/gapmap/screen.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_a_same_family_candidate_is_refused_paid_runs_until_an_other_family_arm_is_eligible
  - id: screen-eligible-only-after-required-passes
    statement: verdict.json records a candidate eligible only after one passing G1 run and two passing G2 gate-split runs, each in a new directory with an empty closure cache, under the current fixture hash; a complete failing run puts the candidate out and an incomplete run never counts.
    scope: ["gapmap/src/gapmap/screen.py"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_eligibility_is_recorded_only_after_one_g1_and_two_g2_passes
---
# Closure judges are chosen by the screening entry point

## Context

D1b chose its closure judges by measurement (`docs/plans/gapmap-fix-and-d1-rerun.md` §2.1–2.2): G1
(N3 L7.3 fixtures) and G2 (topicality-controlled plants, gate split twice). The order of the checks,
ADR 0009's parallel arm and the number of required runs lived in prose, and sol's paid runs were
started before the free Stop A count that should have stopped them (lesson 2026-10-26).

## Decision

- `python -m gapmap.screen` is the one way a closure judge becomes eligible for N3 work: S0 fixtures
  ($0), S1 parallel arm ($0, same-family candidates), G1 once, G2 gate split twice, in that order,
  through the committed runners with their rules unchanged (`docs/plans/judge-screening-standard.md`).
- The runners stay where they are (`research/d1b_rerun/g1.py`, `g2.py`); `gapmap.screen` calls them
  as subprocesses and reads their result files, so the package imports nothing outside itself
  (ADR 0008's import rule holds).
- Replay stays the default: without `--live` no paid run starts (ADR 0009 `gapmap-live-judges-opt-in`).
- **An addition to ADR 0009, not its reading.** 0009 needs the other-family arm to have run; S1
  needs it to be eligible, because a same-family judge cannot be used alone.
- **Which runs need a top-tier arm.** Screening runs measure a candidate against owner-confirmed
  labels, so a cheap candidate's screening runs need no top-tier arm of their own. The rule that
  the cheap arm alone never settles applies when a judge is used: `pair` reports a usable pair
  only when both arms are eligible on one fixture hash.

## Consequences (cost)

- A same-family top-tier candidate is screened only after the cheap arm is eligible, so the two
  arms can no longer be screened in parallel; screening takes longer in wall time.
- A judge that fails one complete run is out on that fixture hash; a borderline judge cannot be
  re-run until it passes. Changing any fixture or runner file voids every earlier run.
- The fixture set is D1's (dependence-forecastability) for G2 and N3's for G1. A domain with its own
  fixtures needs a new sequence version and new hashed files.
- Eligibility is advisory until the gapmap CLI and control2 read `verdict.json`; neither does yet
  (follow-up in `docs/plans/judge-screening-standard.md` §6).
- A study-level $0 gate (D1b's Stop A) is enforced only when the plan passes its record as `--after`.
- Adding `screen.py` changes the gapmap package hash (`gapmap.manifest`), as every change under
  `gapmap/src/gapmap/` does; the manifest is regenerated at the MS2 freeze.
