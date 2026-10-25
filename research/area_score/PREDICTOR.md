# I12: no replacement passes the committed predictor screen

**Question:** Can either source-count-adjusted lens predictor pass the committed structural rules?
**Answer:** 0/2 pass on PLC: both pass (b), but (a) is untestable for constant k_step and noise rejection is 87.95%, below 95%; no sampling interval is claimed for this deterministic replay.
**Changed:** No replacement is selected for I7; the owner must choose deferral or an explicit lens-reference fallback.

## Owner decision pending — no option selected

**No replacement passes: should E-CTA be deferred until DS7 revives a feature, or should I7 pre-register the fixed lens reference while accepting a possible tie with the density baseline?**

1. **Defer E-CTA until DS7 revives a feature (Recommended).** Neither replacement passes the fixed screen: the random stand-ins fail (b) only 1,759/2,000 times, and `k_step = 1` on every PLC HYP makes one required part of (a) undefined. Keep I7's predictor choice open; DS7's task is to find public boundary sources that could revive a feature, not a promise that they will. The pool also still requires wave-3 re-judging. Sources: [PLC replay](predictors/plc.json), [DS7](../../docs/plans/deep-search-queue.md), [I12 prompt](../../docs/plans/prompts/I12-predictor-replacement.md).
2. **Pre-register the fixed lens reference with arithmetic-mean area aggregation.** This is the simplest fallback, with PLC within-stratum rho 1.0000, length rho 0.1911, and four distinct nonempty area means. It also fails the fixed screen: choosing it requires an explicit owner exception, not relabelling it a passing candidate. Accept the possibility that DeltaAUROC ties the density baseline and retain the wave-3 re-judging prerequisite. No DeltaAUROC has been computed. Sources: [PLC reference comparator](predictors/plc.json), [I12 fallback options](../../docs/plans/prompts/I12-predictor-replacement.md).

**What would change the recommendation:** a new eligible pool with variation in every required covariate, stand-ins rejected at the fixed 95% rate, and a candidate passing both (a) and (b); alternatively, the owner could explicitly accept the unvalidated fallback and its limits. None of those conditions has been supplied by this replay. This is a recommendation, not an owner decision.

**Decision it feeds:** the E-CTA predictor that I7 hashes for MS2, and the primary-model/baseline choice alongside I5 and DS5 ([implementation queue](../../docs/plans/implement-queue.md), [I12 prompt](../../docs/plans/prompts/I12-predictor-replacement.md)). No MS2 predictor is selected or frozen here.

## Result and scope

Two replacements were implemented and evaluated after the orchestrator's rules commit `14cbdab`. On PLC, topic rank and density residual retain the specified lens signal (within-stratum rho 1.0000 and 0.9549) while their length correlations are 0.2001 and 0.1936. Every defined candidate-level covariate correlation is below the fixed 0.8 trip line, but the mandatory `k_step` check is undefined and the common stand-in calibration fails. Therefore **0 of 2 pass**, even before any choice between them. The reference comparator is also ineligible under those same rules. This is a failure of structural-screen eligibility, not evidence of predictive failure against human gold. Full-precision results: [PLC](predictors/plc.json), [GDPR v1](predictors/gdpr_v1.json), [GDPR v2](predictors/gdpr_v2.json).

All results remain **conditional on an ineligible judge's candidate pool**. `record.categorize` and the existing semantic pipeline determine HYP membership using qwen's cached closure judgements; the new predictors take no semantic closure or confidence-rubric term. Qwen's real-judge diagnostic records `eligible: false` and `stand_in_fires: true`. No judge was called, no cache changed, no gold read, and no paid or network operation ran. Re-judging with sol plus an eligible guard arm stays required for MS2; no guard arm is chosen (coder32 was dropped on 2026-10-24, and Jev cannot be ADR 0009's guard). Sources: [admission code](../../gapmap/src/gapmap/record.py), [qwen diagnostic](../n3_control_v3/qwen/l73/l73.json), [I12 context](../../docs/plans/prompts/I12-predictor-replacement.md).

## Predictors and replay

The two functions in [area.py](../../gapmap/src/gapmap/area.py) were added after rules commit `14cbdab`; they and their first results share commit `b518774`, so their order within it rests on the author's report. No extra candidate was searched:

