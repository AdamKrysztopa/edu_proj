#!/usr/bin/env python3
"""N9 cost ledger (I11): every recorded model call in one table, reconciled against each run's
own recorded total.

    python3 scripts/cost_ledger.py --private /path/to/.private [--headroom-usd X] [--out PATH]
    python3 scripts/cost_ledger.py --no-private ...

Reads call logs and caches only. From the sealed `.private/` runs it reads `calls.jsonl` and the
plant-authoring log, the files the N2 protocol lets a decision read; it never opens a sealed
ledger, sidecar or snapshot, and it keeps no prompt hash or free text in a row. Without
--headroom-usd the key's limit fields are read once (a free GET, via key_headroom.py).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TOLERANCE_USD = 0.01
BILLED_FAILURES = {"truncated", "malformed_json", "refusal", "no_choices", "served_mismatch"}
QWEN_LEVELS = {"states", "partially", "no"}

# Run status and recorded totals, as the committed reports state them.
E_LIVE = {
    "20260928T133336Z-59ec876b3d7e": {"label": "v1 PLC", "result": "usable", "report_usd": 0.679, "n3": "plc"},
    "20260928T135354Z-eb840a85b7d1": {"label": "v1 GDPR", "result": "usable", "report_usd": 0.500, "n3": "gdpr_v1"},
    "20260928T145115Z-518f99363336": {"label": "v2 PLC", "result": "failed: UnicodeEncodeError crash",
                                      "report_usd": 0.193, "n3": None},
    "20260928T145943Z-bc1cc9a30a02": {"label": "v2 GDPR", "result": "usable (defect-compromised)",
                                      "report_usd": 1.002, "n3": "gdpr_v2"},
    "20260928T171449Z-518f99363336": {"label": "v3 PLC", "result": "failed: key limit at first call",
                                      "report_usd": None, "n3": None},
    "20260928T171508Z-bc1cc9a30a02": {"label": "v3 GDPR", "result": "failed: key limit at first call",
                                      "report_usd": None, "n3": None},
}
E_LIVE_REPORT = "research/n2/e_live_report.md"
EPE_REPORT = "research/n2/e_plant_eabst_report.md"
JEV_RESULTS = "research/spikes/jev/RESULTS.md"
EVALUATION = {
    "e_plant/baseline": {"result": "usable", "recorded": [(f"{EPE_REPORT} §1.1", 0.0735), (f"{EPE_REPORT} §3", 0.074)]},
    "e_plant/plant_authoring": {"result": "usable", "recorded": [(f"{EPE_REPORT} §3", 0.121)]},
    "e_plant/pipeline_run1": {"result": "rerun unit (amendment 1): sealed, unscored",
                              "recorded": [(f"{EPE_REPORT} §3", 1.758), (f"{EPE_REPORT} §1.2 food", 0.883, {"unit": "food"}),
                                           (f"{EPE_REPORT} §1.2 concreting", 0.875, {"unit": "concreting"})]},
    "e_abst/baseline": {"result": "usable", "recorded": [(f"{EPE_REPORT} §2.1", 0.0068), (f"{EPE_REPORT} §3", 0.007)]},
    "e_abst/exposure": {"result": "usable (pre-amendment-2 exposure.json)", "recorded": []},
    "e_abst/pipeline_run1": {"result": "rerun unit (amendment 1): sealed, unscored",
                             "recorded": [(f"{EPE_REPORT} §2.2/§3", 0.488)]},
}
V2B_PENDING = 140  # e_live_report.md §5: located claims left pending by dropped verify calls
DECOYS_PER_RUN = 30  # reconstruct/src/reconstruct/evidence.py: 10 per mutation type, 3 types
N3_DOMAINS = ("plc", "gdpr_v1", "gdpr_v2")
NON_TEMPLATE_CATEGORIES = {"HYP", "RG-SINGLE", "RG-SIBLING", "RG-UNVER"}

PLANNED = [
    ("I2 Jev on the rebuilt control (cap --max-usd 0.10)", 0.10),
    ("I4 out-of-sample domain run (planned $0.5-1; upper end)", 1.00),
    ("I10 pre-gold corpus pilot (cap --max-usd 1)", 1.00),
    ("Deferred N2: E-LIVE v3, both domains (final-review estimate, unregistered)", 2.00),
    ("Deferred N2: E-PLANT run 2 (registered cap)", 3.00),
    ("Deferred N2: E-ABST run 2 (registered cap, P3)", 14.40),
]


def classify(records: list[dict]) -> list[str]:
    """A failed attempt that the same task re-sent with the same spec later in the log is a retry;
    the last failed attempt is a failure. Logs older than outcome logging say nothing: unknown."""
    out = []
    for i, r in enumerate(records):
        if "outcome" not in r:
            out.append("unknown")
        elif r["outcome"] == "ok":
            out.append("success")
        else:
            again = any(s.get("task") == r.get("task") and s.get("spec_sha256") == r.get("spec_sha256")
                        for s in records[i + 1:])
            out.append("retry" if again else "failure")
    return out


def _row(*, run, unit, stage, kind, model, served_model, provider, input_tokens, output_tokens, usd,
         status, outcome, source):
    return {"run": run, "unit": unit, "stage": stage, "kind": kind, "model": model,
            "served_model": served_model, "provider": provider, "input_tokens": input_tokens,
            "output_tokens": output_tokens, "usd": usd, "status": status, "outcome": outcome,
            "source": source}


def rows_from_calls(records: list[dict], *, run: str, kind: str, unit: str | None = None,
                    source: str | None = None) -> list[dict]:
    return [_row(run=run, unit=unit, stage=r.get("task"), kind=kind, model=r.get("model"),
                 served_model=r.get("served_model"), provider="openrouter",
                 input_tokens=r.get("input_tokens"), output_tokens=r.get("output_tokens"),
                 usd=r.get("cost") or 0.0, status=status, outcome=r.get("outcome"), source=source)
            for r, status in zip(records, classify(records))]


def rows_from_plant_authoring(records: list[dict], *, run: str, source: str | None = None) -> list[dict]:
    """A rejected page is a retry when the same page is accepted later, else a failure."""
    rows = []
    for i, r in enumerate(records):
        if r.get("accepted"):
            status = "success"
        else:
            later = any(s.get("page_id") == r.get("page_id") and s.get("accepted") for s in records[i + 1:])
            status = "retry" if later else "failure"
        rows.append(_row(run=run, unit=None, stage="plant_authoring", kind="evaluation",
                         model=r.get("served_model"), served_model=r.get("served_model"), provider="openrouter",
                         input_tokens=r.get("input_tokens"), output_tokens=r.get("output_tokens"),
                         usd=r.get("cost") or 0.0, status=status,
                         outcome="accepted" if r.get("accepted") else "rejected", source=source))
    return rows


def _chat_text(resp: dict) -> str:
    if resp.get("choices"):
        return resp["choices"][0].get("message", {}).get("content") or ""
    return (resp.get("message") or {}).get("content") or ""


def _json_object(text: str) -> dict | None:
    m = re.search(r"\{.*\}", text, re.S)
    try:
        d = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None
    return d if isinstance(d, dict) else None


def rows_from_jev_cache(entries: list[dict], *, source: str | None = None) -> list[dict]:
    """Readability uses judge_swap.py's own parse rule, so a failure here is an answer the spike excluded."""
    rows = []
    for e in entries:
        req, resp = e["request"], e["response"]
        model = req.get("model")
        usage = resp.get("usage") or {}
        if model == "typesafe/jev-1.13":
            stage = "jev_tacit_signal" if "statement" in req.get("state", {}) else "jev_closure_substitution"
            ok = bool(resp.get("answers"))
            provider, tin, tout = "openrouter", usage.get("input_tokens"), usage.get("output_tokens")
        else:
            parsed = _json_object(_chat_text(resp))
            if model == "anthropic/claude-sonnet-5.5":
                stage, ok = "sonnet_reference", parsed is not None
            else:
                stage = "qwen_same_prompt" if "/" in model else "qwen_same_prompt_local"
                ok = parsed is not None and parsed.get("choice") in QWEN_LEVELS
            provider = "openrouter" if "/" in model else "local"
            tin = usage.get("prompt_tokens", resp.get("prompt_eval_count"))
            tout = usage.get("completion_tokens", resp.get("eval_count"))
        rows.append(_row(run="spike/jev", unit=None, stage=stage, kind="engineering", model=model,
                         served_model=resp.get("model"), provider=provider, input_tokens=tin, output_tokens=tout,
                         usd=usage.get("cost") or 0.0, status="success" if ok else "failure",
                         outcome="readable" if ok else "unreadable", source=source))
    return rows


