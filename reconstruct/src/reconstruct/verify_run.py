"""`python -m reconstruct.verify_run <run_dir>`: re-extracts from snapshots and re-slices every
locator (A14). Exit 0 iff every Evidence.selector.exact is exactly its own snapshot's text at
the locator's offsets; a missing snapshot or an unparsable locator is a failure, never a skip.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from residual.ledger import Ledger

_LOCATOR_RE = re.compile(r"^sha256:([0-9a-f]{64});char=(\d+),(\d+)$")


def verify_run(run_dir: str | Path) -> list[str]:
    """Returns a list of problem descriptions; empty means every locator checked out."""
    run_dir = Path(run_dir)
    problems: list[str] = []
    ledger_path = run_dir / "ledger.json"
    if not ledger_path.exists():
        return [f"missing ledger.json in {run_dir}"]
    ledger = Ledger.from_json(ledger_path.read_text())

    for claim in ledger.claims:
        for ev in claim.evidence:
            locator = ev.selector.locator or ""
            m = _LOCATOR_RE.match(locator)
            if not m:
                problems.append(f"{claim.claim_id}: locator does not match sha256:...;char=start,end: {locator!r}")
                continue
            sha, start, end = m.group(1), int(m.group(2)), int(m.group(3))
            snapshot_path = run_dir / "snapshots" / f"{sha}.txt"
            if not snapshot_path.exists():
                problems.append(f"{claim.claim_id}: missing snapshot {snapshot_path}")
                continue
            text = snapshot_path.read_text(encoding="utf-8")
            sliced = text[start:end]
            if sliced != (ev.selector.exact or ""):
                problems.append(f"{claim.claim_id}: snapshot slice does not match Selector.exact "
                                f"(locator {locator!r})")
    return problems


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python -m reconstruct.verify_run <run_dir>", file=sys.stderr)
        return 2
    problems = verify_run(argv[0])
    for p in problems:
        print(p, file=sys.stderr)
    if problems:
        print(f"{len(problems)} problem(s) found", file=sys.stderr)
        return 1
    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
