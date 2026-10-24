#!/usr/bin/env bash
# PreToolUse on Bash: a paid OpenRouter run reads the key's weekly headroom before it starts. A
# per-run --max-usd cap cannot see what other runs already spent from the same key.
set -u

cmd=$(jq -r '.tool_input.command // empty')
grep -qE -- '--live|--max-usd|spikes/[^ ]+\.py +(run|smoke)' <<<"$cmd" || exit 0

need=$(grep -oE -- '--max-usd[ =]+[0-9.]+' <<<"$cmd" | grep -oE '[0-9.]+$' | head -n 1)
out=$(python3 "${CLAUDE_PROJECT_DIR:-.}/scripts/key_headroom.py" --need "${need:-0}" 2>&1)
case $? in
  0) exit 0 ;;
  1) decision=deny
     msg="Refused: the OpenRouter key cannot cover this run. $out. Raise the key's limit or wait for the reset; a per-run cap does not replace this check." ;;
  *) decision=ask
     msg="The key's headroom could not be read before this paid run ($out). Confirm the key's limit_remaining covers it before running." ;;
esac
jq -n --arg d "$decision" --arg m "$msg" \
  '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: $d, permissionDecisionReason: $m}}'
