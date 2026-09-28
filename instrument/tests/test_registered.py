import re
from pathlib import Path

from probe_code import k0

DESIGN = Path(__file__).parents[2] / "research" / "experiment-ai-assisted-cta-physics.md"


def test_k0_code_uses_the_registered_numbers():
    text = DESIGN.read_text()
    assert k0.THRESHOLD == int(re.search(r"Stop\*\* Stage B if fewer than (\d+)% of errors", text).group(1)) / 100
    assert k0.MIN_ERRORED == int(re.search(r"until (\d+) solutions containing an error are coded", text).group(1))
    assert k0.KAPPA_TARGET == float(re.search(r"Target κ ≥ (0\.\d+)", text).group(1))
