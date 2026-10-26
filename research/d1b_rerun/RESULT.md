# D1b result: the gap map's judge fixed, the rerun stopped at A (2026-10-26)

**Question.** Once the gap map's closure judge is chosen by measurement, do fresh questions aimed at
its open spots on dependence-forecastability draw out more knowledge the docs lack than questions on
its closed spots? Plan: `docs/plans/gapmap-fix-and-d1-rerun.md`.

**Answer.** The question can't be answered on this codebase. Recorded as **Change** (owner,
2026-10-26). The rerun stopped at **Stop A**, the free feasibility check before any question was
built. Of the 35 fresh topics that survived the owner's review, the cheap closure arm left only
**7** open in every version, against **23** closed. That is below the floor of 10 per arm, and at
most **3** matched gap–covered pairs were possible. A top-tier arm can only remove topics from
either side, so no reading of it could reach the floor. The stop rule was fixed in the plan before
any closure call (§3.2, §5).

**Changed.** Following plan §3.7: gap-map targeting is **not** a pilot claim. The search for a PW
lecturer and volunteers may still start, as an elicitation-and-onboarding pilot without targeting.
Further ranking work waits for N3 to resume. The fix itself (item 1) holds as far as it got: the
closure judge is selectable beside the default and chosen by measurement. The cheap arm, gemma, passes
both checks (G2 under a disclosed amendment); sol passes G1 and the first of its two required G2 runs.

## How to read it

- **Illustration, not evidence**, as with D1: one expert, who built the system, on one codebase.
  Feeds no N3 gate and is not RQ-B evidence.
- **What the stop says.** Once the closure judge can tell "states the element" from "is on topic"
  (G2 below), it judges most fresh candidate gaps on this codebase as covered by its docs (23 of 35
  closed). The gap map's open side is too rare here to test targeting with balanced arms. It does
  **not** say targeting fails: no answer was collected.
- **The stop rests on an upper bound, not on the cheap arm's judgement alone.** The rerun's gap arm needs
  every version open under **both** arms. Sol could only shrink the 7, so the cheap arm settled
  nothing that a top-tier arm could have changed.
- **The real-data null still flags the map.** With gemma as judge, both gap maps still carry
  `closure-uninformative`: mismatched-evidence control +0.125 (cheap ledger) and +0.111 (top-tier),
  against +0.20 needed. This was expected before any judge ran (plan §2.2 G4): a lexical-overlap
  stand-in passes that check on the cheap ledger (+0.208; +0.200 on the top-tier ledger), so it
  cannot certify a judge on these ledgers. The judge is
  validated only on the constructed checks (G1, G2), as the plan said `RESULT.md` would state.
- **One post-hoc amendment, disclosed.** G2's limit on the random-letter arm was stricter than the
  no-insert limit it contains (every R arm holds the no-insert arm's sentences). On the owner's
  decision, after gemma's gate data, R is scored on what the letters add (`R_excess`). The raw R
  rate is reported (gemma: 0.15 in both runs, which fails the original R ≤ 0.10; gemma passes only
  under the amendment). Commit `b7cc35f`; lesson queued.
- **One ordering slip.** Sol's paid G1 and G2 checks were started in parallel with the cheap arm's
  gap maps, before the free Stop A count, against the plan's order. Sol's G1 and first gate run
  finished before the count; the second gate run was stopped when the count failed. $0.29 spent.
  Lesson queued.

## Figures

**Item 1, the fix: closure judges chosen by measurement**

| Judge | G1 (N3 L7.3 fixtures) | G2 | Verdict |
|---|---|---|---|
| qwen2.5:7b (local, D1's judge) | fails | fails (N 0.83) | out |
| gemini-3.5-flash-lite | fails | fails on the selection split (N 0.50) | out |
| qwen3.8-flash | passes | fails on the selection split (closes nearly every arm) | out |
| mistral-small-2603 | — | unavailable (HTTP 429 on every call) | dropped |
| deepseek-v4.1-flash, glm-5.3-flash | pass | fail on the selection split, which proved unreachable (its seeds state the element) | not gated |
| **gemma-4-31b-it** (cheap arm) | passes | gate split (13 topics), passes twice: P − N 0.92, lower90 0.75, N 0.08, N+ 0.08, no-insert 0.15, R 0.15 (raw), R_excess 0 | **chosen** (passes under the amendment) |
| **gpt-6.1-sol, high** (top-tier arm) | passes | gate split, passes once: P − N 1.00, lower90 1.00, N 0, N+ 0, no-insert 0, R 0 | not yet eligible: the second required gate run was stopped at A |

G2 holds topicality fixed: per topic, the same seed and background with nothing inserted (0), a
sentence stating the element (P), an on-topic non-element at least as long and as on-topic (N),
N plus 2–3 more (N+), and random letters with P's word lengths (R). Pass needs P − N ≥ 0.50, a
cluster-bootstrap lower bound ≥ 0.30, N and N+ ≤ 0.25, no-insert ≤ 0.25, R_excess ≤ 0.10, nothing
undecided. The owner confirmed every fixture label and dropped 7 of 24 topics whose seeds already
state the element or its reason; the gate split keeps 13.

**Item 2, the rerun: the fresh pool at Stop A (gemma closure, both D1 ledgers)**

| | Count |
|---|---|
| Fresh candidate versions (D1 topics excluded) | 72, in 51 topics |
| Topics after the owner's review | 35 |
| Open in every version (gap-eligible) | 7 |
| Closed in every version (covered-eligible) | 23 |
| Mixed, partial or undecided (neither arm) | 5 |
| Matched pairs, upper bound | 3 |
| Floor per arm (fallbacks 15 → 12 → 10) | 10 |

The gemma gap maps against D1's qwen maps (plan §1.1): mismatched-evidence control +0.125 vs
+0.097 (cheap ledger), +0.111 vs +0.044 (top-tier); judge state equal to the lexical state 49/72 vs
39/72 and 29/46 vs 23/46. Both runs complete, 459 calls, 0 truncated. Aggregates only: the
closure caches stay git-ignored.

Built but not used, because the rerun stopped: the decision rule and its L7.3 checks
(`rule.py`, `rule_checks.json`, all passing at 15, 12 and 10 per arm), the sheet builder with
matching and sealing (`build_sheet.py`), blind novelty judging with canaries (`novelty.py`,
`fixtures/canaries.json`) and the retest (`retest.py`). They are tested (`tests/`) and reusable on
a codebase whose open side is large enough.

## Cost

$0.92 of the owner's $6 cap: $0.62 on OpenRouter (judge screening, G1, G2, seed checks and
gemma's two gap maps) and $0.29 on OpenAI (sol's G1, $0.13; its first G2 gate run, $0.14; 9 calls of the stopped second run, $0.02). No local models: the
Mac crashed while screening them, so they were deleted and the cheap arm moved to OpenRouter.
