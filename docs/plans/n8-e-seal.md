# N8: E-SEAL, sealed forecasts for Validation Track A

**Status:** plan, 2026-10-27, revised twice after `methods-critic` (seven blocking findings over two rounds, all addressed below). Owner go-ahead 2026-10-27. Source rules: `REORIENTATION.md` §18.1 (E-SEAL), §20 item 5, §22 (N8), §24 step 7. N8 has no gate: it is secondary and non-gating, and nothing here can change what K0, K1, K2, Stage B arm matching or the 2–3-week delay decides (`research/experiment-ai-assisted-cta-physics.md`, used unchanged). **This file is the scoring protocol.** The seal records its SHA-256 and commit, and the run refuses to start while it has uncommitted changes, so it cannot be edited after the forecast exists without the change showing.

## 1. Scope: which half is ready

| Half | Ready? | Why |
|---|---|---|
| Operation list for the Stage A problems | **Yes** | The four think-aloud problems exist (`instrument/problems/problems.json`, sets A and B, two each). |
| Early-K0 error-category distribution | **No** | §18.1 allows it "only after the early-K0 items are frozen in their registration". `instrument/k0/items.md` and `instrument/k0/prereg-early-k0.md` are drafts. Nothing for this half is built here. |

## 2. What is forecast

For each Stage A think-aloud problem (A1, A2, B1, B2), **at most 12** mental operations a physicist performs when solving it, the ones that matter most, in the order performed. The unit is Stage A's own: "a cue, decision, representation choice, check or heuristic that a novice could be taught". Each operation has `statement` (one sentence), `trigger` (what in the problem calls for it, the roadmap M2 field "trigger condition"), `type` (cue, decision, representation, check, heuristic) and `p_omitted` (the model's probability that an expert would perform it but leave it out of an ordinary worked explanation for a first-year student). If a reply holds more than 12, only the first 12 are scored; the manifest flags it.

**Source: a closed-book model forecast.** The model gets the problem statement and the unit definition only: not the answer field, the codebook, the simulated think-aloud, pilot material, session data, the interviewer prompts or any framework list. The operations therefore come only from what the models learned from public text. It is not the N2 evidence pipeline and is not reported as one. Evidence label: **synthetic extrapolation**; a predictor, never a criterion; it feeds no gate.

**Arms.** Same inputs and prompt, only the model differs; all are sealed together.

| Arm | Model (OpenRouter slug) | Why |
|---|---|---|
| top-tier (primary) | `anthropic/claude-opus-5.5` | The project's top-tier arm in N2 and N3 |
| other family | `openai/gpt-6.1-sol` | Stage A's AI interviewer is an Anthropic model, so coverage of AI-probe-added operations by an Anthropic forecast is partly a model agreeing with itself; this arm separates that |
| cheap | `anthropic/claude-haiku-4.5` | N2's extractor model; never settles a reading alone (`CLAUDE.md`) |

One sample per problem per arm (12 calls). Strict JSON schema output, `max_tokens` 8192 (fixed in `reconstruct/src/reconstruct/llm.py`), no temperature (the provider default); a call whose served model differs from the requested slug is discarded.

