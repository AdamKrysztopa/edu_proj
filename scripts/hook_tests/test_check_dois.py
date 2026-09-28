#!/usr/bin/env python3
"""Prove the DOI hook is registered, runs, and blocks — without the network.

The hook once sat registered under a deleted filename and never ran, so "the file
exists" is not the check. Here the command string is read from .claude/settings.json
and executed as Claude Code would, and each verdict path is shown firing.

    python3 scripts/hook_tests/test_check_dois.py

No dependencies. Exits non-zero on any failure.
"""

from __future__ import annotations

import importlib.util
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETTINGS = ROOT / ".claude/settings.json"
HOOK = ROOT / ".claude/hooks/check-dois.py"

failures: list[str] = []
passed = 0


def check(name: str, condition: bool, detail: str = "") -> None:
    global passed
    if condition:
        passed += 1
        print(f"  ok   {name}")
    else:
        failures.append(f"{name}: {detail}")
        print(f"  FAIL {name}: {detail}")


def registered_command() -> tuple[str, str]:
    settings = json.loads(SETTINGS.read_text())
    for group in settings["hooks"]["PostToolUse"]:
        for hook in group["hooks"]:
            if "check-dois" in hook["command"]:
                return group["matcher"], hook["command"]
    return "", ""


def project_with_hook() -> Path:
    """A throwaway project root holding the real hook, so its cache write stays out of the repo."""
    root = Path(tempfile.mkdtemp())
    (root / ".claude/hooks").mkdir(parents=True)
    shutil.copy2(HOOK, root / ".claude/hooks/check-dois.py")
    return root


def run_registered(command: str, root: Path, file: Path) -> subprocess.CompletedProcess:
    event = {"tool_name": "Edit", "tool_input": {"file_path": str(file)}}
    # A dead proxy makes every doi.org lookup fail the same way on every machine.
    env = {**os.environ, "CLAUDE_PROJECT_DIR": str(root),
           "https_proxy": "http://127.0.0.1:9", "HTTPS_PROXY": "http://127.0.0.1:9",
           "no_proxy": "", "NO_PROXY": ""}
    return subprocess.run(["/bin/sh", "-c", command], input=json.dumps(event), text=True,
                          capture_output=True, env=env, timeout=60)


def load_hook(cache: Path):
    spec = importlib.util.spec_from_file_location("_check_dois_under_test", HOOK)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.CACHE = cache
    return mod


def run_main(mod, file: Path) -> dict | None:
    sys.stdin = io.StringIO(json.dumps({"tool_input": {"file_path": str(file)}}))
    out = io.StringIO()
    try:
        with redirect_stdout(out):
            mod.main()
    finally:
        sys.stdin = sys.__stdin__
    return json.loads(out.getvalue()) if out.getvalue().strip() else None


print("registration")
matcher, command = registered_command()
check("hook is registered on PostToolUse", bool(command), "no check-dois command in settings.json")
check("matcher covers Write and Edit", {"Write", "Edit"} <= set(matcher.split("|")), matcher)
script = Path(command.replace('"$CLAUDE_PROJECT_DIR"', str(ROOT)).replace("$CLAUDE_PROJECT_DIR", str(ROOT)))
check("registered path is the hook script", script.resolve() == HOOK.resolve(), str(script))
check("hook script is executable", os.access(HOOK, os.X_OK), str(HOOK))

print("the registered command executes and reads every DOI form")
root = project_with_hook()
note = root / "note.md"
note.write_text("Smith 2020 doi:10.9999/offline.one\nJones https://doi.org/10.9999/offline.two\n"
                "Brown 2021, 10.9999/offline.three\n")
proc = run_registered(command, root, note)
check("command exits cleanly", proc.returncode == 0, proc.stderr)
try:
    ctx = json.loads(proc.stdout)["hookSpecificOutput"]["additionalContext"]
except (ValueError, KeyError) as e:
    ctx = f"<no report: {e}; stdout={proc.stdout!r}>"
check("unreachable DOIs are reported, not passed", "unverified, not clean" in ctx, ctx)
check("doi: form is read", "10.9999/offline.one" in ctx, ctx)
check("doi.org form is read", "10.9999/offline.two" in ctx, ctx)
check("bare form is read", "10.9999/offline.three" in ctx, ctx)

proc = run_registered(command, root, root / "code.py")
check("non-markdown edits are ignored", proc.returncode == 0 and not proc.stdout.strip(), proc.stdout)

print("verdicts")
cache = root / "cache"
hook = load_hook(cache)
hook.lookup = lambda doi: 404
note.write_text("Nobody 2020 doi:10.9999/missing\n")
out = run_main(hook, note)
check("an unregistered DOI blocks", bool(out) and out.get("decision") == "block"
      and "does not resolve" in out.get("reason", ""), str(out))

csl = {"author": [{"family": "Hestenes"}], "title": "Force concept inventory", "issued": {"date-parts": [[1992]]}}
hook.lookup = lambda doi: csl
note.write_text("Chi, Feltovich and Glaser 1981 doi:10.9999/wrong-work\n")
out = run_main(hook, note)
check("a DOI resolving to another work blocks", bool(out) and out.get("decision") == "block"
      and "does not name" in out.get("reason", ""), str(out))

note.write_text("Hestenes, Wells and Swackhamer 1992 doi:10.9999/right-work\n")
out = run_main(hook, note)
check("a DOI naming its work passes", out is None, str(out))
check("a verified DOI is cached", "10.9999/right-work" in cache.read_text(), cache.read_text())

shutil.rmtree(root)
print(f"\n{passed} passed, {len(failures)} failed")
if failures:
    for f in failures:
        print(f"  - {f}")
sys.exit(1 if failures else 0)
