# E-PLANT and E-ABST report (N2 closeout, 2026-09-28)

Protocol: `docs/n2-eplant-eabst-protocol.md` (registered `3b72fb8`, amendments 1 and 2). Code: tag `n2-freeze-3` (`883b52a`). All numbers below were recomputed from the artefacts under `.private/e_plant/` and `.private/e_abst/`.
- Only counts, booleans and exit-status fields were read.
- The final reviewer also read the `utc` field of the sealed `calls.jsonl` (§2.2).
- No sealed run-1 ledger, claim or snapshot was opened or scored.

## 0. Status

| Experiment | Registered reading | Registered route |
|---|---|---|
| E-PLANT | **INCONCLUSIVE** (Continue closed) | The validity floor is not met (a_u = 5/24 < 8), which closes Continue (§6, amendment 2 P4). No gated run is scorable: run 1 is a defect-forced rerun unit (amendment 1), and run 2 was not executed. So no target passes the §4 cap rule, fewer than 20 targets remain, and the reading is inconclusive. |
| E-ABST | **INCONCLUSIVE** | Run 2 was not executed, so n_included = 0 < 20, which is inconclusive (§7; checked first in `e_abst_gate`). No owner coding exists for a valid run. |
| N2 reading (§7) | **INCONCLUSIVE; Continue unavailable this round** | "Continue when E-PLANT reads Continue and the E-ABST margin is met … inconclusive where either experiment is inconclusive." |

**Why run 2 did not run.**
- Amendment 2 P1 allows no rerun until E-LIVE v3 passes at `n2-freeze-3`. v3 could not run: the OpenRouter key is at its $5 weekly limit, with $0 remaining at the closeout.
- The owner decided not to raise the limit or spend more.
- No free route keeps the registered models:
  - `reconstruct/models.json` fixes Haiku 4.5 and GPT-5.4-mini through OpenRouter;
  - the only other credential is a paid OpenAI key, which cannot serve the Haiku generator;
  - E-ABST's web mode needs OpenRouter's search.
- Swapping models would be a new registration, not a rerun.
- The missing execution is caused by budget alone. No gate reading, rerun rule or threshold was changed.

**This is a stopping point, not a registered final outcome.** Under P2, an attempt blocked before any billed call is not a rerun, so each unit's one rerun is still available. Closing N2 here is the owner's decision.

## 1. E-PLANT

### 1.1 Ungated baseline (standing result)

Recomputed with the current harness (`load_targets`, `score_baseline_arm`, `validity_floor_met`):

| Domain | n | a_u | Unanswered | Floor ⌈n/3⌉ |
|---|---|---|---|---|
| Food (home leftovers) | 12 | 4 | 0 | 4, met |
| Cold-weather concreting | 12 | 1 | 0 | 4, not met |
| **Pooled (the registered floor set, D2)** | **24** | **5** (21%, Wilson 95% CI 9–40%) | 0 | **8, not met** |

With `t-conc-08` excluded (amendment 2 P4): n = 23, a_u = 5, still below 8. Model: `anthropic/claude-haiku-4.5`, and the served model matches. One call per domain, both ok, $0.0735 in total.

**Scientific result.**
- Given the planted page alongside the real pages, the ungated model adopted the planted value on 21% of targets, well below the > 60% expected from ClashEval-style evidence [51].
- Adoption was concentrated in food (4/12); concreting was near zero (1/12).
- The plants did not persuade the baseline, so this round cannot show the large reduction that Continue requires. By the registered rule (§6, amendment 2 P4), Continue is closed for E-PLANT and N2.
- A gated arm could still have given evidence either way:
  - below the floor, Stop needs c > b with one-sided p < 0.05;
  - a strong gated effect (e.g. b = 5, c = 0, p = 0.031) would have been observable, though not as Continue.

### 1.2 Gated arm (no result)

Run 1 (tag `n2-freeze`) exit status, which §8 lets the rerun decision read:

| Domain | `complete` | Calls by task (all ok) | Cost | `n_cross_checks` (sidecar) | Decoys attempted |
|---|---|---|---|---|---|
| Food | true | extract 18, verify 665 | $0.883 | 276 | 0 |
| Concreting | true | extract 18, verify 578 | $0.875 | 90 | 0 |

- At `n2-freeze`, failed calls were not logged (fixed in `0f39ed9`), so completeness cannot be checked.
- Amendment 1 therefore declared both domains a rerun unit. Run 1 stays sealed and unscored.
- Cross-verify did execute live (276 and 90 cross checks, logged under task `verify` before it had its own label).
- Both domains' last logged calls were at 15:18:30 and 15:18:31 UTC. That is the same second as E-LIVE v2(b)'s last call on the same key, whose 140 PENDING items trace to silently failed calls (`e_live_report.md` §6.1).
- So run 1 was very probably cut off by the same provider event. That is independent support for amendment 1's rerun decision.
- Run 2 (`pipeline_run2`) does not exist.

