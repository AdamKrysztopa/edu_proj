"""Offline tests for the E-ABST harness (reconstruct.eabst). Everything here uses a fake
3-item set (fixtures/eabst/) and a synthetic repo checkout — never the private items under
.private/e_abst/, and no live network or model call.
"""
from __future__ import annotations

import csv
import json
from datetime import date
from pathlib import Path
from typing import Mapping

import pytest
from e2e_support import ScriptedBackend, search_result

from reconstruct import eabst
from reconstruct.eabst import (
    CodedUnit,
    Item,
    RepoCheck,
    accidental_correct_counts,
    audit_miss_rate,
    build_frame,
    build_gold_claim,
    build_gold_ledger,
    build_item_areas,
    check_registered_hashes,
    check_repo_private,
    check_term,
    classify_item_arm,
    classify_unit,
    cohens_kappa,
    compute_kappa,
    count_zero_extraction_or_capped,
    decide,
    far_counts,
    is_zero_extraction_or_capped,
    item_arm_labels,
    load_accidental,
    load_key,
    mechanical_exclusion_reasons,
    overlaps_question,
    paired_false_counts,
    paired_newcombe_ci,
    render_eabst_markdown,
    run_baseline,
    run_baseline_item,
    score_eabst,
    total_spent,
    unit_labels_all,
    units_finished,
    variant_match,
    wilson_ci,
    would_breach_cap,
    write_code_sheet_files,
)
from reconstruct.llm import BudgetExceeded, Model
from reconstruct.run import reconstruct
from residual.claims import Scope
from residual.ledger import Ledger
from residual.provenance import Agent, Evidence, Generation, Search, Selector, Verification
from residual.vocab import EpistemicLabel, KnowledgeType, Layer, Question, SourceKind, Voice, World
from residual.claims import ClaimRecord

DAY = date(2026, 9, 28)
FIXTURES = Path(__file__).parent / "fixtures" / "eabst"

FAKE_ITEMS = (
    Item(id="q1", question="Where does the render pipeline write its output frames?"),
    Item(id="q2", question="What encoder does the deliver step call?"),
    Item(id="q3", question="Which config key sets the target frame rate?"),
)


def fake_model(role: str = "planner", family: str = "anthropic") -> tuple[Model, ScriptedBackend]:
    backend = ScriptedBackend(role=role, family=family)
    return Model(agent=Agent(kind="model", id=f"fake/{role}", family=family), backend=backend), backend


# --- hash check ------------------------------------------------------------------------------

def test_check_registered_hashes_passes_when_matching(tmp_path, monkeypatch):
    q = tmp_path / "questions.json"
    q.write_text('{"items": []}')
    k = tmp_path / "key.json"
    k.write_text('{"items": []}')
    monkeypatch.setattr(eabst, "QUESTIONS_SHA256", eabst.sha256_file(q))
    monkeypatch.setattr(eabst, "KEY_SHA256", eabst.sha256_file(k))
    check_registered_hashes(q, k)  # does not raise


def test_check_registered_hashes_refuses_on_drift(tmp_path, monkeypatch):
    q = tmp_path / "questions.json"
    q.write_text('{"items": []}')
    k = tmp_path / "key.json"
    k.write_text('{"items": []}')
    monkeypatch.setattr(eabst, "QUESTIONS_SHA256", eabst.sha256_file(q))
    monkeypatch.setattr(eabst, "KEY_SHA256", "0" * 64)
    with pytest.raises(ValueError, match="register.*again"):
        check_registered_hashes(q, k)


# --- exposure ---------------------------------------------------------------------------------

def test_check_term_no_hit_when_all_results_are_known_unrelated():
    model, backend = fake_model()
    backend.script_search("informant-video", search_result(
        "informant-video", [("https://github.com/AdamKrysztopa/edu_proj", "edu_proj"),
                             ("https://example.com/RyanPiao/econ-lectures", "econ-lectures")]))
    result = check_term(model, "informant-video")
    assert result.hit is False
    assert len(result.known_unrelated) == 2


def test_check_term_hit_on_an_unexplained_result():
    model, backend = fake_model()
    backend.script_search("informant-video", search_result(
        "informant-video", [("https://someblog.example/post", "a leak about informant-video")]))
    result = check_term(model, "informant-video")
    assert result.hit is True
    assert result.unexplained_hits == ("https://someblog.example/post",)


def test_check_repo_private_ok_when_private_and_no_fork():
    check = check_repo_private(runner=lambda args: json.dumps({"visibility": "PRIVATE", "forkCount": 0}))
    assert check == RepoCheck(visibility="PRIVATE", fork_count=0, ok=True)


@pytest.mark.parametrize("payload", [
    {"visibility": "PUBLIC", "forkCount": 0},
    {"visibility": "PRIVATE", "forkCount": 1},
])
def test_check_repo_private_fails_when_public_or_forked(payload):
    check = check_repo_private(runner=lambda args: json.dumps(payload))
    assert check.ok is False


def test_check_repo_private_records_the_error_when_gh_fails():
    def boom(args):
        raise RuntimeError("gh: not authenticated")
    check = check_repo_private(runner=boom)
    assert check.ok is False
    assert "not authenticated" in check.error


# --- baseline ---------------------------------------------------------------------------------

def test_run_baseline_item_returns_the_answer():
    model, backend = fake_model(role="baseline")
    backend.script("baseline", "", {"answer": "dist/frames"})
    record = run_baseline_item(model, FAKE_ITEMS[0])
    assert record == {"item": "q1", "question": FAKE_ITEMS[0].question, "answer": "dist/frames"}


