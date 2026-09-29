"""JEV spike, part 2: can one Jev call do the N3 closure judge's LLM call, and at what cost?

First reference: the committed qwen2.5:7b-instruct answer cache (research/n3/*/closure_judgements.json);
its rule (RULE) failed. Because that judge is itself uninformative, a strong-model reference on a
random sample was then added (REF_*), and finally local qwen was rerun with Jev's own instructions
(SAME_PROMPT_RULE) to separate the model from the prompt. None of the references is ground truth.

    uv run --project gapmap python research/spikes/jev/judge_swap.py prompts   # offline replay
    uv run --project gapmap python research/spikes/jev/judge_swap.py run       # Jev calls, cached
    uv run --project gapmap python research/spikes/jev/judge_swap.py analyse
"""
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE))
import spike  # noqa: E402  (cache, budget, headroom and HTTP helpers)

RUNS = ROOT / "reconstruct/runs"
DOMAINS = {  # args as committed for research/n3/<domain>
    "plc": ("20260928T133336Z-59ec876b3d7e", None),
    "gdpr_v1": ("20260928T135354Z-eb840a85b7d1", "20260928T145943Z-bc1cc9a30a02"),
    "gdpr_v2": ("20260928T145943Z-bc1cc9a30a02", "20260928T135354Z-eb840a85b7d1"),
}
PROMPTS = HERE / "judge_prompts.json"
LEVELS = {
    "states": "The sentence explicitly states the element the question asks for.",
    "partially": "The sentence states part of the element, or states it only implicitly.",
    "no": "The sentence does not state the element; being on the same topic is not enough.",
}
# Registered before any Jev judge call: Cohen's kappa vs the cached qwen answers.
RULE = {"substitutes_if_kappa_at_least": 0.60, "does_not_if_kappa_below": 0.40}


def cmd_prompts():
    from gapmap import judge as judge_mod
    from gapmap.__main__ import build_gapmap
    from residual.ledger import Ledger

    class Recording(judge_mod.CachedJudge):
        seen: dict = {}

        def ask(self, prompt):
            ans = super().ask(prompt)
            self.seen[judge_mod.cache_key(self.model_id, prompt)] = {"prompt": prompt, "qwen": ans}
            return ans

    out = {}
    for domain, (run, sib) in DOMAINS.items():
        cache = ROOT / f"research/n3/{domain}/closure_judgements.json"
        j = Recording(judge_mod.OllamaJudge(), cache, live=False)
        Recording.seen = {}
        text = (RUNS / run / "ledger.json").read_text()
        build_gapmap(Ledger.from_json(text), domain=domain, judge=j,
                     sidecar=json.loads((RUNS / run / "sidecar.json").read_text()),
                     sibling=Ledger.from_json((RUNS / sib / "ledger.json").read_text()) if sib else None,
                     ledger_text=text)
        n_cache = len(json.loads(cache.read_text()))
        print(f"{domain}: {len(Recording.seen)} prompts recovered of {n_cache} cache entries")
        for k, v in Recording.seen.items():
            out[f"{domain}:{k}"] = v
    PROMPTS.write_text(json.dumps(out, indent=1, sort_keys=True))


def parse_prompt(prompt):
    seed = re.search(r'^Seed assertion: "(.*)"$', prompt, re.M).group(1)
    question = re.search(r"^Question: (.*)$", prompt, re.M).group(1)
    body = prompt.split("\nSentences:\n", 1)[1].split("\n\nRespond as JSON only", 1)[0]
    sents = {}
    for line in body.split("\n"):
        m = re.match(r"^(\d+): (.*)$", line)
        if m:
            sents[m.group(1)] = m.group(2)
        elif sents:  # a sentence containing a newline continues the previous id
            last = next(reversed(sents))
            sents[last] += "\n" + line
    return seed, question, sents


def jev_body(prompt):
    seed, question, sents = parse_prompt(prompt)
    questions = {
        f"s{i}": {
            "type": "choice",
            "instructions": (f"Question about the seed assertion: {question} "
                             f"Does sentences[\"{i}\"] state the element this question asks for?"),
            "criteria": LEVELS,
        }
        for i in sents
    }
    return {"model": spike.MODEL, "state": {"seed_assertion": seed, "sentences": sents},
            "questions": questions}


def usable(entries):
    """Qwen answers the N3 parser could read; unreadable ones are counted, never defaulted."""
    ok, bad = {}, 0
    for k, e in entries.items():
        q = e["qwen"]
        if not isinstance(q, dict) or not parse_prompt(e["prompt"])[2]:
            bad += 1
            continue
        ok[k] = e
    return ok, bad


