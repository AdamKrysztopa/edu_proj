"""Pure, deterministic core of N2a: normalisation, span location, canonical URLs, independence
clustering, source typing, and every construction of residual's Evidence/Selector/Verification.
No network calls, no model calls — everything here is a function of its arguments alone.
"""
from __future__ import annotations

import difflib
import hashlib
import json
import math
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from typing import Mapping, Sequence
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from tldextract import TLDExtract

from residual.claims import ClaimRecord, Scope
from residual.ledger import Area, Contradiction
from residual.provenance import (
    Agent,
    Evidence,
    Generation,
    Search,
    Selector,
    Source,
    Verdict,
    Verification,
    short_hash,
)
from residual.vocab import KnowledgeType, Layer, Question, SourceKind, Voice, World

_EXTRACT = TLDExtract(suffix_list_urls=(), include_psl_private_domains=True)

# --- normalisation ------------------------------------------------------------------------

_ZERO_WIDTH_AND_SOFT_HYPHEN = "­​‌‍﻿"
_CHAR_MAP = {"‘": "'", "’": "'", "“": '"', "”": '"',
             "–": "-", "—": "-"}
_WHITESPACE_RE = re.compile(r"\s+")


def normalise(text: str) -> str:
    """NFKC; drop soft hyphens/zero-width chars; curly quotes -> straight; en/em dash ->
    hyphen; collapse all whitespace (including newlines) to a single space. No case folding,
    no fuzzy matching — this is the one text form every span offset is measured against."""
    text = unicodedata.normalize("NFKC", text)
    for ch in _ZERO_WIDTH_AND_SOFT_HYPHEN:
        text = text.replace(ch, "")
    for src, dst in _CHAR_MAP.items():
        text = text.replace(src, dst)
    return _WHITESPACE_RE.sub(" ", text).strip()


def word_count(text: str) -> int:
    return len(text.split(" ")) if text else 0


def locate(quote: str, haystack_normalised: str) -> tuple[int, int] | None:
    """6-80 words, exact after normalisation, contiguous. `haystack_normalised` must already
    be normalise()'d; the caller normalises the document text once and reuses it."""
    q = normalise(quote)
    if not (6 <= word_count(q) <= 80):
        return None
    idx = haystack_normalised.find(q)
    if idx == -1:
        return None
    return idx, idx + len(q)


def quote_in_span(quote: str, span_exact: str) -> bool:
    """A5: a supporting/contradiction quote counts only if it is a substring of the span it is
    claimed to come from, after the same normalisation. `span_exact` is assumed already
    normalised (it is a slice of our normalised text)."""
    q = normalise(quote)
    return bool(q) and q in span_exact


# --- prompt-injection flag (spans, not the whole page: web.py already strips hidden text) -----

_INJECTION_RE = re.compile(
    r"ignore previous|ignore all|you are now|system:|<\||assistant:", re.IGNORECASE)


def injection_flag(span_text: str) -> bool:
    return bool(_INJECTION_RE.search(span_text))


# --- question/template rejection (A1) ----------------------------------------------------

PROBES: tuple[KnowledgeType, ...] = (
    KnowledgeType.CONCEPT, KnowledgeType.DECISION, KnowledgeType.CUE, KnowledgeType.CHECK,
    KnowledgeType.FAILURE_MODE, KnowledgeType.NORM, KnowledgeType.RATIONALE,
)

TEMPLATES: dict[KnowledgeType, str] = {
    KnowledgeType.CONCEPT: "What concepts, principles or definitions govern {area}?",
    KnowledgeType.DECISION: "What conditions determine which option is chosen in {area}?",
    KnowledgeType.CUE: ("What observable features of a situation signal that {area} applies "
                        "or needs a different response?"),
    KnowledgeType.CHECK: "How is work in {area} checked for correctness or compliance?",
    KnowledgeType.FAILURE_MODE: "How does work in {area} typically go wrong, and what are the signs?",
    KnowledgeType.NORM: "What counts as acceptable or sufficient work in {area}?",
    KnowledgeType.RATIONALE: "Why is {area} done the way it is?",
}