def test_run_baseline_item_accepts_a_null_answer_as_abstention():
    model, backend = fake_model(role="baseline")
    backend.script("baseline", "", {"answer": None})
    record = run_baseline_item(model, FAKE_ITEMS[0])
    assert record["answer"] is None


def test_run_baseline_writes_one_file_per_item_and_marks_status(tmp_path):
    model, backend = fake_model(role="baseline")
    for item in FAKE_ITEMS:
        backend.script("baseline", item.question[:10], {"answer": f"answer for {item.id}"})
    results = run_baseline(FAKE_ITEMS, model, tmp_path)
    assert len(results) == 3
    for item in FAKE_ITEMS:
        assert (tmp_path / item.id / "baseline.json").exists()
    status = json.loads((tmp_path / "status.json").read_text())
    assert all(status[item.id]["baseline"] == "ran" for item in FAKE_ITEMS)


def test_run_baseline_records_budget_exhaustion_as_excluded(tmp_path):
    model, backend = fake_model(role="baseline")

    def blow_up(_task, _system, _user, _schema):
        raise BudgetExceeded("out of money")
    backend.complete_json = blow_up  # type: ignore[method-assign]
    results = run_baseline(FAKE_ITEMS, model, tmp_path)
    assert all(r["excluded"] for r in results)
    status = json.loads((tmp_path / "status.json").read_text())
    assert all(status[item.id]["baseline"] == "excluded" for item in FAKE_ITEMS)


def test_run_baseline_is_idempotent_and_does_not_recall_the_model(tmp_path):
    model, backend = fake_model(role="baseline")
    backend.script("baseline", "", {"answer": "x"})
    run_baseline(FAKE_ITEMS[:1], model, tmp_path)
    n_calls_before = len(backend.calls)
    run_baseline(FAKE_ITEMS[:1], model, tmp_path)
    assert len(backend.calls) == n_calls_before


# --- pipeline areas file -----------------------------------------------------------------------

def test_build_item_areas_has_one_area_whose_only_query_is_the_question():
    areas = build_item_areas(FAKE_ITEMS[0])
    assert len(areas["areas"]) == 1
    area = areas["areas"][0]
    assert area["name"] == FAKE_ITEMS[0].question
    assert area["queries"] == [FAKE_ITEMS[0].question]


# --- budget bookkeeping ------------------------------------------------------------------------

def test_total_spent_sums_every_calls_jsonl_under_the_tree(tmp_path):
    (tmp_path / "q1").mkdir()
    (tmp_path / "q1" / "calls.jsonl").write_text(
        json.dumps({"cost": 0.10}) + "\n" + json.dumps({"cost": 0.05}) + "\n")
    (tmp_path / "q2").mkdir()
    (tmp_path / "q2" / "calls.jsonl").write_text(json.dumps({"cost": None}) + "\n")
    assert total_spent(tmp_path) == pytest.approx(0.15)


def test_would_breach_cap(tmp_path):
    (tmp_path / "calls.jsonl").write_text(json.dumps({"cost": 5.90}) + "\n")
    assert would_breach_cap(tmp_path, 0.25, cap=6.00) is True
    assert would_breach_cap(tmp_path, 0.05, cap=6.00) is False


# --- units_finished (sealing) -------------------------------------------------------------------

def test_units_finished_false_until_every_item_has_both_arms(tmp_path):
    finished, missing = units_finished(FAKE_ITEMS, tmp_path)
    assert finished is False
    assert len(missing) == 6  # 3 items x 2 arms

    for item in FAKE_ITEMS:
        eabst._write_status(tmp_path, item.id, "baseline", "ran")
        eabst._write_status(tmp_path, item.id, "pipeline", "ran")
    finished, missing = units_finished(FAKE_ITEMS, tmp_path)
    assert finished is True
    assert missing == []


# --- mechanical exclusion --------------------------------------------------------------------

def _claim(assertion: str, *, source_url: str, snapshot_text: str, world=World.A,
           kind=SourceKind.DOCUMENTATION, organisation=None) -> tuple[ClaimRecord, str]:
    """Builds one criterion-labelled claim (software-verified span, over a manufactured verifier
    of a different family — evidence.py's own restriction lives in run.py, not in the ClaimRecord
    validator, so a plain 'model' verifier of a distinct family is enough here) and returns the
    snapshot text keyed by its locator's sha256, for the caller to write to disk."""
    import hashlib
    text_sha = hashlib.sha256(snapshot_text.encode()).hexdigest()
    start = snapshot_text.find(assertion)
    assert start != -1, "fixture text must contain the claim's quote verbatim"
    end = start + len(assertion)
    source = eabst.Source(identifier=source_url, kind=kind, world=world, voice=Voice.EXPERT,
                          independence_key=f"ind-{source_url}", published=None, organisation=organisation)
    verification = Verification(verdict="supports",
                                 verifier=Agent(kind="model", id="verifier-x", family="openai"), on=DAY)
    evidence = Evidence(source=source, selector=Selector(exact=assertion,
                        locator=f"sha256:{text_sha};char={start},{end}"), retrieved=DAY,
                        verification=verification)
    generation = Generation(agent=Agent(kind="model", id="extractor-x", family="anthropic"),
                            activity="extraction", on=DAY, spec_sha256="a" * 64)
    claim = ClaimRecord(assertion=assertion, question=Question.DOMAIN, layer=Layer.DOMAIN_STRUCTURE,
                        knowledge_type=KnowledgeType.CONCEPT, scope=Scope(domain="d", task="t"),
                        evidence=(evidence,), generation=generation)
    return claim, text_sha