- **Topic rank (`topic_rank_predictor`).** In each exact `k_topic` stratum of size n, let r be the reference's average rank and set `s = (r - (n+1)/2) / n`. Singleton and reference-constant strata score zero. Every HYP gets a score. Removing stratum means does not guarantee zero Spearman correlation with source count.
- **Density residual (`density_residual_predictor`).** Let s be topic rank and let d be the same within-stratum transformation of candidate `|X|`. Fit the single zero-intercept projection `beta = sum(s*d)/sum(d*d)` on that ledger, using beta=0 if d is constant zero; return `s - beta*d`. No clipping or re-ranking. This is an in-sample structural adjustment without labels or gold, not a trained or validated predictive model. Orthogonality is in transformed values; Spearman correlation need not be zero.
- **Fallback comparator.** Evaluate the unchanged phase-1 lens reference itself, without fitting or residualising it. This is reported separately from the two replacements.

All use the phase-1 **arithmetic mean** within an area, with empty areas undefined. Means can decrease when a below-mean candidate is added; equal-score replication leaves a mean unchanged. No noisy-OR or sum was added. Scores and means are uncalibrated ranking quantities, not probabilities. Tests cover these behaviors, ties, singleton strata, removal of all signal by density adjustment, malformed inputs, and uncapped-pool preservation ([tests](../../gapmap/tests/test_predictors.py)).

The replay sorts all merged HYPs by `gap_id`, uses the original sibling handling for GDPR, and records hashes of the ledger, sidecar, closure cache and sibling ledger. It changes no parser, admission rule, merge rule or frozen ledger field. It preserves the committed uncapped IDs (24/1/6); zero records change category and no candidate is silently discarded. The I6 score, functions and outputs remain unchanged. Evidence: the three replay files' `rows` and `input_sha256`, plus the integration tests above, checked against I6's committed `candidates.json` files.

## Candidate-level associations

Each entry is Spearman rho. `undefined` is never a pass. `size` and `area density` are the candidate's area's values; `length` is the fixed `len(anchor)`. Tables are generated directly from the linked JSON; each JSON also records every covariate's planted result, random trip rate and discrimination flag. These are deterministic finite-corpus descriptions; no sampling confidence interval or independent generalisation claim is attached.
### plc — 24 uncapped HYPs

Source: [plc.json](predictors/plc.json), `predictors.*.a.checks`, `predictors.*.b`, and `reference_comparator`.

| Predictor | k_topic | k_step | \|X\| | size | area density | within-stratum | length | (a)/(b)/(c) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Density residual | -0.0370 | undefined | 0.0634 | 0.0588 | 0.0588 | 0.9549 | 0.1936 | no pass/pass/no pass |
| Topic rank | 0.0099 | undefined | -0.1460 | 0.0948 | 0.0948 | 1.0000 | 0.2001 | no pass/pass/no pass |
| Reference (fallback comparator) | -0.0514 | undefined | -0.0668 | 0.0336 | 0.0336 | 1.0000 | 0.1911 | no pass/pass/no pass |
### gdpr_v1 — 1 uncapped HYPs

Source: [gdpr_v1.json](predictors/gdpr_v1.json), `predictors.*.a.checks`, `predictors.*.b`, and `reference_comparator`.

| Predictor | k_topic | k_step | \|X\| | size | area density | within-stratum | length | (a)/(b)/(c) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Density residual | undefined | undefined | undefined | undefined | undefined | undefined | undefined | no pass/no pass/no pass |
| Topic rank | undefined | undefined | undefined | undefined | undefined | undefined | undefined | no pass/no pass/no pass |
| Reference (fallback comparator) | undefined | undefined | undefined | undefined | undefined | undefined | undefined | no pass/no pass/no pass |
### gdpr_v2 — 6 uncapped HYPs

Source: [gdpr_v2.json](predictors/gdpr_v2.json), `predictors.*.a.checks`, `predictors.*.b`, and `reference_comparator`.

| Predictor | k_topic | k_step | \|X\| | size | area density | within-stratum | length | (a)/(b)/(c) |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Density residual | 0.0000 | undefined | 0.0000 | 0.0294 | -0.0294 | 0.9535 | -0.3714 | no pass/no pass/no pass |
| Topic rank | 0.0000 | undefined | -0.1270 | -0.0938 | -0.1563 | 1.0000 | -0.2732 | no pass/pass/no pass |
| Reference (fallback comparator) | 0.1118 | undefined | 0.0000 | -0.2066 | -0.3019 | 1.0000 | -0.4012 | no pass/no pass/no pass |

