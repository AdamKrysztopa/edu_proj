import io
from datetime import date
from pathlib import Path

import httpx
import pytest
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

from reconstruct.web import (
    Fetched,
    FetchCache,
    FetchFailure,
    MAX_BYTES,
    SnapshotStore,
    extract_visible_text,
    fetch,
    fetch_all,
)

FIXTURES = Path(__file__).parent / "fixtures"

# Below the 500-char near-empty floor `fetch()` enforces (MUST 1); every test of ordinary
# fetch() success pads its body with this so it exercises what it means to test, not the floor.
PADDING = ("<p>Filler sentence to keep this test page above the near-empty-page "
           "threshold enforced by fetch().</p>\n") * 6


def read_fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


def client_for(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


def make_pdf(pages: list[str], *, title: str | None = None, creation_date: str | None = None,
             mod_date: str | None = None, user_password: str | None = None) -> bytes:
    """Builds a small, real PDF (via pypdf) with one Tj-drawn text line per page — enough for
    pypdf's own extract_text() to read back, so fetch()'s PDF path can be exercised offline."""
    writer = PdfWriter()
    for text in pages:
        page = writer.add_blank_page(width=200, height=200)
        stream = DecodedStreamObject()
        escaped = text.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")
        stream.set_data(f"BT /F1 12 Tf 10 100 Td ({escaped}) Tj ET".encode())
        page[NameObject("/Contents")] = writer._add_object(stream)
        font = DictionaryObject()
        font[NameObject("/Type")] = NameObject("/Font")
        font[NameObject("/Subtype")] = NameObject("/Type1")
        font[NameObject("/BaseFont")] = NameObject("/Helvetica")
        resources = DictionaryObject()
        fontdict = DictionaryObject()
        fontdict[NameObject("/F1")] = writer._add_object(font)
        resources[NameObject("/Font")] = fontdict
        page[NameObject("/Resources")] = resources
    metadata = {}
    if title is not None:
        metadata["/Title"] = title
    if creation_date is not None:
        metadata["/CreationDate"] = creation_date
    if mod_date is not None:
        metadata["/ModDate"] = mod_date
    if metadata:
        writer.add_metadata(metadata)
    if user_password is not None:
        writer.encrypt(user_password=user_password, owner_password="owner-secret")
    buf = io.BytesIO()
    writer.write(buf)
    return buf.getvalue()


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
                               content=f"<html><body><p>Landed here.</p>{PADDING}</body></html>".encode())

    result = fetch("https://example.org/old", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.requested_url == "https://example.org/old"
    assert result.final_url == "https://example.org/new"
    assert "Landed here." in result.text


def test_fetch_rejects_non_html_non_pdf_content_type():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/json"}, content=b'{"a": 1}')

    result = fetch("https://example.org/doc.json", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "unsupported content type: application/json" in result.reason
    assert result.status == 200
    assert result.final_url == "https://example.org/doc.json"


# --- fetch(): non-2xx status, near-empty pages, bot walls (MUST 1) ---------------------------

def test_fetch_rejects_non_2xx_status():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(403, headers={"content-type": "text/html"},
                               content=b"<html><body><p>Access Denied</p></body></html>")

    result = fetch("https://example.org/blocked", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert result.reason == "http 403"
    assert result.status == 403


def test_fetch_rejects_429_status():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(429, headers={"content-type": "text/html"}, content=b"<html></html>")

    result = fetch("https://example.org/rate-limited", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert result.reason == "http 429"


def test_fetch_rejects_near_empty_visible_text():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=b"<html><body></body></html>")

    result = fetch("https://example.org/empty", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "too little visible text" in result.reason


def test_fetch_rejects_short_bot_wall_page():
    # Padded past the near-empty floor so this isolates the marker check, not the length check
    # (a real bot-wall page this short would already be caught by the near-empty rule alone).
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=f"<html><body><p>Access Denied</p>{PADDING}</body></html>".encode())

    result = fetch("https://example.org/wall", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "bot-wall or challenge page marker matched" in result.reason


@pytest.mark.parametrize("marker", ["enable JavaScript", "Checking your browser", "Cloudflare",
                                     "Please complete the CAPTCHA", "Just a moment..."])
def test_fetch_rejects_known_bot_wall_markers(marker):
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=f"<html><body><p>{marker}</p>{PADDING}</body></html>".encode())

    result = fetch("https://example.org/wall", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "bot-wall" in result.reason


def test_fetch_does_not_flag_a_long_page_that_merely_mentions_a_marker_word():
    # "captcha" appearing once in a normal, long article must not be misflagged (the marker
    # check only fires on SHORT pages, per _BOT_WALL_MAX_CHARS).
    body = ("<p>This article discusses why captcha systems annoy users.</p>" + PADDING * 10)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=f"<html><body>{body}</body></html>".encode())

    result = fetch("https://example.org/long-article", client=client_for(handler))
    assert isinstance(result, Fetched)


def test_fetch_enforces_size_cap():
    oversized = b"a" * (MAX_BYTES + 1)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=oversized)

    result = fetch("https://example.org/huge", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "exceeds size cap" in result.reason


def test_sanitize_surrogates_replaces_lone_surrogates_only():
    from reconstruct.web import _sanitize_surrogates
    assert _sanitize_surrogates("clean text") == "clean text"
    assert _sanitize_surrogates("bad \ud800 text") == "bad � text"
    assert _sanitize_surrogates("bad \udfff text") == "bad � text"
    sanitized = _sanitize_surrogates("bad \ud800 text")
    sanitized.encode()  # must never raise UnicodeEncodeError


def test_fetch_sanitizes_lone_surrogates_from_html_text(monkeypatch):
    """defect D3 (web.py:371): a lone UTF-16 surrogate reaching hashlib.sha256(text.encode())
    crashed the whole fetch phase with UnicodeEncodeError. Sanitized at extraction time, before
    the near-empty check and before the hash, so snapshot text/hash stay consistent."""
    import hashlib

    import reconstruct.web as web

    bad_text = "Visible text with a lone surrogate \ud800 inline. " + PADDING
    monkeypatch.setattr(web, "extract_visible_text", lambda html: bad_text)

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"},
                              content=b"<html><body>irrelevant, patched above</body></html>")

    result = fetch("https://example.org/bad.html", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert "\ud800" not in result.text
    assert "�" in result.text
    assert result.text_sha256 == hashlib.sha256(result.text.encode()).hexdigest()


def test_fetch_sanitizes_lone_surrogates_from_pdf_text(monkeypatch):
    import hashlib

    import reconstruct.web as web
    from reconstruct.web import Metadata

    bad_text = "Pumps lose prime under a lone surrogate \ud800 in extracted text. " + PADDING
    monkeypatch.setattr(web, "_extract_pdf", lambda raw, *, host: (
        bad_text, Metadata(title=None, publisher=host, published=None, published_field=None)))

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"},
                              content=b"%PDF-1.4 irrelevant, patched above")

    result = fetch("https://example.org/bad.pdf", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert "\ud800" not in result.text
    assert "�" in result.text
    assert result.text_sha256 == hashlib.sha256(result.text.encode()).hexdigest()


def test_fetch_records_raw_and_text_hashes():
    body = f"<html><body><p>Hash me.</p>{PADDING}</body></html>".encode()

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=body)

    result = fetch("https://example.org/hash", client=client_for(handler))
    assert isinstance(result, Fetched)
    import hashlib
    assert result.raw_sha256 == hashlib.sha256(body).hexdigest()
    assert result.text_sha256 == hashlib.sha256(result.text.encode()).hexdigest()


# --- PDF extraction (SHOULD 2) -----------------------------------------------------------------

_PDF_PAGE_1 = ("The first page states that pumps lose prime under high suction lift conditions, "
               "a fact technicians are expected to check before any other diagnostic step is taken "
               "on site, since it accounts for most reported intermittent failures in the field, "
               "well before any electrical cause is even considered by an experienced crew.")
_PDF_PAGE_2 = ("The second page states that impellers wear faster once cavitation has begun, "
               "and that continued operation under those conditions shortens the service life of "
               "every downstream seal and bearing far more than routine wear alone would predict, "
               "which is why the manual insists on stopping the pump at the very first sign.")


def test_fetch_extracts_pdf_text_with_page_boundaries_as_paragraph_breaks():
    pdf_bytes = make_pdf([_PDF_PAGE_1, _PDF_PAGE_2])

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=pdf_bytes)

    result = fetch("https://example.org/guide.pdf", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.content_type == "application/pdf"
    assert _PDF_PAGE_1 in result.text
    assert _PDF_PAGE_2 in result.text
    first_end = result.text.index(_PDF_PAGE_1) + len(_PDF_PAGE_1)
    second_start = result.text.index(_PDF_PAGE_2)
    assert "\n\n" in result.text[first_end:second_start]


def test_fetch_pdf_metadata_title_and_published_from_creation_date():
    pdf_bytes = make_pdf([_PDF_PAGE_1, _PDF_PAGE_2], title="Troubleshooting Guide",
                          creation_date="D:20240315120000+00'00'")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=pdf_bytes)

    result = fetch("https://example.org/guide.pdf", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.title == "Troubleshooting Guide"
    assert result.metadata.published == date(2024, 3, 15)
    assert result.metadata.published_field == "pdf:CreationDate"


def test_fetch_pdf_modified_from_moddate():
    pdf_bytes = make_pdf([_PDF_PAGE_1, _PDF_PAGE_2], creation_date="D:20200101000000Z",
                          mod_date="D:20250601000000Z")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=pdf_bytes)

    result = fetch("https://example.org/guide.pdf", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.published == date(2020, 1, 1)
    assert result.metadata.modified == date(2025, 6, 1)
    assert result.metadata.modified_field == "pdf:ModDate"


def test_fetch_rejects_encrypted_pdf():
    pdf_bytes = make_pdf([_PDF_PAGE_1, _PDF_PAGE_2], user_password="secret")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=pdf_bytes)

    result = fetch("https://example.org/locked.pdf", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert result.reason == "encrypted PDF"


def test_fetch_rejects_image_only_pdf():
    pdf_bytes = make_pdf([""])  # a blank page, as an image-only scan would extract to: no Tj text

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=pdf_bytes)

    result = fetch("https://example.org/scan.pdf", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert result.reason == "image-only or empty PDF text"


def test_fetch_rejects_unreadable_pdf_bytes():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=b"%PDF-1.4 not a real pdf")

    result = fetch("https://example.org/broken.pdf", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert result.reason.startswith("unreadable PDF")
    assert result.status == 200


def test_fetch_enforces_size_cap_on_pdfs_too():
    oversized = b"%PDF-1.4" + b"a" * MAX_BYTES

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "application/pdf"}, content=oversized)

    result = fetch("https://example.org/huge.pdf", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert "exceeds size cap" in result.reason


# --- fetch(): non-2xx, near-empty text and modified-date fields on FetchFailure ----------------

def test_fetch_failure_carries_status_and_final_url_after_redirect():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/old":
            return httpx.Response(302, headers={"location": "https://example.org/blocked"})
        return httpx.Response(403, headers={"content-type": "text/html"}, content=b"<html></html>")

    result = fetch("https://example.org/old", client=client_for(handler))
    assert isinstance(result, FetchFailure)
    assert result.final_url == "https://example.org/blocked"
    assert result.status == 403


# --- modified date (SHOULD 3) -------------------------------------------------------------------

def test_metadata_modified_from_article_modified_time():
    html = (f"<html><head><title>t</title>"
            f'<meta property="article:modified_time" content="2024-06-01T00:00:00Z"></head>'
            f"<body><p>Body.</p>{PADDING}</body></html>")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=html.encode())

    result = fetch("https://example.org/article", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.modified == date(2024, 6, 1)
    assert result.metadata.modified_field == "article:modified_time"


def test_metadata_modified_from_ldjson_datemodified():
    html = ('<html><head><title>t</title><script type="application/ld+json">'
            '{"@type": "Article", "dateModified": "2023-09-15"}</script></head>'
            f"<body><p>Body.</p>{PADDING}</body></html>")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html"}, content=html.encode())

    result = fetch("https://example.org/article", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.modified == date(2023, 9, 15)
    assert result.metadata.modified_field == "json-ld:dateModified"


def test_metadata_modified_falls_back_to_last_modified_header():
    html = f"<html><body><p>Body.</p>{PADDING}</body></html>"

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html",
                                             "last-modified": "Wed, 21 Oct 2015 07:28:00 GMT"},
                               content=html.encode())

    result = fetch("https://example.org/article", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.modified == date(2015, 10, 21)
    assert result.metadata.modified_field == "http:last-modified"


def test_metadata_modified_prefers_article_meta_over_last_modified_header():
    html = (f"<html><head>"
            f'<meta property="article:modified_time" content="2024-06-01T00:00:00Z"></head>'
            f"<body><p>Body.</p>{PADDING}</body></html>")

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, headers={"content-type": "text/html",
                                             "last-modified": "Wed, 21 Oct 2015 07:28:00 GMT"},
                               content=html.encode())

    result = fetch("https://example.org/article", client=client_for(handler))
    assert isinstance(result, Fetched)
    assert result.metadata.modified == date(2024, 6, 1)
    assert result.metadata.modified_field == "article:modified_time"