def _write_pipeline_dir(tmp_path: Path, item_id: str, claims: list[tuple[ClaimRecord, str, str]]) -> Path:
    """claims: (claim, text_sha, snapshot_text) triples."""
    pdir = tmp_path / item_id / "pipeline"
    (pdir / "snapshots").mkdir(parents=True)
    for _, text_sha, text in claims:
        (pdir / "snapshots" / f"{text_sha}.txt").write_text(text, encoding="utf-8")
    ledger = Ledger(purpose="reconstruction", claims=tuple(c for c, _, _ in claims))
    (pdir / "ledger.json").write_text(ledger.to_json())
    return pdir


def test_mechanical_exclusion_flags_a_github_adamkrysztopa_source(tmp_path):
    text = "The pipeline writes frames to dist/frames before encoding."
    claim, text_sha = _claim("The pipeline writes frames to dist/frames",
                             source_url="https://github.com/AdamKrysztopa/informant-video/blob/x/a.md",
                             snapshot_text=text)
    pdir = _write_pipeline_dir(tmp_path, "q1", [(claim, text_sha, text)])
    reasons = mechanical_exclusion_reasons(pdir)
    assert len(reasons) == 1
    assert "github.com/AdamKrysztopa/" in reasons[0]


def test_mechanical_exclusion_flags_a_snapshot_mentioning_the_repo_name(tmp_path):
    text = "A blog post explains how informant-video renders its clips."
    claim, text_sha = _claim("A blog post explains how informant-video renders its clips",
                             source_url="https://someblog.example/post", snapshot_text=text)
    pdir = _write_pipeline_dir(tmp_path, "q1", [(claim, text_sha, text)])
    reasons = mechanical_exclusion_reasons(pdir)
    assert len(reasons) == 1


def test_mechanical_exclusion_clean_ledger_has_no_reasons(tmp_path):
    text = "The general render pipeline writes frames to a configurable output directory."
    claim, text_sha = _claim("The general render pipeline writes frames to a configurable output directory",
                             source_url="https://docs.example/render", snapshot_text=text)
    pdir = _write_pipeline_dir(tmp_path, "q1", [(claim, text_sha, text)])
    assert mechanical_exclusion_reasons(pdir) == []


def test_mechanical_exclusion_ignores_a_source_below_the_criterion_labels(tmp_path):
    """A synthetic (model-only, unverified) claim never triggers exclusion, even if it mentions
    the repo name — it isn't criterion-labelled."""
    unverified_evidence = Evidence(
        source=eabst.Source(identifier="https://github.com/AdamKrysztopa/other", kind=SourceKind.DOCUMENTATION,
                            world=World.A, voice=Voice.EXPERT, independence_key="ind-x", published=None),
        selector=Selector(exact="a", locator="sha256:" + "0" * 64 + ";char=0,1"), retrieved=DAY)
    claim = ClaimRecord(assertion="informant-video is unverified here", question=Question.DOMAIN,
                        layer=Layer.DOMAIN_STRUCTURE, knowledge_type=KnowledgeType.CONCEPT,
                        scope=Scope(domain="d", task="t"), evidence=(unverified_evidence,),
                        generation=Generation(agent=Agent(kind="model", id="x", family="anthropic"),
                                              activity="extraction", on=DAY, spec_sha256="a" * 64))
    pdir = tmp_path / "q1" / "pipeline"
    (pdir / "snapshots").mkdir(parents=True)
    ledger = Ledger(purpose="reconstruction", claims=(claim,))
    (pdir / "ledger.json").write_text(ledger.to_json())
    assert mechanical_exclusion_reasons(pdir) == []


def test_mechanical_exclusion_with_no_ledger_is_clean(tmp_path):
    assert mechanical_exclusion_reasons(tmp_path / "nope") == []


# --- overlap / frame -----------------------------------------------------------------------------

def test_overlaps_question_true_on_shared_content_word():
    assert overlaps_question("Where does the pipeline write frames?",
                             "The pipeline writes frames to dist/frames.") is True


def test_overlaps_question_false_when_only_stopwords_shared():
    assert overlaps_question("What is it?", "The cat sat on the mat.") is False


def test_build_frame_excludes_a_contaminated_item_from_both_arms(tmp_path):
    for item in FAKE_ITEMS:
        (tmp_path / item.id).mkdir()
    text = "A blog post explains how informant-video renders its clips."
    claim, text_sha = _claim("A blog post explains how informant-video renders its clips",
                             source_url="https://someblog.example/post", snapshot_text=text)
    _write_pipeline_dir(tmp_path, "q1", [(claim, text_sha, text)])
    (tmp_path / "q1" / "baseline.json").write_text(json.dumps({"item": "q1", "answer": "x"}))
    for item in FAKE_ITEMS[1:]:
        (tmp_path / item.id / "pipeline").mkdir(parents=True)
        Ledger(purpose="reconstruction").to_json()
        (tmp_path / item.id / "pipeline" / "ledger.json").write_text(
            Ledger(purpose="reconstruction").to_json())
        (tmp_path / item.id / "baseline.json").write_text(json.dumps({"item": item.id, "answer": None}))

    frame = build_frame(FAKE_ITEMS, tmp_path)
    assert "q1" in frame.excluded_items
    assert all(u.item_id != "q1" for u in frame.units)


