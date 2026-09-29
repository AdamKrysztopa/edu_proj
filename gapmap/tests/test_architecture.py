import ast
import re
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = sorted((ROOT / "src" / "gapmap").rglob("*.py"))
ALLOWED = set(sys.stdlib_module_names) | {"pydantic", "residual", "gapmap"}
FORBIDDEN = {"instrument", "probe_app", "probe_code", "anthropic", "openai", "httpx", "requests",
            "langgraph", "langchain", "networkx", "fastapi", "neo4j", "rdflib", "chromadb",
            "qdrant_client", "pinecone", "weaviate", "faiss", "lancedb", "pgvector"}


def imports(path):
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            yield from (alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.module.split(".")[0]


def test_runtime_dependencies_are_exactly_pydantic_and_residual():
    deps = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["dependencies"]
    names = sorted(re.split(r"[\s<>=!~;\[]", d, maxsplit=1)[0].lower() for d in deps)
    assert names == ["pydantic", "residual"]


def test_there_are_modules_to_check():
    assert {p.name for p in MODULES} >= {"text.py", "link.py", "lenses.py", "record.py", "rank.py",
                                         "checks.py", "config.py", "render.py", "__main__.py"}


@pytest.mark.parametrize("path", MODULES, ids=lambda p: p.name)
def test_modules_import_only_stdlib_pydantic_residual_and_gapmap(path):
    found = set(imports(path))
    assert found <= ALLOWED, found - ALLOWED
    assert not found & FORBIDDEN
