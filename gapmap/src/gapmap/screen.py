"""Judge screening, N3's standard way to choose a closure judge (`docs/plans/judge-screening-standard.md`,
ADR 0010). It runs D1b's checks in a fixed order through their committed runners, rules unchanged:

    S0 fixtures      $0    research/d1b_rerun/g2.py --stand-ins --split gate: no stand-in passes, the P oracle does
    S1 parallel arm  $0    a same-family candidate waits for an eligible other-family one (ADR 0009)
    G1               paid  research/d1b_rerun/g1.py (N3 L7.3 fixtures), 1 passing run
    G2               paid  research/d1b_rerun/g2.py --split gate, 2 passing runs

    uv run --directory gapmap python -m gapmap.screen status --candidate SLUG
    uv run --directory gapmap python -m gapmap.screen run --candidate SLUG --model M \
        [--reasoning-effort E | --reasoning-max-tokens N] [--live --max-usd X --spend-ledger F] \
        [--after GATE.json] [--owner-note TEXT]
    uv run --directory gapmap python -m gapmap.screen adopt --candidate SLUG --model M [...] \
        --step G1|G2 --from DIR --note TEXT
    uv run --directory gapmap python -m gapmap.screen pair --cheap SLUG --top SLUG

A paid run starts only after every earlier step is satisfied, at most one per invocation and one
per spend ledger at a time, each in a new directory (an empty closure cache). A complete failing
run puts the model out for this sequence, under any fixture hash and any slug. `verdict.json`
records eligibility only after the required passes under the current fixture hash."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from gapmap import judge as judge_mod

ROOT = Path(__file__).resolve().parents[3]
SEQUENCE = "screen-v1"
G2_RULE = "g2.passes as committed, R scored as R_excess (owner amendment 2026-10-26)"
SCREEN_DIR = Path("research/judge_screening")
LOCK = ".lock"
TOP_TIER = frozenset({"gpt-6.1-sol"})
# Generator and verifier families of the N2 and D1 ledgers a closure judge is used on.
TARGET_LEDGER_FAMILIES = frozenset({"anthropic", "openai"})
G1_SCRIPT = Path("research/d1b_rerun/g1.py")
G2_SCRIPT = Path("research/d1b_rerun/g2.py")
KEY_HEADROOM = Path("scripts/key_headroom.py")
# What decides a judgement: fixtures, prompt building, reply parsing, stand-ins and the rules.
# judge.py (prices, transport) and g1.py (argument routing) are left out so adding a candidate's
# price or a flag does not void every verdict.
FIXTURE_FILES = (
    Path("research/d1b_rerun/fixtures/topics.json"),
    Path("research/d1b_rerun/fixtures/inserts.json"),
    Path("research/d1b_rerun/fixtures/confirmations.json"),
    G2_SCRIPT,
    Path("research/n3_control_v3/l73.py"),
    Path("gapmap/tests/l73_fixtures.py"),
    Path("gapmap/tests/conftest.py"),
    Path("gapmap/src/gapmap/semantic.py"),
    Path("gapmap/src/gapmap/standins.py"),
    Path("gapmap/src/gapmap/control2.py"),
    Path("gapmap/src/gapmap/text.py"),
    Path("gapmap/src/gapmap/config.py"),
)
STEPS = ("S0", "S1", "G1", "G2")
REQUIRED = {"S0": 1, "S1": 1, "G1": 1, "G2": 2}
PAID = frozenset({"G1", "G2"})
# l73.py rules on the seed-free arms only and reads an unanswered call there as "not closed"; as
# G2 rules, an undecided arm makes the run incomplete instead.
G1_RULED_ARMS = ("own_sf", "ctrl_sf")
FREE_INCOMPLETE_RETRIES = 1

Runner = Callable[[list[str], Path], int]
Headroom = Callable[[str, float], tuple[bool, str]]


class Refused(RuntimeError):
    pass


def _subprocess_runner(argv: list[str], cwd: Path) -> int:
    return subprocess.run(argv, cwd=cwd).returncode


def _key_headroom(root: Path) -> Headroom:
    def check(provider: str, need: float) -> tuple[bool, str]:
        if provider != "openrouter":
            return True, "unreadable for this provider; the owner's stated balance applies"
        p = subprocess.run([sys.executable, str(root / KEY_HEADROOM), "--need", f"{need:.4f}"],
                           capture_output=True, text=True)
        return p.returncode == 0, (p.stdout + p.stderr).strip()
    return check


def fixture_hash(root: Path) -> str:
    h = hashlib.sha256()
    for rel in FIXTURE_FILES:
        h.update(str(rel).encode() + b"\0" + hashlib.sha256((root / rel).read_bytes()).digest())
    return h.hexdigest()


def candidate_record(cand: dict) -> dict:
    model = cand["model"]
    if model in judge_mod.OPENAI_PRICES_PER_MTOK:
        provider, settings = "openai", {"reasoning_effort": cand.get("reasoning_effort") or "medium"}
    elif model in judge_mod.OPENROUTER_PRICES_PER_MTOK:
        provider, settings = "openrouter", {"reasoning_max_tokens": cand.get("reasoning_max_tokens")}
    else:
        raise Refused(f"no recorded price for {model!r} in gapmap.judge; add it before screening")
    return {"model": model, "provider": provider, "family": judge_mod.family(model),
            "tier": "top" if model in TOP_TIER else "cheap", "settings": settings}


def _dir(root: Path, slug: str) -> Path:
    return root / SCREEN_DIR / slug


def _load(root: Path, slug: str) -> dict | None:
    p = _dir(root, slug) / "verdict.json"
    return json.loads(p.read_text()) if p.exists() else None


def _all(root: Path) -> dict[str, dict]:
    base = root / SCREEN_DIR
    if not base.exists():
        return {}
    return {d.name: v for d in sorted(base.iterdir()) if d.is_dir() and (v := _load(root, d.name))}


def _same_family(cand: dict) -> bool:
    return cand["family"] in TARGET_LEDGER_FAMILIES


def summarise(root: Path, verdict: dict | None, *, slug: str = "") -> dict:
    """Every step's state from the recorded runs. Passes count only under the current fixture hash;
    a complete fail counts under any hash, so changing a fixture never readmits a failed judge."""
    current = fixture_hash(root)
    v = dict(verdict or {"sequence": SEQUENCE, "slug": slug, "candidate": None, "runs": []})
    runs = v["runs"]
    live = [r for r in runs if r["fixtures_sha256"] == current]
    steps = {}
    for step in STEPS:
        passes = sum(r["outcome"] == "pass" for r in live if r["step"] == step)
        fails = sum(r["outcome"] == "fail" for r in runs if r["step"] == step)
        incomplete = sum(r["outcome"] == "incomplete" for r in live if r["step"] == step)
        if step == "S1" and v["candidate"] is not None and not _same_family(v["candidate"]):
            state = "n/a"
        else:
            state = "failed" if fails else "satisfied" if passes >= REQUIRED[step] else "pending"
        steps[step] = {"required": REQUIRED[step], "passes": passes, "fails": fails,
                       "incomplete": incomplete, "state": state}
    done = all(s["state"] in ("satisfied", "n/a") for s in steps.values())
    out = any(s["state"] == "failed" for s in steps.values())
    gated = sorted(s for s, o in {**_all(root), **({slug: v} if slug else {})}.items()
                   if any(r["step"] == "G2" and r["fixtures_sha256"] == current for r in o["runs"]))
    v.update(fixtures_sha256=current, steps=steps, stale_runs=len(runs) - len(live), g2_rule=G2_RULE,
             status="out" if out else "eligible" if done else "pending", eligible=done and not out,
             gated_on_this_hash=gated)
    v["settles_alone"] = False if v["candidate"] is None or v["candidate"]["tier"] == "cheap" else v["eligible"]
    return v


def status(root: Path, slug: str) -> dict:
    return summarise(root, _load(root, slug), slug=slug)


def _save(root: Path, slug: str, verdict: dict) -> dict:
    v = summarise(root, verdict, slug=slug)
    d = _dir(root, slug)
    d.mkdir(parents=True, exist_ok=True)
    (d / "verdict.json").write_text(json.dumps(v, indent=1, sort_keys=True) + "\n")
    return v


def _next_step(v: dict) -> str | None:
    if v["status"] == "out":
        failed = next(s for s, st in v["steps"].items() if st["state"] == "failed")
        raise Refused(f"candidate is out: a complete {failed} run failed")
    return next((s for s in STEPS if v["steps"][s]["state"] == "pending"), None)


def _ledger_usd(path: Path | None) -> float:
    if path is None or not path.exists():
        return 0.0
    return sum(json.loads(line)["usd"] for line in path.read_text().splitlines() if line.strip())


def command(root: Path, step: str, cand: dict, run_dir: Path, *, live: bool,
            cap: float | None = None, spend_ledger: Path | None = None) -> list[str]:
    """The runner's own command line, as D1b ran it; without `live`, the same command in replay mode."""
    s = cand["settings"]
    if step == "S0":
        return [sys.executable, str(root / G2_SCRIPT), "--out", str(run_dir), "--split", "gate", "--stand-ins"]
    if step == "G1":
        argv = [sys.executable, str(root / G1_SCRIPT), "--tag", run_dir.name, "--out-root", str(run_dir.parent),
                "--model", cand["model"]]
    else:
        argv = [sys.executable, str(root / G2_SCRIPT), "--out", str(run_dir), "--split", "gate", "--model", cand["model"]]
    if cand["provider"] == "openai":
        argv += ["--reasoning-effort", s["reasoning_effort"]]
    elif s.get("reasoning_max_tokens") is not None:
        argv += ["--reasoning-max-tokens", str(s["reasoning_max_tokens"])]
    if live:
        # l73.py knows only --judge openai; g1.py routes an OpenRouter model through it.
        judge_flag = "openai" if step == "G1" else cand["provider"]
        argv += ["--judge", judge_flag, "--max-usd", f"{cap:.6f}" if cap is not None else "PRIOR_LEDGER_USD+MAX_USD",
                 "--spend-ledger", str(spend_ledger)]
    return argv


