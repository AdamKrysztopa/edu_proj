#!/usr/bin/env bash
# PreToolUse (Bash): a command that reads a sealed key/answer file (e.g. .private/e_abst/key.json)
# and also prints something is asked to confirm first. A branch that prints the value on one arm
# and only the type on the other is not a type check — it leaks sealed content into the transcript
# (caught once by re-reading tool output after the fact, not before running it).
set -u
input=$(cat)
command=$(jq -r '.tool_input.command // empty' <<<"$input")
[ -n "$command" ] || exit 0
grep -qE '\.private/[^"'"'"' ]*key[^"'"'"' ]*\.json' <<<"$command" || exit 0
grep -q 'print(' <<<"$command" || exit 0
jq -n '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask",
  permissionDecisionReason: "This command reads a sealed key/answer file and prints something. Confirm every branch prints only shape metadata (type(v), len(v), sorted(v.keys())) and never the value itself, before running it."}}'