def rows_from_closure_cache(cache: dict, *, domain: str, model: str, source: str | None = None) -> list[dict]:
    rows = []
    for ans in cache.values():
        ok = isinstance(ans, dict) and any(isinstance(ans.get(k), list) for k in ("states", "partially"))
        rows.append(_row(run=f"n3/{domain}", unit=None, stage="closure_judge", kind="engineering", model=model,
                         served_model=model, provider="local", input_tokens=None, output_tokens=None, usd=0.0,
                         status="success" if ok else "failure", outcome="readable" if ok else "unreadable",
                         source=source))
    return rows


def summarise(rows: list[dict]) -> dict:
    total = sum(r["usd"] for r in rows)
    by_status = {}
    for r in rows:
        s = by_status.setdefault(r["status"], {"calls": 0, "usd": 0.0})
        s["calls"] += 1
        s["usd"] += r["usd"]
    lost = sum(v["usd"] for k, v in by_status.items() if k in ("failure", "retry"))
    return {"calls": len(rows), "usd": total, "by_status": by_status, "lost_usd": lost,
            "lost_share": lost / total if total else None}


def reconcile(rows: list[dict], recorded: dict, *, runs: list[str]) -> list[dict]:
    out = []
    for run in runs:
        mine = [r for r in rows if r["run"] == run]
        checks = []
        for entry in recorded.get(run, []):
            src, usd, where = (*entry, {}) if len(entry) == 2 else entry
            ledger = sum(r["usd"] for r in mine if all(r.get(k) == v for k, v in where.items()))
            gap = ledger - usd
            checks.append({"source": src, "where": where, "recorded_usd": usd, "ledger_usd": ledger,
                           "gap_usd": gap, "ok": abs(gap) <= TOLERANCE_USD})
        out.append({"run": run, "ledger_usd": sum(r["usd"] for r in mine), "calls": len(mine),
                    "checks": checks, "ok": all(c["ok"] for c in checks) if checks else None})
    return out


