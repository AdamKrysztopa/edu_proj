# I2: An eligible other-family judge for the closure control (guard arm), and Jev as a cheap substitute

Rewritten 2026-10-24 after I1c. The old I2 targeted I1's leaky control and compared Jev with qwen; both are superseded.

**Branch:** `i2-guard-judge`, from `plans-2026-10-24`.
**Outputs:** `research/n3_control_v3/coder32/` and `research/n3_control_v3/jev/` (results, caches), `research/n3_control_v3/GUARD.md` with its `report.json` (`_common.md` § Finish), and the `pairs_sha256` field added to `sol/*/control2.json` and `qwen/*/control2.json` (step 1).
**Cost:** qwen2.5-coder $0 (local). Jev at most $0.10 on OpenRouter (`--max-usd 0.10`). No OpenAI calls: sol's run is cached.

## Context
- Read `research/n3_control_v3/RESULT.md` (I1c) whole, and `docs/plans/implement-queue.md` § I1 (the owner decision of 2026-10-24).
- ADR 0009 (`docs/architecture/decisions/0009-same-family-judge-as-parallel-arm.md`, active): sol (`gpt-6.1-sol`, OpenAI) counts only where an other-family arm on the same pairs, prompt and parser agrees in direction. qwen2.5:7b is that arm today, and it fails L7.3 (8 of 12 stand-ins close its own arm), so no reading counts.
- **Owner decision (2026-10-24):** replace the guard arm. Screen the local `qwen2.5-coder:32b-instruct-q4_K_M` first. It is the same vendor as qwen 7b, but neither OpenAI nor Anthropic.
- Code: `research/n3_control_v3/l73.py` (the real-judge L7.3 runner and its pre-stated rule), `run_live.sh`, `compare.py`, and `gapmap/src/gapmap/control2.py` (`--parallel-arm`, `pairs_sha256`).
- Jev is `typesafe/jev-1.13` via OpenRouter's Decisions API (`research/spikes/jev/RESULTS.md`, `judge_swap.py`, `spike.py`). It answers per sentence, so it cannot share control2's prompt and parser. It is therefore never ADR 0009's guard arm; it can only be a cheaper substitute candidate.

## Rules, committed before any coder32 or Jev domain result exists
- **ADR 0009 reading:** a domain's reading counts iff coder32 is eligible, both coder32 and sol are '+' in GDPR v1, and neither is '−' in PLC. Sol's direction uses its noise-inflated CI (step 6). '0'/'0' is not a reading that counts. Report kappa coder32–sol; below 0.4, flag the guard as weak even if directions agree.
- **Jev arm state:** an arm is closed iff at least one sentence gets 'states' as Jev's top choice; partial iff none does and at least one gets 'partially'; else open. **"Close to sol":** the same direction as sol in every domain, |Δ primary| ≤ 0.05, and kappa ≥ 0.6.
- **Limits to state in the note:** coder32 runs at temperature 0 with seed 0, so its retest cannot show instability (qwen 7b's was 1.00); the L7.3 fixtures are synthetic and SEL only.

## Steps
1. **Pair identity.** Replay sol's and qwen's three domains offline (no `--judge`) to add `pairs_sha256` to their `control2.json`. `pairs`, `summary` and `length_stand_in` must stay identical; report it if any differs, and stop.
2. **Screen qwen2.5-coder 32b on L7.3**, twice (`l73.py --tag coder32 --model qwen2.5-coder:32b-instruct-q4_K_M --judge ollama`, then a second tag). Eligible iff the pre-stated rule passes in both runs with identical states. Time the first run and project the domain runtime from it (about 532 domain prompts), and tell the owner the projection in one line before continuing.
3. **If eligible:** run the three domains (`control2 --judge ollama --model qwen2.5-coder:32b-instruct-q4_K_M`, run in the background). Then extend `compare.py` to read coder32 beside sol, qwen and Luna, and report:
   - the primary per domain with its CI, and the ADR 0009 direction table for coder32 and sol (agree / counts);
   - kappa coder32–sol and coder32–qwen;
   - the length-only stand-in, unchanged (same pairs).
4. **If not eligible:** stop at the owner decision below.
5. **Jev (independent of steps 2–4).** Run `python3 scripts/key_headroom.py`. Build a Jev judge for control2 behind the cache rule (cache first, live only for misses, a miss on a prompt the old control issued is a bug). Screen it on L7.3 twice ($ ≈ 0.01), then run the three domains only if it is eligible. Its top-tier parallel arm is sol's cached run on the same pairs. Report Jev against sol per domain (primary, kappa), and its cost per judged arm.
6. **Sol noise (offline), before step 3's reading.** Sol's reply state changed on 6–8% of identical prompts between I1c runs. Build the empirical run 1 → run 2 state-transition matrix per domain from the prompts both runs sent, and draw each arm's state from it inside the seed bootstrap. This noise-inflated CI sets sol's direction for the ADR 0009 reading. State whether GDPR v1's lower bound stays above 0.

## Owner decision (stop and ask, `_common.md`)
If coder32 is not eligible, the owner has already decided the next step (`research/n3_control_v3/RESULT.md`, owner decision): add an OpenRouter judge backend to `gapmap` (stdlib `urllib` only, per the architecture test) and screen a hosted non-OpenAI, non-Anthropic model on L7.3. Ask only which model and what cap, with two or three models ordered by merit (price, documented family, JSON mode), one recommended.

## Done when
`GUARD.md` and `report.json` give: coder32's L7.3 table (both runs), its domain results and the ADR 0009 reading if eligible, Jev's L7.3 and domain results if eligible, the noise-inflated CI for sol, live-call counts and actual spend. `citation-verifier` has passed on `GUARD.md`.

## Decision it feeds
- **coder32 eligible and agrees with sol in GDPR v1:** control2 with seed-free arms becomes the MS1 instrument, judged by sol with coder32 as guard. I4 (V1 kit) can build on it.
- **coder32 eligible but disagrees:** no reading counts; report where and how they differ. Owner decides whether the instrument is registered with PLC and GDPR v1 as uninformative.
- **Jev eligible and close to sol:** a V1 panel candidate at a fraction of the cost. **Not eligible or far from sol:** stop treating judge substitution as the closure repair.
- Fix `research/spikes/jev/RESULTS.md` in the same commit: line 80 says "641" where the unique count is 542; line 118 holds an unsupported causal sentence and the word "fair" (L7.4).
