"""I1: the closure control rebuilt so it can discriminate (coverage audit findings 6-9, 11, 18).

Each lens candidate `i` is paired with the topically nearest other candidate `j` of the same lens
(max probe-stem Jaccard; ties by sorted seed claim ids, then lens -- never the config hash).
Both arms take the same number `k` of non-seed, other-source sentences, the cap applied after the
seed: `k = min(JUDGE_A_CAP, |own pool|, |donor pool|)`. Both pools drop the seed sources of both
`i` and `j` (own: `i`'s retrieval; donor: `j`'s retrieval, also minus `i`'s own capped pool so
the arms are disjoint), so both arms are seed-free under the same seed exclusions. Two comparisons: equal-cap (`i`'s seed + k
sentences) and seed-free (the k sentences alone), both only on pairs with `k >= 1`; two splits,
closed-or-partial and closed only; intervals resample seed claims.

    uv run --directory gapmap python -m gapmap.control2 --ledger L --sidecar S --domain NAME \
        --out DIR [--audit-cache research/n3/<d>/closure_judgements.json] [--judge ollama]
        [--judge openai --model M --reasoning-effort E --max-usd X --spend-ledger F --parallel-arm A]
"""
from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import random
import statistics
from dataclasses import dataclass
from pathlib import Path

from residual.ledger import Ledger

from gapmap import checks, config, judge as judge_mod, lenses, link, manifest, record, semantic

PRIMARY = ("seed_free", "closed")
BOOTSTRAP_B = 2000
BOOTSTRAP_SEED = 20261024
ARMS = ("own_eq", "ctrl_eq", "own_sf", "ctrl_sf")
COMPARISONS = {"equal_cap": ("own_eq", "ctrl_eq"), "seed_free": ("own_sf", "ctrl_sf")}
SPLITS = {"closed_or_partial": ("closed", "partial"), "closed": ("closed",)}

Row = tuple[str, int, str]


@dataclass(frozen=True)
class PairSpec:
    lens: str
    seeds: tuple[str, ...]
    donor_seeds: tuple[str, ...]
    donor_tied: bool
    seed_rows: tuple[Row, ...]
    own_other: tuple[Row, ...]
    donor_other: tuple[Row, ...]
    own_pool: int
    donor_pool: int
    question: str
    seed_text: str

    @property
    def k(self) -> int:
        return len(self.own_other)

    def arm(self, name: str) -> semantic.Retrieval:
        rows = {"own_eq": self.seed_rows + self.own_other, "ctrl_eq": self.seed_rows + self.donor_other,
                "own_sf": self.own_other, "ctrl_sf": self.donor_other}[name]
        return semantic.Retrieval(
            a_items=tuple((str(n), cid, sent) for n, (cid, _i, sent) in enumerate(rows, start=1)),
            s_items=())


@dataclass(frozen=True)
class Pair:
    lens: str
    seeds: tuple[str, ...]
    donor_seeds: tuple[str, ...]
    donor_tied: bool
    k: int
    own_pool: int
    donor_pool: int
    states: dict

    @property
    def discriminable(self) -> bool:
        return self.k >= 1

    @property
    def cluster(self) -> str:
        return self.seeds[0]


def donor_key(cand: lenses.Candidate, seed_ids) -> tuple:
    return tuple(sorted(seed_ids)), cand.lens


def nearest_donor(i: int, stems: list[frozenset[str]], keys: list[tuple]) -> tuple[int, bool]:
    scores = {j: link.jaccard(stems[i], stems[j]) for j in range(len(stems)) if j != i}
    best = max(scores.values())
    tied = sorted((j for j, s in scores.items() if s == best), key=lambda j: keys[j])
    return tied[0], len(tied) > 1


def _keys(rows) -> set[tuple[str, int]]:
    return {(cid, i) for cid, i, _s in rows}


