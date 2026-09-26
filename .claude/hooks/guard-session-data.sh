#!/usr/bin/env bash
# PreToolUse: session directories are study data and are git-ignored, so nothing restores them.
# Only the app writes there. File tools are denied; Bash commands that would delete or overwrite them ask first.
set -u
input=$(cat)
root="${CLAUDE_PROJECT_DIR:-.}"
tool=$(jq -r '.tool_name' <<<"$input")

emit() {
  jq -n --arg d "$1" --arg r "$2" '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: $d, permissionDecisionReason: $r}}'
  exit 0
}

if [ "$tool" = Bash ]; then
  cmd=$(jq -r '.tool_input.command // empty' <<<"$input")
  if grep -qE 'git[[:space:]]+clean[^;&|]*-[a-zA-Z]*[xX]' <<<"$cmd"; then
    emit ask "git clean -x/-X deletes ignored files, which includes every session directory. Confirm nothing under sessions/ is lost."
  fi
  if grep -qE '(^|[;&|(`[:space:]])(rm|mv|truncate|shred|tee|sed[[:space:]]+-i)([[:space:]][^;&|]*)?sessions(/|[[:space:]"'"'"']|$)|>>?[[:space:]]*["'"'"']?[^[:space:]]*sessions/' <<<"$cmd"; then
    emit ask "This command would change a session directory. Sessions are study data, git-ignored and not backed up: only the app should write there."
  fi
  exit 0
fi

file=$(jq -r '.tool_input.file_path // .tool_input.notebook_path // empty' <<<"$input")
case "$file" in
  "$root"/sessions/*|"$root"/instrument/sessions/*|sessions/*|instrument/sessions/*)
    emit deny "$(basename "$file") is recorded session data. Only the app writes to sessions/; corrections go through the console (trace review), and analysis reads exports." ;;
esac
exit 0
