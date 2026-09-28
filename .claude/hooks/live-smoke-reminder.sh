#!/usr/bin/env bash
# PostToolUse on Edit|Write: the fakes never refuse and hand audio over whole, so a change to what
# reaches a model is untested until a live run.
set -u

file=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty')
case "$file" in
  */instrument/models.json|*/instrument/prompts/*|*/instrument/src/probe_app/llm.py|\
  */instrument/src/probe_app/backends.py|*/instrument/src/probe_app/transcribe.py|\
  */instrument/src/probe_app/simulate.py|*/instrument/src/probe_app/engine.py|\
  */instrument/src/probe_app/contract.py) ;;
  *) exit 0 ;;
esac

msg="$(basename "$file") changes what a live model or transcriber sees. The fakes cannot refuse, drop a chunk or reject a schema, so this change is not done until a live run passes: \`uv run --directory instrument probe-app simulate\` (or /preflight pilot)."
jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $m}}'
