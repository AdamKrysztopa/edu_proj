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
_CHAR_MAP = {
    # quotes: every curly/guillemet/prime variant -> the one straight ASCII form (SHOULD 4)
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "‚": "'", "„": '"',              # single/double low-9 quotes
    "‹": "'", "›": "'", "«": '"', "»": '"',  # guillemets
    "′": "'",                        # prime (NFKC above already decomposes double prime "″"
                                      # into two of these, so both collapse to "''", not '"')
    # dashes
    "–": "-", "—": "-",
    # bullets, checkboxes and table-cell pipes: collapsed to a space (whitespace-collapse below
    # absorbs the rest), so a bulleted/tabular line matches the same quote with or without its
    # list marker or cell separator on either side of the comparison (SHOULD 4/5: E-LIVE lost 10
    # of 33 unlocated quotes to `|` alone).
    "|": " ", "•": " ", "▪": " ", "‣": " ", "◦": " ", "·": " ",
    "☐": " ", "☑": " ", "☒": " ", "■": " ", "□": " ", "●": " ", "○": " ",
}
_WHITESPACE_RE = re.compile(r"\s+")


def normalise(text: str) -> str:
    """NFKC; drop soft hyphens/zero-width chars; every quote style -> straight quotes; en/em
    dash -> hyphen; bullet/checkbox list markers and table-cell `|` separators -> a space;
    collapse all whitespace (including newlines) to a single space. No case folding, no fuzzy
    matching — this is the one text form every span offset is measured against. The same
    mapping runs on both the document (haystack) and the quote, so a page that renders a bullet
    list one way and a quote that renders it another way still compare exactly (SHOULD 4)."""
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
    KnowledgeType.PROCEDURE_STEP,
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
    KnowledgeType.PROCEDURE_STEP: "What steps make up {area}, and in what order?",
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


# --- host-rule table for Source kind/voice/boundary (A9, SHOULD 6) -------------------------

@dataclass(frozen=True)
class SourceClassification:
    kind: SourceKind
    kind_rule: str
    voice: Voice
    voice_rule: str
    boundary: bool
    tier: str
    """"curated" for STUDY/STANDARD and regulator guidance, "open" otherwise (SHOULD 6)."""


def _host_or_subdomain(host: str, known: frozenset[str]) -> bool:
    return host in known or any(host.endswith("." + h) for h in known)


_FORUM_HOSTS = frozenset({"stackoverflow.com", "serverfault.com", "superuser.com", "askubuntu.com",
                          "reddit.com", "news.ycombinator.com", "eng-tips.com", "plctalk.net"})


def _is_forum_host(host: str) -> bool:
    return (_host_or_subdomain(host, _FORUM_HOSTS) or host.endswith(".stackexchange.com")
            or host.startswith("forums."))


# Academic publishers, preprint servers and full-text mirrors -> STUDY.
_ACADEMIC_PUBLISHER_HOSTS = frozenset({
    "mdpi.com", "springer.com", "link.springer.com", "sciencedirect.com", "dl.acm.org",
    "arxiv.org", "doi.org", "ncbi.nlm.nih.gov", "pubmed.ncbi.nlm.nih.gov",
})


def _is_academic_publisher_host(host: str) -> bool:
    return _host_or_subdomain(host, _ACADEMIC_PUBLISHER_HOSTS)


# Legislation and official gazettes -> STANDARD, rule "legislation".
_LEGISLATION_HOSTS = frozenset({"legislation.gov.uk", "eur-lex.europa.eu"})


def _is_legislation_host(host: str) -> bool:
    return _host_or_subdomain(host, _LEGISLATION_HOSTS) or "gazette" in host


# Data-protection and workplace-safety regulators -> PROCEDURE_DOCUMENT, rule "regulator-guidance".
_REGULATOR_HOSTS = frozenset({"ico.org.uk", "edpb.europa.eu", "cnil.fr", "dataprotection.ie",
                              "cnpd.public.lu", "osha.gov", "nist.gov"})


def _is_regulator_host(host: str) -> bool:
    return _host_or_subdomain(host, _REGULATOR_HOSTS)


