# Plan: D1c, the gap-map targeting test on a second codebase (2026-10-27)

D1b asked a question and could not answer it on dependence-forecastability: only 7 of 35 fresh topics were open in every version, against a floor of 10 per arm (`research/d1b_rerun/RESULT.md`). D1c asks **the same question on another codebase the owner wrote**, with D1b's rule, arms, blinding and judges unchanged wherever possible (`docs/plans/gapmap-fix-and-d1-rerun.md`, cited below as "D1b plan §x"). Like D1 and D1b it is exploratory: one expert, who built both the system and the codebase. It feeds no N3 gate and is not RQ-B evidence. N3 stays paused with its registered rules unchanged (`REORIENTATION.md` §22).

Status: **draft for the owner's approval.** Built at $0. No codebase is chosen here: a parallel gap-density survey recommends one, the owner confirms it, and only then is `codebase.json` filled (§2). Every paid run in §8 happens later, under caps the owner sets.

## 1. Question and decision rule, carried over

**Question (D1b, unchanged).** On a codebase the owner wrote, do questions aimed at the gap map's open spots draw out more knowledge the docs lack than questions aimed at its closed spots?

Carried over unchanged:
- **Arms** (D1b plan §3.2). A topic is *gap* iff every closure judgement of every ledger version of it, by both closure arms, is open, and *covered* iff all are closed. Anything else goes to neither arm. The arms are matched by seeded code within strata (lens, k_topic band 1 vs ≥ 2, ledgers of origin, source origin) on question length and retrieval similarity, with means within 10% (`build_sheet.match`, `balance`).
- **Size and fallbacks** (D1b plan §3.2). 15 + 15. If that cannot be filled, 12 + 12, then 10 + 10. Fewer than 10 matched, balanced topics per arm stops the test (Stop A, §4).
- **Rule** (D1b plan §3.4, `research/d1b_rerun/rule.py`, unchanged code). **Continue** iff the gap "new" rate minus the covered rate is ≥ 0.30 with one-sided exact permutation p ≤ 0.10 on the criterion labels. Under criterion (b) it must hold on the two judges' agreed labels *and* on judge A's labels alone. Otherwise **Change**. Fewer than ⌈8n/15⌉ answers with content by both judges gives **No reading**, which counts as Change. The L7.3 checks (`rule_checks.json`: planted positive, all novel, all copied, filler, 7-vs-4 of 15, judge disagreement, judge-A dissent, at 15, 12 and 10) are rerun and must pass before the sheet is shown.
- **Operating characteristics** (D1b plan §3.4, SYNTHETIC simulation, base rate 0.58, judges 0.9 accurate). Under (b) with the judge-A clause, P(Continue) at 15/15 is 0.03 under no difference, 0.33 at +0.30, 0.52 at +0.40 and 0.71 at +0.50. At 10/10 it is 0.03, 0.23, 0.37 and 0.54. **A Change cannot separate "the map does not target" from "the effect is below about 0.4."** `RESULT.md` prints this, as in D1b.
- **Secondary readings, never gating** (D1b plan §3.4): a length-only labeller, the count of new content units, the owner's self-ratings, and each closure arm's assignment on its own, revealed with the key.
- **Blinding** (D1b plan §3.3). Per-candidate states, caches, rebuilt gap maps and the key are git-ignored (`research/d1c/.gitignore`), then sealed to the owner's RSA public key (`build_sheet.seal`). The builder prints only aggregates and hashes. After all answers are hash-locked, the owner guesses each question's arm. Accuracy ≥ 0.70 at binomial p < 0.05 marks the run "unblinded". `novelty.py reveal` now computes this from `guesses.json` (§10).
- **Collection** (D1b plan §3.6). One question at a time in chat, typed answers, no follow-ups. Two sittings if the owner prefers, split at question 15. The answers are hash-locked (`novelty.py lock`), then the self-ratings and the arm guesses are taken in one pass.

**Criterion.** The D1b owner chose (b): the LLM judges' labels, advisory (D1b plan §3.4). D1c proposes the same. Criterion (a), the one blind second coder, stays available if a coder is found (owner decision, §11).

**What each outcome triggers** (adapted from D1b plan §3.7, fixed in `RULE.md` at approval). D1b was recorded as Change, so gap-map targeting is not currently a pilot claim.
- **Continue under (a):** targeting may become one of the pilot's claims, revising D1b's Change. The pilot keeps its own preconditions.
- **Continue under (b):** advisory. The owner may weigh it in the pilot call. Targeting is not claimed.
- **Change, No reading or Stop A:** D1b's Change stands. Ranking work waits for N3 to resume. A Stop A on a second codebase is recorded as "targeting not testable on two of the owner's codebases", not as a negative result.