def unit_costs(*, spend_usd: float, n_verified_claims: int, n_candidates: int, n_hyp: int) -> dict:
    return {
        "spend_usd": spend_usd,
        "per_verified_claim_usd": spend_usd / n_verified_claims if n_verified_claims else None,
        "per_gap_candidate_usd": spend_usd / n_candidates if n_candidates else None,
        "per_hyp_candidate_usd": spend_usd / n_hyp if n_hyp else None,
        "per_validated_item_usd": None,
        "per_validated_item_reason": "unavailable: no item is validated (no gold, no human coding); "
                                     "never computed from model-supported claims",
    }


def prospective(caps: list[tuple[str, float]], *, headroom_usd: float | None) -> dict:
    total = sum(c for _, c in caps)
    fits = None if headroom_usd is None else total <= headroom_usd
    return {"caps": [{"item": n, "cap_usd": c} for n, c in caps], "sum_caps_usd": total,
            "headroom_usd": headroom_usd, "fits": fits,
            "shortfall_usd": None if headroom_usd is None else max(0.0, total - headroom_usd)}


def _jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _rel(path: Path, base: Path, prefix: str) -> str:
    return f"{prefix}{path.relative_to(base)}"


def _private_rows(private: Path) -> list[dict]:
    rows = []
    src = lambda p: _rel(p, private, ".private/")  # noqa: E731
    for domain in ("food", "concreting"):
        for arm, run in (("baseline", "e_plant/baseline"), ("pipeline_run1", "e_plant/pipeline_run1")):
            p = private / "e_plant" / "runs" / domain / arm / "calls.jsonl"
            rows += rows_from_calls(_jsonl(p), run=run, kind="evaluation", unit=domain, source=src(p))
    p = private / "e_plant" / "plant_authoring_log.jsonl"
    rows += rows_from_plant_authoring(_jsonl(p), run="e_plant/plant_authoring", source=src(p))
    # E-ABST items still await blind coding: a row tied to an item (by id or log order) would tell a
    # coder which items the raw arm answered, so these rows carry no item and are sorted by cost.
    p = private / "e_abst" / "runs" / "_baseline" / "calls.jsonl"
    abst = rows_from_calls(_jsonl(p), run="e_abst/baseline", kind="evaluation", source=src(p))
    p = private / "e_abst" / "exposure_calls.jsonl"
    abst += rows_from_calls(_jsonl(p), run="e_abst/exposure", kind="evaluation", source=src(p))
    for p in sorted((private / "e_abst" / "runs").glob("E-ABST-*/pipeline_run1/calls.jsonl")):
        abst += rows_from_calls(_jsonl(p), run="e_abst/pipeline_run1", kind="evaluation",
                                source=".private/e_abst/runs/*/pipeline_run1/calls.jsonl")
    return rows + sorted(abst, key=lambda r: (r["run"], r["stage"], r["usd"], r["input_tokens"] or 0))


