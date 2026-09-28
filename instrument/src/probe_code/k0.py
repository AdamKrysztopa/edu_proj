"""K0 decision rules, as registered in research/experiment-ai-assisted-cta-physics.md and extended by research/roadmap.md M1.

Codes are `<top>[.<subcode>]`; only the registered top level decides K0.
"""
import random
from dataclasses import dataclass
from math import sqrt

from probe_code.agreement import cohen_kappa

ERROR_CODES = {"PM", "SR", "OT"}
NON_ERROR_CODES = {"BLANK", "CORRECT"}
THRESHOLD = 0.30
MIN_ERRORED = 100
KAPPA_TARGET = 0.70
FORM_AGREEMENT_MIN_N = 60
PAIRS = {"K0-1": "K0-1b", "K0-2": "K0-2b"}
COMPONENTS = {"K0-1": ("C1a", "C1b"), "K0-2": ("C2a", "C2b")}
Z95 = 1.959963984540054


def wilson(k: int, n: int, z: float = Z95) -> tuple[float, float]:
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return centre - half, centre + half


def top(code: str) -> str:
    t = code.split(".")[0]
    if t not in ERROR_CODES | NON_ERROR_CODES:
        raise ValueError(f"unknown K0 code {code!r}")
    return t


def _by_student(rows: list[dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for r in rows:
        if r.get("top") and r["top"] != top(r["code"]):
            raise ValueError(f"student {r['student_id']}: top {r['top']!r} does not match code {r['code']!r}")
        top(r["code"])
        if r["student_id"] in out:
            raise ValueError(f"student {r['student_id']} has more than one coded solution; K0 codes one item per student")
        out[r["student_id"]] = r
    return out


def sample_plan(student_ids: list[str], items: list[str], seed: int, exclude: set[str] = frozenset()) -> list[dict]:
    rng = random.Random(seed)
    order = sorted(set(student_ids) - set(exclude))
    rng.shuffle(order)
    return [{"order": i, "student_id": s, "item_id": rng.choice(items)} for i, s in enumerate(order, 1)]


def follow_plan(rows: list[dict], plan: list[dict], min_errored: int = MIN_ERRORED) -> tuple[list[dict], int]:
    """Coded rows in plan order, cut after the min_errored-th errored solution; also the count of rows cut."""
    coded = _by_student(rows)
    planned = {p["student_id"]: p["item_id"] for p in plan}
    unregistered = sorted({i for i in planned.values() if i not in COMPONENTS})
    if unregistered:
        raise ValueError(f"the plan draws {unregistered}; K0 is decided on the registered Form 1 items {sorted(COMPONENTS)}")
    for s, r in coded.items():
        if s not in planned:
            raise ValueError(f"student {s} is not in the coding plan")
        if r["item_id"] != planned[s]:
            raise ValueError(f"student {s}: coded {r['item_id']}, but the plan drew {planned[s]}")
    ordered = [coded[p["student_id"]] for p in sorted(plan, key=lambda p: int(p["order"])) if p["student_id"] in coded]
    positions = [int(p["order"]) for p in sorted(plan, key=lambda p: int(p["order"])) if p["student_id"] in coded]
    first_order = min(int(p["order"]) for p in plan)
    for expected, (pos, r) in enumerate(zip(positions, ordered), first_order):
        if pos != expected:
            gap = next(p["student_id"] for p in plan if int(p["order"]) == expected)
            raise ValueError(f"student {gap} (plan position {expected}) is uncoded but later students are coded")
    kept, errored = [], 0
    for r in ordered:
        if errored == min_errored:
            break
        kept.append(r)
        errored += top(r["code"]) in ERROR_CODES
    return kept, len(ordered) - len(kept)


@dataclass(frozen=True)
class Decision:
    errored: int
    selection_representation: int
    blank: int
    correct: int
    share: float
    ci: tuple[float, float]
    decision: str
    ignored: int


def decide(rows: list[dict], plan: list[dict], early: bool = False,
           threshold: float = THRESHOLD, min_errored: int = MIN_ERRORED) -> Decision:
    kept, ignored = follow_plan(rows, plan, min_errored)
    tops = [top(r["code"]) for r in kept]
    errored = sum(t in ERROR_CODES for t in tops)
    sr = tops.count("SR")
    share = sr / errored if errored else 0.0
    ci = wilson(sr, errored) if errored else (0.0, 1.0)
    if errored < min_errored:
        if not early:
            raise ValueError(f"pretest K0 needs {min_errored} errored solutions; {errored} coded")
        decision = "inconclusive"
    else:
        decision = "stop" if share < threshold else "continue"
    return Decision(errored, sr, tops.count("BLANK"), tops.count("CORRECT"), share, ci, decision, ignored)


@dataclass(frozen=True)
class Agreement:
    n: int
    raw_agreement: float
    kappa: float


def _agreement(a: dict[str, str], b: dict[str, str]) -> Agreement:
    units = list(a)
    raw = sum(a[u] == b[u] for u in units) / len(units) if units else 0.0
    kappa = cohen_kappa(a, b) if len(set(a.values()) | set(b.values())) > 1 else float("nan")
    return Agreement(len(units), raw, kappa)


def coder_kappa(coder_a: list[dict], coder_b: list[dict], plan: list[dict],
                min_errored: int = MIN_ERRORED) -> Agreement:
    """Top-level agreement over the double-coded plan prefix: solutions either coder calls errored, up to min_errored."""
    a, b = _by_student(coder_a), _by_student(coder_b)
    units = []
    for p in sorted(plan, key=lambda p: int(p["order"])):
        s = p["student_id"]
        if len(units) == min_errored or s not in a or s not in b:
            continue
        if top(a[s]["code"]) in ERROR_CODES or top(b[s]["code"]) in ERROR_CODES:
            units.append(s)
    return _agreement({s: top(a[s]["code"]) for s in units}, {s: top(b[s]["code"]) for s in units})


@dataclass(frozen=True)
class ComponentShare:
    passed_both: int
    selection_representation: int
    failed_any: int
    missing: int


def component_share(codes: list[dict], components: list[dict]) -> ComponentShare:
    """Among errored students: who passed both components of their coded item, and how many of those erred on SR."""
    results: dict[tuple[str, str], bool] = {
        (r["student_id"], r["component_id"]): r["correct"].strip() in {"1", "true", "yes"} for r in components}
    passed_both = sr = failed = missing = 0
    for s, r in _by_student(codes).items():
        t = top(r["code"])
        if t not in ERROR_CODES:
            continue
        needed = COMPONENTS[r["item_id"]]
        if any((s, c) not in results for c in needed):
            missing += 1
        elif all(results[(s, c)] for c in needed):
            passed_both += 1
            sr += t == "SR"
        else:
            failed += 1
    return ComponentShare(passed_both, sr, failed, missing)


@dataclass(frozen=True)
class FormAgreement:
    n: int
    raw_agreement: float
    kappa: float
    sufficient: bool
    ci: tuple[float, float]


def form_agreement(form1: list[dict], form2: list[dict]) -> FormAgreement:
    a, b = _by_student(form1), _by_student(form2)
    for s in a.keys() & b.keys():
        if PAIRS.get(a[s]["item_id"]) != b[s]["item_id"]:
            raise ValueError(f"student {s}: {a[s]['item_id']} is not paired with {b[s]['item_id']}")
    both = [s for s in a if s in b and top(a[s]["code"]) in ERROR_CODES and top(b[s]["code"]) in ERROR_CODES]
    ta, tb = {s: top(a[s]["code"]) for s in both}, {s: top(b[s]["code"]) for s in both}
    g = _agreement(ta, tb)
    return FormAgreement(g.n, g.raw_agreement, g.kappa, g.n >= FORM_AGREEMENT_MIN_N, bootstrap_kappa(ta, tb))


def bootstrap_kappa(a: dict[str, str], b: dict[str, str], reps: int = 2000, seed: int = 0) -> tuple[float, float]:
    """Percentile 95% interval, resampling students; draws with a single category are skipped."""
    units = list(a)
    if len(units) < 2:
        return float("nan"), float("nan")
    rng = random.Random(seed)
    kappas = []
    for _ in range(reps):
        draw = [rng.choice(units) for _ in units]
        da = {f"{i}": a[u] for i, u in enumerate(draw)}
        db = {f"{i}": b[u] for i, u in enumerate(draw)}
        if len(set(da.values()) | set(db.values())) > 1:
            kappas.append(cohen_kappa(da, db))
    kappas.sort()
    return kappas[int(0.025 * len(kappas))], kappas[int(0.975 * len(kappas)) - 1]
