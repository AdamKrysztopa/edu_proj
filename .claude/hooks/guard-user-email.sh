#!/usr/bin/env bash
# PreToolUse on every tool, subagents included: deny any call whose input carries the user's email.
# Polite-pool APIs (Unpaywall, Crossref, OpenAlex) invite an email and a search agent will supply it.
set -u

email=$(git -C "${CLAUDE_PROJECT_DIR:-.}" config user.email 2>/dev/null)
[ -n "$email" ] || exit 0
jq -c '.tool_input // {}' | grep -qiF "$email" || exit 0

jq -n '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: "Refused: this call would send the user'"'"'s email address to a tool or external service. Drop the email/mailto parameter or use an anonymous request; the user must ask explicitly before their address is sent anywhere."}}'
