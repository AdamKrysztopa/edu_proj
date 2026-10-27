"""Build a codebase's local corpus from its config's `corpus_build` section (D1c plan §3.1): the
owner's user-facing docs at the pinned commit of a local checkout, plus outside pages on the same
methods, so that a gap can reach k_topic >= 2. D1's converter and fetchers are reused unchanged
(`research/d1_demonstrator/build_corpus.py`); only the lists and the repository are parameters.
Outside pages are fetched from the network ($0, no model call); tests inject fake fetchers.

    uv run --directory gapmap python ../research/d1b_rerun/corpus_build.py --codebase CFG
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import codebase

D1_BUILDER = Path(__file__).resolve().parent.parent / "d1_demonstrator" / "build_corpus.py"


def _d1():
    spec = importlib.util.spec_from_file_location("d1_build_corpus", D1_BUILDER)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _title(text_: str, fallback: str) -> str:
    return next((ln.lstrip("#").strip() for ln in text_.splitlines() if ln.startswith("#")), fallback)


def build(config: Path, fetchers: dict | None = None) -> dict:
    cb = codebase.load(config)
    spec = json.loads(Path(config).read_text())["corpus_build"]
    d1 = _d1()
    fetchers = fetchers or {"wikipedia": d1.wikipedia_markdown, "sphinx": d1.sphinx_markdown}
    checkout = cb.root / spec["checkout"]
    head = subprocess.run(["git", "-C", str(checkout), "rev-parse", "HEAD"],
                          capture_output=True, text=True, check=True).stdout.strip()
    if head != spec["commit"]:
        raise SystemExit(f"checkout is at {head}, not the pinned commit {spec['commit']}")
    missing = [rel for rel in spec["docs"] if not (checkout / rel).is_file()]
    if missing:
        raise SystemExit(f"docs missing at the pinned commit: {missing}")
    pages: list[tuple[dict, dict, bytes]] = []
    for rel in spec["docs"]:
        text_ = (checkout / rel).read_text(encoding="utf-8")
        title = _title(text_, rel)
        page = d1.md_to_html(text_, title).encode("utf-8")
        pages.append(({"url": f"{spec['repo_url']}/blob/{head}/{rel}", "title": title},
                      {"path": rel, "source_bytes": len(text_.encode("utf-8"))}, page))
    outside = [(f"https://en.wikipedia.org/wiki/{t}", *fetchers["wikipedia"](t)) for t in spec["outside_wikipedia"]]
    outside += [(u, *fetchers["sphinx"](u)) for u in spec["outside_sphinx"]]
    for url, text_, raw in outside:
        title = _title(text_, url)
        page = d1.md_to_html(text_, title).encode("utf-8")
        pages.append(({"url": url, "title": title},
                      {"url": url, "outside": True, "raw_sha256": hashlib.sha256(raw).hexdigest(),
                       "source_bytes": len(text_.encode("utf-8"))}, page))
    files_dir = cb.corpus / "files"
    files_dir.mkdir(parents=True, exist_ok=True)
    documents, inventory = [], []
    for doc, inv, page in pages:
        digest = hashlib.sha256(page).hexdigest()
        (files_dir / f"{digest}.html").write_bytes(page)
        documents.append({"url": doc["url"], "content_type": "text/html; charset=utf-8",
                          "file": f"files/{digest}.html", "title": doc["title"]})
        inventory.append({**inv, "html_sha256": digest})
    manifest = {"commit": head, "repo": spec["repo_url"], "documents": documents}
    (cb.corpus / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    (cb.corpus / "inventory.json").write_text(json.dumps(
        {"commit": head, "documents": inventory, "total_source_bytes": sum(d["source_bytes"] for d in inventory)},
        indent=1) + "\n")
    return manifest


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="corpus_build")
    p.add_argument("--codebase", required=True)
    args = p.parse_args(argv)
    manifest = build(Path(args.codebase))
    print(json.dumps({"commit": manifest["commit"], "documents": len(manifest["documents"])}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
