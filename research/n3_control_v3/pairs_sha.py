"""I2 step 1: add `pairs_sha256` to sol's and qwen's committed `control2.json`, offline.

Each domain is replayed from its committed cache in a temporary directory (no `--judge`, no
network). The field is added only if the replay's `pairs`, `summary` and `length_stand_in` equal
the committed ones; any other differing field is reported. The committed `spend` is kept: an
offline replay of an OpenAI cache reports zero calls.

    uv run --directory gapmap python ../research/n3_control_v3/pairs_sha.py [--write]
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

from gapmap import control2

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RUNS = ROOT / "reconstruct/runs"
DOMAINS = {"plc": ("PLC intermittent-fault diagnosis", "20260928T133336Z-59ec876b3d7e"),
           "gdpr_v1": ("GDPR DPIA (run v1)", "20260928T135354Z-eb840a85b7d1"),
           "gdpr_v2": ("GDPR DPIA (run v2)", "20260928T145943Z-bc1cc9a30a02")}
JUDGES = {"sol": ["--model", "gpt-6.1-sol", "--reasoning-effort", "high"],
          "qwen": ["--model", "qwen2.5:7b-instruct"]}
MUST_MATCH = ("pairs", "summary", "length_stand_in")


def replay(judge: str, domain: str, tmp: Path) -> dict:
    name, run = DOMAINS[domain]
    out = tmp / judge / domain
    out.mkdir(parents=True)
    shutil.copy(HERE / judge / domain / "closure_judgements.json", out / "closure_judgements.json")
    control2.main(["--ledger", str(RUNS / run / "ledger.json"), "--sidecar", str(RUNS / run / "sidecar.json"),
                   "--domain", name, "--out", str(out),
                   "--audit-cache", str(ROOT / "research/n3" / domain / "closure_judgements.json"),
                   *JUDGES[judge]])
    return json.loads((out / "control2.json").read_text())


def main() -> int:
    write = "--write" in sys.argv[1:]
    report, ok = {}, True
    with tempfile.TemporaryDirectory() as t:
        for judge in JUDGES:
            for domain in DOMAINS:
                path = HERE / judge / domain / "control2.json"
                committed = json.loads(path.read_text())
                new = replay(judge, domain, Path(t))
                differ = sorted(k for k in set(committed) | set(new)
                                if k not in ("pairs_sha256", "spend") and committed.get(k) != new.get(k))
                good = not any(k in differ for k in MUST_MATCH)
                ok &= good
                report[f"{judge}/{domain}"] = {"pairs_sha256": new["pairs_sha256"], "differs": differ,
                                               "identical_pairs_summary_length": good}
                if write and good:
                    committed["pairs_sha256"] = new["pairs_sha256"]
                    path.write_text(json.dumps(committed, sort_keys=True, indent=1) + "\n")
    print(json.dumps(report, indent=1, sort_keys=True))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
