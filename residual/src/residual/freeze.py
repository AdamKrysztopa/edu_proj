"""Hash-freeze of the N1 schema and gap-map feature set (REORIENTATION.md §14.3, §22 N1),
after the FrozenConfig pattern of Track A: a test fails if either changes without a re-freeze.

    uv run --directory residual python -m residual.freeze --write
"""
from __future__ import annotations

import hashlib
import json
import sys
from enum import StrEnum
from pathlib import Path

from residual import vocab
from residual.claims import ClaimRecord, ResponseDistribution
from residual.gapmap import FEATURE_SET, AreaFeatures
from residual.gates import GateDecision, Measurement, Threshold
from residual.ledger import Ledger
from residual.residual import EstimatedResidual, GapMapPrediction, ResidualAccount

HERE = Path(__file__).resolve().parent
FROZEN = HERE.parents[1] / "frozen" / "n1.json"
MODELS = (ClaimRecord, ResponseDistribution, Ledger, Measurement, Threshold, GateDecision, ResidualAccount,
          EstimatedResidual, GapMapPrediction, AreaFeatures)


SEMANTICS = ("vocab.py", "provenance.py", "claims.py", "ledger.py", "gates.py", "residual.py")
"""The code that decides labels, gate admission and coverage: part of the freeze (L1.9)."""


def _sha(obj: object) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest()


def _structure(schema: object) -> object:
    """A JSON schema without prose, so rewording a docstring is not a schema change. Under
    'properties' and '$defs' the keys are names, which are structure, whatever they are."""
    if isinstance(schema, list):
        return [_structure(v) for v in schema]
    if not isinstance(schema, dict):
        return schema
    out = {}
    for k, v in schema.items():
        if k in ("properties", "$defs"):
            out[k] = {name: _structure(sub) for name, sub in v.items()}
        elif k not in ("description", "title"):
            out[k] = _structure(v)
    return out


def fingerprint() -> dict[str, str]:
    vocabularies = {name: [m.value for m in cls] for name, cls in vars(vocab).items()
                    if isinstance(cls, type) and issubclass(cls, StrEnum) and cls is not StrEnum}
    return {
        "schema_sha256": _sha({"models": {m.__name__: _structure(m.model_json_schema())
                                          for m in MODELS},
                               "vocabularies": vocabularies}),
        "features_sha256": _sha(list(FEATURE_SET)),
        "semantics_sha256": _sha({f: hashlib.sha256((HERE / f).read_bytes()).hexdigest()
                                  for f in SEMANTICS}),
    }


def frozen() -> dict[str, str]:
    return {k: v for k, v in json.loads(FROZEN.read_text()).items() if k.endswith("_sha256")}


if __name__ == "__main__" and sys.argv[1:] == ["--write"]:
    FROZEN.write_text(json.dumps({**fingerprint(), "frozen_by": "N1"}, indent=2) + "\n")