def test_build_frame_raw_unit_present_only_for_a_non_null_answer(tmp_path):
    for item in FAKE_ITEMS:
        (tmp_path / item.id / "pipeline").mkdir(parents=True)
        (tmp_path / item.id / "pipeline" / "ledger.json").write_text(Ledger(purpose="reconstruction").to_json())
    (tmp_path / "q1" / "baseline.json").write_text(json.dumps({"item": "q1", "answer": "dist/frames"}))
    (tmp_path / "q2" / "baseline.json").write_text(json.dumps({"item": "q2", "answer": None}))
    (tmp_path / "q3" / "baseline.json").write_text(json.dumps({"item": "q3", "answer": "ffmpeg"}))

    frame = build_frame(FAKE_ITEMS, tmp_path)
    raw_items = {u.item_id for u in frame.units if u.arm == "raw"}
    assert raw_items == {"q1", "q3"}
    assert all(u.in_second_coder_subset for u in frame.units if u.arm == "raw")


def test_build_frame_pipeline_unit_present_only_when_overlapping_and_criterion_labelled(tmp_path):
    for item in FAKE_ITEMS:
        (tmp_path / item.id).mkdir()
        (tmp_path / item.id / "baseline.json").write_text(json.dumps({"item": item.id, "answer": None}))
    text = "The render pipeline writes its output frames to dist/frames before encoding."
    overlapping, text_sha = _claim("The render pipeline writes its output frames to dist/frames",
                                   source_url="https://docs.example/a", snapshot_text=text)
    pdir = _write_pipeline_dir(tmp_path, "q1", [(overlapping, text_sha, text)])
    for item in FAKE_ITEMS[1:]:
        (tmp_path / item.id / "pipeline").mkdir(parents=True)
        (tmp_path / item.id / "pipeline" / "ledger.json").write_text(Ledger(purpose="reconstruction").to_json())

    frame = build_frame(FAKE_ITEMS, tmp_path)
    pipeline_units = [u for u in frame.units if u.arm == "pipeline"]
    assert len(pipeline_units) == 1
    assert pipeline_units[0].claim_id == overlapping.claim_id
    assert pipeline_units[0].is_audit is False


def test_build_frame_is_deterministic_across_calls(tmp_path):
    for item in FAKE_ITEMS:
        (tmp_path / item.id).mkdir()
        (tmp_path / item.id / "baseline.json").write_text(json.dumps({"item": item.id, "answer": "a"}))
        (tmp_path / item.id / "pipeline").mkdir(parents=True)
        (tmp_path / item.id / "pipeline" / "ledger.json").write_text(Ledger(purpose="reconstruction").to_json())
    frame_a = build_frame(FAKE_ITEMS, tmp_path)
    frame_b = build_frame(FAKE_ITEMS, tmp_path)
    assert [u.unit_id for u in frame_a.units] == [u.unit_id for u in frame_b.units]
    assert [(u.item_id, u.arm) for u in frame_a.units] == [(u.item_id, u.arm) for u in frame_b.units]


# --- code sheet files --------------------------------------------------------------------------

def test_write_code_sheet_files_refuses_before_every_unit_has_finished(tmp_path):
    with pytest.raises(ValueError, match="sealed"):
        write_code_sheet_files(FAKE_ITEMS, tmp_path, coding_sheet_path=tmp_path / "s.csv",
                               coding_map_path=tmp_path / "m.json", second_coder_path=tmp_path / "s2.csv")


def test_write_code_sheet_files_writes_csvs_once_sealed(tmp_path):
    for item in FAKE_ITEMS:
        (tmp_path / item.id).mkdir()
        (tmp_path / item.id / "baseline.json").write_text(json.dumps({"item": item.id, "answer": "a"}))
        (tmp_path / item.id / "pipeline").mkdir(parents=True)
        (tmp_path / item.id / "pipeline" / "ledger.json").write_text(Ledger(purpose="reconstruction").to_json())
        eabst._write_status(tmp_path, item.id, "baseline", "ran")
        eabst._write_status(tmp_path, item.id, "pipeline", "ran")

    sheet, cmap, second = tmp_path / "s.csv", tmp_path / "m.json", tmp_path / "s2.csv"
    frame = write_code_sheet_files(FAKE_ITEMS, tmp_path, coding_sheet_path=sheet, coding_map_path=cmap,
                                   second_coder_path=second)
    assert sheet.exists() and cmap.exists() and second.exists()
    with sheet.open(newline="") as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == len(frame.units) == 3  # one raw unit per item, no pipeline overlap
    with second.open(newline="") as f:
        second_rows = list(csv.DictReader(f))
    assert len(second_rows) == 3  # all raw-arm units


# --- scoring rules -------------------------------------------------------------------------------

def test_variant_match_is_word_boundary_and_casefolded():
    assert variant_match("It's ffmpeg under the hood", ["FFmpeg"]) is True
    assert variant_match("ffmpegxyz", ["ffmpeg"]) is False
    assert variant_match("no relation", ["ffmpeg"]) is False


@pytest.mark.parametrize(("answers", "candidates", "expected"), [
    (False, (), "abstain"),
    (True, ("ffmpeg",), "correct"),
    (True, ("gstreamer",), "false"),
    (True, ("ffmpeg", "gstreamer"), "false"),  # multi-candidate rule: every candidate must accept
])
def test_classify_unit(answers, candidates, expected):
    assert classify_unit(answers, candidates, ["ffmpeg"]) == expected


@pytest.mark.parametrize(("labels", "expected"), [
    ((), "abstain"),
    (("abstain", "abstain"), "abstain"),
    (("abstain", "correct"), "correct"),
    (("correct", "false"), "false"),
])
def test_classify_item_arm(labels, expected):
    assert classify_item_arm(labels) == expected


