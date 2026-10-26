"""D1b plan §2.2 G4 condition, stated before any judge result: run the length, source-count,
lexical-overlap, specificity, closing-lexicon and coin-flip stand-ins through the gap map's own
mismatched-evidence control on the real D1 ledgers. G4 may gate only if every stand-in fails it
(own - control < 0.20 in total). $0, no model.

    uv run --directory gapmap python ../research/d1b_rerun/g4_standins.py
"""
from __future__ import annotations

import glob
import hashlib
import json
from pathlib import Path

from residual.ledger import Ledger

from gapmap import checks, lenses, link, standins, text

HERE = Path(__file__).resolve().parent
D1 = HERE.parent / "d1_demonstrator" / "runs"
LEDGERS = {"cheap-26b": D1 / "cheap-26b", "toptier-26b": D1 / "toptier-26b"}
PASS_DIFF = 0.20


def _ledger_path(run_dir: Path) -> Path:
    (path,) = glob.glob(str(run_dir / "*" / "ledger.json"))
    return Path(path)


def _source_of_sentence(ledger: Ledger, index: link.Index) -> dict[str, str]:
    out = {}
    for cid, body in index.T.items():
        src = checks._source_of(ledger, cid)
        for sent in text.sentences(body):
            out.setdefault(sent, src)
    return out


def measure(ledger_path: Path) -> dict:
    ledger_text = ledger_path.read_text()
    ledger = Ledger.from_json(ledger_text)
    sha = hashlib.sha256(ledger_text.encode()).hexdigest()
    index = link.build_index(ledger)
    cands = lenses.run_all(ledger, index, link.SETTING_1)
    rec = standins.RecordingJudge()
    checks.mismatched_evidence_control(ledger, sha, index, rec, cands)
    judges = [standins.calibrate("length", standins.length, rec.prompts),
              standins.calibrate("overlap", standins.overlap, rec.prompts),
              standins.calibrate("specificity", standins.specificity, rec.prompts),
              standins.calibrate("sources", standins.source_count(_source_of_sentence(ledger, index)), rec.prompts),
              standins.LexiconJudge(), standins.CoinFlipJudge()]
    rows = {}
    for j in judges:
        total = checks.mismatched_evidence_control(ledger, sha, index, j, cands)["total"]
        diff = total["own_rate"] - total["control_rate"]
        rows[j.model_id] = {"own_rate": round(total["own_rate"], 3), "control_rate": round(total["control_rate"], 3),
                            "diff": round(diff, 3), "passes_g4": diff >= PASS_DIFF, "n": total["n"]}
    return {"ledger_sha256": sha, "prompts": len(rec.prompts), "stand_ins": rows}


def main() -> int:
    result = {name: measure(_ledger_path(d)) for name, d in LEDGERS.items()}
    result["g4_may_gate"] = not any(r["passes_g4"] for v in result.values() if isinstance(v, dict)
                                    for r in v["stand_ins"].values())
    (HERE / "g4_standins.json").write_text(json.dumps(result, indent=1, sort_keys=True) + "\n")
    for name in LEDGERS:
        for jid, r in result[name]["stand_ins"].items():
            print(name, jid, r["own_rate"], r["control_rate"], r["diff"], "PASSES" if r["passes_g4"] else "fails")
    print("g4_may_gate", result["g4_may_gate"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