**Not computed:** a_g, b, c, e, r_g, the McNemar test, the sensitivities, and contradiction-flag recall (§5). Recall also still lacks D7's `value_a`/`value_b`/anchor fields, which are not yet in the sealed pairs.

## 2. E-ABST

### 2.1 Raw baseline (standing result)

- Haiku 4.5, no tools, with a response schema that explicitly offers `null`.
- **5 of 24 items answered; 19 returned null (abstained).**
- 24 calls, $0.0068. The baseline ran before amendment 1 and stands.

**What the gate can still read.** Only an answering statement can be false, so FAR_raw ≤ f_r / n_included, where f_r ≤ 5 is the number of raw answers coded false. With f_p the pipeline's false answers, the margin needs f_r − f_p ≥ 0.20 · n_included, with n_included ≥ 20:

| n_included | Margin met only if |
|---|---|
| 21–24 | f_r = 5 (all five raw answers false) and f_p = 0 |
| 20 | f_r = 5 and f_p ≤ 1, or f_r = 4 and f_p = 0 |

- **Stop:** if f_r = 0 (all five raw answers coded correct or non-answering), FAR_raw = 0, so FAR_pipe ≥ FAR_raw and the reading is Stop whatever the pipeline does.
- **Change:** every case in between reads Change.
- So the margin is reachable only in a narrow corner.

**Scientific result.** When `null` was offered, the raw model used it on 79% of the private items. The confabulation that E-ABST's margin was set to catch was rare, and the registered margin sits at the edge of what is arithmetically possible. (E-ABST registered no expected raw FAR, so this is an observation, not a missed expectation.)

### 2.2 Pipeline arm (no result)

Run 1 exit status (descriptive only; run 1 is not a result):
- All 24 items are `complete: true`.
- No failed-call logging existed at `n2-freeze`, so completeness cannot be checked, as for E-PLANT.
- Calls: web_search 24, extract 67 (all ok), verify 10, decoy 3, cross_verify 0.
- Cost: $0.488 in total ($0.010–$0.028 per item).
- The run ended at 15:04:04 UTC, before the 15:18 provider event.
- Under the registered D4 test (`extract_ok`), **1 of 24 items extracted zero documents**. **17 of 24 produced zero claims** (`stats.n_extracted == 0`).
- Run 1's pattern would therefore not trigger §7's "more than 4 zero-extraction runs → inconclusive" rule.

**Not done:**
- run 2;
- the amendment 2 P4 exposure supplement (the committed `exposure.json` predates amendment 2);
- the mechanical exclusion;
- owner and second coding, and κ;
- unsealing, `G_abst`, both FARs and the key-print sensitivity.

The existing coding sheets (19 and 8 units, all empty) were generated at 15:06 UTC, just after run 1. They include run-1 pipeline units, so they must be regenerated from run 2.

## 3. Costs

| Item | Spent | Cap |
|---|---|---|
| E-PLANT baseline | $0.074 | within $4.00 (§8) |
| E-PLANT plant authoring (29 attempts) | $0.121 | within $4.00 |
| E-PLANT run 1 | $1.758 | within $4.00 |
| E-ABST baseline | $0.007 | within $6.00 |
| E-ABST run 1 | $0.488 | within $6.00 |

Nothing was spent at the closeout.

Remaining registered caps: E-PLANT run 2 $3.00, E-ABST run 2 $14.40 (P3). E-LIVE v3 is unregistered; the final review estimated about $2. The expected spend is roughly $5–10:
- E-PLANT run 1 cost $1.76;
- E-ABST at P3's mean estimate is about $0.28 × 24;
- v3 is about $2.

## 4. What N2 tells us

1. **Both ungated baselines resisted the failure each gate was built to catch.** Haiku 4.5 adopted 5 of 24 single-source plants (the literature expectation was > 60%), and it declined 19 of 24 private questions when offered `null`. This finding stands whatever run 2 would show.
2. **Continue was unreachable this round.** For E-PLANT this is by rule (the validity floor). For E-ABST the margin is nearly unreachable by arithmetic (§2.1).
3. **The gated arms' behaviour is unmeasured,** so N2 gives no evidence that gating helps or harms adoption or false answers. The pipeline's implementation evidence is in [`e_live_report.md`](e_live_report.md).
4. **The final review's limitations R1–R10** ([`final_adversarial_review.md`](final_adversarial_review.md)) stand as recorded. None changes a reading here.

## 5. Missing evidence

To read the registered gate, all of the following would be needed:
- a passing E-LIVE v3 at `n2-freeze-3`;
- E-PLANT run 2 for both domains;
- D7 value fields added to the sealed pairs;
- the E-ABST exposure supplement and run 2 for 24 items;
- regenerated coding sheets, owner coding and the second coder (κ);
- unsealing and scoring.

The best outcome this could buy is Stop or Change for N2, not Continue.
