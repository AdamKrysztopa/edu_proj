import ast
import re
import sys
import tomllib
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MODULES = sorted((ROOT / "src" / "residual").rglob("*.py"))
ALLOWED = set(sys.stdlib_module_names) | {"pydantic", "residual"}
FORBIDDEN = {"instrument", "probe_app", "probe_code", "anthropic", "openai", "httpx", "requests",
             "langgraph", "langchain", "networkx", "fastapi", "neo4j", "rdflib", "chromadb",
             "qdrant_client", "pinecone", "weaviate", "faiss", "lancedb", "pgvector"}


def imports(path):
    for node in ast.walk(ast.parse(path.read_text(), filename=str(path))):
        if isinstance(node, ast.Import):
            yield from (alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            yield node.module.split(".")[0]


def test_runtime_dependencies_are_exactly_pydantic():
    deps = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["dependencies"]
    assert [re.split(r"[\s<>=!~;\[]", d, maxsplit=1)[0].lower() for d in deps] == ["pydantic"]


def test_there_are_modules_to_check():
    assert {p.name for p in MODULES} >= {"vocab.py", "provenance.py", "claims.py", "ledger.py",
                                         "gates.py", "residual.py", "gapmap.py", "freeze.py"}


@pytest.mark.parametrize("path", MODULES, ids=lambda p: p.name)
def test_modules_import_only_stdlib_pydantic_and_residual(path):
    found = set(imports(path))
    assert found <= ALLOWED, found - ALLOWED
    assert not found & FORBIDDEN
