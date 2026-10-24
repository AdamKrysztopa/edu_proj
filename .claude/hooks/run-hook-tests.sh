#!/usr/bin/env bash
# PostToolUse on Edit|Write: an edited hook reruns every test that names it. A drain once changed a
# hook's output and left two of its tests failing, because only the DOI test was ever run.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
file=$(jq -r '.tool_input.file_path // empty')
case "${file#"$root"/}" in
  .claude/hooks/*) ;;
  *) exit 0 ;;
esac

name=$(basename "$file")
tests=$(grep -lF -- "$name" "$root"/scripts/hook_tests/test_*.py "$root"/scripts/lessons_loop_tests/test_*.py 2>/dev/null)
if [ -z "$tests" ]; then
  msg="No test under scripts/hook_tests/ or scripts/lessons_loop_tests/ names $name, so this hook edit is unverified. Add one to scripts/hook_tests/ that triggers the hook and reads what it prints."
  jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $m}}'
  exit 0
fi

fail=""
for t in $tests; do
  out=$(python3 "$t" 2>&1) || fail+="== ${t#"$root"/}"$'\n'"$(tail -n 25 <<<"$out")"$'\n'
done
[ -z "$fail" ] && exit 0
jq -n --arg o "$fail" '{decision: "block", reason: ("Tests that invoke this hook fail after the edit. Fix before moving on.\n" + $o)}'
