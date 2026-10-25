#!/bin/sh
# Replays I6 from the committed E-LIVE ledgers and judge caches: no network, no cost.
set -eu
cd "$(dirname "$0")/../../gapmap"
R=../reconstruct/runs
OUT=../research/area_score
PLC=20260928T133336Z-59ec876b3d7e
V1=20260928T135354Z-eb840a85b7d1
V2=20260928T145943Z-bc1cc9a30a02
uv run python -m gapmap.area run --ledger $R/$PLC/ledger.json --sidecar $R/$PLC/sidecar.json \
  --cache ../research/n3/plc/closure_judgements.json --domain plc --out $OUT/plc
uv run python -m gapmap.area run --ledger $R/$V1/ledger.json --sidecar $R/$V1/sidecar.json \
  --sibling $R/$V2/ledger.json --cache ../research/n3/gdpr_v1/closure_judgements.json \
  --domain gdpr_v1 --out $OUT/gdpr_v1
uv run python -m gapmap.area run --ledger $R/$V2/ledger.json --sidecar $R/$V2/sidecar.json \
  --sibling $R/$V1/ledger.json --cache ../research/n3/gdpr_v2/closure_judgements.json \
  --domain gdpr_v2 --out $OUT/gdpr_v2
uv run python -m gapmap.area summary --out $OUT $OUT/plc $OUT/gdpr_v1 $OUT/gdpr_v2
