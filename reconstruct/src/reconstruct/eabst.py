"""E-ABST harness (N2 pre-registration, `docs/n2-eplant-eabst-protocol.md`, E-ABST section;
binding). Five sealed-until-ready stages, run as CLI subcommands:

  exposure    -- pre-run public-exposure + repo-visibility check
  baseline    -- raw Haiku baseline per item (no tools)
  run         -- pipeline run per item (planner skipped; software-written areas file)
  code-sheet  -- deterministic coding frame + CSVs, mechanical exclusions applied
  score       -- after coding: hash-check the key, score, gate

Never constructs Evidence/Selector/Verification directly (reconstruct/tests/test_architecture.py
enforces this repo-wide): every one goes through reconstruct.evidence's builders. Source, Agent,
ClaimRecord, Ledger, Generation, Search and LocatedSpan are not restricted and are built here.

The private items live at `.private/e_abst/questions.json` (ids + questions; not sealed) and
`.private/e_abst/key.json` (answers; SEALED). This module's `score` functions are the only ones
that read key.json, and only after `check_registered_hashes` passes; nothing here ever prints a
key value, and no key content is written into a path this repo would commit (`.private/` is
git-ignored in full).

**key.json schema** *(this module's own design, undocumented elsewhere; mirrors eplant.py's
"our choice" file shapes)*: `{"commit": str, "items": [{"id": str, "answer": str,
"accept": [str, ...], "evidence_file": str, "evidence_quote": str}, ...]}`. `commit` is the
`.private/e_abst/informant-video` checkout's commit, shared by every item's gold source
citation; `accept` is the list of accept-variant strings `variant_match` checks candidates
against (§7 Scoring); `evidence_file`/`evidence_quote` locate the gold span `build_gold_claim`
verifies.

**accidental.json** (optional, `.private/e_abst/accidental.json`): `{"unit_ids": [str, ...]}`,
the owner's list of units coded "correct" that were guessed right without real support (§7
"Accidentally correct guesses count as correct ... and are reported separately"). `score_eabst`
only tallies these by arm for the report; it never changes a unit's `correct`/`false`/`abstain`
label, and refuses if a listed unit was not itself coded `correct`.

**score outputs.** `score` writes two files: `.private/e_abst/results.json` (sealed; per-item
raw/pipeline labels, exclusion reasons, the gate decision) and a PUBLIC
`research/n2/e_abst_results.json` + `.md` holding only aggregate counts, rates, the CI, kappa,
the audit miss rate and the `GateDecision` — no item id -> label map, no question or answer
text.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Callable, Literal, Mapping, Sequence

import httpx

from reconstruct import evidence
from reconstruct.eplant import provider_outage
from reconstruct.evidence import LocatedSpan, content_words, normalise
from reconstruct.llm import (
    Budget,
    BudgetExceeded,
    CallLog,
    LLMRefused,
    LLMUnavailable,
    Model,
    load_models,
    web_search,
)
from reconstruct.run import reconstruct
from residual.claims import ClaimRecord, Scope
from residual.gates import GateDecision, Measurement, Threshold, evidential_gate, measure
from residual.ledger import Ledger
from residual.provenance import Agent, Source
from residual.vocab import CRITERION_LABELS, EpistemicLabel, KnowledgeType, Layer, Question, SourceKind, Voice, World

REGISTRATION = "docs/n2-eplant-eabst-protocol.md#e-abst"

# --- registered constants (§7, §8) -----------------------------------------------------------

QUESTIONS_SHA256 = "19fe7e32d3162b0dd4d4f7114b59886cd0ac9fe4b142838f6d00e9a77b99f6a7"
KEY_SHA256 = "5629076e30e151d97e6449565cc103c6dcd5b17d8f696d33faca8b2cfd6b3ba1"

REPO = "AdamKrysztopa/informant-video"
EXPOSURE_TERMS: tuple[str, ...] = ("informant-video", "The Informant")
KNOWN_UNRELATED_HITS: tuple[str, ...] = (
    "github.com/AdamKrysztopa/edu_proj",  # edu_proj is public and names the repository
    "RyanPiao/econ-lectures",             # contains "informant-video" unrelated to the repo
)

PIPELINE_DOMAIN = "informant-video repository by AdamKrysztopa"
PIPELINE_BLOCKLIST: tuple[str, ...] = ("github.com/AdamKrysztopa/",)
"""D5: `run.py`'s `_is_blocklisted` matches by plain substring (`p.casefold() in url.casefold()`,
or a host suffix) — a trailing `*` is never in a real URL, so the pre-D5 entry blocked nothing."""
PIPELINE_MAX_RESULTS = 3
PIPELINE_MAX_DOC_CHARS = 20_000
PIPELINE_PER_ITEM_MAX_USD = 0.25
BASELINE_ARM_MAX_USD = 0.20
OVERALL_CAP_USD = 6.00

FAR_MARGIN = Threshold(name="eabst.far_margin", value=0.20, registered_in=REGISTRATION)
MIN_INCLUDED = Threshold(name="eabst.n_included_min", value=20, registered_in=REGISTRATION)
KAPPA_MIN = Threshold(name="eabst.kappa_min", value=0.60, registered_in=REGISTRATION)
ZERO_EXTRACTION_MAX = Threshold(name="eabst.zero_extraction_max", value=4, registered_in=REGISTRATION)

BASELINE_PROMPT = "Answer the question concisely."
BASELINE_SCHEMA = {
    "type": "object",
    "properties": {"answer": {"type": ["string", "null"]}},
    "required": ["answer"], "additionalProperties": False,
}

_DISQUALIFYING_TERMS = ("informant-video", "the informant")


# --- items (questions.json; not sealed) -------------------------------------------------------

@dataclass(frozen=True)
class Item:
    id: str
    question: str


def load_items(path: str | Path) -> tuple[Item, ...]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(Item(id=it["id"], question=it["question"]) for it in data["items"])


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def check_registered_hashes(questions_path: str | Path, key_path: str | Path) -> None:
    """§7. Refuses (registers again) if either private item has drifted from its registered
    hash. Called before `score` reads either file."""
    got_q, got_k = sha256_file(questions_path), sha256_file(key_path)
    if got_q != QUESTIONS_SHA256:
        raise ValueError(f"questions.json sha256 {got_q} != registered {QUESTIONS_SHA256}; "
                          "the experiment must be registered again")
    if got_k != KEY_SHA256:
        raise ValueError(f"key.json sha256 {got_k} != registered {KEY_SHA256}; "
                          "the experiment must be registered again")


# --- exposure (§7 pre-run checks) --------------------------------------------------------------

@dataclass(frozen=True)
class TermResult:
    term: str
    hit: bool
    known_unrelated: tuple[str, ...] = ()
    unexplained_hits: tuple[str, ...] = ()


def _excuse(url: str, title: str) -> str | None:
    hay = f"{url} {title}".casefold()
    return next((pat for pat in KNOWN_UNRELATED_HITS if pat.casefold() in hay), None)


def check_term(model: Model, term: str, *, max_results: int = 5) -> TermResult:
    """One Exa search for `term` via reconstruct.llm.web_search with the planner model. A hit
    is any result not matched by a registered known-unrelated pattern."""
    result = web_search(model, term, max_results=max_results)
    unexplained, excused = [], []
    for h in result.hits:
        pat = _excuse(h.url, h.title)
        (excused if pat is not None else unexplained).append(
            f"{h.url} (known-unrelated: {pat})" if pat is not None else h.url)
    return TermResult(term=term, hit=bool(unexplained), known_unrelated=tuple(excused),
                       unexplained_hits=tuple(unexplained))


def _default_gh_runner(args: list[str]) -> str:
    return subprocess.run(["gh", *args], capture_output=True, text=True, check=True).stdout


@dataclass(frozen=True)
class RepoCheck:
    visibility: str | None
    fork_count: int | None
    ok: bool
    error: str | None = None


def check_repo_private(repo: str = REPO, *,
                        runner: Callable[[list[str]], str] = _default_gh_runner) -> RepoCheck:
    """`gh repo view <repo> --json visibility,forkCount`: private, with no public fork."""
    try:
        data = json.loads(runner(["repo", "view", repo, "--json", "visibility,forkCount"]))
    except Exception as e:  # gh missing, not authenticated, network down, bad JSON
        return RepoCheck(visibility=None, fork_count=None, ok=False, error=repr(e))
    visibility, fork_count = data.get("visibility"), data.get("forkCount")
    return RepoCheck(visibility=visibility, fork_count=fork_count,
                      ok=(visibility == "PRIVATE" and fork_count == 0))


@dataclass(frozen=True)
class ExposureReport:
    repo: RepoCheck
    terms: tuple[TermResult, ...]

    @property
    def passed(self) -> bool:
        return self.repo.ok and all(not t.hit for t in self.terms)


def run_exposure_check(model: Model, *, repo: str = REPO, extra_terms: Sequence[str] = (),
                        max_results: int = 5,
                        gh_runner: Callable[[list[str]], str] = _default_gh_runner) -> ExposureReport:
    """§7. `extra_terms` lets the owner add "each distinctive identifier in the key" by hand:
    this function never reads key.json (the key is sealed until `score`), so any identifier
    terms beyond the two registered ones must be supplied by the caller from outside this code.
    This is a real gap against the protocol text, reported to the caller (see the module docstring
    and the implementation report)."""
    repo_check = check_repo_private(repo, runner=gh_runner)
    terms = tuple(check_term(model, t, max_results=max_results) for t in (*EXPOSURE_TERMS, *extra_terms))
    return ExposureReport(repo=repo_check, terms=terms)


def write_exposure_report(report: ExposureReport, out: str | Path) -> None:
    payload = {
        "passed": report.passed,
        "repo": {"visibility": report.repo.visibility, "fork_count": report.repo.fork_count,
                 "ok": report.repo.ok, "error": report.repo.error},
        "terms": [{"term": t.term, "hit": t.hit, "known_unrelated": list(t.known_unrelated),
                   "unexplained_hits": list(t.unexplained_hits)} for t in report.terms],
    }
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, sort_keys=True, indent=1) + "\n", encoding="utf-8")


def term_print_lines(terms: Sequence[TermResult], *, n_registered: int) -> list[str]:
    """D6: §7 says the script "never displays the key" -- only the `n_registered` public,
    code-constant `EXPOSURE_TERMS` print their own text; every term after them came from
    `--terms-file` (identifiers derived from the sealed key), so it prints only its index."""
    lines = []
    for i, t in enumerate(terms):
        label = t.term if i < n_registered else f"term {i - n_registered + 1}"
        lines.append(f"{label}: {'HIT' if t.hit else 'NO-HIT'}")
    return lines


# --- run-status bookkeeping (both arms; "sealed until every unit has finished") ---------------

def _status_path(out_dir: Path) -> Path:
    return out_dir / "status.json"


def _read_status(out_dir: Path) -> dict:
    p = _status_path(out_dir)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def _write_status(out_dir: Path, item_id: str, arm: str, state: str) -> None:
    p = _status_path(out_dir)
    data = _read_status(out_dir)
    data.setdefault(item_id, {})[arm] = state
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, sort_keys=True, indent=1) + "\n", encoding="utf-8")


def units_finished(items: Sequence[Item], out_dir: Path) -> tuple[bool, list[str]]:
    """§8 / the protocol's general sealing rule: every unit (both arms, every item) must have a
    recorded terminal state before code-sheet may run."""
    status = _read_status(Path(out_dir))
    missing = []
    for item in items:
        st = status.get(item.id, {})
        if "baseline" not in st:
            missing.append(f"{item.id}: baseline not finished")
        if "pipeline" not in st:
            missing.append(f"{item.id}: pipeline not finished")
    return (not missing), missing


# --- budget bookkeeping across the whole experiment (§8) ---------------------------------------

def total_spent(out_dir: str | Path) -> float:
    total = 0.0
    for p in Path(out_dir).rglob("*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            total += json.loads(line).get("cost") or 0.0
    return total


def would_breach_cap(out_dir: str | Path, planned_usd: float, *, cap: float = OVERALL_CAP_USD) -> bool:
    return total_spent(out_dir) + planned_usd > cap


# --- baseline arm --------------------------------------------------------------------------

def run_baseline_item(model: Model, item: Item) -> dict:
    result = model.json("baseline", system=BASELINE_PROMPT, user=item.question, schema=BASELINE_SCHEMA)
    answer = result.get("answer")
    if answer is not None and not isinstance(answer, str):
        raise LLMUnavailable(f"baseline for {item.id}: answer was not string|null: {answer!r}")
    return {"item": item.id, "question": item.question, "answer": answer}


def run_baseline(items: Sequence[Item], model: Model, out_dir: str | Path) -> list[dict]:
    """One shared $0.20 budget (protocol §8) across the whole raw arm, carried by `model`'s own
    CallLog/Budget: a unit that hits it, or any other model failure, is recorded excluded and
    counted, never silently retried."""
    out_dir = Path(out_dir)
    results = []
    for item in items:
        result_path = out_dir / item.id / "baseline.json"
        if result_path.exists():
            results.append(json.loads(result_path.read_text(encoding="utf-8")))
            continue
        try:
            record = run_baseline_item(model, item)
        except BudgetExceeded as e:
            record = {"item": item.id, "excluded": True, "reason": f"baseline budget exceeded: {e}"}
        except (LLMUnavailable, LLMRefused) as e:
            record = {"item": item.id, "excluded": True, "reason": f"baseline call failed: {e}"}
        else:
            result_path.parent.mkdir(parents=True, exist_ok=True)
            result_path.write_text(json.dumps(record, sort_keys=True, indent=1) + "\n", encoding="utf-8")
        _write_status(out_dir, item.id, "baseline", "excluded" if record.get("excluded") else "ran")
        results.append(record)
    return results


# --- pipeline arm ---------------------------------------------------------------------------

def build_item_areas(item: Item) -> dict:
    """One area named after the question, whose only query is the question verbatim (orchestrator
    amendment, cost): skips the planner entirely."""
    return {"areas": [{"name": item.question, "queries": [item.question]}]}


def write_item_areas(item: Item, path: str | Path) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_item_areas(item), sort_keys=True, indent=1) + "\n", encoding="utf-8")
    return path


def run_pipeline_item(item: Item, *, models_path: str | Path, item_dir: Path, http: httpx.Client,
                       today: date, max_results: int = PIPELINE_MAX_RESULTS,
                       max_doc_chars: int = PIPELINE_MAX_DOC_CHARS,
                       per_item_usd: float = PIPELINE_PER_ITEM_MAX_USD,
                       blocklist: Sequence[str] = PIPELINE_BLOCKLIST,
                       env: Mapping[str, str] = None) -> Path:
    areas_path = write_item_areas(item, item_dir.parent / "areas_in.json")
    log = CallLog(item_dir / "calls.jsonl", budget=Budget(max_usd=per_item_usd))
    models = load_models(models_path, log=log, env=env if env is not None else os.environ)
    return reconstruct(PIPELINE_DOMAIN, item.question, models=models, http=http, out=item_dir,
                        today=today, areas=areas_path, blocklist=blocklist,
                        max_results=max_results, max_doc_chars=max_doc_chars)


def run_pipeline_all(items: Sequence[Item], *, models_path: str | Path, out_dir: str | Path,
                      http: httpx.Client, today: date, overall_cap: float = OVERALL_CAP_USD,
                      per_item_usd: float = PIPELINE_PER_ITEM_MAX_USD,
                      max_results: int = PIPELINE_MAX_RESULTS, max_doc_chars: int = PIPELINE_MAX_DOC_CHARS,
                      blocklist: Sequence[str] = PIPELINE_BLOCKLIST,
                      env: Mapping[str, str] = None) -> list[dict]:
    """Skip-start rule (§8): no item starts if its budget could breach the overall cap, tracked
    against every calls.jsonl already written under `out_dir` (both arms, this and prior CLI
    invocations). A skipped item never starts, and is excluded and counted."""
    out_dir = Path(out_dir)
    results = []
    for item in items:
        item_dir = out_dir / item.id / "pipeline"
        if (item_dir / "ledger.json").exists():
            results.append({"item": item.id, "status": "already-run"})
            continue
        if would_breach_cap(out_dir, per_item_usd, cap=overall_cap):
            results.append({"item": item.id, "status": "skipped", "reason": "would breach the overall cap"})
            _write_status(out_dir, item.id, "pipeline", "skipped")
            continue
        run_pipeline_item(item, models_path=models_path, item_dir=item_dir, http=http, today=today,
                           max_results=max_results, max_doc_chars=max_doc_chars,
                           per_item_usd=per_item_usd, blocklist=blocklist, env=env)
        results.append({"item": item.id, "status": "ran", "run_dir": str(item_dir)})
        _write_status(out_dir, item.id, "pipeline", "ran")
    return results


# --- mechanical exclusion (§7, before unsealing) ------------------------------------------------

def _snapshot_text(pipeline_dir: Path, locator: str | None) -> str:
    m = re.match(r"^sha256:([0-9a-f]{64});char=\d+,\d+$", locator or "")
    if not m:
        return ""
    p = pipeline_dir / "snapshots" / f"{m.group(1)}.txt"
    return p.read_text(encoding="utf-8") if p.exists() else ""


def mechanical_exclusion_reasons(pipeline_dir: Path) -> list[str]:
    """An item is removed from both arms when a criterion-labelled claim in its pipeline ledger
    is evidenced by a source under github.com/AdamKrysztopa/, or whose snapshot text contains
    "informant-video" or "The Informant" (casefolded)."""
    ledger_path = pipeline_dir / "ledger.json"
    if not ledger_path.exists():
        return []
    ledger = Ledger.from_json(ledger_path.read_text(encoding="utf-8"))
    reasons: list[str] = []
    checked: set[str] = set()
    for claim in ledger.claims:
        if ledger.label(claim.claim_id) not in CRITERION_LABELS:
            continue
        for ev in claim.evidence:
            src = ev.source
            if src.source_id in checked:
                continue
            checked.add(src.source_id)
            if "github.com/adamkrysztopa/" in src.identifier.casefold():
                reasons.append(f"source under github.com/AdamKrysztopa/: {src.identifier}")
                continue
            hay = _snapshot_text(pipeline_dir, ev.selector.locator).casefold()
            if any(term in hay for term in _DISQUALIFYING_TERMS):
                reasons.append(f"snapshot text mentions a disqualifying term: {src.identifier}")
    return reasons


# --- coding frame (§7 "Coding", before unsealing) -----------------------------------------------

def _rng_seed(purpose: str) -> int:
    """A documented, reproducible seed (the protocol registers "seeded" sampling but not a seed
    value; this derives one deterministically from a fixed string per purpose, logged in
    coding_meta.json, rather than an unregistered magic number)."""
    return int(hashlib.sha256(f"e-abst:{purpose}".encode()).hexdigest()[:8], 16)


def overlaps_question(question: str, assertion: str) -> bool:
    return bool(content_words(question) & content_words(assertion))


@dataclass(frozen=True)
class Unit:
    unit_id: str
    item_id: str
    arm: Literal["pipeline", "raw"]
    label: Literal["criterion", "synthetic"] | None
    """None for the raw arm; "criterion" or "synthetic" for a pipeline claim (§7 sensitivity)."""
    question: str
    statement: str
    claim_id: str | None
    is_audit: bool
    in_second_coder_subset: bool = False


@dataclass(frozen=True)
class Frame:
    units: tuple[Unit, ...]
    excluded_items: dict[str, list[str]]
    seeds: dict[str, int]


def build_frame(items: Sequence[Item], out_dir: Path) -> Frame:
    out_dir = Path(out_dir)
    excluded: dict[str, list[str]] = {}
    pipeline_candidates: list[tuple[Item, ClaimRecord, Literal["criterion", "synthetic"], bool]] = []
    raw_units: list[Unit] = []

    for item in items:
        pipeline_dir = out_dir / item.id / "pipeline"
        reasons = mechanical_exclusion_reasons(pipeline_dir)
        if provider_outage(pipeline_dir):
            # D3/§8: a provider-outage unit is not scored as a result -- excluded and counted,
            # same as a mechanically-contaminated item.
            reasons = [*reasons, "provider outage (protocol §8): excluded and counted; rerun before scoring"]
        if reasons:
            excluded[item.id] = reasons
            continue

        baseline_path = out_dir / item.id / "baseline.json"
        if baseline_path.exists():
            b = json.loads(baseline_path.read_text(encoding="utf-8"))
            if b.get("answer"):
                raw_units.append(Unit(unit_id="", item_id=item.id, arm="raw", label=None,
                                       question=item.question, statement=b["answer"],
                                       claim_id=None, is_audit=False))

        ledger_path = pipeline_dir / "ledger.json"
        if not ledger_path.exists():
            continue
        ledger = Ledger.from_json(ledger_path.read_text(encoding="utf-8"))
        for claim in ledger.claims:
            label = ledger.label(claim.claim_id)
            if label in CRITERION_LABELS:
                kind: Literal["criterion", "synthetic"] = "criterion"
            elif label is EpistemicLabel.SYNTHETIC_EXTRAPOLATION:
                kind = "synthetic"
            else:
                continue
            overlap = overlaps_question(item.question, claim.assertion)
            pipeline_candidates.append((item, claim, kind, overlap))

    overlap_units = [Unit(unit_id="", item_id=it.id, arm="pipeline", label=kind, question=it.question,
                           statement=c.assertion, claim_id=c.claim_id, is_audit=False)
                      for it, c, kind, ov in pipeline_candidates if ov]
    zero_overlap_criterion = [(it, c) for it, c, kind, ov in pipeline_candidates
                               if not ov and kind == "criterion"]

    audit_rng_seed = _rng_seed("audit")
    audit_n = math.ceil(0.10 * len(zero_overlap_criterion))
    audit_sample = _seeded_sample(zero_overlap_criterion, audit_n, audit_rng_seed)
    audit_units = [Unit(unit_id="", item_id=it.id, arm="pipeline", label="criterion", question=it.question,
                         statement=c.assertion, claim_id=c.claim_id, is_audit=True)
                   for it, c in audit_sample]

    pipeline_units = overlap_units + audit_units
    second_rng_seed = _rng_seed("second-coder")
    second_n = math.ceil(0.20 * len(pipeline_units))
    second_sample_ids = {id(u) for u in _seeded_sample(pipeline_units, second_n, second_rng_seed)}
    pipeline_units = [u if id(u) not in second_sample_ids else
                       Unit(**{**u.__dict__, "in_second_coder_subset": True})
                       for u in pipeline_units]
    raw_units = [Unit(**{**u.__dict__, "in_second_coder_subset": True}) for u in raw_units]

    all_units = raw_units + pipeline_units
    shuffle_seed = _rng_seed("shuffle")
    shuffled = _seeded_sample(all_units, len(all_units), shuffle_seed)
    numbered = [Unit(**{**u.__dict__, "unit_id": f"u{i + 1:03d}"}) for i, u in enumerate(shuffled)]

    seeds = {"audit": audit_rng_seed, "second_coder": second_rng_seed, "shuffle": shuffle_seed}
    return Frame(units=tuple(numbered), excluded_items=excluded, seeds=seeds)


def _seeded_sample(population: Sequence, k: int, seed: int) -> list:
    """A Fisher-Yates-derived deterministic sample, seed-only (no dependence on the interpreter's
    `random` module state or its algorithm version, so a re-run reproduces the same sample)."""
    items = list(population)
    k = max(0, min(k, len(items)))
    state = seed & 0xFFFFFFFF
    for i in range(len(items) - 1, 0, -1):
        state = (state * 1103515245 + 12345) & 0xFFFFFFFF
        j = state % (i + 1)
        items[i], items[j] = items[j], items[i]
    return items[:k]


CODING_COLUMNS = ("unit_id", "question", "statement", "answers", "candidates", "notes")


def write_coding_csv(units: Sequence[Unit], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CODING_COLUMNS)
        w.writeheader()
        for u in units:
            w.writerow({"unit_id": u.unit_id, "question": u.question, "statement": u.statement,
                        "answers": "", "candidates": "", "notes": ""})


def write_coding_map(frame: Frame, path: Path) -> None:
    payload = {
        "units": {u.unit_id: {"item_id": u.item_id, "arm": u.arm, "label": u.label,
                               "claim_id": u.claim_id, "is_audit": u.is_audit,
                               "in_second_coder_subset": u.in_second_coder_subset}
                   for u in frame.units},
        "excluded_items": frame.excluded_items,
        "seeds": frame.seeds,
        "generated_at": datetime.now(UTC).isoformat(),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, sort_keys=True, indent=1) + "\n", encoding="utf-8")


def write_code_sheet_files(items: Sequence[Item], out_dir: Path, *, coding_sheet_path: Path,
                           coding_map_path: Path, second_coder_path: Path) -> Frame:
    finished, missing = units_finished(items, out_dir)
    if not finished:
        raise ValueError("run directories are sealed until every unit has finished: " + "; ".join(missing))
    frame = build_frame(items, out_dir)
    write_coding_csv(frame.units, coding_sheet_path)
    write_coding_map(frame, coding_map_path)
    second_units = [u for u in frame.units if u.arm == "raw" or u.in_second_coder_subset]
    write_coding_csv(second_units, second_coder_path)
    return frame


# --- scoring (§7 "Scoring", after unsealing and a hash check) -----------------------------------

def _norm(s: str) -> str:
    return normalise(s).casefold()


def variant_match(candidate: str, accept_variants: Sequence[str]) -> bool:
    hay = _norm(candidate)
    for v in accept_variants:
        needle = _norm(v)
        if needle and re.search(r"(?<!\w)" + re.escape(needle) + r"(?!\w)", hay):
            return True
    return False


UnitLabel = Literal["correct", "false", "abstain"]


def classify_unit(answers: bool, candidates: Sequence[str], accept_variants: Sequence[str]) -> UnitLabel:
    if not answers:
        return "abstain"
    if candidates and all(variant_match(c, accept_variants) for c in candidates):
        return "correct"
    return "false"


def classify_item_arm(unit_labels: Sequence[UnitLabel]) -> UnitLabel:
    """§7 Scoring: correct needs >=1 answering statement with every candidate accepted; false if
    any candidate anywhere is not accepted; abstain if there is no answering statement at all."""
    if not unit_labels or all(l == "abstain" for l in unit_labels):
        return "abstain"
    if any(l == "false" for l in unit_labels):
        return "false"
    return "correct"


@dataclass(frozen=True)
class CodedUnit:
    unit_id: str
    answers: bool
    candidates: tuple[str, ...]


def read_coded_csv(path: Path) -> dict[str, CodedUnit]:
    out = {}
    with Path(path).open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            answers = (row.get("answers") or "").strip().casefold() in ("y", "yes", "true", "1")
            raw = (row.get("candidates") or "").strip()
            candidates = tuple(c.strip() for c in raw.split(",") if c.strip()) if raw else ()
            out[row["unit_id"]] = CodedUnit(unit_id=row["unit_id"], answers=answers, candidates=candidates)
    return out


# --- key.json / accidental.json (§7 Scoring, sealed inputs) -------------------------------------

def load_key(path: str | Path) -> tuple[str, dict[str, dict]]:
    """Returns (commit, {item_id: key-item}). Only called after `check_registered_hashes`; never
    logs or returns anything beyond what the caller explicitly asks of the parsed structure."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return data["commit"], {it["id"]: it for it in data["items"]}


