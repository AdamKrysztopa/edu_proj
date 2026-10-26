# Implement queue: buildable now (2026-10-24)

This queue merges three passes ([C] Claude, [X] Codex, [R2] an adversarial second-round review; see [coverage-audit.md](coverage-audit.md); finding numbers below refer to it).

**Wave 1 report:** https://claude.ai/artifact/2bdygzaVgPF6LE9DoaNDLc (figures, decisions, what wave 2 must settle).

**Wave 2 report:** https://claude.ai/artifact/M1NDPick23TyXjJ1gPQis1 (figures, decisions, what wave 3 must settle; reviewed against the sources by Codex, 30 fixes applied).

**Wave 3 report:** https://claude.ai/artifact/3x2P5bJ8RKBBQ9KMw3Dnce (I4, I8, I10; figures, decisions, what wave 4 must settle; reviewed against the sources by Codex, 13 findings, all addressed).

**Wave 4 report:** https://claude.ai/artifact/Naa5KmhJHbUq3TZenVBHXX (DS9–DS12; figures, owner decisions, what the next wave must settle; reviewed against the sources by Codex, 24 findings, all addressed).

**Programme synthesis, waves 1–4:** https://claude.ai/artifact/XwWjHGbKjDuBgyKX4BEME9 (what we achieved and what is not shown, N0–N9 status, the route to the first N3 reading, candidate products and their licensing tests, four owner decisions due; reviewed against the sources by Codex, 11 findings, all applied; passed a cold-read test). Polish version, translated by Codex gpt-5.6-sol: https://claude.ai/artifact/Xxd7uctiATokr9C4TPNUF7

"Ready" means no gold, no participants and no unmet dependency. The only blockers allowed are the owner decisions each item names. Every item ends in a result that a decision reads (R13).

**Order.** By technical merit on the critical path:
1. Make the MS1 instrument discriminate.
2. Settle closure (Phase 0, MS1).
3. Prepare the MS2 freeze and the gold test.

**Rules for every item.**
- Write to a separate output directory, never over `research/n3/<domain>/`. The manifest SHA pins and the byte-identical replay claim must survive (finding 18).
- Before a parser, filter or admissibility rule is changed, replay it on the committed artefacts and report what it flips (`docs/lessons.md`).
- A plan that registers paid runs lists the sum of their caps next to the key's headroom: $14.99 of $15/week on 2026-10-24 (L7.2).
- Show every gate or control discriminates before using it (L7.3).

## I1. Rebuild the closure control so it can discriminate (recommended first) [C+X+R2]
- **What.** In a new script or module beside `gapmap/src/gapmap/checks.py`, leaving the committed maps untouched:
  1. **Parser precondition.** Return undecided unless at least one of `states` / `partially` is present and every present key is a list (finding 11). Add tests for the empty object, a wrong type, a missing key and states-only. Replay result: 0 committed replies change state; the 16 states-only replies stay valid.
  2. **Equal caps.** Both arms take the same number of non-seed sentences, so the seed no longer crowds the control out (finding 6). Report the truncation counts before and after.
  3. **Fixed donor pairing.** Make it independent of `CONFIG_SHA256`, for example by tie-breaking on seed claim ids (finding 7).
  4. **A seed-free comparison**, restricted to pairs where both arms are non-empty (finding 9).
  5. **Both splits reported**: closed-or-partial, and closed only (finding 8).
  6. **Discrimination proof** (L7.3): a planted positive, with the element stated in an other-source sentence, must fire; a length-matched stand-in must not.
