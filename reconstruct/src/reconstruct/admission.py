"""I7: historical admission. Which documents may enter a reconstruction scored against a gold that
became public on `gold_date` (REORIENTATION.md §14.3; coverage audit findings 15 and 21).

A document is admitted only with a publication date from the page itself, before the gold. An HTTP
`Last-Modified` header is server file time, not evidence of a date in either direction: it cannot
date a document, and it cannot reject one. A page-stated modification date after the gold rejects,
since the bytes held are then a post-gold revision. The gold itself is kept out by DOI, normalised
title or landing-page URL, whatever the document's date."""
from __future__ import annotations

import re
import unicodedata
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date
from urllib.parse import unquote, urlsplit

LAST_MODIFIED_FIELD = "http:last-modified"
"""`reconstruct.web`'s `modified_field` for a date read from the `Last-Modified` header."""

_DOI = re.compile(r"10\.\d{4,9}/[^\s?#]+", re.IGNORECASE)


def normalise_doi(value: str) -> str | None:
    match = _DOI.search(unquote(value))
    return match.group(0).rstrip("./").casefold() if match else None


def normalise_title(value: str) -> str:
    return " ".join(re.sub(r"[\W_]+", " ", unicodedata.normalize("NFKC", value).casefold()).split())


def normalise_url(value: str) -> str:
    """Host without `www.`, path without a trailing slash, query kept; scheme, port and fragment dropped."""
    parts = urlsplit(value.strip())
    host = (parts.hostname or "").casefold().removeprefix("www.")
    query = f"?{parts.query}" if parts.query else ""
    return f"{host}{unquote(parts.path).rstrip('/')}{query}"


@dataclass(frozen=True)
class Blocklist:
    dois: frozenset[str]
    titles: frozenset[str]
    urls: frozenset[str]

    @classmethod
    def of(cls, *, dois: Iterable[str] = (), titles: Iterable[str] = (), urls: Iterable[str] = ()) -> Blocklist:
        return cls(dois=frozenset(d for d in map(normalise_doi, dois) if d),
                   titles=frozenset(map(normalise_title, titles)), urls=frozenset(map(normalise_url, urls)))


@dataclass(frozen=True)
class Document:
    url: str
    published: date | None
    published_field: str | None = None
    modified: date | None = None
    modified_field: str | None = None
    title: str | None = None
    doi: str | None = None
    final_url: str | None = None


@dataclass(frozen=True)
class Admission:
    admitted: bool
    reasons: tuple[str, ...]


def _blocked(doc: Document, blocklist: Blocklist) -> list[str]:
    urls = [u for u in (doc.url, doc.final_url) if u]
    dois = {d for d in map(normalise_doi, [*urls, *([doc.doi] if doc.doi else [])]) if d}
    reasons = []
    if any(d == b or d.startswith(b + "/") for d in dois for b in blocklist.dois):
        reasons.append("blocklist_doi")
    if doc.title and normalise_title(doc.title) in blocklist.titles:
        reasons.append("blocklist_title")
    if any(normalise_url(u) in blocklist.urls for u in urls):
        reasons.append("blocklist_url")
    return reasons


def admit(document: Document, gold_date: date, blocklist: Blocklist) -> Admission:
    """Every reason a document is refused, in a fixed order; admitted iff there is none. A document
    dated on the gold's own day is refused: a day's precision cannot order the two."""
    reasons = _blocked(document, blocklist)
    published = None if document.published_field == LAST_MODIFIED_FIELD else document.published
    if published is None:
        header_only = LAST_MODIFIED_FIELD in (document.published_field, document.modified_field)
        reasons.append("last_modified_only" if header_only else "undated")
    else:
        stated = [published]
        if document.modified is not None and document.modified_field != LAST_MODIFIED_FIELD:
            stated.append(document.modified)
        if max(stated) >= gold_date:
            reasons.append("on_or_after_gold")
    return Admission(admitted=not reasons, reasons=tuple(reasons))