# Standards bodies -> STANDARD, rule "standard-body".
_STANDARDS_BODY_HOSTS = frozenset({"iso.org", "ietf.org", "w3.org", "iec.ch", "isa.org", "ieee.org"})


def _is_standards_body_host(host: str) -> bool:
    return _host_or_subdomain(host, _STANDARDS_BODY_HOSTS)


_KIND_RULES: tuple[tuple[str, callable, SourceKind], ...] = (
    ("forum-qa-site", _is_forum_host, SourceKind.FORUM_POST),
    ("docs-readthedocs", lambda h: h.endswith("readthedocs.io") or h.endswith("readthedocs.org"),
     SourceKind.DOCUMENTATION),
    ("docs-github", lambda h: h == "github.com" or h.endswith(".github.io"), SourceKind.DOCUMENTATION),
    ("docs-wikipedia", lambda h: h.endswith("wikipedia.org"), SourceKind.DOCUMENTATION),
    ("academic-publisher", _is_academic_publisher_host, SourceKind.STUDY),
    ("legislation", _is_legislation_host, SourceKind.STANDARD),
    ("regulator-guidance", _is_regulator_host, SourceKind.PROCEDURE_DOCUMENT),
    ("standard-body", _is_standards_body_host, SourceKind.STANDARD),
)

_CURATED_KINDS = frozenset({SourceKind.STUDY, SourceKind.STANDARD})
_CURATED_RULES = frozenset({"regulator-guidance"})


def _tier_for(kind: SourceKind, rule_name: str) -> str:
    return "curated" if kind in _CURATED_KINDS or rule_name in _CURATED_RULES else "open"


def classify_source(url: str) -> SourceClassification:
    host = urlsplit(url).netloc.split(":", 1)[0].casefold()
    for rule_name, predicate, kind in _KIND_RULES:
        if predicate(host):
            break
    else:
        rule_name, kind = "default-documentation", SourceKind.DOCUMENTATION
    tier = _tier_for(kind, rule_name)
    if kind is SourceKind.FORUM_POST:
        return SourceClassification(kind=kind, kind_rule=rule_name, voice=Voice.MIXED,
                                     voice_rule="forum-mixed-boundary", boundary=True, tier=tier)
    return SourceClassification(kind=kind, kind_rule=rule_name, voice=Voice.EXPERT,
                                 voice_rule="default-unassessed", boundary=False, tier=tier)


# --- independence clustering (A7, SHOULD 5) --------------------------------------------------

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


# Registrable domains that host many *independent* organisations, papers or authors, where "same
# domain" would wrongly cluster all of them (SHOULD 5b, runner (b) finding 2: europa.eu merged
# EDPB/EDPS/the Commission; a curated corpus would merge every MDPI/Springer/arXiv paper). These
# group by the full host instead of the registrable domain. `github.io`/`blogspot.com` are already
# host-granular through tldextract's private-suffix list; they are listed here too so the table is
# the single place this policy is documented, not split across two mechanisms.
_MULTI_ORG_DOMAINS = frozenset({
    "europa.eu", "mdpi.com", "springer.com", "sciencedirect.com", "acm.org", "arxiv.org",
    "studylib.net", "exa.ai", "medium.com", "substack.com", "github.io", "blogspot.com",
})
# A platform host that puts every author at one host, not one subdomain (unlike substack.com):
# group by host + first path segment, e.g. "medium.com/@jane" != "medium.com/@joe".
_AUTHOR_PATH_DOMAINS = frozenset({"medium.com"})


def domain_grouping_key(url: str) -> str:
    """The independence union-find's "same domain" key (A7). The registrable domain, except for
    `_MULTI_ORG_DOMAINS`, where it is the full host, or (medium.com) the host plus author path."""
    domain = registrable_domain(url)
    if domain not in _MULTI_ORG_DOMAINS:
        return domain
    parts = urlsplit(url)
    host = parts.netloc.rsplit("@", 1)[-1].split(":", 1)[0].casefold()
    if domain not in _AUTHOR_PATH_DOMAINS:
        return host
    segment = parts.path.strip("/").split("/", 1)[0]
    return f"{host}/{segment}" if segment else host


