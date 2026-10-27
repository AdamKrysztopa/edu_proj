# Plan: D1c, the gap-map targeting test on a second codebase (2026-10-27)

D1b asked a question it could not answer on dependence-forecastability: only 7 of 35 fresh topics were open in every version, against a floor of 10 per arm (`research/d1b_rerun/RESULT.md`). D1c asks **the same question on another codebase the owner wrote**. It keeps D1b's rule, arms, blinding and judges wherever possible (`docs/plans/gapmap-fix-and-d1-rerun.md`, cited below as "D1b plan §x"). Like D1 and D1b, it is exploratory: one expert, who built both the system and the codebase. It feeds no N3 gate and is not RQ-B evidence. N3 stays paused with its registered rules unchanged (`REORIENTATION.md` §22).

**Status:** a draft for the owner's approval. It was built at $0 and revised after two rounds of `methods-critic`. Round 1 had eight blocking findings and round 2 had four. All are applied below; §12 lists them, and a third round checks them. No codebase is chosen here. A parallel gap-density survey recommends one, the owner confirms it, and only then is `codebase.json` filled in (§2). Every paid run in §8 happens later, under caps the owner sets.

## 1. Question and decision rule, carried over

**Question (D1b, unchanged).** On a codebase the owner wrote, do questions aimed at the gap map's open spots draw out more knowledge the docs lack than questions aimed at its closed spots?

The following carry over unchanged:

- **Arms** (D1b plan §3.2). A topic is *gap* if and only if every closure judgement of every ledger version of it, by both closure arms, is open. It is *covered* if and only if all of them are closed. Anything else goes to neither arm. The arms are matched by seeded code within strata (lens; k_topic band, 1 or ≥ 2; ledgers of origin; source origin) on question length and retrieval similarity. Their means must lie within 10% (`build_sheet.match`, `balance`).
- **Size and fallbacks** (D1b plan §3.2). 15 + 15. If that is not possible, 12 + 12, then 10 + 10. With fewer than 10 matched, balanced topics per arm, the test stops (§4).
- **Rule** (D1b plan §3.4, `research/d1b_rerun/rule.py`, the code unchanged).
  - **Continue** if and only if the gap arm's "new" rate minus the covered arm's is ≥ 0.30, with a one-sided exact permutation p ≤ 0.10, on the criterion labels. Under criterion (b) it must hold both on the two judges' agreed labels and on judge A's labels alone.
  - Otherwise **Change**.
  - **No reading** if fewer than ⌈8N/15⌉ answers, where N is the total number of answers on the sheet (16 of 30), carry content by both judges. No reading counts as Change.
  - The L7.3 checks (`rule_checks.json`) are rerun and must pass before the sheet is shown.
- **Operating characteristics** (D1b plan §3.4; SYNTHETIC simulation; base rate 0.58, judges 0.9 accurate). Under (b) with the judge-A clause, P(Continue) is:
  - at 15/15: 0.03 under no difference, 0.33 at +0.30, 0.52 at +0.40, 0.71 at +0.50;
  - at 10/10: 0.03, 0.23, 0.37 and 0.54.
  - **A Change cannot separate "the map does not target" from "the effect is below about 0.4."** `RESULT.md` prints this.
  - **The canary void lowers these figures.** If each judge were 0.9 accurate on each canary independently, both would pass all five with probability of about 0.35 (§5.3), and P(Continue | +0.30) at 15/15 would fall to about 0.33 × 0.35 ≈ 0.12. Canaries are built to be easier than that, but no measurement shows it yet.
- **Secondary readings, never gating** (D1b plan §3.4): a labeller that uses answer length only; the number of new content units; the owner's self-ratings; and each closure arm's assignment on its own, revealed with the key.
- **Blinding** (D1b plan §3.3). Per-candidate states, caches, rebuilt maps and the key are git-ignored (`research/d1c/.gitignore`), then sealed to the owner's RSA public key. The builder prints only aggregates and hashes. Once every answer is hash-locked, the owner guesses each question's arm; `novelty.py reveal` reads `guesses.json`. **The guess accuracy is reported as a descriptive figure, whatever its p.** D1b's "unblinded" flag (accuracy ≥ 0.70 at p < 0.05) is kept, but at 30 questions a true accuracy of 0.70 trips it only about 59% of the time. The owner wrote these docs and knows what they cover, so a Continue may still partly reflect that knowledge, and `RESULT.md` says so.
- **Collection** (D1b plan §3.6). One question at a time in chat, typed answers, no follow-ups, two sittings split at question 15. The answers are locked first (`novelty.py lock`), then the self-ratings and the arm guesses are taken in one pass.

