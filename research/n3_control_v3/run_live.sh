#!/bin/bash
# I1c live runs. One cap, --max-usd 10, covers every OpenAI call in steps 5 and 6: each command
# charges openai_spend.jsonl, and the cap is checked against its total before every call.
# Usage: run_live.sh l73 <qwen|luna|sol>   |   run_live.sh domains <qwen|luna|sol>
set -euo pipefail
W="$(cd "$(dirname "$0")/../.." && pwd)"
V="$W/research/n3_control_v3"
R="$W/reconstruct/runs"
CAP=10
case "$2" in
  qwen) MODEL=qwen2.5:7b-instruct; LIVE=(--judge ollama) ;;
  luna) MODEL=gpt-5.6-luna; LIVE=(--judge openai --reasoning-effort medium --max-usd $CAP --spend-ledger "$V/openai_spend.jsonl") ;;
  sol) MODEL=gpt-6.1-sol; LIVE=(--judge openai --reasoning-effort high --max-usd $CAP --spend-ledger "$V/openai_spend.jsonl") ;;
esac
domain() {  # dir name run
  uv run --directory "$W/gapmap" python -m gapmap.control2 --ledger "$R/$3/ledger.json" \
    --sidecar "$R/$3/sidecar.json" --domain "$2" --out "$V/$TAG/$1" \
    --audit-cache "$W/research/n3/$1/closure_judgements.json" --model "$MODEL" "${LIVE[@]}" \
    ${PARALLEL:+--parallel-arm "$V/$PARALLEL/$1/control2.json"}
}
TAG=$2
# ADR 0009, enforced since I1c ran: an OpenAI judge goes live only beside the other-family arm.
[ "$2" = qwen ] || PARALLEL=qwen
if [ "$1" = l73 ]; then
  uv run --directory "$W/gapmap" python "$V/l73.py" --tag "$TAG" --model "$MODEL" "${LIVE[@]}"
else
  domain plc "PLC intermittent-fault diagnosis" 20260928T133336Z-59ec876b3d7e
  domain gdpr_v1 "GDPR DPIA (run v1)" 20260928T135354Z-eb840a85b7d1
  domain gdpr_v2 "GDPR DPIA (run v2)" 20260928T145943Z-bc1cc9a30a02
fi
