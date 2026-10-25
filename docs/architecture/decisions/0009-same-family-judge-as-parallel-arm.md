---
id: 0009
status: active
skill: decide-architecture
date: 2026-10-24
commit: 4867598
supersedes:
  - 0008#closure-judge-other-family
  - 0008#gapmap-replays-by-default
rules:
  - id: same-family-judge-only-as-parallel-arm
    statement: A closure judge whose family matches a ledger's generator or verifier runs only as a parallel arm on the same pairs, prompt and parser as an other-family judge; results are reported per arm, and a gate reading counts only where both arms agree in direction.
    scope: ["gapmap/src/gapmap/judge.py", "gapmap/src/gapmap/control2.py", "gapmap/src/gapmap/semantic.py"]
    severity: blocking
    verification: review
  - id: gapmap-live-judges-opt-in
    statement: The gapmap CLIs replay closure judgements from the committed cache and make no network call unless a live judge flag (--judge ollama, or --judge openai in control2) is passed; a cache miss in replay mode raises an error naming the live flag that would fill it (--judge openai for an OpenAI judge in control2, else --judge ollama) rather than calling a model.
    scope: ["gapmap/src/gapmap/**"]
    severity: blocking
    verification: deterministic
    verified_by: pytest-archon#test_replay_mode_raises_a_clear_error_naming_judge_ollama_on_cache_miss
---
# A same-family closure judge runs only as a parallel arm

## Context

0008 required the closure judge to come from a family other than the N2 ledgers' generator (Anthropic) and verifier (OpenAI), against self-preference (R5 [152]). The owner's standing rule (`CLAUDE.md`, 2026-10-24) gives every cheap-model run a top-tier parallel arm. On 2026-10-24 the owner chose `gpt-6.1-sol` at reasoning effort high as that arm for the closure control (`docs/plans/implement-queue.md` § I1). OpenAI is the verifier's family, so 0008 forbade it. I1b's `gpt-5.6-luna` run already breached 0008 (`research/n3_control_luna/RESULT.md`). `control2.py` already has `--judge openai`, outside 0008's replay rule.

## Decision

- **Same family, parallel only.** An OpenAI or Anthropic judge may run on N2 ledgers only beside an other-family judge (local qwen), on identical pairs. Neither arm alone settles a gate: a reading counts only where both arms agree in direction.
- **R5 answer.** The verifier chose which claims are SUPPORTED, so a same-family judge may share its blind spots. Agreement with an other-family arm is the guard; disagreement is reported, never resolved in the same-family arm's favour. The arms share pairs, prompt and parser. They differ in family, model, serving and decoding: qwen runs at temperature 0, while the OpenAI arm sends no temperature and sets a reasoning effort. So a disagreement cannot be attributed to family alone.
- **Replay stays the default.** `--judge openai` joins `--judge ollama` as a live flag, with a hard `--max-usd` checked before every call.

## Consequences (cost)

- I1b's Luna results meet the family rule as a parallel arm. Luna is still ineligible as a judge until it passes the real-judge L7.3 check after the donor fix, and it is OpenAI's nano tier, not the top-tier arm.
- A gate now needs two judges to agree, which makes a Continue harder to reach.
- 0008's "runs at temperature 0" is not met by the OpenAI arm; the decoding difference is recorded in each arm's cache metadata.
- control2 enforces the rule's precondition before any live call (`test_a_live_same_family_judge_runs_only_beside_an_other_family_arm_on_the_same_pairs`): a judge of the sidecar's generator or verifier family needs `--parallel-arm`, an other-family arm's `control2.json` with the same ledger hash and the same `pairs_sha256` (every arm's sentence keys), so the other-family arm runs first. The rest stays review: the shared prompt and parser hold by construction, the agreement in direction is computed outside the package (`research/n3_control_v3/compare.py`), and the check compares vendor family only, not whether that arm passed the real-judge L7.3 check.
- The replay rule is tested for both messages: the main CLI's `--judge ollama` (`test_main.py`) and control2's `--judge openai` (`test_control2.py`).
