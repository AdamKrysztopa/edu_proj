Fire wave 2 of docs/plans/prompts/README.md: run nine items in parallel, each in its own isolated git worktree, and report back. I am the owner and I authorise the commits described here. Do not push, merge or open PRs.

Step 0 (preflight, do this yourself, sequentially):
1. Stay on `plans-2026-10-24`; the worktrees start from it, not from `main`. Commit any uncommitted change under docs/plans/ first; leave every other uncommitted file alone.
2. Run `python3 scripts/key_headroom.py` and `ollama list`. Stop and tell me if `qwen2.5-coder:32b-instruct-q4_K_M` is missing (I2 needs it) or OpenRouter headroom is below $0.10.
3. L7.2 record (write it under "Before E-CTA registration" in docs/plans/implement-queue.md, dated): the only paid caps in this wave are I2's Jev runs, `--max-usd 0.10` on OpenRouter, against the headroom just read. No OpenAI calls: sol's I1c run is cached ($4.97 of the owner's $10 OpenAI cap stays unspent). Everything else is $0.

Step 1: in ONE message, launch these nine Agent calls in parallel, each with isolation "worktree", subagent_type "general-purpose", run_in_background true:
- I2 → docs/plans/prompts/I2-jev-control.md (guard judge; the long one: a 32b local model judges about 600 prompts)
- I5 → docs/plans/prompts/I5-gate-simulation.md
- I12 → docs/plans/prompts/I12-predictor-replacement.md
- I7 → docs/plans/prompts/I7-freeze-manifest.md
- DS2 → docs/plans/prompts/DS2-closure-codebook.md
- DS5 → docs/plans/prompts/DS5-pregold-fulltext.md
- DS6 → docs/plans/prompts/DS6-verifier-validity.md
- DS7 → docs/plans/prompts/DS7-boundary-sources.md
- DS8 → docs/plans/prompts/DS8-oss-departures.md

Each agent's prompt is exactly (with <FILE> filled in):
"Read docs/plans/prompts/_common.md, then execute docs/plans/prompts/<FILE> exactly. You are in an isolated git worktree cut from plans-2026-10-24: create the item's branch there with `git switch -c <branch named in the file>`. You cannot ask the owner anything: when the file names an owner decision, stop at that point, do not decide, and put the question, its options ordered by merit and your one recommended option with evidence at the top of your final report. If a skill tells you to spawn subagents and you cannot, do the work directly. Your final report: result (one paragraph), the decision it feeds, branch name, commit SHA, worktree path, the path of your report.json, any owner question, and any lesson you captured."

Step 2: while they run, do nothing else in the repo. When each finishes, record its report. Ask every owner question as it arrives, with AskUserQuestion (exactly one option "(Recommended)", evidence included); do not wait for the others. If an agent failed, say why in one line and do not retry it without asking me.

Step 3, when all nine are done: merge each branch into plans-2026-10-24 (I authorise local merges), merging I7 last; then regenerate I7's `research/freeze_manifest/manifest.json` so it covers I2's, I5's and I12's files. Run the three package suites, then run `citation-verifier` over every new note and fix what it finds.

Step 4, the wave 2 report, built to wave 1's final level from the start:
1. Collect every item's report.json.
2. Ask Codex (`gpt-5.6-sol`, effort high, read-only) for a storyboard from those files, as for wave 1 (`codex_storyboard_prompt.md` pattern): a one-paragraph story, worked/failed bullets, one figure per decision with exact rows and sources, and a cut list.
3. Build it as a new Claude Docs report: a verdict line, "Wave 2 at a glance" (worked / failed), the decision path, one section per decision with a figure and a Question/Answer/Changed card, decisions taken, and what wave 3 must settle. Put the full notes in a second tab. Screenshot every figure before publishing it.
4. Ask Codex to review the built report against the sources, apply every verified fix, and save the link in PROGRESS.md and docs/plans/implement-queue.md.

Then give me: one line per item (result, decision, branch, commit), the report link, and which wave 3 prompts are unblocked, as copy-paste lines.

Not for agents (owner actions, run any time before the freeze):
- Presence-check each primary gold list once you hold it: `uv run --directory residual python -m residual.presence <gold file>`. It prints one sealed line and never item text. A list that is absent falls to the next fallback before any other gold's result is seen.