- **Run.** Local qwen (`--judge ollama`, $0).
- **Result → decision.** The share of pairs that can discriminate, and the own − control difference on the seed-free, equal-cap pairs, with a seed-resampled interval. Together they decide whether this control is the MS1 instrument, needs narrowing, or must be replaced before any human codes 210 pools against it.
- **Why first.** MS1 is the first gate in both programmes. As built, the arms are uneven in 80 of 153 pairs, the donor is tied in 53, and the own-arm rate is 1.0 in 11 of 14 cells (`report/sections/10_n3.tex:113-114`). **What would change it:** the owner adopting `REORIENTATION.md` §22 instead of the report's MS1. Then I3 (R4, fatal-class) leads.
- **Status 2026-10-24: done.** control2 built. Primary (own arm seed-free, donor arm still carrying the donor's seed at `control2.py:123`; closed): PLC +0.04 [−0.09, +0.17], uninformative; GDPR v1 +0.26 [+0.11, +0.39], but a length-only judge also passes (+0.28 [+0.06, +0.49]). Note `research/n3_control/RESULT.md`; commit 535d7b5.
- **I1b (owner-requested judge swap), 2026-10-24.** Same pairs with `gpt-5.6-luna` (OpenAI's nano-equivalent tier): no domain separates on the primary (PLC +0.11 [−0.06, +0.30], GDPR v1 +0.10 [−0.06, +0.25]); kappa with qwen 0.14 pooled. Real-judge L7.3 fails for both judges: Luna's planted positive does not fire; qwen's random-letter stand-in fires. $0.342. Note `research/n3_control_luna/RESULT.md`; commit 2f65c06.
- **Owner decision 2026-10-24.** Fix control2's donor pool first: drop the donor's own seed sentences from the donor arm (`control2.py:123`). Re-run L7.3 through real judges with plain-text plants. Only then swap judges, with a top-tier arm in I2. The top-tier arm is `gpt-6.1-sol` at effort high, under ADR 0009 (see the checklist below).
- **I1c (donor fix + gpt-6.1-sol), 2026-10-24.**
  - **Fix.** Both arms now drop both candidates' seed sources. 140 of 153 pairs can still discriminate, against 149 before; the best reachable difference is 0.92, against 0.97. I1's control arms had carried the donor's seed in 77 pairs, and its own arms in 58.
  - **L7.3.** Three plain-text plants, with random-letter and length-matched stand-ins. Sol passes, identically in two runs. Qwen fails: 8 of 12 stand-ins close the own arm. Luna passed run 1 but failed run 2 on identical prompts.
  - **Primary (sol).** PLC +0.13 [−0.02, +0.28], uninformative. GDPR v1 +0.23 [+0.07, +0.39], discriminates. The length-only judge passes nowhere.
  - **ADR 0009.** No reading counts: the guard arm, qwen, is ineligible.
  - **Owner decision 2026-10-24.** Replace the guard arm: wave 2 screens the local `qwen2.5-coder:32b-instruct-q4_K_M` on `l73.py` first ($0), then re-runs the three domains beside sol's cached run; if it fails, a hosted non-OpenAI, non-Anthropic model on OpenRouter is screened next, after an OpenRouter judge backend is added.
  - **Owner decision 2026-10-24, superseding the line above.** coder32 is dropped, not deferred: it is not runnable on this laptop (24 GB RAM, 76 s per trivial reply, first L7.3 run hung about 4 h with nothing saved), and no hosted coder32 run follows. No guard arm is eligible; choosing one is open.
  - **Cost.** OpenAI spend $5.03 of one $10 cap, including the superseded run 1 ($2.55).
  - Note `research/n3_control_v3/RESULT.md`; commit fccf477.
  - **Re-reading, 2026-10-26 (D1b plan §1.5; no N3 rule changed).** control2 is topicality-biased: the own arm is ranked by candidate *i*'s probe and the donor arm by *j*'s (`gapmap/src/gapmap/control2.py:120,128-132`). A lexical-overlap stand-in passes it at +0.68 (PLC) and +0.46 (GDPR v1), above sol's +0.13 and +0.23 (stand-in values computed in session for plan §1.5 and not saved as a file; sol's from `research/n3_control_v3/RESULT.md`). So sol's GDPR v1 reading is not protected against an "is on topic" judge, and control2 cannot certify a judge on its own. A topicality-controlled check (D1b's G2: an on-topic non-element N beside the planted element P) should run before any control2 reading counts for MS1.

## Before E-CTA registration (methods-critic, 2026-10-24)

