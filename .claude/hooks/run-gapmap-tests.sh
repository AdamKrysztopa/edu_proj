#!/usr/bin/env bash
# PostToolUse on Edit|Write|NotebookEdit: an edit under gapmap/ reruns the gapmap suite.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
file=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')
case "${file#"$root"/}" in
  gapmap/src/*|gapmap/tests/*|gapmap/pyproject.toml) ;;
  *) exit 0 ;;
esac

out=$(uv run --quiet --directory "$root/gapmap" pytest -q -x --tb=short 2>&1) && exit 0

jq -n --arg o "$(tail -n 40 <<<"$out")" \
  '{decision: "block", reason: ("Gapmap tests fail after this edit. Fix before moving on.\n" + $o)}'
