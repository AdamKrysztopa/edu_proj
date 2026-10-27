# Plan: judge screening as N3's standard way to choose a closure judge (2026-10-27)

D1b chose its closure judges by measurement (`docs/plans/gapmap-fix-and-d1-rerun.md` §2.1–2.2,
`research/d1b_rerun/RESULT.md`), but the order of its checks, the parallel-arm rule and the number
of required runs were written only as prose. One ordering slip followed: sol's paid runs started before
the free Stop A count that should have stopped them (lesson 2026-10-26, "Paid runs started in
parallel with the free gate that should have stopped them"). This plan turns D1b's screening into
one entry point that enforces that order in code. It changes no gapmap default and no `research/n3/` cache.
Like D1b it is exploratory. It feeds no N3 gate and is not RQ-B evidence. It decides which judge
may be used, not what any gap map shows.

Status: **built and adopted, 2026-10-27** (`gapmap/src/gapmap/screen.py`, ADR 0010 active; owner
decisions in §6). `methods-critic`
reviewed the first draft: "build with changes". Its findings 1–10 are applied below, and §6 lists the
rule changes it found. Note on process: the module was drafted while that review was running, not
after it. The critic flagged this, and the findings were applied before anything was committed.

## 1. Entry point

    uv run --directory gapmap python -m gapmap.screen status --candidate SLUG
    uv run --directory gapmap python -m gapmap.screen run --candidate SLUG --model M \
        [--reasoning-effort E | --reasoning-max-tokens N] \
        [--live --max-usd X --spend-ledger F] [--after GATE.json] [--owner-note TEXT]
    uv run --directory gapmap python -m gapmap.screen adopt --candidate SLUG --model M [...] \
        --step G1|G2 --from DIR --note TEXT
    uv run --directory gapmap python -m gapmap.screen pair --cheap SLUG --top SLUG

The provider follows the model id (`gapmap.judge` price tables). A model with no recorded price is
refused. The first call pins the model and its settings in the verdict, and a later call with other
settings is refused. State lives in `research/judge_screening/<SLUG>/`: `verdict.json` (machine-readable)
and one directory per run (`<step>-run<k>/`), holding the runner's own outputs and closure cache.
`gapmap.screen` calls the committed runners as subprocesses and imports nothing from `research/`.

## 2. The standard sequence (`screen-v1`)

| Step | Cost | What it runs | Satisfied when |
|---|---|---|---|
| S0 fixtures | $0 | `research/d1b_rerun/g2.py --stand-ins --split gate`. It refuses fixtures the owner has not confirmed, and fixtures where N does not match P or the markers do not balance. It scores the five stand-ins and an oracle that closes only P. | no stand-in passes and the oracle passes |
| S1 parallel arm | $0 | reads the other verdicts | only for a candidate whose family is a target ledger's generator or verifier family (`anthropic`, `openai`): an other-family candidate is **eligible** on the same fixture hash |
| G1 | paid | `research/d1b_rerun/g1.py` (N3 L7.3 fixtures through `research/n3_control_v3/l73.py`) | 1 passing run |
| G2 | paid | `research/d1b_rerun/g2.py --split gate` (13 topics, `g2.passes` as committed, R as `R_excess`) | 2 passing runs |

## 3. What the entry point enforces

1. **Free gates before spend.** `run` executes every pending $0 step first. It starts a paid run only
   when all earlier steps are satisfied, and at most one paid run per invocation.
2. **A plan's own gate.** `--after GATE.json` refuses the paid run unless that record exists and says
   `"continue": true`. D1b's Stop A was such a gate. It belonged to the study, not to the screening,
   so a plan that places spend behind its own $0 gate must pass that gate's record here (finding 5).
   Without `--after`, the lesson's slip is not prevented, so the lesson stays open for study-level gates.
3. **Locks.** One lock per candidate and one per spend ledger, each made by exclusive create. The runners' caps
   are cumulative over the ledger, so two runs on one ledger at once would each see the wrong
   prior spend.
4. **Budget.** A paid run needs `--live`, `--max-usd` (this run's own cap) and `--spend-ledger`.
   The runner gets `prior ledger spend + max-usd`. Before an OpenRouter run, `scripts/key_headroom.py
   --need max-usd` must pass. OpenAI's balance cannot be read, so the record says so, and the owner's
   stated balance applies. Spend is recorded as the ledger delta.
5. **Independent runs.** Each run writes into a new directory that must not exist yet, so its
   closure cache starts empty.
6. **Outcomes.** Each run is `pass`, `fail` or `incomplete`. Incomplete covers a non-zero exit, a
   missing result, any undecided arm in G2, and any undecided seed-free arm in G1 (see §6). A complete
   `fail` puts the **model** out for `screen-v1`. That holds under any fixture hash, and under a new
   slug unless the owner gives `--owner-note`, which is recorded as `readmitted` (finding 2). One
   incomplete run per step may be retried freely. A further retry needs `--owner-note`, so a run
   heading for a fail cannot simply be stopped and rerun (finding 3). The partial figures of every
   incomplete run stay in `verdict.json`.
7. **Eligibility recorded only after the required passes.** `eligible: true` needs S0, S1 (where it
   applies), one G1 pass and two G2 passes under the current fixture hash, and no recorded fail.
8. **Fixture hash.** The hash is a sha256 over the files that decide a judgement (finding 4): the
   G2 fixtures (`topics`, `inserts`, `confirmations`), `g2.py`, `l73.py`, `gapmap/tests/l73_fixtures.py`
   and `conftest.py`, and the prompt, parser and stand-in code (`semantic`, `standins`, `control2`,
   `text`, `config`). `judge.py` (prices and transport) and `g1.py` (argument routing) are left out,
   so adding a candidate's price does not void every verdict. Passes recorded under another hash do
   not count.
9. **The cheap arm alone settles nothing.** A cheap verdict carries `settles_alone: false`. `pair` reports a
   usable pair only when an eligible cheap other-family candidate and an eligible top-tier candidate
   (`gpt-6.1-sol`) share one fixture hash. It prints every run note, the G2 rule, and agreement and
   Cohen's kappa over the two arms' G2 states (aggregates only; D1b plan §2.2 "Pairing").
10. **Selection is visible.** `gated_on_this_hash` lists every candidate with a G2 run on the current
    hash, so a pass among many gated candidates can be read against how many were tried (finding 1).
11. **Replay by default.** Without `--live` no paid run starts. `run` executes only the $0 steps and
    prints the next paid command (ADR 0009 `gapmap-live-judges-opt-in`).

## 4. Adopting D1b's runs ($0)

`adopt` copies a finished run's closure cache into a new run directory and re-scores it through the
current runner in replay mode. A cache miss stops it. The replay must reproduce the source run's own
result file; otherwise nothing is recorded (finding 7). The same order applies. A note is required.
That cold start held is checked from the spend ledgers' `prompt_sha256` against the 65 rebuilt
gate-split prompts (by `methods-critic`, and again here after sol's second run):

- gemma (OpenRouter): every gate prompt was paid exactly twice. Both gate runs started cold.
- sol (OpenAI): 56 gate prompts were paid twice and 9 three times. That matches gate1, the 9-call stopped
  run and a cold gate2.

**Done on 2026-10-27:**

- `gemma-4-31b-it` (reasoning capped at 2,000 tokens) has G1 from `g1/google_gemma-4-31b-it-r3` and
  G2 from `g2/google_gemma-4-31b-it-gate1` and `-gate2`. All three replays reproduce, and the candidate is **eligible**. Each
  run note says it passes G2 only under the post-hoc R amendment.
- `gpt-6.1-sol` (effort high): S0 and S1 pass (S1 via gemma). **D1b's G1 could not be adopted.**
  In `g1/sol-r1`, one call left no cache entry, so its arm is `undecided` (an equal-cap control arm,
  `ctrl_eq`, which l73's rule does not rule on), and the replay misses that prompt. `OpenAIJudge`
  had no retry then. An exception in the call (most likely a transport error) was caught in
  `semantic.judge_retrieval` and became `undecided`, with no line in the spend ledger. That is fixed:
  `OpenAIJudge` now retries transient errors and raises `JudgeUnavailable` on persistent ones.
  A **fresh G1 through the screen** (`research/judge_screening/gpt-6.1-sol/G1-run1`, 2026-10-27) passed:
  planted positive fires, no stand-in fires, 0 undecided seed-free arms. It made 76 calls, all
  finishing `stop`, and cost $0.139 against a $0.30 cap, on `research/d1b_rerun/openai_spend.jsonl`.
  Then G2 was adopted from `g2/sol-gate1` and `g2/sol-gate2`, both replays reproducing. Sol is
  **eligible**.

`pair --cheap gemma-4-31b-it --top gpt-6.1-sol` is **ready** on fixture hash `474b636c4584…`. Its
G2 state agreement is 0.78, kappa 0.59, over 130 states. `gated_on_this_hash` lists the two
candidates.

D1b's other candidates are not in the screen. They failed the selection split or ran locally:
qwen2.5:7b fails G1 and G2, gemini-3.5-flash-lite fails G1, and qwen3.8-flash fails the selection
split (`RESULT.md`). The model-keyed "out" rule covers only failures recorded in the screen.

Aggregates over the D1b G2 states, $0: gemma against sol, run k against run k, gives agreement
0.78 and kappa 0.59 (130 states). Sol run 1 against run 2 gives 0.94 and kappa 0.89 (65 states).

## 5. Tests (offline, fake runners and judges)

`gapmap/tests/test_screen.py` (31 tests) uses an injected runner that writes the result files a
fake judge would produce. The ordering tests cover: a paid step refused while S0 is failed or
pending, an S0 that fails when the oracle cannot pass, an S1 refusal until an other-family arm is
eligible, `--after` refusing a missing or non-continue record, and at most one paid run per invocation.
The budget tests cover: a cap and ledger being required, the cumulative cap of prior + cap, the
headroom refusal, and the spend-ledger lock.
The outcome tests cover: eligibility only after one G1 and two G2 passes, a fail that keeps the
candidate out across hashes and slugs, the owner-note readmission, incomplete runs that do not
count and get fresh directories, the second incomplete retry needing a note, and an undecided
seed-free G1 arm counting as incomplete.
The remaining tests cover: refusal of an existing directory, a stale hash, the candidate lock,
pinned settings, the price check, adoption order and reproduction, and `pair` with its agreement.
The result readers are checked against D1b's committed outputs.
`research/d1b_rerun/tests` covers the G2 oracle and g1.py's flag handling.

## 6. Owner decisions (taken 2026-10-27)

**Outcome.** The owner accepted all five rule readings below, (a) to (e). The owner kept gemma as
the cheap arm under the disclosed R_excess amendment (item 2). The owner ordered the OpenAI retry fix
and then one fresh sol G1 (item 3), and promoted ADR 0010 to active (item 4).

**Follow-up (not yet built):** the gapmap CLI (`--judge openai|openrouter`) and `control2` must
read `verdict.json` and refuse a live judge that is not in a ready `pair`. Until then, eligibility
is recorded but not binding.

1. **Rule changes the critic found** (accepted). Each is a reading or tightening of D1b's prose,
   not a change to `g2.passes` or `l73.evaluate`:
   - (a) The G2 selection split is not a step. D1b made eligibility "G1 and the selection split",
     but the split proved unable to select: 2 of its 4 kept seeds read as stating the element to
     every judge, and gemma was gated only under a waiver. Choosing among several eligible cheap
     candidates is left to the owner, with `gated_on_this_hash` shown. **Recommended:** accept it,
     and rebuild a selection split only if more than one cheap candidate ever becomes eligible.
   - (b) G2 needs its first two complete runs to pass, with no "two of three".
   - (c) In G1, an undecided seed-free arm makes the run incomplete. l73's rule would read it as
     "not closed", which favours the stand-ins.
   - (d) S1 is stricter than ADR 0009. The ADR needs the other-family arm to have run; S1 needs it
     to be eligible.
   - (e) Cheap screening runs need no top-tier arm of their own. In screening the criterion is the
     owner-confirmed labels, not a judge, so CLAUDE.md's "the cheap arm alone never settles" applies
     when a judge is used, which `pair` enforces.
2. **gemma under the post-hoc amendment** (kept as the cheap arm). gemma is eligible only under
   the R_excess amendment, which was found on its own gate data. At temperature 0 a fresh run would
   reproduce the same result. The note stays in its verdict and `pair` prints it.
3. **sol's G1** (ordered). First, `OpenAIJudge` took OpenRouterJudge's retry and `JudgeUnavailable`
   contract, so a failed call stops the run as incomplete instead of becoming `undecided`. Then one
   fresh G1 ran through the screen with a $0.30 cap, and sol's two G2 runs were adopted at $0 (§4).
4. **ADR 0010** (promoted to active, constitution regenerated). The screen is now the only way a
   closure judge becomes usable on N3. It binds only once the follow-up above is built.

## 7. Known limits

- The 13-topic gate split was formed after deepseek and glm read its no-insert arms: topics that both
  closed were dropped, which makes close(0) easier to meet.
- Claude wrote the P and N plants, so a future Anthropic-family candidate would judge text from its
  own family.
- The target ledger families and the top-tier list are constants in `gapmap.screen`.
- The fixture set is D1's domain for G2 and N3's for G1. A new domain needs its own fixtures and a new
  sequence version.
