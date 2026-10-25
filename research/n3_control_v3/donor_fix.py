"""I1c step 1: what the donor fix changes on the committed ledgers, offline (no judge).

Per domain: pairs that can discriminate and the best reachable own - control difference (the
discriminable share) under I1's donor pool, under a pool that drops only the donor's seed
sentences, and under the fixed pools (both candidates' seed sources dropped from both arms); how many I1 control
control and own arms carried a donor seed sentence or a donor seed-source sentence; how many
pairs' arms change.

    uv run --directory gapmap python ../research/n3_control_v3/donor_fix.py > ../research/n3_control_v3/donor_fix.json
"""
import json
from pathlib import Path

from residual.ledger import Ledger

from gapmap import checks, config, control2, lenses, link, semantic

ROOT = Path(__file__).resolve().parents[2]
RUNS = {"plc": "20260928T133336Z-59ec876b3d7e", "gdpr_v1": "20260928T135354Z-eb840a85b7d1",
        "gdpr_v2": "20260928T145943Z-bc1cc9a30a02"}


def sentence_only_ks(lg, idx, cands) -> list[int]:
    """control2.build_pairs' k, had only the donor's seed sentences been dropped from I1's pool."""
    by_lens: dict[str, list] = {}
    for c in cands:
        by_lens.setdefault(c.lens, []).append(c)
    cap, out = config.JUDGE_A_CAP, []
    for ln in sorted(by_lens):
        cs = by_lens[ln]
        if len(cs) < 2:
            continue
        probes = [semantic.primary_probe(lg, c) for c in cs]
        keys = [control2.donor_key(c, p[1]) for c, p in zip(cs, probes)]
        order = sorted(range(len(cs)), key=lambda n: keys[n])
        probes, keys = [probes[n] for n in order], [keys[n] for n in order]
        seed_rows = [semantic.seed_sentences(idx, p[1]) for p in probes]
        ranked = [semantic.ranked_sentences(idx, idx.a_ids, p[0], control2._keys(s))
                  for p, s in zip(probes, seed_rows)]
        for i, (_st, ids_i, _q, _t) in enumerate(probes):
            srcs_i = {checks._source_of(lg, s) for s in ids_i}
            own_all = [r for r in ranked[i] if checks._source_of(lg, r[0]) not in srcs_i]
            own_top = control2._keys(own_all[:cap])
            j, _tied = control2.nearest_donor(i, [p[0] for p in probes], keys)
            donor = [r for r in ranked[j] if checks._source_of(lg, r[0]) not in srcs_i and (r[0], r[1]) not in own_top]
            out.append(min(cap, len(own_all), len(donor)))
    return out


def main() -> None:
    out = {}
    for d, run in RUNS.items():
        lg = Ledger.from_json((ROOT / "reconstruct/runs" / run / "ledger.json").read_text())
        idx = link.build_index(lg)
        cands = lenses.run_all(lg, idx, link.SETTING_1)
        legacy = control2.build_pairs(lg, idx, cands, legacy_donor_seed=True)
        fixed = control2.build_pairs(lg, idx, cands)
        sent_k = sentence_only_ks(lg, idx, cands)
        n = len(legacy)
        assert [s.seeds for s in legacy] == [s.seeds for s in fixed] and len(sent_k) == n
        donor_srcs = [{checks._source_of(lg, c) for c in s.donor_seeds} for s in legacy]
        seed_rows = [sum(r[0] in s.donor_seeds for r in s.donor_other) for s in legacy]
        src_rows = [sum(checks._source_of(lg, r[0]) in ds for r in s.donor_other) for s, ds in zip(legacy, donor_srcs)]
        out[d] = {
            "pairs": n,
            "i1_discriminable": sum(s.k >= 1 for s in legacy),
            "seed_sentences_only_discriminable": sum(k >= 1 for k in sent_k),
            "fixed_discriminable": sum(s.k >= 1 for s in fixed),
            "i1_control_arms_with_donor_seed_sentence": sum(x > 0 for x in seed_rows),
            "i1_donor_seed_sentences_in_control_arms": sum(seed_rows),
            "i1_control_arms_with_donor_seed_source_sentence": sum(x > 0 for x in src_rows),
            "i1_own_arms_with_donor_seed_sentence": sum(any(r[0] in s.donor_seeds for r in s.own_other)
                                                        for s in legacy),
            "i1_own_arms_with_donor_seed_source_sentence": sum(
                any(checks._source_of(lg, r[0]) in ds for r in s.own_other) for s, ds in zip(legacy, donor_srcs)),
            "pairs_whose_control_arm_changes": sum(a.donor_other != b.donor_other for a, b in zip(legacy, fixed)),
            "pairs_whose_own_arm_changes": sum(a.own_other != b.own_other for a, b in zip(legacy, fixed)),
            "pairs_whose_k_drops": sum(b.k < a.k for a, b in zip(legacy, fixed)),
            "k_sum_i1": sum(s.k for s in legacy), "k_sum_fixed": sum(s.k for s in fixed),
        }
    out["total"] = {k: sum(v[k] for v in out.values()) for k in out["plc"]}
    for v in out.values():
        for arm in ("i1", "seed_sentences_only", "fixed"):
            v[f"{arm}_best_reachable_diff"] = v[f"{arm}_discriminable"] / v["pairs"]
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