**Dry run first.** One non-conservation problem (`research/n8_eseal/dry_run_problem.md`, horizontal projectile kinematics; not an FCI or AAAS conservation item, and outside N3's gold domains) goes to every arm. Only whether each reply fits the schema is kept; the replies are discarded unread. The seal refuses to start unless a dry run passed with the same prompt and schema hashes.

**Cost.** Prices from `https://openrouter.ai/api/v1/models`, read 2026-10-27: Opus 5.5 $4 / $20, gpt-6.1-sol $2 / $10, Haiku 4.5 $1 / $5 per M input / output tokens. Worst case per call at 8192 output tokens: about $0.17, $0.085 and $0.042. Hard caps: dry run `--max-usd 0.25`, seal `--max-usd 0.75`, **$1.00 in all**. Before every call the runner charges that call's worst case (a byte bound on the prompt plus `max_tokens`, at the read prices) against what is left and refuses the call if it would overshoot, so no cap can be exceeded. The seal runs `scripts/key_headroom.py` itself (L7.1), refuses if the key or the account has less than $10 left, and records the measured line.

## 3. Sealing

- **In process, never displayed.** Replies are held in memory and encrypted in one piece; plaintext reaches openssl only on stdin. Nothing is printed except hashes, cost and per-call outcomes. Errors print the exception class only, never its message. The `openai` and `httpx` loggers are held at WARNING, and the run refuses if `OPENAI_LOG` is set (the SDK would log bodies). No temporary file is used.
- **Scheme.** The repo's D1b hybrid (`research/d1b_rerun/build_sheet.py` `seal`), changed to stdin only: a fresh 256-bit key encrypts the JSON (`openssl enc -aes-256-cbc -pbkdf2 -iter 600000 -md sha256 -salt`, the `probe-app backup` parameters), and the key is wrapped with RSA-OAEP-SHA256 under a public key of at least 3072 bits.
- **Key custody is mandatory, not advisory.** A custodian who holds no Track A role, and will take none, generates the key pair and gives the operator only the public key, named at run time by the environment variable `E_SEAL_PUBLIC_KEY`. The owner may not generate it. The run never needs a private key; if `E_SEAL_PUBLIC_KEY` is unset or not an RSA key of at least 3072 bits, it stops before any network call. The custodian's name and role, and the public key's SHA-256, go in `research/n8_eseal/README.md`.
- **Provider logs.** OpenRouter can store and show prompts and replies when input/output logging is on. The operator turns it off before the run and confirms with `--provider-logging-off`, which the manifest records; without the flag the run refuses.
- **Commitment.** The plaintext includes a random 256-bit nonce, so its SHA-256 can be committed without allowing a guess. Committed in `research/n8_eseal/sealed/`: `forecast.enc`, `key.enc`, `manifest.json`, `calls.jsonl`. §24 step 7 says "commit only their hashes"; the ciphertext is committed too so that the forecast cannot be lost, which reveals nothing without the private key.
- **The manifest holds no content:** model slugs, families and settings; SHA-256 of the system prompt, user template, schema, `problems.json`, this plan (with its commit) and the dry-run manifest; caps, the measured key headroom, spend; per call the outcome, the call log's outcomes (`ok`, `truncated`, `refusal`, …), schema validity (pass or fail), tokens and cost; the cipher parameters; the hashes of `forecast.enc`, `key.enc`, the plaintext and the public key. No operation counts or other content-derived figure.
- **Partial runs.** If a call fails, the successful replies are still sealed and the manifest records the failure (class only). A seal is never overwritten.
- **Test.** A fake model's replies carry a canary string; the tests assert it occurs in no stdout, stderr, log record or written file, in plain, JSON-escaped, base64, hex or UTF-16 form, and that decrypting with the test key recovers it. Further tests: a failing call whose message carries the canary leaks nothing; each precondition above stops the run before any call; the cap refuses a call before dispatch; a seal cannot be overwritten; unsealing refuses each breach in §4.

## 4. When and how it is unsealed

- **Gate.** Only after K1 adjudication is locked: the K1 adjudication record (a JSON file with the coded operation list and a `k1_decision` field) is committed to git. `python -m reconstruct.eseal unseal` refuses unless that file is tracked, unchanged since its commit and carries `k1_decision`; it records the file's SHA-256 and commit in `research/n8_eseal/unseal_record.json`. The same SHA-256 should appear in Track A's own lock record.
- **Validity of the seal.** It is scored only if its `problems.json` SHA-256 equals the one frozen by `probe-app freeze` in `instrument/prereg.json`. If the problems change before the freeze, this seal is void and never scored, and a new seal is made before the first data session.
- **Who.** The custodian decrypts. The command checks the ciphertext and plaintext hashes against the manifest and writes plaintext only outside the git working tree.
- **Who may see it.** The custodian and the two matchers, who hold no Track A role and take none afterwards, including the Stage B test-writer and answer-scorer roles. Anyone else who sees it becomes ineligible for every Track A human role (§18.1).
- **Pre-registration.** The owner names this plan's SHA-256 (as recorded in the manifest) in Track A's pre-registration before M4, as §20 item 5 requires for these additions.
- If Stage A never runs, the seal stays closed.

## 5. Pre-stated scoring

Secondary and non-gating. Nothing below can change K0, K1 or K2, and no number below feeds a gate. Values marked *(project choice)* are judgments.

**Framework baseline.** Before Stage A's first data session, someone with no Track A role transcribes the step lists of the three frameworks named in Stage A's published-framework tag (Heller & Reif 1984; Dufresne et al. 1992; Docktor et al. 2015) into `research/n8_eseal/framework_baseline.json` and commits it. If it is absent at scoring, the decoy baseline alone is used.

**Matching.** For each problem X, the matchers get (i) Stage A's operations coded on X, with every source and status tag removed (explanation, trace, AI or human probe, shared, absent, published-framework); and (ii) one shuffled list, with no arm or origin labels, holding:
- X's forecast operations from all three arms;
- **decoys, size-matched per arm**: for each arm, as many operations as that arm has on X (n_arm(X), at most 12), drawn at random (seed 20261027) from the same arm's forecasts for the other three problems;
- the framework baseline items;
- **planted positives**: one paraphrase of each of X's Stage A operations, written after K1 is locked by someone who is not a matcher. Their hit rate is reported as the matchers' sensitivity. For each list item they mark which of X's operations it matches, if any, using Stage A's own "is this the same operation?" criterion. They match independently; κ on match versus no match is reported, and they then settle disagreements together. Origins and tags are rejoined by script only after the settled matches are committed. Matching is **per problem**: an operation coded on several problems counts as covered if some problem's own forecast matches it there.

**Denominator.** The **K1 operations** are exactly those counted under K1(a): performed, shared and absent from the ordinary material, trace-only or AI-probe-added. Human-probe-added operations are reported separately.

**Measures, per arm (top-tier first; all three always reported):**

1. **Coverage:** the share of K1 operations matched by that arm's own forecast, with a Wilson 95% CI (§20 item 5's "coverage of K1's new shared operations").
2. **Baselines, size-matched to the arm.** The **decoy rate**: the same share matched by that arm's own decoys. The **framework rate**: per problem, the mean over 1,000 random subsets (seed 20261027) of n_arm(X) framework items of the share matched; if the framework list is shorter than n_arm(X), all of it. A baseline list never holds more items than the arm it is compared with, because coverage rises with list size.
3. **Splits** (descriptive): coverage among trace-only versus AI-probe-added K1 operations, and among K1 operations with versus without the published-framework tag. The AI-probe-added split carries the stated caveat that the interviewer and two arms share a model family.
4. **Precision:** the share of the arm's forecast operations matched to any performed operation of their problem.
5. **Omission calibration** (descriptive): mean `p_omitted` of matched forecast operations whose Stage A match is coded absent versus present in the ordinary material.

