"""D1b plan §2.2 G1: the N3 L7.3 fixtures through `research/n3_control_v3/l73.py`, rule unchanged,
with outputs under `research/d1b_rerun/g1/<tag>/` instead of the N3 control record. Same flags.

    uv run --directory gapmap python ../research/d1b_rerun/g1.py --tag gemma3 --model gemma3:12b --judge ollama
"""
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("l73", HERE.parent / "n3_control_v3" / "l73.py")
l73 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(l73)
l73.HERE = HERE / "g1"

if __name__ == "__main__":
    l73.main()
