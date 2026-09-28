"""Fetch, HTML -> visible text, page metadata, content-addressed snapshot store.

Visible text is what a person sees: script/style/noscript/template/svg/head content, and any
element hidden by the `hidden` attribute, `aria-hidden="true"`, or an inline
display:none/visibility:hidden style, is dropped along with its descendants. This is also the
first prompt-injection defence (R11): text an author hid from readers never reaches a model.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime
from html.parser import HTMLParser
from pathlib import Path

import httpx

USER_AGENT = "edu_proj-reconstruct/0.1 (+https://github.com/AdamKrysztopa/edu_proj; research use, contact via repo)"
TIMEOUT_S = 20.0
MAX_BYTES = 5 * 1024 * 1024
_HTML_TYPES = {"text/html", "application/xhtml+xml"}

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


def _is_hidden(attrs: dict[str, str | None]) -> bool:
    if "hidden" in attrs:
        return True
    if (attrs.get("aria-hidden") or "").strip().casefold() == "true":
        return True
    style = (attrs.get("style") or "").casefold()
    return bool(_DISPLAY_NONE_RE.search(style) or _VISIBILITY_HIDDEN_RE.search(style))


def _ldjson_dates(blob: str) -> list[str]:
    try:
        data = json.loads(blob)
    except (json.JSONDecodeError, ValueError):
        return []
    found: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "datePublished" and isinstance(value, str):
                    found.append(value)
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
        for raw in _ldjson_dates(parser.ldjson_text()):
            parsed = _parse_date(raw)
            if parsed is not None:
                published, published_field = parsed, "json-ld:datePublished"
                break

    publisher = site_name or host
    return Metadata(title=title, publisher=publisher, published=published, published_field=published_field)


def extract_visible_text(html: str) -> str:
    parser = _PageParser()
    parser.feed(html)
    return parser.visible_text()


def fetch(url: str, *, client: httpx.Client) -> Fetched | FetchFailure:
    try:
        with client.stream("GET", url, headers={"User-Agent": USER_AGENT}, follow_redirects=True,
                            timeout=TIMEOUT_S) as response:
            final_url = str(response.url)
            status = response.status_code
            content_type = response.headers.get("content-type", "")
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
    if mime not in _HTML_TYPES:
        return FetchFailure(requested_url=url, final_url=final_url, status=status,
                             reason=f"unsupported content type: {content_type or 'unknown'}")

    raw_sha256 = hashlib.sha256(raw).hexdigest()
    html = raw.decode(response.encoding or "utf-8", errors="replace")
    text = extract_visible_text(html)
    text_sha256 = hashlib.sha256(text.encode()).hexdigest()
    host = httpx.URL(final_url).host
    metadata = _extract_metadata(html, host=host)
    return Fetched(requested_url=url, final_url=final_url, status=status, content_type=content_type,
                    retrieved=datetime.now(UTC), raw_sha256=raw_sha256, text=text,
                    text_sha256=text_sha256, metadata=metadata)


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