def cmd_run():
    entries, bad = usable(json.loads(PROMPTS.read_text()))
    bodies = {spike.cache_key(b): b for b in (jev_body(e["prompt"]) for e in entries.values())}
    pending = {k: b for k, b in bodies.items() if not spike.cache_path(k).exists()}
    est = sum(spike.est_tokens(b) for b in pending.values()) / 1e6 * spike.PRICE_PER_M_INPUT
    print(f"{len(entries)} usable prompts ({bad} unreadable qwen answers excluded); "
          f"{len(pending)} uncached Jev calls, est ${est:.4f}")
    if not pending:
        return
    key = spike.get_api_key()
    spike.require_key_headroom(key, est)
    spent, _ = spike.cached_cost_sum()
    if spent + est > spike.HARD_CAP_USD:
        sys.exit(f"hard cap ${spike.HARD_CAP_USD} would be exceeded (spent ${spent:.4f} + est ${est:.4f})")

    def one(item):
        k, b = item
        status, resp = spike.call_api(b, key)
        if status != 200 or resp is None:
            raise RuntimeError(f"HTTP {status}")
        missing = [q for q in b["questions"] if not resp.get("answers", {}).get(q, {}).get("choice")]
        if missing:
            raise RuntimeError(f"unparsed choice for {missing[:3]}")
        spike.cache_path(k).write_text(json.dumps({"request": b, "response": resp}, indent=2))

    with ThreadPoolExecutor(8) as pool:
        list(pool.map(one, pending.items()))
    print(f"cumulative cost over all cached calls = ${spike.cached_cost_sum()[0]:.4f}")


def kappa(a, b):
    labels = sorted(set(a) | set(b))
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(l) / n) * (b.count(l) / n) for l in labels)
    return (po - pe) / (1 - pe) if pe < 1 else float("nan")