PLC alone supplies the intended structural screen. Its four varying covariate checks discriminate, with zero random trips in 2,000 draws each; **k_step is 1 everywhere**, so the fifth cannot discriminate for any predictor. GDPR v1 has one HYP, making the required correlations undefined. GDPR v2 is descriptive only because 140 verdicts are pending; its `k_topic` and `|X|` checks also fail discrimination, and `k_step` is constant. The area's size/density checks in v2 discriminate but cannot rescue the conjunction. A numerical value below 0.8 in an untestable check is not a pass. Sources: the tables' replay files and their `admissibility_note` and `a.checks` fields.

## Area-level spread — descriptive, no size-association pass

PLC has only four candidate-bearing areas. Area-level association with size is **untestable** there; it was not computed or counted as a pass. The GDPR runs offer only one and four nonempty areas. Empty-area means are `null`, not zero. No task-step partition is available in this replay; the partition is the original planner partition, as in [I6](RESULT.md).

| Domain | Predictor | nonempty / empty | min | max | range | distinct nonempty means |
|---|---|---:|---:|---:|---:|---:|
| plc | Density residual | 4 / 1 | -0.0458 | 0.0596 | 0.1054 | 4 |
| plc | Topic rank | 4 / 1 | -0.0500 | 0.0417 | 0.0917 | 4 |
| plc | Reference (fallback comparator) | 4 / 1 | 0.0000 | 0.3333 | 0.3333 | 4 |
| gdpr_v1 | Density residual | 1 / 4 | 0.0000 | 0.0000 | 0.0000 | 1 |
| gdpr_v1 | Topic rank | 1 / 4 | 0.0000 | 0.0000 | 0.0000 | 1 |
| gdpr_v1 | Reference (fallback comparator) | 1 / 4 | 0.0000 | 0.0000 | 0.0000 | 1 |
| gdpr_v2 | Density residual | 4 / 1 | -0.2812 | 0.2500 | 0.5312 | 4 |
| gdpr_v2 | Topic rank | 4 / 1 | -0.2500 | 0.2500 | 0.5000 | 4 |
| gdpr_v2 | Reference (fallback comparator) | 4 / 1 | 0.0000 | 1.0000 | 1.0000 | 3 |

Source: each linked replay JSON's `area_spread` and `areas`; every individual area mean and count is retained there. Both replacements distinguish all four nonempty PLC areas without multiplicative saturation, but spread is not accuracy. Their numerical ranges are on different scales from the old I6 noisy-OR; this is not an effect-size comparison.

## L7.3, reachability and the failed control

The phase-1 PLC control reproduces exactly, including its exclusions: four strata have multiple candidates, but only two have varying reference values, retaining eight candidates for the within-stratum component. The thirteen candidates in reference-constant multi-candidate strata and three singletons remain in the covariate and length checks. These exclusions are identical in every arm and were not revised. Source: [committed phase-1 controls](phase1_controls.json), and the replayed `c` fields.

| Pool | source-count plant rho | source-count check discriminates | uniform failures / 2000 | length failures / 2000 | (c) |
|---|---:|---|---:|---:|---|
| plc | 1.0000 | yes | 1759 | 2000 | no pass |
| gdpr_v1 | undefined | no | 2000 | 2000 | no pass |
| gdpr_v2 | 1.0000 | no | 1812 | 2000 | no pass |

The stand-in rates use 2,000 draws and seed 0, unchanged from the rules. V1's all-fail result is vacuous (`testable: false`), not successful calibration. V2 rejects uniform stand-ins in 90.60% of draws, also below 95%. No inference about judge family or human validity follows: the arms differ only in the supplied score vector, sharing population, reference, lengths, exclusions and checks.

**Best reachable result on PLC:** within-stratum rho can reach 1 (the topic-rank candidate attains it). Nevertheless, the complete conjunction is unreachable on this pool: constant `k_step` cannot yield a defined rho for any scores, and the candidate-independent calibration (c) fails. Therefore no candidate-level improvement can make this fixed screen pass on these inputs. This is why lower nuisance correlations do not justify selecting either replacement.

