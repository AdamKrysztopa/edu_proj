# Plan: how dense is the gap map's open side, codebase by codebase? (2026-10-27)

**Question.** D1b stopped at Stop A because on dependence-forecastability (single owner, thorough
docs) the cheap closure judge (gemma; validated on constructed checks only, G2 under a disclosed
amendment) left only 7 of 35 fresh topics open in every version
(`research/d1b_rerun/RESULT.md`). Does the open share differ across codebases (single owner vs many
authors, thin vs thorough docs)? Which codebase gives a later targeting test (D1c) at least 10
matched open and 10 matched covered topics per arm?

Like D1 and D1b, this is illustration-grade. It counts the gap map's states on public docs and
collects no answers. It feeds no N3 gate and is not RQ-B evidence. No question is built here.

**Status, 2026-10-27: stopped before any paid call.** At D1's pipeline, no candidate fits the line's
$4.00 cap. With one top-tier ledger, one fits at a time (antropy or modmrmr; both cost $6.65). The brief requires three (§2). The $0
parts are done and the paid part waits for the owner (§9). $0 spent. One `methods-critic` round
judged the stop correct by a wide margin and found the funded design not runnable as first written.
Its findings are applied below. The remaining preconditions (§7) must be met before any funding.

**Owner decision, 2026-10-27:** (1) the stop is accepted; there is no paid part, and ranking work
stays deferred to N3, per D1b's Change; (2) turbo-design is excluded from any later study
(`REORIENTATION.md` §18.1, conservation content). §9 is closed.

## 1. Pipeline (D1's and D1b's)

Per codebase:

1. **Corpus** ($0), in `research/d1_demonstrator/build_corpus.py`'s format (HTML-wrapped,
   content-addressed, manifest), with selection rules fixed here. D1's own corpus was picked by hand
   and does not follow them.
   - **Project docs.** The rule is in `estimate.py`'s `user_docs`. It takes README and docs prose
     (`.md`, `.rst`, `llms.txt`) and excludes plans, archives, changelogs, contributing guides,
     notebooks, and agent and CI files. Up to 16 files are taken, largest truncated size first, at
     the pinned commit. Docstrings are excluded for every codebase alike, as in D1.
   - **Outside pages.** Ten pages: the six Wikipedia articles and four upstream API-reference pages
     a fresh subagent names from the README alone, as the methods the project implements and the
     libraries it builds on. The subagent sees no ledger, gap map or state. The list is committed
     before the first call.
2. **Ledgers**, as D1's runs, both on OpenRouter:
   `uv run --directory reconstruct python -m reconstruct.run --live --corpus MANIFEST --domain D --task T --max-doc-chars 12000 --max-results 5 --max-usd X [--models research/d1_demonstrator/models_toptier.json] --out research/gap_density/runs/<codebase>/<ledger>`.
   The cheap ledger uses the package's `models.json` (Haiku 4.5, verifier gpt-5.4-mini). The
   top-tier ledger uses Opus 5.5 with verifier gpt-6.1-sol. The task is D1's wording with the
   codebase's name.
3. **Closure judges on each ledger**, as D1b:
   `uv run --directory gapmap python -m gapmap --ledger L --sidecar S --domain D --out DIR --judge openrouter --model google/gemma-4-31b-it --reasoning-max-tokens 2000 --max-usd X --spend-ledger research/gap_density/runs/openrouter_spend.jsonl`,
   and in parallel `--judge openai --model gpt-6.1-sol --reasoning-effort high --spend-ledger research/gap_density/runs/openai_spend.jsonl --parallel-arm GEMMA_DIR`.
   **Sol runs on every codebase**, not only where gemma passes, so no density figure rests on the
   cheap judge alone.
4. **Topics.** D1b's debris rule, then D1b's topic clustering (`build_sheet.cluster`). D1b
   plan §3.1 step 4 also applies: a fresh subagent sees one text per topic, with no arm and no state,
   and flags duplicate topics. The owner confirms each flag before a topic is dropped, as in D1b, so
   no synthetic output alone decides what is counted. D1b's D1-overlap filter applies only to
   dependence-forecastability. Counts before step 4 are labelled pre-review upper bounds.
5. **Stop A count**: `build_sheet.arm_of`, `match` and `choose_size` unchanged, through
   `research/gap_density/stop_a.py`.

## 2. Cost estimate ($0, done first)