def load_accidental(path: str | Path) -> frozenset[str]:
    p = Path(path)
    if not p.exists():
        return frozenset()
    data = json.loads(p.read_text(encoding="utf-8"))
    return frozenset(data.get("unit_ids", ()))


def unit_labels_all(coding_map: Mapping, coded: Mapping[str, CodedUnit],
                     accept_by_item: Mapping[str, Sequence[str]]) -> dict[str, UnitLabel]:
    """Owner or second-coder labels for every unit *present in `coded`* (a second-coder CSV only
    ever holds its own subset, per `write_code_sheet_files`)."""
    out = {}
    for unit_id, meta in coding_map["units"].items():
        c = coded.get(unit_id)
        if c is None:
            continue
        out[unit_id] = classify_unit(c.answers, c.candidates, accept_by_item.get(meta["item_id"], ()))
    return out


def item_arm_labels(items: Sequence[Item], coding_map: Mapping, labels: Mapping[str, UnitLabel],
                     excluded_ids: set[str], *, include_synthetic: bool = False
                     ) -> dict[str, dict[str, UnitLabel]]:
    """§7 Scoring, per included item and arm: `classify_item_arm` over that item+arm's non-audit
    units. An item with no units in an arm (the baseline abstained, or nothing pipeline-side
    overlapped or was audited) has no statement in that arm, i.e. abstain.

    D1: §7 says synthetic claims (and, generally, anything not criterion-labelled) "are not
    answers" for the registered FAR — a unit whose `meta["label"]` is `"synthetic"` (or any label
    other than `None`/`"criterion"`) is skipped here by default. Pass `include_synthetic=True` to
    get the separate, explicitly non-gating "synthetic-counted" sensitivity FAR instead."""
    per_item: dict[str, dict[str, list[UnitLabel]]] = {}
    for unit_id, meta in coding_map["units"].items():
        if meta.get("is_audit") or unit_id not in labels:
            continue
        if not include_synthetic and meta.get("label") not in (None, "criterion"):
            continue
        per_item.setdefault(meta["item_id"], {}).setdefault(meta["arm"], []).append(labels[unit_id])
    out: dict[str, dict[str, UnitLabel]] = {}
    for item in items:
        if item.id in excluded_ids:
            continue
        arms = per_item.get(item.id, {})
        out[item.id] = {"raw": classify_item_arm(arms.get("raw", ())),
                        "pipeline": classify_item_arm(arms.get("pipeline", ()))}
    return out


