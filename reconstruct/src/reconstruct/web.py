"""Fetch, HTML -> visible text, page metadata, content-addressed snapshot store.

Visible text is what a person sees: script/style/noscript/template/svg/head content, and any
element hidden by the `hidden` attribute, `aria-hidden="true"`, or an inline
display:none/visibility:hidden style, is dropped along with its descendants. This is also the
first prompt-injection defence (R11): text an author hid from readers never reaches a model.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

import httpx
import pypdf
from pypdf.errors import PyPdfError

USER_AGENT = "edu_proj-reconstruct/0.1 (+https://github.com/AdamKrysztopa/edu_proj; research use, contact via repo)"
TIMEOUT_S = 20.0
MAX_BYTES = 5 * 1024 * 1024
_HTML_TYPES = {"text/html", "application/xhtml+xml"}
_PDF_TYPE = "application/pdf"

# A page below this length is near-empty regardless of content (fixture evidence: E-LIVE's rejected
# bot walls ran 0-209 chars; the shortest real article body observed was well over 1000).
_MIN_VISIBLE_CHARS = 500
# Bot-wall/captcha pages are themselves short; the marker check only fires below this length so a
# long, legitimate page that happens to mention "captcha" in passing is never misflagged.
_BOT_WALL_MAX_CHARS = 3000
_BOT_WALL_RE = re.compile(
    r"access denied|enable javascript|checking your browser|verifying you are human|"
    r"verify you are a human|are you a robot|attention required|just a moment|"
    r"please enable cookies|cloudflare|i'm not a robot|captcha",
    re.IGNORECASE)

# Void elements never receive a matching end tag; they must not be pushed onto the drop-scope
# stack or every later close tag misreads the scope.
_VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta",
              "param", "source", "track", "wbr"}
_DROP_TAGS = {"script", "style", "noscript", "template", "svg", "head"}
_BLOCK_TAGS = {"p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6", "tr",
               "table", "section", "article", "header", "footer", "blockquote", "pre"}
_DISPLAY_NONE_RE = re.compile(r"display\s*:\s*none")
_VISIBILITY_HIDDEN_RE = re.compile(r"visibility\s*:\s*hidden")

# Priority order for the published date (A9: latest of published/modified is picked by the
# caller from the recorded fields; this module records what each field parsed to).
_DATE_META_FIELDS = ("citation_publication_date", "article:published_time", "dc.date")

# D3: pypdf's CID-font decoding (and some malformed encodings) can leave lone UTF-16 surrogates
# in extracted text; hashlib.sha256(text.encode()) then raises UnicodeEncodeError ("surrogates
# not allowed") and aborts the whole fetch phase. Replaced with U+FFFD at extraction time — before
# any hashing or normalisation — so snapshot text, its hash and every span offset stay consistent.
_LONE_SURROGATE_RE = re.compile("[\ud800-\udfff]")


def _sanitize_surrogates(text: str) -> str:
    return _LONE_SURROGATE_RE.sub("�", text)


def _is_hidden(attrs: dict[str, str | None]) -> bool:
    if "hidden" in attrs:
        return True
    if (attrs.get("aria-hidden") or "").strip().casefold() == "true":
        return True
    style = (attrs.get("style") or "").casefold()
    return bool(_DISPLAY_NONE_RE.search(style) or _VISIBILITY_HIDDEN_RE.search(style))


_LDJSON_DATE_KEYS = ("datePublished", "dateModified")


def _ldjson_dates(blob: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {key: [] for key in _LDJSON_DATE_KEYS}
    try:
        data = json.loads(blob)
    except (json.JSONDecodeError, ValueError):
        return found

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key in _LDJSON_DATE_KEYS and isinstance(value, str):
                    found[key].append(value)
                else:
                    walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)
    return found


def _parse_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).date()
    except ValueError:
        pass
    try:
        return date.fromisoformat(value[:10])
    except ValueError:
        return None


def _parse_http_date(value: str | None) -> date | None:
    """RFC 1123 (the HTTP `Last-Modified` header format), e.g. 'Wed, 21 Oct 2015 07:28:00 GMT'."""
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    return parsed.date() if parsed is not None else None


class _PageParser(HTMLParser):
    """Single pass: collects visible text plus the metadata fields fetch() needs."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._drop_stack: list[bool] = []
        self._parts: list[str] = []
        self.title: str | None = None
        self._in_title = False
        self.meta_tags: list[dict[str, str | None]] = []
        self._ldjson_blocks: list[str] = []
        self._in_ldjson = False

    def _dropping(self) -> bool:
        return self._drop_stack[-1] if self._drop_stack else False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        own_drop = tag in _DROP_TAGS or _is_hidden(attrs_dict)
        effective = self._dropping() or own_drop

        if tag == "meta":
            self.meta_tags.append(attrs_dict)
        if tag == "title":
            self._in_title = True
        if tag == "script" and (attrs_dict.get("type") or "").strip().casefold() == "application/ld+json":
            self._in_ldjson = True

        if tag in _BLOCK_TAGS and not effective:
            self._parts.append("\n")
        if tag not in _VOID_TAGS:
            self._drop_stack.append(effective)

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        if tag == "script":
            self._in_ldjson = False
        if tag not in _VOID_TAGS and self._drop_stack:
            was_dropping = self._drop_stack.pop()
            if tag in _BLOCK_TAGS and not was_dropping:
                self._parts.append("\n")

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self.title = (self.title or "") + data
        if self._in_ldjson:
            self._ldjson_blocks.append(data)
        if not self._dropping():
            self._parts.append(data)

    def visible_text(self) -> str:
        raw = "".join(self._parts)
        lines = [" ".join(line.split()) for line in raw.splitlines()]
        return "\n".join(line for line in lines if line).strip()

    def ldjson_text(self) -> str:
        return "".join(self._ldjson_blocks)


