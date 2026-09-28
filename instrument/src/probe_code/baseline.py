import json
import math
import statistics
from pathlib import Path

from probe_code.guard_audit import ai_rejection_counts

RATES = ("fallback", "guard_rejection", "contract_rejection", "refusal")
PROPOSED_THRESHOLDS = {"fallback": 0.05, "guard_rejection": 0.10, "contract_rejection": 0.05, "refusal": 0.05,
                       "latency_median_s": 6.0, "min_turns": 30, "margin": 0.05, "reruns": 3}


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float] | None:
    if n == 0:
        return None
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def _rate(k: int, n: int) -> dict:
    return {"k": k, "n": n, "rate": k / n if n else None, "ci95": wilson(k, n)}


def _latency(gaps: list[float]) -> dict:
    return {"gaps": gaps, "n": len(gaps), "median": statistics.median(gaps) if gaps else None,
            "max": max(gaps) if gaps else None}


def _derive(counts: dict, gaps: list[float], ai_sets: dict) -> dict:
    c = counts
    return {"ai_sets": ai_sets, "counts": c, "latency_s": _latency(gaps), "rates": {
        "fallback": _rate(c["fallback"], c["delivered"]),
        "contract_rejection": _rate(c["rejected_contract"], c["generated"]),
        "guard_rejection": _rate(c["rejected_leading"], c["guard_checked"]),
        "refusal": _rate(c["interviewer_refused"], c["delivered"])}}


def thresholds_from_baseline(pooled: dict) -> dict:
    return {name: round(pooled["rates"][name]["ci95"][1] * 20) / 20 for name in RATES}


def session_metrics(session_dir: Path) -> dict:
    session_dir = Path(session_dir)
    manifest = json.loads((session_dir / "manifest.json").read_text())
    events = [json.loads(line) for line in (session_dir / "events.jsonl").read_text().splitlines() if line.strip()]
    ai = {e["set_id"] for e in events if e["type"] == "probe_started" and e["arm"] == "ai"}
    c = ai_rejection_counts(session_dir)
    c["ended_by_interviewer"] = sum(e["type"] == "session_ended_by_interviewer" for e in events)
    c["discarded_at_cap"] = sum(e["type"] == "cap_reached" and e.get("source") == "ai" for e in events)
    c["delivered"] = c["accepted"] + c["fallback"]
    c["generated"] = (c["accepted"] + c["discarded_at_cap"] + c["rejected_leading"] + c["rejected_contract"]
                      + c["ended_by_interviewer"])
    c["guard_checked"] = c["accepted"] + c["discarded_at_cap"] + c["rejected_leading"]
    gaps, pending = [], {}
    for e in events:
        if e["type"] == "expert_answer":
            pending[e["set_id"]] = e["t_mono"]
        elif e["type"] == "probe" and e["set_id"] in pending:
            gaps.append(round(e["t_mono"] - pending.pop(e["set_id"]), 3))
    finished = sum(e["type"] == "probe_finished" and e["set_id"] in ai for e in events)
    return {"session_id": session_dir.name, "config": manifest.get("config"),
            "simulated": bool(manifest.get("simulated")),
            **_derive(c, gaps, {"started": len(ai), "finished": finished})}


def pooled_metrics(sessions: list[dict]) -> dict:
    """Pilot and simulated sessions of one configuration; mixing configurations is refused."""
    configs = {json.dumps(s["config"], sort_keys=True) for s in sessions}
    if len(configs) > 1:
        raise ValueError(f"sessions from {len(configs)} configurations cannot be pooled")
    counts = {k: sum(s["counts"][k] for s in sessions) for k in sessions[0]["counts"]}
    gaps = [g for s in sessions for g in s["latency_s"]["gaps"]]
    ai_sets = {k: sum(s["ai_sets"][k] for s in sessions) for k in ("started", "finished")}
    return {"simulated_sessions": sum(s["simulated"] for s in sessions), **_derive(counts, gaps, ai_sets)}


def freeze_decision(pooled: dict, t: dict = PROPOSED_THRESHOLDS) -> dict:
    """Decision 0004's freeze rule over pooled metrics: accept, rerun, change one variable, or change the model.
    A rate near its threshold asks for simulated reruns until the pool holds t["reruns"] simulated sessions."""
    if pooled["counts"]["delivered"] < t["min_turns"]:
        return {"outcome": "rerun", "why": [f"fewer than {t['min_turns']} AI turns delivered"]}
    empty = [n for n in RATES if pooled["rates"][n]["rate"] is None]
    if empty:
        return {"outcome": "rerun", "why": [f"no denominator for {n}" for n in empty]}
    rates = {n: pooled["rates"][n]["rate"] for n in RATES}
    over = [n for n, r in rates.items() if r > t[n]]
    median = pooled["latency_s"]["median"]
    if median is not None and median > t["latency_median_s"]:
        over.append("latency_median_s")
    if "refusal" in over:
        return {"outcome": "change the model", "why": over}
    if over:
        return {"outcome": "change one variable", "why": over}
    near = [n for n, r in rates.items() if r > t[n] - t["margin"]]
    if near and pooled["simulated_sessions"] < t["reruns"]:
        return {"outcome": "rerun", "why": [f"{n} within {t['margin']:.0%} of its threshold" for n in near]}
    return {"outcome": "accept", "why": []}
