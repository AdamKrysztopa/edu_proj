"""I7 step 3: `admit` on the planted fixtures, then replayed on every committed E-LIVE sidecar's
sources at the fixtures' invented gold date (1994-06-01, the era of the 1993-94 CTA golds), with no
blocklist. The replay reads only dates; it opens no gold.

    uv run --directory reconstruct python ../research/freeze_manifest/admission_report.py
"""
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "reconstruct/tests"))
from admission_fixtures import BLOCKLIST, GOLD_DATE, PLANTED  # noqa: E402

from reconstruct.admission import Blocklist, Document, admit  # noqa: E402


def _date(s: str | None) -> date | None:
    return date.fromisoformat(s) if s else None


def from_sidecar(s: dict) -> Document:
    """A sidecar's `published` is the later of the page's published and modified dates (run.py A9);
    with no `published_field` it came from a modification field, so it is not a publication date.
    Sidecars before modified_field existed leave the field unknown, which `admit` treats as page-stated."""
    return Document(url=s["requested_url"], final_url=s.get("final_url"), title=s.get("title"),
                    published=_date(s.get("published")) if s.get("published_field") else None,
                    published_field=s.get("published_field"), modified=_date(s.get("modified")),
                    modified_field=s.get("modified_field"))


fixtures = []
for name, doc, expected in PLANTED:
    got = admit(doc, GOLD_DATE, BLOCKLIST)
    fixtures.append({"plant": name, "expected": expected or "admitted",
                     "observed": "admitted" if got.admitted else ",".join(got.reasons),
                     "ok": (got.admitted and expected is None) or (expected in got.reasons)})

replay = []
for path in sorted((ROOT / "reconstruct/runs").glob("*/sidecar.json")):
    sources = json.loads(path.read_text()).get("sources", {})
    if not sources:
        continue
    reasons = Counter()
    for s in sources.values():
        got = admit(from_sidecar(s), GOLD_DATE, Blocklist.of())
        reasons["admitted" if got.admitted else got.reasons[0]] += 1
    replay.append({"run": path.parent.name, "sources": len(sources), **dict(sorted(reasons.items()))})

out = {"gold_date": GOLD_DATE.isoformat(), "fixtures": fixtures,
       "fixtures_ok": sum(f["ok"] for f in fixtures), "fixtures_n": len(fixtures),
       "replay_committed_sidecars": replay,
       "replay_admitted": sum(r.get("admitted", 0) for r in replay),
       "replay_sources": sum(r["sources"] for r in replay)}
(HERE / "admission.json").write_text(json.dumps(out, indent=1) + "\n")
print(f"fixtures {out['fixtures_ok']}/{out['fixtures_n']}; replay admitted "
      f"{out['replay_admitted']}/{out['replay_sources']}: {replay}")