def is_question_or_template(assertion: str, area_name: str) -> bool:
    a = assertion.strip()
    if a.endswith("?"):
        return True
    filled = {t.format(area=area_name).casefold() for t in TEMPLATES.values()}
    return a.casefold() in filled


def probe_question(probe: KnowledgeType) -> Question:
    return Question.DOMAIN if probe is KnowledgeType.CONCEPT else Question.PERFORMANCE


def layer_for_question(question: Question) -> Layer:
    return Layer.DOMAIN_STRUCTURE if question is Question.DOMAIN else Layer.PERFORMANCE


# --- canonical URL / registrable domain (A7, A9) -------------------------------------------

_TRACKING_PARAMS = {"gclid", "fbclid", "msclkid", "mc_cid", "mc_eid", "ref", "ref_src", "igshid"}


def _is_tracking_param(key: str) -> bool:
    k = key.casefold()
    return k.startswith("utm_") or k in _TRACKING_PARAMS


def canonical_url(url: str) -> str:
    """Drop the fragment and utm_*/tracking params; keep everything else, including query
    param order, so distinct resources never collapse into one Source by accident."""
    parts = urlsplit(url)
    kept = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if not _is_tracking_param(k)]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(kept), ""))


def registrable_domain(url: str) -> str:
    """Offline PSL lookup. When the host's suffix is not recognised at all (no real TLD —
    a reserved documentation domain like `.example`, or a bare hostname), fall back to the
    full host rather than collapsing every such host into one empty-string 'domain'."""
    host = urlsplit(url).netloc.rsplit("@", 1)[-1].split(":", 1)[0] or url
    result = _EXTRACT(host)
    return result.top_domain_under_public_suffix if result.suffix else host


# --- host-rule table for Source kind/voice/boundary (A9) -----------------------------------

@dataclass(frozen=True)
class SourceClassification:
    kind: SourceKind
    kind_rule: str
    voice: Voice
    voice_rule: str
    boundary: bool


def _is_forum_host(host: str) -> bool:
    forum_hosts = {"stackoverflow.com", "serverfault.com", "superuser.com", "askubuntu.com",
                   "reddit.com", "news.ycombinator.com"}
    return host in forum_hosts or host.endswith(".stackexchange.com") or host.endswith(".reddit.com")


_KIND_RULES: tuple[tuple[str, callable, SourceKind], ...] = (
    ("forum-qa-site", _is_forum_host, SourceKind.FORUM_POST),
    ("docs-readthedocs", lambda h: h.endswith("readthedocs.io") or h.endswith("readthedocs.org"),
     SourceKind.DOCUMENTATION),
    ("docs-github", lambda h: h == "github.com" or h.endswith(".github.io"), SourceKind.DOCUMENTATION),
    ("docs-wikipedia", lambda h: h.endswith("wikipedia.org"), SourceKind.DOCUMENTATION),
    ("standard-body", lambda h: h.endswith("iso.org") or h.endswith("ietf.org")
     or h.endswith("w3.org"), SourceKind.STANDARD),
)


def classify_source(url: str) -> SourceClassification:
    host = urlsplit(url).netloc.split(":", 1)[0].casefold()
    for rule_name, predicate, kind in _KIND_RULES:
        if predicate(host):
            break
    else:
        rule_name, kind = "default-documentation", SourceKind.DOCUMENTATION
    if kind is SourceKind.FORUM_POST:
        return SourceClassification(kind=kind, kind_rule=rule_name, voice=Voice.MIXED,
                                     voice_rule="forum-mixed-boundary", boundary=True)
    return SourceClassification(kind=kind, kind_rule=rule_name, voice=Voice.EXPERT,
                                 voice_rule="default-unassessed", boundary=False)


# --- independence clustering (A7) -----------------------------------------------------------