@dataclass(frozen=True)
class Metadata:
    title: str | None
    publisher: str | None
    published: date | None
    published_field: str | None
    modified: date | None = None
    modified_field: str | None = None


@dataclass(frozen=True)
class Fetched:
    requested_url: str
    final_url: str
    status: int
    content_type: str
    retrieved: datetime
    raw_sha256: str
    text: str
    text_sha256: str
    metadata: Metadata


@dataclass(frozen=True)
class FetchFailure:
    requested_url: str
    reason: str
    final_url: str | None = None
    status: int | None = None


def _extract_metadata(html: str, *, host: str) -> Metadata:
    parser = _PageParser()
    parser.feed(html)
    title = (parser.title or "").strip() or None

    meta_by_key: dict[str, str] = {}
    site_name: str | None = None
    for attrs in parser.meta_tags:
        content = attrs.get("content")
        if content is None:
            continue
        name = (attrs.get("name") or attrs.get("property") or "").strip().casefold()
        if not name:
            continue
        meta_by_key.setdefault(name, content)
        if name == "og:site_name" and site_name is None:
            site_name = content
        if name == "og:title" and title is None:
            title = content

    ldjson = _ldjson_dates(parser.ldjson_text())

    published: date | None = None
    published_field: str | None = None
    for field in _DATE_META_FIELDS:
        raw = meta_by_key.get(field)
        if raw is None:
            continue
        parsed = _parse_date(raw)
        if parsed is not None:
            published, published_field = parsed, field
            break
    if published is None:
        for raw in ldjson["datePublished"]:
            parsed = _parse_date(raw)
            if parsed is not None:
                published, published_field = parsed, "json-ld:datePublished"
                break

    modified: date | None = None
    modified_field: str | None = None
    raw = meta_by_key.get("article:modified_time")
    if raw is not None:
        parsed = _parse_date(raw)
        if parsed is not None:
            modified, modified_field = parsed, "article:modified_time"
    if modified is None:
        for raw in ldjson["dateModified"]:
            parsed = _parse_date(raw)
            if parsed is not None:
                modified, modified_field = parsed, "json-ld:dateModified"
                break

    publisher = site_name or host
    return Metadata(title=title, publisher=publisher, published=published, published_field=published_field,
                     modified=modified, modified_field=modified_field)


