#!/usr/bin/env python3
"""Prove session_start_lessons.py injects what it should and invents nothing.

The shipped lessons-loop suite skips this hook because the project edits it, so these are its
project-owned checks. Each case builds a throwaway project and runs the real hook against it.

    python3 scripts/hook_tests/test_session_start_lessons.py

No dependencies. Exits non-zero on any failure.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOOK = ROOT / ".claude/hooks/session_start_lessons.py"
CHECKER = ROOT / "scripts/lessons_graph.py"

ARCHIVE = """# Lessons — archive

## Applied

## 2026-01-01 — drain 1

| id | rule | home | commit | edges |
|------|------|------|--------|-------|
| L1.1 | Run the thing before saying it works. | `CLAUDE.md` | abc1234 | — |
"""

failures: list[str] = []
passed = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global passed
    if condition:
        passed += 1
        print(f"  ok   {name}")
    else:
        failures.append(f"{name}: {detail}")
        print(f"  FAIL {name}")


def run(archive: str | bytes | None = None, settings: str | None = None) -> str:
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts").mkdir()
        shutil.copy(CHECKER, root / "scripts/lessons_graph.py")
        if archive is not None:
            (root / "docs").mkdir()
            path = root / "docs/LESSONS-ARCHIVE.md"
            path.write_bytes(archive if isinstance(archive, bytes) else archive.encode())
        if settings is not None:
            (root / ".claude").mkdir()
            (root / ".claude/settings.json").write_text(settings)
        env = {k: v for k, v in os.environ.items() if not k.startswith("LESSONS_")}
        env["CLAUDE_PROJECT_DIR"] = str(root)
        out = subprocess.run([sys.executable, str(HOOK)], capture_output=True, text=True, env=env)
        return out.stdout


def context(stdout: str) -> str:
    return json.loads(stdout)["hookSpecificOutput"]["additionalContext"] if stdout.strip() else ""


def main() -> int:
    print("session_start_lessons.py")
    out = run()
    check("no ledger and no settings: emits nothing", out == "", repr(out))

    out = run(archive=b"\x00\x01 not markdown \xff" * 200)
    check("unreadable archive, no settings: emits nothing rather than something reassuring",
          out == "", repr(out))

    ctx = context(run(archive=ARCHIVE))
    check("a live rule is injected", "Run the thing before saying it works." in ctx, ctx)
    check("a missing settings.json is not reported as unreadable", "cannot run" not in ctx, ctx)

    ctx = context(run(archive=ARCHIVE, settings="{not json"))
    check("an unreadable settings.json is reported", "could not read .claude/settings.json" in ctx, ctx)

    missing = json.dumps({"hooks": {"PreToolUse": [{"matcher": "Bash", "hooks": [
        {"type": "command", "command": '"$CLAUDE_PROJECT_DIR"/.claude/hooks/gone.sh'}]}]}})
    ctx = context(run(archive=ARCHIVE, settings=missing))
    check("a registered hook whose script is missing is reported", ".claude/hooks/gone.sh" in ctx, ctx)

    print(f"\n{passed} passed, {len(failures)} failed")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
