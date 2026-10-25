"""I12 offline replay. Run with the gapmap dev environment; writes only --out.

    uv run --directory gapmap python ../research/area_score/predictor_replay.py

The synthetic diagnostic reuses the committed phase-1 test specification and
is written separately. It never supplies data to an observed-pool evaluation.
"""
from __future__ import annotations

import argparse
import json
import runpy
from pathlib import Path

from gapmap import area

ROOT = Path(__file__).resolve().parents[2]
RUNS = {"plc": "20260928T133336Z-59ec876b3d7e", "gdpr_v1": "20260928T135354Z-eb840a85b7d1",
        "gdpr_v2": "20260928T145943Z-bc1cc9a30a02"}


def replay(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for domain, run_id in RUNS.items():
        run = ROOT / "reconstruct/runs" / run_id
        sibling = {"gdpr_v1": "gdpr_v2", "gdpr_v2": "gdpr_v1"}.get(domain)
        result = area.replay_predictors(
            ledger_path=run / "ledger.json", sidecar_path=run / "sidecar.json", domain=domain,
            cache_path=ROOT / "research/n3" / domain / "closure_judgements.json",
            sibling_path=ROOT / "reconstruct/runs" / RUNS[sibling] / "ledger.json" if sibling else None,
        )
        (out / f"{domain}.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    fixture = runpy.run_path(str(ROOT / "gapmap/tests/test_predictor_rules.py"))["synthetic_controls"]
    spec_sha, positive, reference, lengths, covariates = fixture()
    inputs = dict(reference=reference, covariates=covariates, text_lengths=lengths,
                  area_ids=["synthetic"] * len(reference), partition={"synthetic": ()})
    diagnostic = {"label": "SYNTHETIC", "purpose": "pipeline diagnostic only; never a criterion or research gate input",
                  "spec_sha256": spec_sha, "spec_source": "gapmap/tests/test_predictor_rules.py:synthetic_controls",
                  "n": len(reference), "positive": area.evaluate_predictor(scores=positive, **inputs),
                  "source_count_plant": area.evaluate_predictor(scores=covariates["k_topic"], **inputs)}
    (out / "synthetic").mkdir(exist_ok=True)
    (out / "synthetic/l73.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path(__file__).resolve().parent / "predictors")
    replay(parser.parse_args().out)