## 2. The codebase as a parameter

Everything codebase-specific is one JSON file, `research/d1c/<name>/codebase.json`, copied from `research/d1c/codebase.template.json` the day the owner confirms the codebase. `codebase.load` refuses any file that still holds a `TODO`. Relative paths resolve against the file's directory, which is also where the outputs go: pool, fixtures, questions, sealed key.

| Field | What it is | Who fills it, when |
|---|---|---|
| `name`, `owner_repo` | the repository; `owner_repo` is the substring that marks a source as the owner's (source-origin stratum) | session, at Stop 0 |
| `domain` | the label passed to `gapmap --domain` and `retest.py --domain` | session |
| `seed` | the matching, shuffle and canary seed; fixed in `RULE.md` before any closure call | session, at Stop 1 |
| `corpus`, `corpus_build` | the pinned commit, the owner docs, the outside pages (§3.1) | session proposes, owner confirms at Stop 1 |
| `reconstruct` | domain line, task, `max_doc_chars` 12,000, `max_results` 5, the cheap and top-tier model files (D1's) | session, from D1's values |
| `ledgers` | the two reconstruction run directories | written after each run |
| `prior_items` | earlier questions on this codebase to exclude by topic overlap (D1's 15 for D1b); `null` for a codebase never tested | `null` |
| `canaries`, `canary_mode` | `generated`: canaries from this codebase's own corpus (§5.3) | built in Phase 6 |

D1b's own `research/d1b_rerun/codebase.json` is the default for every script, and replays D1b's committed `pool.json` and topic-review pack byte for byte (tested in `tests/test_codebase.py`).

**What `prior_items: null` changes.** D1b's fresh-question filter (D1b plan §3.1, steps 1 and 4) excluded D1's topics. On a new codebase there is nothing to exclude, so step 1 is a no-op and the topic review (step 4) checks only duplicates among the topics. Debris filtering and topic clustering run unchanged.

## 3. Inputs built per codebase

### 3.1 Corpus

`research/d1b_rerun/corpus_build.py --codebase CFG`, with D1's converter and fetchers reused unchanged:
- **Owner docs:** the user-facing docs at a commit the owner pins, from a local checkout. That means the README, quickstart, how-tos, theory or explanation pages and the reference pages, chosen as D1 chose them. Generated API dumps, changelogs and licences are left out. The aim is 12 to 20 docs. The builder refuses a checkout at another commit and a listed doc that is missing.
- **Outside pages:** about 10 Wikipedia or library-reference pages on the methods the codebase uses. Without them no gap can reach k_topic ≥ 2, because one repository is one independence key (D1b plan §1.3). The session proposes them from the README's method names. The owner confirms both lists at Stop 1, before any paid call.

Cost scales with the corpus (§8), so the list is fixed before any reconstruction.

### 3.2 Reconstruction, both arms (N2 package, unchanged)

`python -m reconstruct.run --live --corpus <corpus>/manifest.json --domain … --task … --max-doc-chars 12000 --max-results 5 --max-usd X`, with the same corpus and task for both arms:
- **cheap arm:** `reconstruct/models.json` (Haiku 4.5 for planner, extractor and baseline; verifier gpt-5.4-mini);
- **top-tier arm:** `research/d1_demonstrator/models_toptier.json` (Opus 5.5; verifier gpt-6.1-sol).

A cap hit saves an incomplete but usable ledger (fix `17e539f`). D1's cheap arm stopped at its $1.50 cap. If either arm stops at its cap, `RESULT.md` says so.

### 3.3 Gap maps, both closure arms

`python -m gapmap --ledger L --sidecar S --domain <domain> --out <root>/closure/<arm>/<ledger>`, run first with `--judge openrouter --model google/gemma-4-31b-it` and later with `--judge openai --model gpt-6.1-sol --reasoning-effort high --parallel-arm <gemma's gapmap.json>`. The parallel arm is required because both ledgers have OpenAI-family verifiers (ADR 0009, D1b plan §2.3). Each run has `--max-usd` and `--spend-ledger research/d1c/<name>/{openrouter,openai}_spend.jsonl`. Caps are cumulative per spend ledger.

### 3.4 Pool, topic review, count

`build_sheet.py pool --codebase CFG` runs before any closure state is read. Then a fresh subagent sees only one representative text per topic and flags duplicates. It never sees arms or states. **Changed from D1b:** the owner does not review the topic list. In D1b he read every candidate topic before answering. On a codebase he wrote, that is an advance look at every question, so D1c keeps him naive until collection. Then `count` (Stop A) and `build`.

## 4. Stop rules

- **Stop 1, before any paid call ($0).** The owner confirms the codebase, the docs list and the outside pages, and sets the stage caps (§8). If the corpus has fewer than 8 owner docs, the session reports this, because the D1b pool came from 16 owner docs.
- **Spend gate A1, after Stage 1 (§8).** `pool --ledger cheap --pool <root>/pool_cheap.json`, then `count --unreviewed --arm gemma=… --pool <root>/pool_cheap.json`, printing aggregates only. **This is a funding gate, not a result.** The top-tier ledger can add topics of its own, so the cheap ledger alone is not a bound. In D1b, top-tier-only topics were 3 of 35. The session reports the count, and the owner either funds Stage 2 or records D1c as **"not run (unfunded at A1)"**, which is not Change and not Stop A. This keeps the cheap arm from settling any decision (`CLAUDE.md`). The session recommends not funding when the cheap-ledger matched-pair count is below 7: reaching 10 would then take at least 3 more matched pairs from top-tier-only topics, about twice D1b's total of top-tier-only topics.
- **Stop A (D1b plan §3.2, unchanged).** It runs after both ledgers have gemma states and the topic review is done, and before any OpenAI closure call. If the matched upper bound is below 10 per arm, the test stops. Sol can only remove topics, so this is a true bound. This is D1b's own stop, and the session counts before starting any sol run. D1b's ordering slip (sol's paid checks started before the free count) is not repeated.
- **Stop B (D1b plan §5 step 7).** Sol must pass its second G2 gate run (§5.1) and both closure maps must be complete. Only aggregates are shown: pass or fail per check, kappa, pool counts. If either arm fails, the test stops.
- **No reading** (§1) and the **blinding check** (§1) are applied at reveal.

## 5. Judges

### 5.1 Closure judges (cheap and top-tier arms)

- **Cheap: `google/gemma-4-31b-it`** on OpenRouter. It passed G1 and G2 in D1b, two gate runs, P − N 0.92, lower bound 0.75, R_excess 0. It passes G2 under the disclosed R amendment (D1b plan §2.2).
- **Top-tier: `gpt-6.1-sol`**, reasoning effort high, on the OpenAI API. It passed G1 and the first of its two required G2 gate runs. The second was stopped at D1b's Stop A. **It must pass that second run before its states are used** (Stage 3). The R amendment was stated before that run, so it applies to sol as written.
- **Domain transfer, stated.** G1 and G2 were built on the N3 fixtures and on dependence-forecastability, not on the new codebase. G2 tests a reading property ("states the element" vs "is on topic") rather than domain knowledge. Even so, the judges are validated only off-domain, and `RESULT.md` says so. A G2 on the new codebase would consume pool topics or need new ones, so it is an owner decision (§11), and `g2_topics.py` is not generalised for it.
- **Retest:** sol re-asks a seeded 20% of its prompts with the cache bypassed (`retest.py --domain …`). Agreement is reported and never gates (D1b plan §4 R4).

### 5.2 Novelty judges (two families, blind)

Unchanged from D1b plan §3.5. Judge A is a fresh Claude Opus 5.5 subagent. Judge B is Codex `gpt-5.6-sol`. Each judge's only working directory is the temp directory holding `cases.json` (question, answer, the top-10 corpus passages, no arm). Their tool logs are kept. Neither closure judge labels novelty. Both novelty judges are top-tier, so no cheap model judges novelty. Judge B shares the OpenAI family with the top-tier closure arm, and the judge-A clause of §1 answers that.

### 5.3 Canaries, generated per codebase

Each judge must give the expected label on every canary before any real case counts (`novelty.py ingest` refuses otherwise):

| Canary | Built by | Expected |
|---|---|---|
| filler, 40 and 90 words | fixed text | no content |
| copied | the eligible passage the retriever ranks first for the sheet's first question | already written |
| paraphrase | a separate author, from a **seeded** source passage | already written |
| planted | the same author, on that passage's topic | new |

`research/d1b_rerun/canaries.py`:
1. `pick` chooses the source passage by seeded code from the codebase's own corpus. Eligible passages are owner-doc prose blocks of 30 to 150 words with at least two sentences and no table row. The command writes a brief for the author.
2. A fresh subagent writes `fixtures/canaries.json` from the brief alone: a paraphrase, a planted answer stating 2 to 3 invented concrete facts, and their `planted_terms`. It never sees a sheet, a question or an arm.
3. `check` applies code checks that guard what each canary is for. The paraphrase must not pass on lexical match: content-word Jaccard with its source ≤ 0.50, longest shared word run ≤ 6, length within 0.5 to 2 times the source. Its source must also be among the 10 passages the judges are shown, or the label "already written" is unreachable. For the planted answer, every planted term must be absent from the whole corpus, and the answer must share at least 3 content words with the passages shown, so that it is "new" on content and not off-topic. Its Jaccard with any shown passage must be ≤ 0.30.
4. **The owner confirms both labels after his answers are locked**, so that an invented fact on his own codebase cannot cue an answer. Only then does `novelty.py cases` accept them (`canaries.ready`).

Tested on dependence-forecastability's committed corpus (`tests/test_canaries.py`). D1b's hand-written paraphrase and planted answer pass the checks. A verbatim copy, a paraphrase whose source is not shown, a planted term the corpus contains, and an off-topic planted answer each fail. A dry run of steps 1 to 3 on that corpus is in `research/d1c/dryrun-dependence-forecastability/`, with a fresh author and `owner_confirmed` false. The canaries are synthetic, and they gate only the judges' eligibility, never the result. The owner's confirmation is what makes them fixtures, as with G2's plants.

## 6. Cheap and top-tier arms, everywhere a model generates or judges

| Step | Cheap arm | Top-tier arm | How the two combine |
|---|---|---|---|
| Reconstruction | Haiku 4.5, verifier gpt-5.4-mini | Opus 5.5, verifier gpt-6.1-sol | each ledger contributes versions; a topic enters an arm only if all its versions agree |
| Closure | gemma-4-31b-it | gpt-6.1-sol | a topic enters an arm only if both judges agree on every version; kappa reported as an aggregate |
| Novelty | none (both judges top-tier) | Opus 5.5 subagent, Codex gpt-5.6-sol | agreed labels plus the judge-A clause |

Same inputs and prompts in each pair; only the model differs. Each paid run has a hard `--max-usd`. Both arms are reported, and the cheap arm alone settles nothing: A1 is a funding gate, and Stop A is a bound the top-tier arm cannot change.

## 7. The owner's time

| When | What | Time |
|---|---|---|
| Stop 0 | confirm the codebase from the survey; approve this plan; choose the criterion; set the caps | 15 min |
| Stop 1 | confirm the docs list, the outside pages and the pinned commit; state the OpenAI and OpenRouter balances | 10 min |
| A1 | fund Stage 2 or not | 5 min |
| Stop C | type the passphrase for the seal key | 2 min |
| Collection | **30 questions at full size (24 or 20 at the fallbacks), in two sittings of 15, typed answers**; then self-ratings and arm guesses | 60–90 min, plus 15 min |
| After the lock | confirm the two generated canary labels | 5 min |

If the owner meant 15 questions in total, that is 8 + 7, below D1b's floor of 10 per arm, and D1b's rule could not be carried over (owner decision, §11).

## 8. Cost estimate and caps

Measured on D1 (26 docs, 16 owner and 10 outside, `max_doc_chars` 12,000): cheap reconstruction $1.50 (stopped at its cap), top-tier $3.96 (complete); gemma ≈ $0.00046 per closure call; sol ≈ $0.0020 per call; 459 closure prompts over both ledgers (`research/d1b_rerun/*_spend.jsonl`, `research/d1_demonstrator/runs/*/calls.jsonl`).

| Stage | Run | Est. at D1's size | Proposed `--max-usd` |
|---|---|---|---|
| 1 | cheap reconstruction | $1.50 | 1.50 |
| 1 | gemma closure, cheap ledger | $0.15 | 0.30 |
| **1 total** | | **$1.65** | **1.80** |
| 2 | top-tier reconstruction | $4.00 | 4.50 |
| 2 | gemma closure, top-tier ledger | $0.10 | 0.20 |
| 3 | sol second G2 gate run | $0.15 | 0.30 |
| 3 | sol closure, both ledgers (parallel arm) | $0.95 | 1.50 |
| 3 | sol retest, 20% | $0.20 | 0.30 |
| — | novelty judges, canary author, topic reviewer | $0 (session subagents, Codex) | — |
| **All** | | **≈ $7.05** | **≈ $8.60** |

**The proposed $3.00 cap covers Stage 1 and the A1 gate, not the whole test.** At D1's corpus size, the whole test costs about $7. Costs scale with the corpus, at about $0.27 per document. A whole test under $3.00 would need about 11 documents in all, and on D1b's yield (about 2 topics per document before review) that would very likely stop at A. So the plan proposes **$3.00 for Stage 1**, and a second cap the owner sets at A1 for Stages 2 and 3. The figures are recomputed from the confirmed corpus at Stop 1. Before every paid stage, the session runs `scripts/key_headroom.py` and the owner states the OpenAI balance.

## 9. Order and stop points

1. **Stop 0.** The owner confirms the codebase, approves this plan, chooses the criterion and sets the Stage 1 cap.
2. **Phase 1 ($0).** Copy the template to `research/d1c/<name>/codebase.json`. Clone the checkout into `source/` (git-ignored) at the pinned commit. Fill the lists, run `corpus_build.py`, recompute §8 from the corpus, then run `canaries.py pick` to confirm eligible passages exist.
3. **Stop 1.** The owner confirms the lists and the commit. The seed is fixed. `RULE.md` (draft) is committed with the hashes of `rule.py`, `build_sheet.py` and `codebase.json`.
4. **Stage 1 (paid, cap $1.80 of $3.00).** Cheap reconstruction, then gemma on the cheap ledger.
5. **A1.** The aggregate count from the cheap ledger alone. The owner funds Stages 2 and 3 or records "not run".
6. **Stage 2 (paid).** Top-tier reconstruction, then gemma on the top-tier ledger. Then pool, topic review by a subagent, and **Stop A** (free).
7. **Stage 3 (paid, OpenAI).** Sol's second G2 gate run, sol closure on both ledgers, retest. **Stop B.**
8. **Phase 4 ($0).** Build, seal, rerun the L7.3 checks, and `methods-critic` on `RULE.md`. **Stop C:** the passphrase.
9. **Phase 5.** Collection, the lock, self-ratings, guesses.
10. **Phase 6 ($0).** The canary author writes, `canaries.py check` runs, and the owner confirms the canaries. Then `cases`, both judges, `ingest` (canaries must pass), `reveal` (rule, length-only reading, blinding), `RESULT.md`, and `citation-verifier` on everything changed under `research/`.

## 10. Code (built at $0; offline tests, fake judges, no network)

- `research/d1b_rerun/codebase.py` and `codebase.json`: the config layer. `build_sheet.py` (pool, count, build) and `novelty.py` (lock, cases, ingest, reveal) take `--codebase`, with D1b's config as the default. `retest.py` takes `--domain`. `build_sheet.py pool --ledger` and `count --unreviewed` serve A1. `novelty.py reveal` adds the blinding check from `guesses.json` (D1b plan §3.3 specified it, but the script did not compute it).
- `research/d1b_rerun/canaries.py`: §5.3.
- `research/d1b_rerun/corpus_build.py`: §3.1.
- `research/d1c/codebase.template.json`, `research/d1c/.gitignore`, `research/d1c/dryrun-dependence-forecastability/`.
- **Replay:** with the default config, `build_sheet.py pool` rewrites `pool.json` and `fixtures/topic_review_pack.md` byte-identically, and `rule.py` rewrites `rule_checks.json` identically. A test covers the pool and the pack.
- Not generalised: `g1.py`, `g2.py`, `g2_topics.py`, `g4_standins.py`. G1 and G2 are judge checks on fixed fixtures and are reused as they are (§5.1). G4 is reported only, and was expected not to gate (D1b plan §2.2).

## 11. Open until the codebase is known, and owner decisions

Open:
- The docs list, the outside pages, the commit, `domain`, `task` and `seed` (§2).
- Whether the open side is large enough. That is what the survey estimates, and only Stop A settles it.
- The cost recomputed from the confirmed corpus (§8).
- Whether a cheap-arm reconstruction cap hit leaves the two ledgers too unequal (reported).
- Whether enough eligible owner-doc prose exists for the canary source (`canaries.py pick` says so at $0).

Owner decisions:
- **Budget:** $3.00 for Stage 1 plus a second cap at A1 (proposed), or one cap of about $8.60 set now, or a corpus of about 11 documents under $3.00.
- **Criterion:** (b), as in D1b (proposed), or (a), if a blind coder is found.
- **Sheet size:** 30 questions as in D1b (proposed), or about 15, which would break the carried-over rule.
- **Domain-transfer G2 for the closure judges:** not run, with the validation domain disclosed (proposed), or a G2 on the new codebase (owner confirmation of about 50 to 100 sentences, and topics taken from the pool).
