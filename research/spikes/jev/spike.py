#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy"]
# ///
"""JEV spike: does a System-One decision model's tacit-knowledge judgement
carry signal beyond the N3 gap map's own source-density features?

Subcommands: estimate | smoke | run | analyse
Run with: uv run research/spikes/jev/spike.py <subcommand>
"""
import json
import hashlib
import math
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

HERE = Path(__file__).parent
CACHE_DIR = HERE / "cache"
ANALYSIS_PATH = HERE / "analysis.json"
REPO_ROOT = HERE.parent.parent.parent  # research/spikes/jev -> repo root
GAPMAP_PATHS = {
    "plc": REPO_ROOT / "research/n3/plc/gapmap.json",
    "gdpr_v1": REPO_ROOT / "research/n3/gdpr_v1/gapmap.json",
    "gdpr_v2": REPO_ROOT / "research/n3/gdpr_v2/gapmap.json",
}
FIELD_BY_DOMAIN = {
    "plc": "industrial PLC troubleshooting",
    "gdpr_v1": "GDPR data protection impact assessments",
    "gdpr_v2": "GDPR data protection impact assessments",
}
KEEP_CATEGORIES = {"HYP", "RG-SINGLE", "RG-SIBLING", "RG-UNVER"}
EXPECTED_N = 61
MODEL = "typesafe/jev-1.13"
API_URL = "https://openrouter.ai/api/alpha/decisions"
PRICE_PER_M_INPUT = 0.042
HARD_CAP_USD = 3.00

QUESTIONS = {
    "tacit_a": {
        "type": "noul",
        "instructions": "Is the missing element something experienced practitioners typically know from hands-on practice but rarely write down explicitly?",
        "criteria": {
            "true": "Tacit, experience-based know-how that written sources seldom state.",
            "false": "Something routinely stated in written guidance, standards or textbooks.",
        },
    },
    "tacit_b": {
        "type": "noul",
        "instructions": "Would supplying what is missing most likely require asking a seasoned practitioner rather than consulting standard documentation?",
        "criteria": {
            "true": "Only practitioners' experience would supply it.",
            "false": "Standard documentation would supply it.",
        },
    },
    "mainstream": {
        "type": "noul",
        "instructions": "Is the statement about a mainstream topic that introductory material in this field commonly covers?",
        "criteria": {
            "true": "A core, widely covered topic.",
            "false": "A niche or specialised topic.",
        },
    },
    "has_number": {
        "type": "noul",
        "instructions": "Does the statement or the missing element contain a specific number, date or quantity?",
        "criteria": {
            "true": "Contains a number, date or quantity.",
            "false": "Contains none.",
        },
    },
}


def load_records():
    """Load and filter the 61 admissible gap-map records, in stable order."""
    records = []
    counts = {}
    for domain, path in GAPMAP_PATHS.items():
        data = json.loads(path.read_text())
        raw = data["map"] + data["retrieval_gaps"]
        for r in raw:
            cat = r.get("category")
            counts[(domain, cat)] = counts.get((domain, cat), 0) + 1
            if cat not in KEEP_CATEGORIES:
                continue
            c = r["confidence"]
            records.append({
                "domain": domain,
                "gap_id": r["gap_id"],
                "category": cat,
                "lens": r.get("lens"),
                "k_topic": c["k_topic"],
                "k_step": c["k_step"],
                "score": c["score"],
                "rank": r.get("rank"),
                "anchor": r["anchor"],
                "missing": r["missing"],
            })
    return records, counts


def print_counts(counts):
    by_dc = {}
    for (domain, cat), n in sorted(counts.items()):
        by_dc.setdefault(domain, {})[cat] = n
    for domain, cats in by_dc.items():
        print(f"  {domain}: {cats}")
    kept = {}
    for (domain, cat), n in counts.items():
        if cat in KEEP_CATEGORIES:
            kept[cat] = kept.get(cat, 0) + n
    print(f"  KEPT by category: {kept} -> total {sum(kept.values())}")


