"""I7: planted documents for `reconstruct.admission.admit`, against one invented gold. Every
blocklisted plant is dated before the gold, so the blocklist alone rejects it; every date plant
is unrelated to the gold, so the date alone rejects it. The near-misses must be admitted."""
from __future__ import annotations

from datetime import date

from reconstruct.admission import Blocklist, Document

GOLD_DATE = date(1994, 6, 1)
BLOCKLIST = Blocklist.of(
    dois=["10.9999/gold.1994.001"],
    titles=["Cognitive Task Analysis of Fault Diagnosis in Process Control"],
    urls=["https://www.example-journal.org/article/gold-1994"],
)


def _doc(url: str, published: date | None, field: str | None = "citation_publication_date", **kw) -> Document:
    return Document(url=url, published=published, published_field=field if published else None, **kw)


PLANTED: tuple[tuple[str, Document, str | None], ...] = (
    ("after the gold", _doc("https://a.example/1", date(1995, 1, 10)), "on_or_after_gold"),
    ("one day after the gold", _doc("https://a.example/2", date(1994, 6, 2)), "on_or_after_gold"),
    ("on the gold's date", _doc("https://a.example/3", date(1994, 6, 1)), "on_or_after_gold"),
    ("revised after the gold", _doc("https://a.example/4", date(1990, 1, 1), modified=date(2015, 3, 1),
                                    modified_field="article:modified_time"), "on_or_after_gold"),
    ("undated", _doc("https://a.example/5", None), "undated"),
    ("modification date only", _doc("https://a.example/6", None, modified=date(1993, 1, 1),
                                    modified_field="json-ld:dateModified"), "undated"),
    ("Last-Modified only", _doc("https://a.example/7", None, modified=date(1993, 1, 1),
                                modified_field="http:last-modified"), "last_modified_only"),
    ("Last-Modified as the published date", _doc("https://a.example/8", date(1993, 1, 1),
                                                 field="http:last-modified"), "last_modified_only"),
    ("gold DOI, other case and resolver prefix", _doc("https://a.example/9", date(1993, 1, 1),
                                                      doi="https://doi.org/10.9999/GOLD.1994.001"), "blocklist_doi"),
    ("gold DOI inside a landing-page URL", _doc("https://journals.example.org/doi/full/10.9999/gold.1994.001",
                                                date(1993, 1, 1)), "blocklist_doi"),
    ("gold title, other case, punctuation and spacing",
     _doc("https://a.example/11", date(1993, 1, 1),
          title="COGNITIVE task analysis of fault-diagnosis  in process control."), "blocklist_title"),
    ("gold landing page, other scheme, host prefix, slash and fragment",
     _doc("http://example-journal.org/article/gold-1994/#abstract", date(1993, 1, 1)), "blocklist_url"),
    ("gold landing page reached by redirect", _doc("https://a.example/13", date(1993, 1, 1),
                                                   final_url="https://example-journal.org/article/gold-1994"),
     "blocklist_url"),
    ("properly dated scholarly record", _doc("https://doi.org/10.9999/other.1990.7", date(1990, 3, 1),
                                             doi="10.9999/other.1990.7",
                                             title="Troubleshooting strategies of process operators"), None),
    ("near-miss: longer title containing the gold's", _doc(
        "https://a.example/15", date(1992, 5, 1),
        title="A precursor to cognitive task analysis of fault diagnosis in process control"), None),
    ("near-miss: the gold's DOI plus one character", _doc("https://a.example/16", date(1992, 5, 1),
                                                      doi="10.9999/gold.1994.0010"), None),
    ("near-miss: Last-Modified after the gold beside a pre-gold publication date",
     _doc("https://a.example/17", date(1990, 3, 1), modified=date(2024, 2, 2),
          modified_field="http:last-modified"), None),
)
