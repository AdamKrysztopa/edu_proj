import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from probe_app.backends import make_backend
from probe_app.config import INSTRUMENT_DIR, load_models, load_problems, load_prompt
from probe_app.llm import Guard
from probe_code.agreement import alpha_nominal, cohen_kappa, decoy_false_rate, guess_rate
from probe_code.corroboration import corroboration_sheet
from probe_code.export import export_blind, export_trace, read_csv, write_csv
from probe_code.guard_audit import ai_rejection_counts, guard_audit
from probe_code.loader import load_session


def _labels(path: Path, id_col: str, label_col: str) -> dict[str, str]:
    return {r[id_col]: r[label_col] for r in read_csv(path) if r[label_col] != ""}


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "y", "yes"}


def main(argv: list[str] | None = None) -> None:
    load_dotenv(INSTRUMENT_DIR / ".env")
    p = argparse.ArgumentParser(prog="probe-code")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("export-blind", "export-trace", "guard-audit"):
        c = sub.add_parser(name)
        c.add_argument("sessions", nargs="+", type=Path)
        c.add_argument("--out", type=Path, required=True)
        c.add_argument("--seed", type=int, default=0)
        c.add_argument("--allow-simulated", action="store_true")
    c = sub.add_parser("corroboration")
    c.add_argument("operations", type=Path)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--seed", type=int, default=0)
    for name in ("alpha", "kappa"):
        c = sub.add_parser(name)
        c.add_argument("a", type=Path)
        c.add_argument("b", type=Path)
        c.add_argument("--id", default="unit_id")
        c.add_argument("--label", default="label")
    c = sub.add_parser("decoys")
    c.add_argument("judgments", type=Path, help="item_id, corroborated")
    c.add_argument("key", type=Path, help="corroboration_key.csv")
    c = sub.add_parser("guesses")
    c.add_argument("guesses", type=Path, help="blind_session, arm")
    c.add_argument("key", type=Path, help="key_units.csv")
    args = p.parse_args(argv)

    if args.cmd in ("export-blind", "export-trace", "guard-audit"):
        sessions = [load_session(s, args.allow_simulated) for s in args.sessions]
        if args.cmd == "export-blind":
            export_blind(sessions, args.out, args.seed)
        elif args.cmd == "export-trace":
            export_trace(sessions, args.out, args.seed)
        else:
            args.out.mkdir(parents=True, exist_ok=True)
            log_path = args.out / "guard_audit_llm.jsonl"

            def log(record: dict) -> None:
                with log_path.open("a") as f:
                    f.write(json.dumps(record) + "\n")

            guard = Guard(make_backend("guard", load_models().guard), log, load_prompt("guard_system.md"))
            statements = {k: v["statement"] for k, v in load_problems()["problems"].items()}
            rows = guard_audit(sessions, guard, statements)
            write_csv(args.out / "guard_audit.csv", rows)
            for arm in ("ai", "human"):
                arm_rows = [r for r in rows if r["arm"] == arm]
                if arm_rows:
                    print(f"{arm}: {sum(r['flagged'] for r in arm_rows)}/{len(arm_rows)} questions flagged")
            for s in sessions:
                print(s.session_id, ai_rejection_counts(s.dir))
    elif args.cmd == "corroboration":
        print(corroboration_sheet(read_csv(args.operations), args.out, args.seed))
    elif args.cmd in ("alpha", "kappa"):
        a, b = _labels(args.a, args.id, args.label), _labels(args.b, args.id, args.label)
        print(f"{(alpha_nominal if args.cmd == 'alpha' else cohen_kappa)(a, b):.3f}")
    elif args.cmd == "decoys":
        judgments = {r["item_id"]: _truthy(r["corroborated"]) for r in read_csv(args.judgments)}
        is_decoy = {r["item_id"]: _truthy(r["is_decoy"]) for r in read_csv(args.key)}
        print(f"false corroboration on decoys: {decoy_false_rate(judgments, is_decoy):.3f}")
    elif args.cmd == "guesses":
        guesses = {r["blind_session"]: r["arm"] for r in read_csv(args.guesses)}
        truth = {r["blind_session"]: r["arm"] for r in read_csv(args.key)}
        print(f"condition guessed correctly: {guess_rate(guesses, truth):.3f} (chance 0.5)")
