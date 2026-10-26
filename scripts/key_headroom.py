#!/usr/bin/env python3
"""Read the OpenRouter key's remaining limit and the account's balance before a paid run.

A run's own --max-usd cap counts only that run's spend; the key's weekly limit is shared by every
run and spike, and twice a run was built and launched against a key already at zero. The key's
limit is not money: on 2026-10-25 the key showed $14.99 left while the account was empty (HTTP 402),
so the account balance (`/credits`) is read too and the smaller of the two decides.

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
CREDITS_URL = "https://openrouter.ai/api/v1/credits"


def _get(url: str, key: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())["data"]


def read_key_data() -> dict:
    """The key's fields plus `account` ({total_credits, total_usage}); a fake file without
    `account` stands for an account whose balance is not limiting."""
    fake = os.environ.get("KEY_HEADROOM_JSON")
    if fake:
        with open(fake) as f:
            return json.load(f)
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError("OPENROUTER_API_KEY is not in this environment")
    return {**_get(URL, key), "account": _get(CREDITS_URL, key)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--need", type=float, default=0.0, help="the run's estimate or cap, in USD")
    args = ap.parse_args(argv)
    try:
        d = read_key_data()
    except Exception as e:  # noqa: BLE001 — any failure means "not checked", never "fine"
        print(f"key headroom not read: {type(e).__name__}: {e}", file=sys.stderr)
        return 2
    account = d.get("account")
    balance = None if account is None else account["total_credits"] - account["total_usage"]
    print(f"key limit={d.get('limit')} remaining={d.get('limit_remaining')} usage_weekly={d.get('usage_weekly')} "
          f"reset={d.get('limit_reset')} account_balance={None if balance is None else round(balance, 4)} "
          f"need={args.need}")
    for name, left in (("key headroom", d.get("limit_remaining")), ("account balance", balance)):
        if left is not None and (left <= 0 or left < args.need):
            print(f"{name} ${left:.4f} does not cover ${args.need}", file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
