#!/usr/bin/env bash
# PreToolUse on Bash: refuse a bulk `git add` while an untracked directory holds its own repository,
# which git would commit as an embedded repo (an agent worktree nearly went in this way).
set -u

cmd=$(jq -r '.tool_input.command // empty')
printf '%s' "$cmd" | grep -qE 'git( -C [^ ]+)? add( [^;&|]*)? (-A|--all|\.|:/)( |$|;|&)' || exit 0

cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
nested=()
while IFS= read -r d; do
  [ -e "${d%/}/.git" ] && nested+=("${d%/}")
done < <(git ls-files --others --exclude-standard --directory 2>/dev/null | grep '/$')
[ ${#nested[@]} -eq 0 ] && exit 0

msg="Refused: untracked nested repository ${nested[*]} would be committed as an embedded repo. Gitignore it (or remove the worktree with \`git worktree remove\`), or stage explicit paths."
jq -n --arg m "$msg" '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: "deny", permissionDecisionReason: $m}}'
