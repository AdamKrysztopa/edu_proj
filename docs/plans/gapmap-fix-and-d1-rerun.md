# Plan: fix the gap map's ranking, then rerun D1 on fresh questions (2026-10-26)

Two NOW-timeline items, in order: **(1) fix the gap map's ranking** (Nov 2026), **(2) rerun D1 on fresh questions** (Nov–Dec 2026). Both finish before the search for a PW lecturer and volunteers starts. N3 stays paused with its registered rules unchanged (`REORIENTATION.md` §22). Like D1, this is exploratory: one expert, who built the system; it feeds no N3 gate and is not RQ-B evidence. What each outcome triggers is in §3.7.

Status: **approved by the owner, 2026-10-26**, after two `methods-critic` rounds (first draft: "would not run as designed"; second: "with them made, I would run it"; all findings applied). Owner decisions: plan approved as written; **criterion (b)**, LLM judges, advisory (§3.4, §3.7); **total cap $6**, which includes the optional sol G3 run (R5).

## 1. Diagnosis: why D1's ranking failed

Sources: `research/d1_demonstrator/gapmap/{cheap-26b,toptier-26b}/gapmap.json` (checks), `key_revealed.json`, `result.json`, `corpus/manifest.json`, `research/n3_control_v3/RESULT.md`. Figures recomputed on 2026-10-26 and re-verified independently by `methods-critic`.

### 1.1 The closure judge is no better than chance (necessary cause)

| Check on the D1 maps (qwen2.5:7b-instruct) | Cheap ledger | Top-tier ledger | Pass needs |
|---|---|---|---|
| Mismatched-evidence control, own − control (closed or partial) | 0.625 − 0.528 = **+0.097** (n 72) | 0.378 − 0.333 = **+0.044** (n 45) | ≥ +0.20 |
| Lexical donor null, observed closures vs null mean [band] | 16 vs 23.1 [17, 29] | 16 vs 15.2 [10, 20] | above band |
| Judge state = lexical state | 39 of 72 (0.54) | 23 of 46 (0.50) | (descriptive) |

Every lens is flagged on both maps (`closure-uninformative`). The same judge already failed real-judge L7.3 on the N3 domains: 8 of 12 stand-ins closed the own arm (I1c). **Both D1 arms were defined by this judge**: covered = qwen "closed"; gap = qwen "open" and k_topic ≥ 2. With a chance-level judge the covered arm is close to a random draw of fired candidates, and the arms differed mainly in k_topic. D1 could not test targeting; it agrees with the flag, as `RESULT.md` says.

### 1.2 Arm definitions: "covered" did not mean "nothing left to say" (contributing)

- Novelty was high everywhere: 7 of 12 agreed answers were "new" (0.58). Covered drew 2 new of 3 agreed (Q7, Q14). A high base rate compresses any difference.
- Q7 (covered, new/new) quotes a flattened table row; the judge "closed" conversion debris. Q15 (gap, no content) is debris of the same kind. Debris landed in both arms.
- The covered rate rested on **3 agreed answers**; the gap rate on 9.

### 1.3 Corpus and independence keys (contributing; forces an arm change in the rerun)

- One repository is one independence key. On the 16-doc corpus all 27 open candidates were RG-SINGLE and HYP was empty.
- On the 26-doc corpus, candidates at k_topic ≤ 1: **54 of 72** (cheap) and **41 of 46** (top-tier). HYP was 7 and 3; the gap arm needed one RG-SINGLE fallback (Q10, k = 1; new/new).
- So HYP (k ≥ 2) selects topics the outside pages also discuss. In a single-owner corpus k_topic counts Wikipedia/sklearn/statsmodels mentions, not independent attestation of the owner's practice.
- **Binding for the rerun:** after excluding D1's topics (content-token Jaccard < 0.10), the ledgers hold 54 (cheap) and 25 (top-tier) fresh candidates, of which only **5 and 0** have k_topic ≥ 2. A HYP-only gap arm cannot be filled.
- k_topic vs novelty in D1 (agreed answers): k = 1, 2 of 2 new; k = 2, 3 of 8; k = 3, 2 of 2. Uninformative at this n.

