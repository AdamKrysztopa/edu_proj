# Closure topicality check: result (2026-10-27)

**Question.** A lexical-overlap stand-in passes control2 on every ledger
(`docs/plans/gapmap-fix-and-d1-rerun.md` §1.5) and the gap map's mismatched-evidence control (MEC)
on D1's cheap ledger (`research/d1b_rerun/RESULT.md`, `g4_standins.json`), so neither null can
certify a closure judge. Can a check that runs on real ledgers make that stand-in fail while a good
judge passes? Can control2 and MEC be repaired? Does sol's I1c GDPR v1 reading, +0.23
[+0.07, +0.39] (`research/n3_control_v3/GUARD.md`), survive the topicality explanation? Plan:
`docs/plans/closure-topicality-check.md`, fixed before any paid call (commit `85060c7`).

**Answer.**
- **Yes on the D1 ledgers, for part I.** RT places an authored sentence that states the element (P),
  or an authored on-topic sentence that does not (N), among the candidate's own real retrieved
  sentences, and asks whether the judge cites it.
  - No stand-in passes. That covers D1b's overlap stand-in and the other 24: the 10 per-sentence
    statistics at every threshold, 3 coins and 11 other arm-level stand-ins.
  - gemma-4-31b-it and gpt-6.1-sol cite every P, and no N or random-letter insert in a closed arm,
    in two cold runs each. Sol marked N as *partially* stating the element in t07 and t15, in both
    runs; that does not count under the rule.
  - Part II asks whether a judge cites real background sentences that do not state the element.
    Sol meets it trivially: 2 background rows cited in closed arms. Gemma's part II waits for the
    owner's labels: it cited 6 rows, which are 5 distinct sentences.
- **control2 and MEC: not repaired.** They are declared unrepairable as judge certificates. A
  real-data null has no element labels, so no planted positive can be built for it. Matching the
  donor arm on the overlap statistic sets the overlap stand-in to 0.00 by construction. But only
  the pairs that can be matched survive: 4 of 44 on GDPR v1.
- **Sol's reading does not survive as a counted ADR 0009 reading.**
  - Gemma's control2 on the same GDPR v1 pairs is **incomplete**: one control arm was undecided, so
    under plan §0 its verdict is not read. Its point estimate is +0.16 [−0.02, +0.32], the same sign
    as sol's.
  - A sensitivity check added after the run fills that arm either way; the 95% interval still
    crosses 0. So the plan's condition (c), gemma's interval above 0, cannot hold for this run.
  - The two sol-only parts of the re-read wait for the owner's labels: RT's GDPR split, and the
    recount of sol's own citations. Both are built.

**Changed.** A closure judge can now be tested with authored inserts placed in real retrievals, not
only against constructed off-topic backgrounds. Why control2 and MEC fail their stand-ins is now
explained, not only measured. Sol's +0.23 stays an uncounted sol-only reading, as `GUARD.md`
already left it. To finish the work, the owner must label 286 sentences
(`fixtures/owner_pack.md`). Those labels complete gemma's D1 part II, let RT's GDPR split run, and
let sol's citations be recounted.

## How to read it

- **Feeds no gate and is not RQ-B evidence.** It decides only whether a closure judge can be checked
  on real ledgers, and whether one sol reading is protected from the topicality explanation.
- **What RT holds fixed (L7.4).** Every arm shares:
  - the seed, in the prompt header only;
  - the lens question;
  - the real background, the first `min(k, 7)` sentences of control2's seed-free own arm;
  - the insert position.

  Arms differ only in the insert, which is authored. A hit is a closed arm whose cited sentence
  numbers include the insert.
  - **D1 matching.** On D1, P and N are matched on length and on seed-and-question overlap: N is
    never shorter than P and never shares fewer of those words. These are the owner-confirmed G2
    sentences, unchanged.
  - **What D1 does not match.** P carries more novel content words than N in 8 of 13 topics (t10:
    14 against 7). 11 of 13 D1 pairs would fail the stricter checks the GDPR inserts had to meet.
  - **What RT shows.** Both judges cite an authored P over an authored N placed among real
    retrieved sentences, and no stand-in we ran explains the choice. It does not show that a
    judge's closures on real retrievals are correct.
- **The binding constraint: only the owner can say whether a real sentence states an element.** RT's
  paid calls ran only on the D1 split, whose inserts the owner confirmed for G2 on 2026-10-26. Gemma's
  G1 retest and its control2 run use no element labels.
  - The GDPR split is built and its stand-ins fail.
  - A blind LLM labeller agreed with the author on all 16 topics (`fixtures/labels_llm.json`,
    SYNTHETIC). Those labels only choose and rewrite fixtures.
  - The runner still refuses the split until the owner's labels exist (`rt.py`,
    `require_confirmed`).