def test_cohens_kappa_perfect_agreement_is_one():
    labels = ["correct", "false", "abstain", "correct", "false"]
    assert cohens_kappa(labels, labels) == pytest.approx(1.0)


def test_cohens_kappa_below_one_when_coders_disagree():
    a = ["correct", "correct", "false", "false", "abstain", "abstain"]
    b = ["correct", "false", "false", "correct", "abstain", "abstain"]
    kappa = cohens_kappa(a, b)
    assert kappa < 1.0


def test_cohens_kappa_requires_matching_length():
    with pytest.raises(ValueError):
        cohens_kappa(["a"], ["a", "b"])


# --- Wilson / Newcombe CI -------------------------------------------------------------------------

def test_wilson_ci_contains_the_point_estimate():
    l, u = wilson_ci(7, 10)
    assert l <= 0.7 <= u


def test_wilson_ci_degenerate_n_zero():
    assert wilson_ci(0, 0) == (0.0, 0.0)


def test_paired_newcombe_ci_is_narrow_and_centred_at_zero_when_perfectly_concordant():
    # every item agrees (n10 = n01 = 0): phi = 1 collapses most of the width; the residual comes
    # only from Wilson's asymmetry around the point estimate, so the interval stays narrow and
    # still contains the (zero) point difference.
    lower, upper = paired_newcombe_ci(n11=5, n10=0, n01=0, n00=15)
    assert lower <= 0.0 <= upper
    assert upper - lower < 0.2


def test_paired_newcombe_ci_contains_the_point_difference():
    n11, n10, n01, n00 = 2, 10, 1, 7
    n = n11 + n10 + n01 + n00
    p1, p2 = (n11 + n10) / n, (n11 + n01) / n
    lower, upper = paired_newcombe_ci(n11, n10, n01, n00)
    assert lower <= (p1 - p2) <= upper


def test_paired_newcombe_ci_swap_negates_the_interval():
    lower, upper = paired_newcombe_ci(n11=2, n10=10, n01=1, n00=7)
    lower_swap, upper_swap = paired_newcombe_ci(n11=2, n10=1, n01=10, n00=7)
    assert lower_swap == pytest.approx(-upper, abs=1e-9)
    assert upper_swap == pytest.approx(-lower, abs=1e-9)


# --- gold ledger + gate --------------------------------------------------------------------------

def _gold_claims(n: int) -> list[ClaimRecord]:
    items = FAKE_ITEMS[:n]
    quotes = {
        "q1": "writes its output frames to the `dist/frames` directory",
        "q2": "writes its output frames to the `dist/frames` directory",
        "q3": "writes its output frames to the `dist/frames` directory",
    }
    answers = {"q1": "dist/frames", "q2": "dist/frames", "q3": "dist/frames"}
    return [
        build_gold_claim(item=item, answer=answers[item.id], evidence_file="README.md",
                         evidence_quote=quotes[item.id], repo_root=FIXTURES / "repo",
                         commit="deadbeef", today=DAY)
        for item in items
    ]


def test_build_gold_claim_is_organisational_artefact_supported():
    claims = _gold_claims(1)
    ledger = build_gold_ledger(claims)
    assert ledger.label(claims[0].claim_id) is EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED


def test_build_gold_claim_refuses_a_quote_not_in_the_file():
    with pytest.raises(ValueError, match="not found verbatim"):
        build_gold_claim(item=FAKE_ITEMS[0], answer="x", evidence_file="README.md",
                         evidence_quote="this sentence does not exist in the fixture",
                         repo_root=FIXTURES / "repo", commit="deadbeef", today=DAY)


def test_decide_continues_when_margin_is_met():
    claims = _gold_claims(3)
    ledger = build_gold_ledger(claims)
    decision = decide(far_raw_value=0.60, far_pipe_value=0.20, n_included=24, kappa=0.75,
                      zero_extraction_or_capped=1, gold_claims=claims, gold_ledger=ledger)
    assert decision.outcome == "continue"
    assert set(decision.criterion_ids) == {c.claim_id for c in claims}


def test_decide_stops_when_pipeline_is_no_better():
    claims = _gold_claims(3)
    ledger = build_gold_ledger(claims)
    decision = decide(far_raw_value=0.30, far_pipe_value=0.35, n_included=24, kappa=0.75,
                      zero_extraction_or_capped=0, gold_claims=claims, gold_ledger=ledger)
    assert decision.outcome == "stop"


def test_decide_changes_when_margin_is_partial():
    claims = _gold_claims(3)
    ledger = build_gold_ledger(claims)
    decision = decide(far_raw_value=0.40, far_pipe_value=0.30, n_included=24, kappa=0.75,
                      zero_extraction_or_capped=0, gold_claims=claims, gold_ledger=ledger)
    assert decision.outcome == "change"


@pytest.mark.parametrize(("n_included", "kappa", "zero_or_capped"), [
    (10, 0.75, 0), (24, 0.40, 0), (24, 0.75, 5),
])
def test_decide_inconclusive_conditions(n_included, kappa, zero_or_capped):
    claims = _gold_claims(3)
    ledger = build_gold_ledger(claims)
    decision = decide(far_raw_value=0.60, far_pipe_value=0.10, n_included=n_included, kappa=kappa,
                      zero_extraction_or_capped=zero_or_capped, gold_claims=claims, gold_ledger=ledger)
    assert decision.outcome == "inconclusive"


