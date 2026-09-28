from pathlib import Path

import pytest

from reconstruct.corpus import CorpusSearchBackend, ManifestDocument, corpus_client, load_manifest
from reconstruct.llm import Hit, SearchResult
from reconstruct.web import FetchFailure, fetch

FIXTURES = Path(__file__).parent / "fixtures" / "corpus"


class _RecordingInner:
    def __init__(self, response: dict | None = None):
        self.calls = []
        self.response = response or {"ok": True}

    def complete_json(self, task, system, user, schema):
        self.calls.append((task, system, user, schema))
        return self.response

    def search(self, query, *, max_results):  # never used through the wrapper
        raise AssertionError("CorpusSearchBackend must not delegate search() to the inner backend")


# --- load_manifest ---------------------------------------------------------------------------

def test_load_manifest_reads_documents():
    docs = load_manifest(FIXTURES / "manifest.json")
    assert docs == (
        ManifestDocument(url="https://real-a.test/leftovers", content_type="text/html",
                          file="doc-a.html", title="Document A"),
        ManifestDocument(url="https://real-b.test/concrete", content_type="text/html",
                          file="doc-b.html", title=None),
    )


def test_load_manifest_refuses_an_empty_corpus(tmp_path):
    empty = tmp_path / "manifest.json"
    empty.write_text('{"documents": []}')
    with pytest.raises(ValueError, match="no documents"):
        load_manifest(empty)


# --- corpus_client -----------------------------------------------------------------------------

def test_corpus_client_serves_each_document_at_its_url_with_its_content_type():
    client = corpus_client(FIXTURES / "manifest.json", FIXTURES)
    response = client.get("https://real-a.test/leftovers")
    assert response.status_code == 200
    assert response.headers["content-type"] == "text/html"
    assert "74 degrees C" in response.text

    response_b = client.get("https://real-b.test/concrete")
    assert response_b.status_code == 200
    assert "48 hours" in response_b.text


def test_corpus_client_404s_any_url_not_in_the_manifest():
    client = corpus_client(FIXTURES / "manifest.json", FIXTURES)
    response = client.get("https://not-in-corpus.test/x")
    assert response.status_code == 404


def test_corpus_documents_go_through_the_normal_fetch_and_snapshot_path():
    client = corpus_client(FIXTURES / "manifest.json", FIXTURES)
    result = fetch("https://real-a.test/leftovers", client=client)
    assert not isinstance(result, FetchFailure)
    assert result.status == 200
    assert "core temperature of 74 degrees C" in result.text
    assert result.metadata.title == "Document A"
    assert len(result.raw_sha256) == 64
    assert len(result.text_sha256) == 64


def test_corpus_client_rejects_non_html_content_types_like_a_live_fetch_would(tmp_path):
    manifest = tmp_path / "manifest.json"
    manifest.write_text('{"documents": [{"url": "https://real.test/data.json", '
                        '"content_type": "application/json", "file": "data.json"}]}')
    (tmp_path / "data.json").write_text('{"not": "html"}')
    client = corpus_client(manifest, tmp_path)
    result = fetch("https://real.test/data.json", client=client)
    assert isinstance(result, FetchFailure)
    assert "content type" in result.reason


# --- CorpusSearchBackend -------------------------------------------------------------------------

def test_search_returns_every_corpus_url_for_any_query_without_touching_the_network():
    inner = _RecordingInner()
    backend = CorpusSearchBackend(inner=inner, manifest=FIXTURES / "manifest.json")
    result = backend.search("anything at all, ignored", max_results=1)
    assert isinstance(result, SearchResult)
    assert result.executed_query == "anything at all, ignored"
    assert result.hits == (
        Hit(url="https://real-a.test/leftovers", title="Document A"),
        Hit(url="https://real-b.test/concrete", title="https://real-b.test/concrete"),
    )


def test_search_is_the_same_for_every_query_and_ignores_max_results():
    inner = _RecordingInner()
    backend = CorpusSearchBackend(inner=inner, manifest=FIXTURES / "manifest.json")
    a = backend.search("query one", max_results=1)
    b = backend.search("a totally different query", max_results=100)
    assert a.hits == b.hits


def test_search_accepts_an_already_loaded_manifest_tuple():
    docs = load_manifest(FIXTURES / "manifest.json")
    backend = CorpusSearchBackend(inner=_RecordingInner(), manifest=docs)
    assert backend.search("q", max_results=5).hits[0].url == docs[0].url


def test_complete_json_delegates_unchanged_to_the_inner_backend():
    inner = _RecordingInner(response={"areas": []})
    backend = CorpusSearchBackend(inner=inner, manifest=FIXTURES / "manifest.json")
    result = backend.complete_json("plan", "sys", "usr", {"type": "object"})
    assert result == {"areas": []}
    assert inner.calls == [("plan", "sys", "usr", {"type": "object"})]