- **Part II on D1.** As coded, part II reads background rows cited in **closed** arms.
  - **Gemma:** 6 rows in three topics, which are 5 distinct sentences. It closed arm 0 (and R) of
    t07 and t18 in both runs on background sentences. It closed the N arm of t07 (both runs) and of
    t21 (run 2) by citing background, not N. The owner's labels decide whether those citations were
    element statements or topicality.
  - **Sol:** 2 rows, both in t09, so it meets part II trivially.
  - **Partial marks.** Counting sentences marked only as partially stating the element, sol adds 9
    rows. These rows are in the pack too (6 of the 9 are rows gemma cited), but part II as fixed
    does not read them.
- **Matching did not do what the plan predicted.** The plan expected matching to leave the
  probe-overlap stand-in passing control2-T. Instead matching left too few pairs to read, except on
  PLC (24 and 33 pairs), where no stand-in's interval stayed above 0. The unrepairable verdict does
  not rest on that prediction. It rests on the missing planted positive, as fixed in plan §2.3.
- **Neither judge reproduces exactly.** The judge here means the whole judge: model, serving and
  decoding (`docs/plans/prompts/_common.md:36`).
  - **gemma-4-31b-it via OpenRouter at temperature 0, G1 retest.** It was eligible again. 5 of the
    76 cached judgements differ from the first run's, all in equal-cap arms, which shows as 16
    arm-state entries in `g1/compare.json`. The seed-free states, the only ones the l73 rule reads,
    are identical.
  - **What the retest means for ADR 0009.** `_common.md:35` asks for "two runs with identical
    results". Under the state-level reading, gemma does not count as an ADR 0009 arm; under a
    verdict-level reading, it would.
  - **How the reading was chosen** (this session's account; the file has no history from before
    the run). `g1_retest.py` compared the full topic records before the run. The seed-free field
    was added after it.
  - **RT runs, both judges.** Each judge's two RT runs have identical hits. Arm states differ in
    t18 and t21 for each judge, through background citations or partial marks only.
- **Undecided arms.** In gemma's control2, one reply for pair 47's control arm (WHY) held no
  parseable JSON. The parser made that arm `undecided`, which made the run incomplete. Every RT
  run was complete.
