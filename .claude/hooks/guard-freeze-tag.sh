#!/usr/bin/env bash
# PreToolUse on Bash: a freeze tag names the live run that passed. Three N2 freeze tags went on
# before any live run had exercised cross_verify or decoys, because a tag never counted as "done".
set -u

cmd=$(jq -r '.tool_input.command // empty')
grep -qE 'git( -C [^ ]+)? tag [^;&|]*freeze' <<<"$cmd" || exit 0
grep -qE 'git( -C [^ ]+)? tag +(-d|--delete|-l|--list|-v|--verify)( |$)' <<<"$cmd" && exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
for d in $(grep -oE '[A-Za-z0-9_./-]*runs/[A-Za-z0-9_.-]+' <<<"$cmd"); do
  [ -f "$d/sidecar.json" ] && jq -e '.complete == true' "$d/sidecar.json" >/dev/null 2>&1 && exit 0
done

msg="Refused: a freeze tag must name, in its message, the live run directory that passed (a runs/<id> whose sidecar.json has complete: true), and that run must have exercised every path the freeze covers (e.g. cross_verify and decoy calls). The fakes never refuse, so nothing a live model sees is frozen before a live run passes."
jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $m}}'
