import json
import math

import pytest

from probe_code.agreement import (alpha_masi, alpha_nominal, cohen_kappa, decoy_false_rate, guess_rate,
                                  masi_distance, per_code_kappa)
from probe_code.corroboration import corroboration_sheet
from probe_code.export import read_csv
from probe_code.guard_audit import ai_rejection_counts, guard_audit
from probe_code.loader import load_session
from probe_app.models import GuardVerdict
from test_export import make_session


def test_alpha_hand_computed():
    a = {"1": "a", "2": "a", "3": "b", "4": "b"}
    b = {"1": "a", "2": "b", "3": "b", "4": "b"}
    assert alpha_nominal(a, b) == pytest.approx(8 / 15)
    assert alpha_nominal(a, a) == pytest.approx(1.0)


def test_kappa_hand_computed():
    a = {"1": "a", "2": "a", "3": "b", "4": "b"}
    b = {"1": "a", "2": "b", "3": "b", "4": "b"}
    assert cohen_kappa(a, b) == pytest.approx(0.5)


MULTI_A = {"1": frozenset({"x"}), "2": frozenset({"x", "y"}), "3": frozenset({"y"}), "4": frozenset()}
MULTI_B = {"1": frozenset({"x"}), "2": frozenset({"x"}), "3": frozenset({"z"}), "4": frozenset()}


def test_masi_distance_hand_computed():
    assert masi_distance(frozenset({"x"}), frozenset({"x"})) == 0
    assert masi_distance(frozenset(), frozenset()) == 0
    assert masi_distance(frozenset({"x", "y"}), frozenset({"x"})) == pytest.approx(2 / 3)
    assert masi_distance(frozenset({"x", "y"}), frozenset({"y", "z"})) == pytest.approx(1 - (1 / 3) * (1 / 3))
    assert masi_distance(frozenset({"y"}), frozenset({"z"})) == 1
    assert masi_distance(frozenset(), frozenset({"x"})) == 1


def test_alpha_masi_hand_computed():
    # D_o = (0 + 2/3 + 1 + 0) / 4 = 5/12; D_e = (136/3) / (8 * 7) = 17/21 over all ordered pairs of the 8 values.
    assert alpha_masi(MULTI_A, MULTI_B) == pytest.approx(33 / 68)
    assert alpha_masi(MULTI_A, MULTI_A) == pytest.approx(1.0)


def test_alpha_masi_on_single_labels_equals_nominal_alpha():
    a = {"1": "a", "2": "a", "3": "b", "4": "b"}
    b = {"1": "a", "2": "b", "3": "b", "4": "b"}
    as_sets = lambda d: {u: frozenset({v}) for u, v in d.items()}
    assert alpha_masi(as_sets(a), as_sets(b)) == pytest.approx(alpha_nominal(a, b))


def test_alpha_masi_ignores_units_only_one_coder_coded():
    assert alpha_masi({**MULTI_A, "5": frozenset({"x"})}, MULTI_B) == pytest.approx(33 / 68)


def test_per_code_kappa_hand_computed():
    # y: A marks units 2 and 3, B none, p_o = 1/2 = p_e; z: A none, B unit 3, p_o = 3/4 = p_e.
    result = per_code_kappa(MULTI_A, MULTI_B)
    assert list(result) == ["x", "y", "z"]
    assert result["x"] == {"kappa": pytest.approx(1.0), "a": 2, "b": 2, "units": 4}
    assert result["y"]["kappa"] == pytest.approx(0.0) and (result["y"]["a"], result["y"]["b"]) == (2, 0)
    assert result["z"]["kappa"] == pytest.approx(0.0)


def test_per_code_kappa_is_undefined_when_a_code_is_constant():
    every = {"1": frozenset({"x"}), "2": frozenset({"x"})}
    assert math.isnan(per_code_kappa(every, every)["x"]["kappa"])


