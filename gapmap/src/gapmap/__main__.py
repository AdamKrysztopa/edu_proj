"""CLI (spec §0, S1): `python -m gapmap --ledger L.json [--sibling S.json] [--sidecar sc.json]
--domain NAME --out DIR [--judge ollama]`. Deterministic given a filled judge cache: replay mode
(no `--judge`) never opens a socket -- a closure-judge cache miss raises a clear error instead."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from residual.ledger import Ledger
from residual.provenance import Verdict

from gapmap import checks, config, judge as judge_mod, lenses, link, rank, record, render, semantic


def _sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()


def _admissibility_note(ledger: Ledger, sidecar: dict | None) -> str | None:
    reasons = []
    if sidecar is not None and sidecar.get("n3_input") is False:
        reason = sidecar.get("n3_input_reason")
        reasons.append("sidecar n3_input is false" + (f": {reason}" if reason else ""))
    pending = sum(1 for c in ledger.claims for e in c.evidence if e.verification.verdict is Verdict.PENDING)
    if pending:
        reasons.append(f"{pending} pending verification(s) in the ledger")
    return "; ".join(reasons) if reasons else None


def _lexical_category(cand: lenses.Candidate, k_topic: int) -> str | None:
    if cand.lexical_state == "closed":
        return None
    return record.categorize(cand.lexical_state, k_topic)


def _primary_records(ledger: Ledger, index: link.Index, ledger_sha: str, judge) -> list[record.Record]:
    # Robustness (§1.4) is measured on the LEXICAL construct across the 4 link-parameter
    # settings, not re-judged 4x: the judge decides the ONE displayed state (SETTING_1), and
    # retrieval/prompts are independent of `common_cut`/`shared_threshold` by design, so a
    # judge-based robustness would just re-ask the SETTING_1 question with different `x_a`
    # membership -- lexical reproducibility is what `r/4` has always measured (see Implementation
    # notes: "robustness is measured lexically").
    lexical_settings_results = [
        [(cand, _lexical_category(cand, len(link.breadth(ledger, cand.x_a))))
         for cand in lenses.run_all(ledger, index, s)]
        for s in link.SETTINGS]
    out = []
    for cand in lenses.run_all(ledger, index, link.SETTING_1):
        outcome, sub = semantic.judge_candidate(ledger, index, judge, cand)
        if outcome.state == "closed":
            continue
        k_topic = len(link.breadth(ledger, sub.x_a))
        cat = record.categorize(outcome.state, k_topic)
        lex_cat = _lexical_category(cand, k_topic)
        r = record.robustness(cand, lex_cat, lexical_settings_results) if lex_cat is not None else 0
        out.append(record.build_record(ledger, ledger_sha, sub, outcome, cat, r))
    return out


def build_gapmap(ledger: Ledger, *, domain: str, judge, sidecar: dict | None = None,
                 sibling: Ledger | None = None, ledger_text: str | None = None) -> record.GapMapResult:
    ledger_sha = _sha256_text(ledger_text if ledger_text is not None else ledger.to_json())
    index = link.build_index(ledger)

    all_records = [*_primary_records(ledger, index, ledger_sha, judge),
                  *record.unk_gaps(ledger, index, sidecar, ledger_sha)]

    pool = rank.merge(all_records)
    stats = checks.candidate_stats(ledger, index, judge)
    check_data: dict = {}
    check_data["promo_excluded"] = lenses.promo_excluded_count(ledger, index)

    lens_candidates = lenses.run_all(ledger, index, link.SETTING_1)
    check_data["lexical_donor_null"] = checks.lexical_donor_null(ledger, index, lens_candidates)
    check_data["mismatched_evidence_control"] = checks.mismatched_evidence_control(
        ledger, ledger_sha, index, judge, lens_candidates)
    check_data["judge_lexical_confusion"] = checks.judge_lexical_confusion(stats)

    if sibling is not None:
        sib_index = link.build_index(sibling)
        sib_stats = checks.candidate_stats(sibling, sib_index, judge)  # judged too, same cache
        all_records = [checks.apply_sibling(r, sib_stats) for r in all_records]
        pool = rank.merge(all_records)
        sib_records = rank.merge(_primary_records(sibling, sib_index, _sha256_text(sibling.to_json()), judge))
        open_a = [r for r in pool if r.category in ("HYP", "RG-SINGLE")]
        open_b = [r for r in sib_records if r.category in ("HYP", "RG-SINGLE")]
        check_data["cross_run_stability"] = checks.cross_run_stability(open_a, open_b, sib_records, pool)

    map_records, rg_records = rank.build(all_records, ledger, ledger_sha)
    map_only = [r for r in map_records if r.category == "HYP"]
    # F2: §7.1 is computed over lens candidates only (HYP, RG-SINGLE, RG-UNVER, RG-SIBLING and
    # closed candidates) -- RG-UNK and CONTROL never vary in density and would dilute the check.
    lens_pool = [r for r in pool if r.category != "RG-UNK"]
    anti_renaming = checks.anti_renaming(map_only, lens_pool, stats)
    null = check_data["lexical_donor_null"]
    if null["total"]["flag"] or any(v["flag"] for v in null["by_lens"].values()):
        anti_renaming["flags"].append("closure-uninformative")
    mismatched = check_data["mismatched_evidence_control"]
    if (mismatched["total"] and mismatched["total"]["flag"]) or any(
            v["flag"] for v in mismatched["by_lens"].values()):
        if "closure-uninformative" not in anti_renaming["flags"]:
            anti_renaming["flags"].append("closure-uninformative")
    check_data["anti_renaming"] = anti_renaming

    note = _admissibility_note(ledger, sidecar)
    return record.GapMapResult(domain=domain, ledger_sha256=ledger_sha, config_sha256=config.CONFIG_SHA256,
                               admissible=note is None, admissibility_note=note,
                               map=map_records, retrieval_gaps=rg_records, check_data=check_data)


def _load_json(path: str | None) -> dict | None:
    if path is None:
        return None
    return json.loads(Path(path).read_text())


def _default_judge(out_dir: str, judge_mode: str | None):
    cache_path = Path(out_dir) / "closure_judgements.json"
    return judge_mod.CachedJudge(judge_mod.OllamaJudge(), cache_path, live=(judge_mode == "ollama"))


def run(ledger_path: str, *, domain: str, out_dir: str, sibling_path: str | None = None,
       sidecar_path: str | None = None, judge_mode: str | None = None, judge=None) -> None:
    ledger_text = Path(ledger_path).read_text()
    ledger = Ledger.from_json(ledger_text)
    sibling = Ledger.from_json(Path(sibling_path).read_text()) if sibling_path else None
    sidecar = _load_json(sidecar_path)

    j = judge if judge is not None else _default_judge(out_dir, judge_mode)

    result = build_gapmap(ledger, domain=domain, judge=j, sidecar=sidecar, sibling=sibling,
                          ledger_text=ledger_text)

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "gapmap.json").write_text(
        json.dumps(record.to_json_dict(result), sort_keys=True, indent=1) + "\n")
    (out / "gapmap.md").write_text(render.render(result))
    if isinstance(j, judge_mod.CachedJudge):
        j.save()


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="gapmap")
    p.add_argument("--ledger", required=True)
    p.add_argument("--sibling")
    p.add_argument("--sidecar")
    p.add_argument("--domain", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--judge", choices=["ollama"], default=None,
                   help="fill/refresh the closure-judgement cache from a live local Ollama call; "
                        "omit for replay mode (cache only, no network)")
    args = p.parse_args(argv)
    run(args.ledger, domain=args.domain, out_dir=args.out, sibling_path=args.sibling,
       sidecar_path=args.sidecar, judge_mode=args.judge)


if __name__ == "__main__":
    main()
