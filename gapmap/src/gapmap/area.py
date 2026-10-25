"""Area-level view of the gap map (I6): every merged candidate before the display caps, an area
score over them, and the check that the score is not just source count or size in disguise.

The area score is an uncalibrated ranking score, not a probability that knowledge is missing:
no gold exists to calibrate it against.

    uv run python -m gapmap.area run --ledger L.json --sidecar SC.json [--sibling S.json] \\
        --cache research/n3/<d>/closure_judgements.json --domain D --out DIR [--areas A.json]
    uv run python -m gapmap.area summary --out DIR DOMAIN_DIR...

Replay only: the judge cache is read, never written, and no network is opened.
"""
from __future__ import annotations

import argparse
import json
import math
import random
from collections.abc import Collection, Mapping, Sequence
from datetime import date
from pathlib import Path

from residual.features import Partition, area_features, planner_partition
from residual.ledger import Ledger

from gapmap import __main__ as cli
from gapmap import checks, judge as judge_mod, link, rank, record

SCORE_MIN, SCORE_MAX = -2, 4
"""The range of `record.confidence_rubric`'s A + B - P - Q."""

ASSOCIATION_THRESHOLD = 0.8
"""Pre-stated before any association was computed (research/area_score/RESULT.md §1): the score
is 'close to a monotone function' of a covariate when |Spearman rho| >= this within HYP
candidates."""
RANDOM_TRIP_MAX = 0.05
N_DRAWS = 2000
RANDOM_SEED = 0
CONFOUND_THRESHOLD = 0.8

CANDIDATE_COVARIATES = ("k_topic", "dens", "area_n_claims", "area_evidence_density")
AREA_COVARIATES = ("n_claims", "evidence_density", "n_independent_sources")

# I12 additions are deliberately separate from the replayable I6 path above/below.
PREDICTOR_COVARIATES = (*CANDIDATE_COVARIATES, "k_step")
LENS_SIGNAL_MIN = 0.5
TEXT_LENGTH_MAX = 0.3


def lens_signal_reference(lens: str, lexical_state: str) -> float:
    """I12 reference, NOT a fitted predictor: (lens term + lexical term) / 2.

    The cue/decision lenses receive 1, WHY/RESULT 0. Lexical open and
    synthetic-closed receive 1, partial 1/2, closed 0. Only these two inputs
    are allowed; semantic closure, source counts and rubric scores are absent.
    See research/area_score/PREDICTOR.md for the pre-stated interpretation.
    """
    lens_terms = {"DISC": 1, "DIAG": 1, "SEL": 1, "HEDGE": 1, "GUARD": 1,
                  "WHY": 0, "RESULT": 0}
    lexical_terms = {"open": 1.0, "synthetic-closed": 1.0, "partial": 0.5, "closed": 0.0}
    if lens not in lens_terms or lexical_state not in lexical_terms:
        raise ValueError("a known lens and lexical state are required")
    return (lens_terms[lens] + lexical_terms[lexical_state]) / 2


def candidate_records(ledger: Ledger, ledger_sha: str, judge, *, sidecar: dict | None = None,
                      sibling: Ledger | None = None) -> list[record.Record]:
    """The records `cli.build_gapmap` ranks, before merging and caps."""
    index = link.build_index(ledger)
    records = [*cli._primary_records(ledger, index, ledger_sha, judge),
               *record.unk_gaps(ledger, index, sidecar, ledger_sha)]
    if sibling is not None:
        sib_stats = checks.candidate_stats(sibling, link.build_index(sibling), judge)
        records = [checks.apply_sibling(r, sib_stats) for r in records]
    return records


def claim_area(partition: Partition) -> dict[str, str]:
    return {cid: aid for aid, cids in partition.items() for cid in cids}


def seed_area(rec: record.Record, claim_to_area: Mapping[str, str]) -> str | None:
    seeds = sorted(i.claim_id for i in rec.observed_evidence if i.role in ("seed", "rival"))
    return next((claim_to_area[c] for c in seeds if c in claim_to_area), None)