def unit_prices(rows: list[dict]) -> dict:
    """Per run, because v2 prompts cost about twice v1's per verify call."""
    out: dict[str, dict] = {}
    for r in rows:
        if r["usd"]:
            s = out.setdefault(r["run"], {}).setdefault(r["stage"], {"calls": 0, "usd": 0.0, "max_usd": 0.0})
            s["calls"] += 1
            s["usd"] += r["usd"]
            s["max_usd"] = max(s["max_usd"], r["usd"])
    return {run: {k: {**v, "mean_usd": v["usd"] / v["calls"]} for k, v in sorted(st.items())}
            for run, st in sorted(out.items())}


def project_v3_domain(rows: list[dict], *, base_run: str, n_supports: int, n_pending: int,
                      decoy_runs: list[str], n_decoys: int) -> dict:
    """A floor: the base run's spend plus the calls the provider defect dropped (its pending verifies),
    at most 2 cross-verify calls per supported claim (P3; cross-verify replaced the contradiction
    pass), and each decoy's generation and verification. Pending claims that turn out supported
    would add cross-verifies on top."""
    def mean(run_ids, stage):
        xs = [r["usd"] for r in rows if r["run"] in run_ids and r["stage"] == stage]
        return sum(xs) / len(xs) if xs else 0.0

    base = sum(r["usd"] for r in rows if r["run"] == base_run)
    verify = mean([base_run], "verify")
    pending = n_pending * verify
    cross = 2 * n_supports * verify
    decoys = n_decoys * (mean(decoy_runs, "decoy") + verify)
    return {"base_run": base_run, "base_usd": base, "pending_verify_usd": pending, "cross_verify_usd": cross,
            "decoy_usd": decoys, "projected_usd": base + pending + cross + decoys}


