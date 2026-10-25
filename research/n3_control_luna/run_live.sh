#!/bin/bash
# I1b live run: control2 with gpt-5.6-luna on the three I1 domains. Caps sum to $5 with l73.py's $0.40.
set -euo pipefail
W="$(cd "$(dirname "$0")/../.." && pwd)"
R="$W/reconstruct/runs"
run() {  # name domain run cap
  uv run --directory "$W/gapmap" python -m gapmap.control2 --ledger "$R/$3/ledger.json" \
    --sidecar "$R/$3/sidecar.json" --domain "$2" --out "$W/research/n3_control_luna/$1" \
    --audit-cache "$W/research/n3/$1/closure_judgements.json" \
    --judge openai --model gpt-5.6-luna --max-usd "$4"
}
run plc "PLC intermittent-fault diagnosis" 20260928T133336Z-59ec876b3d7e 1.5
run gdpr_v1 "GDPR DPIA (run v1)" 20260928T135354Z-eb840a85b7d1 1.6
run gdpr_v2 "GDPR DPIA (run v2)" 20260928T145943Z-bc1cc9a30a02 1.5