def audit_miss_rate(coding_map: Mapping, labels: Mapping[str, UnitLabel]) -> tuple[int, int]:
    """§7: "the miss rate is the answering share of the audit" — a diagnostic on the zero-overlap
    sample, not part of any item's scored label. Returns (answering, total audited)."""
    audit_ids = [uid for uid, meta in coding_map["units"].items() if meta.get("is_audit")]
    coded_audit = [uid for uid in audit_ids if uid in labels]
    answering = sum(1 for uid in coded_audit if labels[uid] != "abstain")
    return answering, len(coded_audit)


def accidental_correct_counts(coding_map: Mapping, labels: Mapping[str, UnitLabel],
                               accidental_ids: frozenset[str]) -> dict[str, int]:
    """§7: "Accidentally correct guesses count as correct in both arms and are reported
    separately." Refuses a flagged unit the owner did not in fact code `correct` — the override
    reports, it never manufactures, a correct label."""
    counts = {"raw": 0, "pipeline": 0}
    for unit_id in accidental_ids:
        meta = coding_map["units"].get(unit_id)
        if meta is None:
            raise ValueError(f"accidental.json names unit {unit_id!r}, not in coding_map.json")
        if labels.get(unit_id) != "correct":
            raise ValueError(f"accidental.json names unit {unit_id!r}, coded {labels.get(unit_id)!r} "
                              "(not correct)")
        counts[meta["arm"]] += 1
    return counts