def build_pairs(ledger: Ledger, index: link.Index, candidates: list, *,
                legacy_donor_seed: bool = False) -> list[PairSpec]:
    """`legacy_donor_seed=True` rebuilds I1/I1b's pairs, whose donor pool began with the donor's own
    seed sentences; only for replaying research/n3_control and research/n3_control_luna."""
    by_lens: dict[str, list] = {}
    for cand in candidates:
        by_lens.setdefault(cand.lens, []).append(cand)
    cap = config.JUDGE_A_CAP
    out = []
    for lens_name in sorted(by_lens):
        cs = by_lens[lens_name]
        if len(cs) < 2:
            continue
        probes = [semantic.primary_probe(ledger, c) for c in cs]
        keys = [donor_key(c, p[1]) for c, p in zip(cs, probes)]
        order = sorted(range(len(cs)), key=lambda n: keys[n])
        cs, probes, keys = [cs[n] for n in order], [probes[n] for n in order], [keys[n] for n in order]
        seed_rows = [semantic.seed_sentences(index, p[1]) for p in probes]
        ranked = [semantic.ranked_sentences(index, index.a_ids, p[0], _keys(s))
                  for p, s in zip(probes, seed_rows)]
        for i, (stems_i, ids_i, question, seed_text) in enumerate(probes):
            srcs_i = {checks._source_of(ledger, s) for s in ids_i}
            j, tied = nearest_donor(i, [p[0] for p in probes], keys)
            if legacy_donor_seed:
                pool, excluded = (*seed_rows[j], *ranked[j]), srcs_i
            else:
                pool = ranked[j]
                excluded = srcs_i | {checks._source_of(ledger, s) for s in probes[j][1]}
            own_all = [r for r in ranked[i] if checks._source_of(ledger, r[0]) not in excluded]
            own_top = _keys(own_all[:cap])
            donor_all = [r for r in pool
                         if checks._source_of(ledger, r[0]) not in excluded and (r[0], r[1]) not in own_top]
            k = min(cap, len(own_all), len(donor_all))
            out.append(PairSpec(lens=lens_name, seeds=keys[i][0], donor_seeds=keys[j][0], donor_tied=tied,
                                seed_rows=tuple(seed_rows[i]), own_other=tuple(own_all[:k]),
                                donor_other=tuple(donor_all[:k]), own_pool=len(own_all),
                                donor_pool=len(donor_all), question=question, seed_text=seed_text))
    return out


def pairs_sha256(specs: list[PairSpec]) -> str:
    """Hash of every arm's sentence keys: pairs with equal (lens, seeds, k) can still hold other
    sentences, e.g. I1's legacy donor pool against the fixed one."""
    keys = [[s.lens, s.seeds, s.donor_seeds, [list(r[:2]) for r in s.seed_rows],
             [list(r[:2]) for r in s.own_other], [list(r[:2]) for r in s.donor_other]] for s in specs]
    return _sha256_text(json.dumps(keys))


def parallel_arm_problem(model_id: str, sidecar: dict | None, arm: dict | None, ledger_sha256: str,
                         specs: list[PairSpec]) -> str | None:
    """ADR 0009: a live judge of the ledger's generator or verifier family runs only beside an
    other-family arm already judged on the same ledger and pairs. Returns why not, or None."""
    fam = judge_mod.family(model_id)
    if fam == "other":
        return None
    if sidecar is None:
        return f"a live {fam} judge needs --sidecar to compare its family with the ledger's"
    ledger_families = {m["family"] for m in sidecar["config"]["models"].values()}
    if fam not in ledger_families:
        return None
    if arm is None:
        return (f"{model_id} shares the ledger's {fam} family; ADR 0009 runs it only beside an "
                f"other-family arm: pass that arm's control2.json as --parallel-arm")
    if judge_mod.family(arm["judge_model"]) in ledger_families:
        return f"--parallel-arm was judged by {arm['judge_model']}, not an other-family judge"
    if arm["ledger_sha256"] != ledger_sha256:
        return "--parallel-arm was judged on a different ledger"
    if arm.get("pairs_sha256") != pairs_sha256(specs):
        return "--parallel-arm was judged on different pairs (or predates pairs_sha256: re-run it)"
    return None


def judge_pairs(specs: list[PairSpec], judge) -> list[Pair]:
    out = []
    for s in specs:
        states = ({arm: semantic.judge_retrieval(judge, s.arm(arm), s.seed_text, s.question).state
                   for arm in ARMS} if s.k >= 1 else {})
        out.append(Pair(lens=s.lens, seeds=s.seeds, donor_seeds=s.donor_seeds, donor_tied=s.donor_tied,
                        k=s.k, own_pool=s.own_pool, donor_pool=s.donor_pool, states=states))
    return out


def run(ledger: Ledger, index: link.Index, judge, candidates: list) -> list[Pair]:
    return judge_pairs(build_pairs(ledger, index, candidates), judge)


