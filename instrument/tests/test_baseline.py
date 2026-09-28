import json

import pytest

from probe_code.baseline import (PROPOSED_THRESHOLDS, freeze_decision, pooled_metrics, session_metrics,
                                 thresholds_from_baseline, wilson)


def write_events(d, events, config=None, simulated=False):
    d.mkdir(parents=True)
    (d / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events) + "\n")
    (d / "manifest.json").write_text(json.dumps({"config": config or {"guard_model": "g"}, "simulated": simulated}))
    return d


def probe(t, source="ai", set_id="A"):
    return {"type": "probe", "t_mono": t, "set_id": set_id, "turn": {"source": source}}


def answer(t, set_id="A"):
    return {"type": "expert_answer", "t_mono": t, "set_id": set_id}


FAKE = [
    {"type": "probe_started", "t_mono": 0, "set_id": "A", "arm": "ai"},
    probe(3),
    answer(10),
    {"type": "turn_rejected", "t_mono": 14, "set_id": "A", "reason": "leading: it introduces 'units'"},
    probe(18),
    answer(20),
    {"type": "turn_rejected", "t_mono": 22, "set_id": "A", "reason": "contract: bad anchor"},
    {"type": "interviewer_failed", "t_mono": 23, "set_id": "A", "reason": "LLMRefused('no')"},
    probe(24, "ai_fallback"),
    answer(30),
    {"type": "guard_failed", "t_mono": 30.5, "set_id": "A", "reason": "LLMUnavailable('x')"},
    {"type": "cap_reached", "t_mono": 31, "set_id": "A", "source": "ai", "discarded": {}},
    {"type": "session_ended_by_interviewer", "t_mono": 32, "set_id": "A"},
    {"type": "probe_finished", "t_mono": 32, "set_id": "A"},
    {"type": "probe_started", "t_mono": 40, "set_id": "B", "arm": "human"},
    {"type": "probe_finished", "t_mono": 60, "set_id": "B"},
]


def test_session_metrics_on_a_fake_session(tmp_path):
    m = session_metrics(write_events(tmp_path / "S1", FAKE))
    assert m["ai_sets"] == {"started": 1, "finished": 1}
    assert m["counts"]["delivered"] == 3 and m["counts"]["generated"] == 6
    assert m["rates"]["fallback"]["k"] == 1 and m["rates"]["fallback"]["n"] == 3
    assert m["rates"]["contract_rejection"] == {"k": 1, "n": 6, "rate": 1 / 6, "ci95": pytest.approx(wilson(1, 6))}
    assert (m["rates"]["guard_rejection"]["k"], m["rates"]["guard_rejection"]["n"]) == (1, 4)
    assert (m["rates"]["refusal"]["k"], m["rates"]["refusal"]["n"]) == (1, 3)
    assert m["latency_s"]["gaps"] == [8, 4] and m["latency_s"]["median"] == 6


def test_pooled_metrics_sum_counts_before_dividing(tmp_path):
    a = session_metrics(write_events(tmp_path / "S1", FAKE))
    b = session_metrics(write_events(tmp_path / "S2", FAKE[:3] + [probe(12)]))
    pooled = pooled_metrics([a, b])
    assert pooled["counts"]["delivered"] == 5
    assert pooled["rates"]["fallback"]["k"] == 1 and pooled["rates"]["fallback"]["n"] == 5
    assert pooled["ai_sets"] == {"started": 2, "finished": 1}
    assert pooled["latency_s"]["gaps"] == [8, 4, 2]


def test_pooling_refuses_mixed_configurations(tmp_path):
    a = session_metrics(write_events(tmp_path / "S1", FAKE))
    b = session_metrics(write_events(tmp_path / "S2", FAKE, config={"guard_model": "other"}))
    with pytest.raises(ValueError):
        pooled_metrics([a, b])


def test_thresholds_are_the_baseline_upper_bounds_rounded_to_5_points():
    def r(k, n):
        return {"k": k, "n": n, "rate": k / n, "ci95": wilson(k, n)}
    # The pooled counts of the three current-configuration simulated sessions in docs/freeze-baseline.md.
    baseline = {"rates": {"fallback": r(1, 86), "contract_rejection": r(0, 95), "guard_rejection": r(4, 89),
                          "refusal": r(0, 86)}}
    derived = thresholds_from_baseline(baseline)
    assert derived == {k: PROPOSED_THRESHOLDS[k] for k in derived}
    assert derived == {"fallback": 0.05, "contract_rejection": 0.05, "guard_rejection": 0.10, "refusal": 0.05}


def test_wilson_matches_hand_computation():
    low, high = wilson(3, 34)
    assert low == pytest.approx(0.0304, abs=1e-3) and high == pytest.approx(0.2295, abs=1e-3)
    assert wilson(0, 0) is None


def _pooled(delivered=40, fallback=2, guard=(3, 40), contract=(1, 45), refused=0, median=4.0, simulated=0):
    def r(k, n):
        return {"k": k, "n": n, "rate": k / n if n else None}
    return {"counts": {"delivered": delivered}, "simulated_sessions": simulated,
            "rates": {"fallback": r(fallback, delivered), "guard_rejection": r(*guard),
                      "contract_rejection": r(*contract), "refusal": r(refused, delivered)},
            "latency_s": {"median": median}}


@pytest.mark.parametrize("pooled, outcome", [
    (_pooled(), "accept"),
    (_pooled(delivered=20, fallback=0), "rerun"),
    (_pooled(fallback=12), "change one variable"),
    (_pooled(median=7.5), "change one variable"),
    (_pooled(refused=6), "change the model"),
    (_pooled(guard=(7, 40)), "rerun"),
    (_pooled(guard=(7, 40), simulated=3), "accept"),
    (_pooled(guard=(0, 0)), "rerun"),
])
def test_freeze_decision(pooled, outcome):
    rule = {**PROPOSED_THRESHOLDS, "fallback": 0.15, "guard_rejection": 0.20, "contract_rejection": 0.10, "refusal": 0.10}
    assert freeze_decision(pooled, rule)["outcome"] == outcome
