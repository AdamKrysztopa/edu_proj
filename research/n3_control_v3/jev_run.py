"""I2 step 5: Jev as control2's judge, on the L7.3 fixtures (twice) and, only if eligible both
times with identical states, on the three domains. Jev's top-tier arm is sol's cached run on the
same pairs (equal `pairs_sha256`).

Cache rule: the JEV spike's raw cache first, then this run's; live only for misses; a miss on a
prompt the old control issued (`research/spikes/jev/judge_prompts.json`) stops the run. The L7.3
retest reads no earlier cache, so it re-asks every prompt. One ledger, `jev/jev_spend.jsonl`,
carries every call, so `--max-usd` covers all of this item's Jev runs together.

    uv run --directory gapmap python ../research/n3_control_v3/jev_run.py check
    uv run --directory gapmap python ../research/n3_control_v3/jev_run.py l73 {run1|retest} [--live --max-usd 0.10]
    uv run --directory gapmap python ../research/n3_control_v3/jev_run.py domains [--live --max-usd 0.10]
"""
import argparse
import dataclasses
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
import l73  # noqa: E402

from gapmap import control2, jev, judge as judge_mod, lenses, link  # noqa: E402
from gapmap.__main__ import _admissibility_note  # noqa: E402
from residual.ledger import Ledger  # noqa: E402

OUT = HERE / "jev"
SPIKE = ROOT / "research/spikes/jev"
LEDGER = OUT / "jev_spend.jsonl"
L73_DIRS = {"run1": OUT / "l73", "retest": OUT / "l73_retest"}
DOMAINS = {"plc": ("PLC intermittent-fault diagnosis", "20260928T133336Z-59ec876b3d7e"),
           "gdpr_v1": ("GDPR DPIA (run v1)", "20260928T135354Z-eb840a85b7d1"),
           "gdpr_v2": ("GDPR DPIA (run v2)", "20260928T145943Z-bc1cc9a30a02")}


def issued_prompts() -> dict[str, str]:
    """Prompts the spike sent to Jev: those whose stored qwen answer parsed (`judge_swap.usable`)."""
    entries = json.loads((SPIKE / "judge_prompts.json").read_text())
    return {hashlib.sha256(e["prompt"].encode()).hexdigest(): e["prompt"] for e in entries.values()
            if isinstance(e["qwen"], dict) and jev.parse_prompt(e["prompt"])[2]}


def cmd_check() -> None:
    issued = issued_prompts()
    keys = {jev.body_key(jev.request_body(p)) for p in issued.values()}
    hit = sum((SPIKE / "cache" / f"{k}.json").exists() for k in keys)
    top_is_argmax = total = 0
    for k in keys:
        f = SPIKE / "cache" / f"{k}.json"
        if f.exists():
            for a in json.loads(f.read_text())["response"]["answers"].values():
                total += 1
                top_is_argmax += a["choice"] == max(a["probabilities"], key=a["probabilities"].get)
    print(json.dumps({"issued_prompts": len(issued), "unique_bodies": len(keys), "cached": hit,
                      "answers": total, "choice_is_argmax": top_is_argmax}))
    if hit != len(keys):
        raise SystemExit("the spike cache misses a body the old control issued")


def make_judge(raw_dir: Path, closure_cache: Path, args, prior=(SPIKE / "cache",)):
    backend = jev.JevJudge(max_usd=args.max_usd or 0.0, cache_dir=raw_dir, spend_ledger=LEDGER,
                           prior_cache_dirs=prior, issued_prompt_sha256s=set(issued_prompts()),
                           live=args.live)
    return backend, judge_mod.CachedJudge(backend, closure_cache, live=args.live, meta={"model": jev.MODEL},
                                          live_flag="jev_run.py --live")


def recorded_spend(path: Path, backend, args) -> dict:
    """An offline replay makes no call, so it keeps the spend the live run recorded."""
    if not args.live and path.exists():
        return json.loads(path.read_text())["spend"]
    return backend.spend()


def cmd_l73(args) -> None:
    out = L73_DIRS[args.run]
    prior = (SPIKE / "cache",) if args.run == "run1" else ()
    backend, judge = make_judge(out / "raw", out / "closure_judgements.json", args, prior)
    try:
        result = {"judge_model": jev.MODEL, "judge_settings": None, **l73.evaluate(judge)}
    finally:
        judge.save()
    result["spend"] = recorded_spend(out / "l73.json", backend, args)
    (out / "l73.json").write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")
    print(json.dumps({k: result[k] for k in ("planted_fires", "stand_in_fires", "eligible")}))


def target_states(result: dict) -> dict:
    return {t: {name: row["target_states"] for name, row in rows.items()} for t, rows in result["topics"].items()}


def eligible_twice() -> tuple[bool, str]:
    runs = {r: json.loads((d / "l73.json").read_text()) for r, d in L73_DIRS.items() if (d / "l73.json").exists()}
    if len(runs) < 2:
        return False, "L7.3 has not run twice"
    if not all(r["eligible"] for r in runs.values()):
        return False, "Jev fails L7.3 in at least one run"
    if target_states(runs["run1"]) != target_states(runs["retest"]):
        return False, "Jev's L7.3 states differ between runs"
    return True, "eligible in both runs with identical states"


def cmd_domains(args) -> None:
    ok, why = eligible_twice()
    if not ok:
        raise SystemExit(f"not running the domains: {why}")
    for d, (name, run) in DOMAINS.items():
        ledger_text = (ROOT / "reconstruct/runs" / run / "ledger.json").read_text()
        ledger = Ledger.from_json(ledger_text)
        sidecar = json.loads((ROOT / "reconstruct/runs" / run / "sidecar.json").read_text())
        index = link.build_index(ledger)
        specs = control2.build_pairs(ledger, index, lenses.run_all(ledger, index, link.SETTING_1))
        out = OUT / d
        backend, judge = make_judge(OUT / "raw", out / "closure_judgements.json", args)
        note = _admissibility_note(ledger, sidecar)
        result = {"domain": name, "ledger_sha256": hashlib.sha256(ledger_text.encode()).hexdigest(),
                  "judge_model": jev.MODEL, "primary": list(control2.PRIMARY),
                  "bootstrap": {"b": control2.BOOTSTRAP_B, "seed": control2.BOOTSTRAP_SEED,
                                "cluster": "min seed claim id"},
                  "admissible": note is None, "admissibility_note": note,
                  "pairs_sha256": control2.pairs_sha256(specs)}
        try:
            pairs = control2.judge_pairs(specs, judge)
        finally:
            judge.save()
        result.update(complete=True, spend=recorded_spend(out / "control2.json", backend, args),
                      summary=control2.summarise(pairs),
                      length_stand_in=control2.length_stand_in(specs),
                      length_matched=control2.length_matched(specs, pairs),
                      pairs=[dataclasses.asdict(p) for p in pairs])
        out.mkdir(parents=True, exist_ok=True)
        (out / "control2.json").write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")
        print(d, json.dumps(result["summary"]["total"]["seed_free"]["closed"]), json.dumps(result["spend"]))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["check", "l73", "domains"])
    ap.add_argument("run", nargs="?", choices=list(L73_DIRS))
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--max-usd", type=float)
    args = ap.parse_args()
    if args.live and args.max_usd is None:
        ap.error("--live needs --max-usd")
    if args.cmd == "check":
        cmd_check()
    elif args.cmd == "l73":
        if args.run is None:
            ap.error("l73 needs run1 or retest")
        cmd_l73(args)
    else:
        cmd_domains(args)


if __name__ == "__main__":
    main()