def build_state(rec):
    return {
        "field": FIELD_BY_DOMAIN[rec["domain"]],
        "statement": rec["anchor"],
        "what_is_missing": rec["missing"],
    }


def build_request(rec):
    return {"model": MODEL, "state": build_state(rec), "questions": QUESTIONS}


def cache_key(body):
    canon = json.dumps(body, sort_keys=True)
    return hashlib.sha256(canon.encode()).hexdigest()


def cache_path(key):
    return CACHE_DIR / f"{key}.json"


def est_tokens(body):
    return math.ceil(len(json.dumps(body)) / 3)


def cached_cost_sum():
    total = 0.0
    n = 0
    for f in CACHE_DIR.glob("*.json"):
        d = json.loads(f.read_text())
        total += d["response"]["usage"]["cost"]
        n += 1
    return total, n


def require_key_headroom(api_key, needed_usd):
    """The run's own cap counts only this spike's spend; the key's limit is separate."""
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/key", headers={"Authorization": f"Bearer {api_key}"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        d = json.loads(resp.read().decode())["data"]
    remaining = d.get("limit_remaining")
    print(f"key limit={d.get('limit')} remaining={remaining} reset={d.get('limit_reset')}")
    if remaining is not None and remaining < needed_usd:
        print(f"key headroom ${remaining} < needed ${needed_usd:.6f}; not sending", file=sys.stderr)
        sys.exit(1)


def cmd_estimate():
    records, counts = load_records()
    print("Category counts (domain x category), full ledger before filtering:")
    print_counts(counts)
    assert len(records) == EXPECTED_N, f"expected {EXPECTED_N} records, got {len(records)}"
    bodies = [build_request(r) for r in records]
    tokens = [est_tokens(b) for b in bodies]
    total_tokens = sum(tokens)
    est_usd = total_tokens / 1_000_000 * PRICE_PER_M_INPUT
    n_cached = sum(1 for b in bodies if cache_path(cache_key(b)).exists())
    print(f"\nn_calls = {len(bodies)}")
    print(f"est total input tokens = {total_tokens}")
    print(f"est cost @ ${PRICE_PER_M_INPUT}/M input tokens = ${est_usd:.6f}")
    print(f"already cached = {n_cached}/{len(bodies)}")
    prior_cost, prior_n = cached_cost_sum()
    print(f"actual cost already spent (from cache) = ${prior_cost:.6f} over {prior_n} calls")


def get_api_key():
    import os
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY not set in environment", file=sys.stderr)
        sys.exit(1)
    return key


def call_api(body, api_key):
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        API_URL,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    attempt = 0
    while True:
        attempt += 1
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                return resp.status, json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            body_text = e.read().decode(errors="replace")
            if e.code == 429 and attempt == 1:
                print("429 received, retrying once after 5s backoff", file=sys.stderr)
                time.sleep(5)
                continue
            print(f"HTTP {e.code}: {body_text}", file=sys.stderr)
            return e.code, None


def validate_answers(resp):
    for qid in QUESTIONS:
        ans = resp.get("answers", {}).get(qid)
        if not ans or not isinstance(ans.get("noul"), (int, float)):
            return qid
    return None


def cmd_smoke():
    records, _ = load_records()
    assert len(records) == EXPECTED_N
    rec = records[0]
    body = build_request(rec)
    key = cache_key(body)
    cpath = cache_path(key)
    if cpath.exists():
        print(f"already cached at {cpath}, printing cached response")
        print(json.dumps(json.loads(cpath.read_text())["response"], indent=2))
        return
    api_key = get_api_key()
    require_key_headroom(api_key, est_tokens(body) / 1_000_000 * PRICE_PER_M_INPUT)
    print(f"sending smoke request for gap_id={rec['gap_id']} domain={rec['domain']}")
    status, resp = call_api(body, api_key)
    if status != 200 or resp is None:
        print(f"smoke call failed with status {status}", file=sys.stderr)
        sys.exit(1)
    bad = validate_answers(resp)
    if bad:
        print(f"missing/non-numeric noul for question id: {bad}", file=sys.stderr)
        sys.exit(1)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cpath.write_text(json.dumps({"request": body, "response": resp}, indent=2))
    print(json.dumps(resp, indent=2))