def test_decide_inconclusive_with_no_second_coder():
    claims = _gold_claims(3)
    ledger = build_gold_ledger(claims)
    decision = decide(far_raw_value=0.60, far_pipe_value=0.10, n_included=24, kappa=None,
                      zero_extraction_or_capped=0, gold_claims=claims, gold_ledger=ledger)
    assert decision.outcome == "inconclusive"
    assert "second coder" in decision.reason


def test_the_gate_refuses_a_synthetic_measurement_as_criterion():
    """A defence-in-depth check: a Measurement scored over a claim ledger.label()'s as synthetic
    must be refused by e_abst_gate itself, matching residual.gates' SyntheticRefused contract —
    this module's own gate is not exempt from it."""
    from residual.gates import SyntheticRefused, measure as residual_measure
    synthetic = ClaimRecord(assertion="a guess", question=Question.DOMAIN, layer=Layer.DOMAIN_STRUCTURE,
                            knowledge_type=KnowledgeType.CONCEPT, scope=Scope(domain="d"),
                            generation=Generation(agent=Agent(kind="model", id="x", family="anthropic"),
                                                  activity="simulation", on=DAY, spec_sha256="a" * 64,
                                                  tier="T1"))
    ledger = Ledger(purpose="surrogate", claims=(synthetic,))
    bad = residual_measure("eabst.far.raw", 0.5, [synthetic], ledger=ledger)
    good_claims = _gold_claims(1)
    good_ledger = build_gold_ledger(good_claims)
    good = residual_measure("eabst.far.pipe", 0.1, good_claims, ledger=good_ledger)
    with pytest.raises(SyntheticRefused):
        eabst.e_abst_gate(far_raw=bad, far_pipe=good, n_included=good, kappa=good, zero_extraction_or_capped=good)


# --- zero-extraction / capped counter -------------------------------------------------------------

def test_is_zero_extraction_or_capped_true_when_no_sidecar(tmp_path):
    assert is_zero_extraction_or_capped(tmp_path / "nope") is True


def test_is_zero_extraction_or_capped_true_when_incomplete(tmp_path):
    (tmp_path / "sidecar.json").write_text(json.dumps({"complete": False, "stats": {"n_sources_fetched": 3}}))
    assert is_zero_extraction_or_capped(tmp_path) is True


def test_is_zero_extraction_or_capped_true_when_no_sources_fetched(tmp_path):
    (tmp_path / "sidecar.json").write_text(json.dumps({"complete": True, "stats": {"n_sources_fetched": 0}}))
    assert is_zero_extraction_or_capped(tmp_path) is True


def test_is_zero_extraction_or_capped_false_for_a_healthy_run(tmp_path):
    (tmp_path / "sidecar.json").write_text(json.dumps({"complete": True, "stats": {"n_sources_fetched": 4}}))
    assert is_zero_extraction_or_capped(tmp_path) is False


# --- run_pipeline_all against a real (scripted) reconstruct() call ---------------------------------

def test_run_pipeline_all_skips_an_item_that_would_breach_the_overall_cap(tmp_path, monkeypatch):
    """Uses the real reconstruct.run.reconstruct() entry point with fully scripted, offline
    backends (per the e2e test-support contract) to exercise the skip-start rule end to end."""
    import httpx
    from e2e_support import http_client, make_models, page_from_fixture, script_default_decoys

    out_dir = tmp_path / "runs"
    # Pre-seed spend so the overall cap is already exhausted before the pipeline step starts.
    (out_dir / "_baseline").mkdir(parents=True)
    (out_dir / "_baseline" / "calls.jsonl").write_text(json.dumps({"cost": 6.00}) + "\n")

    models_path = tmp_path / "models.json"
    models_path.write_text(json.dumps({
        "planner": {"provider": "openrouter", "model": "anthropic/claude-haiku-4.5", "family": "anthropic"},
        "extractor": {"provider": "openrouter", "model": "anthropic/claude-haiku-4.5", "family": "anthropic"},
        "verifier": {"provider": "openrouter", "model": "openai/gpt-5.4-mini", "family": "openai"},
        "contradiction": {"provider": "openrouter", "model": "openai/gpt-5.4-mini", "family": "openai"},
        "baseline": {"provider": "openrouter", "model": "anthropic/claude-haiku-4.5", "family": "anthropic"},
    }))
    monkeypatch.setenv("OPENROUTER_API_KEY", "test-key")

    with httpx.Client() as http:
        results = eabst.run_pipeline_all(FAKE_ITEMS[:1], models_path=models_path, out_dir=out_dir,
                                         http=http, today=DAY)
    assert results == [{"item": "q1", "status": "skipped", "reason": "would breach the overall cap"}]
    status = json.loads((out_dir / "status.json").read_text())
    assert status["q1"]["pipeline"] == "skipped"


# --- score wiring: key.json / accidental.json / coding-map classification --------------------------

def _coding_map(units: Mapping[str, dict], excluded_items: dict | None = None) -> dict:
    return {"units": units, "excluded_items": excluded_items or {}, "seeds": {}, "generated_at": "x"}


def test_load_key_returns_commit_and_items_by_id(tmp_path):
    p = tmp_path / "key.json"
    p.write_text(json.dumps({"commit": "deadbeef", "items": [
        {"id": "q1", "answer": "a", "accept": ["a"], "evidence_file": "README.md", "evidence_quote": "q"},
    ]}))
    commit, by_id = load_key(p)
    assert commit == "deadbeef"
    assert set(by_id) == {"q1"}
    assert by_id["q1"]["answer"] == "a"


def test_load_accidental_missing_file_is_empty(tmp_path):
    assert load_accidental(tmp_path / "nope.json") == frozenset()


