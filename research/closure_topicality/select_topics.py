"""RT topics (plan §1.3), $0, reads no judge state.

- d1: G2's 13 gate topics (owner-confirmed P and N, `research/d1b_rerun/fixtures/`) with each
  topic's control2 spec on its D1 ledger as background.
- gdpr: one control2 pair per seed cluster from GDPR v1's discriminable pairs, lens quotas, in the
  order of a seeded shuffle; the rest of each lens's order is kept as the replacement reserve.

    uv run --directory gapmap python ../research/closure_topicality/select_topics.py d1|gdpr
"""
from __future__ import annotations

import glob
import json
import random
import sys
from pathlib import Path

from residual.ledger import Ledger

from gapmap import control2, lenses, link, semantic

HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
FIXTURES = HERE / "fixtures"
G2 = W / "research" / "d1b_rerun" / "fixtures"
GDPR_V1 = W / "reconstruct" / "runs" / "20260928T135354Z-eb840a85b7d1" / "ledger.json"
SOL_GDPR_V1 = W / "research" / "n3_control_v3" / "sol" / "gdpr_v1" / "control2.json"
QUOTAS = {"DISC": 3, "WHY": 3, "HEDGE": 3, "SEL": 2, "RESULT": 5}
SEED = 20261027


def pick(specs: list, quotas: dict[str, int], *, seed: int) -> tuple[list, dict[str, list]]:
    order = [s for s in specs if s.k >= 1]
    random.Random(seed).shuffle(order)
    chosen, used, reserve = [], set(), {lens: [] for lens in quotas}
    for s in order:
        if s.lens not in quotas or s.seeds[0] in used:
            continue
        if sum(c.lens == s.lens for c in chosen) < quotas[s.lens]:
            chosen.append(s)
            used.add(s.seeds[0])
    for s in order:
        if s.lens in quotas and s.seeds[0] not in used and all(r.seeds[0] != s.seeds[0] for r in reserve[s.lens]):
            reserve[s.lens].append(s)
    return chosen, reserve


def _specs_and_probes(ledger_path: Path):
    lg = Ledger.from_json(ledger_path.read_text())
    idx = link.build_index(lg)
    cands = lenses.run_all(lg, idx, link.SETTING_1)
    probes = {}
    for c in cands:
        stems, ids, question, _seed = semantic.primary_probe(lg, c)
        probes[(c.lens, tuple(sorted(ids)), question)] = stems
    return control2.build_pairs(lg, idx, cands), probes


def _topic(tid: str, split: str, cluster: str, spec, probe) -> dict:
    return {"topic_id": tid, "split": split, "cluster": cluster, "lens": spec.lens, "seeds": list(spec.seeds),
            "seed_text": spec.seed_text, "question": spec.question, "k": spec.k,
            "background_rows": [list(r) for r in spec.own_other], "probe": sorted(probe)}


def build_d1() -> dict:
    g2 = json.loads((G2 / "topics.json").read_text())["topics"]
    dropped = json.loads((G2 / "confirmations.json").read_text())["_dropped"]
    inserts = json.loads((G2 / "inserts.json").read_text())
    gate = [t for t in g2 if t["split"] == "gate" and t["topic_id"] not in dropped]
    loaded = {}
    topics, ins = [], {}
    for t in gate:
        if t["ledger"] not in loaded:
            (path,) = glob.glob(str(W / f"research/d1_demonstrator/runs/{t['ledger']}/*/ledger.json"))
            loaded[t["ledger"]] = _specs_and_probes(Path(path))
        specs, probes = loaded[t["ledger"]]
        cid = t["test_id"].split(":", 1)[1]
        (spec,) = [s for s in specs if s.lens == t["lens"] and cid in s.seeds
                   and s.seed_text == t["seed_text"] and s.question == t["question"]]
        topic = _topic(t["topic_id"], "d1", t["cluster"], spec, probes[(spec.lens, spec.seeds, spec.question)])
        topic["ledger"] = t["ledger"]
        topics.append(topic)
        ins[t["topic_id"]] = {"P": inserts[t["topic_id"]]["P"], "N": inserts[t["topic_id"]]["N"]}
    note = ("G2's gate topics after the owner's drops; P and N copied unchanged from "
            "research/d1b_rerun/fixtures/inserts.json, confirmed by the owner 2026-10-26")
    return {"topics": {"note": note, "topics": topics}, "inserts": {"note": note, "inserts": ins}}


def build_gdpr() -> dict:
    specs, probes = _specs_and_probes(GDPR_V1)
    sha = control2.pairs_sha256(specs)
    if sha != json.loads(SOL_GDPR_V1.read_text())["pairs_sha256"]:
        raise SystemExit("GDPR v1 pairs differ from sol's I1c pairs")
    chosen, reserve = pick(specs, QUOTAS, seed=SEED)
    topics = [_topic(f"g{n:02d}", "gdpr", s.seeds[0], s, probes[(s.lens, s.seeds, s.question)]) for n, s in enumerate(chosen, 1)]
    res = {lens: [_topic(f"r-{lens}-{n}", "gdpr", s.seeds[0], s, probes[(s.lens, s.seeds, s.question)])
                  for n, s in enumerate(rs, 1)] for lens, rs in reserve.items()}
    return {"topics": {"pairs_sha256": sha, "seed": SEED, "quotas": QUOTAS, "topics": topics, "reserve": res}}


def main() -> int:
    which = sys.argv[1]
    out = build_d1() if which == "d1" else build_gdpr()
    FIXTURES.mkdir(parents=True, exist_ok=True)
    (FIXTURES / f"topics_{which}.json").write_text(json.dumps(out["topics"], indent=1, sort_keys=True) + "\n")
    if "inserts" in out:
        (FIXTURES / f"inserts_{which}.json").write_text(json.dumps(out["inserts"], indent=1, sort_keys=True) + "\n")
    print(which, len(out["topics"]["topics"]), "topics")
    return 0


if __name__ == "__main__":
    sys.exit(main())