def extract_visible_text(html: str) -> str:
    parser = _PageParser()
    parser.feed(html)
    return parser.visible_text()


def _near_empty_or_bot_wall_reason(text: str) -> str | None:
    """MUST 1: reject near-empty pages and short bot-wall/captcha challenge pages. The marker
    check is scoped to short pages only, so a long legitimate page that mentions "captcha" in
    passing is never misflagged."""
    stripped = text.strip()
    if len(stripped) < _MIN_VISIBLE_CHARS:
        return f"too little visible text ({len(stripped)} chars)"
    if len(stripped) <= _BOT_WALL_MAX_CHARS:
        match = _BOT_WALL_RE.search(stripped)
        if match:
            return f"bot-wall or challenge page marker matched: {match.group(0)!r}"
    return None


def _extract_pdf(raw: bytes, *, host: str) -> tuple[str, Metadata] | str:
    """Extract text and metadata from a PDF (SHOULD 2). Returns (text, metadata) on success, or
    a FetchFailure reason string on failure (encrypted, corrupt, or image-only/no extractable
    text). Page boundaries become paragraph breaks in `text`, the same as block elements do for
    HTML in `extract_visible_text`."""
    try:
        reader = pypdf.PdfReader(io.BytesIO(raw))
    except (PyPdfError, ValueError) as e:
        return f"unreadable PDF: {e}"

    if reader.is_encrypted:
        try:
            decrypted = reader.decrypt("")
        except (PyPdfError, NotImplementedError):
            decrypted = 0
        if not decrypted:
            return "encrypted PDF"

    try:
        pages = [(page.extract_text() or "").strip() for page in reader.pages]
    except (PyPdfError, ValueError) as e:
        return f"unreadable PDF: {e}"
    text = "\n\n".join(p for p in pages if p)
    if not text:
        return "image-only or empty PDF text"

    info = reader.metadata
    title = (info.title or "").strip() or None if info and info.title else None
    published = info.creation_date.date() if info and info.creation_date else None
    modified = info.modification_date.date() if info and info.modification_date else None
    metadata = Metadata(title=title, publisher=host, published=published,
                        published_field="pdf:CreationDate" if published else None,
                        modified=modified, modified_field="pdf:ModDate" if modified else None)
    return text, metadata