def test_load_accidental_reads_unit_ids(tmp_path):
    p = tmp_path / "accidental.json"
    p.write_text(json.dumps({"unit_ids": ["u001", "u002"]}))
    assert load_accidental(p) == frozenset({"u001", "u002"})


def test_unit_labels_all_only_covers_units_present_in_coded():
    cmap = _coding_map({
        "u001": {"item_id": "q1", "arm": "raw"},
        "u002": {"item_id": "q2", "arm": "raw"},
    })
    coded = {"u001": CodedUnit(unit_id="u001", answers=True, candidates=("dist/frames",))}
    labels = unit_labels_all(cmap, coded, {"q1": ["dist/frames"]})
    assert labels == {"u001": "correct"}


def test_item_arm_labels_defaults_missing_arm_to_abstain_and_skips_excluded_items():
    cmap = _coding_map({
        "u001": {"item_id": "q1", "arm": "raw", "is_audit": False},
        "u002": {"item_id": "q1", "arm": "pipeline", "is_audit": False},
    }, excluded_items={"q2": ["reason"]})
    labels = {"u001": "correct", "u002": "false"}
    out = item_arm_labels(FAKE_ITEMS, cmap, labels, excluded_ids={"q2"})
    assert out == {"q1": {"raw": "correct", "pipeline": "false"}, "q3": {"raw": "abstain", "pipeline": "abstain"}}
    assert "q2" not in out


def test_item_arm_labels_ignores_audit_units():
    cmap = _coding_map({
        "u001": {"item_id": "q1", "arm": "pipeline", "is_audit": True},
    })
    out = item_arm_labels(FAKE_ITEMS[:1], cmap, {"u001": "correct"}, excluded_ids=set())
    assert out == {"q1": {"raw": "abstain", "pipeline": "abstain"}}


def test_audit_miss_rate_counts_answering_share_of_audit_units_only():
    cmap = _coding_map({
        "u001": {"item_id": "q1", "arm": "pipeline", "is_audit": True},
        "u002": {"item_id": "q1", "arm": "pipeline", "is_audit": True},
        "u003": {"item_id": "q1", "arm": "raw", "is_audit": False},
    })
    labels = {"u001": "correct", "u002": "abstain", "u003": "correct"}
    assert audit_miss_rate(cmap, labels) == (1, 2)


def test_far_counts():
    item_labels = {"q1": {"raw": "correct", "pipeline": "false"}, "q2": {"raw": "false", "pipeline": "correct"}}
    assert far_counts(item_labels, "raw") == (1, 2)
    assert far_counts(item_labels, "pipeline") == (1, 2)


def test_paired_false_counts_all_four_cells():
    item_labels = {
        "q1": {"raw": "correct", "pipeline": "correct"},   # n00
        "q2": {"raw": "false", "pipeline": "abstain"},      # n10
        "q3": {"raw": "abstain", "pipeline": "false"},      # n01
    }
    assert paired_false_counts(item_labels) == (0, 1, 1, 1)


def test_accidental_correct_counts_tallies_by_arm():
    cmap = _coding_map({
        "u001": {"item_id": "q1", "arm": "raw"},
        "u002": {"item_id": "q1", "arm": "pipeline"},
    })
    labels = {"u001": "correct", "u002": "correct"}
    counts = accidental_correct_counts(cmap, labels, frozenset({"u001"}))
    assert counts == {"raw": 1, "pipeline": 0}


def test_accidental_correct_counts_refuses_a_unit_not_coded_correct():
    cmap = _coding_map({"u001": {"item_id": "q1", "arm": "raw"}})
    with pytest.raises(ValueError, match="not correct"):
        accidental_correct_counts(cmap, {"u001": "false"}, frozenset({"u001"}))


def test_accidental_correct_counts_refuses_an_unknown_unit():
    cmap = _coding_map({})
    with pytest.raises(ValueError, match="not in coding_map"):
        accidental_correct_counts(cmap, {}, frozenset({"u999"}))


def test_compute_kappa_none_with_no_second_coder():
    cmap = _coding_map({"u001": {"item_id": "q1", "arm": "raw", "in_second_coder_subset": True}})
    assert compute_kappa(cmap, {"u001": "correct"}, None) is None


def test_compute_kappa_none_when_second_coder_covers_nothing_in_the_subset():
    cmap = _coding_map({"u001": {"item_id": "q1", "arm": "raw", "in_second_coder_subset": True}})
    assert compute_kappa(cmap, {"u001": "correct"}, {}) is None


def test_compute_kappa_perfect_agreement_over_the_second_coder_subset():
    cmap = _coding_map({
        "u001": {"item_id": "q1", "arm": "raw", "in_second_coder_subset": True},
        "u002": {"item_id": "q2", "arm": "raw", "in_second_coder_subset": True},
        "u003": {"item_id": "q3", "arm": "pipeline", "in_second_coder_subset": False},
    })
    owner = {"u001": "correct", "u002": "false", "u003": "correct"}
    second = {"u001": "correct", "u002": "false"}
    assert compute_kappa(cmap, owner, second) == pytest.approx(1.0)


def test_count_zero_extraction_or_capped_across_items(tmp_path):
    for item_id, stats in (("q1", {"complete": True, "stats": {"n_sources_fetched": 3}}),
                           ("q2", {"complete": True, "stats": {"n_sources_fetched": 0}})):
        d = tmp_path / item_id / "pipeline"
        d.mkdir(parents=True)
        (d / "sidecar.json").write_text(json.dumps(stats))
    # q3 has no pipeline dir at all -> also counted (no sidecar.json).
    assert count_zero_extraction_or_capped(FAKE_ITEMS, tmp_path) == 2