**Criterion.** D1b's owner chose (b): the LLM judges' labels, advisory. D1c proposes the same. (a), the one blind second coder, stays open (§11).

**What each outcome triggers.** It is fixed in `RULE.md` at approval and adapted from D1b plan §3.7. D1b was recorded as Change, so gap-map targeting is not a pilot claim today.

- **Continue under (a):** targeting may become one of the pilot's claims, which revises D1b's Change.
- **Continue under (b):** the result is advisory. Targeting becomes a candidate claim that the pilot's own design may test. It is not a claim.
- **Change, No reading, any Stop A, or "not run":** D1b's Change stands, and ranking work waits for N3. A Stop A is recorded as "targeting not testable on two of the owner's codebases", not as a negative result.
- **What the owner buys** for about $10 to $12 and about 2.5 hours of his time (§7, §8): under (b) a Continue moves targeting from "dropped" to "worth designing into the pilot", and a Change closes the ranking line until N3 resumes. Neither changes a registered rule. Under (b) the power is 0.33 at +0.30, so the decision value is modest, and the owner should weigh it before Stage 1 (§11).

## 2. The codebase as a parameter

Everything codebase-specific lives in one JSON file, `research/d1c/<name>/codebase.json`. It is copied from `research/d1c/codebase.template.json` on the day the owner confirms the codebase. `codebase.load` refuses any file that still holds a `TODO`, and refuses an excluded repository (§4, Stop 0). Relative paths resolve against the file's directory, which is also where the outputs go.

