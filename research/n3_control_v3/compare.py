"""I1c step 7: the fixed control per judge and domain, its L7.3 verdict, qwen/sol agreement under
ADR 0009, Cohen's kappa between each pair of judges, and each judge's test-retest on the prompts
run 1 (`run1_asymmetric/`) and run 2 both sent. Reads only committed outputs.

I2 adds the judges it screened (`SCREENED`): each one's two L7.3 runs, and, for each one whose
domains ran, its rows beside sol, qwen and Luna, the guard-sol ADR 0009 reading and Jev against
sol, both with sol's noise-inflated direction (`sol_noise.json`).

    python3 research/n3_control_v3/compare.py [run1_asymmetric] > <that dir>/compare.json

The optional argument, a subdirectory, gives run 1's tables.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN1 = HERE / "run1_asymmetric"
BASE = HERE / sys.argv[1] if len(sys.argv) > 1 else HERE
JUDGES = ("qwen", "luna", "sol")
# I2: the Jev substitute with its L7.3 retest directory. No ADR 0009 guard arm is chosen
# (coder32 was dropped on 2026-10-24); a future guard adds its entry here and sets GUARD.
SCREENED = {"jev": ("jev/l73", "jev/l73_retest")}
GUARD: str | None = None
WEAK_GUARD_KAPPA = 0.4
CLOSE_TO_SOL = {"max_abs_delta_primary": 0.05, "min_kappa": 0.6}
DOMAINS = ("plc", "gdpr_v1", "gdpr_v2")
ADMISSIBLE = ("plc", "gdpr_v1")
STATES = ("closed", "partial", "open")
ARMS = ("own_eq", "ctrl_eq", "own_sf", "ctrl_sf")


def load(judge: str, domain: str) -> dict:
    return json.loads((BASE / judge / domain / "control2.json").read_text())


def l73(judge: str) -> dict:
    return json.loads((BASE / judge / "l73" / "l73.json").read_text())


def verdict(primary: dict, length: dict, eligible: dict) -> str:
    if not (eligible["planted_fires"] and not eligible["stand_in_fires"]):
        return "design-wrong (judge fails L7.3)"
    if length.get("ci95") and length["ci95"][0] > 0:
        return "design-wrong (length-only judge passes)"
    ci = primary.get("ci95")
    return "discriminates" if ci and ci[0] > 0 else "uninformative"


def kappa(a: list[str], b: list[str]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[s] * cb[s] for s in set(ca) | set(cb)) / n ** 2
    return None if pe == 1 else (po - pe) / (1 - pe)


def labels(judge: str, domain: str) -> dict[tuple, str]:
    out = {}
    for p in load(judge, domain)["pairs"]:
        for arm, state in p["states"].items():
            out[(tuple(p["seeds"]), p["lens"], arm)] = state
    return out


def agreement(j1: str, j2: str, domains) -> dict:
    a, b = [], []
    for d in domains:
        l1, l2 = labels(j1, d), labels(j2, d)
        for key in sorted(set(l1) & set(l2)):
            if l1[key] in STATES and l2[key] in STATES:
                a.append(l1[key])
                b.append(l2[key])
    return {"n": len(a), "raw": sum(x == y for x, y in zip(a, b)) / len(a) if a else None, "kappa": kappa(a, b)}


def reply_state(reply) -> str:
    """The state a cached reply asks for, before the parser validates sentence numbers."""
    if not isinstance(reply, dict):
        return "undecided"
    if reply.get("states"):
        return "closed"
    return "partial" if reply.get("partially") else "open"


def retest(judge: str, part: str) -> dict:
    a = json.loads((RUN1 / judge / part / "closure_judgements.json").read_text())
    b = json.loads((HERE / judge / part / "closure_judgements.json").read_text())
    keys = sorted((set(a) & set(b)) - {"_meta"})
    sa, sb = [reply_state(a[k]) for k in keys], [reply_state(b[k]) for k in keys]
    return {"n": len(keys), "state_agreement": sum(x == y for x, y in zip(sa, sb)) / len(keys) if keys else None,
            "kappa": kappa(sa, sb)}


def direction(row: dict) -> str:
    ci = row.get("ci95")
    if ci and ci[0] > 0:
        return "+"
    if ci and ci[1] < 0:
        return "-"
    return "0"


def target_states(result: dict) -> dict:
    return {t: {name: row["target_states"] for name, row in rows.items()} for t, rows in result["topics"].items()}


def screen(judge: str) -> dict:
    """I2's eligibility: the pre-stated L7.3 rule passes in both runs with identical states."""
    runs = [json.loads((HERE / d / "l73.json").read_text()) for d in SCREENED[judge]]
    caches = [json.loads((HERE / d / "closure_judgements.json").read_text()) for d in SCREENED[judge]]
    keys = sorted((set(caches[0]) & set(caches[1])) - {"_meta"})
    sa, sb = [reply_state(caches[0][k]) for k in keys], [reply_state(caches[1][k]) for k in keys]
    identical = target_states(runs[0]) == target_states(runs[1])
    return {"runs": [{k: r[k] for k in ("planted_fires", "stand_in_fires", "eligible")} for r in runs],
            "identical_target_states": identical,
            "retest_prompts": len(keys), "retest_state_agreement": sum(x == y for x, y in zip(sa, sb)) / len(keys),
            "eligible": identical and all(r["eligible"] for r in runs)}


