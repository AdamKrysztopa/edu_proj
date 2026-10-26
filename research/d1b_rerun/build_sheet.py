"""D1b plan §3.1-3.3: fresh questions, topic clusters, arms by agreement, matching, sheet, seal.

    uv run --directory gapmap python ../research/d1b_rerun/build_sheet.py pool
    uv run --directory gapmap python ../research/d1b_rerun/build_sheet.py count --arm local=DIR
    uv run --directory gapmap python ../research/d1b_rerun/build_sheet.py build --arm local=DIR --arm sol=DIR \
        --public-key ~/.d1b/seal.pub

`pool` applies the fresh-question and debris filters and clusters versions of one topic across
both ledgers, before any closure state is read, and writes `pool.json` and the topic-review pack.
`count` gives Stop A's upper bound of matched topics from the local arm alone (sol can only remove
topics). `build` reads every arm's cached states (replay, no model call), assigns a topic to gap
only if every version and every arm says open and to covered only if all say closed, matches the
arms within strata (lens, k_topic band, ledgers, source origin) on question length and retrieval
similarity, writes `questions.md`, and seals the key with the closure caches and rebuilt maps under
the owner's public key. It prints aggregates and hashes only, never an arm.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import os
import random
import re
import shutil
import subprocess
import tarfile
from collections import Counter
from pathlib import Path

import common

SEED = 20261026
SIZES = (15, 12, 10)
BALANCE_TOL = 0.10
OWNER_REPO = "github.com/AdamKrysztopa/dependence-forecastability"
POOL = common.HERE / "pool.json"
REVIEW_PACK = common.HERE / "fixtures" / "topic_review_pack.md"
REVIEW = common.HERE / "fixtures" / "topic_review.json"


class TooFew(RuntimeError):
    pass


def cluster(rows: list[dict]) -> list[dict]:
    parent = list(range(len(rows)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    toks = [common.tokens(r["quote"]) for r in rows]
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            if rows[i]["anchor"] == rows[j]["anchor"] or common.jaccard(toks[i], toks[j]) >= common.TOPIC_JACCARD:
                parent[find(i)] = find(j)
    groups: dict[int, list[dict]] = {}
    for i, r in enumerate(rows):
        groups.setdefault(find(i), []).append(r)
    topics = []
    for members in sorted(groups.values(), key=lambda m: min((r["ledger"], r["test_id"]) for r in m)):
        members = sorted(members, key=lambda r: (r["ledger"], r["test_id"]))
        rep = members[0]
        topics.append({"topic_id": f"T{len(topics) + 1:03d}", "versions": [(r["ledger"], r["test_id"]) for r in members],
                       "lens": rep["lens"], "k_band": "1" if max(r["k_topic"] for r in members) <= 1 else ">=2",
                       "ledgers": "+".join(sorted({r["ledger"] for r in members})),
                       "source_origin": rep["source_origin"], "words": rep["words"], "similarity": rep["similarity"],
                       "question_text": rep["question_text"], "lenses": sorted({r["lens"] for r in members})})
    return topics


def arm_of(topic: dict, states: dict, judges: tuple[str, ...] | None = None) -> str | None:
    judges = judges or tuple(sorted({j for v in topic["versions"] for j in states.get(tuple(v), {})}))
    seen = []
    for v in topic["versions"]:
        st = states.get(tuple(v), {})
        if any(j not in st for j in judges):
            return None
        seen += [st[j] for j in judges]
    if seen and all(s == "open" for s in seen):
        return "gap"
    if seen and all(s == "closed" for s in seen):
        return "covered"
    return None


def stratum(t: dict) -> tuple:
    return (t["lens"], t["k_band"], t["ledgers"], t["source_origin"])


def _distance(g: dict, c: dict) -> float:
    return abs(g["words"] - c["words"]) / max(g["words"], c["words"], 1) + abs(g["similarity"] - c["similarity"]) / 0.05


def match(gaps: list[dict], covs: list[dict], *, n: int, seed: int) -> list[tuple[dict, dict]]:
    rng = random.Random(seed)
    gaps, covs = gaps[:], covs[:]
    rng.shuffle(gaps)
    rng.shuffle(covs)
    pairs, used = [], set()
    for g in gaps:
        options = [c for c in covs if c["topic_id"] not in used and stratum(c) == stratum(g)]
        if options:
            best = min(options, key=lambda c: _distance(g, c))
            used.add(best["topic_id"])
            pairs.append((g, best))
    pairs.sort(key=lambda p: (_distance(*p), p[0]["topic_id"]))
    return pairs[:n]


def balance(pairs: list[tuple[dict, dict]]) -> dict:
    mean = lambda xs: sum(xs) / len(xs) if xs else 0.0
    out = {k: {"gap": mean([g[k] for g, _ in pairs]), "covered": mean([c[k] for _, c in pairs])}
           for k in ("words", "similarity")}
    out["ok"] = all(abs(v["gap"] - v["covered"]) <= BALANCE_TOL * max(v["gap"], v["covered"])
                    for v in (out["words"], out["similarity"]))
    return out


def choose_size(gaps: list[dict], covs: list[dict], *, seed: int) -> tuple[int, list[tuple[dict, dict]]]:
    for n in SIZES:
        pairs = match(gaps, covs, n=n, seed=seed)
        if len(pairs) == n and balance(pairs)["ok"]:
            return n, pairs
    raise TooFew(f"fewer than {SIZES[-1]} matched, balanced topics per arm: the rerun stops (plan §3.2)")


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def seal(src: Path, public_key: Path, dest: Path) -> Path:
    """tar `src`, encrypt it under a fresh AES key, encrypt that key to the owner's RSA public key,
    then delete `src`. Only the owner's private key opens it."""
    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as tar:
        tar.add(src, arcname=".")
    sym = os.urandom(32).hex()
    dest.mkdir(parents=True, exist_ok=True)
    enc = subprocess.run(["openssl", "enc", "-aes-256-cbc", "-pbkdf2", "-salt", "-pass", "stdin"],
                         input=sym.encode() + b"\n" + buf.getvalue(), capture_output=True, check=True).stdout
    (dest / "archive.enc").write_bytes(enc)
    wrapped = subprocess.run(["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", str(public_key),
                              "-pkeyopt", "rsa_padding_mode:oaep"], input=sym.encode(),
                             capture_output=True, check=True).stdout
    (dest / "key.enc").write_bytes(wrapped)
    (dest / "sealed.sha256.json").write_text(json.dumps(
        {"archive_sha256": _sha(dest / "archive.enc"), "key_sha256": _sha(dest / "key.enc"),
         "public_key_sha256": _sha(public_key)}, indent=1) + "\n")
    shutil.rmtree(src)
    return dest