def test_decoy_and_guess_rates():
    assert decoy_false_rate({"i1": True, "i2": False, "i3": True}, {"i1": True, "i2": True, "i3": False}) == 0.5
    assert guess_rate({"S1": "ai", "S2": "ai"}, {"S1": "ai", "S2": "human"}) == 0.5


def test_corroboration_mixes_decoys_from_other_experts_and_problems(tmp_path):
    ops = [
        {"op_id": "o1", "session_id": "s1", "expert_id": "E01", "problem_id": "A1", "text": "checks limiting case", "source": "ai_probe"},
        {"op_id": "o2", "session_id": "s1", "expert_id": "E01", "problem_id": "A1", "text": "notices sticking", "source": "trace_only"},
        {"op_id": "o3", "session_id": "s2", "expert_id": "E02", "problem_id": "B1", "text": "splits into stages", "source": "trace_only"},
        {"op_id": "o4", "session_id": "s2", "expert_id": "E02", "problem_id": "A1", "text": "same problem other expert", "source": "trace_only"},
    ]
    counts = corroboration_sheet(ops, tmp_path, seed=3)
    sheet = read_csv(tmp_path / "corroboration_sheet.csv")
    key = {r["item_id"]: r for r in read_csv(tmp_path / "corroboration_key.csv")}
    assert counts == {"targets": 1, "decoys": 1, "short": 0}
    decoy = next(r for r in sheet if key[r["item_id"]]["is_decoy"] == "True")
    assert key[decoy["item_id"]]["op_id"] == "o3"
    assert "is_decoy" not in sheet[0] and "op_id" not in sheet[0]


class FlagHuman:
    def check(self, utterance, problem_text, expert_text):
        return GuardVerdict(flagged="HUMAN" in utterance, introduced="x" if "HUMAN" in utterance else "")


def test_guard_audit_covers_both_arms(tmp_path):
    s = load_session(make_session(tmp_path, "E01"))
    rows = guard_audit([s], FlagHuman(), {p: p for p in ("A1", "A2", "B1", "B2")})
    by_arm = {r["arm"]: r["flagged"] for r in rows}
    assert by_arm == {"ai": False, "human": True}


def test_ai_rejection_counts(tmp_path):
    d = make_session(tmp_path, "E01")
    events = [{"type": "probe", "turn": {"source": "ai"}}, {"type": "probe", "turn": {"source": "ai_fallback"}},
              {"type": "turn_rejected", "reason": "leading: it introduces 'units'"},
              {"type": "turn_rejected", "reason": "contract: bad anchor"},
              {"type": "interviewer_failed", "reason": "LLMRefused('interviewer refused')"},
              {"type": "interviewer_failed", "reason": "LLMUnavailable('timeout')"},
              {"type": "interviewer_failed", "reason": "LLMUnavailable('timeout')"},
              {"type": "guard_failed", "set_id": "A", "attempt": 0, "reason": "LLMUnavailable('timeout')"}]
    (d / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    assert ai_rejection_counts(d) == {"accepted": 1, "fallback": 1, "rejected_leading": 1, "rejected_contract": 1,
                                     "interviewer_refused": 1, "interviewer_unavailable": 2,
                                     "guard_failed": 1}


def test_guard_audit_cli_runs_the_configured_guard(tmp_path, monkeypatch, capsys):
    from fakes import TEST_MODELS, FakeAnthropic
    from probe_app.backends import AnthropicBackend
    from probe_code import cli

    built = []

    def fake_make_backend(name, role, env=None):
        built.append((name, role))
        return AnthropicBackend(FakeAnthropic(), TEST_MODELS.guard)

    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: None)
    monkeypatch.setattr(cli, "make_backend", fake_make_backend)
    out = tmp_path / "out"
    cli.main(["guard-audit", str(make_session(tmp_path, "E01")), "--out", str(out), "--allow-drift"])
    assert built == [("guard", TEST_MODELS.guard)]
    assert len(read_csv(out / "guard_audit.csv")) == 2
    assert "ai: 0/1 questions flagged" in capsys.readouterr().out
