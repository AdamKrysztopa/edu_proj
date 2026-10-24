#!/usr/bin/env python3
"""Read the OpenRouter key's remaining limit before a paid run.

A run's own --max-usd cap counts only that run's spend; the key's weekly limit is shared by every
run and spike, and twice a run was built and launched against a key already at zero.

    python3 scripts/key_headroom.py [--need USD]

Prints the limit fields only, never the key. Exit 0: headroom covers --need (or the key has no
limit). Exit 1: it does not. Exit 2: the headroom could not be read.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request

URL = "https://openrouter.ai/api/v1/key"


def read_key_data() -> dict:
    fake = os.environ.get("KEY_HEADROOM_JSON")
    if fake:
        with open(fake) as f:
            return json.load(f)
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not in this environment")
    req = urllib.request.Request(URL, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())["data"]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need", type=float, default=0.0, help="the run's estimate or cap, in USD")
    args = ap.parse_args(argv)
    try:
        d = read_key_data()
    except Exception as e:  # noqa: BLE001 — any failure means "not checked", never "fine"
        print(f"key headroom not read: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    remaining = d.get("limit_remaining")
    print(f"key limit={d.get('limit')} remaining={remaining} usage_weekly={d.get('usage_weekly')} "
          f"reset={d.get('limit_reset')} need={args.need}")
    if remaining is None:
        return 0
    if remaining <= 0 or remaining < args.need:
        print(f"key headroom ${remaining} does not cover ${args.need}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
