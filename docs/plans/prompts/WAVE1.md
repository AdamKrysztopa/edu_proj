Fire wave 1 of docs/plans/prompts/README.md: run eight items in parallel, each in its own isolated git worktree, and report back. I am the owner and I authorise the commits described here. Do not push, merge or open PRs.

Step 0 (preflight, do this yourself, sequentially):
1. If docs/plans/ or docs/lessons.md have uncommitted changes, run `git switch -c plans-2026-10-24` (or switch to it if it exists), commit only docs/plans/ and docs/lessons.md with message "Plans: coverage audit, queues, fire prompts (wave plan)", and stay on that branch so the worktrees start from it. Leave every other uncommitted file alone.
2. Run `python3 scripts/key_headroom.py` and `ollama list`. Stop and tell me if qwen2.5:7b-instruct is missing (I1 needs it) or headroom is below $1.

Step 1: in ONE message, launch these eight Agent calls in parallel, each with isolation "worktree", subagent_type "general-purpose", run_in_background true:
- I1 → docs/plans/prompts/I1-closure-control.md
- DS1 → docs/plans/prompts/DS1-gold-availability.md
- I3 → docs/plans/prompts/I3-residual-identifiability.md
- DS3 → docs/plans/prompts/DS3-decisive-delta.md
- DS4 → docs/plans/prompts/DS4-identifiability.md
- I6 → docs/plans/prompts/I6-area-features.md
- I9 → docs/plans/prompts/I9-provenance-fixes.md
- I11 → docs/plans/prompts/I11-cost-ledger.md

Each agent's prompt is exactly (with <FILE> filled in):
"Read docs/plans/prompts/_common.md, then execute docs/plans/prompts/<FILE> exactly. You are in an isolated git worktree: create the item's branch there with `git switch -c <branch named in the file>` instead of starting from main. You cannot ask the owner anything: when the file names an owner decision, stop at that point, do not decide, and put the question, its options ordered by merit and your one recommended option with evidence at the top of your final report. If a skill tells you to spawn subagents and you cannot, do the work directly. Your final report: result (one paragraph), the decision it feeds, branch name, commit SHA, worktree path, any owner question, and any lesson you captured."

Step 2: while they run, do nothing else in the repo. When each finishes, record its report. When all eight are done (or failed), give me:
- one line per item: result, decision it feeds, branch, commit;
- every owner question, asked with AskUserQuestion (exactly one option "(Recommended)" each, evidence included);
- which wave-2 prompts are now unblocked (see docs/plans/prompts/README.md), as copy-paste lines.
If an agent failed, say why in one line and do not retry it without asking me.
