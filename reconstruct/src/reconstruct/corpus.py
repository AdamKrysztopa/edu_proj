"""Corpus mode (protocol `docs/n2-eplant-eabst-protocol.md`, "Corpus mode"): E-PLANT reads a
frozen manifest of local documents instead of the live web, but every document still goes
through the ordinary fetch -> snapshot -> independence path — nothing here constructs
Evidence/Selector/Verification (that stays evidence.py's job alone) and nothing here is aware
of which page is planted (protocol: "in a fixed-seed shuffled order with no planted flag").

Two seams, both requested by the pipeline contract:
  - `corpus_client`: an httpx.Client backed by a MockTransport that serves each manifest
    document's frozen bytes at its own URL, with its own content type. Any other URL 404s.
    `reconstruct.web.fetch` cannot tell this client apart from a live one.
  - `CorpusSearchBackend`: wraps the planner's Backend so `search()` never touches the
    network. It returns every corpus document (in the manifest's own order — the manifest is
    the thing that was shuffled once, under a fixed seed, when it was built) regardless of the
    query actually asked. `complete_json` (plan/extract/verify/contradict) is untouched: only
    search is a corpus operation, and it is enough to make the planner-facing search a no-op
    surface over local documents that AreaConditioned queries still "run" against.

Manifest shape (`manifest.json`, built by the corpus-authoring side): a JSON object with a
top-level "documents" list, each `{"url": str, "content_type": str, "file": str, "title"?: str}`.
`file` is a path relative to `root` (the frozen bytes live content-addressed, named by their own
sha256, matching `reconstruct.web.SnapshotStore`'s own `{sha256}.raw` naming, but this module
does not require that convention — it only reads whatever `file` names). `title` is optional;
falling back to the URL keeps `search()` total over every manifest shape the corpus side might
ship.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Sequence

import httpx

from reconstruct.llm import Backend, Hit, SearchResult


@dataclass(frozen=True)
class ManifestDocument:
    url: str
    content_type: str
    file: str
    title: str | None = None


def load_manifest(manifest_path: str | Path) -> tuple[ManifestDocument, ...]:
    raw = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    docs = raw["documents"] if isinstance(raw, dict) else raw
    if not docs:
        raise ValueError(f"{manifest_path}: manifest has no documents")
    return tuple(
        ManifestDocument(url=d["url"], content_type=d["content_type"], file=d["file"],
                          title=d.get("title"))
        for d in docs
    )


def corpus_client(manifest_path: str | Path, root: str | Path) -> httpx.Client:
    """An httpx.Client whose MockTransport serves each manifest document's frozen bytes at its
    URL, with its content type; any other URL gets a 404. `reconstruct.web.fetch` reads this
    exactly as it would a live response — same size cap, same encoding, same HTML-only
    acceptance — so corpus mode differs from a live run only in where the bytes come from."""
    documents = load_manifest(manifest_path)
    root = Path(root)
    bodies: dict[str, tuple[bytes, str]] = {
        doc.url: ((root / doc.file).read_bytes(), doc.content_type) for doc in documents
    }

    def handler(request: httpx.Request) -> httpx.Response:
        served = bodies.get(str(request.url))
        if served is None:
            return httpx.Response(404, headers={"content-type": "text/plain"}, content=b"not found")
        content, content_type = served
        return httpx.Response(200, headers={"content-type": content_type}, content=content)

    return httpx.Client(transport=httpx.MockTransport(handler))


@dataclass
class CorpusSearchBackend:
    """Wraps the planner's Backend (contract: `CorpusSearchBackend(inner: Backend, manifest)`).

    `search()` never calls the network: it returns every corpus document's URL (title from the
    manifest, falling back to the URL) for any query, in the manifest's own order, and records
    the query it was actually asked as `executed_query` — run.py builds its `Search` record from
    that field. `complete_json` delegates unchanged: corpus mode replaces only what discovers
    documents, not the model calls that plan, extract, verify or classify contradictions.

    `manifest` is either a path to `manifest.json` (loaded once, here) or an already-loaded
    tuple of `ManifestDocument`, so a caller who has already parsed the manifest for its own
    purposes (e.g. to build a gold ledger) does not pay to parse it twice.
    """

    inner: Backend
    manifest: str | Path | Sequence[ManifestDocument]
    documents: tuple[ManifestDocument, ...] = field(init=False)

    def __post_init__(self) -> None:
        self.documents = (tuple(self.manifest) if isinstance(self.manifest, (list, tuple))
                          else load_manifest(self.manifest))

    def complete_json(self, task: str, system: str, user: str, schema: dict) -> dict:
        return self.inner.complete_json(task, system, user, schema)

    def search(self, query: str, *, max_results: int) -> SearchResult:
        hits = tuple(Hit(url=doc.url, title=doc.title or doc.url) for doc in self.documents)
        return SearchResult(executed_query=query, on=self._today(), hits=hits)

    @staticmethod
    def _today() -> date:
        return datetime.now(UTC).date()