def cmd_analyse():
    entries, bad = usable(json.loads(PROMPTS.read_text()))
    sent_q, sent_j, sent_jp, call_q, call_j = [], [], [], [], []
    per_domain = {}
    jev_cost = jev_in = 0.0
    for k, e in entries.items():
        body = jev_body(e["prompt"])
        resp = json.loads(spike.cache_path(spike.cache_key(body)).read_text())["response"]
        jev_cost += resp["usage"]["cost"]
        jev_in += resp["usage"]["input_tokens"]
        st = {str(x) for x in (e["qwen"].get("states") or [])}
        pa = {str(x) for x in (e["qwen"].get("partially") or [])} - st
        any_q, any_j = "no", "no"
        for qid, ans in resp["answers"].items():
            i = qid[1:]
            q = "states" if i in st else "partially" if i in pa else "no"
            j = ans["choice"]
            sent_q.append(q), sent_j.append(j)
            sent_jp.append(ans["probabilities"].get("states", 0) + ans["probabilities"].get("partially", 0))
            any_q = "states" if q == "states" or any_q == "states" else ("partially" if q == "partially" else any_q)
            any_j = "states" if j == "states" or any_j == "states" else ("partially" if j == "partially" else any_j)
        call_q.append(any_q), call_j.append(any_j)
        d = per_domain.setdefault(k.split(":")[0], ([], []))
        d[0].append(any_q), d[1].append(any_j)

    binar = lambda xs: ["hit" if x != "no" else "no" for x in xs]  # noqa: E731
    qwen_prompt_tokens = sum(len(e["prompt"]) for e in entries.values()) / 4  # ~4 chars/token
    qwen_out_tokens = 40 * len(entries)
    result = {
        "rule": RULE,
        "n_prompts": len(entries), "n_unreadable_qwen_excluded": bad, "n_sentences": len(sent_q),
        "sentence_kappa_3way": kappa(sent_q, sent_j),
        "sentence_kappa_hit_vs_no": kappa(binar(sent_q), binar(sent_j)),
        "sentence_agreement_hit_vs_no": sum(a == b for a, b in zip(binar(sent_q), binar(sent_j))) / len(sent_q),
        "prompt_kappa_closed_state": kappa(call_q, call_j),
        "prompt_kappa_any_hit": kappa(binar(call_q), binar(call_j)),
        "prompt_kappa_any_hit_by_domain": {d: kappa(binar(a), binar(b)) for d, (a, b) in per_domain.items()},
        "qwen_label_rates": {l: sent_q.count(l) / len(sent_q) for l in LEVELS},
        "jev_label_rates": {l: sent_j.count(l) / len(sent_j) for l in LEVELS},
        "prompt_state_rates_qwen": {l: call_q.count(l) / len(call_q) for l in LEVELS},
        "prompt_state_rates_jev": {l: call_j.count(l) / len(call_j) for l in LEVELS},
        "jev_cost_usd": jev_cost, "jev_input_tokens": jev_in,
        "qwen_est_tokens_in_out": [qwen_prompt_tokens, qwen_out_tokens],
    }
    k = result["sentence_kappa_hit_vs_no"]
    result["verdict"] = ("substitutes" if k >= RULE["substitutes_if_kappa_at_least"]
                         else "does not substitute" if k < RULE["does_not_if_kappa_below"] else "partial")
    (HERE / "analysis_judge_swap.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


# The qwen judge is itself uninformative against its fair control (report 10_n3.tex), so
# agreement with it cannot decide substitution. A strong reference answers a random sample of
# the identical prompts; both cheap judges are scored against it. Registered before any call.
REF_MODEL = "anthropic/claude-sonnet-5.5"  # Opus 5.5 refuses reasoning off; its worst case breaks the cap
REF_PRICE_IN, REF_PRICE_OUT, REF_MAX_OUT = 2.0, 10.0, 1500
REF_N = 100
REF_RULE = {"substitutes_if_jev_minus_qwen_kappa_at_least": -0.05,
            "does_not_if_jev_minus_qwen_kappa_below": -0.15}
HOSTED_QWEN_PRICE_IN, HOSTED_QWEN_PRICE_OUT = 0.10, 0.20  # qwen/qwen-2.5-7b-instruct on OpenRouter


def ref_sample(entries):
    import random
    by_prompt = {}
    for k in sorted(entries):
        by_prompt.setdefault(entries[k]["prompt"], k)
    keys = sorted(by_prompt.values())
    return random.Random(0).sample(keys, REF_N)


def ref_body(prompt):
    return {"model": REF_MODEL, "messages": [{"role": "user", "content": prompt}],
            "temperature": 0, "max_tokens": REF_MAX_OUT, "usage": {"include": True},
            "reasoning": {"effort": "low"}}


def parse_ref(resp):
    text = resp["choices"][0]["message"]["content"] or ""
    m = re.search(r"\{.*\}", text, re.S)
    try:
        d = json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        d = None
    return d if isinstance(d, dict) else None


def call_chat(body, api_key):
    import urllib.error
    import urllib.request
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    import time
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 5:
                time.sleep(2 ** attempt)
                continue
            raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')[:300]}")


def cmd_reference():
    entries, _ = usable(json.loads(PROMPTS.read_text()))
    sample = ref_sample(entries)
    pending = {spike.cache_key(b): b for b in (ref_body(entries[k]["prompt"]) for k in sample)
               if not spike.cache_path(spike.cache_key(b)).exists()}
    est = sum(spike.est_tokens(b) * REF_PRICE_IN + REF_MAX_OUT * REF_PRICE_OUT for b in pending.values()) / 1e6
    print(f"reference {REF_MODEL}: {len(pending)} uncached calls, worst-case est ${est:.3f}")
    if not pending:
        return
    key = spike.get_api_key()
    spike.require_key_headroom(key, est)
    spent, _ = spike.cached_cost_sum()
    if spent + est > spike.HARD_CAP_USD:
        sys.exit(f"hard cap ${spike.HARD_CAP_USD} would be exceeded (spent ${spent:.4f} + est ${est:.3f})")

    def one(item):
        k, b = item
        resp = call_chat(b, key)
        if "usage" not in resp or "cost" not in resp["usage"]:
            raise RuntimeError("response carries no usage.cost; cannot account for spend")
        spike.cache_path(k).write_text(json.dumps({"request": b, "response": resp}, indent=2))

    with ThreadPoolExecutor(4) as pool:
        list(pool.map(one, pending.items()))
    print(f"cumulative cost over all cached calls = ${spike.cached_cost_sum()[0]:.4f}")


def _hits(ans, ids):
    st = {str(x) for x in (ans.get("states") or [])}
    pa = {str(x) for x in (ans.get("partially") or [])} - st
    return {i: ("states" if i in st else "partially" if i in pa else "no") for i in ids}


def cmd_compare():
    import numpy as np
    entries, _ = usable(json.loads(PROMPTS.read_text()))
    rows, unreadable, ref_cost, ref_in, ref_out = [], 0, 0.0, 0, 0
    jev_cost_sample = qwen_hosted = 0.0
    for k in ref_sample(entries):
        e = entries[k]
        rb = ref_body(e["prompt"])
        rresp = json.loads(spike.cache_path(spike.cache_key(rb)).read_text())["response"]
        ref_cost += rresp["usage"]["cost"]
        ref_in += rresp["usage"]["prompt_tokens"]
        ref_out += rresp["usage"]["completion_tokens"]
        ref = parse_ref(rresp)
        jb = jev_body(e["prompt"])
        jresp = json.loads(spike.cache_path(spike.cache_key(jb)).read_text())["response"]
        jev_cost_sample += jresp["usage"]["cost"]
        qwen_hosted += (rresp["usage"]["prompt_tokens"] * HOSTED_QWEN_PRICE_IN + 40 * HOSTED_QWEN_PRICE_OUT) / 1e6
        if ref is None:
            unreadable += 1
            continue
        ids = list(jb["questions"])
        ids = [i[1:] for i in ids]
        r, q = _hits(ref, ids), _hits(e["qwen"], ids)
        j = {qid[1:]: a["choice"] for qid, a in jresp["answers"].items()}
        rows.append([(r[i], q[i], j[i]) for i in ids])

    def kap(pairs, bin_):
        f = (lambda x: "hit" if x != "no" else "no") if bin_ == "hit" else (lambda x: "states" if x == "states" else "not")
        return kappa([f(a) for a, _ in pairs], [f(b) for _, b in pairs])

    def scores(rs):
        flat = [t for p in rs for t in p]
        out = {}
        for b in ("hit", "states"):
            out[b] = {"jev_ref": kap([(r, j) for r, _, j in flat], b),
                      "qwen_ref": kap([(r, q) for r, q, _ in flat], b),
                      "jev_qwen": kap([(q, j) for _, q, j in flat], b)}
        pr = lambda idx: [("hit" if any(t[0 if idx == "r" else 1 if idx == "q" else 2] != "no" for t in p) else "no") for p in rs]  # noqa: E731
        out["prompt_any_hit"] = {"jev_ref": kappa(pr("r"), pr("j")), "qwen_ref": kappa(pr("r"), pr("q"))}
        return out

    s = scores(rows)
    rng = np.random.default_rng(0)
    diffs = []
    for _ in range(2000):
        bs = [rows[i] for i in rng.integers(0, len(rows), len(rows))]
        sb = scores(bs)["hit"]
        diffs.append(sb["jev_ref"] - sb["qwen_ref"])
    diff = s["hit"]["jev_ref"] - s["hit"]["qwen_ref"]
    verdict = ("substitutes" if diff >= REF_RULE["substitutes_if_jev_minus_qwen_kappa_at_least"]
               else "does not substitute" if diff < REF_RULE["does_not_if_jev_minus_qwen_kappa_below"] else "partial")
    result = {
        "reference": REF_MODEL, "rule": REF_RULE, "n_sampled": REF_N, "n_ref_unreadable_excluded": unreadable,
        "n_prompts_scored": len(rows), "n_sentences": sum(len(p) for p in rows),
        "kappa": s, "jev_minus_qwen_hit_kappa": diff,
        "jev_minus_qwen_ci95": [float(np.percentile(diffs, 2.5)), float(np.percentile(diffs, 97.5))],
        "cost_per_judgement_usd": {"jev": jev_cost_sample / REF_N, "reference": ref_cost / REF_N,
                                   "hosted_qwen_2.5_7b_est": qwen_hosted / REF_N},
        "ref_tokens_in_out": [ref_in, ref_out],
        "verdict": verdict,
    }
    (HERE / "analysis_reference.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


# Review fix: Jev got new per-sentence three-level criteria while qwen kept the original prompt.
# Same instructions to local qwen isolate the model from the prompt. Registered before any call.
SAME_PROMPT_RULE = {"gain_is_prompt_if_qwen_within": 0.05, "gain_is_jev_if_qwen_below_by": 0.15}


def qwen_same_body(jev_b, qid):
    q = jev_b["questions"][qid]
    options = "\n".join(f'- "{k}": {v}' for k, v in q["criteria"].items())
    prompt = (f"State:\n{json.dumps(jev_b['state'], ensure_ascii=False, indent=1)}\n\n"
              f"Question: {q['instructions']}\n\nOptions:\n{options}\n\n"
              'Respond as JSON only: {"choice": "states" | "partially" | "no"}.')
    return {"model": "qwen/qwen-2.5-7b-instruct", "messages": [{"role": "user", "content": prompt}],
            "temperature": 0, "seed": 0, "max_tokens": 30, "usage": {"include": True}}


def cmd_qwen_same():
    entries, _ = usable(json.loads(PROMPTS.read_text()))
    items = []
    for k in ref_sample(entries):
        jb = jev_body(entries[k]["prompt"])
        items += [qwen_same_body(jb, qid) for qid in jb["questions"]]
    pending = {spike.cache_key(b): b for b in items if not spike.cache_path(spike.cache_key(b)).exists()}
    est = sum(spike.est_tokens(b) * HOSTED_QWEN_PRICE_IN + 30 * HOSTED_QWEN_PRICE_OUT for b in pending.values()) / 1e6
    print(f"hosted qwen-2.5-7b, same instructions as Jev: {len(pending)} of {len(items)} calls uncached, est ${est:.3f}")
    if not pending:
        return
    key = spike.get_api_key()
    spike.require_key_headroom(key, est)
    spent, _ = spike.cached_cost_sum()
    if spent + est > spike.HARD_CAP_USD:
        sys.exit(f"hard cap ${spike.HARD_CAP_USD} would be exceeded (spent ${spent:.4f} + est ${est:.3f})")

    def one(item):
        k, b = item
        resp = call_chat(b, key)
        if "usage" not in resp or "cost" not in resp["usage"]:
            raise RuntimeError("response carries no usage.cost; cannot account for spend")
        spike.cache_path(k).write_text(json.dumps({"request": b, "response": resp}, indent=2))

    with ThreadPoolExecutor(6) as pool:
        list(pool.map(one, pending.items()))
    print(f"cumulative cost over all cached calls = ${spike.cached_cost_sum()[0]:.4f}")


def cmd_compare_same():
    entries, _ = usable(json.loads(PROMPTS.read_text()))
    ref_l, jev_l, qs_l, unreadable = [], [], [], 0
    for k in ref_sample(entries):
        e = entries[k]
        ref = parse_ref(json.loads(spike.cache_path(spike.cache_key(ref_body(e["prompt"]))).read_text())["response"])
        jb = jev_body(e["prompt"])
        jresp = json.loads(spike.cache_path(spike.cache_key(jb)).read_text())["response"]
        r = _hits(ref, [q[1:] for q in jb["questions"]])
        for qid in jb["questions"]:
            raw = json.loads(spike.cache_path(spike.cache_key(qwen_same_body(jb, qid))).read_text())["response"]
            parsed = parse_ref(raw)
            choice = parsed.get("choice") if parsed else None
            if choice not in LEVELS:
                unreadable += 1
                continue
            ref_l.append(r[qid[1:]]), jev_l.append(jresp["answers"][qid]["choice"]), qs_l.append(choice)
    hit = lambda xs: ["hit" if x != "no" else "no" for x in xs]  # noqa: E731
    k_jev, k_qs = kappa(hit(ref_l), hit(jev_l)), kappa(hit(ref_l), hit(qs_l))
    gap = k_jev - k_qs
    verdict = ("gain is the prompt" if gap <= SAME_PROMPT_RULE["gain_is_prompt_if_qwen_within"]
               else "gain is Jev's" if gap >= SAME_PROMPT_RULE["gain_is_jev_if_qwen_below_by"] else "mixed")
    result = {"rule": SAME_PROMPT_RULE, "n_sentences_scored": len(ref_l), "n_qwen_unreadable_excluded": unreadable,
              "kappa_hit_vs_sonnet": {"jev": k_jev, "qwen_same_prompt": k_qs},
              "kappa_3way_vs_sonnet": {"jev": kappa(ref_l, jev_l), "qwen_same_prompt": kappa(ref_l, qs_l)},
              "qwen_same_label_rates": {l: qs_l.count(l) / len(qs_l) for l in LEVELS},
              "jev_minus_qwen_same": gap, "verdict": verdict}
    (HERE / "analysis_same_prompt.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    if sys.argv[1] in ("qwen-same", "compare-same"):
        {"qwen-same": cmd_qwen_same, "compare-same": cmd_compare_same}[sys.argv[1]]()
        sys.exit()
    {"prompts": cmd_prompts, "run": cmd_run, "analyse": cmd_analyse,
     "reference": cmd_reference, "compare": cmd_compare}[sys.argv[1]]()
