"""Guard calibration (decision 0004, `guard-calibrated-before-freeze`): human labels are the reference."""
import random
from dataclasses import dataclass

from probe_code.agreement import cohen_kappa
from probe_code.k0 import wilson

from pathlib import Path

ITEMS_PATH = Path(__file__).parents[2] / "calibration" / "items.csv"
SHEET_COLUMNS = ("item_id", "problems", "expert_said", "question")


def labelling_sheet(items: list[dict], seed: int) -> list[dict]:
    rows = [{k: r[k] for k in SHEET_COLUMNS} | {"leading": "", "introduced": "", "origin_guess": ""} for r in items]
    random.Random(f"calibration:{seed}").shuffle(rows)
    return rows


def run_guard(items: list[dict], guard) -> list[dict]:
    rows = []
    for r in items:
        v = guard.check(r["question"], r["problems"], r["expert_said"])
        rows.append({"item_id": r["item_id"], "flagged": v.flagged, "introduced": v.introduced})
    return rows


def _yes(value) -> bool:
    return str(value).strip().lower() in {"1", "true", "y", "yes"}


MIN_CLASS = 25


@dataclass(frozen=True)
class Report:
    leading: int
    not_leading: int
    sensitivity_by_stratum: dict[str, tuple[int, int]]
    sensitivity_rule: float
    sensitivity_rule_ci: tuple[float, float]
    specificity: float
    specificity_ci: tuple[float, float]
    labeller_raw_agreement: float
    labeller_kappa: float
    origin_guess_accuracy: float
    sufficient: bool


def _stratum(item: dict) -> str:
    return "natural" if item["origin"] == "original" else item["style"]


def report(items: list[dict], labels_a: list[dict], labels_b: list[dict], adjudicated: list[dict],
           verdicts: list[dict], min_class: int = MIN_CLASS) -> Report:
    """Sensitivity is reported per stratum; the decision uses natural and subtle items, not the explicit rewrites."""
    ids = [r["item_id"] for r in items]
    truth = {r["item_id"]: _yes(r["leading"]) for r in adjudicated}
    flagged = {r["item_id"]: _yes(r["flagged"]) for r in verdicts}
    for name, have in (("adjudicated label", truth), ("guard verdict", flagged)):
        missing = [i for i in ids if i not in have]
        if missing:
            raise ValueError(f"no {name} for {missing}")
    by_id = {r["item_id"]: r for r in items}
    lead = [i for i in ids if truth[i]]
    plain = [i for i in ids if not truth[i]]
    strata: dict[str, tuple[int, int]] = {}
    for i in lead:
        s = _stratum(by_id[i])
        k, n = strata.get(s, (0, 0))
        strata[s] = (k + flagged[i], n + 1)
    rule_k = sum(strata.get(s, (0, 0))[0] for s in ("natural", "subtle"))
    rule_n = sum(strata.get(s, (0, 0))[1] for s in ("natural", "subtle"))
    tn = sum(not flagged[i] for i in plain)
    a = {r["item_id"]: r for r in labels_a}
    b = {r["item_id"]: r for r in labels_b}
    shared = [i for i in ids if i in a and i in b]
    la = {i: str(_yes(a[i]["leading"])) for i in shared}
    lb = {i: str(_yes(b[i]["leading"])) for i in shared}
    raw = sum(la[i] == lb[i] for i in shared) / len(shared) if shared else 0.0
    kappa = cohen_kappa(la, lb) if len(set(la.values()) | set(lb.values())) > 1 else float("nan")
    guesses = [(r.get("origin_guess", "").strip().lower(), by_id[i]["origin"])
               for labels in (a, b) for i, r in labels.items() if i in by_id and r.get("origin_guess", "").strip()]
    correct = sum((g == "authored") == (o == "variant") for g, o in guesses)
    return Report(len(lead), len(plain), strata,
                  rule_k / rule_n if rule_n else float("nan"), wilson(rule_k, rule_n) if rule_n else (0.0, 1.0),
                  tn / len(plain) if plain else float("nan"), wilson(tn, len(plain)) if plain else (0.0, 1.0),
                  raw, kappa, correct / len(guesses) if guesses else float("nan"),
                  len(lead) >= min_class and len(plain) >= min_class)