def _cluster_ci(diffs: list[tuple[str, float]], b: int, seed: int) -> list[float] | None:
    by_cluster: dict[str, list[float]] = {}
    for cluster, d in diffs:
        by_cluster.setdefault(cluster, []).append(d)
    groups = [by_cluster[c] for c in sorted(by_cluster)]
    if len(groups) < 2:
        return None
    rng = random.Random(seed)
    means = []
    for _ in range(b):
        draw = [v for _ in groups for v in rng.choice(groups)]
        means.append(sum(draw) / len(draw))
    means.sort()
    return [means[int(0.025 * b)], means[min(b - 1, int(0.975 * b))]]


def _split_row(pairs: list[Pair], own_arm: str, ctrl_arm: str, hits: tuple[str, ...],
               b: int, seed: int) -> dict:
    n = len(pairs)
    if not n:
        return {"n": 0, "clusters": 0, "own_rate": None, "control_rate": None, "diff": None, "ci95": None}
    own = [p.states[own_arm] in hits for p in pairs]
    ctrl = [p.states[ctrl_arm] in hits for p in pairs]
    diffs = [(p.cluster, float(o) - float(c)) for p, o, c in zip(pairs, own, ctrl)]
    return {"n": n, "clusters": len({p.cluster for p in pairs}), "own_rate": sum(own) / n,
            "control_rate": sum(ctrl) / n, "diff": sum(d for _c, d in diffs) / n,
            "ci95": _cluster_ci(diffs, b, seed)}


def _group(pairs: list[Pair], b: int, seed: int) -> dict:
    disc = [p for p in pairs if p.discriminable]
    n = len(pairs)
    row = {"n_pairs": n, "n_discriminable": len(disc),
           "share_discriminable": len(disc) / n if n else None,
           "best_reachable_diff": len(disc) / n if n else None,
           "donor_tied": sum(p.donor_tied for p in pairs),
           "own_pool_empty": sum(p.own_pool == 0 for p in pairs),
           "donor_pool_empty": sum(p.donor_pool == 0 for p in pairs),
           "undecided": {arm: sum(p.states.get(arm) == "undecided" for p in disc) for arm in ARMS}}
    for comparison, (own_arm, ctrl_arm) in COMPARISONS.items():
        row[comparison] = {split: _split_row(disc, own_arm, ctrl_arm, hits, b, seed)
                           for split, hits in SPLITS.items()}
    return row


def summarise(pairs: list[Pair], *, b: int = BOOTSTRAP_B, seed: int = BOOTSTRAP_SEED) -> dict:
    lens_names = sorted({p.lens for p in pairs})
    return {"by_lens": {ln: _group([p for p in pairs if p.lens == ln], b, seed) for ln in lens_names},
            "total": _group(pairs, b, seed)}


def verdict(primary_row: dict, *, planted_fires: bool, stand_in_fires: bool,
            length_row: dict | None = None) -> str:
    """`length_row` is `length_stand_in`'s result on the same pairs: a length-only judge whose CI
    lower bound is above 0 passes the control, so the control is design-wrong there."""
    if not planted_fires or stand_in_fires:
        return "design-wrong"
    length_ci = (length_row or {}).get("ci95")
    if length_ci is not None and length_ci[0] > 0:
        return "design-wrong"
    ci = primary_row.get("ci95")
    return "discriminates" if ci is not None and ci[0] > 0 else "uninformative"


def length_stand_in(specs: list[PairSpec], *, b: int = BOOTSTRAP_B, seed: int = BOOTSTRAP_SEED) -> dict:
    """L7.3 trivial stand-in on the observed pairs: a 'judge' that closes an arm iff its non-seed
    character total reaches the median over every arm. The control must not pass it."""
    disc = [s for s in specs if s.k >= 1]
    if not disc:
        return {"n": 0}
    chars = {(n, arm): sum(len(r[2]) for r in rows) for n, s in enumerate(disc)
             for arm, rows in (("own", s.own_other), ("ctrl", s.donor_other))}
    cut = statistics.median(chars.values())
    pairs = [Pair(lens=s.lens, seeds=s.seeds, donor_seeds=s.donor_seeds, donor_tied=s.donor_tied, k=s.k,
                  own_pool=s.own_pool, donor_pool=s.donor_pool,
                  states={"own_sf": "closed" if chars[(n, "own")] >= cut else "open",
                          "ctrl_sf": "closed" if chars[(n, "ctrl")] >= cut else "open"})
             for n, s in enumerate(disc)]
    return {"median_chars": cut, **_split_row(pairs, "own_sf", "ctrl_sf", ("closed",), b, seed)}


