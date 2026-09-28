import argparse
import json
import math
from pathlib import Path

from dotenv import load_dotenv

from probe_app.backends import make_backend
from dataclasses import asdict

from probe_app.config import INSTRUMENT_DIR, current_config, load_models, load_problems
from probe_app.llm import make_guard
from probe_code.agreement import (alpha_masi, alpha_nominal, cohen_kappa, decoy_false_rate, guess_rate,
                                  per_code_kappa)
from probe_code.corroboration import corroboration_sheet
from probe_code import calibration, k0
from probe_code.baseline import freeze_decision, pooled_metrics, session_metrics
from probe_code.export import export_blind, export_leading, export_trace, read_csv, write_csv, write_unmarked_key
from probe_code.guard_audit import ai_rejection_counts, config_drift, guard_audit, leading_by_arm
from probe_code.loader import load_session


def _labels(path: Path, id_col: str, label_col: str) -> dict[str, str]:
    return {r[id_col]: r[label_col] for r in read_csv(path) if r[label_col] != ""}


def codebook_types(path: Path) -> list[str]:
    section = path.read_text().split("\n## Type", 1)[1].split("\n## ", 1)[0]
    rows = [line.split("|")[1].strip() for line in section.splitlines() if line.startswith("|")]
    return [r for r in rows if r not in ("Type", "") and not r.startswith("---")]


def _label_sets(path: Path, id_col: str, label_col: str,
                types: list[str]) -> tuple[dict[str, frozenset[str]], set[str]]:
    """Codebook v0 "Agreement": `;`-separated codes, `none` for a unit with no operation, blank for not coded."""
    canonical = {t.casefold(): t for t in types}
    seen: set[str] = set()
    out: dict[str, frozenset[str]] = {}
    for r in read_csv(path):
        unit, cell = r[id_col], r[label_col].strip()
        if unit in seen:
            raise ValueError(f"{path.name}: unit {unit} appears twice; put its codes in one cell, separated by ';'")
        seen.add(unit)
        if cell == "":
            continue
        codes = {c.strip() for c in cell.split(";") if c.strip()}
        if "none" in {c.casefold() for c in codes}:
            if len(codes) > 1:
                raise ValueError(f"{path.name}: unit {unit} combines 'none' with codes")
            out[unit] = frozenset()
            continue
        unknown = sorted(c for c in codes if c.casefold() not in canonical)
        if unknown:
            raise ValueError(f"{path.name}: unit {unit} has codes not in the codebook's Type table: {unknown}")
        out[unit] = frozenset(canonical[c.casefold()] for c in codes)
    return out, seen


def _coverage(a: dict, b: dict, units: set[str]) -> str:
    both = len(set(a) & set(b))
    if both < 2:
        raise ValueError(f"fewer than 2 units coded by both coders ({both})")
    return (f"{both} of {len(units)} units coded by both; "
            f"left blank or missing: A {len(units - set(a))}, B {len(units - set(b))}")


def _truthy(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "y", "yes"}


