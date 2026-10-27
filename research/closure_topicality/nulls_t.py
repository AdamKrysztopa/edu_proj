"""control2 and MEC with topicality-matched donors, stand-ins only, $0 (plan §2).

The rule is fixed in the plan: both nulls are declared unrepairable as judge certificates on these
ledgers, because without element labels no planted positive can be built for them. This measures
how far matching goes on all five ledgers:
- control2-T: control2's pairs and exclusions, the donor rebuilt only from j's ranked pool (minus
  i's own top k and both seed sources) by exact per-sentence match on seed-and-question overlap,
  ties by closest length; control2-TT also matches probe overlap. Seed-free arms.
- MEC-T, MEC-TT: the gap map's MEC arms (seed + own other-source rows vs seed + donor rows), the
  donor rows matched the same two ways from j's ranked pool minus i's seed sources and own rows.
A pair with an unmatched own sentence is dropped from both arms.

    uv run --directory gapmap python ../research/closure_topicality/nulls_t.py
"""
from __future__ import annotations

import glob
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from residual.ledger import Ledger

from gapmap import checks, config, control2, lenses, link, record, semantic, standins, text

import standins_t as st

HERE = Path(__file__).resolve().parent
W = HERE.parents[1]
LEDGERS = {
    "d1_cheap": ("research/d1_demonstrator/runs/cheap-26b/*/ledger.json",),
    "d1_top": ("research/d1_demonstrator/runs/toptier-26b/*/ledger.json",),
    "plc": ("reconstruct/runs/20260928T133336Z-59ec876b3d7e/ledger.json",),
    "gdpr_v1": ("reconstruct/runs/20260928T135354Z-eb840a85b7d1/ledger.json",),
    "gdpr_v2": ("reconstruct/runs/20260928T145943Z-bc1cc9a30a02/ledger.json",),
}
READ_FLOOR = 20

Row = tuple[str, int, str]


@dataclass(frozen=True)
class ArmPair:
    cluster: str
    seed_text: str
    question: str
    own: list
    ctrl: list


def overlap_key(seed_text: str, question: str) -> Callable[[str], int]:
    ctx = text.cw(seed_text + " " + question)
    return lambda s: len(ctx & text.cw(s))


def both_key(seed_text: str, question: str, probe: frozenset[str]) -> Callable[[str], tuple]:
    ov = overlap_key(seed_text, question)
    return lambda s: (len(probe & text.cw(s)), ov(s))


def match(own: list[Row], pool: list[Row], key: Callable[[str], object],
          exclude: set[tuple[str, int]] = frozenset()) -> list[Row] | None:
    used: set[tuple[str, int]] = set()
    out = []
    for o in own:
        cands = [(abs(len(r[2]) - len(o[2])), n, r) for n, r in enumerate(pool)
                 if (r[0], r[1]) not in exclude and (r[0], r[1]) not in used and key(r[2]) == key(o[2])]
        if not cands:
            return None
        _d, _n, r = min(cands, key=lambda c: (c[0], c[1]))
        used.add((r[0], r[1]))
        out.append(r)
    return out


def _prompt(pair: ArmPair, rows: list[Row]) -> str:
    return semantic.build_prompt(pair.seed_text, pair.question, semantic.build_retrieval(rows))


def stand_in_rows(pairs: list[ArmPair], *, source_of: dict[str, str]) -> dict:
    """Arm-level stand-ins on the pairs: own - control closed rate with control2's cluster CI."""
    prompts = [_prompt(p, rows) for p in pairs for rows in (p.own, p.ctrl)]
    if not prompts:
        return {}
    judges = [*st.arm_level(prompts),
              standins.calibrate("sources", standins.source_count(source_of), prompts)]
    out = {}
    for j in judges:
        diffs = []
        for p in pairs:
            o = j.ask(_prompt(p, p.own))["states"] != []
            c = j.ask(_prompt(p, p.ctrl))["states"] != []
            diffs.append((p.cluster, float(o) - float(c)))
        out[j.model_id] = {"diff": sum(d for _c, d in diffs) / len(diffs),
                           "ci95": control2._cluster_ci(diffs, control2.BOOTSTRAP_B, control2.BOOTSTRAP_SEED)}
    return out


def _source_of_sentence(ledger: Ledger, index: link.Index) -> dict[str, str]:
    out = {}
    for cid, body in index.T.items():
        for sent in text.sentences(body):
            out.setdefault(sent, checks._source_of(ledger, cid))
    return out