def length_matched(specs: list[PairSpec], pairs: list[Pair], *, tol: float = 0.25,
                   b: int = BOOTSTRAP_B, seed: int = BOOTSTRAP_SEED) -> dict:
    """Post hoc, added after the length stand-in passed on GDPR v1: the summary restricted to pairs
    whose two non-seed character totals differ by at most `tol` of the longer one."""
    keep = []
    for s, p in zip(specs, pairs):
        lo, lc = sum(len(r[2]) for r in s.own_other), sum(len(r[2]) for r in s.donor_other)
        if p.discriminable and abs(lo - lc) <= tol * max(lo, lc):
            keep.append(p)
    return {"tol": tol, **_group(keep, b, seed)}


def audit_current(ledger: Ledger, ledger_sha: str, index: link.Index, judge, candidates: list) -> dict:
    """Step 2: the current `checks.mismatched_evidence_control` measured pair by pair."""
    cap = config.JUDGE_A_CAP
    by_lens: dict[str, list] = {}
    for cand in candidates:
        by_lens.setdefault(cand.lens, []).append(cand)

    def gap_id(c) -> str:
        return record.make_gap_id(config.CONFIG_SHA256, ledger_sha, c.lens, c.seeds)

    counts = dict.fromkeys(("n_pairs", "identical_arms", "closure_on_seed_only", "own_closed_or_partial",
                            "control_truncated", "own_truncated", "seed_fills_cap", "donor_tied",
                            "own_other_empty", "donor_other_empty"), 0)
    for lens_name in sorted(by_lens):
        cs = sorted(by_lens[lens_name], key=gap_id)
        if len(cs) < 2:
            continue
        gap_ids = [gap_id(c) for c in cs]
        probes = [semantic.primary_probe(ledger, c) for c in cs]
        stems = [p[0] for p in probes]
        retrievals = [semantic.retrieve(index, ids, st) for st, ids, _q, _t in probes]
        for i, (_st, ids_i, question, seed_text) in enumerate(probes):
            ret_i = retrievals[i]
            srcs_i = {checks._source_of(ledger, s) for s in ids_i}
            seed_items = [x for x in ret_i.a_items if x[1] in ids_i]
            other_i = [x for x in ret_i.a_items if checks._source_of(ledger, x[1]) not in srcs_i]
            j = checks._nearest_other(i, stems, gap_ids)
            best = link.jaccard(stems[i], stems[j])
            other_j = [x for x in retrievals[j].a_items if checks._source_of(ledger, x[1]) not in srcs_i]
            own_ret = semantic.build_retrieval(checks._rows(seed_items) + checks._rows(other_i))
            ctrl_ret = semantic.build_retrieval(checks._rows(seed_items) + checks._rows(other_j))
            own_out = semantic.judge_retrieval(judge, own_ret, seed_text, question)
            closed = own_out.state in SPLITS["closed_or_partial"]
            counts["n_pairs"] += 1
            counts["identical_arms"] += [s for _n, _c, s in own_ret.a_items] == [s for _n, _c, s in ctrl_ret.a_items]
            counts["own_closed_or_partial"] += closed
            counts["closure_on_seed_only"] += closed and set(own_out.a_hits + own_out.partial_hits) <= set(ids_i)
            counts["control_truncated"] += len(seed_items) + len(other_j) > cap
            counts["own_truncated"] += len(seed_items) + len(other_i) > cap
            counts["seed_fills_cap"] += len(semantic.seed_sentences(index, ids_i)) >= cap
            counts["donor_tied"] += sum(1 for n in range(len(cs)) if n != i and
                                        link.jaccard(stems[i], stems[n]) == best) > 1
            counts["own_other_empty"] += not other_i
            counts["donor_other_empty"] += not other_j
    return counts


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def main(argv: list[str] | None = None) -> None:
    from gapmap.__main__ import _admissibility_note

    p = argparse.ArgumentParser(prog="gapmap.control2")
    p.add_argument("--ledger", required=True)
    p.add_argument("--sidecar")
    p.add_argument("--domain", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--audit-cache", help="read-only judge cache for the step-2 audit of the old control")
    p.add_argument("--judge", choices=["ollama", "openai"], default=None, help="live: fill the cache")
    p.add_argument("--model", default=config.JUDGE_MODEL,
                   help=f"judge model; one of {sorted(judge_mod.OPENAI_PRICES_PER_MTOK)} selects OpenAI")
    p.add_argument("--max-usd", type=float, help="hard spend cap, required with --judge openai")
    p.add_argument("--reasoning-effort", default="medium", help="OpenAI judge only; recorded in the cache _meta")
    p.add_argument("--max-completion-tokens", type=int, default=6000, help="OpenAI judge only")
    p.add_argument("--spend-ledger", help="OpenAI judge only: JSONL shared by runs, so --max-usd covers them all")
    p.add_argument("--parallel-arm", help="the other-family arm's control2.json on the same ledger; "
                   "required to run a judge of the ledger's own family live (ADR 0009)")
    p.add_argument("--legacy-donor-seed", action="store_true",
                   help="rebuild I1/I1b's pairs (donor pool begins with the donor's seed) to replay their caches")
    p.add_argument("--require-manifest", metavar="SHA",
                   help="refuse to run unless the repository hashes to this freeze manifest and --model "
                        "with --reasoning-effort is one of its closure arms (gapmap.manifest)")
    args = p.parse_args(argv)
    use_openai = args.judge == "openai" or args.model in judge_mod.OPENAI_PRICES_PER_MTOK
    if args.require_manifest:
        try:
            manifest.check(args.require_manifest, model=args.model,
                           reasoning_effort=args.reasoning_effort if use_openai else None)
        except manifest.Refused as exc:
            p.error(f"--require-manifest: {exc}")
    if args.judge == "openai" and args.max_usd is None:
        p.error("--judge openai needs --max-usd")

    ledger_text = Path(args.ledger).read_text()
    ledger = Ledger.from_json(ledger_text)
    sidecar = json.loads(Path(args.sidecar).read_text()) if args.sidecar else None
    index = link.build_index(ledger)
    candidates = lenses.run_all(ledger, index, link.SETTING_1)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    if use_openai:
        backend = judge_mod.OpenAIJudge(args.model, max_usd=args.max_usd if args.judge == "openai" else 0.0,
                                        reasoning_effort=args.reasoning_effort,
                                        max_completion_tokens=args.max_completion_tokens,
                                        spend_ledger=args.spend_ledger if args.judge == "openai" else None)
        meta = {"model": args.model, **backend.settings}
    else:
        backend, meta = judge_mod.OllamaJudge(model=args.model), None
    result: dict = {"domain": args.domain, "ledger_sha256": _sha256_text(ledger_text),
                    "judge_model": backend.model_id, "primary": list(PRIMARY),
                    "bootstrap": {"b": BOOTSTRAP_B, "seed": BOOTSTRAP_SEED, "cluster": "min seed claim id"}}
    note = _admissibility_note(ledger, sidecar)
    result["admissible"], result["admissibility_note"] = note is None, note
    if args.require_manifest:
        result["manifest_sha256"] = args.require_manifest
    if args.audit_cache:
        old = judge_mod.CachedJudge(judge_mod.OllamaJudge(), args.audit_cache, live=False)
        result["audit_current"] = audit_current(ledger, result["ledger_sha256"], index, old, candidates)

    specs = build_pairs(ledger, index, candidates, legacy_donor_seed=args.legacy_donor_seed)
    result["pairs_sha256"] = pairs_sha256(specs)
    if args.judge is not None:
        arm = json.loads(Path(args.parallel_arm).read_text()) if args.parallel_arm else None
        problem = parallel_arm_problem(backend.model_id, sidecar, arm, result["ledger_sha256"], specs)
        if problem:
            p.error(problem)
    if args.legacy_donor_seed:
        result["donor_pool"] = "legacy: begins with the donor's seed sentences (I1, I1b)"
    judge = judge_mod.CachedJudge(backend, out / "closure_judgements.json", live=args.judge is not None,
                                  meta=meta, live_flag="--judge openai" if use_openai else "--judge ollama")
    if meta is not None:
        result["judge_settings"] = meta
    try:
        pairs = judge_pairs(specs, judge)
    except judge_mod.BudgetExceeded as exc:
        result.update(complete=False, stopped=str(exc), spend=backend.spend())
        (out / "control2.json").write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")
        raise SystemExit(f"incomplete: {exc}") from exc
    finally:
        judge.save()
        if use_openai and backend.calls:
            with (out / "judge_calls.jsonl").open("a") as f:
                f.writelines(json.dumps(c, sort_keys=True) + "\n" for c in backend.calls)
    result["complete"] = True
    if use_openai:
        result["spend"] = backend.spend()
    result["summary"] = summarise(pairs)
    result["length_stand_in"] = length_stand_in(specs)
    result["length_matched"] = length_matched(specs, pairs)
    result["pairs"] = [dataclasses.asdict(pr) for pr in pairs]
    (out / "control2.json").write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")


if __name__ == "__main__":
    main()