def weight(score: int) -> float:
    """Strictly monotone in the rubric score and positive for every HYP, so each candidate adds
    to its area's noisy-OR."""
    s = min(max(score, SCORE_MIN), SCORE_MAX)
    return (s - SCORE_MIN + 1) / (SCORE_MAX - SCORE_MIN + 1)


def uncapped(records: list[record.Record], ledger: Ledger, ledger_sha: str,
             claim_to_area: Mapping[str, str]) -> list[dict]:
    """Every merged HYP candidate in map order, with `shown` marking the ones `gapmap.md`
    displays after its caps."""
    ranked, _ = rank.build(records, ledger, ledger_sha)
    shown = {r.gap_id for r in ranked if r.category == "HYP"}
    hyp = sorted((r for r in rank.merge(records) if r.category == "HYP"), key=rank.order_key)
    return [{"order": i + 1, "gap_id": r.gap_id, "lens": r.lens, "anchor": r.anchor,
             "area_id": seed_area(r, claim_to_area), "score": r.confidence.score,
             "weight": weight(r.confidence.score), "k_topic": r.confidence.k_topic,
             "k_step": r.confidence.k_step, "dens": checks.dens(r),
             "robustness": r.confidence.robustness, "merged_from": list(r.merged_from),
             "shown": r.gap_id in shown}
            for i, r in enumerate(hyp)]


def noisy_or(weights: Collection[float]) -> float:
    return 1 - math.prod(1 - w for w in weights)


def area_scores(rows: list[dict], partition: Partition,
                names: Mapping[str, str] | None = None) -> list[dict]:
    out = []
    for aid in sorted(partition):
        mine = [r for r in rows if r["area_id"] == aid]
        ws = [r["weight"] for r in mine]
        out.append({"area_id": aid, "name": (names or {}).get(aid, aid), "n_candidates": len(mine),
                    "score_noisy_or": noisy_or(ws), "score_max": max(ws, default=0.0),
                    "gap_ids": [r["gap_id"] for r in mine]})
    return out


