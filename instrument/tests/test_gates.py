import argparse
import dataclasses
import re
import subprocess
from pathlib import Path

import pytest

from probe_app import cli as app_cli
from probe_app import config
from probe_code import cli as code_cli

TESTS = Path(__file__).parent

# Subcommands no test runs through main(). Shrink only: a new subcommand must arrive with a smoke test.
UNRUN = frozenset()


def _subcommands(main, monkeypatch) -> set[str]:
    seen = {}

    def capture(self, *a, **k):
        seen["parser"] = self
        raise SystemExit(0)

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", capture)
    with pytest.raises(SystemExit):
        main([])
    sub = next(a for a in seen["parser"]._actions if isinstance(a, argparse._SubParsersAction))
    return set(sub.choices)


def test_every_cli_subcommand_is_run_by_a_test(monkeypatch):
    sources = "\n".join(p.read_text() for p in TESTS.glob("test_*.py") if p.name != Path(__file__).name)
    run = set(re.findall(r'main\(\[\s*"([a-z0-9-]+)"', sources))
    unrun = {("probe-app", c) for c in _subcommands(app_cli.main, monkeypatch) - run}
    unrun |= {("probe-code", c) for c in _subcommands(code_cli.main, monkeypatch) - run}
    assert unrun == UNRUN, "update UNRUN: remove commands that gained a test; add a smoke test for new ones"


def test_frozen_config_covers_every_role_setting():
    frozen = {f.name for f in dataclasses.fields(config.FrozenConfig)}
    required = {f"{role}_{field}" for role in ("interviewer", "guard") for field in config.RoleModel.model_fields}
    required |= {f"transcriber_{field}" for field in config.TranscriberModel.model_fields}
    assert required <= frozen, f"not frozen: {sorted(required - frozen)}"


def test_no_generated_artefact_is_tracked():
    tracked = subprocess.run(["git", "ls-files", ":/"], cwd=TESTS, capture_output=True, text=True, check=True).stdout
    generated = [p for p in tracked.splitlines() if re.search(r"__pycache__/|\.pyc$|\.venv/|\.pytest_cache/", p)]
    assert not generated, f"tracked generated files would trip git_dirty(): {generated[:5]}"


# probe_app modules outside the freeze, each for a stated reason: serving and storage move no arm data between
# the expert and the model; cli/simulate/backup are operator tools.
FREEZE_EXEMPT = frozenset({"__init__.py", "server.py", "storage.py", "cli.py", "simulate.py", "backup.py"})


def test_every_probe_app_module_is_frozen_or_exempt():
    modules = {p.name for p in (Path(config.__file__).parent).glob("*.py")}
    frozen = {Path(f).name for f in config.MODEL_FACING_FILES if f.startswith("src/probe_app/")}
    assert modules - frozen == FREEZE_EXEMPT, "classify each new probe_app module: frozen (arm data) or exempt"