- **Replay.** After the citation-mapping fix (`rt.py`: background rows that share a claim are
  mapped by the reply's sentence numbers), every RT `rt.json` was rebuilt from its cache with no
  call. Hits did not change. Spend is in the ledgers, not in the replayed `rt.json`.

## Figures

**Item 1: RT on the D1 split (13 topics, 10 clusters, real D1 retrievals, owner-confirmed inserts)**

| Judge | Run | hit(P) | hit(N) | hit(R) | P − N | lower bound | Part I | Arm 0 closed | Background rows cited (closed arms) |
|---|---|---|---|---|---|---|---|---|---|
| gemma-4-31b-it | 1 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | pass | 0.15 | 4 |
| gemma-4-31b-it | 2 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | pass | 0.15 | 6 |
| gpt-6.1-sol, high | 1 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | pass | 0.00 | 2 |
| gpt-6.1-sol, high | 2 | 1.00 | 0.00 | 0.00 | 1.00 | 1.00 | pass | 0.00 | 2 |

The rule was fixed before any call:
- **Part I:** hit(P) − hit(N) ≥ 0.50, cluster-bootstrap lower bound ≥ 0.30, hit(N) ≤ 0.25,
  hit(R) ≤ 0.10, nothing undecided, in two cold runs.
- **Part II:** of a judge's cited background sentences, at most 0.25 labelled by the owner as not
  stating the element. Under 5 cited, part II passes trivially.

**Stand-ins on RT ($0, `rt/standins_d1.json`, `rt/standins_gdpr.json`).**
- **The family.** 10 per-sentence statistics, each in four forms (at or above the median, at or
  below it, argmax, argmin) and swept over every threshold in both directions. Also 3 coin flips and
  12 arm-level stand-ins.
- **D1:** 597 citing stand-ins, none passes.
  - Best: overlap fraction ≤ 0.46, P − N +0.46, lower bound +0.21.
  - Novel content words ≥ 9 gives +0.46, lower bound +0.27, hit(R) 1.00. It fails on the difference,
    the lower bound and hit(R). Its function-word form fails on the first two.
  - D1b's overlap stand-in, arm level: −0.08.
- **GDPR (16 topics):** 699 citing stand-ins, none passes. Best: specificity ≤ 0, +0.44, lower
  bound +0.25.

**Item 2: the nulls with topicality-matched donors ($0, `nulls_t.json`)**

| Ledger | control2: overlap stand-in | control2-T pairs | control2-TT pairs | MEC: overlap stand-in | MEC-T pairs | MEC-TT pairs |
|---|---|---|---|---|---|---|
| D1 cheap | +0.78 | 9 / 72 | 4 / 72 | +0.17 | 16 / 72 | 7 / 72 |
| D1 top-tier | +0.78 | 10 / 45 | 4 / 45 | +0.13 | 17 / 45 | 3 / 45 |
| PLC | +0.69 | **24** / 54 | 2 / 54 | +0.17 | **33** / 54 | 4 / 54 |
| GDPR v1 | +0.45 | 4 / 44 | 0 / 44 | +0.08 | 10 / 51 | 0 / 51 |
| GDPR v2 | +0.38 | 9 / 42 | 3 / 42 | +0.08 | 17 / 48 | 3 / 48 |

- **Matched sets.** On every non-empty matched set the overlap stand-in gives 0.00, by
  construction, on the pairs that could be matched.
- **Unmatched control2.** On GDPR v1, five stand-ins have a 95% interval above 0: overlap, overlap
  fraction, idf overlap, probe overlap and specificity.
- **The 20-pair floor.** Only PLC's two matched sets reach it, and on both no stand-in's interval
  is above 0. Below it, some stand-ins still have intervals above 0:
  - idf overlap, D1 cheap control2-T (9 pairs);
  - a coin, D1 top-tier control2-T (10 pairs);
  - length, novel content words and its function-word form, GDPR v2 control2-TT (3 pairs).
- **Calibration differs from D1b.** MEC's overlap figures here are calibrated on its own and
  control arms. D1b's +0.208 (`research/d1b_rerun/g4_standins.json`) also used the
  other-source-only arm.
- **Why matching is so scarce.** control2's own arm is the top k of the retriever's score, and the
  score's words are in the prompt. Any donor disjoint from the own arm scores no higher, and it
  ties only at the rank-k boundary.

**Item 3: sol's I1c GDPR v1 reading**

| Part (all three must hold) | Status |
|---|---|
| (a) RT's GDPR split, sol, parts I and II | built and checked at $0; waits for the owner's labels |
| (b) sol's citations recounted on the owner's labels, with the overlap stand-in's citations and a planted fake in the same blind pack | built (`reread.py`); waits for the owner's labels |
| (c) ADR 0009: gemma on the same pairs, interval above 0 | **cannot hold**: run incomplete (1 undecided control arm), +0.16 [−0.02, +0.32]; filled either way after the run, +0.14 [−0.03, +0.29] or +0.16 [−0.02, +0.32] |
| gemma as a counted arm: G1 passes twice, identically | passes twice; identical at verdict level, not at state level (5 of 76 equal-cap judgements differ) |

For reference, on these pairs sol closes 19 of 44 own arms against 9 control arms. The overlap
stand-in closes 32 against 12 (+0.45).

The owner pack (`fixtures/owner_pack.md`; provenance in `fixtures/owner_pack_key.json`) shows no
source, arm or cited mark. It holds 345 provenance entries, merged across all sources into 286
items under 41 topic headers:
- **RT GDPR:** 32 inserts and 100 background rows.
- **D1 part II:** 8 rows cited in closed arms, 3 more marked partial, and 10 decoys.
- **I1c:** 63 sentences sol cited, 44 the overlap stand-in cited, and 85 decoys.

## Cost

$0.43 of the line's $3.00 cap:
- **OpenAI, $0.29:** 104 sol calls, the two RT D1 runs.
- **OpenRouter, $0.14:** 359 gemma calls:
  - the G1 retest, $0.02 (76 calls);
  - control2 on GDPR v1, $0.09 (179 calls, 3 of them retries after a truncated reply);
  - the two RT D1 runs, $0.03 (104 calls).

Spend ledgers: `openai_spend.jsonl` and `openrouter_spend.jsonl`. Session observation, not a
committed artefact: `scripts/key_headroom.py` read $29.23 remaining on the OpenRouter key before
the RT runs.

Still to come, once the owner's labels exist: RT's GDPR split, two runs each for gemma and sol,
about $0.55, within the remaining caps.

## Files

All under `research/closure_topicality/`:
- **RT:** `rt.py` with its stand-ins in `standins_t.py`. Fixtures are
  `fixtures/topics_{d1,gdpr}.json`, `fixtures/inserts_{d1,gdpr}.json` and `fixtures/insert_spec.md`.
- **Topic selection:** `select_topics.py`. It is not called `select.py`, which would shadow the
  standard library's `select`.
- **RT runs:** `rt/d1/<judge>-run<n>/`, holding the cache and `rt.json`, plus
  `rt/standins_{d1,gdpr}.json`.
- **Nulls:** `nulls_t.py`, output in `nulls_t.json`.
- **Item 3:** `c2_gemma.py` (output in `control2_gemma/gdpr_v1/`), `g1_retest.py` (output in
  `g1/`) and `reread.py`.
- **Owner pack:** `pack.py`, output in `fixtures/owner_pack.md` and `fixtures/owner_pack_key.json`.
- **Simulation:** `sim.py`, output in `sim.json` (SYNTHETIC operating characteristics). Its figures
  supersede the scratch figures in plan §1.6, which were 0.92, 0.85, 0.56 and 0.38 at 13 topics
  against 0.88, 0.81, 0.56 and 0.40 here.
- **Tests:** `tests/`, 43 tests with fake judges and no network. Run them with
  `uv run --directory gapmap pytest ../research/closure_topicality/tests -q`.

Once the owner has labelled the pack:
1. Write the labels as `fixtures/owner_labels.json` (`{"items": {id: true|false}}`).
2. Run `rt.py --split gdpr` for both judges.
3. Run `pack.py` to rebuild the key.
4. Run `reread.py`.
