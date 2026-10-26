#!/usr/bin/env python3
"""Prove drain 7's hooks are registered, fire on the input they exist for, and stay quiet otherwise.

Each hook is run through the command string in .claude/settings.json, as Claude Code runs it,
with a JSON payload on stdin. No network: guard-key-headroom.sh reads a fake key response.

    python3 scripts/hook_tests/test_drain7_hooks.py

No dependencies beyond jq. Exits non-zero on any failure.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SETTINGS = json.loads((ROOT / ".claude/settings.json").read_text())
PASSED_RUN = "reconstruct/runs/20260928T133336Z-59ec876b3d7e"

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


def registered(event: str, script: str) -> tuple[str, str]:
    for group in SETTINGS["hooks"].get(event, []):
        for hook in group["hooks"]:
            if hook["command"].endswith(f"/.claude/hooks/{script}"):
                return group.get("matcher", ""), hook["command"]
    raise AssertionError(f"{script} is not registered under {event}")


def fire(event: str, script: str, payload: dict, env: dict | None = None) -> dict:
    _, command = registered(event, script)
    full_env = {**os.environ, "CLAUDE_PROJECT_DIR": str(ROOT), **(env or {})}
    out = subprocess.run(["bash", "-c", command], input=json.dumps(payload), capture_output=True,
                         text=True, env=full_env, cwd=ROOT)
    return json.loads(out.stdout) if out.stdout.strip() else {}


def decision(result: dict) -> str | None:
    return result.get("hookSpecificOutput", {}).get("permissionDecision") or result.get("decision")


def context(result: dict) -> str:
    return result.get("hookSpecificOutput", {}).get("additionalContext", "")


def bash(cmd: str) -> dict:
    return {"tool_name": "Bash", "tool_input": {"command": cmd}}


def edit(path: str, new: str) -> dict:
    return {"tool_name": "Edit", "tool_input": {"file_path": str(ROOT / path), "new_string": new}}


def key_headroom() -> None:
    print("guard-key-headroom.sh")
    check("matcher covers Bash", "Bash" in registered("PreToolUse", "guard-key-headroom.sh")[0])
    with tempfile.TemporaryDirectory() as d:
        spent, plenty = Path(d) / "spent.json", Path(d) / "plenty.json"
        spent.write_text(json.dumps({"limit": 5, "limit_remaining": 0, "usage_weekly": 5.02}))
        plenty.write_text(json.dumps({"limit": 15, "limit_remaining": 9.5, "usage_weekly": 5.5}))
        live = "uv run --directory reconstruct python -m reconstruct.run --live --max-usd 2"
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live), {"KEY_HEADROOM_JSON": str(spent)})
        check("a spent key refuses a --live run", decision(r) == "deny", r)
        r = fire("PreToolUse", "guard-key-headroom.sh", bash("python3 research/spikes/jev/spike.py smoke"),
                 {"KEY_HEADROOM_JSON": str(spent)})
        check("a spent key refuses a spike smoke run with no cap", decision(r) == "deny", r)
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live.replace("2", "12")),
                 {"KEY_HEADROOM_JSON": str(plenty)})
        check("headroom below the run's --max-usd refuses", decision(r) == "deny", r)
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live), {"KEY_HEADROOM_JSON": str(plenty)})
        check("headroom covering the cap allows", r == {}, r)
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live),
                 {"KEY_HEADROOM_JSON": str(Path(d) / "absent.json")})
        check("unreadable headroom asks, never passes silently", decision(r) == "ask", r)
        r = fire("PreToolUse", "guard-key-headroom.sh", bash("python3 research/spikes/jev/spike.py estimate"),
                 {"KEY_HEADROOM_JSON": str(spent)})
        check("a non-paying command is left alone", r == {}, r)
        empty_account = Path(d) / "empty_account.json"
        empty_account.write_text(json.dumps({"limit": 15, "limit_remaining": 14.99, "usage_weekly": 0.01,
                                             "account": {"total_credits": 80, "total_usage": 80.0}}))
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live), {"KEY_HEADROOM_JSON": str(empty_account)})
        check("an empty account refuses although the key has headroom", decision(r) == "deny", r)
        low_account = Path(d) / "low_account.json"
        low_account.write_text(json.dumps({"limit": 15, "limit_remaining": 14.99, "usage_weekly": 0.01,
                                           "account": {"total_credits": 100, "total_usage": 99.0}}))
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live), {"KEY_HEADROOM_JSON": str(low_account)})
        check("an account balance below the run's --max-usd refuses", decision(r) == "deny", r)
        rich = Path(d) / "rich.json"
        rich.write_text(json.dumps({"limit": 15, "limit_remaining": 9.5, "usage_weekly": 5.5,
                                    "account": {"total_credits": 100, "total_usage": 80.0}}))
        r = fire("PreToolUse", "guard-key-headroom.sh", bash(live), {"KEY_HEADROOM_JSON": str(rich)})
        check("key and account both covering the cap allows", r == {}, r)


def freeze_tag() -> None:
    print("guard-freeze-tag.sh")
    r = fire("PreToolUse", "guard-freeze-tag.sh", bash("git tag -a n2-freeze-4 -m 'freeze prompts'"))
    check("a freeze tag naming no live run is refused", decision(r) == "deny", r)
    r = fire("PreToolUse", "guard-freeze-tag.sh",
             bash("git tag -a n2-freeze-4 -m 'live run reconstruct/runs/no-such-run passed'"))
    check("a freeze tag naming a missing run is refused", decision(r) == "deny", r)
    r = fire("PreToolUse", "guard-freeze-tag.sh",
             bash(f"git tag -a n2-freeze-4 -m 'live run {PASSED_RUN} passed'"))
    check("a freeze tag naming a completed live run is allowed", r == {}, r)
    r = fire("PreToolUse", "guard-freeze-tag.sh", bash("git tag -d n2-freeze-4"))
    check("deleting a freeze tag is left alone", r == {}, r)
    r = fire("PreToolUse", "guard-freeze-tag.sh", bash("git tag -a report-v1.2 -m 'release'"))
    check("a non-freeze tag is left alone", r == {}, r)


def hook_tests() -> None:
    # A throwaway project: in this repo the hook would rerun this very file and recurse.
    print("run-hook-tests.sh")
    registered("PostToolUse", "run-hook-tests.sh")
    script = ROOT / ".claude/hooks/run-hook-tests.sh"
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        (root / "scripts/hook_tests").mkdir(parents=True)
        (root / "scripts/hook_tests/test_good.py").write_text("# good.sh\n")
        (root / "scripts/hook_tests/test_bad.py").write_text("# bad.sh\nraise SystemExit('bad.sh broke')\n")

        def run(path: str) -> dict:
            payload = {"tool_name": "Edit", "tool_input": {"file_path": str(root / path)}}
            out = subprocess.run(["bash", str(script)], input=json.dumps(payload), capture_output=True,
                                 text=True, env={**os.environ, "CLAUDE_PROJECT_DIR": str(root)})
            return json.loads(out.stdout) if out.stdout.strip() else {}

        r = run(".claude/hooks/good.sh")
        check("an edited hook whose tests pass is quiet", r == {}, r)
        r = run(".claude/hooks/bad.sh")
        check("an edited hook whose test fails blocks with the output",
              decision(r) == "block" and "bad.sh broke" in r.get("reason", ""), r)
        r = run(".claude/hooks/untested.sh")
        check("an edited hook no test names is reported as unverified", "unverified" in context(r), r)
        r = run("docs/lessons.md")
        check("a non-hook edit is left alone", r == {}, r)


def prereg() -> None:
    print("prereg-checklist.sh")
    gate = "| N3 | continue if the gap map's hit rate ≥ 0.30 over the donor null |"
    r = fire("PostToolUse", "prereg-checklist.sh", edit("REORIENTATION.md", gate))
    check("a gate written into the plan injects the discrimination checks",
          "trivial stand-in" in context(r) and "planted positive" in context(r), r)
    r = fire("PostToolUse", "prereg-checklist.sh", edit("research/spikes/jev/spike.py",
                                                          "PROMISING if gap >= 0.20"))
    check("a decision rule in spike code injects them too", "trivial stand-in" in context(r), r)
    r = fire("PostToolUse", "prereg-checklist.sh", edit("REORIENTATION.md", "Reworded §1 for clarity."))
    check("prose with no rule is left alone", r == {}, r)
    r = fire("PostToolUse", "prereg-checklist.sh", edit("gapmap/src/gapmap/config.py", "THRESHOLD >= 0.5"))
    check("code outside plans and spikes is left alone", r == {}, r)


def render_claims() -> None:
    print("agent-render-claims.sh")
    matcher = registered("PostToolUse", "agent-render-claims.sh")[0]
    check("matcher covers the Agent tool", "Agent" in matcher, matcher)
    claim = {"tool_name": "Agent", "tool_response": {"content": [
        {"type": "text", "text": "fig03.png rendered, visually inspected, clean."}]}}
    r = fire("PostToolUse", "agent-render-claims.sh", claim)
    check("an agent's 'inspected, clean' render report injects the look-yourself rule",
          "Read every render" in context(r), r)
    plain = {"tool_name": "Agent", "tool_response": {"content": [
        {"type": "text", "text": "Found 3 call sites in gapmap/src."}]}}
    check("an unrelated agent report is left alone",
          fire("PostToolUse", "agent-render-claims.sh", plain) == {})


def manifest() -> None:
    print("check-results-manifest.sh")
    r = fire("PostToolUse", "check-results-manifest.sh", edit("research/n3/README.md", "no links here"))
    check("a research edit with the manifest current is quiet", r == {}, r)
    moving = "see https://github.com/AdamKrysztopa/edu_proj/blob/main/research/n3/README.md"
    r = fire("PostToolUse", "check-results-manifest.sh", edit("report/notes/04_results.md", moving))
    check("a report link to the moving main branch blocks", decision(r) == "block", r)
    pinned = moving.replace("/blob/main/", "/blob/be82433/")
    r = fire("PostToolUse", "check-results-manifest.sh", edit("report/notes/04_results.md", pinned))
    check("a link pinned to a commit is quiet", r == {}, r)


def main() -> int:
    for section in (key_headroom, freeze_tag, hook_tests, prereg, render_claims, manifest):
        try:
            section()
        except AssertionError as e:
            check(section.__name__, False, str(e))
    print(f"\n{passed} passed, {len(failures)} failed")
    for f in failures:
        print(f"  - {f}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
