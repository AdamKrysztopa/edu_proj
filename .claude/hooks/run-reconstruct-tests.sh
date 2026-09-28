#!/usr/bin/env bash
# PostToolUse on Edit|Write|NotebookEdit: an edit under reconstruct/ reruns the reconstruct suite.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
file=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty')
case "${file#"$root"/}" in
  reconstruct/src/*|reconstruct/tests/*|reconstruct/pyproject.toml) ;;
  *) exit 0 ;;
esac

out=$(uv run --quiet --directory "$root/reconstruct" pytest -q -x --tb=short 2>&1) && exit 0

jq -n --arg o "$(tail -n 40 <<<"$out")" \
  '{decision: "block", reason: ("Reconstruct tests fail after this edit. Fix before moving on.\n" + $o)}'