`research/gap_density/estimate.py report` writes `estimate.json`. The unit costs come from D1's and
D1b's own spend records, with **each ledger priced complete**: every attempted call is priced at its
task's mean paid cost.

| Item, at D1's 26-doc corpus | USD | Source |
|---|---|---|
| Top-tier ledger | 6.29 (est.) | `runs/toptier-26b` spent $3.95. It is marked complete, but 761 of its 802 cross-verifications, 32 of 601 verifications and all 30 decoys ended in `api_error`, unpaid. |
| Cheap ledger | 1.95 (est.) | `runs/cheap-26b` stopped at its $1.50 cap. The missing cross-verifications are priced at its own paid mean and scaled to the top tier's count by claims, plus D1's decoy cost. |
| Gemma closure, both ledgers | 0.23 | The last 459 rows of `d1b_rerun/openrouter_spend.jsonl` (277 + 182 calls, from the two maps' `judge.json`). |
| Sol closure, both ledgers | 0.91 (est.) | 459 calls at sol's mean of $0.0020 per call in `d1b_rerun/openai_spend.jsonl`. |
| **One codebase, D1 pipeline** | **9.38** | 8.47 on OpenRouter, 0.91 on OpenAI |

Each corpus is priced by its truncated characters (each document cut at 12,000, as reconstruct cuts
it) relative to D1's 199,086, plus 10 outside pages at D1's mean outside size. Scaling by characters
is roughly supported: two incomplete top-tier runs (16 docs, and the failed 26-doc run), which reached
extraction and verification only, differ in cost by 0.619 and in characters by 0.627. The largest-first rule makes the estimate an upper bound on corpus size. It is not a bound on
prices. On the reference, the rule selects 263,529 characters ($12.41), not D1's actual 199,086.

| Codebase | Humans (top author's share) | User-facing doc files (KB) | Project chars in corpus | D1 pipeline, USD | Top-tier ledger only, USD |
|---|---|---|---|---|---|
| dependence-forecastability (reference, not rerun) | 1 (1.00) | 91 (688) | 125 K actual | 9.38 at D1's corpus | — |
| modmrmr | 1 (1.00) | 5 (34) | 31 K | 4.96 | 3.57 |
| statmate-ai | 1 (1.00) | 27 (306) | 175 K | 11.75 | 8.45 |
| sciagent | 1 (1.00) | 21 (320) | 175 K | 11.76 | 8.45 |
| weft | 1 (1.00) | 48 (1,686) | 192 K | 12.54 | 9.01 |
| turbo-design (a NASA fork; excluded, §5) | 3 (0.98) | 25 (54) | 44 K | 5.59 | 4.01 |
| antropy | 13 (0.82) | 3 (17) | 17 K | 4.29 | 3.08 |
| pmdarima | 24 (0.75) | 27 (92) | 75 K | 7.00 | 5.03 |
| tsfresh | 103 (0.33) | 30 (112) | 99 K | 8.14 | 5.85 |

**What fits $4.00:** under the D1 pipeline, none. With the top-tier ledger only, one at a time
(antropy at $3.08 or modmrmr at $3.57, not both). The
brief requires three, so **no paid call is made** (brief, step d). Even counting the $0 reference as
the third codebase, two more would have to be bought, and the cheapest two cost $9.25. Reconstruct has
no `--spend-ledger`; its spend is the run's `calls.jsonl`, capped per run by `--max-usd`. OpenRouter
headroom read on 2026-10-27 (`key_headroom.py`, `headroom.json`): key $29.34 left, account **$19.32**.

## 3. The comparison, fixed before any paid call

There are two axes:

- **Ledger**: cheap or top-tier.
- **Judge**: gemma or sol.

The **primary cell** is D1b's rule: both ledgers and both judges, with a topic open only if every
version under every judge is open, and closed likewise. Each single cell is reported beside it. Per
cell and per codebase, the report gives:

- topics, open in every version, closed in every version, mixed;
- the matched-pair upper bound (`build_sheet.match`);
- open share (open / topics), with a Wilson 95% interval.

Covariates, reported because each moves the share without describing the docs:

- versions per topic and the version-level open share (on the reference, the topic share is 0.21
  at 1.47 versions per topic and 0.35 at 1.11);
- opens with the reason "nothing retrieved to judge" (`semantic.judge_candidate`), reported apart;
- the split by source origin (project docs vs outside pages);
- each ledger's cross-verification completion fraction (on the reference, cheap 54%, top-tier 5%);
- project characters in the corpus, and the count of agent-tooling files.

Classes:

- **Single owner**: one human with at least 0.95 of commits.
- **Many authors**: at least 10 humans, top share at most 0.85.
- **Thin**: at most 50 K project characters in the corpus.
- **Thorough**: at least 70 K (the reference has 125 K).

The depth boundaries were set after reading the inventory, so they are post hoc: 50 K is the
largest gap below the thin codebases, and 70 K is a little over half the reference.

The comparison is descriptive only. With one codebase per cell, and intervals of about ±15–30
points at 10–40 topics, only a difference larger than about 0.35 in open share could show. Authorship
is also confounded with domain, with age and exposure in training data (the owner's repositories date
from 2025–26 and carry agent tooling; the libraries are older and public), and with corpus size.

## 4. "Enough open side", fixed before any paid call

A codebase is **D1c-eligible** iff all three hold:

- in the primary cell, after step 4, `build_sheet.choose_size` reaches at least 10 matched, balanced
  pairs. This is D1b's floor, with its fallbacks 15 → 12 → 10 unchanged;
- the owner wrote the codebase, because D1c needs its expert to answer and NOW recruits no
  participants;
- the codebase is not D1's.

The early stop runs on the **judge axis only**: if gemma's bound in the primary cell is below 10,
the codebase cannot be eligible, because sol can only remove topics. Sol still runs for the density
figures. Across ledgers the bound is not monotone (12 for one ledger, 9 for both), so no ledger is
skipped on that argument. Joining the ledgers raises the open count (16, against 13 and 14) but
splits matching by ledger set (`build_sheet.stratum`), so 7 of the 16 gaps find no partner.

**The floor is a count, not a validity check (L7.3, L7.4).** A random judge at gemma's own
version-level marginals, drawing each version independently, reaches the floor on the reference's
two-ledger pool in **77%** of 300 seeds. One drawing a single state per topic reaches it in 98%, and a
50/50 coin in 99%. Gemma itself does not reach it (`reference_d1.json`). Two independent random
judges, as the two-judge primary cell would face, never reach it (0 of 300); that assumes independent
judges, and no comparator brackets a real, correlated pair. The floor therefore says the pool is large enough to match. It cannot say the
judge reads the new docs correctly. For each codebase, the one-judge and two-judge random rates are
reported beside the judges' count. **Before any
D1c, the closure judges pass a G2-style planted check built on that codebase's docs** (D1b plan
§2.2). G2 validated them on dependence-forecastability only.

**The reference, at $0** (`stop_a.py reference`, which replays gemma's cached states with no model
call, debris rule only, before step 4):

| Ledger | Topics | Open | Closed | Mixed | Upper bound |
|---|---|---|---|---|---|
| Both | 75 | 16 | 42 | 17 | 9 |
| Top-tier alone | 37 | 13 | 16 | 8 | 11 |
| Cheap alone | 57 | 14 | 35 | 8 | 12 |

All are gemma-only upper bounds. The count includes 14 of D1's 15 questions (Q7 falls to the debris rule), so it calibrates the rule
and cannot host D1c. 69 of the 75 topics come from the project's own docs, so outside pages add
independence keys, not topics. A thin codebase therefore has few topics. By linear scaling (rough;
outside pages yield about 7 times fewer topics per character), modmrmr would have about 17 project-doc topics
with both ledgers, plus about 6 from outside pages. Origin is its own matching stratum, so 10 pairs
would need almost no mixed topics. The reference ledgers were 54% (cheap) and
5% (top-tier) cross-verified. Funded ledgers capped on complete-ledger estimates should come out near
100%, so any comparison with the reference differs in cross-verification completeness too.

## 5. Candidates and why

**Owner-written**: weft, statmate-ai, sciagent, modmrmr.

**turbo-design is excluded.** It is a fork of NASA's repository, with 98% of commits by its NASA
author, so it is not the owner's. Its subject, turbomachinery radial-equilibrium design, rests on
mass, momentum and energy conservation. `REORIENTATION.md` §18.1 makes anyone who has seen
reconstructed conservation content ineligible for a Track A human role, and has NOW mechanics runs
exclude conservation items; reconstructing this codebase for the owner would risk both.

**Many-author projects.** All are Python time-series libraries near the reference's methods,
permissively licensed, of comparable repository size (8–83 MB, against 14 MB), each with a docs site:

- **antropy** (13 humans, BSD-3): entropy measures, the reference's nearest neighbour. Its prose docs
  are thin; its API lives in docstrings.
- **pmdarima** (24 humans, MIT): forecasting with auto-ARIMA. Moderate prose docs, tips and use
  cases.
- **tsfresh** (103 humans, top share 0.33, MIT): feature extraction and relevance testing. The most
  distributed authorship, and thorough docs.

None of the many-author projects can host D1c. They answer the density question only. Third-party
corpora and closure caches stay git-ignored; only aggregates are committed.

## 6. Procedure when funded

1. Meet §7's preconditions.
2. For each codebase, build its corpus ($0). Commit the commit hash, the doc list and the outside-page
   list before any call.
3. Run `scripts/key_headroom.py` before every OpenRouter run (L7.1). Stop if less than $10 remains,
   because other agents share the key. Record the sum of the chosen option's caps beside the
   headroom (L7.2).
4. Run the ledgers, then gemma's maps, then sol's maps (with `--parallel-arm`), then step 4 and the
   count. For D1c candidates, take the codebases in order and stop at the first eligible one.
5. Cap each run's `--max-usd` at about 1.25 times its estimate, cumulative per provider. A ledger
   stopped by its cap is still used (`17e539f`), and its completion fraction is reported.
6. Write `research/gap_density/RESULT.md` in D1's shape, run `citation-verifier`, and commit
   aggregates only.

## 7. Preconditions before any funding (from `methods-critic`)

- **An owner decision reopening targeting work before N3.** D1b's recorded Change says further
  ranking work waits for N3 to resume, and that gap-map targeting is not a pilot claim. D1c is a
  targeting test.
- **Parameterise the reused code per codebase, test first.** `build_sheet.OWNER_REPO`,
  `common.LEDGER_DIRS` and the novelty retriever's corpus (`novelty.passages`) are fixed to
  dependence-forecastability. Run unchanged on another codebase, every topic would read as
  "outside", and similarity would be scored against the wrong corpus. A test with a planted
  non-reference codebase must come out with project origin and similarity against its own corpus.
- **An OpenRouter top-up (L7.2).** About 90% of each option's cost is on OpenRouter (95% for the top-tier-only options). One thorough
  codebase alone is about $10.6 there, $13.3 at 1.25× caps. Against the account's $19.32 and the
  $10 reserve, the $9.32 left covers no thorough codebase and at most one thin one. The top-up must cover the option's
  capped OpenRouter sum plus the reserve, and the sum is recorded beside a fresh headroom read.
- **A $0 check** that no candidate is in E-OSS's held-out departure set (the Avelino et al. 2019
  register, `research/ds8-oss-departures.md`). The list is not in this repository. tsfresh, at 9.5 K
  stars, is the candidate most likely to be in it.