def _control2_pairs(ledger: Ledger, index: link.Index, candidates: list) -> dict[str, list[ArmPair]]:
    """control2.build_pairs' loop, keeping j's whole eligible pool and i's probe."""
    by_lens: dict[str, list] = {}
    for c in candidates:
        by_lens.setdefault(c.lens, []).append(c)
    out = {"control2": [], "control2-T": [], "control2-TT": []}
    cap = config.JUDGE_A_CAP
    for lens_name in sorted(by_lens):
        cs = by_lens[lens_name]
        if len(cs) < 2:
            continue
        probes = [semantic.primary_probe(ledger, c) for c in cs]
        keys = [control2.donor_key(c, p[1]) for c, p in zip(cs, probes)]
        order = sorted(range(len(cs)), key=lambda n: keys[n])
        probes, keys = [probes[n] for n in order], [keys[n] for n in order]
        seed_rows = [semantic.seed_sentences(index, p[1]) for p in probes]
        ranked = [semantic.ranked_sentences(index, index.a_ids, p[0], control2._keys(s))
                  for p, s in zip(probes, seed_rows)]
        for i, (stems_i, ids_i, question, seed_text) in enumerate(probes):
            j, _tied = control2.nearest_donor(i, [p[0] for p in probes], keys)
            excluded = {checks._source_of(ledger, s) for s in ids_i} | {checks._source_of(ledger, s) for s in probes[j][1]}
            own_all = [r for r in ranked[i] if checks._source_of(ledger, r[0]) not in excluded]
            own_top = control2._keys(own_all[:cap])
            donor_all = [r for r in ranked[j] if checks._source_of(ledger, r[0]) not in excluded
                         and (r[0], r[1]) not in own_top]
            k = min(cap, len(own_all), len(donor_all))
            if k < 1:
                continue
            own = own_all[:k]
            mk = lambda ctrl: ArmPair(cluster=keys[i][0][0], seed_text=seed_text, question=question,
                                      own=list(own), ctrl=list(ctrl))
            out["control2"].append(mk(donor_all[:k]))
            for name, key in (("control2-T", overlap_key(seed_text, question)),
                              ("control2-TT", both_key(seed_text, question, stems_i))):
                m = match(own, donor_all, key)
                if m is not None:
                    out[name].append(mk(m))
    return out


def _mec_pairs(ledger: Ledger, ledger_sha: str, index: link.Index, candidates: list) -> dict[str, list[ArmPair]]:
    by_lens: dict[str, list] = {}
    for c in candidates:
        by_lens.setdefault(c.lens, []).append(c)
    out = {"MEC": [], "MEC-T": [], "MEC-TT": []}

    def gap_id(c) -> str:
        return record.make_gap_id(config.CONFIG_SHA256, ledger_sha, c.lens, c.seeds)

    for lens_name in sorted(by_lens):
        cs = sorted(by_lens[lens_name], key=gap_id)
        if len(cs) < 2:
            continue
        gap_ids = [gap_id(c) for c in cs]
        probes = [semantic.primary_probe(ledger, c) for c in cs]
        retrievals = [semantic.retrieve(index, ids, stems) for stems, ids, _q, _t in probes]
        for i, (stems_i, ids_i, question, seed_text) in enumerate(probes):
            srcs_i = {checks._source_of(ledger, s) for s in ids_i}
            seed_items = [(x[1], 0, x[2]) for x in retrievals[i].a_items if x[1] in ids_i]
            other_i = [(x[1], 0, x[2]) for x in retrievals[i].a_items if checks._source_of(ledger, x[1]) not in srcs_i]
            j = checks._nearest_other(i, [p[0] for p in probes], gap_ids)
            other_j = [(x[1], 0, x[2]) for x in retrievals[j].a_items if checks._source_of(ledger, x[1]) not in srcs_i]
            mk = lambda ctrl: ArmPair(cluster=min(ids_i), seed_text=seed_text, question=question,
                                      own=seed_items + other_i, ctrl=seed_items + list(ctrl))
            out["MEC"].append(mk(other_j))
            if not other_i:
                continue
            seed_j = control2._keys(semantic.seed_sentences(index, probes[j][1]))
            pool = [r for r in semantic.ranked_sentences(index, index.a_ids, probes[j][0], seed_j)
                    if checks._source_of(ledger, r[0]) not in srcs_i]
            own_texts = {s for _c, _n, s in other_i}
            pool = [r for r in pool if r[2] not in own_texts]
            for name, key in (("MEC-T", overlap_key(seed_text, question)),
                              ("MEC-TT", both_key(seed_text, question, stems_i))):
                m = match(other_i, pool, key)
                if m is not None:
                    out[name].append(mk(m))
    return out


def measure(name: str) -> dict:
    (path,) = glob.glob(str(W / LEDGERS[name][0]))
    ledger_text = Path(path).read_text()
    ledger = Ledger.from_json(ledger_text)
    index = link.build_index(ledger)
    cands = lenses.run_all(ledger, index, link.SETTING_1)
    sha = control2._sha256_text(ledger_text)
    src = _source_of_sentence(ledger, index)
    nulls = {**_control2_pairs(ledger, index, cands), **_mec_pairs(ledger, sha, index, cands)}
    base = {"control2": len(nulls["control2"]), "MEC": len(nulls["MEC"])}
    out = {}
    for null, pairs in nulls.items():
        n0 = base["control2" if null.startswith("control2") else "MEC"]
        rows = stand_in_rows(pairs, source_of=src)
        passing = sorted(j for j, r in rows.items() if r["ci95"] is not None and r["ci95"][0] > 0)
        out[null] = {"n_pairs": len(pairs), "of": n0, "best_reachable": len(pairs) / n0 if n0 else None,
                     "readable": len(pairs) >= READ_FLOOR, "stand_ins_with_ci_above_0": passing,
                     "stand_ins": rows}
    return {"ledger_sha256": sha, "nulls": out}


def main() -> int:
    result = {name: measure(name) for name in LEDGERS}
    result["rule"] = ("declared unrepairable as judge certificates (plan §2.3): no planted positive "
                      "exists for a real-data null without element labels")
    (HERE / "nulls_t.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    for name in LEDGERS:
        for null, r in result[name]["nulls"].items():
            ov = r["stand_ins"].get("standin-overlap", {})
            pr = r["stand_ins"].get("standin-probe", {})
            print(f"{name:9s} {null:12s} n {r['n_pairs']:3d}/{r['of']:3d} overlap {ov.get('diff', float('nan')):+.2f} "
                  f"{ov.get('ci95')} probe {pr.get('diff', float('nan')):+.2f} {pr.get('ci95')} "
                  f"passing {r['stand_ins_with_ci_above_0']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