def read_outcome(step: str, run_dir: Path, exit_code: int) -> dict:
    """pass / fail / incomplete from a runner's own result file. A missing file or a non-zero exit
    is incomplete (a budget stop, a provider error, a crash), and so is any undecided arm G1 or G2
    rules on."""
    if step == "S0":
        p, o = run_dir / "g2_standins_gate.json", run_dir / "g2_oracle_gate.json"
        if not p.exists() or not o.exists():
            return {"outcome": "incomplete", "figures": {"exit": exit_code}}
        passing = [r["judge_model"] for r in json.loads(p.read_text()) if r["passes"]]
        oracle = json.loads(o.read_text())["passes"]
        ok = not passing and oracle
        return {"outcome": "pass" if ok and exit_code == 0 else "fail" if not ok else "incomplete",
                "figures": {"passing_stand_ins": passing, "oracle_passes": oracle}}
    if step == "G1":
        p = run_dir / "l73" / "l73.json"
        if exit_code != 0 or not p.exists():
            return {"outcome": "incomplete", "figures": {"exit": exit_code}}
        r = json.loads(p.read_text())
        undecided = {arm: sum(pr["states"].get(arm) == "undecided" for t in r.get("topics", {}).values()
                              for row in t.values() for pr in row["all_pairs"]) for arm in G1_RULED_ARMS}
        figures = {**{k: r[k] for k in ("planted_fires", "stand_in_fires", "eligible")}, "undecided": undecided}
        if any(undecided.values()):
            return {"outcome": "incomplete", "figures": figures}
        return {"outcome": "pass" if r["eligible"] else "fail", "figures": figures}
    p = run_dir / "g2_gate.json"
    if exit_code != 0 or not p.exists():
        return {"outcome": "incomplete", "figures": {"exit": exit_code}}
    r = json.loads(p.read_text())
    figures = {k: r.get(k) for k in ("diff", "lower90", "rates", "R_excess", "undecided", "n_topics")}
    if not r["complete"]:
        return {"outcome": "incomplete", "figures": figures}
    return {"outcome": "pass" if r["passes"] else "fail", "figures": figures}