def build(repo: Path, *, private: Path | None, headroom_usd: float | None = None,
          key_snapshot: dict | None = None) -> dict:
    rows: list[dict] = []
    recorded: dict[str, list] = {}
    sidecar_stats = {}
    for run_id, meta in E_LIVE.items():
        d = repo / "reconstruct" / "runs" / run_id
        run = f"e_live/{run_id}"
        rows += rows_from_calls(_jsonl(d / "calls.jsonl"), run=run, kind="engineering",
                                source=_rel(d / "calls.jsonl", repo, ""))
        stats = json.loads((d / "sidecar.json").read_text())["stats"]
        sidecar_stats[run_id] = stats
        recorded[run] = [(f"reconstruct/runs/{run_id}/sidecar.json stats.total_cost_usd", stats["total_cost_usd"])]
        if meta["report_usd"] is not None:
            recorded[run].append((E_LIVE_REPORT, meta["report_usd"]))

    jev_dir = repo / "research" / "spikes" / "jev" / "cache"
    entries = [json.loads(p.read_text()) for p in sorted(jev_dir.glob("*.json"))]
    rows += rows_from_jev_cache(entries, source="research/spikes/jev/cache/")
    recorded["spike/jev"] = [(JEV_RESULTS, 0.45), (JEV_RESULTS, 0.37, {"stage": "sonnet_reference"})]

    n3_counts = {}
    judge_model = "qwen2.5:7b-instruct"
    for dom in N3_DOMAINS:
        p = repo / "research" / "n3" / dom / "closure_judgements.json"
        rows += rows_from_closure_cache(json.loads(p.read_text()), domain=dom, model=judge_model,
                                        source=_rel(p, repo, ""))
        recorded[f"n3/{dom}"] = [("research/n3/README.md (local Ollama)", 0.0)]
        g = json.loads((repo / "research" / "n3" / dom / "gapmap.json").read_text())
        cats = [r["category"] for r in g["map"] + g["retrieval_gaps"]]
        n3_counts[dom] = {"candidates": sum(c in NON_TEMPLATE_CATEGORIES for c in cats),
                          "hyp": cats.count("HYP"), "admissible": g["admissible"]}

    missing = []
    if private is None:
        missing.append("private")
    else:
        rows += _private_rows(private)
        for run, meta in EVALUATION.items():
            recorded[run] = list(meta["recorded"])

    runs = sorted({r["run"] for r in rows} | set(recorded))
    recon = reconcile(rows, recorded, runs=runs)

    def _filter(pred):
        return [r for r in rows if pred(r)]

    e_live_used = [f"e_live/{k}" for k, m in E_LIVE.items() if m["n3"]]
    direct_spend = sum(r["usd"] for r in rows if r["run"] in e_live_used)
    loaded_spend = sum(r["usd"] for r in rows if r["run"].startswith("e_live/"))
    n_verified = sum(sidecar_stats[k]["n_supports"] for k, m in E_LIVE.items() if m["n3"])
    n_cand = sum(v["candidates"] for v in n3_counts.values())
    n_hyp = sum(v["hyp"] for v in n3_counts.values())

    run_results = {f"e_live/{k}": m["result"] for k, m in E_LIVE.items()}
    run_results.update({k: v["result"] for k, v in EVALUATION.items()} if private is not None else {})
    run_results.update({"spike/jev": "usable", **{f"n3/{d}": "usable" for d in N3_DOMAINS}})
    lost_runs = [k for k, v in run_results.items() if v.startswith(("failed", "rerun unit"))]
    total = sum(r["usd"] for r in rows)
    run_lost = sum(r["usd"] for r in rows if r["run"] in lost_runs)
    v2b, v1 = "20260928T145943Z-bc1cc9a30a02", [f"e_live/{k}" for k, m in E_LIVE.items() if m["label"].startswith("v1")]
    projection = project_v3_domain(rows, base_run=f"e_live/{v2b}", n_supports=sidecar_stats[v2b]["n_supports"],
                                   n_pending=V2B_PENDING, decoy_runs=v1,
                                   n_decoys=DECOYS_PER_RUN)

    sources: dict[str, set] = {}
    for r in rows:
        sources.setdefault(r["run"], set()).add(r.pop("source"))

    return {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "tolerance_usd": TOLERANCE_USD,
        "sources_missing": missing,
        "totals": {
            "all": summarise(rows),
            "engineering": summarise(_filter(lambda r: r["kind"] == "engineering")),
            "evaluation": summarise(_filter(lambda r: r["kind"] == "evaluation")),
            "by_run": {run: summarise(_filter(lambda r, run=run: r["run"] == run)) for run in runs},
        },
        "run_results": run_results,
        "lost_to_failed_runs": {"runs": lost_runs, "usd": run_lost, "share": run_lost / total if total else None},
        "reconciliation": recon,
        "unit_costs": {
            **unit_costs(spend_usd=direct_spend, n_verified_claims=n_verified, n_candidates=n_cand, n_hyp=n_hyp),
            "basis": "the three E-LIVE runs whose ledgers feed N3 (N3 itself $0); verified = verifier SUPPORTS "
                     "(sidecar stats.n_supports, a model judgement); candidates = HYP, RG-SINGLE, RG-SIBLING, "
                     "RG-UNVER (RG-UNK and CONTROL are templates)",
            "loaded": unit_costs(spend_usd=loaded_spend, n_verified_claims=n_verified, n_candidates=n_cand,
                                 n_hyp=n_hyp),
            "n_verified_claims": n_verified, "n3_counts": n3_counts,
            "evaluation_runs": "unavailable: E-PLANT and E-ABST run-1 claims are sealed and unscored",
        },
        "unit_prices": unit_prices(rows),
        "projection_v3_domain": projection,
        "prospective": prospective(PLANNED, headroom_usd=headroom_usd),
        "sources": {run: sorted(s) for run, s in sorted(sources.items())},
        "key_snapshot": key_snapshot,
        "rows": rows,
    }


