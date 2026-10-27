"""The parameterised pipeline on a second, unrelated unit (coordinator, 2026-10-27): E-LIVE's GDPR
ledger (`reconstruct/runs/20260928T145943Z-bc1cc9a30a02`, complete), with a corpus built from that
ledger's own assertions, one page per source. Pool, arms and the Stop A count must come out
non-empty and specific to this unit, with no D1 path, ledger or corpus involved. Fake closure
states; no model, no network."""
import hashlib
import html
import json
from pathlib import Path

import pytest

import build_sheet as bs
import codebase

REPO = Path(__file__).resolve().parents[3]
RUN = REPO / "reconstruct" / "runs" / "20260928T145943Z-bc1cc9a30a02"
D1B_POOL = Path(__file__).resolve().parents[1] / "pool.json"


@pytest.fixture(scope="module")
def unit(tmp_path_factory):
    from residual.ledger import Ledger

    root = tmp_path_factory.mktemp("gdpr")
    (root / "runs" / "gdpr").mkdir(parents=True)
    (root / "runs" / "gdpr" / RUN.name).symlink_to(RUN)
    lg = Ledger.from_json((RUN / "ledger.json").read_text())
    pages: dict[str, list[str]] = {}
    for claim in lg.by_id.values():
        for ev in claim.evidence:
            pages.setdefault(ev.source.identifier, []).append(claim.assertion)
    files = root / "corpus" / "files"
    files.mkdir(parents=True)
    docs = []
    for url, paras in sorted(pages.items()):
        body = "".join(f"<p>{html.escape(p)}</p>" for p in dict.fromkeys(paras))
        page = f"<!doctype html><html><body>{body}</body></html>".encode()
        digest = hashlib.sha256(page).hexdigest()
        (files / f"{digest}.html").write_bytes(page)
        docs.append({"url": url, "content_type": "text/html", "file": f"files/{digest}.html", "title": url})
    (root / "corpus" / "manifest.json").write_text(json.dumps({"documents": docs}))
    cfg = {"name": "gdpr-elive", "title": "Second unit", "owner_repo": "ico.org.uk", "domain": "gdpr", "seed": 11,
           "corpus": "corpus", "ledgers": {"gdpr": "runs/gdpr"}, "prior_items": None,
           "canaries": "fixtures/canaries.json", "canary_mode": "generated"}
    (root / "codebase.json").write_text(json.dumps(cfg))
    return codebase.load(root / "codebase.json")


def test_the_pool_on_a_second_unit_is_non_empty_and_its_own(unit):
    pool_text, pack_text, summary = bs.pool_outputs(unit)
    rows = json.loads(pool_text)["rows"]
    assert len(rows) >= 20 and {r["ledger"] for r in rows} == {"gdpr"}
    assert {r["source_origin"] for r in rows} == {"owner", "outside"}
    assert sum(r["similarity"] > 0 for r in rows) >= 0.9 * len(rows)
    d1b_quotes = {r["quote"] for r in json.loads(D1B_POOL.read_text())["rows"]}
    assert not d1b_quotes & {r["quote"] for r in rows}
    assert "D1" not in pack_text and summary["topics"] >= 10


def test_arms_and_the_stop_a_count_run_on_the_second_unit(unit, monkeypatch, tmp_path):
    pool_text, _, _ = bs.pool_outputs(unit)
    pool = tmp_path / "pool.json"
    pool.write_text(pool_text)
    (tmp_path / "review.json").write_text(json.dumps({"drop": []}))

    def fake_states(arm_dirs, rows_by_version, cb):
        assert cb is unit
        parity = lambda v: int(hashlib.sha256("|".join(v).encode()).hexdigest(), 16) % 2
        return {v: {arm: ("open" if parity(v) else "closed") for arm in arm_dirs} for v in rows_by_version}

    monkeypatch.setattr(bs, "_states", fake_states)
    args = type("A", (), {"pool": str(pool), "review": str(tmp_path / "review.json"), "unreviewed": False,
                          "arm": ["fake=/nonexistent"]})()
    topics, _, gaps, covs = bs._arms(args, unit)
    res = bs.count_summary(topics, gaps, covs, seed=unit.seed)
    assert res["all_open"] > 0 and res["all_closed"] > 0 and res["matched_pairs_uncapped"] > 0
    assert all(v[0] == "gdpr" for t in gaps + covs for v in t["versions"])


def test_an_incomplete_ledger_is_refused_unless_the_config_allows_it():
    dry = codebase.load(Path(__file__).resolve().parents[2] / "d1c" / "dryrun-dependence-forecastability"
                        / "codebase.json")
    assert dry.allow_incomplete_ledgers is True
    with pytest.raises(codebase.Incomplete, match="cross_verify: 761 failed calls"):
        bs.pool_rows(codebase.replace(dry, allow_incomplete_ledgers=False))
