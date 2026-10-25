"""I9 replay: the provenance rules before and after the fix, over the committed N2 runs, offline.

    uv run --directory reconstruct python ../research/n2/provenance_fixes_replay.py [--before REV]

"Before" is `evidence.py` and `verify_run.py` at REV (default d413a4b), loaded from git; "after"
is the working tree. No model is called: the replay re-applies each rule to the
verdicts, quotes and flags the runs recorded, and to the git-ignored snapshots under
`reconstruct/runs/<run>/snapshots/`. Prints one JSON object per run.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

from reconstruct import evidence as new_ev
from reconstruct import run as new_run
from reconstruct import verify_run as new_verify
from residual.ledger import Ledger
from residual.provenance import Verdict

REPO = Path(__file__).resolve().parents[2]
RUNS = REPO / "reconstruct" / "runs"


def _load_at(rev: str, rel: str, name: str):
    src = subprocess.run(["git", "-C", str(REPO), "show", f"{rev}:{rel}"], check=True,
                         capture_output=True, text=True).stdout
    path = Path(tempfile.mkdtemp()) / f"{name}.py"
    path.write_text(src)
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _slot_status(n: int, verifier_ran_all: bool) -> str:
    return new_ev.slot_status(n_criterion_clusters=n, docs_fetched_and_extracted=True,
                              area_lost_to_truncation=False, verifier_ran_on_all_located=verifier_ran_all)


def replay(run_dir: Path, old_ev, old_verify) -> dict:
    sidecar = json.loads((run_dir / "sidecar.json").read_text())
    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    out: dict = {"run": run_dir.name, "n_claims": len(ledger.claims)}
    out["verify_run"] = {"before": len(old_verify.verify_run(run_dir)),
                         "after": new_verify.verify_run(run_dir)}
    if not ledger.claims:
        return out

    snap = run_dir / "snapshots"
    text_by_source = {sid: (snap / f"{s['text_sha256']}.txt").read_text(encoding="utf-8")
                      for sid, s in sidecar["sources"].items() if s.get("text_sha256")}
    folded = {sid: new_ev.fold(t) for sid, t in text_by_source.items()}
    area_names = {a["area_id"]: a["name"] for a in sidecar["areas"]}

    # quote_in_span: re-check every recorded per-extraction verdict against its own span.
    flips: Counter = Counter()
    flipped_locators: set[tuple[str, str]] = set()
    recorded = [e for e in sidecar["extractions"] if "verify_verdict" in e]
    for e in recorded:
        if e["verify_verdict"] not in ("supports", "refutes") or not e["located"]:
            continue
        doc = text_by_source[e["source_id"]]
        span = new_ev.locate_span(e["quote"], doc)
        quote = e["verify_supporting_quote"] or ""
        assert old_ev.quote_in_span(quote, span.exact), e
        if not new_ev.quote_in_span(quote, span.exact):
            flips[f"{e['verify_verdict']}->insufficient"] += 1
            sha = sidecar["sources"][e["source_id"]]["text_sha256"]
            flipped_locators.add((e["claim_id"], f"sha256:{sha};char={span.start},{span.end}"))
    out["quote_in_span"] = {"replayable": bool(recorded), "verdicts_checked": sum(
        1 for e in recorded if e["verify_verdict"] in ("supports", "refutes")), "flips": dict(flips)}

    def after_quote(c):
        ev = tuple(e.model_copy(update={"verification": e.verification.model_copy(
            update={"verdict": Verdict.INSUFFICIENT})}) if (c.claim_id, e.selector.locator) in flipped_locators
            else e
            for e in c.evidence)
        return c.model_copy(update={"evidence": ev})

    claims = {c.claim_id: after_quote(c) for c in ledger.claims}

    # R3 at merge: identical-assertion claims carrying supporting spans from 2+ clusters.
    merge_copies = 0
    for c in claims.values():
        sup = c.supporting
        if len({e.source.independence_key for e in sup}) < 2:
            continue
        merge_copies += len(new_ev.collapse_verbatim_copies([
            new_ev.CopyItem(str(i), e.source.independence_key, e.selector.exact,
                            folded[e.source.source_id]) for i, e in enumerate(sup)]))
    out["merge"] = {"claims_corroboration_ge2_before": sum(1 for c in ledger.claims if c.corroboration >= 2),
                    "members_dropped_after": merge_copies}

    # R3 at cross-verify: which candidates the fixed filter withholds from the verifier.
    by_area: dict[str, list[str]] = {}
    for cid, aid in ledger.assignments:
        if cid in claims and claims[cid].supporting:
            by_area.setdefault(aid, []).append(cid)
    old_spans = [(e.selector.locator, e.source.independence_key, e.selector.exact or "")
                 for c in claims.values() for e in c.evidence if e.selector.locator]
    old_dup, new_dup = old_ev.span_duplicates(old_spans), new_ev.span_duplicates(old_spans)
    cv = Counter()
    withheld_words: list[int] = []
    for aid, cids in by_area.items():
        first = {cid: claims[cid].supporting[0] for cid in cids}
        for cid in cids:
            claim = claims[cid]
            own_keys = {e.source.independence_key for e in claim.evidence}
            old_cands, new_cands = [], []
            for other in cids:
                o = first[other]
                if other == cid or o.source.independence_key in own_keys:
                    continue
                old_ok = old_dup[o.selector.locator] not in {old_dup[e.selector.locator] for e in claim.evidence}
                new_ok = (new_dup[o.selector.locator] not in {new_dup[e.selector.locator] for e in claim.evidence}
                          and not any(new_ev.is_verbatim_copy(
                              e.selector.exact, folded[e.source.source_id], o.selector.exact,
                              folded[o.source.source_id]) for e in claim.evidence))
                if old_ok:
                    old_cands.append((other, o))
                if new_ok:
                    new_cands.append((other, o))
                if old_ok and not new_ok:
                    withheld_words.append(new_ev.word_count(o.selector.exact))

            def top2(cands):
                return [x[0] for x in sorted(cands, key=lambda item: (
                    -new_ev.jaccard(new_ev.content_words(claim.assertion),
                                    new_ev.content_words(item[1].selector.exact or "")), item[0]))[:2]]

            t_old, t_new = top2(old_cands), top2(new_cands)
            cv["pairs_before"] += len(old_cands)
            cv["pairs_after"] += len(new_cands)
            cv["top2_calls_before"] += len(t_old)
            cv["top2_calls_after"] += len(t_new)
            cv["top2_calls_withheld"] += len(set(t_old) - {x[0] for x in new_cands})
            cv["claims_with_changed_top2"] += t_old != t_new
    if withheld_words:
        cv["withheld_span_words_min"] = min(withheld_words)
        cv["withheld_span_words_median"] = sorted(withheld_words)[len(withheld_words) // 2]
    cv["span_dup_groups_before"] = sum(1 for k, v in old_dup.items() if k != v)
    cv["span_dup_groups_after"] = sum(1 for k, v in new_dup.items() if k != v)
    out["cross_verify_candidates"] = dict(cv)

    # R4: scope-flagged REFUTES among recorded cross-checks.
    cross = sidecar.get("cross_checks")
    out["contradictions"] = {
        "ledger_before": len(ledger.contradictions),
        "methods": sorted({c.method.split(":")[0] for c in ledger.contradictions}),
        "cross_checks_recorded": None if cross is None else len(cross),
        "scope_flagged_refutes": None if cross is None else sum(
            1 for c in cross if c["verdict"] == "refutes" and c["subject_or_scope_differs"]),
    }
    out["contradictions"]["ledger_after"] = (out["contradictions"]["ledger_before"]
                                             - (out["contradictions"]["scope_flagged_refutes"] or 0))

    # Slots: recorded status, the current rule replayed, and the fixed rule.
    transitions: Counter = Counter()
    changed = []
    slot_copies = 0
    for slot in sidecar["slots"]:
        if slot["status"] not in ("covered", "thin") and not slot["claim_ids"]:
            transitions[(slot["status"], slot["status"], slot["status"])] += 1
            continue
        slot_claims = [claims[cid] for cid in slot["claim_ids"]]
        ran_all = all(e.verification.verdict is not Verdict.PENDING for c in slot_claims for e in c.evidence)
        n_before = len({e.source.independence_key for cid in slot["claim_ids"]
                        for e in ledger.by_id[cid].supporting})
        n_after, n_copies = new_run._independent_support(slot_claims, folded)
        slot_copies += n_copies
        before = (_slot_status(n_before, ran_all) if slot["status"] in ("covered", "thin", "unknown")
                  else slot["status"])
        after = _slot_status(n_after, ran_all) if before in ("covered", "thin") or n_after else before
        transitions[(slot["status"], before, after)] += 1
        if before != after:
            changed.append({"area": area_names.get(slot["area_id"]), "probe": slot["probe"],
                            "clusters": [n_before, n_after], "copies": n_copies, "status": [before, after]})
    out["slots"] = {"transitions_recorded_current_fixed": {"|".join(k): v for k, v in sorted(transitions.items())},
                    "changed": changed, "copy_spans_in_slots": slot_copies}
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--before", default="d413a4b")
    args = p.parse_args()
    old_ev = _load_at(args.before, "reconstruct/src/reconstruct/evidence.py", "evidence_before")
    old_verify = _load_at(args.before, "reconstruct/src/reconstruct/verify_run.py", "verify_run_before")
    for run_dir in sorted(RUNS.iterdir()):
        if (run_dir / "ledger.json").exists():
            print(json.dumps(replay(run_dir, old_ev, old_verify), default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