def dump(ledger: dict) -> str:
    """One row per line, so a diff of the ledger reads call by call."""
    head = {k: v for k, v in ledger.items() if k != "rows"}
    body = ",\n".join("  " + json.dumps(r, sort_keys=True) for r in ledger["rows"])
    text = json.dumps(head, indent=1, sort_keys=True)
    return text[:-2] + ',\n "rows": [\n' + body + "\n ]\n}\n"


def main(argv: list[str] | None = None) -> int:
    repo = Path(__file__).resolve().parents[1]
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--private", type=Path, help="the .private/ directory holding the E-PLANT and E-ABST logs")
    g.add_argument("--no-private", action="store_true")
    ap.add_argument("--headroom-usd", type=float)
    ap.add_argument("--out", type=Path, default=repo / "research" / "cost_ledger" / "ledger.json")
    args = ap.parse_args(argv)
    if args.private is not None and not args.private.is_dir():
        print(f"{args.private} is not a directory", file=sys.stderr)
        return 2
    headroom, snapshot = args.headroom_usd, None
    if headroom is None:
        sys.path.insert(0, str(repo / "scripts"))
        import key_headroom
        d = key_headroom.read_key_data()
        snapshot = {k: d.get(k) for k in ("limit", "limit_remaining", "limit_reset", "usage", "usage_monthly",
                                           "usage_weekly")}
        snapshot["read_utc"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
        headroom = d.get("limit_remaining")
    ledger = build(repo, private=args.private, headroom_usd=headroom, key_snapshot=snapshot)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(dump(ledger))
    bad = [r["run"] for r in ledger["reconciliation"] if r["ok"] is False]
    t = ledger["totals"]["all"]
    print(f"{t['calls']} calls, ${t['usd']:.4f}; reconciliation gaps over ${TOLERANCE_USD}: {bad or 'none'}; "
          f"wrote {args.out}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
