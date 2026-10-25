# I1: Rebuild the closure control so it can discriminate

**Branch:** `i1-closure-control`
**Outputs:** code in a new module `gapmap/src/gapmap/control2.py` with tests in `gapmap/tests/test_control2.py`; results under `research/n3_control/`.
**Cost:** $0. The judge is local Ollama `qwen2.5:7b-instruct`.

## Context
- Read `docs/plans/implement-queue.md` § I1 and `docs/plans/coverage-audit.md` findings 6–9, 11 and 18.
- The current control is `gapmap/src/gapmap/checks.py:156-223` (`mismatched_evidence_control`).
- Retrieval is `gapmap/src/gapmap/semantic.py:64-101`. `retrieve()` puts the seed's sentences inside `JUDGE_A_CAP = 8`.
- The parser is `semantic.py:174-199`.
- Donor tie-breaking is `checks.py:139-150`, which uses `record.make_gap_id`, and that hashes `CONFIG_SHA256` (`record.py:107-111`).
- The committed maps and caches under `research/n3/{plc,gdpr_v1,gdpr_v2}/` are read-only.
- To regenerate the inputs, use the domain arguments in `research/spikes/jev/judge_swap.py:24-28`.

## Steps
1. **Parser precondition.** In `semantic.py`, a reply is undecided unless at least one of `states` / `partially` is present and every present key is a list.
   - Write tests for: the empty object `{}`, a wrong type, a reply with neither key, and a states-only reply.
   - Replay every committed reply in `research/n3/*/closure_judgements.json` through the new rule. Report the flips. Expect 0, with the 16 states-only replies staying valid. If any reply flips, stop and report.
   - This edit changes gapmap behaviour, so check that `uv run --directory gapmap pytest -q` passes and that a replay of the committed maps is still byte-identical.
2. **Measure the current control as it stands**, offline from the cache. For each pair, count:
   - identical arms;
   - pairs whose closure rests on seed sentences only;
   - control arms truncated by the cap, and own arms truncated by it;
   - pairs where the seed alone fills the cap;
   - pairs with a tied donor;
   - pairs with an empty own or donor other-source pool.

   Check these against audit finding 6: 80/153 truncated, 53/153 tied, 21 and 7 empty.
3. **Build `control2`:**
   - Both arms get the same number of non-seed sentences, with the cap applied *after* the seed.
   - Donor tie-breaking does not depend on the config hash: use sorted seed claim ids, then the lens.
   - Add a seed-free comparison, with seed and same-source sentences excluded from both arms, run only on pairs where both arms are non-empty.
   - Report both splits: closed-or-partial, and closed only.
   - Resample intervals by seed claim.
4. **Prove it discriminates (L7.3)**, on fixtures:
   - A planted positive, where the element is stated in an other-source sentence of the own arm only, must give own > control.
   - A length-matched stand-in, with the same sentence lengths and random words, must not.
   - Record the best reachable difference on the observed data.
5. **Run `control2`** with `--judge ollama`-equivalent calls on PLC and GDPR v1, plus GDPR v2 marked not admissible. Write into `research/n3_control/<domain>/` together with a new judgement cache. Check that `research/n3/` is unchanged: `git status` shows no diff there.

## Done when
- The tests pass.
- `research/n3_control/RESULT.md` gives, per domain and lens:
  - the share of pairs able to discriminate;
  - the own − control difference on equal-cap pairs and on seed-free pairs, each with a seed-resampled 95% interval, for both splits;
  - the planted-positive and stand-in outcomes.

## Decision it feeds
- **The control discriminates** (planted positive fires, stand-in fails, and the real difference is non-zero): it is the MS1 instrument candidate. I2 runs Jev on it.
- **It is mechanically fine but the real difference is about 0:** the qwen judge is uninformative even on a fair control. Report that; I2 tests whether a different judge separates.
- **The planted positive does not fire:** the control design itself is wrong. Report it and stop; DS2 and the owner revisit the design.