def unseal(sealed: Path, private_key: Path, out: Path) -> Path:
    sym = subprocess.run(["openssl", "pkeyutl", "-decrypt", "-inkey", str(private_key),
                          "-pkeyopt", "rsa_padding_mode:oaep", "-in", str(sealed / "key.enc")],
                         capture_output=True, check=True).stdout
    raw = subprocess.run(["openssl", "enc", "-d", "-aes-256-cbc", "-pbkdf2", "-pass", "stdin"],
                         input=sym + b"\n" + (sealed / "archive.enc").read_bytes(),
                         capture_output=True, check=True).stdout
    out.mkdir(parents=True, exist_ok=True)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        tar.extractall(out, filter="data")
    return out


# ---- ledger-facing steps (need the gapmap env and the D1 ledgers) ----

def _retriever():
    import importlib.util
    spec = importlib.util.spec_from_file_location("d1_judge_retriever", common.HERE / "novelty.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Retriever(mod.passages())


def _clean(text_: str) -> str:
    text_ = re.sub(r"\s>\s(?![\d=])", " ", text_)
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text_)


def pool_rows() -> list[dict]:
    from gapmap import lenses, link, semantic

    d1 = common.d1_items()
    d1_tok = common.d1_tokens()
    d1_keys = {(" ".join(sorted(common.tokens(common.quote(it["text"])))), it["lens"]) for it in d1}
    retriever = _retriever()
    rows = []
    for name in common.LEDGER_DIRS:
        lg, index, _ = common.load(name)
        cands = [c for c in lenses.run_all(lg, index, link.SETTING_1) if c.question_text and not c.excluded]
        d1_seeds = {sid for c in cands
                    if (" ".join(sorted(common.tokens(common.quote(c.question_text)))), c.lens) in d1_keys
                    for sid in c.seeds}
        for c in cands:
            q = common.quote(c.question_text)
            if (common.debris(q) or c.seeds & d1_seeds
                    or common.max_d1_jaccard(c, d1_tok)[0] >= common.FRESH_JACCARD):
                continue
            seed_ids = semantic.primary_probe(lg, c)[1]
            src = lg.by_id[min(seed_ids)].evidence[0].source.identifier
            question = _clean(c.question_text)
            rows.append({"ledger": name, "test_id": c.test_id, "lens": c.lens, "quote": q, "anchor": c.anchor,
                         "k_topic": len(link.breadth(lg, c.x_a)),
                         "source_origin": "owner" if OWNER_REPO in src else "outside",
                         "words": len(question.split()), "similarity": retriever.similarity(question),
                         "question_text": question})
    return rows


def cmd_pool(_args) -> int:
    rows = pool_rows()
    topics = cluster(rows)
    POOL.write_text(json.dumps({"rows": rows, "topics": topics}, indent=1, sort_keys=True) + "\n")
    lines = ["# D1b topic review pack", "",
             "Flag any topic below that shares a topic with one of D1's 15 questions or with another topic below.",
             "", "## D1's 15 questions", ""]
    lines += [f"- D1-Q{it['q']}: {it['text']}" for it in common.d1_items()]
    lines += ["", "## Candidate topics", ""] + [f"- {t['topic_id']}: {t['question_text']}" for t in topics]
    REVIEW_PACK.write_text("\n".join(lines) + "\n")
    print(json.dumps({"fresh_versions": len(rows), "topics": len(topics),
                      "by_lens": Counter(t["lens"] for t in topics), "by_k_band": Counter(t["k_band"] for t in topics),
                      "by_ledgers": Counter(t["ledgers"] for t in topics),
                      "by_source_origin": Counter(t["source_origin"] for t in topics)}, indent=1))
    return 0