| Field | What it is | Filled when |
|---|---|---|
| `name`, `owner_repo` | the repository; `owner_repo` marks a source as the owner's (source-origin stratum) | Stop 0 |
| `domain` | the label for `gapmap --domain`, `retest.py --domain` | Stop 0 |
| `seed` | the matching, shuffle and canary-source seed; fixed in `RULE.md` before any closure call | Stop 1 |
| `corpus`, `corpus_build` | pinned commit, owner docs, outside pages (§3.1) | proposed by the session, confirmed by the owner at Stop 1 |
| `reconstruct` | domain line, task, `max_doc_chars` 12,000, `max_results` 5, the cheap and top-tier model files (D1's) | Stop 1 |
| `ledgers` | the two reconstruction run directories | after each run |
| `prior_items` | earlier questions on this codebase to exclude by topic overlap (D1's 15 for D1b) | `null` for a codebase never tested |
| `canaries`, `canary_mode` | `generated`: canaries from this codebase's own corpus (§5.3) | Phase 6 |

D1b's `research/d1b_rerun/codebase.json` is every script's default. It replays D1b's committed `pool.json`, the topic-review pack and `g4_standins.json` byte for byte (`tests/test_codebase.py`; the replays were run).

With `prior_items: null`, step 1 of D1b's fresh-question filter (D1b plan §3.1) has nothing to exclude, and the topic review (step 4) checks only for duplicates among the topics. Debris filtering and clustering are unchanged.

## 3. Inputs built per codebase

### 3.1 Corpus

`research/d1b_rerun/corpus_build.py --codebase CFG` reuses D1's converter and fetchers unchanged.

- **Owner docs.** The user-facing docs at a commit the owner pins: README, quickstart, how-tos, theory or explanation pages, reference pages. Generated API dumps, changelogs and licences are left out. The aim is 12 to 20 docs. The builder refuses a checkout at another commit, a checkout with uncommitted changes, and a listed doc that is missing.
- **Outside pages.** About 10 Wikipedia or library-reference pages on the codebase's methods. Without them no gap can reach k_topic ≥ 2 (D1b plan §1.3). The session proposes them from the README's method names, and the owner confirms both lists at Stop 1.

### 3.2 Reconstruction, both arms (N2 package, unchanged)

`python -m reconstruct.run --live --corpus <corpus>/manifest.json --domain … --task … --max-doc-chars 12000 --max-results 5 --models M --max-usd X --out <root>/runs/<arm>` is run with the same corpus and task for both arms:

- **Cheap arm:** `reconstruct/models.json`. Haiku 4.5 for planner, extractor and baseline; gpt-5.4-mini as verifier.
- **Top-tier arm:** `research/d1_demonstrator/models_toptier.json`. Opus 5.5; gpt-6.1-sol as verifier.

**Completeness rule.** A run is **incomplete** if `codebase.reconstruction_problems(run_dir)` returns anything. That happens when the sidecar is not `complete`, when it lists `incomplete_reasons` (a cap stop, for instance), or when any task's `failed_calls_by_task` is non-zero. Failures are counted after retries, so a transient error that a retry fixed does not count (tested). The sidecar's own `complete` flag is not enough, because it only means that no exception or budget stop ended the run. An incomplete ledger does not enter D1c. The stage stops, and the owner either tops up the account and reruns that arm from scratch, once, or records D1c as "not run (incomplete inputs)". Without this rule the two arms would differ in coverage as well as in model. **Neither D1 ledger was complete**:

- The cheap arm stopped at its $1.50 cap partway through cross-verification and ran no decoys.
- The top-tier arm's sidecar says `complete: true`, yet it records 761 failed cross-verifications, 30 failed decoys and 32 failed verifications, all HTTP 402.

Both are flagged by the rule (tested on D1's committed runs). D1's `RESULT.md` calls the top-tier run "complete"; that word came from the sidecar flag, and it is reported as a lesson candidate.

### 3.3 Gap maps, both closure arms

The gap map is built with `python -m gapmap --ledger L --sidecar S --domain <domain> --out <root>/closure/<arm>/<ledger> --max-usd X --spend-ledger F`:

- **Cheap arm:** `--judge openrouter --model google/gemma-4-31b-it`, writing to the spend ledger `research/d1c/<name>/openrouter_spend.jsonl`.
- **Top-tier arm:** `--judge openai --model gpt-6.1-sol --reasoning-effort high --parallel-arm <gemma's gapmap.json>`, writing to `research/d1c/<name>/openai_spend.jsonl`. The parallel arm is required because both ledgers have OpenAI-family verifiers (ADR 0009).

Both spend ledgers are new and start at $0. **Caps are cumulative per spend ledger**, because the judge counts each ledger's earlier spend (`gapmap/src/gapmap/judge.py`). §8 gives the cumulative figure for every run.

### 3.4 Pool, topic review, count

1. `build_sheet.py pool --codebase CFG` runs before any closure state is read.
2. **Review.** A fresh subagent runs the registered prompt `research/d1c/topic_review_prompt.md`. It sees only the candidate-topic list, with no arm and no state, keeps the lowest ID of each group and drops the rest.
3. **Lexical backstop.** At the same point, before any closure state is read, `build_sheet.lexical_drops` drops the higher ID of any pair whose quoted spans reach content-word Jaccard 0.30. It reads only topic text. It is inert on D1b's pool, where the largest pairwise Jaccard is 0.22.
4. **Changed from D1b:** the owner does not review the topic list. On a codebase he wrote, reading the list would give him an advance look at every question.
5. **Recall check.** The subagent review is checked against the owner's D1b review: the same prompt is run blind on D1b's candidate topics (`research/d1c/review_check/`). Its recall of the owner's 10 within-pool "same as T…" drops is scored; the other 6 drops were "same as D1-Q…", which a new codebase does not have. **The floor, registered before the run, is recall ≥ 0.8.** Below it, two independent reviewers run, and their union of drops is used. If that is also below the floor on D1b, the owner reviews, and the advance look is disclosed. The result is recorded in §12.

## 4. Stop rules

- **Stop 0, before anything.**
  - *Exclusion check.* The session confirms that the codebase is none of these:
    - `AdamKrysztopa/informant-video`, E-ABST's private-objective repository (`reconstruct/src/reconstruct/eabst.py`), still registered as future validation;
    - edu_proj itself;
    - anything carrying physics-conservation content (`REORIENTATION.md` §18.1);
    - any domain of N3's gold set (`REORIENTATION.md` §22, threshold table; `research/ds1-gold-availability.md`), meaning DS1's ranked golds:
      - surgical and clinical procedures;
      - fireground incident command (Okoli);
      - en-route air traffic control;
      - urban-operations (MOUT) small-unit training;
    - any repository in E-OSS's departure corpora: the 133 projects [109], Chromium plus 7 [111], the 1,932 projects [112].
    
    `codebase.load` refuses the two repositories in code, normalising scheme, case and `.git`, and checking both `owner_repo` and `corpus_build.repo_url`. The session confirms the rest in writing.
  - *Survey.* The gap-density survey may show the owner per-codebase aggregate scores only, never topic-level text. No closure state from the survey feeds D1c's arms: D1c rebuilds every ledger and gap map. The choice of codebase is a decision, so the survey must be model-free ($0), or else run a top-tier parallel arm beside any cheap model it uses (`CLAUDE.md`).
  - *Data.* The session states that the codebase's docs go to OpenRouter's providers and to OpenAI, and the owner's answers to the session and to Codex.
- **Stop 1, before any paid call.** The owner confirms the lists and the commit, and states the OpenAI and OpenRouter balances. `scripts/key_headroom.py` runs, and its output, the sum of caps, and whether Codex bills the same OpenAI key are written into `RULE.md`. If there are fewer than 8 owner docs, the session reports it: D1b's pool came from 16.
- **Spend gate A1, after Stage 1. This is a funding gate, not a result.**
  - **Procedure.** Run `pool --ledger cheap --pool <root>/pool_cheap.json`. The same subagent duplicate review runs on that pool and writes `<root>/fixtures/topic_review_cheap.json`. Then run `count --review <that file> --arm gemma=… --pool <root>/pool_cheap.json`, which prints aggregates only, including `matched_pairs_uncapped`.
  - **Why the count overstates.** In D1b's replay (offline, on D1b's gemma caches), the cheap ledger alone, unreviewed, gave 10 matched pairs; `methods-critic`'s mapping of D1b's drops onto that pool gives 6; the real Stop A count after adding the top-tier ledger and the review was 3. Adding the top-tier ledger moved topics into the "both ledgers" stratum and made some gap topics mixed, so it mostly subtracted.
  - **Decision.** The session recommends funding Stages 2 and 3 only if the reviewed, uncapped cheap-ledger count is at least **30**. D1b's count halved from 6 to 3, so a count of 20 would leave an expected 10, exactly the floor and a coin flip, before sol removes anything. At 30, about 15 remain before sol. This rests on one data point, and is disclosed as such. The owner decides. If he does not fund, D1c is recorded as **"not run (unfunded at A1)"**: not Change, not Stop A, and no inference. The cheap arm therefore settles nothing (`CLAUDE.md`).
- **Stop A, after Stage 2** (D1b plan §3.2). Both ledgers have gemma states, and the full pool has been reviewed. The test stops if `matched_pairs_upper_bound` is below 10 (the code reads only the pair count: `stop_at_A` in `count_summary`). Sol can only remove topics, so the bound holds. This holds because `match` has no caliper, so the pair count is the sum over strata of min(gap, covered). Balance is not monotone, so it is checked only at `build`. The count runs before any sol closure or G2 call. (The top-tier reconstruction's gpt-6.1-sol verifier has already run by then.) This avoids D1b's ordering slip, where sol's paid checks started before the free count.
- **Stop B, in Stage 3.**
  - Sol's second G2 gate run comes first, before any sol closure call. If it fails, the stage stops with only $0.30 spent on that ledger.
  - Then both sol closure maps must be complete.
  - Only aggregates are shown: pass or fail per check, kappa, pool counts, and both arms' figures.
- **Stop A (after sol).** If `build` cannot fill 10 balanced pairs per arm after sol's states are joined (`build` exits 3), the outcome is "Stop A (after sol)", with Stop A's consequences.
- **No reading** (§1). It is also triggered if any canary is mislabelled by either judge (§5.3).

## 5. Judges

### 5.1 Closure judges (cheap and top-tier arms)

- **Cheap: `google/gemma-4-31b-it`.** It passed G1, and passed G2 twice on 13 gate topics: P − N 0.92, lower bound 0.75. It passes G2 **only under the R amendment, which was made post hoc on its own data** (D1b plan §2.2).
- **Top-tier: `gpt-6.1-sol`, high effort.** It passed G1 and the first of its two required G2 gate runs. The second is run in Stage 3, under the R amendment, which was stated before that run.
- **Domain transfer.** G1 and G2 were built on the N3 fixtures and on dependence-forecastability. The claim that G2 tests a reading property ("states the element" against "is on topic") rather than domain knowledge is **an assumption**. On the new codebase, the closure judges are therefore validated off-domain only, and `RESULT.md` says so.
- **On-domain evidence at $0.** `g4_standins.py --codebase CFG` (now parameterised) runs the length, lexical-overlap, specificity, source-count, lexicon and coin-flip stand-ins through the mismatched-evidence control on the new ledgers. `RESULT.md` reports:
  - the control for both judges;
  - the lexical stand-in;
  - judge-against-lexical agreement;
  - gemma–sol kappa.
  
  None of these gates. As in D1b, the control is expected to be unable to certify a judge (D1b plan §1.5, §2.2 G4).
- **A new G2 on the codebase** is an owner decision (§11). It is not built.
- **Retest.** Sol re-asks a seeded 20% of its prompts with the cache bypassed (`retest.py --domain …`). The result is reported and never gates.

### 5.2 Novelty judges (two families, blind)

Unchanged from D1b plan §3.5:

- **Judges.** Judge A is a fresh Claude Opus 5.5 subagent. Judge B is Codex `gpt-5.6-sol`.
- **Isolation.** Each judge's only working directory is a temp directory holding `cases.json`. Their tool logs are kept.
- **Families.** Both novelty judges are top-tier, so no cheap model judges novelty. Judge B shares the OpenAI family with the top-tier closure arm; the judge-A clause in §1 answers that.
- **Changed from D1b, in code.** Canaries and real cases now sit in **one** `cases.json`, at random positions and under random 8-hex IDs. D1b had a separate `canaries.json` with IDs such as `c-new`, so a judge could pass the gate by reading IDs. The ID map, `case_map.json`, stays in the codebase directory, outside the judges' directory. It is hashed when `cases` runs, and its hash goes into `RULE.md` before any judge call.
- **One pass per judge.** Each judge's raw output is committed, with its hash, the moment it returns, before `ingest`. `ingest` refuses a second pass and records both hashes, so a rerun judge would show up as a hash change. The judges' tool logs are kept as evidence of what each one read.
- **Canary questions look like real cases.** The filler and copied canaries carry spare questions: lens-template questions from pool topics that are not on the sheet (`novelty.spare_questions`). They no longer repeat the sheet's first question. The author writes the paraphrase and planted questions in the same template style, from three other spare questions shown in the brief. No expert answer to any spare question exists.

### 5.3 Canaries, generated per codebase

| Canary | Built by | Expected |
|---|---|---|
| Filler, 40 and 90 words | fixed text | no content |
| Copied | the eligible passage the retriever ranks first for the sheet's first question | already written |
| Paraphrase | a separate author, from a **seeded** source passage | already written |
| Planted | the same author, on that passage's topic | new |

Steps (`research/d1b_rerun/canaries.py`):

1. **Pick.** `pick` chooses the source passage by seeded code. Eligible passages are prose blocks from the owner's docs, 30 to 150 words, with at least two sentences and no table rows. It also writes the author's brief.
2. **Write.** A fresh subagent writes `fixtures/canaries.json` from the brief alone. It runs in a temp directory holding only the brief and a copy of the corpus, because by Phase 6 `answers.md` exists in the codebase directory. It never sees a sheet, a question or an arm.
3. **Check.** `check` applies these code checks:
   - **Paraphrase.** Content-word Jaccard with the source ≤ 0.50; longest shared word run ≤ 6; length 0.5 to 2 times the source. The source must rank in the top 10 passages the judges are shown for question plus paraphrase, and the failure message gives the rank.
   - **Planted answer.** No planted term occurs anywhere in the corpus. The answer shares ≥ 3 content words with the shown passages, so it is not off-topic, and its Jaccard with any shown passage is ≤ 0.30.
   - **Trivial labellers.** Three trivial labellers must each mislabel the paraphrase or the planted answer: "new if it contains a digit", "the longer answer is new" (the planted answer may be at most 20% longer), and "the answer with less word overlap with the shown passages is new" (the planted answer's overlap may not be lower). Lexical overlap is the stand-in that passed G4 on D1b.
4. **Confirm.** The owner confirms both labels **after his answers are locked**, so that an invented fact about his own codebase cannot cue an answer. If he rejects one, a fresh author rewrites it before any judge sees it.
5. **Freeze.** `canaries.json` and its expected labels are hashed into `RULE.md` before any judge call. They are not regenerated once a judge has run.
6. **Gate.** A canary mislabelled by either judge voids that judge: the outcome is **No reading** (counts as Change), with the rule's figures still reported (`novelty.reveal`). D1's judges passed their canaries. If each judge were 0.9 accurate on each canary independently, both would pass all five with probability of only about 0.35. Canaries are meant to be easy, but this risk is stated before any judge is run.

Tests on dependence-forecastability's committed corpus (`tests/test_canaries.py`):

- **Fail cases:** a verbatim copy, a paraphrase whose source is not shown, a planted term the corpus contains, an off-topic planted answer, and each trivial labeller all fail.
- **D1b's hand-written pair:** it passes every check except length matching.
- **Dry run:** a fresh author wrote canaries from the brief alone (`research/d1c/dryrun-dependence-forecastability/`, `owner_confirmed` false). The final pair passes every check, and each round exposed a defect:
  - **First round:** the check gave no rank and no hint, so the author could not tell which input to change.
  - **Second round:** the digit and length labellers both passed the pair.
  - **Third round:** the overlap labeller passed it, at 0.093 against 0.135.
  
  The author also pointed out that the brief's examples are real candidate questions. They are spare questions never put to the owner, and the brief now says so.

The canaries are synthetic. They gate only the judges' eligibility, never the result, and the owner's confirmation is what makes them fixtures.

## 6. Cheap and top-tier arms

| Step | Cheap arm | Top-tier arm | How they combine |
|---|---|---|---|
| Reconstruction | Haiku 4.5, verifier gpt-5.4-mini | Opus 5.5, verifier gpt-6.1-sol | each complete ledger adds versions; a topic enters an arm only if all versions agree |
| Closure | gemma-4-31b-it | gpt-6.1-sol | a topic enters an arm only if both judges agree on every version; kappa reported |
| Novelty | none (both judges are top-tier) | Opus 5.5 subagent, Codex gpt-5.6-sol | agreed labels plus the judge-A clause |

Within each pair, the inputs, prompts and corpus are the same; only the model differs, and the completeness rule (§3.2) keeps that true. Every paid run has a hard `--max-usd`. Both arms are reported, and the cheap arm alone never settles anything: A1 is a funding gate, and Stop A is a bound the top-tier arm cannot raise.

## 7. The owner's time

| When | What | Time |
|---|---|---|
| Stop 0 | confirm the codebase and its exclusion check; approve; choose the criterion; set the Stage 1 cap | 15 min |
| Stop 1 | confirm the docs, outside pages and commit; state the balances | 10 min |
| A1 | fund Stages 2 and 3, or not | 5 min |
| Stop C | type the seal key's passphrase | 2 min |
| Collection | **30 questions at full size (24 or 20 at the fallbacks), two sittings of 15, typed answers**; then self-ratings and arm guesses | 60–90 min, plus 15 min |
| After the lock | confirm the two generated canaries | 5 min |

If "about 15 questions" was meant as the total, that is 8 + 7, below D1b's floor of 10 per arm, and D1b's rule could not be carried over (§11).

## 8. Cost estimate and caps

The figures are measured per call (`research/d1_demonstrator/runs/*/calls.jsonl`, `research/d1b_rerun/*_spend.jsonl`) and projected to a **complete** run at D1's size: 26 docs, `max_doc_chars` 12,000, 459 closure prompts over both ledgers.

- **Cheap reconstruction:** extract $0.016, verify and cross-verify about $0.001 each, decoys at extraction cost. About $2.30.
- **Top-tier reconstruction:** extract $0.082, verify $0.0030, cross-verify $0.0027, decoys priced between verify and extract cost. $6.10 to $8.60.
- **Closure:** gemma $0.0005 per call, sol $0.0020 per call.

| Stage | Run | Spend ledger | Est. | Cap for the run | Cumulative cap on its ledger |
|---|---|---|---|---|---|
| 1 | cheap reconstruction | its own `calls.jsonl` | $2.30 | 2.75 | — |
| 1 | gemma, cheap ledger | `openrouter_spend.jsonl` | $0.14 | 0.30 | 0.30 |
| 2 | top-tier reconstruction | its own `calls.jsonl` | $6.10–8.60 | 9.50 | — |
| 2 | gemma, top-tier ledger | `openrouter_spend.jsonl` | $0.09 | 0.25 | 0.55 |
| 3 | sol, second G2 gate run (`g2.py --split gate`) | `openai_spend.jsonl` | $0.15 | 0.30 | 0.30 |
| 3 | sol, cheap ledger (parallel arm) | `openai_spend.jsonl` | $0.55 | 0.80 | 1.10 |
| 3 | sol, top-tier ledger (parallel arm) | `openai_spend.jsonl` | $0.37 | 0.60 | 1.70 |
| 3 | sol retest, 20% | `openai_spend.jsonl` | $0.18 | 0.40 | 2.10 |
| — | novelty judges, canary author, topic reviewer | — | $0 (session subagents, Codex) | — | — |
| **All** | | | **$9.80–12.30** | | **sum of caps $14.90** |

- **Which figure to pass.** For closure runs, `--max-usd` takes the **cumulative** column, because the judge checks earlier spend plus this run's spend against it (`gapmap/src/gapmap/judge.py`). Passing the per-run figure would refuse the top-tier-ledger sol run outright. Reconstruction runs take the per-run cap, since each has its own `calls.jsonl`.
- **Closure caps per ledger.** The 459-prompt closure estimate comes from D1's truncated ledgers. Before each closure run, the session counts that ledger's prompts with a $0 replay through `standins.RecordingJudge` and recomputes the cap.
- **Headroom per provider.** OpenRouter carries both reconstructions and gemma, up to $12.80 of caps; `scripts/key_headroom.py` reads its balance. OpenAI carries sol, up to $2.10, plus Codex if it bills the same key; the owner states that balance. Both go into `RULE.md` beside the caps.
- **Scaling.** Reconstruction costs scale with the corpus: about $0.09 per document for the cheap arm and $0.23 to $0.33 for the top-tier arm. At Stop 1 the session recomputes every row from the confirmed corpus.
- **The proposed $3.00 cap** covers Stage 1 and the A1 gate for corpora up to about 25 documents (cap 2.75 + 0.30 at 26 docs). It does not cover the whole test. Stages 2 and 3 need a second cap, which the owner sets at A1.
- **A whole test under $3.00** would mean a corpus of about 6 documents, which would almost certainly stop at A.

## 9. Order and stop points

1. **Stop 0.** Confirm the codebase and its exclusion check, approve, choose the criterion, set the Stage 1 cap.
2. **Phase 1 ($0).**
   - Copy the template.
   - Clone into `source/` (git-ignored) at the pinned commit.
   - Fill in the lists and run `corpus_build.py`.
   - Recompute §8.
   - Run `canaries.py pick` to check that eligible passages exist.
3. **Stop 1.** Confirm the lists and the commit; state the balances; run `key_headroom`. The seed is fixed. `RULE.md` (draft) is committed with the hashes of `rule.py`, `build_sheet.py`, `novelty.py`, `canaries.py` and `codebase.json`, the caps and the headroom.
4. **Stage 1.** Cheap reconstruction (completeness rule), then gemma on the cheap ledger.
5. **A1.** Cheap pool, subagent review, count. The owner funds Stages 2 and 3, or records "not run".
6. **Stage 2.** Top-tier reconstruction (completeness rule), then gemma on the top-tier ledger. Then the full pool, the subagent review and **Stop A** (free).
7. **Stage 3.** Sol's second G2 gate run (stop if it fails), sol on both ledgers, the retest, `g4_standins.py --codebase`. **Stop B.**
8. **Phase 4 ($0).**
   - `build`: near-duplicate refusal; "Stop A (after sol)" if it cannot fill.
   - Seal.
   - L7.3 checks.
   - `methods-critic` on `RULE.md`.
   - **Stop C:** the passphrase.
9. **Phase 5.** Collection, lock, self-ratings, guesses.
10. **Phase 6 ($0).**
    - The canary author writes in an isolated temp directory; `check`; the owner confirms; the canaries are hashed into `RULE.md`.
    - `cases`, whose map hash goes into `RULE.md`.
    - Both judges, one pass each.
    - `ingest`, then `reveal`: rule, length-only reading, blinding, void on any canary failure.
    - `RESULT.md`.
    - `citation-verifier` on everything changed under `research/`.

## 10. Code (built at $0; offline tests, fake judges, no network)

- **`research/d1b_rerun/codebase.py` and `codebase.json`:** the config layer. It refuses `TODO` and the excluded repositories, with names normalised. `reconstruction_problems` implements the completeness rule and is tested on D1's real runs.
- **`build_sheet.py`:**
  - `--codebase`, `pool --ledger`, `count --unreviewed | --review`, and `--pool`;
  - `count_summary` reads Stop A from the pair count alone and reports `matched_pairs_uncapped`;
  - `lexical_drops` acts as part of the review, before any state is read;
  - `build` exits 3 on "Stop A (after sol)".
- **`novelty.py`:**
  - `--codebase`;
  - one mixed, opaque `cases.json` plus `case_map.json`;
  - spare questions for the canaries;
  - a one-pass `ingest` that records the raw-output hashes;
  - `reveal` voids the reading on canary failure and computes the blinding check from `guesses.json`, which D1b's plan specified but its script did not compute.
- **`research/d1c/topic_review_prompt.md`** (the registered prompt) and **`research/d1c/review_check/`** (the recall check, §3.4).
- **`retest.py --domain`** and **`g4_standins.py --codebase`**.
- **`canaries.py`** (§5.3) and **`corpus_build.py`** (§3.1).
- **`research/d1c/`:** `codebase.template.json`, `.gitignore`, and `dryrun-dependence-forecastability/`.
- **Replays, with the default config:** `build_sheet.py pool` rewrites `pool.json` and the review pack, `rule.py` rewrites `rule_checks.json`, and `g4_standins.py` rewrites `g4_standins.json`, all byte-identically.
- **Not generalised:** `g1.py`, `g2.py`, `g2_topics.py`. G1 and G2 run on fixed fixtures and are reused as they are (§5.1).

## 11. Open until the codebase is known, and owner decisions

Open:

- The docs list, outside pages, commit, `domain`, `task` and `seed` (§2).
- The costs recomputed from the confirmed corpus (§8).
- Whether enough eligible owner prose exists for the canary source (`canaries.py pick` reports it at $0).
- Whether the open side is large enough. Only Stop A settles this; A1 and the survey estimate it.
- How the survey measures gap density, and what it shows the owner (§4, Stop 0).

Owner decisions (each with a recommendation):

- **Budget:** $3.00 for Stage 1, with a second cap at A1 of about $12 for a D1-size corpus (recommended). Alternatively, one cap of about $15 set now. A corpus small enough to fit $3.00 in total would not reach Stop A.
- **Criterion:** (b), as in D1b (recommended, because no coder is available). Alternatively (a), if a blind coder is found; it is the only criterion under which a Continue can become a pilot claim.
- **Sheet size:** 30 questions, as in D1b (recommended). About 15 in total would break the carried-over rule.
- **G2 for the closure judges on the new codebase:** not run, with the validation domain disclosed and the free on-domain stand-ins reported (recommended). Alternatively, a G2 built on the new codebase: an owner confirmation of about 50 to 100 sentences, topics taken from the pool, and `g2_topics.py` generalised.
- **Whether to run D1c at all,** given the decision value in §1. Recommended: run Stage 1 only after the survey's figures for the chosen codebase are known.

## 12. Review record

`methods-critic`, round 1 (2026-10-27): "would not run as written; with the eight blocking fixes, yes." The blocking findings and where each is applied:

1. Truncated D1 runs in the cost table: §3.2, §8.
2. Cumulative caps: §3.3, §8.
3. A1 overstated on D1b's own data: §4, reproduced.
4. Canary IDs gave away the labels: §5.2.
5. No rule for a canary failure: §5.3.
6. No exclusion check: §4, Stop 0.
7. Stop A as coded included balance: §4, in code.
8. The survey unspecified: §4, Stop 0; §11.

The non-blocking findings are applied in §3.1 (a clean tree), §3.4 (tie-break and backstop), §5.1 (on-domain stand-ins, and the assumption stated), §5.3 (stand-in labellers, an isolated author), §1 (descriptive blinding, decision value, the N in the content floor) and §4 (headroom in `RULE.md`, data disclosure).

`methods-critic`, round 2 (2026-10-27): "would not run as written; with B1–B4 fixed, yes." Six round-1 findings were fully applied, one named the wrong domains, and one was only partly applied. The blocking findings and where each is applied:

- **B1.** The completeness rule counted retried calls: §3.2, `reconstruction_problems`.
- **B2.** The exclusion list named the wrong gold domains: §4, Stop 0.
- **B3.** The near-duplicate refusal ran after closure: §3.4, `lexical_drops` at review time.
- **B4.** The subagent review was untested: §3.4.

On B4, the blind review on D1b found 8 of the owner's 10 within-pool duplicates, with no drop outside them. Recall is 0.8, **exactly at the registered floor** (`research/d1c/review_check/score.json`). It missed T040 and T044, both among its own named close calls.

The non-blocking findings are applied as follows:

- **N1.** Spare questions: §5.2.
- **N2.** The overlap labeller: §5.3.
- **N3.** The cumulative column, and caps per ledger: §8.
- **N4.** A1 raised to 30: §4.
- **N5.** Raw hashes: §5.2.
- **N6.** The survey must be model-free or run a parallel arm: §4.
- **N7.** Normalised exclusion: §4.
- **N8.** The canary void in the operating characteristics: §1.
- **N9.** Headroom per provider: §8.
- **N10.** The wording of the Stop A count: §4.
