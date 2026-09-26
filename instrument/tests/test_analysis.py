import json

import pytest

from probe_code.agreement import alpha_nominal, cohen_kappa, decoy_false_rate, guess_rate
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
              {"type": "interviewer_failed", "reason": "LLMRefused('interviewer refused')"}]
    (d / "events.jsonl").write_text("\n".join(json.dumps(e) for e in events))
    assert ai_rejection_counts(d) == {"accepted": 1, "fallback": 1, "rejected_leading": 1, "rejected_contract": 1,
                                     "interviewer_failed": 1}