def guard_reading(out: dict, screens: dict, sol_noise: dict, guard: str) -> dict:
    """I2's ADR 0009 reading, stated before any guard result: it counts iff the guard is eligible,
    the guard and sol are both '+' in GDPR v1, and neither is '-' in PLC; sol's direction is its
    noise-inflated CI (`sol_noise.py`)."""
    sol_dir = {d: sol_noise["domains"][d]["direction_noise_inflated"] for d in DOMAINS}
    if guard not in out["domains"]["plc"]:
        return {"guard": guard, "eligible": screens[guard]["eligible"], "sol_noise_inflated": sol_dir,
                "counts": False, "why": f"{guard} not eligible: its domains were not run"}
    g_dir = {d: direction(out["domains"][d][guard]["seed_free_closed"]) for d in DOMAINS}
    k = out["kappa"][f"sol-{guard}"]["admissible_pooled"]["kappa"]
    counts = (screens[guard]["eligible"] and g_dir["gdpr_v1"] == sol_dir["gdpr_v1"] == "+"
              and "-" not in (g_dir["plc"], sol_dir["plc"]))
    return {"guard": guard, "eligible": screens[guard]["eligible"],
            "by_domain": {d: {"guard": g_dir[d], "sol_noise_inflated": sol_dir[d], "agree": g_dir[d] == sol_dir[d]}
                          for d in DOMAINS},
            "counts": counts, "kappa_guard_sol_admissible": k,
            "weak_guard": k is not None and k < WEAK_GUARD_KAPPA}


def jev_vs_sol(out: dict, sol_noise: dict) -> dict:
    rows, spend = {}, {"usd": 0.0, "calls": 0}
    for d in DOMAINS:
        j, s = out["domains"][d]["jev"], out["domains"][d]["sol"]
        jd, sd = direction(j["seed_free_closed"]), sol_noise["domains"][d]["direction_noise_inflated"]
        delta = j["seed_free_closed"]["diff"] - s["seed_free_closed"]["diff"]
        k = out["kappa"]["sol-jev"][d]["kappa"]
        rows[d] = {"jev": j["seed_free_closed"], "sol_diff": s["seed_free_closed"]["diff"],
                   "jev_direction": jd, "sol_direction_noise_inflated": sd, "same_direction": jd == sd,
                   "delta_primary": delta, "kappa": k,
                   "close": jd == sd and abs(delta) <= CLOSE_TO_SOL["max_abs_delta_primary"]
                   and k is not None and k >= CLOSE_TO_SOL["min_kappa"]}
        spend["usd"] += j["spend"]["usd"]
        spend["calls"] += j["spend"]["calls"]
    return {"rule": CLOSE_TO_SOL, "by_domain": rows, "close_to_sol": all(r["close"] for r in rows.values()),
            "domain_spend": {**spend, "usd_per_judged_arm": spend["usd"] / spend["calls"] if spend["calls"] else None}}


def main() -> None:
    elig = {j: l73(j) for j in JUDGES}
    out = {"l73": {j: {k: elig[j][k] for k in ("planted_fires", "stand_in_fires", "eligible")} for j in JUDGES},
           "domains": {}, "kappa": {}, "adr0009": {}}
    screens = {j: screen(j) for j in SCREENED if BASE == HERE and (HERE / SCREENED[j][1] / "l73.json").exists()}
    extra = tuple(j for j in screens if (HERE / j / "plc" / "control2.json").exists())
    for j in extra:
        elig[j] = {"planted_fires": all(r["planted_fires"] for r in screens[j]["runs"]),
                   "stand_in_fires": any(r["stand_in_fires"] for r in screens[j]["runs"])}
    for d in DOMAINS:
        row = {}
        for j in JUDGES + extra:
            r = load(j, d)
            t = r["summary"]["total"]
            row[j] = {"n_pairs": t["n_pairs"], "n_discriminable": t["n_discriminable"],
                      "undecided": t["undecided"], "admissible": r["admissible"],
                      "seed_free_closed": t["seed_free"]["closed"],
                      "seed_free_closed_or_partial": t["seed_free"]["closed_or_partial"],
                      "equal_cap_closed": t["equal_cap"]["closed"],
                      "equal_cap_closed_or_partial": t["equal_cap"]["closed_or_partial"],
                      "length_stand_in": r["length_stand_in"],
                      "by_lens_primary": {ln: g["seed_free"]["closed"] for ln, g in r["summary"]["by_lens"].items()},
                      "verdict": verdict(t["seed_free"]["closed"], r["length_stand_in"], elig[j]),
                      "spend": r.get("spend"), "judge_settings": r.get("judge_settings")}
        out["domains"][d] = row
        q, s = row["qwen"]["seed_free_closed"], row["sol"]["seed_free_closed"]
        out["adr0009"][d] = {"qwen": direction(q), "sol": direction(s),
                             "agree": direction(q) == direction(s),
                             "counts": direction(q) == direction(s) and all(
                                 elig[j]["eligible"] for j in ("qwen", "sol"))}
    for j1, j2 in combinations(JUDGES + extra, 2):
        out["kappa"][f"{j1}-{j2}"] = {**{d: agreement(j1, j2, [d]) for d in DOMAINS},
                                      "admissible_pooled": agreement(j1, j2, ADMISSIBLE)}
    if RUN1.exists() and BASE == HERE:
        out["retest_run1_vs_run2"] = {j: {part: retest(j, part) for part in ("l73", *DOMAINS)} for j in JUDGES}
    if screens:
        sol_noise = json.loads((HERE / "sol_noise.json").read_text())
        out["i2_l73_screen"] = screens
        if GUARD in screens:
            out["i2_adr0009_guard"] = guard_reading(out, screens, sol_noise, GUARD)
        if "jev" in extra:
            out["i2_jev_vs_sol"] = jev_vs_sol(out, sol_noise)
    print(json.dumps(out, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