**SYNTHETIC diagnostic, stored apart:** the unchanged phase-1 fixture has 64 crossed observations, with reference and small seed-0 noise generated independently of source-count assignment. Its specification SHA-256 is `0c9a0350fcfb35d7bbb64e3ba4387918b37808b0fc6de07636cf081604ef797f`. The positive passes (a), (b), and (c): within-stratum rho 0.9701, length rho 0.0265, and both stand-in families rejected in 2,000/2,000 draws. The source-count plant fails (a), with rho 1; the original tests also cover the negative direction. This verifies reachable software behavior on that fixture only. It neither validates the real pool nor supplies a research criterion or gate input. Sources: [synthetic diagnostic](predictors/synthetic/l73.json), [unchanged fixture/tests](../../gapmap/tests/test_predictor_rules.py).

## Committed rules, retained verbatim

The following section is the phase-1 rules section from `14cbdab`, unchanged except for one trailing blank line. Its historical references to work not yet built describe phase 1; the implementations and results above now supply that work. No threshold, reference weight, exclusion, missingness rule or aggregation rule changed.

## Exact rules

1. **Population and order.** One ledger at a time, every merged HYP before
   display caps, sorted by `gap_id`; exclude all RG categories. PLC decides the
   structural screen. GDPR v1 and v2 will be reported separately in a later
   phase: v1 has one HYP and is untestable; v2 has 140 pending verdicts and
   cannot decide. No gold comparison is part of this screen.

2. **Reference, fixed by design.** `R = (L + S) / 2`, where:

   | Input | Term |
   |---|---:|
   | lens DISC, DIAG, SEL, HEDGE or GUARD | L = 1 |
   | lens WHY or RESULT | L = 0 |
   | lexical state open or synthetic-closed | S = 1 |
   | lexical state partial | S = 0.5 |
   | lexical state closed | S = 0 |

   Read the retained merged record's `lens` and
   `inferred_gap.lexical_state`, never its semantic `closure_state`. The lens
   grouping is a pre-stated emphasis on cue/decision lenses; it is not an
   empirically established ordering of importance. Lexical synthetic-only
   support receives the same absence term as open because it is not attested
   support. The state vocabulary is defined in
   [`lenses.py`](../../gapmap/src/gapmap/lenses.py). Unknown or missing states
   are errors, not defaults. No `k_topic`, `k_step`, rubric A/B/P/Q, semantic
   closure, judge output, density or text length enters this function. The
   reference is an internal structural comparator, not criterion validity or a
   selected predictor.

3. **(a), confounding.** On the full uncapped HYP population, reject when
   Spearman **|rho| >= 0.8**, either sign, against any of:
   `k_topic`, `checks.dens` (`|X|`), the candidate area's `n_claims`, the
   candidate area's `evidence_density`, or `k_step`. Use average ranks for
   ties. Each check must also discriminate under I6's rule: a covariate-equal
   plant trips, and uniform U[0,1) scores trip in at most 100 of 2,000 draws,
   Python `random.Random(0)` restarted per covariate. An undefined or
   nondiscriminating check is untestable and cannot support a pass. All five
   must be defined, discriminating and below 0.8 to pass (a).

4. **(b), lens signal and length.** Within each exact `k_topic` stratum, rank
   scores and reference separately with average ranks for ties and subtract
   `(n_stratum + 1) / 2` from both. Pool these centered ranks and compute
   `sum(x*y) / sqrt(sum(x*x)*sum(y*y))`; do not rank a second time or average
   the stratum correlations. This candidate-pooled statistic gives larger
   strata more rank-variance weight. Include only strata with at least two
   candidates and at least two reference values. Those exclusions are fixed
   from the reference before any arm and identical for every arm; a constant
   *score* never removes a stratum. Require pooled rho **>= 0.5**. Separately,
   on **all** uncapped HYPs, require **|rho(score, text length)| < 0.3**.
   Text length means `len(record.anchor)`: Unicode code points of the stored
   anchor, without stripping, tokenisation or appended generated prose.

5. **Missingness.** All vectors must be aligned, equal-length and finite, with
   every required covariate present. Missing/nonfinite values are errors;
   there is no score-dependent complete-case deletion. A constant score,
   constant length, or absent within-stratum reference variation gives an
   undefined required correlation and cannot pass. The within-stratum mask
   never applies to (a) or to the length correlation.