def far_counts(item_labels: Mapping[str, Mapping[str, UnitLabel]], arm: str) -> tuple[int, int]:
    values = list(item_labels.values())
    false_n = sum(1 for v in values if v[arm] == "false")
    return false_n, len(values)


def paired_false_counts(item_labels: Mapping[str, Mapping[str, UnitLabel]]) -> tuple[int, int, int, int]:
    """(n11, n10, n01, n00) of (raw false, pipeline false), for `paired_newcombe_ci`."""
    n11 = n10 = n01 = n00 = 0
    for v in item_labels.values():
        raw_false, pipe_false = v["raw"] == "false", v["pipeline"] == "false"
        if raw_false and pipe_false:
            n11 += 1
        elif raw_false:
            n10 += 1
        elif pipe_false:
            n01 += 1
        else:
            n00 += 1
    return n11, n10, n01, n00


def count_zero_extraction_or_capped(items: Sequence[Item], out_dir: str | Path) -> int:
    out_dir = Path(out_dir)
    return sum(1 for item in items if is_zero_extraction_or_capped(out_dir / item.id / "pipeline"))


# --- reliability -------------------------------------------------------------------------------

def cohens_kappa(labels_a: Sequence[str], labels_b: Sequence[str]) -> float:
    n = len(labels_a)
    if n == 0 or n != len(labels_b):
        raise ValueError("kappa needs two equal-length, non-empty label sequences")
    categories = sorted(set(labels_a) | set(labels_b))
    po = sum(1 for a, b in zip(labels_a, labels_b) if a == b) / n
    freq_a = {c: sum(1 for x in labels_a if x == c) / n for c in categories}
    freq_b = {c: sum(1 for x in labels_b if x == c) / n for c in categories}
    pe = sum(freq_a[c] * freq_b[c] for c in categories)
    if pe >= 1 - 1e-12:
        return 1.0 if po >= 1 - 1e-12 else 0.0
    return (po - pe) / (1 - pe)