# --- FetchCache / fetch_all (MUST 1: cache failures per canonical URL within a run) -------------

def test_fetch_cache_fetches_a_repeated_url_only_once():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=f"<html><body><p>Once.</p>{PADDING}</body></html>".encode())

    cache = FetchCache(client=client_for(handler))
    first = cache.fetch("https://example.org/page")
    second = cache.fetch("https://example.org/page")
    assert isinstance(first, Fetched) and isinstance(second, Fetched)
    assert len(calls) == 1


def test_fetch_cache_caches_failures_too():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(403, headers={"content-type": "text/html"}, content=b"<html></html>")

    cache = FetchCache(client=client_for(handler))
    first = cache.fetch("https://example.org/blocked")
    second = cache.fetch("https://example.org/blocked")
    assert isinstance(first, FetchFailure) and isinstance(second, FetchFailure)
    assert first.reason == second.reason == "http 403"
    assert len(calls) == 1


def test_fetch_cache_treats_tracking_params_as_the_same_canonical_url():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=f"<html><body><p>Once.</p>{PADDING}</body></html>".encode())

    cache = FetchCache(client=client_for(handler))
    cache.fetch("https://example.org/page?utm_source=newsletter")
    cache.fetch("https://example.org/page")
    assert len(calls) == 1
    assert len(cache) == 1


def test_fetch_all_dedupes_across_a_batch_of_urls():
    calls = []

    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(str(request.url))
        return httpx.Response(200, headers={"content-type": "text/html"},
                               content=f"<html><body><p>Once.</p>{PADDING}</body></html>".encode())

    client = client_for(handler)
    results = fetch_all(["https://example.org/page", "https://example.org/page?utm_source=x",
                        "https://example.org/other"], client=client)
    assert len(calls) == 2  # /page fetched once despite being requested twice
    assert set(results) == {"https://example.org/page", "https://example.org/page?utm_source=x",
                            "https://example.org/other"}
    assert isinstance(results["https://example.org/page"], Fetched)


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