**Readings of measure 1, top-tier arm** *(project choice; read only with the other two arms reported alongside)*:

- **Inconclusive** if there are fewer than 3 K1 operations, or the matchers' κ is below 0.70 (Stage A's own agreement target).
- **Public-recoverable** if the Wilson lower bound exceeds 1/3, and coverage exceeds both the decoy rate and the framework-baseline rate by at least 1/3: much of what Stage A calls new was forecastable from public knowledge, so "new" means new to this course's material.
- **Not anticipated** if the Wilson upper bound is below 2/3, and coverage exceeds neither baseline by 1/3: most of what Stage A calls new was not forecast from public knowledge.
- Otherwise, inconclusive.

**First scoring step.** Before matching, the scoring script checks that the manifest's `problems_sha256` equals the value frozen in `instrument/prereg.json` (§4) and stops if not.

**Blinding limit, reported.** Framework items carry no problem-specific trigger and recur across the four lists, so a matcher may recognise them as non-forecast items; the framework rate is reported with that limit.

The readings describe the forecast. They do not restate, qualify or reopen K1's decision and never count as evidence for or against it.

## 6. Build and run

- Code: `reconstruct/src/reconstruct/eseal.py`; prompts `reconstruct/src/reconstruct/prompts/eseal_system.md` and `eseal_user.md`; tests `reconstruct/tests/test_eseal.py` (fake models, no network). It reuses `llm.py`'s backend and `CallLog` and reads `problems.json` as data.
- Run, in order, with `OPENROUTER_API_KEY` and `E_SEAL_PUBLIC_KEY` set and OpenRouter logging off:
  1. `uv run --directory reconstruct python -m reconstruct.eseal dry-run --live --max-usd 0.25`
  2. `uv run --directory reconstruct python -m reconstruct.eseal seal --live --max-usd 0.75 --provider-logging-off`
- Output: `research/n8_eseal/dry_run/`, `research/n8_eseal/sealed/`. Note: `research/n8_eseal/README.md` (what was sealed, how, hashes, cost; no content).

## 7. Risks

- **Public frameworks are in the models.** That is the point (public knowledge); the framework baseline and the published-framework split separate it.
- **Problem statements leave the machine,** to OpenRouter, Anthropic and OpenAI. They are the instrument's problems, not participant data.
- **One sample per arm.** Three arms give a rough sense of model dependence, not a variance.
- **Key loss** loses the forecast; the custodian keeps a second copy offline.