@dataclass(frozen=True)
class IndependenceResult:
    key_by_source: Mapping[str, str]
    reason_by_source: Mapping[str, str]


def independence_clusters(docs: Sequence[IndependenceDoc]) -> IndependenceResult:
    """Union-find over fetched docs (A7): same domain-grouping key (`domain_grouping_key`, SHOULD
    5b), or 5-shingle containment >= 0.5. The old third rule — a shared >=25-word verbatim run —
    no longer unions whole documents (SHOULD 5a, runner (b) finding 2: it merged 11 documents that
    only shared one quoted passage). A verbatim-shared *span* still matters, but only for
    corroboration counting, through `span_duplicates` below, not for document clustering."""
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

    domains = {d.source_id: domain_grouping_key(d.url) for d in docs}
    shingle_sets = {d.source_id: _shingles(d.text) for d in docs}

    for i, a in enumerate(docs):
        for b in docs[i + 1:]:
            if domains[a.source_id] == domains[b.source_id]:
                union(a.source_id, b.source_id, "same domain-grouping key")
            elif _containment(shingle_sets[a.source_id], shingle_sets[b.source_id]) >= 0.5:
                union(a.source_id, b.source_id, "5-shingle containment >= 0.5")

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


def span_duplicates(spans: Sequence[tuple[str, str, str]], min_words: int = 25) -> dict[str, str]:
    """SHOULD 5a: a span-level replacement for the old whole-document shared-run rule. `spans`:
    (span_id, independence_key, span_exact_text) tuples, one per located Evidence. Two spans from
    DIFFERENT independence clusters that share a run of >= `min_words` words are the same quoted
    passage (e.g. two regulators both quoting GDPR Art. 35 verbatim) — a corroboration count
    should credit that passage once, not once per document that happens to quote it. Returns
    {span_id: canonical_span_id}: every span maps to itself unless it duplicates an
    earlier-clustered span, in which case it maps to that group's smallest span_id."""
    parent = {sid: sid for sid, _, _ in spans}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: str, y: str) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            hi, lo = max(rx, ry), min(rx, ry)
            parent[hi] = lo

    for i, (sid_a, key_a, text_a) in enumerate(spans):
        words_a = text_a.split(" ")
        for sid_b, key_b, text_b in spans[i + 1:]:
            if key_a == key_b:
                continue
            words_b = text_b.split(" ")
            sm = difflib.SequenceMatcher(None, words_a, words_b, autojunk=False)
            if any(block.size >= min_words for block in sm.get_matching_blocks()):
                union(sid_a, sid_b)

    return {sid: find(sid) for sid, _, _ in spans}


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


def build_contradiction(claim_a: str, claim_b: str, *, detected_by: Agent, method: str) -> Contradiction:
    """`method` is a caller-formatted, self-describing string (e.g. "cross-verify:<spec sha256>",
    SHOULD 2) — this builder no longer assumes one particular detection method."""
    return Contradiction(claims=(claim_a, claim_b), detected_by=detected_by, method=method)


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


def merge_extractions(extractions: Sequence[Extraction]) -> list[MergedAssertion]:
    """Identical (casefold-equal) assertions merge into one record. The merged record's area,
    knowledge_type and question are taken from the member with the smallest source_id — first-
    seen, deterministic, no majority vote or tie-break machinery (REMOVE: `_majority` fired on
    0 of 629 extractions across both E-LIVE domains). Any disagreement among members is still
    recorded on `conflict`, whether or not it happens to be a tie."""
    groups: dict[str, list[Extraction]] = {}
    for e in extractions:
        groups.setdefault(e.assertion.casefold(), []).append(e)
    merged = []
    for key in sorted(groups):
        members = tuple(sorted(groups[key], key=lambda e: e.extraction_id))
        primary = min(members, key=lambda e: e.source_id)
        area_names = sorted({m.area_name for m in members})
        kt_values = sorted({m.knowledge_type.value for m in members})
        parts = []
        if len(area_names) > 1:
            parts.append(f"area disagreement: {', '.join(area_names)} (kept {primary.area_name!r})")
        if len(kt_values) > 1:
            parts.append(f"knowledge_type disagreement: {', '.join(kt_values)} "
                         f"(kept {primary.knowledge_type.value!r})")
        merged.append(MergedAssertion(assertion=members[0].assertion, area_name=primary.area_name,
                                       knowledge_type=primary.knowledge_type,
                                       question=primary.question, members=members,
                                       conflict="; ".join(parts) or None))
    return merged