def compute_kappa(coding_map: Mapping, owner_labels: Mapping[str, UnitLabel],
                   second_labels: Mapping[str, UnitLabel] | None) -> float | None:
    """§7 "Coders": the second coder codes all 24 raw-arm units plus 20% of pipeline units
    (`in_second_coder_subset`, set by `build_frame`). None with no second-coder CSV, or if it
    coded none of that subset; `decide()` treats a None kappa as inconclusive."""
    if second_labels is None:
        return None
    ids = [uid for uid, meta in coding_map["units"].items()
           if meta.get("in_second_coder_subset") and uid in second_labels and uid in owner_labels]
    if not ids:
        return None
    return cohens_kappa([owner_labels[uid] for uid in ids], [second_labels[uid] for uid in ids])


# --- paired Newcombe CI (descriptive only) ------------------------------------------------------

def wilson_ci(x: int, n: int, *, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return 0.0, 0.0
    p = x / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def paired_newcombe_ci(n11: int, n10: int, n01: int, n00: int, *, z: float = 1.96) -> tuple[float, float]:
    """Newcombe (1998) Method 10 for the difference between two proportions from paired binary
    data. n11/n10/n01/n00 are the 2x2 counts of (arm-1 false, arm-2 false). Descriptive only
    (§7): reported alongside the point-estimate FAR margin, never gating."""
    n = n11 + n10 + n01 + n00
    if n == 0:
        return 0.0, 0.0
    p1, p2 = (n11 + n10) / n, (n11 + n01) / n
    l1, u1 = wilson_ci(n11 + n10, n, z=z)
    l2, u2 = wilson_ci(n11 + n01, n, z=z)
    denom = math.sqrt(max((n11 + n10) * (n01 + n00) * (n11 + n01) * (n10 + n00), 0))
    phi = 0.0 if denom == 0 else (n11 * n00 - n10 * n01) / denom
    lower = (p1 - p2) - math.sqrt(max(0.0, p1 - l1) ** 2 - 2 * phi * max(0.0, p1 - l1) * max(0.0, u2 - p2)
                                  + max(0.0, u2 - p2) ** 2)
    upper = (p1 - p2) + math.sqrt(max(0.0, u1 - p1) ** 2 - 2 * phi * max(0.0, u1 - p1) * max(0.0, p2 - l2)
                                  + max(0.0, p2 - l2) ** 2)
    return lower, upper


# --- gold ledger G_abst (§7 Gate) ---------------------------------------------------------------

def _find_span(quote: str, text_normalised: str) -> LocatedSpan | None:
    """Like evidence.locate_span, but without its 6-80-word bound: a gold quote from a repo file
    may be shorter than an extracted claim's quote."""
    q = normalise(quote)
    idx = text_normalised.find(q)
    if idx == -1 or not q:
        return None
    exact = text_normalised[idx:idx + len(q)]
    return LocatedSpan(start=idx, end=idx + len(q), exact=exact,
                        injection_flagged=evidence.injection_flag(exact))


def build_gold_claim(*, item: Item, answer: str, evidence_file: str, evidence_quote: str,
                      repo_root: Path, commit: str, today: date) -> ClaimRecord:
    """One G_abst claim: organisation-scoped World B, evidenced by a repository file at `commit`,
    owner-verified SUPPORTS (Agent(kind="human", id="owner")). Built entirely through
    reconstruct.evidence's builders; Source is not construction-restricted (test_architecture.py)."""
    file_path = repo_root / evidence_file
    text = normalise(file_path.read_text(encoding="utf-8"))
    span = _find_span(evidence_quote, text)
    if span is None:
        raise ValueError(f"gold quote for {item.id} not found verbatim in {evidence_file}")
    text_sha256 = hashlib.sha256(text.encode()).hexdigest()
    source = Source(identifier=f"{REPO}@{commit}:{evidence_file}", kind=SourceKind.DOCUMENTATION,
                     world=World.B, voice=Voice.EXPERT, independence_key=f"ind-{REPO}@{commit}",
                     published=None, organisation="AdamKrysztopa", boundary=False)
    verifier = Agent(kind="human", id="owner")
    verification = evidence.build_verification("supports", verifier=verifier, on=today)
    ev = evidence.build_evidence(source=source, span=span, text_sha256=text_sha256, retrieved=today,
                                  verification=verification)
    scope = Scope(domain=PIPELINE_DOMAIN, task=item.question, organisation="AdamKrysztopa")
    return ClaimRecord(assertion=answer, question=Question.DOMAIN, layer=Layer.DOMAIN_STRUCTURE,
                        knowledge_type=KnowledgeType.CONCEPT, scope=scope, evidence=(ev,))


def build_gold_ledger(claims: Sequence[ClaimRecord]) -> Ledger:
    return Ledger(purpose="gold", claims=tuple(claims))


# --- gate (§7 Gate) ------------------------------------------------------------------------------

@evidential_gate
def e_abst_gate(*, far_raw: Measurement, far_pipe: Measurement, n_included: Measurement,
                 kappa: Measurement, zero_extraction_or_capped: Measurement,
                 margin: Threshold = FAR_MARGIN, min_included: Threshold = MIN_INCLUDED,
                 kappa_min: Threshold = KAPPA_MIN,
                 zero_extraction_max: Threshold = ZERO_EXTRACTION_MAX) -> GateDecision:
    if n_included.value < min_included.value:
        return GateDecision(gate="e_abst", outcome="inconclusive",
                             reason=f"n_included={n_included.value:.0f} < {min_included.value:.0f}")
    if kappa.value < kappa_min.value:
        return GateDecision(gate="e_abst", outcome="inconclusive",
                             reason=f"kappa={kappa.value:.3f} < {kappa_min.value}")
    if zero_extraction_or_capped.value > zero_extraction_max.value:
        return GateDecision(gate="e_abst", outcome="inconclusive",
                             reason=(f"{zero_extraction_or_capped.value:.0f} runs capped or "
                                     f"extracted zero documents (> {zero_extraction_max.value:.0f})"))
    diff = far_raw.value - far_pipe.value
    if far_pipe.value >= far_raw.value:
        return GateDecision(gate="e_abst", outcome="stop",
                             reason=f"FAR_pipe={far_pipe.value:.3f} >= FAR_raw={far_raw.value:.3f}")
    if diff >= margin.value:
        return GateDecision(gate="e_abst", outcome="continue",
                             reason=f"FAR margin {diff:.3f} >= {margin.value}")
    return GateDecision(gate="e_abst", outcome="change",
                         reason=f"FAR margin {diff:.3f} is between 0 and {margin.value}")


def decide(*, far_raw_value: float, far_pipe_value: float, n_included: int, kappa: float | None,
           zero_extraction_or_capped: int, gold_claims: Sequence[ClaimRecord],
           gold_ledger: Ledger) -> GateDecision:
    """Wraps e_abst_gate: a missing second coder (kappa is None) is decided inconclusive here,
    outside the gate decorator, because None cannot be passed through it (only Measurement,
    ClaimRecord, Ledger and Threshold carry evidence labels; a bare None is refused)."""
    if kappa is None:
        return GateDecision(gate="e_abst", outcome="inconclusive", reason="no second coder",
                             criterion_ids=tuple(c.claim_id for c in gold_claims))
    m_far_raw = measure("eabst.far.raw", far_raw_value, gold_claims, ledger=gold_ledger)
    m_far_pipe = measure("eabst.far.pipe", far_pipe_value, gold_claims, ledger=gold_ledger)
    m_n = measure("eabst.n_included", float(n_included), gold_claims, ledger=gold_ledger)
    m_kappa = measure("eabst.kappa", kappa, gold_claims, ledger=gold_ledger)
    m_zero = measure("eabst.zero_extraction_or_capped", float(zero_extraction_or_capped),
                      gold_claims, ledger=gold_ledger)
    return e_abst_gate(far_raw=m_far_raw, far_pipe=m_far_pipe, n_included=m_n, kappa=m_kappa,
                        zero_extraction_or_capped=m_zero)


# --- zero-extraction / capped counter (§7 Inconclusive) ------------------------------------------

def is_zero_extraction_or_capped(pipeline_dir: Path) -> bool:
    """D4: "extracted zero documents" counts sources whose extraction call actually succeeded
    (`sources[sid].extract_ok`), not merely fetched -- a run that fetched pages but extracted
    nothing from any of them (truncation, or a provider outage) must still count here."""
    sidecar_path = pipeline_dir / "sidecar.json"
    if not sidecar_path.exists():
        return True
    sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    if not sidecar.get("complete", True):
        return True
    sources = sidecar.get("sources", {})
    return sum(1 for s in sources.values() if s.get("extract_ok")) == 0


# --- score orchestration (§7 Scoring + Gate; sealed/public split, module docstring) --------------

def score_eabst(*, items: Sequence[Item], key_items: Mapping[str, dict], commit: str,
                 coding_map: Mapping, owner_coded: Mapping[str, CodedUnit],
                 second_coded: Mapping[str, CodedUnit] | None, accidental_ids: frozenset[str],
                 repo_root: str | Path, out_dir: str | Path, today: date) -> dict:
    """The `score` CLI's one entry point. Returns `{"sealed": ..., "public": ...}`: "sealed" holds
    per-item raw/pipeline labels (never question or answer text — those stay in questions.json
    and key.json); "public" holds only aggregate counts, rates and the gate decision, safe for
    `research/n2/`."""
    excluded_ids = set(coding_map.get("excluded_items", {}))
    accept_by_item = {iid: k.get("accept", ()) for iid, k in key_items.items()}

    owner_labels = unit_labels_all(coding_map, owner_coded, accept_by_item)
    second_labels = (unit_labels_all(coding_map, second_coded, accept_by_item)
                     if second_coded is not None else None)
    item_labels = item_arm_labels(items, coding_map, owner_labels, excluded_ids)
    # D1: the registered FAR excludes synthetic (and any non-criterion) pipeline units; this
    # second, non-gating reading reproduces the pre-D1 (biased) count as a reported sensitivity.
    item_labels_synthetic = item_arm_labels(items, coding_map, owner_labels, excluded_ids,
                                            include_synthetic=True)

    n_included = len(item_labels)
    false_raw, n_raw = far_counts(item_labels, "raw")
    false_pipe, n_pipe = far_counts(item_labels, "pipeline")
    far_raw_value = (false_raw / n_raw) if n_raw else 0.0
    far_pipe_value = (false_pipe / n_pipe) if n_pipe else 0.0
    false_pipe_syn, n_pipe_syn = far_counts(item_labels_synthetic, "pipeline")
    far_pipe_synthetic_value = (false_pipe_syn / n_pipe_syn) if n_pipe_syn else 0.0
    n11, n10, n01, n00 = paired_false_counts(item_labels)
    newcombe = paired_newcombe_ci(n11, n10, n01, n00)
    kappa = compute_kappa(coding_map, owner_labels, second_labels)
    miss_answering, miss_total = audit_miss_rate(coding_map, owner_labels)
    accidental = accidental_correct_counts(coding_map, owner_labels, accidental_ids)
    zero_or_capped = count_zero_extraction_or_capped(items, out_dir)

    gold_claims = []
    for item in items:
        if item.id not in item_labels:
            continue
        k = key_items.get(item.id)
        if k is None:
            raise ValueError(f"key.json has no entry for included item {item.id!r}")
        gold_claims.append(build_gold_claim(item=item, answer=k["answer"], evidence_file=k["evidence_file"],
                                            evidence_quote=k["evidence_quote"], repo_root=Path(repo_root),
                                            commit=commit, today=today))
    gold_ledger = build_gold_ledger(gold_claims)
    decision = decide(far_raw_value=far_raw_value, far_pipe_value=far_pipe_value, n_included=n_included,
                      kappa=kappa, zero_extraction_or_capped=zero_or_capped, gold_claims=gold_claims,
                      gold_ledger=gold_ledger)
    decision_json = decision.model_dump(mode="json")
    excluded_items = dict(coding_map.get("excluded_items", {}))

    sealed = {"item_labels": item_labels, "excluded_items": excluded_items, "decision": decision_json}
    public = {
        "n_included": n_included,
        "far_raw": {"false": false_raw, "n": n_raw, "rate": far_raw_value},
        "far_pipe": {"false": false_pipe, "n": n_pipe, "rate": far_pipe_value},
        "far_pipe_synthetic_counted": {"false": false_pipe_syn, "n": n_pipe_syn,
                                       "rate": far_pipe_synthetic_value},
        "paired_2x2": {"n11": n11, "n10": n10, "n01": n01, "n00": n00},
        "newcombe_ci": {"lower": newcombe[0], "upper": newcombe[1]},
        "kappa": kappa,
        "audit_miss_rate": {"answering": miss_answering, "total": miss_total,
                            "rate": (miss_answering / miss_total) if miss_total else None},
        "accidental_correct": accidental,
        "zero_extraction_or_capped": zero_or_capped,
        "excluded_items": excluded_items,
        "decision": decision_json,
    }
    return {"sealed": sealed, "public": public}


def render_eabst_markdown(public: Mapping) -> str:
    decision = public["decision"]
    far_raw, far_pipe, ci = public["far_raw"], public["far_pipe"], public["newcombe_ci"]
    miss, paired = public["audit_miss_rate"], public["paired_2x2"]
    kappa_row = (f"| kappa | {public['kappa']:.3f} |" if public["kappa"] is not None
                 else "| kappa | no second coder |")
    miss_rate = f" ({miss['rate']:.0%})" if miss["rate"] is not None else ""
    lines = [
        "## E-ABST\n",
        f"n_included = {public['n_included']} items.\n",
        "| metric | value |\n| --- | --- |",
        f"| FAR raw | {far_raw['false']}/{far_raw['n']} ({far_raw['rate']:.0%}) |",
        f"| FAR pipeline | {far_pipe['false']}/{far_pipe['n']} ({far_pipe['rate']:.0%}) |",
        f"| FAR pipeline (synthetic-counted, non-gating sensitivity) | "
        f"{public['far_pipe_synthetic_counted']['false']}/{public['far_pipe_synthetic_counted']['n']} "
        f"({public['far_pipe_synthetic_counted']['rate']:.0%}) |",
        f"| FAR margin (raw - pipe) | {far_raw['rate'] - far_pipe['rate']:.3f} |",
        f"| paired Newcombe 95% CI (descriptive) | {ci['lower']:.3f} to {ci['upper']:.3f} |",
        f"| paired 2x2 (raw-false, pipe-false) | n11={paired['n11']} n10={paired['n10']} "
        f"n01={paired['n01']} n00={paired['n00']} |",
        kappa_row,
        f"| audit miss rate | {miss['answering']}/{miss['total']}{miss_rate} |",
        f"| accidental-correct (raw / pipeline) | {public['accidental_correct']['raw']} / "
        f"{public['accidental_correct']['pipeline']} |",
        f"| zero-extraction-or-capped runs | {public['zero_extraction_or_capped']} |",
        "",
        f"**Gate decision: {decision['outcome'].upper()}** — {decision['reason']}",
        "",
    ]
    excluded = public.get("excluded_items") or {}
    if excluded:
        lines.append("Excluded items: " + "; ".join(f"{k} ({'; '.join(v)})" for k, v in excluded.items()))
    return "\n".join(lines) + "\n"


# --- CLI -----------------------------------------------------------------------------------------

def _models_json_path() -> Path:
    return Path(__file__).parent.parent.parent / "models.json"


def _cmd_exposure(args: argparse.Namespace) -> int:
    log = CallLog(Path(args.out).parent / "exposure_calls.jsonl")
    models = load_models(_models_json_path(), log=log, env=os.environ)
    extra_terms = Path(args.terms_file).read_text().splitlines() if args.terms_file else []
    extra_terms = [t.strip() for t in extra_terms if t.strip()]
    report = run_exposure_check(models["planner"], extra_terms=extra_terms, max_results=args.max_results)
    write_exposure_report(report, args.out)
    print(f"repo: {'PASS' if report.repo.ok else 'FAIL'}")
    for line in term_print_lines(report.terms, n_registered=len(EXPOSURE_TERMS)):
        print(line)
    print("PASSED" if report.passed else "FAILED (register again)")
    return 0 if report.passed else 1


def _cmd_baseline(args: argparse.Namespace) -> int:
    items = load_items(args.items)
    log = CallLog(Path(args.out) / "_baseline" / "calls.jsonl", budget=Budget(max_usd=BASELINE_ARM_MAX_USD))
    models = load_models(_models_json_path(), log=log, env=os.environ)
    results = run_baseline(items, models["baseline"], args.out)
    print(json.dumps(results, indent=1))
    return 0


def _cmd_run(args: argparse.Namespace) -> int:
    items = load_items(args.items)
    with httpx.Client() as http:
        results = run_pipeline_all(items, models_path=_models_json_path(), out_dir=args.out,
                                    http=http, today=datetime.now(UTC).date())
    print(json.dumps(results, indent=1))
    return 0


def _cmd_code_sheet(args: argparse.Namespace) -> int:
    items = load_items(args.items)
    out_dir = Path(args.out)
    frame = write_code_sheet_files(
        items, out_dir,
        coding_sheet_path=Path(args.coding_sheet),
        coding_map_path=Path(args.coding_map),
        second_coder_path=Path(args.second_coder))
    print(f"{len(frame.units)} units written; {len(frame.excluded_items)} item(s) excluded")
    return 0


def _cmd_score(args: argparse.Namespace) -> int:
    check_registered_hashes(args.questions, args.key)
    print("hash check: PASSED (scoring proceeds)")

    items = load_items(args.questions)
    commit, key_items = load_key(args.key)
    coding_map = json.loads(Path(args.coding_map).read_text(encoding="utf-8"))
    owner_coded = read_coded_csv(args.coding_sheet)
    second_path = Path(args.second_coder)
    second_coded = read_coded_csv(second_path) if second_path.exists() else None
    accidental_ids = load_accidental(args.accidental)

    result = score_eabst(items=items, key_items=key_items, commit=commit, coding_map=coding_map,
                         owner_coded=owner_coded, second_coded=second_coded,
                         accidental_ids=accidental_ids, repo_root=args.repo_root, out_dir=args.out,
                         today=datetime.now(UTC).date())

    sealed_path = Path(args.sealed_out)
    sealed_path.parent.mkdir(parents=True, exist_ok=True)
    sealed_path.write_text(json.dumps(result["sealed"], sort_keys=True, indent=1) + "\n", encoding="utf-8")

    public_path = Path(args.public_out)
    public_path.parent.mkdir(parents=True, exist_ok=True)
    public_path.write_text(json.dumps(result["public"], sort_keys=True, indent=1) + "\n", encoding="utf-8")
    public_path.with_suffix(".md").write_text(render_eabst_markdown(result["public"]), encoding="utf-8")

    decision = result["public"]["decision"]
    print(f"n_included={result['public']['n_included']}")
    print(f"decision: {decision['outcome'].upper()} — {decision['reason']}")
    print(sealed_path)
    print(public_path)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m reconstruct.eabst")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("exposure")
    p.add_argument("--out", default=".private/e_abst/exposure.json")
    p.add_argument("--terms-file")
    p.add_argument("--max-results", type=int, default=5)
    p.set_defaults(fn=_cmd_exposure)

    p = sub.add_parser("baseline")
    p.add_argument("--items", default=".private/e_abst/questions.json")
    p.add_argument("--out", default=".private/e_abst/runs")
    p.set_defaults(fn=_cmd_baseline)

    p = sub.add_parser("run")
    p.add_argument("--live", action="store_true")
    p.add_argument("--items", default=".private/e_abst/questions.json")
    p.add_argument("--out", default=".private/e_abst/runs")
    p.set_defaults(fn=_cmd_run)

    p = sub.add_parser("code-sheet")
    p.add_argument("--items", default=".private/e_abst/questions.json")
    p.add_argument("--out", default=".private/e_abst/runs")
    p.add_argument("--coding-sheet", default=".private/e_abst/coding_sheet.csv")
    p.add_argument("--coding-map", default=".private/e_abst/coding_map.json")
    p.add_argument("--second-coder", default=".private/e_abst/coding_sheet_second.csv")
    p.set_defaults(fn=_cmd_code_sheet)

    p = sub.add_parser("score")
    p.add_argument("--questions", default=".private/e_abst/questions.json")
    p.add_argument("--key", default=".private/e_abst/key.json")
    p.add_argument("--out", default=".private/e_abst/runs")
    p.add_argument("--coding-map", default=".private/e_abst/coding_map.json")
    p.add_argument("--coding-sheet", default=".private/e_abst/coding_sheet.csv")
    p.add_argument("--second-coder", default=".private/e_abst/coding_sheet_second.csv")
    p.add_argument("--accidental", default=".private/e_abst/accidental.json")
    p.add_argument("--repo-root", default=".private/e_abst/informant-video")
    p.add_argument("--sealed-out", default=".private/e_abst/results.json")
    p.add_argument("--public-out", default="research/n2/e_abst_results.json")
    p.set_defaults(fn=_cmd_score)

    args = parser.parse_args(argv)
    if args.cmd == "run" and not args.live:
        print("refusing to run without --live", file=sys.stderr)
        return 2
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