The four owner decisions are recorded but were not ready to register. The critic's verdict: "Would I run this as designed: no." Owner questions are marked (owner).
- [x] (owner) §1 falsifier part 2: retired before any gold, with §14, RQ-D, §17, R4, N5 and Q8 amended to match. The N3 programme gate is H1's only falsifier.
- [x] (owner) Sullivan 2014: excluded as a test gold, and kept as the descriptive recall comparator. Primary set is now DS1 ranks 2–4.
- [x] (owner) Top-tier judge: `gpt-6.1-sol`, reasoning effort high ($2 / $10 per 1M tokens; OpenAI model page, read 2026-10-24), run beside qwen. ADR 0009 supersedes 0008's family rule, allowing a same-family judge only as a parallel arm; a reading counts only where both arms agree. Promoted to active by the owner on 2026-10-24.
- [x] (owner) Terminal branch: if still inconclusive after the fallback gold, E-CTA gives no verdict and E-OSS decides. If E-OSS is also inconclusive, H1 counts as not shown and the project pivots to H3.
- [x] (owner) Pooling, Stop multiplicity and look boundary: DS3's package, set 2026-10-24 (`REORIENTATION.md` §22).
- [ ] I5 (wave 2) replaces the δ row's figures at the expected imbalance. Include L7.3: a planted 0.20 gain Continues, area size alone does not. A pooled minority class of 25 is unreachable at 3 × 20 areas with 79% missed.
- [x] `control2.verdict` (`control2.py:198-201`) returns design-wrong when the length stand-in's CI lower bound is above 0. A judge failing either real-judge L7.3 arm is ineligible. Recompute the best reachable difference after the donor fix. Use more than one planted pair.
- [x] ADR 0009: control2 refuses a live same-family judge without an other-family `--parallel-arm` on the same ledger and pairs (`test_a_live_same_family_judge_runs_only_beside_an_other_family_arm_on_the_same_pairs`); a control2 cache miss names `--judge openai` for an OpenAI model; the replay rule's wording names both flags.
- [x] Before the `gpt-6.1-sol` run: add its price to `OPENAI_PRICES_PER_MTOK` (`judge.py:67`, taken from the model page), and add a `--reasoning-effort` flag to control2 (the default is "medium", `judge.py:86`).
- [x] (owner) If E-OSS cannot run, an inconclusive E-CTA means H1 is not shown, and the project pivots to H3 (2026-10-24).
- [x] L7.2 record, 2026-10-24. Caps: I1c qwen $0. I1c Luna plus sol on the OpenAI key: the owner set $10 in total, but the code enforces `--max-usd` per judge instance (`judge.py:86-110`), so the two arms' caps must sum to at most $10. The OpenAI balance, as the owner stated it on 2026-10-24: $20 or more, not a dated account read. OpenRouter: I2 Jev about $0.01; `scripts/key_headroom.py --need 0.01` gave limit 15, remaining 14.99.
- [ ] Bound `max_completion_tokens` against Luna's measured tokens (about 255k in, 240k out) before any further top-tier run.
- [x] Sealed presence check built: `uv run --directory residual python -m residual.presence <gold file>` prints one line and never item text: "list present, n rows, sha256 …", "list empty", "list absent" or "list unreadable (<error type>)" (`residual/src/residual/presence.py`, 10 tests). Run it on each primary gold before the freeze. Any fallback replacement happens before another gold's result is seen.
- [x] (owner) Okoli: the gold is the 42-cue inventory in 5 stated types (2026-10-24). A dedup rule is needed only if the printed list has duplicates; check at the presence check.
- [ ] Okoli: pre-register the mapping unit from cue to area.
- [x] (owner) Okoli stays a primary gold by choice, although its cue-only score under DS1's rule is 3 (about rank 9) (2026-10-24).
- [x] (owner) If E-CTA cannot run at all, E-OSS alone decides under the same terminal rule (2026-10-24).
- [x] (owner) The central hypothesis (`REORIENTATION.md` §17) is reworded to "locates the areas that reconstruction misses", matching the label (2026-10-24).
- [x] (owner) The label is "area missed by the reconstruction", with no "residual-present" secondary (2026-10-24). "Troubleshooting" is dropped from the N3 row, and Chao & Salvendy is marked as outside the primary and fallback sets in the E-CTA row.
- [x] Pre-registration input: DS1's abstract-exposure log (`research/ds1-gold-availability.md` § Deviations; Canopy, rank 13; Craig, Cioffi, Mumaw, Kancler; Harris-Thompson 2006, which named its cue categories) goes into the pre-registration of any of those golds.
- [ ] Ordering: the control decision (I1c) passes before any primary domain's partition is frozen.
- [ ] Re-judge the gap map's own closure (`research/n3/*/closure_judgements.json`, qwen 7b, which failed L7.3) with sol plus an eligible guard arm (none chosen: coder32 dropped 2026-10-24) before the MS2 freeze; the HYP pool and the rubric's P term depend on it (methods-critic, 2026-10-24). OpenAI spend: the owner sets the cap (wave 3).
- [x] L7.2 record, wave 2, 2026-10-24. The only paid caps are I2's Jev runs, `--max-usd 0.10` on OpenRouter; `scripts/key_headroom.py` gave limit 15, remaining 14.99. No OpenAI calls: sol's I1c run is cached ($4.97 of the owner's $10 OpenAI cap stays unspent). Every other item is $0 (local qwen or no model).
- [ ] Add `reconstruct/src/reconstruct/evidence.py` (`classify_source`, the boundary host rules) to the freeze manifest's file set before gold; today the manifest hashes only `admission.py` from `reconstruct/` (DS7 post-merge citation check, 2026-10-24).

## I2. Jev on the rebuilt control [C+X+R2]
- **Status 2026-10-24: done (rewritten as the guard-judge item).** coder32: dropped (not runnable on local hardware: 24 GB RAM, 76 s per trivial reply, first L7.3 run hung about 4 h with nothing saved; owner's words). ADR 0009 still has no eligible guard arm, so no sol reading counts yet; the choice of guard is open. Jev passes L7.3 twice, identically, but is far from sol: GDPR v1 +0.14 [−0.05, +0.31] against sol's noise-inflated +0.23 [+0.05, +0.38], κ 0.41 pooled. So judge substitution is no longer the closure repair. Sol's GDPR v1 lower bound survives its judge noise. Jev spend $0.047 of the $0.10 cap; no OpenAI calls. Note `research/n3_control_v3/GUARD.md`; commit 6e8b6dd.
- **What.** Pass Jev as the judge object. Every arm the existing control issues is already cached (542 Jev calls). Only I1's seed-free and equal-cap arms need live calls: at most about 153 prompts × $0.00007 ≈ $0.01. Missing cache entries fail loudly.
- **Result → decision.** Jev's own, control and seed-free rates per lens and split. If they tie, stop treating judge substitution as the closure repair (`research/spikes/jev/RESULTS.md`, next step). If they separate, Jev is a V1 panel candidate, subject to ADR 0008 (finding 10).
- **Cost.** About $0.01.

## I3. N5 identifiability: zero catchability and planted dependence (parallel with I1–I2) [C+X+R2]
- **Status 2026-10-24:** done (SYNTHETIC). Text occasions identify only the written universe. τ = 50% on written items is reachable only at ρ ≈ 0, low heterogeneity and N ≈ 200 (0 of 432 DS4 cells at N = 50); τ = 25% is reachable in no cell of 5508. The §22 raw-count form lets errors cancel, and the f1 stand-in passes about half the achievable cells. R4 goes to the owner with both readings. Note `research/n5_sim/RESULT.md`; branch `i3-residual-identifiability`.
- **Owner decision 2026-10-24:** drop the residual size as an objective (DS4 §6 option 2, on I3's N = 50 written-only reading, over DS4's recommended re-specification). R4 applied without its trigger firing; N5's Stop applied (`REORIENTATION.md` §22).
- **What.**
  - Chao1, jackknife, Mh and Lincoln–Petersen go in a **new** `residual/` module. `residual.py` is inside the frozen semantics hash (finding 17).
  - Build synthetic universes that share text-capture histories but differ in their counts of never-written items, then add dependence and heterogeneity.
  - Label everything `SYNTHETIC` and store it apart (§12, use 1).
- **Result → decision.** Identifiability and error for each estimator. These decide:
  - whether the N5 estimand must be the *written* universe;
  - which estimator and tolerance N5 pre-registers.

  The result does not read N5's gate. If nothing is identifiable, raise R4 ("drop the residual as an objective") with the owner before any gold.
- **Cost.** $0.

## I4. V1 closure-study kit (Phase 0, gate MS1) [C, amended by R2]
- **What.**
  1. **Codebook** with anchors for closed / partial / open per lens. GDPR v2's 48 firings are the training set.
  2. **Blinded exporter** over the rebuilt control's pools, frozen **before** any config change. The report's count is 105 firings with a donor, 210 pools, 19 of them identical and coded once (`17_validation.tex:178-182`).
  3. **Analysis**:
     - weighted κ / ordinal α;
     - the MS1 split fixed in advance;
     - seed-claim cluster resampling;
     - the judge margin, with its **sign corrected** (finding 2).

     Copy `instrument/src/probe_code/agreement.py` into `residual/` per decision 0006 rather than writing fresh code.
  4. **Retrieval-recall sampler**: 50 firings, full-snapshot search.
  5. **Retrieval-stability check** under a frozen corpus, before any human time is spent (`26_risks.tex:133-137`).
  6. **Pre-registration**, reviewed by `methods-critic` and hash-committed.
- **Owner decisions.**
  - The blind second coder.
  - The external gate reader, which would be a second human input (finding 5).
  - Which programme gate governs (finding 3).
  - Whether "no new software" in Phase 0 is amended (finding 4).
  - The judge panel against ADR 0008 (finding 10).
  - The out-of-sample domain. Its N2 run is effectively E-LIVE v3. It needs the config frozen first and should be registered as such (finding 15). Cost about $0.5–1, under amendment 2 P1.
- **Result → decision.** MS1: continue, or stop the automated absence check and pivot (report §26).

## I5. Gate reachability, §14.3 baselines and AUROC code [X+R2]
- **What.** Provider-neutral analysis in `residual/`. No AUROC or baseline code exists today.
  - Specify, and build where the data allow, the §14.3 baselines: random, the naive type rule, verbalised confidence, area size, retrieval-support density, corpus frequency, plain-LLM, and the type prior. Date the model-based ones.
  - Enumerate N2's reachable decision regions.
  - Simulate N3 with ties, clustered areas, strongest-baseline selection inside each resample, and 1–3 golds of about 20 areas.
  - Check that "gold items per area" leaves Continue reachable (finding 20).
- **Result → decision.** Continue / Stop / inconclusive frequencies per design, which inform δ, minimum areas and multiplicity once DS3 supplies the inputs; and whether an E-PLANT floor amendment is worth registering.
- **Cost.** $0.
- **Status 2026-10-24: done (SYNTHETIC; N2 part exact). Owner decisions taken 2026-10-24.**
  - **Owner decisions 2026-10-24.** (1) The minimum design is keyed to r measured on the pre-gold partition: smallest r ≥ 0.6 needs 5 golds × 20 areas or 3 × 30; 0.3 to 0.6 needs 5 × 30; below 0.3 E-CTA reads inconclusive by design; every gold needs ≥ 5 clusters plus one fallback gold. (2) K gains a pre-registered rank mean of K, "gold items per area" is dropped, and c = 1.85 for both Continue and Stop. (3) Variance: analytic clustered DeLong primary, cluster bootstrap (B = 2,000) as co-gate under DS3's agreement rule. (4) No E-PLANT floor amendment is registered.
  - At the set rules, 16/4 and map–baseline correlation r = 0.6, a gain of 0.20 continues with P = 0.622 at 3 × 20 areas, 0.855 at 5 × 20 and 0.892 at 3 × 30. A null stops with P = 0.44–0.48; P ≥ 0.8 needs about 80 areas per gold.
  - The planted positive misses 0.8 in 70 of 552 cells at DS3's minority floor of 25, almost all at r = 0.3. So the proposed minimum design is keyed to r measured before gold.
  - Random and size stand-ins reach P(Continue) ≤ 0.008. A rank mean of K reaches 0.152 at r = 0: add it to K.
  - False Continue ≤ 0.045 at c = 1.85. False Stop at a gain of exactly δ reaches 0.07 in small designs.
  - Gold items per area cuts a 0.82 map's P(Continue) from 0.632 to 0.186: exclude it.
  - E-PLANT: Continue unreachable (best Change); no floor amendment proposed.
  - Note `research/gate_sim/RESULT.md`; branch `i5-gate-simulation`.

## I6. `area_features()`, uncapped candidates and an area score [C+X]
- **Status 2026-10-24: done.** The score trips: on PLC, ρ = 0.96 with `k_topic` over 24 merged HYPs, and the check discriminates. So change the predictor before MS2. The dead features stay dead, so the E-CTA pre-registration tests size + density + type plus the lens signal only. The caps hide 15 of PLC's 24 candidates. Note: `research/area_score/RESULT.md`. Threshold pre-stated in `ef5131e`; result on branch `i6-area-features`.
- **What.**
  - A pure, deterministic `area_features()` (a new module in `residual/`, with no new field).
  - Expose every candidate before the display caps (`gapmap/src/gapmap/rank.py:98-108`).
  - Score each area by max or noisy-OR, with an `--areas` input.
  - Report the score's association with `k_topic`, size and density *within* the HYP candidates, not pooled with RG records (finding 19). Do not call the output a calibrated `P(missing)`.
- **Result → decision.** If the score is close to a monotone function of source count or size (threshold set before computing), change the predictor before MS2.
- **Cost.** $0.

## I12. Replace the gap-map predictor (new, from I6)
- **Status 2026-10-24: analysis complete; owner decided 2026-10-24.** Neither of two replacements passes the fixed screen: both pass the lens/length check, but PLC `k_step` is constant and random rejection is 87.95% (required 95%). Recommend deferring E-CTA until an informative feature/pool is available; the lens-reference fallback remains an explicit owner option. Note: `research/area_score/PREDICTOR.md`; report: `research/area_score/report.json`. Rules commit: `14cbdab`; result commit: pending orchestrator (changes uncommitted).
  - **Owner decision 2026-10-24.** I7 freezes the fixed lens reference with mean aggregation. Before the freeze, the rules in `14cbdab` are rerun on each gold domain's pre-gold partition, beside I5's r measurement; if that rerun also fails the noise screen, E-CTA is deferred.
- **What.** Two or three predictors that carry the lens signal net of source count, an area aggregate that does not saturate, and the I6 trip rule plus a within-`k_topic`-stratum test, pre-stated and committed before any association. Prompt: `docs/plans/prompts/I12-predictor-replacement.md`.
- **Result → decision.** The predictor I7 freezes (owner decision). If none passes: pre-register the lens signal and accept a possible tie with the density baseline. Owner decision 2026-10-24: the fixed lens reference (mean aggregation) is frozen, re-screened on each gold domain's pre-gold partition before the freeze; E-CTA is deferred only if that re-screen fails.
- **Cost.** $0.

## I7. Freeze manifest and historical-admission fixtures [X]
- **Status 2026-10-24: done (mechanism only, no value frozen).** `gapmap.manifest` hashes 37 files plus the config values (after the wave 2 merge). `--require-manifest` is on `gapmap` and `gapmap.control2`. Mutation test: 40/40 refused, 2/2 outside edits accepted. `reconstruct.admission.admit`: 17/17 plants as planted. Replay: 0/80 committed E-LIVE sources admissible at a 1994 gold date. The committed manifest (`d38a1720…`) is incomplete by design: the 3 freeze files (partition, eligible golds, closure arms) are missing. Note `research/freeze_manifest/RESULT.md`; branch `i7-freeze-manifest`.
- **What.**
  - A manifest that hashes the predictor code, judge prompts and model ID, configuration, partition and eligible-gold list, and refuses any run that differs from it (finding 13).
  - Fixtures that reject future-dated, undated, `Last-Modified`-only and blocklisted documents.
  - Build it after I1 decouples donor pairing from the config. Freezing the *values* waits for MS1 and I6.
- **Result → decision.** Mutation-detection and temporal-leakage results, showing whether the machinery can hold a pre-registration boundary.
- **Cost.** $0.

## I8. Admissibility as code (Phase 1, V0) [X, reordered by R2]
- **What.** N2 sets `n3_input` only when every located extraction has a verdict, cross-verify and the decoys ran, and no call failed. N3 refuses a missing sidecar. It applies to **new** runs. For legacy sidecars that predate the fields, record a "legacy" flag; do not refuse them silently (finding 12).
- **Result → decision.** The admissible share of the runs made after the freeze, which is the MS2 admissibility rule.
- **Cost.** $0.

## I9. Provenance fixes already specified [R2]
- **Status 2026-10-24: done; continue to I4.** All four fixes fire on planted positives and not on stand-ins. On the committed runs: 0 slots change status, contradictions 1 → 1, `verify_run` 0 → 0 problems, 1 of 207 GDPR v2 SUPPORTS lost to the 5-word quote floor. R3 withholds 242 of 6,114 GDPR v2 cross-verify pairs. Half are Art. 35 quoted by the ICO or WP248, and half are their own commentary (the cost of the two-direction test). Only 1 of 404 calls changes, because no committed run ever ran cross-verify. Note `research/n2/provenance_fixes.md`; branch `i9-provenance-fixes`.
- **Owner decision 2026-10-24:** keep the two-direction R3 copy test.
- **What.** Implement the fixes written in `research/n2/final_adversarial_review.md`:
  - R3: spans tested verbatim against the claim's own sources, robust to whitespace and case;
  - R4: scope-flagged REFUTES reported separately;
  - R9: digest recompute in `verify_run`;
  - plus a minimum length for `quote_in_span` (`reconstruct/src/reconstruct/evidence.py:90-95`).
- **Result → decision.** Contradiction and coverage counts before and after on the committed runs. These decide whether the fixed pipeline is ready for the I4 domain run.
- **Cost.** $0.

## I10. A pre-gold corpus route [C, refocused by R2]
- **Owner, 2026-10-24 (DS5).** Assume no institutional subscription access through an EU research organisation. This closes the paywalled TDM route (Elsevier and Springer, 2–44% of each gold domain) for I10 and later work until such access is obtained. Use DS5's blocklist: cut-off at the earliest same-team disclosure, citing works blocked whatever their date.
- **What.** An N3-eligible local-corpus mode for scholarly full text that predates each gold. Today `--corpus` is hard-coded as not admissible (`reconstruct/src/reconstruct/run.py:657-658`). Add OpenAlex `to_publication_date` filtering, Wayback snapshots for web sources (relevant for Sullivan 2014), and `as_of` enforced at fetch.
- **Pilot.** One non-gold task, `--max-usd 1`.
- **Result → decision.** The dated full-text share. It sets the corpus floor and drops golds whose domain cannot reach it. Do this after DS1 and DS4.

## I11. N9 cost reconciliation [C+X]
- **Status (2026-10-24).** Done: 4,785 calls, $5.30, every run within $0.01 (the E-ABST exposure $0.029 is in no report table); 46% of spend went to runs with no usable result; I4's domain cap should be $2.50 (projection $1.64 to about $1.94). Note: `research/cost_ledger/RESULT.md`; branch `i11-cost-ledger`.
- **What.** Aggregate the committed call and sidecar costs, split by retries vs failures and by engineering vs evaluation. Report cost per verified claim and per candidate; the "validated item" figure stays unavailable.
- **Result.** It informs the I4 and I10 budgets. It has no gate.
- **Cost.** $0.

## D1. End-to-end demonstrator on dependence-forecastability (owner, 2026-10-25)

- **Owner decisions 2026-10-25** (synthesis session; recorded in `REORIENTATION.md` §22 on 2026-10-25):
  - The tool's five steps run once end to end, by the owner and Claude alone, with no hired people.
  - The domain is the owner's public repository https://github.com/AdamKrysztopa/dependence-forecastability. The owner acts as the expert in step 3.
  - Total cap $8, raised to $11 on 2026-10-25 (see below).
  - N3 stays paused with its registered rules unchanged (two non-owner coders, an external gate reader) until independent coders exist.
  - Also taken in that session: merge all seven wave 3–4 branches, wave 3 first; adopt DS8's E-OSS proposals.
- **Purpose (owner, 2026-10-25):** the demonstrator shows how the tool is meant to be used. It is an illustration, not a study. Sequence: demonstrator, then a POC at Warsaw University of Technology on a real course, then presentation, funding applications and partners. The formal machinery (pre-registration document, `methods-critic`, hash commit) is dropped. A light blind check stays (owner choice): 10 thin-area and 5 covered-area questions, shuffled, judged blind. The rule below is written down before the owner answers.
- **Decision rule** (written before the owner answers): Continue if the novelty rate of answers to gap questions exceeds that of covered questions by ≥ 0.30, with ≥ 5 of 10 gap answers new, read by two agreeing judges of different families; otherwise Change the gap map's ranking.
- **Discrimination** (L7.3, kept light): synthetic planted-positive, all-novel, all-copied and length-matched filler answers are run through the rule before the owner answers. The best case is reachable: 10 of 10 gap answers new against 0 of 5 covered gives a difference of 1.00, with an exact permutation p of 1/3003.
- **L7.2 record, 2026-10-25.** Caps: $1.50 (cheap arm), $4 (top-tier arm) and $1.50 (judges), $7 in all, under the owner's $8. The key has $13.94 of $15 left this week (`scripts/key_headroom.py`). Recheck before each live command.
- **Outside report (2026-10-25):** [English](https://claude.ai/artifact/QyyJivGPhJbJCuUwf2DD1E), [Polish](https://claude.ai/artifact/VUKdhJNRs2USo9G5KfymJz); all document links: `docs/artifacts.md`.
- **Outside sources (owner, 2026-10-25).** On the 16-doc corpus the gap map gave no hypotheses: all 16 docs share one independence key ("same domain-grouping key"), and `record.categorize` files an open gap as HYP only at k_topic >= 2, so all 27 open candidates became RG-SINGLE. The owner chose to add outside pages on the same methods (6 Wikipedia articles, 2 scikit-learn and 2 statsmodels reference pages; FPP3 refuses automated requests) rather than change the counting. The 16-doc arms are superseded: cheap complete ($0.71), top-tier stopped mid-verify ($1.90).
- **L7.2 record, revised 2026-10-25.** The owner raised the total cap to $11. Spent: $2.61. New caps: $1.50 (cheap arm), $5 (top-tier arm), $1.50 (judges), $8 in all, against $11.32 of $15 left on the key. Total D1 at most $10.61.
- **Budget-stop crash and rerun (owner, 2026-10-25).** On the 26-doc corpus the cheap arm hit its $1.50 cap inside cross-verification, a stage the one-key corpus never reached. Areas were added to the ledger only after that stage, so the Ledger refused assignments naming absent areas and the run died with no ledger.json ($1.50 lost). The top-tier arm was stopped at $2.87 before it could fail the same way. Fixed test-first in `reconstruct/src/reconstruct/run.py` (areas are rebuilt from assignments after any stop). The owner chose to rerun both arms; a cap hit now saves an incomplete but usable ledger.
- **L7.2 record, rerun, 2026-10-25.** Spent so far $6.98 ($2.61 on the 16-doc arms, $1.50 and $2.87 on the failed 26-doc arms). New caps: $1.50 (cheap), $4 (top-tier), $1 (judges), $6.50 in all, against $6.96 left on the key this week. D1 total at most about $13.48, over the $11 cap, accepted by the owner.
- **Label.** Exploratory: one expert, who also owns the design. Never evidence for RQ-B, and feeds no N3 gate.
- **Prompt:** [`prompts/D1-demonstrator.md`](prompts/D1-demonstrator.md).
- **Where it leads (owner, 2026-10-25): Warsaw University of Technology.** Once the demonstrator is built, the owner plans to run the project at Warsaw University of Technology. There, a sample of lecturers acts as experts (step 3) and a sample of students as learners (steps 4–5). That supplies what NOW cannot: real learners, real lecturers and, possibly, independent coders for N3/MS1. Preconditions before any participant is involved:
  - ethics approval and informed consent;
  - a host course and a named lecturer;
  - GDPR handling of student data;
  - cohort-level diagnosis only (EU AI Act Annex III, `REORIENTATION.md` §21).
  - If the course touches physics conservation, the §18.1 rule applies: anyone who has seen reconstructed conservation content is ineligible for a Track A role.
  - D1's outputs should be shaped so a lecturer can see them as the WUT pitch.

## D1b. Fix the gap map's ranking, then rerun D1 on fresh questions (owner, 2026-10-26)

- **Plan:** `docs/plans/gapmap-fix-and-d1-rerun.md`, approved 2026-10-26 after two `methods-critic` rounds. Owner decisions: criterion (b), LLM judges, advisory; total cap $6; no local models (the Mac crashed screening them), every non-OpenAI judge through OpenRouter.
- **Item 1, done: the fix.** The gap map's closure judge is selectable (`--judge ollama|openai|openrouter`, ADR 0009 parallel-arm guard); defaults and the `research/n3/` caches are unchanged. Judges are screened on G1 (N3's L7.3 fixtures) and G2 (topicality-controlled plants, owner-confirmed). gemma-4-31b-it passes both (G2 twice, under a disclosed post-hoc amendment to the R term, `b7cc35f`; raw R 0.15) and is the cheap arm. gpt-6.1-sol passes G1 and its first G2 gate run; the second required run was stopped at A, so it is not yet eligible. The real-data null (mismatched-evidence control) still flags the gemma maps (+0.125, +0.111) and cannot gate, since a lexical-overlap stand-in passes it on the cheap ledger (+0.208; +0.200 on top-tier).
- **Item 2, stopped at A: Change (owner, 2026-10-26).** Of 35 fresh topics, the cheap judge (gemma) left 7 open in every version against 23 closed; at most 3 matched pairs, floor 10. No questions were built or answered. Per plan §3.7, gap-map targeting is not a pilot claim; the PW lecturer and volunteer search may start as an elicitation-and-onboarding pilot without targeting. Note `research/d1b_rerun/RESULT.md`.
- **Cost.** $0.92 of $6: OpenRouter $0.62, OpenAI $0.29 (sol's checks, started before the Stop A count against the plan's order; lesson queued).
- **Open.** Targeting can be tested only on a corpus whose open side reaches 10 matched topics per arm; the rerun's rule, sheet builder, sealing, canaries and retest are built and tested for that (`research/d1b_rerun/`).

## Conditional: not ready yet

| Item | Waits for |
|---|---|
| E-SEAL (N8): the operation list (about $1, encrypted, never displayed); the K0 half needs registered early-K0 items | Owner go-ahead; secondary and non-gating |
| Deferred N2 reruns (about $19.40 in caps; sequential under amendment 2 P1) | I5 shows a reachable reading worth the spend |
| MS2 value freeze | MS1 (I4) and I6 |
| World B Git adapter | DS8 |
| N4 (E-MISC, E-DIST, E-KC); N7 (E-SYN) | DS9 licences |

## Housekeeping (no gate)
- Fix the stale text (findings 23–24), including the JEV `RESULTS.md` count and wording.
- Namespace the hypotheses in plans that cite both documents.
- Owner: decision 0008, reconciled with V1's panel.