def cmd_run():
    records, _ = load_records()
    assert len(records) == EXPECTED_N
    api_key = get_api_key()
    pending = [build_request(r) for r in records if not cache_path(cache_key(build_request(r))).exists()]
    require_key_headroom(api_key, sum(est_tokens(b) for b in pending) / 1_000_000 * PRICE_PER_M_INPUT)
    cumulative_cost, _ = cached_cost_sum()
    sent = 0
    for rec in records:
        body = build_request(rec)
        key = cache_key(body)
        cpath = cache_path(key)
        if cpath.exists():
            continue
        est_cost = est_tokens(body) / 1_000_000 * PRICE_PER_M_INPUT
        if cumulative_cost + est_cost > HARD_CAP_USD:
            print(
                f"hard cap ${HARD_CAP_USD} would be exceeded "
                f"(cumulative ${cumulative_cost:.6f} + est ${est_cost:.6f}); stopping",
                file=sys.stderr,
            )
            sys.exit(1)
        print(f"sending gap_id={rec['gap_id']} domain={rec['domain']} ({sent + 1} sent so far)...")
        status, resp = call_api(body, api_key)
        if status != 200 or resp is None:
            print(f"call failed with status {status}; stopping after first failure", file=sys.stderr)
            sys.exit(1)
        bad = validate_answers(resp)
        if bad:
            print(f"missing/non-numeric noul for question id: {bad} (gap_id={rec['gap_id']})", file=sys.stderr)
            sys.exit(1)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        cpath.write_text(json.dumps({"request": body, "response": resp}, indent=2))
        cumulative_cost += resp["usage"]["cost"]
        sent += 1
    total_cost, total_n = cached_cost_sum()
    print(f"\ndone. sent {sent} new calls this run. cumulative cost over {total_n} cached calls = ${total_cost:.6f}")


def load_all_answers(records):
    """Join cached answers onto records; error if any record's cache is missing."""
    rows = []
    for rec in records:
        body = build_request(rec)
        key = cache_key(body)
        cpath = cache_path(key)
        if not cpath.exists():
            print(f"missing cached response for gap_id={rec['gap_id']}; run 'run' first", file=sys.stderr)
            sys.exit(1)
        resp = json.loads(cpath.read_text())["response"]
        bad = validate_answers(resp)
        if bad:
            print(f"cached response for gap_id={rec['gap_id']} missing noul {bad}", file=sys.stderr)
            sys.exit(1)
        row = dict(rec)
        for qid in QUESTIONS:
            row[qid] = resp["answers"][qid]["noul"]
        rows.append(row)
    return rows