@dataclass(frozen=True)
class IndependenceDoc:
    source_id: str
    url: str
    text: str
    """Normalised document text."""
    spans: tuple[tuple[int, int], ...] = ()
    """Located evidence spans in this doc (char offsets into `text`)."""


def _shingles(text: str, k: int = 5) -> frozenset[str]:
    words = text.split(" ")
    if len(words) < k:
        return frozenset()
    return frozenset(" ".join(words[i:i + k]) for i in range(len(words) - k + 1))


def _containment(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / min(len(a), len(b))


def _word_ranges(text: str) -> list[tuple[int, int]]:
    ranges = []
    pos = 0
    for w in text.split(" "):
        ranges.append((pos, pos + len(w)))
        pos += len(w) + 1
    return ranges


def _overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] < b[1] and b[0] < a[1]


def _shared_run_links_spans(a: IndependenceDoc, b: IndependenceDoc, min_words: int = 25) -> bool:
    words_a, words_b = a.text.split(" "), b.text.split(" ")
    ranges_a, ranges_b = _word_ranges(a.text), _word_ranges(b.text)
    sm = difflib.SequenceMatcher(None, words_a, words_b, autojunk=False)
    for block in sm.get_matching_blocks():
        if block.size < min_words:
            continue
        range_a = (ranges_a[block.a][0], ranges_a[block.a + block.size - 1][1])
        range_b = (ranges_b[block.b][0], ranges_b[block.b + block.size - 1][1])
        if any(_overlaps(range_a, s) for s in a.spans) or any(_overlaps(range_b, s) for s in b.spans):
            return True
    return False


@dataclass(frozen=True)
class IndependenceResult:
    key_by_source: Mapping[str, str]
    reason_by_source: Mapping[str, str]


def independence_clusters(docs: Sequence[IndependenceDoc]) -> IndependenceResult:
    """Union-find over fetched docs (A7): same registrable domain, 5-shingle containment
    >= 0.5, or a >=25-word verbatim run overlapping an evidence span in either doc."""
    parent = {d.source_id: d.source_id for d in docs}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    edge_reason: dict[frozenset[str], str] = {}

    def union(x: str, y: str, reason: str) -> None:
        edge_reason.setdefault(frozenset((x, y)), reason)
        rx, ry = find(x), find(y)
        if rx != ry:
            hi, lo = max(rx, ry), min(rx, ry)
            parent[hi] = lo

    domains = {d.source_id: registrable_domain(d.url) for d in docs}
    shingle_sets = {d.source_id: _shingles(d.text) for d in docs}

    for i, a in enumerate(docs):
        for b in docs[i + 1:]:
            if domains[a.source_id] == domains[b.source_id]:
                union(a.source_id, b.source_id, "same registrable domain")
            elif _containment(shingle_sets[a.source_id], shingle_sets[b.source_id]) >= 0.5:
                union(a.source_id, b.source_id, "5-shingle containment >= 0.5")
            elif _shared_run_links_spans(a, b):
                union(a.source_id, b.source_id, "shared >=25-word run overlapping an evidence span")

    clusters: dict[str, list[str]] = {}
    for d in docs:
        clusters.setdefault(find(d.source_id), []).append(d.source_id)

    key_by_root = {root: "ind-" + min(members) for root, members in clusters.items()}
    key_by_source = {d.source_id: key_by_root[find(d.source_id)] for d in docs}
    reason_by_source: dict[str, str] = {}
    for d in docs:
        root = find(d.source_id)
        if len(clusters[root]) == 1:
            reason_by_source[d.source_id] = f"singleton (domain={domains[d.source_id]})"
            continue
        for members in (frozenset((d.source_id, other)) for other in clusters[root] if other != d.source_id):
            if members in edge_reason:
                reason_by_source[d.source_id] = edge_reason[members]
                break
        else:
            reason_by_source[d.source_id] = "linked transitively"
    return IndependenceResult(key_by_source=key_by_source, reason_by_source=reason_by_source)


