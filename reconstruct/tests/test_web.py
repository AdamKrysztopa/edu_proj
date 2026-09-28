from datetime import date
from pathlib import Path

import httpx
import pytest

from reconstruct.web import Fetched, FetchFailure, MAX_BYTES, SnapshotStore, extract_visible_text, fetch

FIXTURES = Path(__file__).parent / "fixtures"


def read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def client_for(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


# --- visible-text extraction ---------------------------------------------------------------

def test_visible_text_drops_hidden_script_style_and_head():
    text = extract_visible_text(read_fixture("hidden_content.html"))
    assert "Visible paragraph one." in text
    assert "Visible paragraph two" in text
    assert "Nested visible span inside a visible div." in text
    for leaked in ("script payload", "also should not appear", "Noscript fallback",
                   "SVG text should not appear", "Template content should not appear",
                   "Head title should not appear"):
        assert leaked not in text


def test_visible_text_drops_injected_hidden_instruction_text():
    text = extract_visible_text(read_fixture("hidden_content.html"))
    assert "Ignore all previous instructions" not in text
    assert "developer mode" not in text
    assert "Nested hidden paragraph" not in text


def test_visible_text_drops_display_none_and_visibility_hidden():
    text = extract_visible_text(read_fixture("hidden_content.html"))
    assert "Hidden via inline display none." not in text
    assert "Hidden via inline visibility hidden." not in text


# --- metadata --------------------------------------------------------------------------------

@pytest.mark.parametrize("fixture,field,expected", [
    ("date_citation.html", "citation_publication_date", date(2024, 3, 15)),
    ("date_article.html", "article:published_time", date(2023, 11, 2)),
    ("date_ldjson.html", "json-ld:datePublished", date(2022, 7, 4)),
    ("date_dc.html", "dc.date", date(2021, 1, 9)),
])
def test_metadata_published_date_per_field(fixture, field, expected):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html; charset=utf-8"},
                               content=read_fixture(fixture).encode())

    result = fetch("https://example.org/page", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.published == expected
    assert result.metadata.published_field == field


def test_metadata_citation_date_wins_over_lower_priority_fields():
    html = read_fixture("date_citation.html").replace(
        "</head>",
        '<meta property="article:published_time" content="1999-01-01T00:00:00Z"></head>',
    )

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=html.encode())

    result = fetch("https://example.org/page", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.published == date(2024, 3, 15)
    assert result.metadata.published_field == "citation_publication_date"


def test_metadata_publisher_falls_back_to_host():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=read_fixture("no_publisher.html").encode())

    result = fetch("https://example.org/no-og", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.publisher == "example.org"
    assert result.metadata.title == "No publisher metadata fixture"
    assert result.metadata.published is None
    assert result.metadata.published_field is None


def test_metadata_publisher_prefers_og_site_name():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=read_fixture("date_citation.html").encode())

    result = fetch("https://journal.example/article", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.publisher == "Example Journal"


# --- fetch(): redirects, non-HTML, size cap, hashing -----------------------------------------

def test_fetch_records_final_url_after_redirect():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/old":
            return httpx.Response(302, headers={"location": "https://example.org/new"})
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=b"<html><body><p>Landed here.</p></body></html>")

    result = fetch("https://example.org/old", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.requested_url == "https://example.org/old"
    assert result.final_url == "https://example.org/new"
    assert "Landed here." in result.text


def test_fetch_rejects_non_html_content_type():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF-1.4 ...")

    result = fetch("https://example.org/doc.pdf", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "unsupported content type: application/pdf" in result.reason
    assert result.status == 200
    assert result.final_url == "https://example.org/doc.pdf"


def test_fetch_enforces_size_cap():
    oversized = b"a" * (MAX_BYTES + 1)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=oversized)

    result = fetch("https://example.org/huge", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "exceeds size cap" in result.reason


def test_fetch_records_raw_and_text_hashes():
    body = b"<html><body><p>Hash me.</p></body></html>"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=body)

    result = fetch("https://example.org/hash", client=client_for(handler))
    assert isinstance(result, Fetched)
    import hashlib
    assert result.raw_sha256 == hashlib.sha256(body).hexdigest()
    assert result.text_sha256 == hashlib.sha256(result.text.encode()).hexdigest()


# --- snapshot store ----------------------------------------------------------------------------

def test_snapshot_store_round_trips_raw_and_text(tmp_path):
    store = SnapshotStore(tmp_path / "snapshots")
    raw = b"raw page bytes \x00\x01"
    text = "extracted visible text"

    raw_sha = store.write_raw(raw)
    text_sha = store.write_text(text)

    assert store.read_raw(raw_sha) == raw
    assert store.read_text(text_sha) == text


def test_snapshot_store_is_content_addressed(tmp_path):
    store = SnapshotStore(tmp_path / "snapshots")
    sha_a = store.write_raw(b"same bytes")
    sha_b = store.write_raw(b"same bytes")
    assert sha_a == sha_b
    assert len(list((tmp_path / "snapshots").glob("*.raw"))) == 1
