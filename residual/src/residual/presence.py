"""Sealed presence check for an acquired gold list (REORIENTATION.md §22, methods-critic 2026-10-24):
confirms a list exists and how many items it holds, without showing any item to a human.

    uv run --directory residual python -m residual.presence <gold file>
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

TABULAR = {".csv": ",", ".tsv": "\t"}


def count_items(path: Path) -> int:
    """Items in a JSON list, or data rows of a CSV/TSV after its header; any other text file counts
    its non-empty lines."""
    if path.suffix == ".json":
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            raise ValueError("a JSON gold must be a top-level list")
        return len(data)
    if path.suffix in TABULAR:
        with path.open(newline="", encoding="utf-8") as f:
            rows = [r for r in csv.reader(f, delimiter=TABULAR[path.suffix]) if any(c.strip() for c in r)]
        return max(len(rows) - 1, 0)
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def presence(path: Path) -> str:
    """One line, never item text: a parse error is named by its type only, since its message can
    quote the file."""
    if not path.is_file():
        return "list absent"
    try:
        n = count_items(path)
    except (OSError, ValueError, UnicodeDecodeError, csv.Error) as e:
        return f"list unreadable ({type(e).__name__})"
    if n == 0:
        return "list empty"
    return f"list present, {n} rows, sha256 {hashlib.sha256(path.read_bytes()).hexdigest()}"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python -m residual.presence <gold file>")
        sys.exit(2)
    line = presence(Path(sys.argv[1]))
    print(line)
    sys.exit(0 if line.startswith("list present") else 1)