## 8. Risks

- The estimate bounds corpus size, not prices. The complete-ledger and sol figures are
  extrapolations.
- The closure judge sees the ledger, not the docs. A thin corpus can read as open because the
  extractor kept little, not because the docs are silent.

## 9. Owner decisions

1. What to do with the paid part. Options, by merit:
   - **Accept the stop (Recommended).** No targeting test can follow without reopening the ranking
     work that D1b's recorded Change deferred to N3 (§7). The $0 reference already answers the
     feasibility question on a thorough single-owner codebase: about 9 pairs at the gemma-only upper
     bound, and a random judge reaches the floor on most seeds, so passing the floor elsewhere would
     not show the gap map works. What would change it: an owner decision to reopen targeting before
     N3. The next option is then the strongest.
   - **Sequential search of the thorough owner codebases, D1 pipeline**: statmate-ai, then
     sciagent, then weft, stopping at the first eligible one. $11.75 to $36.05 estimated. This is
     the only option aimed at the actionable D1c question. Thin codebases would need almost no mixed
     topics to reach the floor (§4), and the many-author projects cannot be eligible.
   - **2 × 2, D1 pipeline**: modmrmr, statmate-ai, antropy, pmdarima. About $28.0. It answers the
     density question descriptively, within the precision in §3, with D1b's rule unchanged.
   - **Six codebases, top-tier ledger only**: modmrmr, statmate-ai, sciagent, weft, antropy,
     pmdarima. About $37.6. One ledger breaks D1b's every-version rule over two ledgers, so the owner
     would have to amend that rule.
   - **2 × 2, top-tier ledger only**: the same four as the 2 × 2 above. About $20.1, with the same
     amendment.
   Every option also needs the OpenRouter top-up in §7.
2. Confirm that turbo-design is excluded (a third-party fork, with conservation content).