def _states(arm_dirs: dict[str, Path], rows_by_version: dict) -> dict:
    from gapmap import judge as judge_mod, lenses, link, semantic

    class Replay:
        def __init__(self, model_id):
            self.model_id = model_id

        def ask(self, prompt):
            raise judge_mod.JudgeCacheMiss("replay only")

    states: dict = {}
    for arm, d in arm_dirs.items():
        for name in common.LEDGER_DIRS:
            rec = json.loads((d / name / "judge.json").read_text())
            judge = judge_mod.CachedJudge(Replay(rec["judge_model"]), d / name / "closure_judgements.json", live=False)
            lg, index, _ = common.load(name)
            for c in lenses.run_all(lg, index, link.SETTING_1):
                if (name, c.test_id) in rows_by_version:
                    states.setdefault((name, c.test_id), {})[arm] = semantic.judge_candidate(lg, index, judge, c)[0].state
    return states


def _arms(args) -> tuple[list[dict], dict, list, list]:
    pool = json.loads(POOL.read_text())
    review = json.loads(REVIEW.read_text())
    topics = [t for t in pool["topics"] if t["topic_id"] not in set(review["drop"])]
    rows_by_version = {(r["ledger"], r["test_id"]): r for r in pool["rows"]}
    arm_dirs = dict((k, Path(v)) for k, v in (a.split("=", 1) for a in args.arm))
    states = _states(arm_dirs, rows_by_version)
    judges = tuple(sorted(arm_dirs))
    for t in topics:
        t["versions"] = [tuple(v) for v in t["versions"]]
    gaps = [t for t in topics if arm_of(t, states, judges) == "gap"]
    covs = [t for t in topics if arm_of(t, states, judges) == "covered"]
    return topics, states, gaps, covs


def cmd_count(args) -> int:
    topics, _states_, gaps, covs = _arms(args)
    try:
        n, pairs = choose_size(gaps, covs, seed=SEED)
    except TooFew:
        n, pairs = 0, match(gaps, covs, n=max(SIZES), seed=SEED)
    print(json.dumps({"topics": len(topics), "all_open": len(gaps), "all_closed": len(covs),
                      "matched_pairs_upper_bound": len(pairs), "sheet_size_reachable": n,
                      "stop_at_A": n == 0}, indent=1))
    return 0


def cmd_build(args) -> int:
    topics, states, gaps, covs = _arms(args)
    n, pairs = choose_size(gaps, covs, seed=SEED)
    items = [{"arm": "gap", **g} for g, _ in pairs] + [{"arm": "covered", **c} for _, c in pairs]
    random.Random(SEED).shuffle(items)
    for i, it in enumerate(items, 1):
        it["q"] = i
    sheet = ["# D1b questions", "",
             "One question at a time, in chat. Answer in plain prose, from memory, without the docs or the code open.",
             "\"I don't know\" or \"this never comes up\" is a fine answer.", ""]
    for it in items:
        sheet += [f"## Q{it['q']}", "", it["question_text"], ""]
    (common.HERE / "questions.md").write_text("\n".join(sheet))
    secret = common.HERE / "secret"
    secret.mkdir(exist_ok=True)
    (secret / "key.json").write_text(json.dumps(
        {"seed": SEED, "n_per_arm": n, "items": items, "balance": balance(pairs),
         "states": {f"{k[0]}|{k[1]}": v for k, v in states.items()}}, indent=1, sort_keys=True, default=list) + "\n")
    for arm_dir in (Path(v) for v in (a.split("=", 1)[1] for a in args.arm)):
        shutil.copytree(arm_dir, secret / "arms" / arm_dir.name)
    sealed = seal(secret, Path(args.public_key).expanduser(), common.HERE / "sealed")
    for arm_dir in (Path(v) for v in (a.split("=", 1)[1] for a in args.arm)):
        shutil.rmtree(arm_dir)
    bal = balance(pairs)
    print(json.dumps({"n_per_arm": n, "questions_sha256": _sha(common.HERE / "questions.md"),
                      **json.loads((sealed / "sealed.sha256.json").read_text()),
                      "mean_words": bal["words"], "mean_similarity": bal["similarity"],
                      "lens_mix": Counter(it["lens"] for it in items), "eligible_open": len(gaps),
                      "eligible_closed": len(covs)}, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="build_sheet")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pool")
    for name in ("count", "build"):
        s = sub.add_parser(name)
        s.add_argument("--arm", action="append", required=True, metavar="NAME=DIR")
        if name == "build":
            s.add_argument("--public-key", required=True)
    args = p.parse_args(argv)
    return {"pool": cmd_pool, "count": cmd_count, "build": cmd_build}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
