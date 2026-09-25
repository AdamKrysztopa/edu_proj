#!/usr/bin/env bash
# PostToolUse on Write|Edit: every doi.org link in an edited markdown file must resolve.
set -u

file=$(jq -r '.tool_input.file_path // .tool_response.filePath // empty')
case "$file" in
  *.md) ;;
  *) exit 0 ;;
esac
[ -f "$file" ] || exit 0

cache="${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/.doi-ok"
touch "$cache"

bad=()
while IFS= read -r url; do
  grep -qxF "$url" "$cache" && continue
  # doi.org answers 302 for registered DOIs and 404 for unknown ones; HEAD avoids publisher paywalls.
  code=$(curl -s -o /dev/null -w '%{http_code}' -I --max-time 8 "$url")
  case "$code" in
    30[1278]|200) echo "$url" >> "$cache" ;;
    000) ;;
    *) bad+=("$url ($code)") ;;
  esac
done < <(grep -oE 'https?://(dx\.)?doi\.org/10\.[0-9]{4,9}/[^][[:space:])>"]+' "$file" | sed -E 's/[.,;:]+$//' | sort -u)

[ ${#bad[@]} -eq 0 ] && exit 0

msg="Unresolvable DOI(s) in $(basename "$file"): ${bad[*]}. Verify each against OpenAlex or the publisher, then fix or remove it."
jq -n --arg m "$msg" '{decision: "block", reason: $m}'