def _new_run_dir(root: Path, slug: str, step: str, v: dict) -> Path:
    k = 1 + sum(r["step"] == step for r in v["runs"])
    d = _dir(root, slug) / f"{step}-run{k}"
    if d.exists():
        raise Refused(f"{d} exists; a run needs a new directory so its closure cache starts empty")
    return d


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _record(v: dict, step: str, run_dir: Path | None, outcome: dict, root: Path, **extra) -> None:
    v["runs"].append({"step": step, "dir": str(run_dir.relative_to(root)) if run_dir else None,
                      "fixtures_sha256": fixture_hash(root), "finished": _now(), **outcome,
                      **{k: x for k, x in extra.items() if x is not None}})


def _parallel_arm(root: Path, slug: str) -> str | None:
    for other, o in _all(root).items():
        o = summarise(root, o, slug=other)
        if other != slug and o["candidate"] and not _same_family(o["candidate"]) and o["eligible"]:
            return other
    return None


class _Lock:
    def __init__(self, path: Path, what: str):
        self.path, self.what = path, what

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            os.close(os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        except FileExistsError:
            raise Refused(f"{self.path} exists: another screening run holds the lock on {self.what}") from None
        return self

    def __exit__(self, *exc):
        self.path.unlink(missing_ok=True)


def _open(root: Path, slug: str, cand: dict, owner_note: str | None) -> dict:
    rec = candidate_record(cand)
    v = _load(root, slug)
    if v is None:
        failed = [s for s, o in _all(root).items() if o["candidate"]["model"] == rec["model"]
                  and o.get("sequence") == SEQUENCE and any(r["outcome"] == "fail" for r in o["runs"])]
        if failed and not owner_note:
            raise Refused(f"{rec['model']} is out under {', '.join(failed)}; a new configuration needs --owner-note")
        v = {"sequence": SEQUENCE, "slug": slug, "candidate": rec, "runs": []}
        if failed:
            v["readmitted"] = {"after": failed, "owner_note": owner_note}
    if v["candidate"] != rec:
        raise Refused(f"settings differ from the pinned candidate {v['candidate']}; screen another slug instead")
    return summarise(root, v, slug=slug)


def _free_steps(root: Path, slug: str, v: dict, runner: Runner) -> tuple[dict, str | None]:
    """Run every pending $0 step in order; return the verdict and the first paid step pending."""
    while (step := _next_step(v)) is not None and step not in PAID:
        if step == "S0":
            run_dir = _new_run_dir(root, slug, step, v)
            code = runner(command(root, step, v["candidate"], run_dir, live=False), root / "gapmap")
            outcome = read_outcome(step, run_dir, code)
            _record(v, step, run_dir, outcome, root)
            v = _save(root, slug, v)
            if outcome["outcome"] != "pass":
                raise Refused(f"S0 fixtures is {outcome['outcome']} ({outcome['figures']}); no paid run may start")
        else:
            arm = _parallel_arm(root, slug)
            if arm is None:
                _save(root, slug, v)
                raise Refused(f"S1 parallel arm pending: {v['candidate']['model']} shares a target ledger's "
                              f"family; it is screened only after an other-family candidate is eligible "
                              f"on fixtures {v['fixtures_sha256'][:12]}")
            _record(v, step, None, {"outcome": "pass", "figures": {}}, root, parallel_arm=arm,
                    arm_verdict_sha256=_sha(_dir(root, arm) / "verdict.json"))
            v = _save(root, slug, v)
    return v, step


def _after_gate(after: Path | None) -> dict | None:
    """A plan's own $0 gate before this spend (D1b's Stop A was one): its record must say continue."""
    if after is None:
        return None
    if not after.exists():
        raise Refused(f"--after {after} does not exist: the gate before this spend has not run")
    rec = json.loads(after.read_text())
    if rec.get("continue") is not True:
        raise Refused(f"--after {after} does not say continue: true; no paid run may start")
    return {"path": str(after), "sha256": _sha(after)}


def run(root: Path, slug: str, cand: dict, *, runner: Runner = _subprocess_runner, live: bool = False,
        max_usd: float | None = None, spend_ledger: Path | None = None, after: Path | None = None,
        owner_note: str | None = None, headroom: Headroom | None = None) -> dict:
    """Pending $0 steps, then at most one paid run, and only with `live`, a cap and a ledger."""
    with _Lock(_dir(root, slug) / LOCK, f"candidate {slug}"):
        v = _open(root, slug, cand, owner_note)
        v, step = _free_steps(root, slug, v, runner)
        if step is None:
            return {"verdict": _save(root, slug, v), "waiting_for": None}
        run_dir = _new_run_dir(root, slug, step, v)
        if not live:
            _save(root, slug, v)
            return {"verdict": v, "waiting_for": step,
                    "next_command": command(root, step, v["candidate"], run_dir, live=True, cap=None,
                                            spend_ledger=spend_ledger or Path("SPEND_LEDGER"))}
        gate = _after_gate(after)
        if max_usd is None:
            raise Refused(f"{step} is paid: pass --max-usd (this run's own cap)")
        if spend_ledger is None:
            raise Refused(f"{step} is paid: pass --spend-ledger (the runners' caps are cumulative over it)")
        if v["steps"][step]["incomplete"] >= FREE_INCOMPLETE_RETRIES and not owner_note:
            raise Refused(f"{step} already has {v['steps'][step]['incomplete']} incomplete run(s); "
                          f"another needs --owner-note, so a run heading for a fail is not simply rerun")
        spend_ledger = Path(spend_ledger).resolve()
        ok, room = (headroom or _key_headroom(root))(v["candidate"]["provider"], max_usd)
        if not ok:
            raise Refused(f"the provider's headroom does not cover ${max_usd:.2f}: {room}")
        with _Lock(spend_ledger.with_name(spend_ledger.name + LOCK), f"spend ledger {spend_ledger.name}"):
            prior = _ledger_usd(spend_ledger)
            started = _now()
            code = runner(command(root, step, v["candidate"], run_dir, live=True, cap=prior + max_usd,
                                  spend_ledger=spend_ledger), root / "gapmap")
            spent = _ledger_usd(spend_ledger) - prior
        outcome = read_outcome(step, run_dir, code)
        _record(v, step, run_dir, outcome, root, started=started, max_usd=max_usd, spend_usd=round(spent, 6),
                spend_ledger=str(spend_ledger), headroom=room, after_gate=gate, owner_note=owner_note)
        return {"verdict": _save(root, slug, v), "waiting_for": step, "outcome": outcome}


def adopt(root: Path, slug: str, cand: dict, step: str, source: Path, *, note: str,
          runner: Runner = _subprocess_runner) -> dict:
    """Re-score a finished run's closure cache through the current runner in replay mode ($0; a
    cache miss stops it), into a new run directory, in the standard order. The replay must
    reproduce the source run's own result file, or nothing is recorded."""
    if step not in PAID:
        raise Refused("only G1 and G2 runs can be adopted")
    if not note.strip():
        raise Refused("adopt needs --note saying how the source run was made (cold cache, settings)")
    source = Path(source).resolve()
    with _Lock(_dir(root, slug) / LOCK, f"candidate {slug}"):
        v = _open(root, slug, cand, None)
        v, pending = _free_steps(root, slug, v, runner)
        if pending != step:
            raise Refused(f"cannot adopt {step} while {pending or 'nothing'} is the next pending step")
        original = read_outcome(step, source, 0)
        if original["outcome"] == "incomplete":
            raise Refused(f"{source} holds no complete {step} result to reproduce")
        run_dir = _new_run_dir(root, slug, step, v)
        cache_rel = Path("l73") / "closure_judgements.json" if step == "G1" else Path("closure_judgements.json")
        src_cache = source / cache_rel
        (run_dir / cache_rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src_cache, run_dir / cache_rel)
        code = runner(command(root, step, v["candidate"], run_dir, live=False), root / "gapmap")
        outcome = read_outcome(step, run_dir, code)
        if outcome != original:
            shutil.rmtree(run_dir)
            raise Refused(f"replay gives {outcome}, the source run recorded {original}; not adopted")
        _record(v, step, run_dir, outcome, root, adopted_from=str(source.relative_to(root)), note=note,
                source_cache_sha256=_sha(src_cache))
        return {"verdict": _save(root, slug, v), "outcome": outcome}


def _states(root: Path, v: dict) -> list[dict]:
    return [json.loads((root / r["dir"] / "g2_gate.json").read_text())["states"]
            for r in v["runs"] if r["step"] == "G2" and r["outcome"] == "pass"
            and r["fixtures_sha256"] == v["fixtures_sha256"]]


def agreement(a: list[dict], b: list[dict]) -> dict:
    """Agreement and Cohen's kappa over every (topic, arm) state, run k of one arm against run k of
    the other (D1b plan §2.2 "Pairing"; aggregates only)."""
    pairs = [(x[t][arm], y[t][arm]) for x, y in zip(a, b) for t in x for arm in x[t]]
    if not pairs:
        return {"n": 0, "agreement": None, "kappa": None}
    n = len(pairs)
    po = sum(p == q for p, q in pairs) / n
    labels = {s for p in pairs for s in p}
    pe = sum((sum(p == s for p, _ in pairs) / n) * (sum(q == s for _, q in pairs) / n) for s in labels)
    return {"n": n, "agreement": round(po, 4), "kappa": round((po - pe) / (1 - pe), 4) if pe < 1 else None}


def pair(root: Path, cheap: str, top: str) -> dict:
    """The cheap arm alone settles nothing: a usable pair is an eligible other-family cheap arm and
    an eligible top-tier arm on the same fixture hash."""
    c, t = status(root, cheap), status(root, top)
    problems = []
    if not (c["candidate"] and c["candidate"]["tier"] == "cheap" and not _same_family(c["candidate"])):
        problems.append(f"{cheap} is not a cheap other-family candidate")
    if not (t["candidate"] and t["candidate"]["tier"] == "top"):
        problems.append(f"{top} is not a top-tier candidate")
    problems += [f"{s} is {v['status']}" for s, v in ((cheap, c), (top, t)) if not v["eligible"]]
    notes = {s: [r["note"] for r in v["runs"] if r.get("note")] for s, v in ((cheap, c), (top, t))}
    return {"cheap": cheap, "top": top, "ready": not problems, "problems": problems, "notes": notes,
            "fixtures_sha256": c["fixtures_sha256"], "g2_rule": G2_RULE,
            "g2_state_agreement": agreement(_states(root, c), _states(root, t)) if not problems else None}


def _cand(args) -> dict:
    return {"model": args.model, "reasoning_effort": args.reasoning_effort,
            "reasoning_max_tokens": args.reasoning_max_tokens}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="gapmap.screen", description=__doc__.split("\n\n")[0])
    p.add_argument("--root", default=str(ROOT), help=argparse.SUPPRESS)
    sub = p.add_subparsers(dest="cmd", required=True)
    st = sub.add_parser("status")
    st.add_argument("--candidate", required=True)
    for name in ("run", "adopt"):
        sp = sub.add_parser(name)
        sp.add_argument("--candidate", required=True)
        sp.add_argument("--model", required=True)
        sp.add_argument("--reasoning-effort")
        sp.add_argument("--reasoning-max-tokens", type=int)
        if name == "run":
            sp.add_argument("--live", action="store_true")
            sp.add_argument("--max-usd", type=float)
            sp.add_argument("--spend-ledger")
            sp.add_argument("--after", help="a plan's $0 gate record that must say continue: true")
            sp.add_argument("--owner-note")
        else:
            sp.add_argument("--step", choices=sorted(PAID), required=True)
            sp.add_argument("--from", dest="source", required=True)
            sp.add_argument("--note", required=True)
    pa = sub.add_parser("pair")
    pa.add_argument("--cheap", required=True)
    pa.add_argument("--top", required=True)
    args = p.parse_args(argv)
    root = Path(args.root).resolve()
    try:
        if args.cmd == "status":
            print(json.dumps(status(root, args.candidate), indent=1, sort_keys=True))
            return 0
        if args.cmd == "pair":
            res = pair(root, args.cheap, args.top)
            print(json.dumps(res, indent=1, sort_keys=True))
            return 0 if res["ready"] else 1
        if args.cmd == "adopt":
            res = adopt(root, args.candidate, _cand(args), args.step, Path(args.source), note=args.note)
        else:
            res = run(root, args.candidate, _cand(args), live=args.live, max_usd=args.max_usd,
                      spend_ledger=Path(args.spend_ledger) if args.spend_ledger else None,
                      after=Path(args.after) if args.after else None, owner_note=args.owner_note)
    except Refused as exc:
        print(f"refused: {exc}", file=sys.stderr)
        return 1
    v = res["verdict"]
    print(json.dumps({"status": v["status"], "eligible": v["eligible"], "steps": v["steps"],
                      **{k: res[k] for k in ("waiting_for", "outcome", "next_command") if k in res}},
                     indent=1, sort_keys=True))
    return 2 if res.get("next_command") else 0


if __name__ == "__main__":
    sys.exit(main())
