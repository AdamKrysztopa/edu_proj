"""The codebase parameter (D1c plan §2): one JSON config names everything codebase-specific, and
D1b's own config replays D1b's committed outputs byte for byte. Reads the committed D1 ledgers;
no model, no network."""
import json
from pathlib import Path

import pytest

import build_sheet as bs
import codebase
import common

HERE = Path(__file__).resolve().parents[1]


def test_d1b_config_resolves_to_the_paths_d1b_was_built_with():
    cb = codebase.d1b()
    assert cb.root == HERE
    assert cb.ledgers == common.LEDGER_DIRS
    assert cb.corpus == common.D1 / "corpus"
    assert cb.seed == bs.SEED and cb.domain == "forecastability"
    assert cb.owner_repo == "github.com/AdamKrysztopa/dependence-forecastability"
    assert [it["q"] for it in cb.prior_items()] == [it["q"] for it in common.d1_items()]


def test_relative_paths_resolve_against_the_config_file(tmp_path):
    (tmp_path / "corpus").mkdir()
    cfg = {"name": "x", "title": "X", "owner_repo": "github.com/o/x", "domain": "x", "seed": 7,
           "corpus": "corpus", "ledgers": {"cheap": "runs/cheap"}, "prior_items": None,
           "canaries": "fixtures/canaries.json", "canary_mode": "generated"}
    (tmp_path / "codebase.json").write_text(json.dumps(cfg))
    cb = codebase.load(tmp_path / "codebase.json")
    assert cb.corpus == tmp_path / "corpus" and cb.ledgers == {"cheap": tmp_path / "runs" / "cheap"}
    assert cb.prior_items() == [] and cb.canary_mode == "generated"
    assert cb.pool == tmp_path / "pool.json"


@pytest.mark.parametrize("repo", ["github.com/AdamKrysztopa/informant-video", "github.com/AdamKrysztopa/edu_proj"])
def test_an_excluded_repository_is_refused(tmp_path, repo):
    cfg = {"name": "x", "title": "X", "owner_repo": repo, "domain": "x", "seed": 7, "corpus": "corpus",
           "ledgers": {}, "prior_items": None, "canaries": "c.json"}
    (tmp_path / "codebase.json").write_text(json.dumps(cfg))
    with pytest.raises(codebase.Excluded):
        codebase.load(tmp_path / "codebase.json")


@pytest.mark.parametrize("field,value", [("owner_repo", "https://github.com/AdamKrysztopa/informant-video.git"),
                                         ("repo_url", "https://github.com/adamkrysztopa/Informant-Video/")])
def test_the_exclusion_check_normalises_and_covers_the_corpus_repository(tmp_path, field, value):
    cfg = {"name": "x", "title": "X", "owner_repo": "github.com/AdamKrysztopa/x", "domain": "x", "seed": 7,
           "corpus": "corpus", "ledgers": {}, "prior_items": None, "canaries": "c.json",
           "corpus_build": {"repo_url": "https://github.com/AdamKrysztopa/x"}}
    if field == "owner_repo":
        cfg["owner_repo"] = value
    else:
        cfg["corpus_build"]["repo_url"] = value
    (tmp_path / "codebase.json").write_text(json.dumps(cfg))
    with pytest.raises(codebase.Excluded):
        codebase.load(tmp_path / "codebase.json")


def test_neither_d1_reconstruction_counts_as_complete():
    cb = codebase.d1b()
    cheap = codebase.reconstruction_problems(cb.ledger_path("cheap-26b").parent)
    top = codebase.reconstruction_problems(cb.ledger_path("toptier-26b").parent)
    assert any("budget exceeded" in p for p in cheap)
    assert "cross_verify: 761 failed calls" in top and "decoy: 30 failed calls" in top


def test_a_retried_call_that_succeeded_leaves_a_run_complete(tmp_path):
    (tmp_path / "sidecar.json").write_text(json.dumps(
        {"complete": True, "incomplete_reasons": [], "stats": {"failed_calls_by_task": {"verify": 0, "decoy": 0}}}))
    (tmp_path / "calls.jsonl").write_text(json.dumps({"task": "verify", "outcome": "api_error"}) + "\n"
                                          + json.dumps({"task": "verify", "outcome": "ok"}) + "\n")
    assert codebase.reconstruction_problems(tmp_path) == []


def test_a_config_with_a_placeholder_is_refused(tmp_path):
    cfg = json.loads((HERE.parent / "d1c" / "codebase.template.json").read_text())
    (tmp_path / "codebase.json").write_text(json.dumps(cfg))
    with pytest.raises(codebase.Unfilled, match="TODO"):
        codebase.load(tmp_path / "codebase.json")


def test_d1b_pool_and_review_pack_replay_byte_identically():
    pool_text, pack_text, _ = bs.pool_outputs(codebase.d1b())
    assert pool_text == (HERE / "pool.json").read_text()
    assert pack_text == (HERE / "fixtures" / "topic_review_pack.md").read_text()


def test_with_no_prior_items_nothing_is_excluded_for_overlap_and_the_pack_says_so():
    cb = codebase.replace(codebase.d1b(), prior_items_path=None)
    pool_text, pack_text, _ = bs.pool_outputs(cb)
    rows = json.loads(pool_text)["rows"]
    d1b_rows = json.loads((HERE / "pool.json").read_text())["rows"]
    assert len(rows) > len(d1b_rows)
    assert {(r["ledger"], r["test_id"]) for r in d1b_rows} <= {(r["ledger"], r["test_id"]) for r in rows}
    assert "D1's" not in pack_text and "another topic below" in pack_text


def test_the_pool_can_be_restricted_to_some_ledgers():
    pool_text, _, _ = bs.pool_outputs(codebase.d1b(), ledgers=["cheap-26b"])
    assert {r["ledger"] for r in json.loads(pool_text)["rows"]} == {"cheap-26b"}
