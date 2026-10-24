#!/usr/bin/env bash
# PostToolUse on Edit|Write: headline numbers live in research/results_manifest.json, recomputed
# from their artefacts, and a report links an immutable commit. A README once kept a superseded
# figure while report links followed the moving main branch.
set -u
root="${CLAUDE_PROJECT_DIR:-.}"
input=$(cat)
file=$(jq -r '.tool_input.file_path // empty' <<<"$input")
rel="${file#"$root"/}"
case "$rel" in
  research/*|report/*|PROGRESS.md|README.md) ;;
  *) exit 0 ;;
esac

problems=""
out=$(python3 "$root/scripts/results_manifest.py" --check 2>&1) || problems+="$out"$'\n'
case "$rel" in
  report/*|research/*.md)
    links=$(jq -r '.tool_input.new_string // .tool_input.content // empty' <<<"$input" | grep -oE 'github\.com/[^ )]+/(blob|tree)/(main|master)/[^ )]*' | head -n 5)
    [ -n "$links" ] && problems+="Links to a moving branch (pin them to the audited commit or a release tag):"$'\n'"$links"$'\n' ;;
esac
[ -z "$problems" ] && exit 0
jq -n --arg o "$problems" '{decision: "block", reason: ("Headline numbers or report links are not pinned. Fix before moving on (regenerate with `python3 scripts/results_manifest.py --write` only if the artefact change is intended).\n" + $o)}'
