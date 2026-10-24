#!/usr/bin/env bash
# PostToolUse on Edit|Write: writing a gate, decision rule or control into a plan injects the checks
# that show it can discriminate. Four registered rules passed things they existed to catch: an
# unreachable margin, a check passing by construction, a word-length stand-in, a one-sided null.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
input=$(cat)
file=$(jq -r '.tool_input.file_path // empty' <<<"$input")
case "${file#"$root"/}" in
  REORIENTATION.md|docs/plans/*.md|research/*.md|research/spikes/*.py) ;;
  *) exit 0 ;;
esac

text=$(jq -r '.tool_input.new_string // .tool_input.content // empty' <<<"$input")
grep -qE '(≥|≤|>=|<=|[<>]) ?[0-9]' <<<"$text" || exit 0
grep -qiE 'gate|threshold|stop rule|decision rule|PROMISING|futility|SESOI|kill|continue/change/stop|null|control' <<<"$text" || exit 0

msg="This edit writes a gate, decision rule or control. Before it is registered or cited, show it can discriminate: (1) compute the best case it can reach from the observed baseline and record whether it is still reachable; (2) run it on a planted positive built to show the failure it guards against, which must fire; (3) run it on a trivial stand-in (noise, text length, a surface statistic), which must not pass; (4) a null or control applies the same exclusions to both arms, draws realistic donors, and its conclusion names only the variable its arms differ on. If it gates live runs, compare the sum of their --max-usd caps with \`python3 scripts/key_headroom.py\` and record both. Then run methods-critic."
jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $m}}'