def largest_cluster_share(key_by_source: Mapping[str, str]) -> float:
    if not key_by_source:
        return 0.0
    counts: dict[str, int] = {}
    for key in key_by_source.values():
        counts[key] = counts.get(key, 0) + 1
    return max(counts.values()) / len(key_by_source)


# --- builders: only this module constructs Evidence / Selector / Verification ---------------

def build_source(*, final_url: str, published: date | None, independence_key: str) -> Source:
    classification = classify_source(final_url)
    return Source(identifier=canonical_url(final_url), kind=classification.kind, world=World.A,
                  voice=classification.voice, independence_key=independence_key,
                  published=published, organisation=None, boundary=classification.boundary)


@dataclass(frozen=True)
class LocatedSpan:
    start: int
    end: int
    exact: str
    injection_flagged: bool


def locate_span(quote: str, doc_text_normalised: str) -> LocatedSpan | None:
    span = locate(quote, doc_text_normalised)
    if span is None:
        return None
    start, end = span
    exact = doc_text_normalised[start:end]
    return LocatedSpan(start=start, end=end, exact=exact, injection_flagged=injection_flag(exact))


def build_verification(verdict: str, *, verifier: Agent, on: date) -> Verification:
    return Verification(verdict=Verdict(verdict), verifier=verifier, on=on)


def build_evidence(*, source: Source, span: LocatedSpan, text_sha256: str, retrieved: date,
                    verification: Verification) -> Evidence:
    selector = Selector(exact=span.exact, locator=f"sha256:{text_sha256};char={span.start},{span.end}")
    return Evidence(source=source, selector=selector, retrieved=retrieved, verification=verification)


def context_window(doc_text_normalised: str, span: LocatedSpan, radius: int = 300) -> str:
    return doc_text_normalised[max(0, span.start - radius):min(len(doc_text_normalised), span.end + radius)]


def build_area(name: str, scope: Scope) -> Area:
    return Area(area_id=short_hash("a", name), scope=scope, name=name)


def build_unknown_placeholder(*, area_name: str, probe: KnowledgeType, scope: Scope,
                               searches: tuple[Search, ...]) -> ClaimRecord:
    question = probe_question(probe)
    assertion = TEMPLATES[probe].format(area=area_name)
    return ClaimRecord(assertion=assertion, question=question, layer=layer_for_question(question),
                        knowledge_type=probe, scope=scope, generation=None, searches=searches)


def build_contradiction(claim_a: str, claim_b: str, *, detected_by: Agent, spec_sha256: str) -> Contradiction:
    return Contradiction(claims=(claim_a, claim_b), detected_by=detected_by,
                          method=f"pair-classify:{spec_sha256}")


# --- merge of identical assertions (A10) -----------------------------------------------------

@dataclass(frozen=True)
class Extraction:
    """One claim as extracted from one document, before merge."""
    source_id: str
    assertion: str
    quote: str
    area_name: str
    knowledge_type: KnowledgeType
    question: Question

    @property
    def extraction_id(self) -> str:
        return short_hash("x", self.source_id, self.assertion.casefold(), self.quote)


@dataclass(frozen=True)
class MergedAssertion:
    assertion: str
    area_name: str
    knowledge_type: KnowledgeType
    question: Question
    members: tuple[Extraction, ...]
    conflict: str | None


def _majority(members: Sequence[Extraction], *, key) -> tuple[str, str | None]:
    counts: dict[str, int] = {}
    for m in members:
        counts[key(m)] = counts.get(key(m), 0) + 1
    best = max(counts.values())
    tied = sorted(v for v, c in counts.items() if c == best)
    conflict = ",".join(tied) if len(tied) > 1 else None
    return tied[0], conflict


