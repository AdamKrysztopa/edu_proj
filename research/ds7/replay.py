"""DS7 replay: which URLs in the committed N2 runs (`reconstruct/runs/`, the ledgers N3 reads) are
boundary or incident hosts, under the current host rules and under DS7's proposed hosts (note §3).
"cited" = sources holding evidence in the ledger; "recorded" = every URL in the run's sidecar
(search hits, fetches, failures). Offline, no network. Run from reconstruct/:
    uv run python ../research/ds7/replay.py > ../research/ds7/replay.json
"""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

from reconstruct.evidence import classify_source

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "reconstruct/runs"
N3_LEDGERS = {"20260928T133336Z-59ec876b3d7e": "PLC", "20260928T135354Z-eb840a85b7d1": "GDPR v1",
              "20260928T145943Z-bc1cc9a30a02": "GDPR v2"}

PROPOSED_BOUNDARY_HOSTS = ("firefighternearmiss.com", "wildfirelessons.net", "lessons.wildfire.gov",
                           "psnet.ahrq.gov", "webmm.ahrq.gov", "asrs.arc.nasa.gov", "allnurses.com")
PROPOSED_OTHER_HOSTS = ("judiciary.uk", "api.fda.gov", "accessdata.fda.gov", "ntsb.gov",
                        "academic.oup.com", "casereports.bmj.com")


def _host(url: str) -> str:
    return urlsplit(url).netloc.split(":", 1)[0].casefold()


def _matches(host: str, known: tuple[str, ...]) -> bool:
    return any(host == h or host.endswith("." + h) for h in known)


def proposed_boundary(url: str) -> bool:
    host = _host(url)
    niosh_fire = _matches(host, ("cdc.gov",)) and urlsplit(url).path.startswith("/niosh/fire")
    return niosh_fire or _matches(host, PROPOSED_BOUNDARY_HOSTS)


def proposed_any(url: str) -> bool:
    return proposed_boundary(url) or _matches(_host(url), PROPOSED_OTHER_HOSTS)


def counts(urls: list[str]) -> dict:
    current = [classify_source(u) for u in urls]
    return {
        "n": len(urls),
        "boundary_current_rules": sum(c.boundary for c in current),
        "boundary_current_rules_urls": sorted(u for u, c in zip(urls, current) if c.boundary),
        "boundary_proposed": sum(c.boundary or proposed_boundary(u) for u, c in zip(urls, current)),
        "hit_any_proposed_host": sum(proposed_any(u) for u in urls),
    }


def main() -> None:
    out = {}
    for run_dir in sorted(p for p in RUNS.iterdir() if p.is_dir()):
        ledger = json.loads((run_dir / "ledger.json").read_text())
        sidecar_text = (run_dir / "sidecar.json").read_text()
        cited = sorted({e["source"]["identifier"] for c in ledger["claims"] for e in c["evidence"]})
        recorded = sorted(set(re.findall(r'https?://[^"\s]+', sidecar_text)))
        out[run_dir.name] = {
            "n3_ledger": N3_LEDGERS.get(run_dir.name),
            "complete": json.loads(sidecar_text).get("complete"),
            "cited": counts(cited),
            "recorded": counts(recorded),
        }
    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
