# N9 cost ledger: result (I11, 2026-10-24)

**Result.** Every recorded call is now in one ledger: 4,785 calls, $5.30. That is $2.83 engineering (E-LIVE, the JEV spike, N3) and $2.48 evaluation (E-PLANT, E-ABST). Every run reconciles with its own recorded total to within $0.01; the largest gap is $0.0013. One gap is explained rather than closed: the E-ABST exposure check ($0.029), which no report's cost table lists. Failed or retried calls lost 5.6% of spend. The bigger loss is at run level: **46% of all spend, and 91% of evaluation spend, went to runs that produced no usable result.** Unit costs:
- $0.0030 per verified claim;
- $0.036 per gap candidate;
- $0.14 per HYP candidate.

Cost per validated item is **unavailable**, because no item is validated.

**Decision it feeds.** The I4 and I10 budgets, and any request to raise the key limit. There is no gate.
- **I2 and I10:** the caps stand ($0.10 and $1).
- **I4:** the planned $0.5–1 for the out-of-sample domain run is too low. A complete v3-style domain run costs at least $1.64, and up to about $1.94 if every pending claim turns out supported (§4). A $1 cap would bind. Cross-verify and decoys run last, so a capped run would lack them and fail P1's live criterion; that is the same reason P2 calls a capped unit hollow. Set the cap at **$2.50**.
- **Key limit:** no raise is needed now. I2, I4 at $2.50 and I10 sum to $3.60 against $14.99 of headroom. The deferred N2 reruns cannot share one weekly window (see §4). P1 already makes them sequential, with v3 first; spread across weeks, they fit without a raise.

Data: [`ledger.json`](ledger.json), built by `python3 scripts/cost_ledger.py --private <repo>/.private` (tests: `reconstruct/tests/test_cost_ledger.py`).

## 1. What the ledger holds

Each row is one call. It records the run, stage, model, served model, tokens and USD, plus:
- the status: success, retry, failure or unknown;
- the kind: engineering or evaluation.

| Source | Calls | USD | Kind |
|---|---|---|---|
| E-LIVE, 6 runs (`reconstruct/runs/*/calls.jsonl`) | 1,067 | 2.3744 | engineering |
| JEV spike (`research/spikes/jev/cache/`) | 1,637 | 0.4508 | engineering |
| N3 closure judge, 3 domains (local Ollama cache) | 641 | 0 | engineering |
| E-PLANT: baseline, plant authoring, run 1 (`.private/e_plant/`) | 1,310 | 1.9532 | evaluation |
| E-ABST: baseline, exposure, run 1 (`.private/e_abst/`) | 130 | 0.5242 | evaluation |

**Status rules.**
- `ok` is a success.
- A failed attempt that the same task re-sent later with the same spec is a **retry**; the last failed attempt is a **failure**.
- Billed bad outcomes are failures: truncated, malformed JSON, refusal, served-model mismatch.
- A rejected plant page is a retry if the same page is accepted later.
- A JEV answer that `judge_swap.py`'s own parse rule cannot read is a failure.
- Logs written before outcome logging existed (E-LIVE v1, and the E-ABST baseline and exposure) are **unknown**. That covers 816 calls and $1.22.

**Sealed material.** From `.private/` the script reads only call logs: `calls.jsonl`, from which the protocol's report takes cost and the rerun decision reads (§8), and the cost and acceptance fields of the plant-authoring log. It opens no sealed ledger, sidecar or snapshot, and no row keeps a prompt hash or free text. E-ABST items are still to be coded blind, so E-ABST rows carry no item ID and are ordered by stage and cost within each run, not by log order. Otherwise a row's token count could show a coder which items the raw arm answered.

## 2. Reconciliation

| Run | Ledger | Recorded | Gap |
|---|---|---|---|
| E-LIVE v1 PLC `…59ec876b3d7e` | 0.6789 | sidecar 0.6789; report 0.679 | 0.0000 / −0.0001 |
| E-LIVE v1 GDPR `…eb840a85b7d1` | 0.5003 | sidecar 0.5003; report 0.500 | 0.0000 / +0.0003 |
| E-LIVE v2 PLC `…518f99363336` (crash) | 0.1929 | sidecar 0.1929; report 0.193 | 0.0000 / −0.0001 |
| E-LIVE v2 GDPR `…bc1cc9a30a02` | 1.0024 | sidecar 1.0024; report 1.002 | 0.0000 / +0.0004 |
| E-LIVE v3 PLC and GDPR (blocked) | 0 | sidecar 0 | 0 |
| E-PLANT baseline | 0.0735 | 0.0735 (§1.1); 0.074 (§3) | 0.0000 / −0.0005 |
| E-PLANT plant authoring | 0.1214 | 0.121 | +0.0004 |
| E-PLANT run 1 (food; concreting) | 1.7583 (0.8829; 0.8753) | 1.758 (0.883; 0.875) | +0.0003 (−0.0001; +0.0003) |
| E-ABST baseline | 0.0068 | 0.0068 (§2.1); 0.007 (§3) | 0.0000 / −0.0002 |
| E-ABST run 1 | 0.4883 | 0.488 | +0.0003 |
| E-ABST exposure | 0.0291 | **none** | explained below |
| JEV spike (Sonnet reference) | 0.4508 (0.3687) | 0.45 (0.37) | +0.0008 (−0.0013) |
| N3 plc, gdpr_v1, gdpr_v2 | 0 | $0, local | 0 |

Report figures are rounded to three places (gaps under $0.0005 are rounding) or, for the JEV spike, to two (under $0.005). Sources: the sidecars' `stats.total_cost_usd`, `research/n2/e_live_report.md`, `research/n2/e_plant_eabst_report.md` §1–3, and `research/spikes/jev/RESULTS.md`.

