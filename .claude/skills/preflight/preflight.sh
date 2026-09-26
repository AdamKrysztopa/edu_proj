#!/usr/bin/env bash
# Mechanical half of /preflight. Usage: preflight.sh pilot|data   (run from the repository root)
# Prints one PASS/WARN/FAIL/SKIP line per check, then REVIEW_BASE=<sha|none>. Exits 1 on any FAIL.
set -u
mode="${1:-}"
case "$mode" in pilot|data) ;; *) echo "usage: preflight.sh pilot|data" >&2; exit 2 ;; esac

root=$(git rev-parse --show-toplevel)
inst="$root/instrument"
work=$(mktemp -d "${TMPDIR:-/tmp}/preflight.XXXXXX")
failed=0
report() { echo "$1 $2"; [ "$1" = FAIL ] && failed=1; return 0; }
py() { uv run --quiet --directory "$inst" python -c "$1"; }

dirty=$(git -C "$inst" status --porcelain -- .)
if [ -z "$dirty" ]; then report PASS "tree: instrument/ is clean"
elif [ "$mode" = data ]; then report FAIL "tree: instrument/ has uncommitted changes; the app will refuse a data session"
else report WARN "tree: instrument/ has uncommitted changes; the pilot manifest will record git_dirty=true"
fi

if [ "$mode" = data ]; then
  if out=$(py 'from probe_app.config import check_preregistered, current_config; check_preregistered(current_config())' 2>&1)
  then report PASS "prereg: current config matches prereg.json"
  else report FAIL "prereg: ${out##*ConfigMismatch: }"
  fi
else
  report SKIP "prereg: not required for pilots"
fi

if out=$(uv run --quiet --directory "$inst" pytest -q 2>&1); then report PASS "tests: $(tail -1 <<<"$out")"
else report FAIL "tests: $(tail -1 <<<"$out")"
fi

# Live transcriber check: fakes never exercise the API key, quota or model name.
if command -v say >/dev/null; then
  wav="$work/phrase.wav"
  say --data-format=LEI16@16000 -o "$wav" "The total momentum is conserved in the inelastic collision."
  models=$(py 'from probe_app.config import TRANSCRIBER_MODEL; print(TRANSCRIBER_MODEL)')
  [ "$mode" = pilot ] && models="scribe_v2 whisper-1"
  for m in $models; do
    out=$(uv run --quiet --directory "$inst" probe-app transcribe "$wav" --model "$m" 2>&1)
    if grep -qi momentum <<<"$out" && grep -qi inelastic <<<"$out"; then report PASS "transcriber $m: heard the test phrase"
    else report FAIL "transcriber $m: $(tail -1 <<<"$out")"
    fi
  done
else
  report SKIP "transcriber: no \`say\` to synthesise the test phrase; transcribe a short recording by hand"
fi

# Live simulated session: the only check that exercises real refusals (fakes never refuse).
out=$(uv run --quiet --directory "$inst" probe-app simulate --root "$work/sessions" 2>&1)
sdir=$(sed -n 's/^simulated session: //p' <<<"$out")
if [ -z "$sdir" ]; then
  report FAIL "simulation: $(tail -1 <<<"$out")"
else
  phase=$(jq -r .phase "$sdir/state.json")
  counts=$(py "import json; from probe_code.guard_audit import ai_rejection_counts; print(json.dumps(ai_rejection_counts('$sdir')))")
  read -r turns failures <<<"$(jq -r '"\(.accepted + .fallback) \(.interviewer_failed)"' <<<"$counts")"
  if [ "$phase" != done ]; then report FAIL "simulation: stopped in phase '$phase' ($sdir)"
  elif [ "$turns" -eq 0 ] || [ $((failures * 10)) -gt "$turns" ]; then
    report WARN "simulation: interviewer_failed $failures of $turns AI turns, above the protocol's 1 in 10 ($counts)"
  else report PASS "simulation: completed; $counts"
  fi
fi

# Review base: the commit of the last real session, else the freeze, else none (review everything).
base=none
last=$(ls -t "$root"/sessions/*/manifest.json 2>/dev/null | while read -r m; do
  [ "$(jq -r .simulated "$m")" = true ] || { jq -r .git_commit "$m"; break; }; done)
if [ -n "$last" ]; then base=$last
elif frozen=$(git -C "$root" log -1 --format=%H -- instrument/prereg.json) && [ -n "$frozen" ]; then base=$frozen
fi
echo "REVIEW_BASE=$base"
rm -rf "$work"
exit $failed
