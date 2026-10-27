"""D1b plan §3.1-3.3: fresh questions, topic clusters, arms by agreement, matching, sheet, seal.

    uv run --directory gapmap python ../research/d1b_rerun/build_sheet.py pool [--codebase CFG]
    uv run --directory gapmap python ../research/d1b_rerun/build_sheet.py count --arm local=DIR [--codebase CFG]
    uv run --directory gapmap python ../research/d1b_rerun/build_sheet.py build --arm local=DIR --arm sol=DIR \
        --public-key ~/.d1b/seal.pub [--codebase CFG]

`--codebase` names a config read by `codebase.py`; the default is D1b's own `codebase.json`.

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

import codebase
import common

SEED = 20261026
SIZES = (15, 12, 10)
BALANCE_TOL = 0.10


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


# ---- ledger-facing steps (need the gapmap env and the codebase's ledgers) ----

def _retriever(cb: codebase.Codebase):
    import importlib.util
    spec = importlib.util.spec_from_file_location("d1_judge_retriever", common.HERE / "novelty.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.Retriever(mod.passages(cb.corpus))


def _clean(text_: str) -> str:
    text_ = re.sub(r"\s>\s(?![\d=])", " ", text_)
    return re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text_)


def pool_rows(cb: codebase.Codebase, ledgers: list[str] | None = None) -> list[dict]:
    """Fresh-question and debris filters; `prior_items` are the earlier test's questions on this
    codebase (D1's for D1b), none for a codebase never tested before."""
    from gapmap import lenses, link, semantic

    prior = cb.prior_items()
    prior_tok = common.d1_tokens(prior)
    prior_keys = {(" ".join(sorted(common.tokens(common.quote(it["text"])))), it["lens"]) for it in prior}
    retriever = _retriever(cb)
    rows = []
    for name in ledgers or cb.ledgers:
        lg, index, _ = common.load(name, cb)
        cands = [c for c in lenses.run_all(lg, index, link.SETTING_1) if c.question_text and not c.excluded]
        prior_seeds = {sid for c in cands
                       if (" ".join(sorted(common.tokens(common.quote(c.question_text)))), c.lens) in prior_keys
                       for sid in c.seeds}
        for c in cands:
            q = common.quote(c.question_text)
            if (common.debris(q) or c.seeds & prior_seeds
                    or common.max_d1_jaccard(c, prior_tok)[0] >= common.FRESH_JACCARD):
                continue
            seed_ids = semantic.primary_probe(lg, c)[1]
            src = lg.by_id[min(seed_ids)].evidence[0].source.identifier
            question = _clean(c.question_text)
            rows.append({"ledger": name, "test_id": c.test_id, "lens": c.lens, "quote": q, "anchor": c.anchor,
                         "k_topic": len(link.breadth(lg, c.x_a)),
                         "source_origin": "owner" if cb.owner_repo in src else "outside",
                         "words": len(question.split()), "similarity": retriever.similarity(question),
                         "question_text": question})
    return rows


def review_pack(cb: codebase.Codebase, topics: list[dict]) -> str:
    prior = cb.prior_items()
    lines = [f"# {cb.title} topic review pack", ""]
    if prior:
        label = f"{cb.prior_label}'s {len(prior)} questions"
        lines += [f"Flag any topic below that shares a topic with one of {label} or with another topic below.",
                  "", f"## {label}", ""]
        lines += [f"- {cb.prior_label}-Q{it['q']}: {it['text']}" for it in prior] + [""]
    else:
        lines += ["Flag any topic below that shares a topic with another topic below.", ""]
    lines += ["## Candidate topics", ""] + [f"- {t['topic_id']}: {t['question_text']}" for t in topics]
    return "\n".join(lines) + "\n"


def pool_outputs(cb: codebase.Codebase, ledgers: list[str] | None = None) -> tuple[str, str, dict]:
    rows = pool_rows(cb, ledgers)
    topics = cluster(rows)
    summary = {"fresh_versions": len(rows), "topics": len(topics),
               "by_lens": Counter(t["lens"] for t in topics), "by_k_band": Counter(t["k_band"] for t in topics),
               "by_ledgers": Counter(t["ledgers"] for t in topics),
               "by_source_origin": Counter(t["source_origin"] for t in topics)}
    return (json.dumps({"rows": rows, "topics": topics}, indent=1, sort_keys=True) + "\n",
            review_pack(cb, topics), summary)


def _pool_path(args, cb: codebase.Codebase) -> Path:
    return Path(args.pool) if args.pool else cb.pool


def cmd_pool(args) -> int:
    cb = codebase.load(args.codebase)
    if args.ledger and not args.pool:
        raise SystemExit("a pool restricted with --ledger needs its own --pool path")
    pool_text, pack_text, summary = pool_outputs(cb, args.ledger)
    pool = _pool_path(args, cb)
    pool.write_text(pool_text)
    pack = cb.review_pack if pool == cb.pool else pool.with_suffix(".review_pack.md")
    pack.parent.mkdir(parents=True, exist_ok=True)
    pack.write_text(pack_text)
    print(json.dumps(summary, indent=1))
    return 0


def _states(arm_dirs: dict[str, Path], rows_by_version: dict, cb: codebase.Codebase) -> dict:
    from gapmap import judge as judge_mod, lenses, link, semantic

    class Replay:
        def __init__(self, model_id):
            self.model_id = model_id

        def ask(self, prompt):
            raise judge_mod.JudgeCacheMiss("replay only")

    states: dict = {}
    names = [name for name in cb.ledgers if any(v[0] == name for v in rows_by_version)]
    for arm, d in arm_dirs.items():
        for name in names:
            rec = json.loads((d / name / "judge.json").read_text())
            judge = judge_mod.CachedJudge(Replay(rec["judge_model"]), d / name / "closure_judgements.json", live=False)
            lg, index, _ = common.load(name, cb)
            for c in lenses.run_all(lg, index, link.SETTING_1):
                if (name, c.test_id) in rows_by_version:
                    states.setdefault((name, c.test_id), {})[arm] = semantic.judge_candidate(lg, index, judge, c)[0].state
    return states


def _arms(args, cb: codebase.Codebase) -> tuple[list[dict], dict, list, list]:
    pool = json.loads(_pool_path(args, cb).read_text())
    review = Path(args.review) if getattr(args, "review", None) else cb.review
    drop = set() if getattr(args, "unreviewed", False) else set(json.loads(review.read_text())["drop"])
    drop |= lexical_drops(pool["topics"])
    topics = [t for t in pool["topics"] if t["topic_id"] not in drop]
    rows_by_version = {(r["ledger"], r["test_id"]): r for r in pool["rows"]}
    arm_dirs = dict((k, Path(v)) for k, v in (a.split("=", 1) for a in args.arm))
    states = _states(arm_dirs, rows_by_version, cb)
    judges = tuple(sorted(arm_dirs))
    for t in topics:
        t["versions"] = [tuple(v) for v in t["versions"]]
    gaps = [t for t in topics if arm_of(t, states, judges) == "gap"]
    covs = [t for t in topics if arm_of(t, states, judges) == "covered"]
    return topics, states, gaps, covs


def count_summary(topics: list[dict], gaps: list[dict], covs: list[dict], *, seed: int) -> dict:
    """Stop A reads the pair count only: the top-tier closure arm can only remove topics, so the
    count is a bound, but balance is not monotone and is settled at `build`."""
    pairs = match(gaps, covs, n=max(SIZES), seed=seed)
    try:
        n, _ = choose_size(gaps, covs, seed=seed)
    except TooFew:
        n = 0
    return {"topics": len(topics), "all_open": len(gaps), "all_closed": len(covs),
            "matched_pairs_upper_bound": len(pairs), "balance_ok": balance(pairs)["ok"],
            "matched_pairs_uncapped": len(match(gaps, covs, n=len(gaps) + len(covs), seed=seed)),
            "sheet_size_reachable_now": n, "stop_at_A": len(pairs) < SIZES[-1]}


NEAR_DUPLICATE = 0.30


def lexical_drops(topics: list[dict]) -> set[str]:
    """Topics whose quoted spans reach NEAR_DUPLICATE content-word Jaccard with a lower-numbered
    topic. Reads topic text only, never a closure state, so it acts as part of the review. A
    backstop: on D1b's pool the largest pairwise Jaccard is 0.22 and it drops nothing."""
    ordered = sorted(topics, key=lambda t: t["topic_id"])
    toks = [common.tokens(common.quote(t["question_text"])) for t in ordered]
    return {ordered[j]["topic_id"] for i in range(len(ordered)) for j in range(i + 1, len(ordered))
            if common.jaccard(toks[i], toks[j]) >= NEAR_DUPLICATE}


def cmd_count(args) -> int:
    cb = codebase.load(args.codebase)
    topics, _states_, gaps, covs = _arms(args, cb)
    print(json.dumps(count_summary(topics, gaps, covs, seed=cb.seed), indent=1))
    return 0


def cmd_build(args) -> int:
    cb = codebase.load(args.codebase)
    topics, states, gaps, covs = _arms(args, cb)
    try:
        n, pairs = choose_size(gaps, covs, seed=cb.seed)
    except TooFew:
        print(json.dumps({"outcome": "Stop A (after sol)", **count_summary(topics, gaps, covs, seed=cb.seed)},
                         indent=1))
        return 3
    items = [{"arm": "gap", **g} for g, _ in pairs] + [{"arm": "covered", **c} for _, c in pairs]
    random.Random(cb.seed).shuffle(items)
    for i, it in enumerate(items, 1):
        it["q"] = i
    sheet = [f"# {cb.title} questions", "",
             "One question at a time, in chat. Answer in plain prose, from memory, without the docs or the code open.",
             "\"I don't know\" or \"this never comes up\" is a fine answer.", ""]
    for it in items:
        sheet += [f"## Q{it['q']}", "", it["question_text"], ""]
    (cb.root / "questions.md").write_text("\n".join(sheet))
    secret = cb.root / "secret"
    secret.mkdir(exist_ok=True)
    (secret / "key.json").write_text(json.dumps(
        {"seed": cb.seed, "n_per_arm": n, "items": items, "balance": balance(pairs),
         "states": {f"{k[0]}|{k[1]}": v for k, v in states.items()}}, indent=1, sort_keys=True, default=list) + "\n")
    for arm_dir in (Path(v) for v in (a.split("=", 1)[1] for a in args.arm)):
        shutil.copytree(arm_dir, secret / "arms" / arm_dir.name)
    sealed = seal(secret, Path(args.public_key).expanduser(), cb.root / "sealed")
    for arm_dir in (Path(v) for v in (a.split("=", 1)[1] for a in args.arm)):
        shutil.rmtree(arm_dir)
    bal = balance(pairs)
    print(json.dumps({"n_per_arm": n, "questions_sha256": _sha(cb.root / "questions.md"),
                      **json.loads((sealed / "sealed.sha256.json").read_text()),
                      "mean_words": bal["words"], "mean_similarity": bal["similarity"],
                      "lens_mix": Counter(it["lens"] for it in items), "eligible_open": len(gaps),
                      "eligible_closed": len(covs)}, indent=1))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="build_sheet")
    sub = p.add_subparsers(dest="cmd", required=True)
    pool = sub.add_parser("pool")
    pool.add_argument("--ledger", action="append", metavar="NAME", help="restrict the pool to these ledgers")
    for name in ("count", "build"):
        s = sub.add_parser(name)
        s.add_argument("--arm", action="append", required=True, metavar="NAME=DIR")
        if name == "build":
            s.add_argument("--public-key", required=True)
        else:
            s.add_argument("--unreviewed", action="store_true", help="count without any topic review drops")
        s.add_argument("--review", help="review file (default: fixtures/topic_review.json; A1 uses its own)")
    for s in sub.choices.values():
        s.add_argument("--codebase", default=str(codebase.D1B_CONFIG))
        s.add_argument("--pool", help="default: pool.json in the codebase's root")
    args = p.parse_args(argv)
    return {"pool": cmd_pool, "count": cmd_count, "build": cmd_build}[args.cmd](args)


if __name__ == "__main__":
    raise SystemExit(main())
