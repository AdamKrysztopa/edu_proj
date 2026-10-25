"""scripts/cost_ledger.py (I11): one row per recorded call, reconciled against each run's own total."""

import importlib.util
import json
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location("cost_ledger", REPO / "scripts" / "cost_ledger.py")
cl = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cl)


def _call(task="verify", outcome="ok", cost=0.001, spec="a", **kw):
    r = {"task": task, "role": "verifier", "model": "m", "family": "f", "served_model": "m",
         "spec_sha256": spec, "input_tokens": 10, "output_tokens": 2, "cost": cost,
         "utc": "2026-09-28T00:00:00+00:00", **kw}
    if outcome is not None:
        r["outcome"] = outcome
    return r


def _write_jsonl(path: Path, records: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r) + "\n" for r in records))
    return path


def test_status_ok_is_success_and_missing_outcome_is_unknown():
    assert cl.classify([_call(), _call(outcome=None)]) == ["success", "unknown"]


def test_failed_attempt_repeated_later_is_a_retry_and_the_last_one_a_failure():
    recs = [_call(outcome="api_error", cost=None), _call(outcome="api_error", cost=None),
            _call(outcome="ok"), _call(spec="b", outcome="api_error", cost=None)]
    assert cl.classify(recs) == ["retry", "retry", "success", "failure"]


def test_billed_bad_outcome_is_a_failure_and_its_cost_is_lost():
    rows = cl.rows_from_calls([_call(task="extract", outcome="truncated", cost=0.02), _call(cost=0.01)],
                              run="r", kind="engineering")
    assert [r["status"] for r in rows] == ["failure", "success"]
    s = cl.summarise(rows)
    assert s["lost_usd"] == pytest.approx(0.02)
    assert s["lost_share"] == pytest.approx(0.02 / 0.03)


def test_rows_never_carry_prompt_hashes():
    rows = cl.rows_from_calls([_call()], run="r", kind="evaluation")
    assert not {"spec_sha256", "prompt_sha256", "system", "user"} & set(rows[0])
    assert rows[0]["usd"] == 0.001 and rows[0]["stage"] == "verify" and rows[0]["kind"] == "evaluation"


def test_plant_authoring_rejected_then_accepted_is_retry_never_accepted_is_failure():
    log = [{"page_id": "p1", "accepted": False, "cost": 0.004, "input_tokens": 1, "output_tokens": 1,
            "served_model": "m", "problems": ["x"]},
           {"page_id": "p1", "accepted": True, "cost": 0.004, "input_tokens": 1, "output_tokens": 1,
            "served_model": "m", "problems": []},
           {"page_id": "p2", "accepted": False, "cost": 0.004, "input_tokens": 1, "output_tokens": 1,
            "served_model": "m", "problems": ["y"]}]
    rows = cl.rows_from_plant_authoring(log, run="e_plant/plant_authoring")
    assert [r["status"] for r in rows] == ["retry", "success", "failure"]
    assert all("problems" not in r and "page_id" not in r for r in rows)


def _jev_entry(model, *, content=None, answers=None, cost=0.0001, state=None):
    if model == "typesafe/jev-1.13":
        req = {"model": model, "state": state or {"seed_assertion": "s"}, "questions": {}}
        resp = {"answers": answers or {}, "usage": {"cost": cost, "input_tokens": 5, "output_tokens": 1}}
    else:
        req = {"model": model, "messages": [{"role": "user", "content": "q"}]}
        resp = {"choices": [{"message": {"content": content}}],
                "usage": {"cost": cost, "prompt_tokens": 5, "completion_tokens": 1}}
    return {"request": req, "response": resp}


def test_jev_cache_rows_by_model_and_unreadable_qwen_is_failure(tmp_path):
    entries = [
        _jev_entry("typesafe/jev-1.13", answers={"q": {"choice": "no"}}),
        _jev_entry("typesafe/jev-1.13", answers={"tacit_a": 0.5}, state={"statement": "x"}),
        _jev_entry("qwen/qwen-2.5-7b-instruct", content='{"choice": "states"}'),
        _jev_entry("qwen/qwen-2.5-7b-instruct", content='{"choice": "maybe'),
        _jev_entry("anthropic/claude-sonnet-5.5", content='{"states": [1], "partially": []}', cost=0.004),
    ]
    rows = cl.rows_from_jev_cache(entries)
    assert [r["stage"] for r in rows] == ["jev_closure_substitution", "jev_tacit_signal",
                                          "qwen_same_prompt", "qwen_same_prompt", "sonnet_reference"]
    assert [r["status"] for r in rows] == ["success", "success", "success", "failure", "success"]
    assert {r["kind"] for r in rows} == {"engineering"}