def cmd_analyse():
    import numpy as np
    from scipy import stats

    records, _ = load_records()
    assert len(records) == EXPECTED_N
    rows = load_all_answers(records)
    n = len(rows)

    tacit_a = np.array([r["tacit_a"] for r in rows])
    tacit_b = np.array([r["tacit_b"] for r in rows])
    mainstream = np.array([r["mainstream"] for r in rows])
    has_number = np.array([r["has_number"] for r in rows])
    k_topic = np.array([r["k_topic"] for r in rows], dtype=float)
    k_step = np.array([r["k_step"] for r in rows], dtype=float)
    score = np.array([r["score"] for r in rows], dtype=float)
    C = (tacit_a + tacit_b) / 2.0

    def spearman(a, b):
        rho, _ = stats.spearmanr(a, b)
        return float(rho)

    rho_reliability = spearman(tacit_a, tacit_b)
    rho_C_ktopic = spearman(C, k_topic)
    rho_C_score = spearman(C, score)
    rho_ktopic_score = spearman(k_topic, score)

    # --- residual reliability ---
    domains = np.array([r["domain"] for r in rows])
    domain_dummy = np.array([0.0 if d == "plc" else 1.0 for d in domains])  # 0=plc,1=gdpr
    lens = np.array([r["lens"] for r in rows])
    lens_levels = sorted(set(lens.tolist()))
    text_len = np.array([len(r["anchor"]) + len(r["missing"]) for r in rows], dtype=float)

    def rank(x):
        return stats.rankdata(x)

    def build_design(covariates):
        cols = [np.ones(n)] + covariates
        return np.column_stack(cols)

    def ols_resid(y, X):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        return y - X @ beta

    m1_covariates = [rank(k_topic), rank(k_step), rank(score), text_len, domain_dummy]
    lens_dummies = [
        np.array([1.0 if lv == level else 0.0 for lv in lens])
        for level in lens_levels[1:]  # drop first level
    ]
    m2_covariates = m1_covariates + lens_dummies

    X1 = build_design(m1_covariates)
    X2 = build_design(m2_covariates)

    def pearson(a, b):
        r, _ = stats.pearsonr(a, b)
        return float(r)

    def residual_pair(y1, y2, X):
        r1 = ols_resid(rank(y1), X)
        r2 = ols_resid(rank(y2), X)
        return r1, r2, pearson(r1, r2)

    resid_a_m1, resid_b_m1, r_resid_m1 = residual_pair(tacit_a, tacit_b, X1)
    resid_a_m2, resid_b_m2, r_resid_m2 = residual_pair(tacit_a, tacit_b, X2)

    rng = np.random.default_rng(0)

    def bootstrap_ci(y1, y2, X, n_boot=2000):
        idx_all = np.arange(n)
        vals = []
        for _ in range(n_boot):
            idx = rng.choice(idx_all, size=n, replace=True)
            r1 = ols_resid(rank(y1[idx]), X[idx])
            r2 = ols_resid(rank(y2[idx]), X[idx])
            vals.append(pearson(r1, r2))
        vals = np.array(vals)
        n_bad = int(np.isnan(vals).sum())
        if n_bad:
            print(f"bootstrap: {n_bad}/{n_boot} resamples gave an undefined r; excluded", file=sys.stderr)
        vals = vals[~np.isnan(vals)]
        return float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5))

    ci_m2 = bootstrap_ci(tacit_a, tacit_b, X2)

    # discriminant controls, under M2, tacit_a vs has_number / mainstream
    _, _, r_a_hasnum_m2 = residual_pair(tacit_a, has_number, X2)
    ci_a_hasnum_m2 = bootstrap_ci(tacit_a, has_number, X2)
    _, _, r_a_mainstream_m2 = residual_pair(tacit_a, mainstream, X2)
    ci_a_mainstream_m2 = bootstrap_ci(tacit_a, mainstream, X2)

    # --- descriptive only ---
    rho_mainstream_ktopic = spearman(mainstream, k_topic)
    cat_arr = np.array([r["category"] for r in rows])
    median_C_by_cat = {c: float(np.median(C[cat_arr == c])) for c in sorted(set(cat_arr.tolist()))}
    median_C_by_lens = {l: float(np.median(C[lens == l])) for l in lens_levels}
    rho_C_ktopic_by_domain = {}
    for d in sorted(set(domains.tolist())):
        mask = domains == d
        if mask.sum() > 2:
            rho_C_ktopic_by_domain[d] = spearman(C[mask], k_topic[mask])

    def classify(rel, r_ck, r_cs, r_res, ci_lo, r_ctrl):
        if rel < 0.30 or abs(r_ck) >= 0.70 or r_res < 0.20:
            return "NO SIGNAL"
        if (rel >= 0.50 and abs(r_ck) < 0.40 and abs(r_cs) < 0.40 and r_res >= 0.40
                and ci_lo > 0.10 and (r_res - abs(r_ctrl)) >= 0.20):
            return "PROMISING"
        return "INCONCLUSIVE"

    classification = classify(rho_reliability, rho_C_ktopic, rho_C_score, r_resid_m2, ci_m2[0], r_a_hasnum_m2)

    # Rule sanity check (added after the hostile review): the same rule applied to two
    # trivial word-length statistics of the anchor, standing in for the two paraphrases.
    words = [r["anchor"].split() for r in rows]
    triv_a = np.array([np.mean([len(w) for w in ws]) for ws in words])
    triv_b = np.array([np.mean([len(w) > 7 for w in ws]) for ws in words])
    triv_C = (stats.rankdata(triv_a) + stats.rankdata(triv_b)) / 2
    _, _, triv_r_res = residual_pair(triv_a, triv_b, X2)
    _, _, triv_r_hn = residual_pair(triv_a, has_number, X2)
    triv_ci = bootstrap_ci(triv_a, triv_b, X2)
    trivial = {
        "rho_a_b": spearman(triv_a, triv_b),
        "rho_C_ktopic": spearman(triv_C, k_topic),
        "rho_C_score": spearman(triv_C, score),
        "r_resid_M2": triv_r_res,
        "bootstrap_ci_M2": triv_ci,
        "r_vs_has_number_M2": triv_r_hn,
    }
    trivial["classification"] = classify(trivial["rho_a_b"], trivial["rho_C_ktopic"], trivial["rho_C_score"],
                                         triv_r_res, triv_ci[0], triv_r_hn)
    rho_C_score_by_domain = {d: spearman(C[domains == d], score[domains == d]) for d in sorted(set(domains.tolist()))}
    lens_n = {l: int((lens == l).sum()) for l in lens_levels}

    # --- examples ---
    def trim(s, n=200):
        return s if len(s) <= n else s[: n - 3] + "..."

    low_density_mask = k_topic <= 1
    low_density_idx = np.where(low_density_mask)[0]
    top_C_low_density = sorted(low_density_idx, key=lambda i: -C[i])[:3]

    q75 = np.percentile(k_topic, 75)
    top_density_idx = np.where(k_topic >= q75)[0]
    bottom_C_top_density = sorted(top_density_idx, key=lambda i: C[i])[:3]

    def example_row(i):
        r = rows[i]
        return {
            "domain": r["domain"],
            "category": r["category"],
            "lens": r["lens"],
            "k_topic": r["k_topic"],
            "score": r["score"],
            "C": float(C[i]),
            "anchor": trim(r["anchor"]),
            "missing": trim(r["missing"]),
        }

    examples = {
        "highest_C_among_low_density": [example_row(i) for i in top_C_low_density],
        "lowest_C_among_top_density_quartile": [example_row(i) for i in bottom_C_top_density],
    }

    result = {
        "n": n,
        "reliability": {"rho_tacit_a_tacit_b": rho_reliability},
        "redundancy": {
            "rho_C_ktopic": rho_C_ktopic,
            "rho_C_score": rho_C_score,
            "rho_ktopic_score_reference": rho_ktopic_score,
        },
        "residual_reliability": {
            "r_resid_M1": r_resid_m1,
            "r_resid_M2": r_resid_m2,
            "bootstrap_ci_M2": ci_m2,
        },
        "discriminant_control": {
            "tacit_a_vs_has_number_M2": r_a_hasnum_m2,
            "tacit_a_vs_has_number_M2_ci": ci_a_hasnum_m2,
            "tacit_a_vs_mainstream_M2": r_a_mainstream_m2,
            "tacit_a_vs_mainstream_M2_ci": ci_a_mainstream_m2,
        },
        "descriptive": {
            "rho_mainstream_ktopic": rho_mainstream_ktopic,
            "median_C_by_category": median_C_by_cat,
            "median_C_by_lens": median_C_by_lens,
            "rho_C_ktopic_by_domain": rho_C_ktopic_by_domain,
            "rho_C_score_by_domain": rho_C_score_by_domain,
            "rho_C_mainstream": spearman(C, mainstream),
            "lens_n": lens_n,
        },
        "classification": classification,
        "trivial_text_baseline": trivial,
        "examples": examples,
    }

    ANALYSIS_PATH.write_text(json.dumps(result, indent=2))

    print(f"n = {n}")
    print(f"reliability rho(tacit_a,tacit_b) = {rho_reliability:.3f}")
    print(f"redundancy rho(C,k_topic) = {rho_C_ktopic:.3f}  rho(C,score) = {rho_C_score:.3f}  rho(k_topic,score) = {rho_ktopic_score:.3f}")
    print(f"residual r M1 = {r_resid_m1:.3f}  M2 = {r_resid_m2:.3f}  95% CI M2 = ({ci_m2[0]:.3f}, {ci_m2[1]:.3f})")
    print(f"discriminant tacit_a~has_number M2 = {r_a_hasnum_m2:.3f} CI {ci_a_hasnum_m2}")
    print(f"discriminant tacit_a~mainstream M2 = {r_a_mainstream_m2:.3f} CI {ci_a_mainstream_m2}")
    print(f"rho(mainstream,k_topic) = {rho_mainstream_ktopic:.3f}")
    print(f"median C by category = {median_C_by_cat}")
    print(f"median C by lens = {median_C_by_lens}")
    print(f"rho(C,k_topic) by domain = {rho_C_ktopic_by_domain}")
    print(f"rho(C,score) by domain = {rho_C_score_by_domain}")
    print(f"CLASSIFICATION (registered rule): {classification}")
    print(f"trivial word-length baseline under the same rule: {trivial}")
    print(f"\nwrote {ANALYSIS_PATH}")


