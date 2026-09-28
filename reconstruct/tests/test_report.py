"""D2: report.py's headline surfaces stats.failed_calls_by_task, so a run where calls silently
vanished shows it at a glance instead of only in sidecar.json.
"""
from __future__ import annotations

from reconstruct.report import _headline

_BASE_STATS = {
    "n_located": 3, "n_verified": 2, "decoy_false_accept_rate": 0.0, "total_cost_usd": 0.01,
}

_BASE_SIDECAR = {
    "complete": True, "incomplete_reasons": [],
    "config": {"models": {"verifier": {"family": "openai"}}},
}


def test_headline_omits_failed_calls_line_when_every_task_is_zero():
    sidecar = {**_BASE_SIDECAR, "stats": {
        **_BASE_STATS,
        "failed_calls_by_task": {"plan": 0, "extract": 0, "verify": 0, "cross_verify": 0,
                                  "decoy": 0, "web_search": 0},
    }}
    assert "failed call" not in _headline(sidecar).lower()


def test_headline_lists_nonzero_failed_calls_by_task():
    sidecar = {**_BASE_SIDECAR, "stats": {
        **_BASE_STATS,
        "failed_calls_by_task": {"plan": 0, "extract": 1, "verify": 2, "cross_verify": 0,
                                  "decoy": 0, "web_search": 3},
    }}
    line = _headline(sidecar)
    assert "extract 1" in line
    assert "verify 2" in line
    assert "web_search 3" in line
    assert "plan 0" not in line
    assert "decoy 0" not in line
    assert "cross_verify 0" not in line
