import ast
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = sorted((ROOT / "src" / "reconstruct").rglob("*.py"))
FORBIDDEN = {"instrument", "probe_app", "probe_code"}
ALLOWED = (set(sys.stdlib_module_names) |
           {"pydantic", "httpx", "openai", "tldextract", "residual", "reconstruct"})


def imports(path: Path):
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            yield from (alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            yield node.module.split(".")[0]


def test_there_are_modules_to_check():
    assert {p.name for p in MODULES} >= {"llm.py", "web.py"}


@pytest.mark.parametrize("path", MODULES, ids=lambda p: p.name)
def test_modules_never_import_instrument(path):
    found = set(imports(path))
    assert not found & FORBIDDEN, f"{path}: forbidden import {found & FORBIDDEN}"


@pytest.mark.parametrize("path", MODULES, ids=lambda p: p.name)
def test_modules_import_only_declared_dependencies(path):
    found = set(imports(path))
    assert found <= ALLOWED, f"{path}: undeclared import {found - ALLOWED}"