# Loop 2: is C a surface statistic of the text? Rule fixed before any loop-2 call.
FORM_RULE = {"no_signal_if_rho_len_at_least": 0.5, "objection_removed_if_rho_len_at_most": 0.2}


def _perturb(text, mode, rng, pool_by_len):
    import re
    toks = text.split()
    if mode == "shuffle":
        rng.shuffle(toks)
        return " ".join(toks)
    out = []
    for t in toks:
        m = re.match(r"^(\W*)(\w+)(\W*)$", t)
        if not m:
            out.append(t)
            continue
        pre, core, post = m.groups()
        cands = [w for w in pool_by_len.get(len(core), []) if w.lower() != core.lower()]
        out.append(pre + (rng.choice(cands) if cands else core) + post)
    return " ".join(out)


def perturbed_bodies(records):
    import random
    import re
    pool_by_len = {}
    for r in records:
        for w in re.findall(r"\w+", r["anchor"] + " " + r["missing"]):
            pool_by_len.setdefault(len(w), set()).add(w)
    pool_by_len = {k: sorted(v) for k, v in pool_by_len.items()}
    out = {"lenmatch": [], "shuffle": []}
    for r in records:
        for mode in out:
            rng = random.Random(f"{mode}:{r['gap_id']}")
            state = {
                "field": FIELD_BY_DOMAIN[r["domain"]],
                "statement": _perturb(r["anchor"], mode, rng, pool_by_len),
                "what_is_missing": _perturb(r["missing"], mode, rng, pool_by_len),
            }
            out[mode].append({"model": MODEL, "state": state, "questions": QUESTIONS})
    return out