6. **(c), stand-ins.** On the same fixed reference, strata and lengths,
   independently evaluate 2,000 score vectors from each family with separate
   `random.Random(0)` streams. Uniform scores draw one U[0,1) value per row.
   Length-only scores are `a * length + b`: each draw takes a fair random
   sign, magnitude `1 + U[0,1)`, then intercept `U[0,1)`. **Each family must
   fail (b) in at least 1,900/2,000 draws (95%)**. The length transforms have
   only two rank orderings; their repeated failures are a deterministic
   diagnostic, not 2,000 independent pieces of evidence. An untestable
   reference or length cannot make an all-fail diagnostic count as a pass.
   A candidate passes only if **(a), (b) and (c)** all hold. Failure of (c)
   blocks acceptance regardless of the candidate's own associations.

7. **Area aggregation, declared only.** Use the arithmetic mean of candidate
   scores in each area. An empty area is undefined and reported explicitly,
   not silently assigned zero. No sum, noisy-OR or candidate-count multiplier.
   Adding a below-mean candidate can lower the result. No aggregate is built
   in phase 1. PLC has only four candidate-bearing areas, so area-level
   association with size is **untestable**, never reported as a pass.


## Reproduction and verification

From the repository root, use the pre-synced environment and a writable cache:

```sh
UV_CACHE_DIR="$PWD/.uv-cache" UV_OFFLINE=1 UV_NO_SYNC=1 uv run --directory gapmap python ../research/area_score/predictor_replay.py
UV_CACHE_DIR="$PWD/.uv-cache" UV_OFFLINE=1 UV_NO_SYNC=1 uv run --directory gapmap pytest -q
```

The replay runner writes only `research/area_score/predictors/` (or its explicit `--out`); the separate `synthetic/` output never feeds an observed-pool evaluation. A second replay to a scratch directory was byte-identical for all four JSON files. A source-AST comparison against `14cbdab` confirms that every pre-existing function and every module-level constant in `area.py` is unchanged. The new functions are additions only. [Runner](predictor_replay.py).

Verification at commit `b518774`: **295 gapmap tests passed in 151.34 s**, including all 27 unchanged phase-1 rule tests and 11 new phase-2 tests; **312 residual tests passed** and **460 reconstruct tests passed**. The new functions were developed test-first (missing-function failures were observed before implementation). Reconstruct used the parent repository's pre-existing environment, this worktree's source paths, and a writable `TLDEXTRACT_CACHE` under `.uv-cache`; no dependency or reconstruct code was changed. `git diff --check` passes. The orchestrator committed this result as `b518774`. The figure in [report.json](report.json) reads its numbers from `phase1_controls.json`, already committed in `14cbdab`; the report also includes all phase-2 candidate associations, area spreads, per-area means and L7.3 results from the new replay files.

## Citation review performed here

I checked every citation myself against the local source; no Claude citation-verifier subagent was spawned. There are no external literature citations to resolve and no external empirical claims requiring a network lookup. The checks covered:

- Every table and quoted correlation, count, range and pass flag against the full-precision replay JSON and the implementing code, including undefined `k_step` and v2's admissibility note.
- The phase-1 control against its committed artifact; the synthetic claim against its separately labelled output, specification hash and fixture generator.
- The ineligible-judge qualification against qwen's primary `l73.json`, and HYP selection against `record.categorize`; no new score removes that inherited selection dependence.
- The two fallback choices, wave-3 prerequisite and decision handoff against the I12 prompt and implementation queue; DS7 is described as an investigation, not as successful feature recovery.
- The formula and mean-aggregation claims against the new functions and tests; the historical I6 comparison is restricted to its planner partition, not predictive accuracy.
- The retained rule section against the original commit and its linked `lenses.py` definitions; all local links resolve.

No unsupported citation remained after this self-check. The empirical result does not validate E-CTA, demonstrate a density-baseline tie, license a judge, or resolve the owner choice.

## Handoff and lesson

Analysis is complete; the owner decision above remains open. The implementation queue records this outcome. `PROGRESS.md` is unchanged because no programme-level NOW status or E-CTA/MS2 owner decision has changed. The new [lesson](../../docs/lessons.md) records that requiring a defined nuisance correlation on a constant real covariate makes acceptance impossible, even when a balanced synthetic positive passes. No committed rule was amended to hide that problem.
