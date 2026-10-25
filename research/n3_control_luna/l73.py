"""I1b step 5: the L7.3 fixture checks of control2 run through a real judge instead of FakeJudge.

The fixture is `test_control2._three_sel`, with the planted sentence written as plain text (a real
judge does not read FakeJudge's CLOSES_HERE marker). The stand-in has the same word lengths in
random letters, keeping the two retrieval stems, for three RNG seeds.

    uv run --directory gapmap python ../research/n3_control_luna/l73.py --model gpt-5.6-luna \
        [--judge openai --max-usd 0.4]
    uv run --directory gapmap python ../research/n3_control_luna/l73.py --model qwen2.5:7b-instruct \
        [--judge ollama]
"""
import argparse
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "gapmap/tests"))
from conftest import a_claim, fillers, ledger  # noqa: E402

from gapmap import control2, judge as judge_mod, lenses, link  # noqa: E402

PLANTED = "When an intermittent fault appears, choose first the test whose failure likelihood is highest."
KEEP = {"failure", "likelihood"}
STAND_IN_SEEDS = (7, 8, 9)


def stand_in(sentence: str, seed: int) -> str:
    rng = random.Random(seed)
    letters = "abcdefghijklmnopqrstuvwxyz"
    return " ".join(w if w.strip(".,:").lower() in KEEP else "".join(rng.choice(letters) for _ in w)
                    for w in sentence.split())


def fixture(planted: str):
    seed_i = a_claim("Diagnostic tests should be selected based on failure likelihood.",
                     source_id="s-i", independence_key="k-i")
    foreign_i = a_claim("Selection practice for failure likelihood is documented.",
                        exact=planted, source_id="s-i-f", independence_key="k-i-f")
    seed_j = a_claim("Sampling rate should be selected based on the suspected event.",
                     source_id="s-j", independence_key="k-j")
    foreign_j = a_claim("Sampling rate selection practice is documented for the suspected event.",
                        source_id="s-j-f", independence_key="k-j-f")
    seed_k = a_claim("Sampling interval should be selected based on the suspected event.",
                     source_id="s-k", independence_key="k-k")
    foreign_k = a_claim("Sampling interval selection guidance is documented for the suspected event.",
                        source_id="s-k-f", independence_key="k-k-f")
    lg = ledger([seed_i, foreign_i, seed_j, foreign_j, seed_k, foreign_k, *fillers(40)])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    assert len(cands) == 3
    return lg, idx, cands, seed_i.claim_id


def check(judge, planted: str) -> dict:
    lg, idx, cands, target = fixture(planted)
    specs = control2.build_pairs(lg, idx, cands)
    pairs = control2.judge_pairs(specs, judge)
    spec = next(s for s in specs if target in s.seeds)
    pair = next(p for p in pairs if target in p.seeds)
    summary = control2.summarise(pairs, b=200)["by_lens"]["SEL"]
    return {"planted_text": planted, "k": pair.k,
            "own_other_lengths": sorted(len(r[2]) for r in spec.own_other),
            "target_states": pair.states,
            "fires_seed_free": pair.states["own_sf"] == "closed" and pair.states["ctrl_sf"] != "closed",
            "fires_equal_cap": pair.states["own_eq"] == "closed" and pair.states["ctrl_eq"] != "closed",
            "diff_seed_free_closed": summary["seed_free"]["closed"]["diff"],
            "diff_equal_cap_closed": summary["equal_cap"]["closed"]["diff"],
            "all_pairs": [{"seeds": p.seeds, "states": p.states} for p in pairs]}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--judge", choices=["ollama", "openai"])
    ap.add_argument("--max-usd", type=float)
    args = ap.parse_args()
    use_openai = args.model in judge_mod.OPENAI_PRICES_PER_MTOK
    if use_openai:
        if args.judge == "openai" and args.max_usd is None:
            ap.error("--judge openai needs --max-usd")
        backend = judge_mod.OpenAIJudge(args.model, max_usd=args.max_usd or 0.0)
        meta = {"model": args.model, **backend.settings}
    else:
        backend, meta = judge_mod.OllamaJudge(model=args.model), None
    tag = "luna" if use_openai else "qwen"
    out = HERE / "l73"
    out.mkdir(exist_ok=True)
    judge = judge_mod.CachedJudge(backend, out / f"closure_judgements_{tag}.json",
                                  live=args.judge is not None, meta=meta)
    try:
        planted = check(judge, PLANTED)
        stand_ins = [{"rng_seed": s, **check(judge, stand_in(PLANTED, s))} for s in STAND_IN_SEEDS]
    finally:
        judge.save()
    result = {"judge_model": backend.model_id, "judge_settings": meta, "planted": planted,
              "stand_ins": stand_ins,
              "planted_fires": planted["fires_seed_free"],
              "stand_in_fires": any(s["fires_seed_free"] or s["diff_seed_free_closed"] > 0 for s in stand_ins)}
    if use_openai:
        result["spend"] = backend.spend()
    (out / f"l73_{tag}.json").write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")
    print(json.dumps({k: result[k] for k in ("planted_fires", "stand_in_fires")}))


if __name__ == "__main__":
    main()