**Explained gaps.**
- **E-ABST exposure, $0.029.** Two `web_search` calls are logged in `.private/e_abst/exposure_calls.jsonl`, but the §3 cost table of `e_plant_eabst_report.md` omits them. §3's items therefore sum to $2.448, $0.029 less than the ledger's evaluation spend.
- **The key's totals cannot reconcile with the ledger.** The OpenRouter key reports $66.28 used all time, against $5.30 in the ledger. It also reports $0.057 this month, and the ledger has no October calls. So the key serves spending that no committed log records: other projects, or calls from this repository that were never logged. The weekly headroom is therefore shared, and the ledger cannot see what else draws on it.
- **The 2026-09-28 limit.** The key hit its $5 weekly limit that day, when the ledger records $4.85. If the window opened that Monday, at least $0.15 that day went unlogged.
- **Calls never logged.** Failed provider calls before `0f39ed9` left no line, and the spike's HTTP 429 retries were not logged either. Both are assumed unbilled, so they change no dollar figure, but they are missing from the call counts.

## 3. Unit costs and losses

**Per unit.** The basis is the three E-LIVE runs whose ledgers feed N3, $2.1815; N3 itself cost $0.
- A "verified claim" is a claim the verifier marked SUPPORTS (`stats.n_supports`, 723 in all). That is a model's judgement, not a validation.
- A "candidate" is a record in HYP, RG-SINGLE, RG-SIBLING or RG-UNVER (61 in all, 16 of them HYP). RG-UNK and CONTROL are fixed templates, so they are excluded.
- The "loaded" basis adds the crashed and blocked E-LIVE runs ($2.3744).

| | Direct | Loaded |
|---|---|---|
| Per verified claim | $0.0030 | $0.0033 |
| Per gap candidate | $0.036 | $0.039 |
| Per HYP candidate | $0.136 | $0.148 |
| **Per validated item** | **unavailable**: no gold and no human coding exist | same |

Evaluation runs have no per-claim figure, because their run-1 claims are sealed and unscored. The gdpr_v2 map is not admissible, but its 22 candidates are counted, because its run's spend is counted.

**Lost to failed and retried calls: $0.295, 5.6% of all spend.** Excluding calls of unknown status, it is 7.2%.
- 5 truncated extracts in E-LIVE v2 GDPR cost $0.247, a quarter of that run's spend. Each truncation is a full 8,192-token output that is paid for and then discarded.
- 11 rejected plant pages, re-authored, cost $0.045.
- 58 unreadable answers from hosted qwen in the JEV spike cost $0.003. The spike's 26 unreadable local-qwen answers and E-LIVE v3's 2 provider errors cost $0.

**Lost to runs with no usable result: $2.439, 46% of all spend.**
- E-PLANT run 1 ($1.758) and E-ABST run 1 ($0.488) are rerun units under amendment 1: sealed, never to be scored.
- E-LIVE v2 PLC crashed ($0.193).
- E-LIVE v3 was blocked at its first call ($0).

So 91% of evaluation spend bought no evaluation result, because of the provider-failure defect fixed in `0f39ed9`. For engineering, the figure is 7%.

## 4. Prospective budget

Headroom is $14.99 of the $15 weekly limit (`scripts/key_headroom.py`, 2026-10-24 09:27 UTC).

| Item | Cap | Basis |
|---|---|---|
| I2 Jev on the rebuilt control | $0.10 | prompt cap; expected about $0.01 |
| I4 out-of-sample domain run | $1.00 as planned; **$2.50 recommended** | projection $1.64 to about $1.94, below |
| I10 pre-gold corpus pilot | $1.00 | prompt cap |
| Deferred N2: E-LIVE v3, both domains | $2.00 (final-review estimate) | projection at least $3.3 (2 × $1.64) |
| Deferred N2: E-PLANT run 2 | $3.00 | registered; run 1 cost $1.76 |
| Deferred N2: E-ABST run 2 | $14.40 | registered (P3); run 1 cost $0.49 |
| **Sum as planned** | **$21.50** | **$6.51 over the headroom** |

**The v3-style domain projection: at least $1.64.**
- E-LIVE v2 GDPR is the base, $1.002. It used the current prompts, under which a verify call costs $0.00106, against $0.00057 in v1.
- The 140 claims the provider defect left pending (`e_live_report.md` §5) add $0.148 of verifies.
- Cross-verify adds $0.438: up to 2 calls per supported claim (P3), 207 claims, at $0.00106. It replaced the old contradiction pass (amendment 1, `080b109`), so no contradiction term is added.
- 30 decoys add $0.049: 10 per mutation type (`reconstruct/src/reconstruct/evidence.py`), generation at the v1 price plus one verify.

v2 logged none of these calls. If all 140 pending claims turned out supported, cross-verify would add up to $0.297 more, about $1.94 in all. Either way a $1 cap is below the projection, and $2.50 clears the ceiling.

**What it means.**
- I2, I4 at $2.50 and I10 sum to $3.60, which fits in one window.
- The deferred N2 reruns total $19.40 as planned, or about $20.70 with v3 at its projection. That exceeds any single weekly window.
- E-ABST run 2's $14.40 cap alone needs a week in which nothing else is spent: $0.59 of slack against today's headroom, on a key that other spending also draws on.
- Run 1 cost 3% of that cap, but run 1 was hollow (17 of 24 items made no claims), so it is no evidence for lowering a registered cap.

## Not done

- Wall-clock per item (E-COST, `REORIENTATION.md` §18).
- The cost–accuracy frontier.
- Comparison with published CTA effort.

None of these is in I11's scope. The frontier needs a validated item, which no data yet provides.
