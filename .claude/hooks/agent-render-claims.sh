#!/usr/bin/env bash
# PostToolUse on Agent|Task: a subagent's "rendered, inspected, clean" is a claim. Seven figures
# reported that way had overlapping boxes and clipped labels; the user found them, no check did.
set -u

resp=$(jq -r '.tool_response | tostring')
grep -qiE '\.(png|pdf|svg|jpe?g)\b|render' <<<"$resp" || exit 0
grep -qiE 'visually (inspected|checked|verified)|inspected[^.]{0,40}clean|looks? (clean|correct|good)|renders? (clean|cleanly|fine|correctly)' <<<"$resp" || exit 0

msg="The agent reports a render as inspected or clean. That is its claim, not a check: Read every render it names yourself before accepting it or telling the user it is done."
jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $m}}'
