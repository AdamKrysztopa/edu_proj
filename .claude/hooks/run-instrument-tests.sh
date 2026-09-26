#!/usr/bin/env bash
# PostToolUse on Edit|Write|NotebookEdit: an edit to instrument code, tests, web, prompts or problems reruns the instrument suite.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
file=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')
case "${file#"$root"/}" in
  instrument/src/*|instrument/tests/*|instrument/web/*|instrument/prompts/*|instrument/problems/*) ;;
  *) exit 0 ;;
esac

out=$(uv run --quiet --directory "$root/instrument" pytest -q -x --tb=short 2>&1) && exit 0

jq -n --arg o "$(tail -n 40 <<<"$out")" \
  '{decision: "block", reason: ("Instrument tests fail after this edit. Fix before moving on.\n" + $o)}'
