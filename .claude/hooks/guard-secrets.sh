#!/usr/bin/env bash
# PreToolUse: keep .env files (API keys) out of tool calls. The app loads them itself.
set -u
input=$(cat)
tool=$(jq -r '.tool_name' <<<"$input")
case "$tool" in
  Bash) target=$(jq -r '.tool_input.command // empty' <<<"$input") ;;
  *)    target=$(jq -r '.tool_input.file_path // .tool_input.path // empty' <<<"$input") ;;
esac
grep -qE '(^|[/[:space:]"'"'"'=(\\])\.env([.[:space:]"'"'"'\\)]|$)' <<<"$target" || exit 0
case "$tool" in
  Bash) grep -qE '^git (check-ignore|status)' <<<"$target" && exit 0 ;;
esac
jq -n '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny",
  permissionDecisionReason: ".env holds API keys and is off limits to tool calls. The CLI loads it itself; ask the user to run anything that needs it directly."}}'