def main(argv: list[str] | None = None) -> None:
    load_dotenv(INSTRUMENT_DIR / ".env")
    p = argparse.ArgumentParser(prog="probe-code")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("export-blind", "export-trace", "guard-audit", "export-leading"):
        c = sub.add_parser(name)
        c.add_argument("sessions", nargs="+", type=Path)
        c.add_argument("--out", type=Path, required=True)
        c.add_argument("--seed", type=int, default=0)
        if name == "guard-audit":
            c.add_argument("--allow-drift", action="store_true",
                           help="audit sessions whose frozen configuration differs from the current one (pilots)")
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
        c.add_argument("--multi", action="store_true",
                       help="several codes per unit: alpha with MASI distance, kappa per code (codebook v0)")
        c.add_argument("--codebook", type=Path, default=INSTRUMENT_DIR / "codebook" / "v0.md",
                       help="with --multi: codes must be rows of its Type table")
    c = sub.add_parser("decoys")
    c.add_argument("judgments", type=Path, help="item_id, corroborated")
    c.add_argument("key", type=Path, help="corroboration_key.csv")
    c = sub.add_parser("guesses")
    c.add_argument("guesses", type=Path, help="blind_session, arm")
    c.add_argument("key", type=Path, help="key_units.csv")
    c = sub.add_parser("leading-rates", help="leading-question rate per arm from blind labels")
    c.add_argument("labels", type=Path, help="item_id, leading")
    c.add_argument("key", type=Path, help="key_leading.csv")
    c = sub.add_parser("freeze-baseline", help="decision 0004 metrics, pooled, and the freeze rule's outcome")
    c.add_argument("sessions", nargs="+", type=Path)
    c = sub.add_parser("guard-calibration-sheet", help="blind labelling sheet for the guard calibration items")
    c.add_argument("items", type=Path)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--seed", type=int, required=True)
    c = sub.add_parser("guard-calibrate", help="run the live guard over the calibration items")
    c.add_argument("items", type=Path)
    c.add_argument("--out", type=Path, required=True)
    c = sub.add_parser("calibration-report", help="guard sensitivity/specificity against adjudicated human labels")
    c.add_argument("items", type=Path)
    c.add_argument("labeller_a", type=Path)
    c.add_argument("labeller_b", type=Path)
    c.add_argument("adjudicated", type=Path)
    c.add_argument("verdicts", type=Path)
    c.add_argument("--min-class", type=int, default=calibration.MIN_CLASS)
    c = sub.add_parser("k0-sample", help="random coding order and one item per student")
    c.add_argument("roster", type=Path, help="student_id")
    c.add_argument("--items", required=True, help="comma-separated item ids")
    c.add_argument("--seed", type=int, required=True)
    c.add_argument("--out", type=Path, required=True)
    c.add_argument("--exclude", type=Path, help="student_id: students to leave out (e.g. early-K0 sitters in the pretest)")
    c = sub.add_parser("k0", help="the registered K0 decision from adjudicated first-error codes")
    c.add_argument("codes", type=Path, help="adjudicated: student_id, item_id, top, code")
    c.add_argument("--plan", type=Path, required=True, help="the k0-sample plan the coders followed")
    c.add_argument("--early", action="store_true", help="early K0: fewer than 100 errored solutions is inconclusive")
    c.add_argument("--components", type=Path, help="student_id, component_id, correct")
    c = sub.add_parser("k0-kappa", help="two coders' top-level agreement over solutions either calls errored")
    c.add_argument("coder_a", type=Path)
    c.add_argument("coder_b", type=Path)
    c.add_argument("--plan", type=Path, required=True)
    c = sub.add_parser("form-agreement", help="per-student first-error agreement between two forms")
    c.add_argument("form1", type=Path)
    c.add_argument("form2", type=Path)
    args = p.parse_args(argv)

    if args.cmd in ("export-blind", "export-trace", "guard-audit", "export-leading"):
        sessions = [load_session(s, args.allow_simulated) for s in args.sessions]
        statements = {k: v["statement"] for k, v in load_problems()["problems"].items()}
        if args.cmd != "export-trace":
            write_unmarked_key(sessions, args.out)
        if args.cmd == "export-blind":
            export_blind(sessions, args.out, args.seed)
        elif args.cmd == "export-trace":
            export_trace(sessions, args.out, args.seed)
        elif args.cmd == "export-leading":
            export_leading(sessions, args.out, args.seed, statements)
        else:
            drifted = {s.session_id: config_drift(s) for s in sessions}
            drifted = {k: v for k, v in drifted.items() if v}
            if drifted and not args.allow_drift:
                raise SystemExit(f"frozen configuration differs from the current one: {drifted}; "
                                 "the audit would not use the guard those sessions had (--allow-drift for pilots)")
            args.out.mkdir(parents=True, exist_ok=True)
            log_path = args.out / "guard_audit_llm.jsonl"

            def log(record: dict) -> None:
                with log_path.open("a") as f:
                    f.write(json.dumps(record) + "\n")

            guard = make_guard(make_backend("guard", load_models().guard), log)
            rows = guard_audit(sessions, guard, statements)
            write_csv(args.out / "guard_audit.csv", rows)
            for arm in ("ai", "human"):
                arm_rows = [r for r in rows if r["arm"] == arm and r["source"] != "unmarked"]
                if arm_rows:
                    print(f"{arm}: {sum(r['flagged'] for r in arm_rows)}/{len(arm_rows)} questions flagged")
            unmarked = [r for r in rows if r["source"] == "unmarked"]
            if unmarked:
                print(f"unmarked speech (speaker unknown): {sum(r['flagged'] for r in unmarked)}/{len(unmarked)} flagged")
            for s in sessions:
                print(s.session_id, ai_rejection_counts(s.dir))
    elif args.cmd == "guard-calibration-sheet":
        write_csv(args.out, calibration.labelling_sheet(read_csv(args.items), args.seed))
    elif args.cmd == "guard-calibrate":
        log_path = args.out.with_suffix(".llm.jsonl")

        def log(record: dict) -> None:
            with log_path.open("a") as f:
                f.write(json.dumps(record) + "\n")

        guard = make_guard(make_backend("guard", load_models().guard), log)
        write_csv(args.out, calibration.run_guard(read_csv(args.items), guard))
    elif args.cmd == "calibration-report":
        r = calibration.report(read_csv(args.items), read_csv(args.labeller_a), read_csv(args.labeller_b),
                               read_csv(args.adjudicated), read_csv(args.verdicts), args.min_class)
        print(json.dumps(asdict(r), indent=2))
    elif args.cmd == "leading-rates":
        labels = {r["item_id"]: r["leading"] for r in read_csv(args.labels)}
        for arm, c in sorted(leading_by_arm(labels, read_csv(args.key)).items()):
            print(f"{arm}: {c['leading']}/{c['coded']} leading"
                  + (f"; {c['unmarked']} unmarked turns not coded" if c["unmarked"] else ""))
    elif args.cmd == "freeze-baseline":
        for s in args.sessions:
            m = json.loads((s / "manifest.json").read_text())
            if not (m.get("pilot") or m.get("simulated")):
                raise SystemExit(f"{s.name} is a data session; the freeze baseline pools only pilot and simulated sessions")
        metrics = [session_metrics(s) for s in args.sessions]
        now = asdict(current_config())
        drift = sorted(k for k in now if (metrics[0]["config"] or {}).get(k) != now[k])
        if drift:
            raise SystemExit(f"these sessions ran a superseded configuration (differs in {drift}); "
                             "rerun simulated sessions on the current one")
        pooled = pooled_metrics(metrics)
        print(json.dumps({"pooled": pooled, "decision": freeze_decision(pooled)}, indent=2, default=str))
    elif args.cmd == "corroboration":
        print(corroboration_sheet(read_csv(args.operations), args.out, args.seed))
    elif args.cmd in ("alpha", "kappa") and args.multi:
        types = codebook_types(args.codebook)
        (a, ids_a), (b, ids_b) = (_label_sets(f, args.id, args.label, types) for f in (args.a, args.b))
        coverage = _coverage(a, b, ids_a | ids_b)
        if args.cmd == "alpha":
            print(f"{alpha_masi(a, b):.3f} ({coverage})")
        else:
            print(coverage)
            for code, r in per_code_kappa(a, b).items():
                kappa = "n/a" if math.isnan(r["kappa"]) else f"{r['kappa']:.3f}"
                print(f"{code}: {kappa} (present: A {r['a']}, B {r['b']} of {r['units']} units)")
    elif args.cmd in ("alpha", "kappa"):
        a, b = _labels(args.a, args.id, args.label), _labels(args.b, args.id, args.label)
        print(f"{(alpha_nominal if args.cmd == 'alpha' else cohen_kappa)(a, b):.3f}")
    elif args.cmd == "decoys":
        judgments = {r["item_id"]: _truthy(r["corroborated"]) for r in read_csv(args.judgments)}
        is_decoy = {r["item_id"]: _truthy(r["is_decoy"]) for r in read_csv(args.key)}
        print(f"false corroboration on decoys: {decoy_false_rate(judgments, is_decoy):.3f}")
    elif args.cmd == "k0-sample":
        ids = [r["student_id"] for r in read_csv(args.roster)]
        exclude = {r["student_id"] for r in read_csv(args.exclude)} if args.exclude else set()
        write_csv(args.out, k0.sample_plan(ids, args.items.split(","), args.seed, exclude))
    elif args.cmd == "k0":
        d = k0.decide(read_csv(args.codes), read_csv(args.plan), early=args.early)
        print(f"errored={d.errored} selection/representation={d.selection_representation} "
              f"share={d.share:.3f} wilson95=[{d.ci[0]:.3f}, {d.ci[1]:.3f}] "
              f"blank={d.blank} correct={d.correct} beyond-stopping-rule={d.ignored} -> {d.decision}")
        if args.components:
            kept, _ = k0.follow_plan(read_csv(args.codes), read_csv(args.plan))
            c = k0.component_share(kept, read_csv(args.components))
            print(f"secondary: passed both components={c.passed_both} (of them selection/representation="
                  f"{c.selection_representation}); failed a component={c.failed_any}; no component sheet={c.missing}")
    elif args.cmd == "k0-kappa":
        g = k0.coder_kappa(read_csv(args.coder_a), read_csv(args.coder_b), read_csv(args.plan))
        print(f"n={g.n} raw agreement={g.raw_agreement:.3f} kappa={g.kappa:.3f} (target {k0.KAPPA_TARGET:.2f})")
    elif args.cmd == "form-agreement":
        f = k0.form_agreement(read_csv(args.form1), read_csv(args.form2))
        print(f"n={f.n} raw agreement={f.raw_agreement:.3f} kappa={f.kappa:.3f}"
              f" bootstrap95=[{f.ci[0]:.3f}, {f.ci[1]:.3f}]"
              f"{'' if f.sufficient else f' (below the minimum n of {k0.FORM_AGREEMENT_MIN_N}: inconclusive)'}")
    elif args.cmd == "guesses":
        guesses = {r["blind_session"]: r["arm"] for r in read_csv(args.guesses)}
        truth = {r["blind_session"]: r["arm"] for r in read_csv(args.key)}
        print(f"condition guessed correctly: {guess_rate(guesses, truth):.3f} (chance 0.5)")