def merge_extractions(extractions: Sequence[Extraction]) -> list[MergedAssertion]:
    groups: dict[str, list[Extraction]] = {}
    for e in extractions:
        groups.setdefault(e.assertion.casefold(), []).append(e)
    merged = []
    for key in sorted(groups):
        members = tuple(sorted(groups[key], key=lambda e: e.extraction_id))
        area_name, area_conflict = _majority(members, key=lambda e: e.area_name)
        kt_value, kt_conflict = _majority(members, key=lambda e: e.knowledge_type.value)
        question_value, _ = _majority(members, key=lambda e: e.question.value)
        parts = []
        if area_conflict:
            parts.append(f"area tie: {area_conflict}")
        if kt_conflict:
            parts.append(f"knowledge_type tie: {kt_conflict}")
        merged.append(MergedAssertion(assertion=members[0].assertion, area_name=area_name,
                                       knowledge_type=KnowledgeType(kt_value),
                                       question=Question(question_value), members=members,
                                       conflict="; ".join(parts) or None))
    return merged


def build_claim(merged: MergedAssertion, *, evidence: tuple[Evidence, ...],
                generation: Generation | None, searches: tuple[Search, ...], scope: Scope) -> ClaimRecord:
    return ClaimRecord(assertion=merged.assertion, question=merged.question,
                        layer=layer_for_question(merged.question), knowledge_type=merged.knowledge_type,
                        scope=scope, evidence=evidence, generation=generation, searches=searches)


# --- slot status (A2) ------------------------------------------------------------------------

def slot_status(*, has_criterion_claim: bool, docs_fetched_and_extracted: bool,
                 area_lost_to_truncation: bool, verifier_ran_on_all_located: bool) -> str:
    if has_criterion_claim:
        return "covered"
    if docs_fetched_and_extracted and not area_lost_to_truncation and verifier_ran_on_all_located:
        return "unknown"
    if docs_fetched_and_extracted:
        return "unverified"
    return "unexamined"


# --- decoys (A6) ------------------------------------------------------------------------------

def decoy_sample_size(n_located: int) -> int:
    if n_located <= 0:
        return 0
    target = max(5, math.ceil(0.2 * n_located))
    return min(target, 20, n_located)


def select_decoy_sample(claim_ids: Sequence[str]) -> list[str]:
    n = decoy_sample_size(len(claim_ids))
    return sorted(claim_ids)[:n]


# --- contradiction candidates (A8) -------------------------------------------------------------

_STOPWORDS = frozenset("""
a an the is are was were be been being of to in on for and or that this it as at by with from
has have had not no than then but if when which what who whom its their his her they them we you
your i he she do does did will would can could should shall may might must so such into out up
down over under again further once here there all each few more most other some own same too
very s t just don now
""".split())

_WORD_RE = re.compile(r"[a-zA-Z0-9]+")


def content_words(text: str) -> frozenset[str]:
    return frozenset(w for w in (m.group(0).casefold() for m in _WORD_RE.finditer(text))
                      if w not in _STOPWORDS and len(w) > 2)


def jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def contradiction_candidates(claims: Sequence[tuple[str, str, str]], k: int = 10) -> list[tuple[str, str]]:
    """`claims`: (claim_id, independence_key, text) tuples already restricted to one area and to
    claims with a located span. Returns up to k pairs from different independence clusters,
    ranked by content-word Jaccard, highest first."""
    words = {cid: content_words(text) for cid, _, text in claims}
    scored = []
    for i, (cid_a, key_a, _) in enumerate(claims):
        for cid_b, key_b, _ in claims[i + 1:]:
            if key_a == key_b:
                continue
            score = jaccard(words[cid_a], words[cid_b])
            pair = tuple(sorted((cid_a, cid_b)))
            scored.append((score, pair))
    scored.sort(key=lambda item: (-item[0], item[1]))
    seen: set[tuple[str, str]] = set()
    out = []
    for _, pair in scored:
        if pair in seen:
            continue
        seen.add(pair)
        out.append(pair)
        if len(out) >= k:
            break
    return out


# --- spec hashing --------------------------------------------------------------------------

def spec_sha256(prompt_text: str, schema: dict) -> str:
    return hashlib.sha256((prompt_text + json.dumps(schema, sort_keys=True)).encode()).hexdigest()
