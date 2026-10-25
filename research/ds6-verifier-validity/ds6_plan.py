"""DS6 planning figures. SYNTHETIC: simulated from a specification; informs design, never a gate."""
import math
import random
from math import comb


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - h) / d, (c + h) / d


def p_mcnemar(b, c):
    m = b + c
    return 1.0 if m == 0 else sum(comb(m, i) for i in range(b, m + 1)) / 2 ** m


def power(n, pu, q, r, sims=20000, seed=20261024):
    """Ungated adopts w.p. pu; the gated arm keeps a fraction q of those adoptions and adopts
    on its own w.p. r where the ungated arm did not. Returns P(one-sided exact McNemar p < .05)."""
    rnd = random.Random(seed)
    hits = 0
    for _ in range(sims):
        b = c = 0
        for _ in range(n):
            if rnd.random() < pu:
                b += rnd.random() >= q
            else:
                c += rnd.random() < r
        hits += p_mcnemar(b, c) < 0.05
    return hits / sims


def p_floor(n, pu, frac):
    f = math.ceil(frac * n)
    return sum(comb(n, i) * pu ** i * (1 - pu) ** (n - i) for i in range(f, n + 1))


def n_for_upper(true, bound, z=1.645):
    # p held at `true`: rounding k = round(true * n) makes the first crossing an artefact.
    return next(n for n in range(10, 5000) if wilson(true * n, n, z)[1] <= bound)


print("min b with c = 0:", [(b, round(p_mcnemar(b, 0), 4)) for b in range(3, 7)])
for n in (24, 48):
    for pu in (0.21, 0.4, 0.5, 0.6):
        pw = [round(power(n, pu, q, 0.05), 2) for q in (0.0, 0.25, 0.5)]
        print(f"n={n} pu={pu} power q=0/.25/.5 (r=.05)={pw} "
              f"P(floor n/3)={p_floor(n, pu, 1/3):.3f} P(floor .4n)={p_floor(n, pu, 0.4):.3f}")
for p, n in ((0.12, 125), (0.15, 125), (0.20, 50)):
    lo, hi = wilson(round(p * n), n)
    print(f"Wilson at p={p} n={n}: {lo:.3f}-{hi:.3f}")
for prev in (0.03, 0.05):
    print(f"n for P(see >=1 of a {prev:.0%} code) >= .95:", math.ceil(math.log(0.05) / math.log(1 - prev)))
for true, bound in ((0.10, 0.15), (0.12, 0.15), (0.12, 0.20)):
    print(f"n for one-sided 95% upper <= {bound} at true {true}:", n_for_upper(true, bound))
