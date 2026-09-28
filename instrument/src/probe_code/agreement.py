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


def masi_distance(x: frozenset[str], y: frozenset[str]) -> float:
    """Passonneau (2006): 1 - Jaccard * monotonicity (1 equal, 2/3 subset, 1/3 overlap, 0 disjoint)."""
    if x == y:
        return 0.0
    monotonicity = 2 / 3 if x <= y or y <= x else 1 / 3 if x & y else 0.0
    return 1 - len(x & y) / len(x | y) * monotonicity


def alpha_masi(a: dict[str, frozenset[str]], b: dict[str, frozenset[str]]) -> float:
    """Krippendorff's alpha for two coders with MASI distance; units only one coder coded are unpairable."""
    units = sorted(set(a) & set(b))
    values = [a[u] for u in units] + [b[u] for u in units]
    n = len(values)
    observed = sum(masi_distance(a[u], b[u]) for u in units) / len(units)
    expected = sum(masi_distance(x, y) for i, x in enumerate(values) for j, y in enumerate(values) if i != j)
    return float("nan") if expected == 0 else 1 - observed / (expected / (n * (n - 1)))


def per_code_kappa(a: dict[str, frozenset[str]], b: dict[str, frozenset[str]]) -> dict[str, dict]:
    units = sorted(set(a) & set(b))
    n = len(units)
    out = {}
    for code in sorted(set().union(*(a[u] | b[u] for u in units))):
        pa = [code in a[u] for u in units]
        pb = [code in b[u] for u in units]
        observed = sum(x == y for x, y in zip(pa, pb)) / n
        ra, rb = sum(pa) / n, sum(pb) / n
        expected = ra * rb + (1 - ra) * (1 - rb)
        kappa = float("nan") if expected == 1 else (observed - expected) / (1 - expected)
        out[code] = {"kappa": kappa, "a": sum(pa), "b": sum(pb), "units": n}
    return out


def decoy_false_rate(judgments: dict[str, bool], is_decoy: dict[str, bool]) -> float:
    decoys = [i for i in judgments if is_decoy[i]]
    return sum(judgments[i] for i in decoys) / len(decoys)


def guess_rate(guesses: dict[str, str], truth: dict[str, str]) -> float:
    return sum(guesses[s] == truth[s] for s in guesses) / len(guesses)