### 1.4 Measurement: D1 could not read a working map reliably (contributing)

Simulation of D1's rule (10 gap / 5 covered, 80% judge agreement; SYNTHETIC): P(Continue) is **0.47** at a true +0.30 difference, **0.60** at +0.40, and **0.14** under no difference at a base rate of 0.6. D1's "Change" is weak evidence against targeting.

### 1.5 The real-data null cannot certify any judge on these ledgers (found by `methods-critic`, reproduced)

control2 ranks the own arm by candidate *i*'s probe and the donor arm by *j*'s (`gapmap/src/gapmap/control2.py:120,128-132`), so the own arm is more on-topic by construction. A **lexical-overlap stand-in** (close an arm iff its overlap with the judged question and seed reaches the median) gives **+0.78 [0.67, 0.87]** (cheap) and **+0.78 [0.65, 0.89]** (top-tier) on D1, and +0.68 (PLC) and +0.46 (GDPR v1) on N3, against sol's +0.13 and +0.23. Length (+0.01, +0.11) and source-count stand-ins fail correctly. Only **6 and 1** D1 pairs are overlap-matched within 25%. So control2 cannot show on D1 that a judge reads "states the element" rather than "is on topic", and I1c's MS1-candidate reading for sol is not protected against this stand-in (lesson queued; an implement-queue note, no N3 rule is changed).

### 1.6 What follows

The judge is the fix both arms depend on. Its validity must be shown on a **constructed** check that holds topicality fixed (§2.2), because no real-data null on these ledgers can do it. The k_topic filter must leave the arm definition. Power stays low at any sheet the owner can answer (§3.4).

## 2. The fix

### 2.1 Candidate closure judges, chosen by measurement

**Top-tier arm:** `gpt-6.1-sol`, reasoning effort high, direct OpenAI API. Its I1c L7.3 pass is not taken as evidence here (§1.5); it is screened like every other candidate.

**Cheap arm (other family, hosted on OpenRouter).** ADR 0009 is active: an OpenAI judge on these ledgers (verifier family OpenAI) runs only beside an other-family judge on the same prompts and parser, and a reading counts only where both agree. **Owner decision, 2026-10-26:** no local models (the gemma3 screening run took the Mac down; all Ollama models were deleted); everything non-OpenAI runs through OpenRouter, OpenAI through the OpenAI account. Candidates, priced from OpenRouter's model list on 2026-10-26 (USD per 1M tokens, in / out): `google/gemini-3.5-flash-lite` (0.30 / 2.50), `deepseek/deepseek-v4.1-flash` (0.02 / 1.00), `qwen/qwen3.8-flash` (0.15 / 0.47), `mistralai/mistral-small-2603` (0.15 / 0.60), one per family, all with JSON output, temperature 0 (`gapmap.judge.OpenRouterJudge`). The local `qwen2.5:7b-instruct` baseline was run before the switch and fails G1 and G2 (§2.2); it is kept as the known-failing reference.

**Selection on separate data.** Each candidate runs G1 and the 6-topic selection split of G2 (§2.2). Eligible: passes both. Among the eligible, the larger plant − on-topic-non-answer difference on the selection split wins; ties go to the cheaper model. The chosen model is then gated on G2's 18-topic gate split, which played no part in choosing it. If none is eligible: stop B.

### 2.2 What "the fix works" means, stated before measuring (L7.3)

A judge arm passes only if **G1 and G2** hold. G3 and G4 are reported; G3 never gates; G4 gates only under the condition stated.

