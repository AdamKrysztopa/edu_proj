"""The per-codebase corpus builder (D1c plan §3.1): owner docs at a pinned commit plus outside pages,
wrapped as HTML in reconstruct.corpus manifest shape with D1's own converter. A local git repo and
fake outside fetchers; no network."""
import importlib.util
import json
import subprocess
from pathlib import Path

import pytest

import codebase
import corpus_build

D1 = Path(__file__).resolve().parents[2] / "d1_demonstrator"


def _git(repo, *args):
    return subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True).stdout.strip()


@pytest.fixture
def project(tmp_path):
    src = tmp_path / "source"
    (src / "docs").mkdir(parents=True)
    (src / "README.md").write_text("# Tool\n\nThe tool triages series. It runs before model fitting.\n")
    (src / "docs" / "why.md").write_text("# Why\n\nBecause fitting first wastes effort.\n\n```\ncode\n```\n")
    _git(src, "init", "-q")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "add", ".")
    _git(src, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-qm", "x")
    commit = _git(src, "rev-parse", "HEAD")
    cfg = {"name": "tool", "title": "D1c", "owner_repo": "github.com/o/tool", "domain": "tool", "seed": 1,
           "corpus": "corpus", "ledgers": {"cheap": "runs/cheap"}, "prior_items": None,
           "canaries": "fixtures/canaries.json", "canary_mode": "generated",
           "corpus_build": {"repo_url": "https://github.com/o/tool", "checkout": "source", "commit": commit,
                            "docs": ["README.md", "docs/why.md"], "outside_wikipedia": ["Forecasting"],
                            "outside_sphinx": ["https://example.org/ref.html"]}}
    (tmp_path / "codebase.json").write_text(json.dumps(cfg))
    return tmp_path, commit


def _fakes():
    return {"wikipedia": lambda t: (f"# {t}\n\nAn outside page on {t}.", b"raw-" + t.encode()),
            "sphinx": lambda u: ("# Ref\n\nA reference page.", b"raw-ref")}


def test_owner_docs_are_pinned_wrapped_and_content_addressed(project):
    root, commit = project
    manifest = corpus_build.build(root / "codebase.json", fetchers=_fakes())
    docs = manifest["documents"]
    assert [d["url"] for d in docs[:2]] == [f"https://github.com/o/tool/blob/{commit}/README.md",
                                           f"https://github.com/o/tool/blob/{commit}/docs/why.md"]
    assert [d["title"] for d in docs] == ["Tool", "Why", "Forecasting", "Ref"]
    for d in docs:
        page = (root / "corpus" / d["file"]).read_bytes()
        assert d["file"] == f"files/{corpus_build.hashlib.sha256(page).hexdigest()}.html"
    assert json.loads((root / "corpus" / "manifest.json").read_text()) == manifest
    inventory = json.loads((root / "corpus" / "inventory.json").read_text())
    assert [d.get("outside", False) for d in inventory["documents"]] == [False, False, True, True]


def test_the_html_is_d1s_converter_output(project):
    root, _ = project
    corpus_build.build(root / "codebase.json", fetchers=_fakes())
    spec = importlib.util.spec_from_file_location("d1_build_corpus", D1 / "build_corpus.py")
    d1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(d1)
    want = d1.md_to_html((root / "source" / "README.md").read_text(), "Tool")
    manifest = json.loads((root / "corpus" / "manifest.json").read_text())
    assert (root / "corpus" / manifest["documents"][0]["file"]).read_text() == want


def test_owner_docs_are_recognised_as_owner_and_outside_pages_are_not(project):
    root, _ = project
    corpus_build.build(root / "codebase.json", fetchers=_fakes())
    cb = codebase.load(root / "codebase.json")
    manifest = json.loads((root / "corpus" / "manifest.json").read_text())
    assert [cb.owner_repo in d["url"] for d in manifest["documents"]] == [True, True, False, False]


def test_a_checkout_at_another_commit_is_refused(project):
    root, _ = project
    cfg = json.loads((root / "codebase.json").read_text())
    cfg["corpus_build"]["commit"] = "0" * 40
    (root / "codebase.json").write_text(json.dumps(cfg))
    with pytest.raises(SystemExit, match="pinned"):
        corpus_build.build(root / "codebase.json", fetchers=_fakes())


def test_a_missing_doc_is_refused_before_anything_is_written(project):
    root, _ = project
    cfg = json.loads((root / "codebase.json").read_text())
    cfg["corpus_build"]["docs"].append("docs/absent.md")
    (root / "codebase.json").write_text(json.dumps(cfg))
    with pytest.raises(SystemExit, match="absent.md"):
        corpus_build.build(root / "codebase.json", fetchers=_fakes())
    assert not (root / "corpus").exists()