def cmd_loop2():
    import numpy as np
    from scipy import stats

    records, _ = load_records()
    assert len(records) == EXPECTED_N
    bodies = perturbed_bodies(records)
    pending = {cache_key(b): b for bs in bodies.values() for b in bs if not cache_path(cache_key(b)).exists()}
    est = sum(est_tokens(b) for b in pending.values()) / 1_000_000 * PRICE_PER_M_INPUT
    print(f"loop2: {len(pending)} uncached calls, est ${est:.6f}")
    print(f"example lenmatch state: {bodies['lenmatch'][0]['state']}")
    if pending:
        api_key = get_api_key()
        require_key_headroom(api_key, est)
        cumulative, _ = cached_cost_sum()
        for key, body in pending.items():
            if cumulative + est_tokens(body) / 1_000_000 * PRICE_PER_M_INPUT > HARD_CAP_USD:
                sys.exit(f"hard cap ${HARD_CAP_USD} would be exceeded; stopping")
            status, resp = call_api(body, api_key)
            if status != 200 or resp is None:
                sys.exit(f"call failed with status {status}; stopping")
            if bad := validate_answers(resp):
                sys.exit(f"missing/non-numeric noul {bad}")
            cache_path(key).write_text(json.dumps({"request": body, "response": resp}, indent=2))
            cumulative += resp["usage"]["cost"]
        print(f"cumulative cost over all cached calls = ${cached_cost_sum()[0]:.6f}")

    def c_of(body):
        a = json.loads(cache_path(cache_key(body)).read_text())["response"]["answers"]
        return (a["tacit_a"]["noul"] + a["tacit_b"]["noul"]) / 2

    # one row per unique original state, so duplicated texts are not double-counted
    seen, idx = set(), []
    for i, r in enumerate(records):
        k = cache_key(build_request(r))
        if k not in seen:
            seen.add(k)
            idx.append(i)
    C = np.array([c_of(build_request(records[i])) for i in idx])
    C_len = np.array([c_of(bodies["lenmatch"][i]) for i in idx])
    C_shuf = np.array([c_of(bodies["shuffle"][i]) for i in idx])
    kt = np.array([records[i]["k_topic"] for i in idx], dtype=float)
    plc = np.array([records[i]["domain"] == "plc" for i in idx])

    rho_len = float(stats.spearmanr(C, C_len)[0])
    rng = np.random.default_rng(0)
    boot = []
    for _ in range(2000):
        s = rng.choice(len(C), len(C), replace=True)
        boot.append(stats.spearmanr(C[s], C_len[s])[0])
    ci = (float(np.nanpercentile(boot, 2.5)), float(np.nanpercentile(boot, 97.5)))
    if rho_len >= FORM_RULE["no_signal_if_rho_len_at_least"]:
        verdict = "NO SIGNAL (C tracks surface form)"
    elif rho_len <= FORM_RULE["objection_removed_if_rho_len_at_most"]:
        verdict = "word-length objection removed (C depends on content)"
    else:
        verdict = "INCONCLUSIVE (partly form-driven)"
    result = {
        "n_unique": len(C),
        "rule": FORM_RULE,
        "rho_C_vs_lenmatch": rho_len,
        "rho_C_vs_lenmatch_ci": ci,
        "rho_C_vs_shuffle": float(stats.spearmanr(C, C_shuf)[0]),
        "mean_C": float(C.mean()), "mean_C_lenmatch": float(C_len.mean()), "mean_C_shuffle": float(C_shuf.mean()),
        "sd_C": float(C.std()), "sd_C_lenmatch": float(C_len.std()),
        "rho_C_lenmatch_vs_ktopic": float(stats.spearmanr(C_len, kt)[0]),
        "rho_C_vs_ktopic_plc": float(stats.spearmanr(C[plc], kt[plc])[0]),
        "rho_C_lenmatch_vs_ktopic_plc": float(stats.spearmanr(C_len[plc], kt[plc])[0]),
        "verdict": verdict,
    }
    (HERE / "analysis_loop2.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


def main():
    cmds = {"estimate": cmd_estimate, "smoke": cmd_smoke, "run": cmd_run, "analyse": cmd_analyse, "loop2": cmd_loop2}
    if len(sys.argv) != 2 or sys.argv[1] not in cmds:
        print(__doc__)
        sys.exit(1)
    cmds[sys.argv[1]]()


if __name__ == "__main__":
    main()