def test_reconcile_flags_a_gap_over_one_cent_and_a_missing_recorded_total():
    rows = [{"run": "a", "usd": 0.500}, {"run": "a", "usd": 0.004}, {"run": "b", "usd": 0.2}]
    out = {r["run"]: r for r in cl.reconcile(rows, {"a": [("sidecar", 0.5)], "b": [("report", 0.18)]},
                                             runs=["a", "b", "c"])}
    assert out["a"]["ok"] is True and out["a"]["checks"][0]["gap_usd"] == pytest.approx(0.004)
    assert out["b"]["ok"] is False and out["b"]["checks"][0]["gap_usd"] == pytest.approx(0.02)
    assert out["c"]["ok"] is None and out["c"]["checks"] == []


def test_validated_item_cost_is_unavailable_whatever_the_claim_counts():
    m = cl.unit_costs(spend_usd=1.0, n_verified_claims=100, n_candidates=10, n_hyp=2)
    assert m["per_verified_claim_usd"] == pytest.approx(0.01)
    assert m["per_gap_candidate_usd"] == pytest.approx(0.1)
    assert m["per_validated_item_usd"] is None
    assert "no item is validated" in m["per_validated_item_reason"]


def test_prospective_caps_flag_when_their_sum_exceeds_headroom():
    p = cl.prospective([("x", 1.0), ("y", 2.5)], headroom_usd=3.0)
    assert p["sum_caps_usd"] == pytest.approx(3.5)
    assert p["fits"] is False and p["shortfall_usd"] == pytest.approx(0.5)
    assert cl.prospective([("x", 1.0)], headroom_usd=3.0)["fits"] is True


def test_unit_prices_are_per_run_and_stage_and_include_billed_failures():
    rows = [{"run": "a", "stage": "extract", "usd": 0.01, "status": "success"},
            {"run": "a", "stage": "extract", "usd": 0.03, "status": "failure"},
            {"run": "b", "stage": "extract", "usd": 0.002, "status": "unknown"}]
    p = cl.unit_prices(rows)
    assert p["a"]["extract"]["mean_usd"] == pytest.approx(0.02) and p["a"]["extract"]["max_usd"] == 0.03
    assert p["b"]["extract"]["calls"] == 1


def test_v3_projection_adds_pending_verifies_cross_verify_and_decoys_to_the_base_run():
    rows = [{"run": "base", "stage": "verify", "usd": 0.001, "status": "success"},
            {"run": "base", "stage": "extract", "usd": 0.5, "status": "success"},
            {"run": "old", "stage": "decoy", "usd": 0.0005, "status": "unknown"}]
    p = cl.project_v3_domain(rows, base_run="base", n_supports=100, n_pending=40, decoy_runs=["old"],
                             n_decoys=30)
    assert p["pending_verify_usd"] == pytest.approx(40 * 0.001)
    assert p["cross_verify_usd"] == pytest.approx(2 * 100 * 0.001)
    assert p["decoy_usd"] == pytest.approx(30 * (0.0005 + 0.001))
    assert p["projected_usd"] == pytest.approx(0.501 + 0.04 + 0.2 + 0.045)


def test_e_abst_rows_cannot_be_linked_to_an_item(tmp_path):
    p = tmp_path / ".private"
    for dom in ("food", "concreting"):
        for arm in ("baseline", "pipeline_run1"):
            _write_jsonl(p / "e_plant" / "runs" / dom / arm / "calls.jsonl", [_call()])
    _write_jsonl(p / "e_plant" / "plant_authoring_log.jsonl", [])
    _write_jsonl(p / "e_abst" / "runs" / "_baseline" / "calls.jsonl",
                 [_call(task="baseline", outcome=None, cost=c) for c in (0.0003, 0.0001, 0.0002)])
    _write_jsonl(p / "e_abst" / "exposure_calls.jsonl", [])
    for item, cost in (("E-ABST-02", 0.02), ("E-ABST-01", 0.01)):
        _write_jsonl(p / "e_abst" / "runs" / item / "pipeline_run1" / "calls.jsonl", [_call(cost=cost)])
    rows = [r for r in cl._private_rows(p) if r["run"].startswith("e_abst/")]
    assert all(r["unit"] is None and "E-ABST" not in str(r["source"]) for r in rows)
    assert [r["usd"] for r in rows if r["run"] == "e_abst/baseline"] == [0.0001, 0.0002, 0.0003]


def test_build_on_the_committed_e_live_runs_reconciles_without_private_data():
    ledger = cl.build(REPO, private=None)
    rec = {r["run"]: r for r in ledger["reconciliation"]}
    e_live = [r for r in rec if r.startswith("e_live/")]
    assert len(e_live) == 6
    assert all(rec[r]["ok"] for r in e_live)
    assert rec["spike/jev"]["ok"] is True
    assert ledger["sources_missing"] == ["private"]
    assert ledger["unit_costs"]["per_validated_item_usd"] is None