def build_claim(merged: MergedAssertion, *, evidence: tuple[Evidence, ...],
                generation: Generation | None, searches: tuple[Search, ...], scope: Scope) -> ClaimRecord:
    return ClaimRecord(assertion=merged.assertion, question=merged.question,
                        layer=layer_for_question(merged.question), knowledge_type=merged.knowledge_type,
                        scope=scope, evidence=evidence, generation=generation, searches=searches)


# --- slot status (A2, SHOULD 3) ----------------------------------------------------------------

def slot_status(*, n_criterion_clusters: int, docs_fetched_and_extracted: bool,
                 area_lost_to_truncation: bool, verifier_ran_on_all_located: bool) -> str:
    """`n_criterion_clusters` is the number of distinct independence clusters contributing
    supporting evidence (any CRITERION_LABELS-worthy claim) to this slot. covered needs >= 2
    clusters; exactly one is `thin` — a real finding (single-source support), never folded into
    UNKNOWN or silently treated the same as 2+ clusters (SHOULD 3)."""
    if n_criterion_clusters >= 2:
        return "covered"
    if n_criterion_clusters == 1:
        return "thin"
    if docs_fetched_and_extracted and not area_lost_to_truncation and verifier_ran_on_all_located:
        return "unknown"
    if docs_fetched_and_extracted:
        return "unverified"
    return "unexamined"


# --- decoys (A6, MUST-FIX 4) -------------------------------------------------------------------

DECOY_MUTATIONS: tuple[str, ...] = ("number", "negation", "scope")
"""Target 10 decoys per type (cap 30 total), not one pooled sample capped at 20: the E-LIVE
review found the pooled 20-cap protocol under-measured every mutation type at once (5/5 scope,
1/13 negation, 1/2 number)."""

DECOYS_PER_TYPE = 10


def select_decoy_sample(claim_ids: Sequence[str], *, per_type: int = DECOYS_PER_TYPE
                         ) -> dict[str, list[str]]:
    """Deterministically partitions claim ids across the three mutation types, round-robin over
    the sorted id list, each type capped at `per_type` (10) and never exceeding what is
    available — "10 per type where enough located claims exist"."""
    ids = sorted(set(claim_ids))
    out: dict[str, list[str]] = {m: [] for m in DECOY_MUTATIONS}
    for i, cid in enumerate(ids):
        mutation = DECOY_MUTATIONS[i % len(DECOY_MUTATIONS)]
        if len(out[mutation]) < per_type:
            out[mutation].append(cid)
        if all(len(v) >= per_type for v in out.values()):
            break
    return out


def decoy_is_valid(original_assertion: str, mutated_claim: str, rationale: str) -> bool:
    """A6's validity check: the mutated claim must actually differ from the original, and the
    decoy prompt must return a one-line rationale for why the span no longer entails it. An
    invalid decoy is excluded from the false-accept rate but still counted (run.py records it)."""
    return (bool(rationale.strip())
            and mutated_claim.strip().casefold() != original_assertion.strip().casefold())


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for k successes out of n trials (report.py's per-type decoy rates)."""
    if n <= 0:
        return (0.0, 0.0)
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    spread = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    lo = (centre - spread) / denom
    hi = (centre + spread) / denom
    return (max(0.0, lo), min(1.0, hi))


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


# --- spec hashing --------------------------------------------------------------------------

def spec_sha256(prompt_text: str, schema: dict) -> str:
    return hashlib.sha256((prompt_text + json.dumps(schema, sort_keys=True)).encode()).hexdigest()