def _ranks(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = (i + j) / 2 + 1
        i = j + 1
    return ranks


def spearman(xs: Sequence[float], ys: Sequence[float]) -> float | None:
    """None when either side is constant: an undefined correlation is not a pass."""
    if len(xs) < 2:
        return None
    rx, ry = _ranks(xs), _ranks(ys)
    mx, my = sum(rx) / len(rx), sum(ry) / len(ry)
    vx = sum((r - mx) ** 2 for r in rx)
    vy = sum((r - my) ** 2 for r in ry)
    if vx == 0 or vy == 0:
        return None
    return sum((a - mx) * (b - my) for a, b in zip(rx, ry)) / math.sqrt(vx * vy)


def _trips(rho: float | None) -> bool:
    return rho is not None and abs(rho) >= ASSOCIATION_THRESHOLD


def _validate_predictor_vectors(*vectors: Sequence[float]) -> None:
    if len({len(v) for v in vectors}) != 1:
        raise ValueError("rule inputs must have equal lengths; no rows may be silently dropped")
    if any(not isinstance(x, (int, float)) or not math.isfinite(x)
           for v in vectors for x in v):
        raise ValueError("rule inputs must be finite numbers; missing rows cannot count as a pass")


def lens_signal_check(*, scores: Sequence[float], reference: Sequence[float],
                      k_topic: Sequence[float], text_lengths: Sequence[float]) -> dict:
    """I12(b): correlate centered within-stratum midranks, without ranking again.

    Eligibility depends only on the fixed reference and strata, never on scores.
    The length check uses the full population, including within-test exclusions.
    """
    _validate_predictor_vectors(scores, reference, k_topic, text_lengths)
    groups: dict[float, list[int]] = {}
    for i, k in enumerate(k_topic):
        groups.setdefault(k, []).append(i)
    xs, ys = [], []
    n_strata = 0
    for indices in groups.values():
        if len(indices) < 2 or len({reference[i] for i in indices}) < 2:
            continue
        n_strata += 1
        center = (len(indices) + 1) / 2
        xs.extend(r - center for r in _ranks([scores[i] for i in indices]))
        ys.extend(r - center for r in _ranks([reference[i] for i in indices]))
    denominator = math.sqrt(sum(x * x for x in xs) * sum(y * y for y in ys))
    within = sum(x * y for x, y in zip(xs, ys)) / denominator if denominator else None
    length = spearman(scores, text_lengths)
    return {"within_rho": within, "length_rho": length, "n_within": len(xs),
            "n_strata": n_strata, "n_length": len(scores),
            "passes": within is not None and within >= LENS_SIGNAL_MIN
            and length is not None and abs(length) < TEXT_LENGTH_MAX}


def predictor_stand_ins(*, reference: Sequence[float], k_topic: Sequence[float],
                       text_lengths: Sequence[float]) -> dict:
    """I12(c): 2,000 draws per family, separate seed-0 streams, fixed inputs.

    Length draws are random signed affine transforms of length, so they test
    both directions but intentionally have only two rank orderings. Their
    rejection rate is a deterministic diagnostic, not independent evidence.
    """
    _validate_predictor_vectors(reference, k_topic, text_lengths)
    uniform_rng, length_rng = random.Random(RANDOM_SEED), random.Random(RANDOM_SEED)
    inputs = dict(reference=reference, k_topic=k_topic, text_lengths=text_lengths)
    uniform_failures = length_failures = 0
    for _ in range(N_DRAWS):
        uniform = [uniform_rng.random() for _ in reference]
        slope = (1 if length_rng.random() < 0.5 else -1) * (1 + length_rng.random())
        offset = length_rng.random()
        length = [slope * value + offset for value in text_lengths]
        uniform_failures += not lens_signal_check(scores=uniform, **inputs)["passes"]
        length_failures += not lens_signal_check(scores=length, **inputs)["passes"]
    # Undefined reference/length checks do not make a vacuous all-fail result a pass.
    groups: dict[float, set[float]] = {}
    for k, value in zip(k_topic, reference):
        groups.setdefault(k, set()).add(value)
    testable = any(len(values) > 1 for values in groups.values()) and len(set(text_lengths)) > 1
    return {"draws": N_DRAWS, "seed": RANDOM_SEED, "uniform_failures": uniform_failures,
            "length_failures": length_failures, "testable": testable,
            "passes": testable and uniform_failures >= (1 - RANDOM_TRIP_MAX) * N_DRAWS
            and length_failures >= (1 - RANDOM_TRIP_MAX) * N_DRAWS}


def association(*, scores: Sequence[float | None], covariate: Sequence[float | None]) -> dict:
    """|rho| against the pre-stated threshold, either sign, with its L7.3 discrimination check:
    a planted score equal to the covariate must trip, and uniform noise must trip at most
    RANDOM_TRIP_MAX of the time."""
    pairs = [(s, c) for s, c in zip(scores, covariate) if s is not None and c is not None]
    xs, cs = [p[0] for p in pairs], [p[1] for p in pairs]
    rho = spearman(xs, cs)
    planted = spearman(cs, cs)
    rng = random.Random(RANDOM_SEED)
    hits = sum(_trips(spearman([rng.random() for _ in cs], cs)) for _ in range(N_DRAWS))
    rate = hits / N_DRAWS
    return {"n": len(pairs), "distinct_covariate": len(set(cs)), "rho": rho, "trips": _trips(rho),
            "planted_rho": planted, "planted_trips": _trips(planted), "random_trip_rate": rate,
            "discriminates": _trips(planted) and rate <= RANDOM_TRIP_MAX}


def candidate_associations(rows: list[dict], features: Mapping[str, Mapping]) -> dict:
    def cov(r: dict, name: str):
        if name.startswith("area_"):
            f = features.get(r["area_id"])
            return None if f is None else f[name.removeprefix("area_")]
        return r[name]
    return {name: association(scores=[r["weight"] for r in rows],
                              covariate=[cov(r, name) for r in rows])
            for name in CANDIDATE_COVARIATES}


def predictor_confound_checks(*, scores: Sequence[float],
                              covariates: Mapping[str, Sequence[float]]) -> dict:
    """I12(a), including k_step; every check must be defined and discriminate.

    This does not build a predictor or select candidates. Callers supply the
    entire merged, uncapped HYP population in a single fixed order.
    """
    if set(covariates) != set(PREDICTOR_COVARIATES):
        raise ValueError(f"exactly these covariates are required: {PREDICTOR_COVARIATES}")
    _validate_predictor_vectors(scores, *covariates.values())
    checks_ = {name: association(scores=scores, covariate=covariates[name])
               for name in PREDICTOR_COVARIATES}
    return {"checks": checks_, "passes": all(
        c["discriminates"] and c["rho"] is not None and not c["trips"] for c in checks_.values())}


def topic_rank_predictor(*, reference: Sequence[float], k_topic: Sequence[float]) -> list[float]:
    """I12 candidate 1: centered midrank / stratum size, including all HYPs.

    Singleton and reference-constant strata score zero. This removes stratum
    means by construction, not necessarily global rank association with k_topic.
    No semantic closure or confidence-rubric term is an input.
    """
    _validate_predictor_vectors(reference, k_topic)
    groups: dict[float, list[int]] = {}
    for i, k in enumerate(k_topic):
        groups.setdefault(k, []).append(i)
    result = [0.0] * len(reference)
    for indices in groups.values():
        n = len(indices)
        for i, r in zip(indices, _ranks([reference[i] for i in indices])):
            result[i] = (r - (n + 1) / 2) / n
    return result


def density_residual_predictor(*, reference: Sequence[float], k_topic: Sequence[float],
                               density: Sequence[float]) -> list[float]:
    """I12 candidate 2: candidate 1 minus its projection on within-topic density ranks.

    Fit one zero-intercept slope on this ledger's uncapped population, without
    labels or gold. Orthogonality is in these transformed values, not a promise
    of zero Spearman correlation. No clipping, reranking or fitted hyperparameter.
    """
    _validate_predictor_vectors(reference, k_topic, density)
    signal = topic_rank_predictor(reference=reference, k_topic=k_topic)
    nuisance = topic_rank_predictor(reference=density, k_topic=k_topic)
    denominator = sum(d * d for d in nuisance)
    slope = sum(s * d for s, d in zip(signal, nuisance)) / denominator if denominator else 0.0
    return [s - slope * d for s, d in zip(signal, nuisance)]


def predictor_area_means(*, scores: Sequence[float], area_ids: Sequence[str],
                         partition: Partition) -> list[dict]:
    """The phase-1 arithmetic mean rule, with explicit undefined empty areas."""
    _validate_predictor_vectors(scores)
    if len(scores) != len(area_ids) or any(a not in partition for a in area_ids):
        raise ValueError("every score must map to an area in the partition")
    groups: dict[str, list[float]] = {a: [] for a in sorted(partition)}
    for a, score in zip(area_ids, scores):
        groups[a].append(score)
    return [{"area_id": a, "n_candidates": len(values),
             "mean": sum(values) / len(values) if values else None} for a, values in groups.items()]


def evaluate_predictor(*, scores: Sequence[float], reference: Sequence[float],
                       covariates: Mapping[str, Sequence[float]], text_lengths: Sequence[float],
                       area_ids: Sequence[str], partition: Partition) -> dict:
    """Apply all three committed rules; a failed control can never be bypassed."""
    a = predictor_confound_checks(scores=scores, covariates=covariates)
    signal_inputs = dict(reference=reference, k_topic=covariates["k_topic"], text_lengths=text_lengths)
    b = lens_signal_check(scores=scores, **signal_inputs)
    c = predictor_stand_ins(**signal_inputs)
    areas = predictor_area_means(scores=scores, area_ids=area_ids, partition=partition)
    present = [row["mean"] for row in areas if row["mean"] is not None]
    return {"a": a, "b": b, "c": c, "passes": a["passes"] and b["passes"] and c["passes"],
            "areas": areas,
            "area_spread": {"n_present": len(present), "n_empty": len(areas) - len(present),
                            "min": min(present) if present else None,
                            "max": max(present) if present else None,
                            "range": max(present) - min(present) if present else None,
                            "distinct": len(set(present))},
            "area_size_association": {"status": "untestable", "rho": None,
                                      "reason": "Too few candidate-bearing areas; not a pass."}}


def replay_predictors(*, ledger_path: str | Path, sidecar_path: str | Path,
                      cache_path: str | Path, domain: str,
                      sibling_path: str | Path | None = None) -> dict:
    """I12 structural replay only: read the existing pool and fixed judge cache.

    No writes, network, gold or new ledger fields. Results remain conditional
    on qwen's ineligible HYP selection, even though scores omit judge terms.
    """
    ledger_text = Path(ledger_path).read_text()
    ledger = Ledger.from_json(ledger_text)
    sidecar = json.loads(Path(sidecar_path).read_text())
    sibling = Ledger.from_json(Path(sibling_path).read_text()) if sibling_path else None
    sha = cli._sha256_text(ledger_text)
    judge = judge_mod.CachedJudge(judge_mod.OllamaJudge(), cache_path, live=False)
    partition = planner_partition(ledger)
    claim_to_area = claim_area(partition)
    features = {f.area_id: f for f in area_features(ledger, sidecar, partition)}
    records = candidate_records(ledger, sha, judge, sidecar=sidecar, sibling=sibling)
    hyps = sorted((r for r in rank.merge(records) if r.category == "HYP"), key=lambda r: r.gap_id)
    rows = []
    for rec in hyps:
        aid = seed_area(rec, claim_to_area)
        if aid not in features:
            raise ValueError(f"unmapped HYP {rec.gap_id}; no row may be silently excluded")
        rows.append({"gap_id": rec.gap_id, "area_id": aid, "lens": rec.lens,
                     "lexical_state": rec.inferred_gap.lexical_state,
                     "reference": lens_signal_reference(rec.lens, rec.inferred_gap.lexical_state),
                     "text_length": len(rec.anchor), "k_topic": rec.confidence.k_topic,
                     "k_step": rec.confidence.k_step, "dens": checks.dens(rec),
                     "area_n_claims": features[aid].n_claims,
                     "area_evidence_density": features[aid].evidence_density})
    reference = [r["reference"] for r in rows]
    covariates = {name: [r[name] for r in rows] for name in PREDICTOR_COVARIATES}
    score_vectors = {
        "topic_rank": topic_rank_predictor(reference=reference, k_topic=covariates["k_topic"]),
        "density_residual": density_residual_predictor(
            reference=reference, k_topic=covariates["k_topic"], density=covariates["dens"]),
    }
    for i, row in enumerate(rows):
        row["scores"] = {name: values[i] for name, values in score_vectors.items()}
    inputs = dict(reference=reference, covariates=covariates,
                  text_lengths=[r["text_length"] for r in rows],
                  area_ids=[r["area_id"] for r in rows], partition=partition)
    paths = {"ledger": ledger_path, "sidecar": sidecar_path, "closure_cache": cache_path}
    if sibling_path:
        paths["sibling_ledger"] = sibling_path
    note = cli._admissibility_note(ledger, sidecar)
    return {"domain": domain, "rules_commit": "14cbdab", "grain": "planner",
            "input_sha256": {name: cli._sha256_text(Path(path).read_text()) for name, path in paths.items()},
            "admissible": note is None, "admissibility_note": note,
            "decision_role": "structural_screen" if domain == "plc" else "descriptive_only",
            "conditional_pool": "HYP selection uses ineligible qwen 7b closure judgements.",
            "rows": rows, "area_names": {a.area_id: a.name for a in ledger.areas},
            "predictors": {name: evaluate_predictor(scores=scores, **inputs)
                           for name, scores in score_vectors.items()},
            "reference_comparator": evaluate_predictor(scores=reference, **inputs),
            "source_count_plant": evaluate_predictor(scores=covariates["k_topic"], **inputs)}


def area_associations(scores: list[dict], features: Mapping[str, Mapping]) -> dict:
    out = {}
    for agg in ("score_noisy_or", "score_max"):
        for name in AREA_COVARIATES:
            out[f"{agg}~{name}"] = association(scores=[s[agg] for s in scores],
                                               covariate=[features[s["area_id"]][name] for s in scores])
    return out


def decide(by_ledger: Mapping[str, Mapping[str, dict]], *, admissible: Collection[str]) -> dict:
    """Trips when, on any N3-admissible ledger, a covariate whose check discriminates reaches
    the threshold."""
    by = [(lg, name, chk["rho"]) for lg, checks_ in sorted(by_ledger.items()) if lg in admissible
          for name, chk in sorted(checks_.items()) if chk["discriminates"] and chk["trips"]]
    return {"tripped": bool(by), "by": by}


def _scalar(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return int(v)
    if isinstance(v, (int, float)):
        return v
    if isinstance(v, date):
        return v.toordinal()
    if isinstance(v, str):
        return date.fromisoformat(v).toordinal()
    if isinstance(v, (list, tuple)):
        return len(v)
    if isinstance(v, Mapping):
        return v["value"]
    raise TypeError(f"no scalar for {v!r}")


def _key(v):
    return json.dumps(v, sort_keys=True, default=str)


def feature_table(by_ledger: Mapping[str, Sequence[Mapping]]) -> list[dict]:
    """Status by code. Dead: one value (or none) within every ledger. Confounded (size): pooled
    |rho| with n_claims >= CONFOUND_THRESHOLD. Live: the rest. Tuples count by length."""
    names = list(next(iter(by_ledger.values()))[0])
    pooled = [f for fs in by_ledger.values() for f in fs]
    out = []
    for name in names:
        if name == "area_id":
            continue
        raw = [f[name] for f in pooled]
        present = [v for v in raw if v is not None]
        per = {lg: {"distinct": len({_key(f[name]) for f in fs if f[name] is not None}),
                    "missing": sum(f[name] is None for f in fs)} for lg, fs in by_ledger.items()}
        vals = [_scalar(v) for v in present]
        mean = sum(vals) / len(vals) if vals else 0.0
        keys = [_key(v) for v in raw]
        pairs = [(_scalar(f[name]), f["n_claims"]) for f in pooled if f[name] is not None]
        rho = spearman([p[0] for p in pairs], [p[1] for p in pairs]) if name != "n_claims" else 1.0
        dead = all(p["distinct"] <= 1 for p in per.values())
        if dead:
            status = "dead"
        elif name == "n_claims":
            status = "live (size)"
        elif rho is not None and abs(rho) >= CONFOUND_THRESHOLD:
            status = "confounded (size)"
        else:
            status = "live"
        out.append({"feature": name, "status": status, "n_areas": len(raw),
                    "missing": len(raw) - len(present),
                    "variance": sum((v - mean) ** 2 for v in vals) / len(vals) if vals else None,
                    "distinct": len({_key(v) for v in present}),
                    "modal_share": max(keys.count(k) for k in set(keys)) / len(keys),
                    "rho_n_claims": rho, "per_ledger": per})
    return out


def load_areas(path: str | Path) -> tuple[dict[str, tuple[str, ...]], dict[str, str]]:
    """An `--areas` file: {"grain": "task_step", "areas": [{"area_id", "name", "claim_ids"}]}."""
    data = json.loads(Path(path).read_text())
    if data.get("grain") != "task_step":
        raise ValueError(f"--areas must be at task_step grain, got {data.get('grain')!r}")
    ids = [a["area_id"] for a in data["areas"]]
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate area ids in --areas")
    return ({a["area_id"]: tuple(sorted(a["claim_ids"])) for a in data["areas"]},
            {a["area_id"]: a.get("name", a["area_id"]) for a in data["areas"]})


def _write(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, sort_keys=True, indent=1, default=str) + "\n")


def run(*, ledger_path: str, sidecar_path: str | None, sibling_path: str | None, cache_path: str,
        domain: str, out_dir: str, areas_path: str | None = None, judge=None) -> None:
    text = Path(ledger_path).read_text()
    lg = Ledger.from_json(text)
    sidecar = json.loads(Path(sidecar_path).read_text()) if sidecar_path else None
    sibling = Ledger.from_json(Path(sibling_path).read_text()) if sibling_path else None
    j = judge or judge_mod.CachedJudge(judge_mod.OllamaJudge(), cache_path, live=False)
    sha = cli._sha256_text(text)
    if areas_path:
        partition, names = load_areas(areas_path)
        grain = "task_step"
    else:
        partition = planner_partition(lg)
        names = {a.area_id: a.name for a in lg.areas}
        grain = "planner"
    feats = {f.area_id: f.model_dump() for f in area_features(lg, sidecar, partition)}
    rows = uncapped(candidate_records(lg, sha, j, sidecar=sidecar, sibling=sibling), lg, sha,
                    claim_area(partition))
    scores = area_scores(rows, partition, names)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    _write(out / "candidates.json", {"domain": domain, "ledger_sha256": sha, "grain": grain,
                                     "n_merged_hyp": len(rows),
                                     "n_hidden_by_caps": sum(not r["shown"] for r in rows),
                                     "n_without_area": sum(r["area_id"] is None for r in rows),
                                     "candidates": rows})
    _write(out / "area_scores.json", {"domain": domain, "grain": grain, "score": "uncalibrated",
                                      "areas": scores})
    _write(out / "features.json", {"domain": domain, "grain": grain, "areas": list(feats.values())})
    note = cli._admissibility_note(lg, sidecar)
    _write(out / "associations.json", {
        "domain": domain, "grain": grain, "admissible": note is None, "admissibility_note": note,
        "threshold": ASSOCIATION_THRESHOLD, "random_trip_max": RANDOM_TRIP_MAX,
        "candidate_level": candidate_associations(rows, feats),
        "area_level": area_associations(scores, feats)})


def summary(*, domain_dirs: Sequence[str], out_dir: str) -> dict:
    by_feats, by_assoc, admissible = {}, {}, set()
    for d in domain_dirs:
        f = json.loads((Path(d) / "features.json").read_text())
        a = json.loads((Path(d) / "associations.json").read_text())
        by_feats[f["domain"]] = f["areas"]
        by_assoc[a["domain"]] = a["candidate_level"]
        if a["admissible"]:
            admissible.add(a["domain"])
    result = {"feature_table": feature_table(by_feats),
              "decision": decide(by_assoc, admissible=admissible),
              "admissible": sorted(admissible)}
    _write(Path(out_dir) / "summary.json", result)
    return result


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="gapmap.area")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--ledger", required=True)
    r.add_argument("--sidecar")
    r.add_argument("--sibling")
    r.add_argument("--cache", required=True, help="a committed closure_judgements.json, read only")
    r.add_argument("--domain", required=True)
    r.add_argument("--out", required=True)
    r.add_argument("--areas", help="a task_step partition JSON; default: the ledger's planner areas")
    s = sub.add_parser("summary")
    s.add_argument("--out", required=True)
    s.add_argument("domain_dirs", nargs="+")
    args = p.parse_args(argv)
    if args.cmd == "run":
        run(ledger_path=args.ledger, sidecar_path=args.sidecar, sibling_path=args.sibling,
            cache_path=args.cache, domain=args.domain, out_dir=args.out, areas_path=args.areas)
    else:
        summary(domain_dirs=args.domain_dirs, out_dir=args.out)


if __name__ == "__main__":
    main()
