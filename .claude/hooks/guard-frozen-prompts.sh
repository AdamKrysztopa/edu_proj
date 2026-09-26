#!/usr/bin/env bash
# PreToolUse: once instrument/prereg.json exists, the hashed prompts are frozen for Stage A.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
[ -f "$root/instrument/prereg.json" ] || exit 0
file=$(jq -r '.tool_input.file_path // empty')
case "$file" in
  */instrument/prompts/*|instrument/prompts/*) ;;
  *) exit 0 ;;
esac
jq -n --arg f "$(basename "$file")" '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "ask",
  permissionDecisionReason: ("instrument/prompts/" + $f + " is frozen by instrument/prereg.json. Editing it invalidates every data session until the user re-runs `probe-app freeze` and updates the pre-registration.")}}'
