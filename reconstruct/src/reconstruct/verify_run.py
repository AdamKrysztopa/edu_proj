"""`python -m reconstruct.verify_run <run_dir>`: checks a run's provenance against its own
snapshots (A14, R9). Exit 0 iff every snapshot a locator or a sidecar source names exists and
hashes to its filename, every Source's evidence points at the snapshot the sidecar binds that
source to, and every Evidence.selector.exact is exactly that snapshot's text at the locator's
offsets. A missing file or an unparsable locator is a failure, never a skip. Web mode stores
normalised text only, so nothing is re-extracted from raw bytes.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from residual.ledger import Ledger

_LOCATOR_RE = re.compile(r"^sha256:([0-9a-f]{64});char=(\d+),(\d+)$")


def verify_run(run_dir: str | Path) -> list[str]:
    """Returns a list of problem descriptions; empty means every check passed."""
    run_dir = Path(run_dir)
    problems: list[str] = []
    ledger_path = run_dir / "ledger.json"
    if not ledger_path.exists():
        return [f"missing ledger.json in {run_dir}"]
    ledger = Ledger.from_json(ledger_path.read_text())
    sidecar_path = run_dir / "sidecar.json"
    if sidecar_path.exists():
        bound = {sid: s.get("text_sha256")
                 for sid, s in json.loads(sidecar_path.read_text()).get("sources", {}).items()}
    else:
        problems.append(f"missing sidecar.json in {run_dir}: Source-to-snapshot binding unchecked")
        bound = None

    texts: dict[str, str | None] = {}

    def snapshot_text(sha: str, who: str) -> str | None:
        if sha not in texts:
            path = run_dir / "snapshots" / f"{sha}.txt"
            if not path.exists():
                problems.append(f"{who}: missing snapshot {path}")
                texts[sha] = None
            else:
                data = path.read_bytes()
                if hashlib.sha256(data).hexdigest() != sha:
                    problems.append(f"{who}: snapshot {path.name} digest does not match its filename")
                texts[sha] = data.decode("utf-8")
        return texts[sha]

    for source_id, sha in (bound or {}).items():
        if sha:
            snapshot_text(sha, f"source {source_id}")

    for claim in ledger.claims:
        for ev in claim.evidence:
            locator = ev.selector.locator or ""
            m = _LOCATOR_RE.match(locator)
            if not m:
                problems.append(f"{claim.claim_id}: locator does not match sha256:...;char=start,end: {locator!r}")
                continue
            sha, start, end = m.group(1), int(m.group(2)), int(m.group(3))
            source_id = ev.source.source_id
            if bound is not None and bound.get(source_id) != sha:
                problems.append(f"{claim.claim_id}: source {source_id} is bound to snapshot "
                                f"{bound.get(source_id)!r} in the sidecar, but its locator names {sha}")
            text = snapshot_text(sha, claim.claim_id)
            if text is None:
                continue
            if text[start:end] != (ev.selector.exact or ""):
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