- **G1. N3 fixtures, unchanged.** `research/n3_control_v3/l73.py`, its rule as committed: on every planted pair the seed-free own arm is closed and the control is not; no random-letter or length-matched stand-in closes the own arm. For sol, a fresh run that bypasses the I1c cache; for OpenRouter candidates one run (outputs under `research/d1b_rerun/g1/`, through `g1.py`).
- **G2. Topicality-controlled plants on the D1 domain (new, the primary check).** 24 topics, taken from D1's 15 used candidates and 9 further candidates excluded from the rerun pool by topic overlap (so no rerun question is contaminated); debris seeds and seeds that already state the element are dropped and replaced from the excluded pool. The 24 are **clustered by D1 anchor**; whole clusters go to the selection split (about 6 topics) or the gate split (about 18), and the bootstrap resamples clusters. For each topic: the seed and the lens question as the gap map builds them; off-topic background sentences from another candidate's retrieval; and these arms:
  - **0**, no insert (seed plus background only): a judge must close it at ≤ 0.25;
  - **P**, a plain-text plant that states the element (the reason, exception or result); about half state it **with no lens-lexicon marker** (no "because", "unless", "so that", "led to");
  - **N**, an on-topic **concrete fact that is not the element** (a default value, a date, a setting), reusing P's content words, at least as long as P and at most 10% longer, and sharing at least as many seed and question words as P (checked in code, `g2.insert_problem`), so no length or overlap stand-in can favour P; about half carry a lexicon marker vacuously (a "because" that gives no reason);
  - **N+**, N plus 2–3 more on-topic non-element sentences, so the arm resembles a real retrieval with several on-topic non-answers (qwen's I1c failure mode);
  - **R**, a random-letter stand-in with P's word lengths.
  
  P, N and N+ are written by a fresh subagent from a fixed spec, never by the session that builds the arms. **Before any judge call, the owner confirms each P, N and N+ sentence's label, and that the topic's seed does not already state the element** (about 96 sentences, about 30 min; allowed, because these topics are excluded from the rerun; under criterion (a) the coder may do it instead); a sentence the owner rejects is rewritten or its topic dropped.
  
  Pass on the gate split, per judge: close(P) − close(N) **≥ 0.50** with cluster-bootstrap lower bound (5th percentile of 2,000 resamples) **≥ 0.30**, close(0) **≤ 0.25**, close(N) **≤ 0.25**, close(N+) **≤ 0.25**, close(R) **≤ 0.10**; only "closed" counts as closing. Best case reachable: 1.0. **Must fail, run on the real fixtures:** lexical-overlap, length and source-count stand-ins (P and N within 10% by construction), the gap map's own lens-lexicon closure (`lexical_state`), and a specificity count (digits, conditionals, named settings). For sol and the chosen cheap model, the gate split runs twice with the cache bypassed; both runs must pass.
  
  **Pass probabilities of this rule** (SYNTHETIC, 18 topics; `methods-critic`'s simulation): a judge closing P / N at 0.90 / 0.10 passes 0.92; 0.80 / 0.10, 0.85; 0.80 / 0.20, 0.58; 0.70 / 0.20, 0.38. The binding term is the 0.50 mean. A judge that closes R 5% of the time meets R ≤ 0.10 only 77% of the time; two required sol passes at 0.85 each give about 0.72. G2 is built to pass a good judge, not a borderline one.
- **G3. control2 on the D1 ledgers: dropped** (owner, 2026-10-26). §1.5 shows it cannot read here (6 and 1 overlap-matched pairs), it never gated, and its sol run (R5) is dropped to stay within the $6 cap.
- **G4. The gap map's own null (mismatched-evidence control), total only.** Before any judge result, the lexical, length, source-count and coin-flip stand-ins are run on the real D1 MEC arms ($0). G4 gates (own − control ≥ 0.20 in total) only if all four stand-ins fail it there; otherwise it is reported and does not gate. It is expected not to gate: the MEC adds *j*'s retrieval (`gapmap/src/gapmap/checks.py:204`), the same topicality asymmetry as control2. Per-lens flags are reported, not gated (n is 2–5 in several lenses). If no real-data null gates, `RESULT.md` states that the judge is validated only on constructed sets.
- **Pairing (ADR 0009).** On every candidate both arms judge: Cohen's kappa and agreement are reported **as aggregates only** (§3.3). Only candidates where both arms agree enter the rerun's arms.

**Offline proof that the checks discriminate (tests, fake judges, written first).** An oracle fake that closes only when P is present passes G2; a topicality fake (closes iff the inserted sentence overlaps the question) fails G2 (P and N alike); length, coin-flip and source-count fakes fail G2.

### 2.3 Code: additive and selectable

- **`gapmap.__main__`:** `--judge openai --model M --reasoning-effort E --max-usd X --spend-ledger F` (mirroring control2), `--judge openrouter` for the cheap arm (`OpenRouterJudge`, same cap and ledger contract), and `--model` for any of them (default `config.JUDGE_MODEL`, the Ollama baseline). With no flag, behaviour is byte-identical to today. A live OpenAI judge on a ledger of OpenAI generator or verifier family is refused unless `--parallel-arm` names an other-family `gapmap.json` on the same ledger hash (ADR 0009, as in control2). `--no-cache-read` for retests.
- **Stand-in judges** (length, source count, lexical overlap, topicality, coin-flip) as `Judge` objects in a new module `gapmap/src/gapmap/standins.py`. `control2.verdict` and its defaults are not changed; the overlap stand-in is a reported row.
- **G2 fixtures and runner** live in `research/d1b_rerun/fixtures/`, not in `gapmap/tests/l73_fixtures.py` (a manifest CONTROLS file).
- `config.py`, the default judge, `record.categorize` and every `research/n3/*/closure_judgements.json` are untouched. Caches for this work live under `research/d1b_rerun/closure/<ledger>/<judge>/`.
- **Manifest drift, stated:** `gapmap.manifest` hashes the package as a file set, so any change under `gapmap/src/gapmap/` changes the repository SHA. The committed manifest is mechanism-only (no value frozen, I7); it is regenerated at the MS2 freeze, not now. No registered N3 rule reads it today.
- **Tests:** offline, fake judges, red then green. All four suites (`instrument`, `residual`, `reconstruct`, `gapmap`) plus the D1b tests pass before anything is called done. No live call in any test.

## 3. The rerun (D1b)

Directory: `research/d1b_rerun/` (new; D1's files are not changed). Same codebase (dependence-forecastability, commit `904fa30`), same expert (the owner), same two ledgers (cheap-26b, toptier-26b): no new reconstruction, no OpenRouter spend.

### 3.1 Fresh questions, deduplicated at topic level before any arm exists

Applied to every fired lens candidate of both ledgers, **before** judge states are joined:
1. Drop candidates that share a seed claim with any D1 item, or whose quoted span plus anchor has content-token Jaccard ≥ 0.10 with any D1 item's.
2. Drop debris: quotes from markdown table rows, or of more than 12 tokens with no sentence-final punctuation. Fixed in code, applied alike to all.
3. **Cluster into topics** across both ledgers (quote Jaccard ≥ 0.5, or a shared anchor). The critic found 16 of 28 fresh top-tier candidates duplicate a cheap one, with differing closure states in 6.
4. A fresh subagent sees only D1's 15 question texts and one representative text per surviving topic (no arm, no state) and flags shared topics with D1 or with each other; flagged topics are dropped.

### 3.2 Arms

- A **topic** is **gap** iff every closure judgement of every ledger version of it, by both arms, is open; **covered** iff all are closed. Anything else (disagreement, partial, undecided) goes to neither arm.
- **Changed from D1, and why:** D1's gap arm was HYP (k_topic ≥ 2); §1.3 shows only 5 fresh k ≥ 2 candidates exist, and k_topic here counts outside pages. Instead the arms are **matched**, by seeded code hashed in `RULE.md`, on: k_topic band (1 vs ≥ 2), lens, ledger of origin, source origin (owner docs vs outside page), length (mean words within 10%) and the novelty retriever's question-to-corpus top-10 similarity (`research/d1_demonstrator/judge.py`'s retriever; the critic found open items 0.144 vs closed 0.163). L7.4: the arms differ in judged closure; they share ledgers, lenses, k_topic mix, source origin, templates, length and retrieval density.
- Matching on lens may leave a WHY-only sheet (the critic's count on qwen states). That is accepted and reported.
- **Size:** 15 + 15. Fallback, fixed now: 12 + 12, then 10 + 10 (rule below unchanged); fewer than 10 matched topics per arm **stops the rerun**. **Feasibility before any OpenAI spend:** once the cheap arm has judged the fresh pool, the matched-pool upper bound is computed (sol can only remove topics); if it is below 10 per arm, stop at A.

### 3.3 Blinding

- Arm membership is a function of the closure caches, the builder and a seed, so **everything that carries a per-candidate state is sealed with the key**. From Phase 1, `research/d1b_rerun/closure/` and every rebuilt gap-map output (`gapmap.json`, `gapmap.md`, cheap and sol, both ledgers) are git-ignored, so nothing enters git history before reveal; only their sha256 is committed. After the sheet is built, those outputs and `sealed/key.json` are written into one archive and piped into `openssl enc -aes-256-cbc -pbkdf2` under a passphrase the owner types (`! ` with `read -s`); plaintext copies are deleted. The builder prints only hashes and aggregates.
- Residual risk, stated: the cheap arm's states could be regenerated by re-running it on OpenRouter (temperature 0), and covered topics are a subset of cheap-closed ones, so a reader who paid for that re-run would hold a partial predictor of the arms. Codex's sandbox blocks writes, not reads; the judges' tool logs are the evidence of what they read.
- **Stop B shows aggregates only** (pass/fail per check, kappa, pool counts), never per-candidate states.
- I present each question verbatim, one at a time; no follow-ups, no comment beyond "recorded". Residual risk, stated: the orchestrating session ran the builder; it prints no states, and I do not open the caches before sealing.
- **Blinding check:** after all 30 answers are hash-locked, the owner guesses each question's arm. Guess accuracy is reported with its binomial p; accuracy ≥ 0.70 at p < 0.05 marks the result "unblinded" in `RESULT.md`.

### 3.4 Decision rule, fixed and written to `RULE.md` before the owner answers

Two candidate criteria; the owner chooses one at approval (`REORIENTATION.md` §22 and `CLAUDE.md`: synthetic output may be a predictor, never a criterion):
- **(a) Human criterion:** the one blind second coder (the NOW programme's only human input, a labeller, not a participant) labels the 30 answers from `cases.json` (question, answer, the same top-10 passages, no arm) as new / partly / already written / no content. The coder's labels are the criterion; the two LLM judges are secondary.
- **(b) LLM criterion, advisory:** the two LLM judges' agreed labels; the result informs the owner's pilot call and licenses nothing.

The rule, on the criterion labels (on agreed labels under (b)):
- **Continue** iff the gap novelty rate minus the covered rate is **≥ 0.30** and the one-sided exact permutation **p ≤ 0.10**. Under (b), the same must also hold on judge A's labels alone (so a Continue never rests on OpenAI-family agreement alone, §3.5). Otherwise **Change**. If fewer than **16 of 30** answers carry content: **No reading**.
- **Changes from D1:** balanced arms (D1's covered rate rested on 3 agreed answers); D1's "at least 5 gap answers new" clause is **dropped** (at 15 it would make power depend on where the effect sits: +0.50 as covered falling gave 0.39 with the clause, 0.89 without, per the critic); a p ≤ 0.10 requirement is added; the content floor is scaled from 8 of 15 to 16 of 30.
- **Operating characteristics** (SYNTHETIC simulation; each judge correct with probability 0.9, so about 82% agreement; base rate 0.58). Under (b), with the judge-A clause, P(Continue) at 15/15: no difference 0.03; +0.30 0.33 whether the effect is even, gap rising or covered falling; +0.40 0.52; +0.50 0.71. Without the judge-A clause: 0.05, 0.43–0.46, 0.63, 0.81–0.85. At 12/12 with the clause: 0.03, 0.24–0.28, 0.39, 0.57–0.62. At 10/10: 0.03, 0.23, 0.37, 0.54–0.55. **A Change cannot separate "the map does not target" from "the effect is below about 0.4"**; `RESULT.md` prints this.
- **L7.3 checks, run and passing before the sheet is shown:** planted positive (15 new vs 15 already written) → Continue, best case p = 1/C(30,15) ≈ 6.4e-9; all-novel, all-copied, length-matched filler, 7-of-15 vs 4-of-15 new, judge disagreement on the gap answers → Change; stances only → No reading; repeated at 12/12 and 10/10.
- **Secondary, never gating:** a length-only labeller on the real answers (new iff the answer's word count reaches the median), reported beside the result, because longer answers are both a confound and a plausible sign of new knowledge (D1: gap 18.3 vs covered 11.8 words). `RULE.md` states: if the length-only labeller alone also gives Continue, or the blinding check marks the run "unblinded", `RESULT.md` says the Continue cannot be separated from answer length or from unblinding. Also secondary: the count of new content units per answer; the owner's self-ratings (§3.6); each closure arm's assignment alone, revealed with the key.

### 3.5 Novelty judges

- Judge A: a fresh Claude Opus 5.5 subagent. Judge B: Codex `gpt-5.6-sol` (codex-companion). Both run with the temp directory holding `cases.json` as their only working directory (Codex in its read-only sandbox there); tool logs are kept as evidence of what each read. The caches and key are encrypted (§3.3), so recomputing the arms is not possible from the repo.
- Neither closure judge labels novelty. Judge B shares the OpenAI family with the top-tier closure arm; the judge-A clause in §3.4 answers that under (b).
- **Canaries first**, each must pass before any real case: filler → no content; a copied corpus passage → already written; a **paraphrased** corpus passage → already written (a copy passes on lexical match alone); a planted answer with a fact absent from the corpus → new.

### 3.6 Collection

One question at a time in chat, free text; the answer is recorded and the next question follows. Two sittings if the owner prefers, split at question 15, fixed now. All 30 answers are hash-locked before anything else. **Then**, in one pass, the self-rating for each answer ("Could a careful reader of the docs have known this? yes / partly / no / not sure"), then the arm guess (§3.3). Asking about doc coverage after each answer would cue the author on the property that defines the arms. A new `lock` / `judge` / `reveal` script reads the encrypted key; D1's `judge.py` reads a plaintext `sealed/key.json` and is not reused for that.

### 3.7 What each outcome triggers (proposed, fixed in `RULE.md` at approval)

- **Continue under (a):** the pilot search may start with gap-map targeting as one of the pilot's claims; the pilot keeps its own preconditions (`REORIENTATION.md` §22).
- **Continue under (b):** the owner may choose to start the pilot search; targeting is not claimed, because the criterion is LLM-labelled.
- **Change:** gap-map targeting is not a pilot claim. The pilot search may still start, as an elicitation-and-onboarding pilot without targeting; further ranking work waits for N3 to resume.
- **No reading:** counts as Change. Re-collecting on the same sheet is not possible: by then the owner has seen every question and guessed every arm.

## 4. Budget (L7.1, L7.2)

Sol runs use the OpenAI account through `research/d1b_rerun/openai_spend.jsonl`; cheap runs use OpenRouter through `research/d1b_rerun/openrouter_spend.jsonl`. Each judge counts its ledger's prior spend against each run's cap, so the caps are **cumulative per ledger**.

| Run | Provider, model | Est. | Cumulative `--max-usd` |
|---|---|---|---|
| R1 sol on G1 (fresh, cache bypassed) and G2, G2 twice | OpenAI, gpt-6.1-sol high | $0.20 | 0.75 |
| R2 gap map rebuilt with sol, cheap-26b (beside C3, ADR 0009) | same | $0.60 | 2.25 |
| R3 gap map rebuilt with sol, toptier-26b | same | $0.40 | 3.25 |
| R4 sol retest, 20% random subset of R2–R3, cache bypassed | same | $0.20 | 3.75 |
| C1 screening: 4 candidates on G1 and the G2 selection split | OpenRouter | $0.15 | 0.40 |
| C2 the chosen cheap model on the G2 gate split, twice | OpenRouter | $0.05 | 0.60 |
| C3 gap maps rebuilt with the chosen cheap model, both ledgers | OpenRouter | $0.70 | 1.75 |
| Novelty judges | session subagent, Codex | $0 | — |

Estimates use the measured cost of about $0.0021 per sol call at effort high (I1c: $5.03 over 2,448 calls), with caps at about twice that. Cheap estimates use the listed prices at about 2,500 prompt and 300 reply tokens per call. G3 is dropped (§2.2). **Sum of caps: $3.75 (OpenAI) + $1.75 (OpenRouter) = $5.50, under the owner's $6 total.** Headroom: OpenAI, the owner's last statement was "$20 or more" (2026-10-24), with $5.03 spent since (`research/n3_control_v3/openai_spend.jsonl`), so about $15 if nothing else used the key; not a dated read. At stop A the owner states the current balance and whether Codex bills the same key. OpenRouter: the owner topped up the account; `scripts/key_headroom.py` now reads the account balance as well as the key limit (lesson 2026-10-26) and gave key $30.00 left, account **$19.98**, on 2026-10-26, against $1.75 of caps.

**The owner sets the total cap before any live call.** No live call inside a test.

## 5. Order, effort, parallel work, stop points

1. **Stop 0 (now).** Owner approves this plan, chooses criterion (a) or (b), and sets the total cap.
2. **Phase 1, offline ($0, about a day).** New branch. Test-first: gapmap's selectable judge, ADR 0009 guard and cache bypass; stand-in judges; G2 runner; stand-ins on the real MEC arms (G4 condition); the D1b builder (filters, topic clusters, matching, sealing); the D1b rule and its L7.3 checks; the encrypted lock/judge/reveal script. All suites pass. **In parallel:** a subagent writes the G2 fixtures from the spec.
3. **Stop A0.** The owner confirms the G2 fixture labels (about 30 min) before any judge sees them.
4. **Phase 2, cheap arm on OpenRouter (C1–C3, cap $1.75).** Screen the four candidates on G1 and the G2 selection split; gate the chosen one on the G2 gate split, twice; rebuild both gap maps with it; compute the matched-pool upper bound.
5. **Stop A.** Before the first OpenAI call: aggregates from Phase 2, the matched-pool upper bound, the owner's stated OpenAI balance and the caps. If the cheap arm fails or the upper bound is below 10 per arm, stop here, with no OpenAI spend.
6. **Phase 3, live (about 1 h wall).** R1–R4 in order.
7. **Stop B.** G1, G2 (and G4 where it gates) per arm, kappa and pool counts: aggregates only. **If either arm fails, I stop and report;** no rerun on a failed judge. Options then: screen further OpenRouter candidates, or stop.
8. **Phase 4 ($0, 1–2 h).** Arms, sheet, sealing; `RULE.md` written and committed with hashes (sheet, sealed archive, rule code, matching code); L7.3 checks pass; `methods-critic` on `RULE.md`.
9. **Stop C.** Owner sees aggregates and types the seal passphrase.
10. **Phase 5.** Collection (owner, 60–90 min), then self-ratings and arm guesses.
11. **Phase 6 ($0, about 1 h).** Canaries; criterion labels (the coder under (a), or judges under (b)) and both LLM judges; reveal under the passphrase; rule; `research/d1b_rerun/RESULT.md` in D1's shape; `PROGRESS.md` and `docs/plans/implement-queue.md` (including the §1.5 note on I1c); `citation-verifier` on everything changed under `research/`; lessons as caught.
12. **Stop D.** The result goes to the owner, with §3.7's consequence. No push, merge or PR unless asked.

Under criterion (a), a coder must be found and trained on the four labels before Phase 6; that runs in parallel with Phases 1–5 and is the likely long pole for the Nov–Dec target.