def fetch(url: str, *, client: httpx.Client) -> Fetched | FetchFailure:
    try:
        with client.stream("GET", url, headers={"User-Agent": USER_AGENT}, follow_redirects=True,
                            timeout=TIMEOUT_S) as response:
            final_url = str(response.url)
            status = response.status_code
            content_type = response.headers.get("content-type", "")
            last_modified_header = response.headers.get("last-modified")
            if not (200 <= status < 300):
                return FetchFailure(requested_url=url, final_url=final_url, status=status,
                                     reason=f"http {status}")
            chunks: list[bytes] = []
            total = 0
            for chunk in response.iter_bytes():
                total += len(chunk)
                if total > MAX_BYTES:
                    return FetchFailure(requested_url=url, final_url=final_url, status=status,
                                         reason=f"exceeds size cap of {MAX_BYTES} bytes")
                chunks.append(chunk)
            raw = b"".join(chunks)
    except httpx.HTTPError as e:
        return FetchFailure(requested_url=url, reason=f"request failed: {e!r}")

    mime = content_type.split(";", 1)[0].strip().casefold()
    host = httpx.URL(final_url).host
    raw_sha256 = hashlib.sha256(raw).hexdigest()

    if mime in _HTML_TYPES:
        html = raw.decode(response.encoding or "utf-8", errors="replace")
        text = _sanitize_surrogates(extract_visible_text(html))
        metadata = _extract_metadata(html, host=host)
    elif mime == _PDF_TYPE:
        result = _extract_pdf(raw, host=host)
        if isinstance(result, str):
            return FetchFailure(requested_url=url, final_url=final_url, status=status, reason=result)
        text, metadata = result
        text = _sanitize_surrogates(text)
    else:
        return FetchFailure(requested_url=url, final_url=final_url, status=status,
                             reason=f"unsupported content type: {content_type or 'unknown'}")

    reject_reason = _near_empty_or_bot_wall_reason(text)
    if reject_reason is not None:
        return FetchFailure(requested_url=url, final_url=final_url, status=status, reason=reject_reason)

    if metadata.modified is None:
        header_date = _parse_http_date(last_modified_header)
        if header_date is not None:
            metadata = replace(metadata, modified=header_date, modified_field="http:last-modified")

    text_sha256 = hashlib.sha256(text.encode()).hexdigest()
    return Fetched(requested_url=url, final_url=final_url, status=status, content_type=content_type,
                    retrieved=datetime.now(UTC), raw_sha256=raw_sha256, text=text,
                    text_sha256=text_sha256, metadata=metadata)


class FetchCache:
    """Caches fetch() results — success or failure — per canonical URL for the life of one run
    (MUST 1 / defect 13): the same URL cited by two searches, or retried after a first failure,
    is fetched at most once. Canonicalisation is `evidence.canonical_url`'s (drop fragment and
    tracking params); it is imported here, not duplicated, since evidence.py owns that function."""

    def __init__(self, *, client: httpx.Client) -> None:
        from reconstruct.evidence import canonical_url  # local: avoids a module-load-order cycle
        self._canonical_url = canonical_url
        self._client = client
        self._by_canonical: dict[str, Fetched | FetchFailure] = {}

    def fetch(self, url: str) -> Fetched | FetchFailure:
        key = self._canonical_url(url)
        cached = self._by_canonical.get(key)
        if cached is not None:
            return cached
        result = fetch(url, client=self._client)
        self._by_canonical[key] = result
        if isinstance(result, Fetched):
            final_key = self._canonical_url(result.final_url)
            self._by_canonical.setdefault(final_key, result)
        return result

    def __len__(self) -> int:
        return len(self._by_canonical)


def fetch_all(urls: Iterable[str], *, client: httpx.Client,
              cache: FetchCache | None = None) -> dict[str, Fetched | FetchFailure]:
    """Fetch many URLs, deduping by canonical URL through a `FetchCache` (MUST 1). Pass a shared
    `cache` across calls to dedupe across an entire run, not just within one batch."""
    cache = cache if cache is not None else FetchCache(client=client)
    return {url: cache.fetch(url) for url in urls}


class SnapshotStore:
    """Content-addressed raw bytes and extracted text (§ Run artefacts): reconstruct/runs/.../snapshots."""

    def __init__(self, directory: str | Path) -> None:
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)

    def write_raw(self, raw: bytes) -> str:
        sha256 = hashlib.sha256(raw).hexdigest()
        path = self.dir / f"{sha256}.raw"
        if not path.exists():
            path.write_bytes(raw)
        return sha256

    def write_text(self, text: str) -> str:
        sha256 = hashlib.sha256(text.encode()).hexdigest()
        path = self.dir / f"{sha256}.txt"
        if not path.exists():
            path.write_text(text, encoding="utf-8")
        return sha256

    def read_raw(self, sha256: str) -> bytes:
        return (self.dir / f"{sha256}.raw").read_bytes()

    def read_text(self, sha256: str) -> str:
        return (self.dir / f"{sha256}.txt").read_text(encoding="utf-8")