# --- score_eabst end to end (offline, synthetic key/coding sheets) ---------------------------------

def _score_eabst_fixture(tmp_path):
    """A hand-built, arithmetic-checkable scenario over FAKE_ITEMS:
    q1 raw=correct, pipeline=correct (an audit unit too, answering);
    q2 raw=false, pipeline has no unit (abstain by omission);
    q3 raw has no unit (abstain by omission), pipeline=false.
    The second coder covers q1's raw+pipeline units and q2's raw unit, agreeing throughout.
    """
    quote = "writes its output frames to the `dist/frames` directory"
    key_items = {qid: {"id": qid, "answer": "dist/frames", "accept": ["dist/frames"],
                       "evidence_file": "README.md", "evidence_quote": quote}
                 for qid in ("q1", "q2", "q3")}

    coding_map = _coding_map({
        "u001": {"item_id": "q1", "arm": "raw", "is_audit": False, "in_second_coder_subset": True},
        "u002": {"item_id": "q1", "arm": "pipeline", "is_audit": False, "in_second_coder_subset": True},
        "u003": {"item_id": "q1", "arm": "pipeline", "is_audit": True, "in_second_coder_subset": False},
        "u004": {"item_id": "q2", "arm": "raw", "is_audit": False, "in_second_coder_subset": True},
        "u005": {"item_id": "q3", "arm": "pipeline", "is_audit": False, "in_second_coder_subset": False},
    })
    owner_coded = {
        "u001": CodedUnit(unit_id="u001", answers=True, candidates=("dist/frames",)),
        "u002": CodedUnit(unit_id="u002", answers=True, candidates=("dist/frames",)),
        "u003": CodedUnit(unit_id="u003", answers=True, candidates=("dist/frames",)),
        "u004": CodedUnit(unit_id="u004", answers=True, candidates=("gstreamer",)),
        "u005": CodedUnit(unit_id="u005", answers=True, candidates=("gstreamer",)),
    }
    second_coded = {
        "u001": CodedUnit(unit_id="u001", answers=True, candidates=("dist/frames",)),
        "u002": CodedUnit(unit_id="u002", answers=True, candidates=("dist/frames",)),
        "u004": CodedUnit(unit_id="u004", answers=True, candidates=("gstreamer",)),
    }
    accidental_ids = frozenset({"u001"})

    out_dir = tmp_path / "runs"
    for item_id, stats in (("q1", {"complete": True, "stats": {"n_sources_fetched": 3}}),
                           ("q2", {"complete": True, "stats": {"n_sources_fetched": 0}}),
                           ("q3", {"complete": True, "stats": {"n_sources_fetched": 2}})):
        d = out_dir / item_id / "pipeline"
        d.mkdir(parents=True)
        (d / "sidecar.json").write_text(json.dumps(stats))

    return dict(items=FAKE_ITEMS, key_items=key_items, commit="deadbeef", coding_map=coding_map,
               owner_coded=owner_coded, second_coded=second_coded, accidental_ids=accidental_ids,
               repo_root=FIXTURES / "repo", out_dir=out_dir, today=DAY)


def test_score_eabst_far_and_paired_counts_match_the_hand_built_scenario(tmp_path):
    result = score_eabst(**_score_eabst_fixture(tmp_path))
    public = result["public"]
    assert public["n_included"] == 3
    assert public["far_raw"] == {"false": 1, "n": 3, "rate": pytest.approx(1 / 3)}
    assert public["far_pipe"] == {"false": 1, "n": 3, "rate": pytest.approx(1 / 3)}
    assert public["paired_2x2"] == {"n11": 0, "n10": 1, "n01": 1, "n00": 1}
    assert public["kappa"] == pytest.approx(1.0)
    assert public["audit_miss_rate"] == {"answering": 1, "total": 1, "rate": 1.0}
    assert public["accidental_correct"] == {"raw": 1, "pipeline": 0}
    assert public["zero_extraction_or_capped"] == 1  # q2's sidecar has n_sources_fetched=0


def test_score_eabst_gate_decision_is_inconclusive_below_min_included(tmp_path):
    result = score_eabst(**_score_eabst_fixture(tmp_path))
    decision = result["public"]["decision"]
    assert decision["outcome"] == "inconclusive"
    assert "n_included" in decision["reason"]


def test_score_eabst_sealed_holds_item_labels_public_does_not(tmp_path):
    result = score_eabst(**_score_eabst_fixture(tmp_path))
    assert result["sealed"]["item_labels"]["q1"] == {"raw": "correct", "pipeline": "correct"}
    assert "item_labels" not in result["public"]


def test_score_eabst_public_has_no_question_or_answer_text(tmp_path):
    """The whole point of the sealed/public split: nothing from questions.json or key.json
    (item questions, answers, accept variants, evidence quotes) leaks into the public half."""
    result = score_eabst(**_score_eabst_fixture(tmp_path))
    blob = json.dumps(result["public"])
    for leaked in ("dist/frames", "gstreamer", "render pipeline", "output frames"):
        assert leaked not in blob


def test_render_eabst_markdown_has_no_question_or_answer_text(tmp_path):
    result = score_eabst(**_score_eabst_fixture(tmp_path))
    md = render_eabst_markdown(result["public"])
    assert "FAR raw" in md and "Gate decision" in md
    for leaked in ("dist/frames", "gstreamer"):
        assert leaked not in md
