import krippendorff
import numpy as np


def alpha_nominal(a: dict[str, str], b: dict[str, str]) -> float:
    units = sorted(set(a) | set(b))
    labels = sorted({*a.values(), *b.values()})
    code = {label: i for i, label in enumerate(labels)}
    data = np.array([[code[c[u]] if u in c else np.nan for u in units] for c in (a, b)], dtype=float)
    return float(krippendorff.alpha(reliability_data=data, level_of_measurement="nominal"))


def cohen_kappa(a: dict[str, str], b: dict[str, str]) -> float:
    units = sorted(set(a) & set(b))
    n = len(units)
    observed = sum(a[u] == b[u] for u in units) / n
    labels = {a[u] for u in units} | {b[u] for u in units}
    expected = sum((sum(a[u] == k for u in units) / n) * (sum(b[u] == k for u in units) / n) for k in labels)
    return (observed - expected) / (1 - expected)


def decoy_false_rate(judgments: dict[str, bool], is_decoy: dict[str, bool]) -> float:
    decoys = [i for i in judgments if is_decoy[i]]
    return sum(judgments[i] for i in decoys) / len(decoys)


def guess_rate(guesses: dict[str, str], truth: dict[str, str]) -> float:
    return sum(guesses[s] == truth[s] for s in guesses) / len(guesses)
