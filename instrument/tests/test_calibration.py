import csv
import json

import pytest

from fakes import FakeAnthropic, FakeResponse
from probe_app.backends import AnthropicBackend
from probe_app.models import GuardVerdict
from probe_code import calibration, cli
from probe_code.export import read_csv
from test_llm import TEST_MODELS


def _items(n_leading=3, n_plain=3):
    rows = []
    for i in range(n_leading + n_plain):
        rows.append({"item_id": f"G{i:02d}", "origin": "variant" if i < n_leading else "original",
                     "style": "explicit" if i < n_leading else "",
                     "problem_ids": "A1", "problems": "A1: a block", "expert_said": "It sticks.",
                     "question": f"question {i}"})
    return rows


def _write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path


def test_labelling_sheet_hides_origin_and_is_shuffled_reproducibly():
    items = _items(5, 5)
    a, b = calibration.labelling_sheet(items, seed=3), calibration.labelling_sheet(items, seed=3)
    assert a == b
    assert "origin" not in a[0]
    assert [r["item_id"] for r in a] != [r["item_id"] for r in items]
    assert {r["leading"] for r in a} == {""}
    assert {r["origin_guess"] for r in a} == {""}


def _cal_items():
    spec = [("original", "")] * 4 + [("variant", "explicit")] * 2 + [("variant", "subtle")] * 2
    return [{"item_id": f"G{n}", "origin": o, "style": s} for n, (o, s) in enumerate(spec)]


def test_report_computes_stratified_sensitivity_specificity_and_labeller_kappa():
    items = _cal_items()
    ids = [r["item_id"] for r in items]
    truth = {"G0": "1", "G1": "0", "G2": "0", "G3": "0", "G4": "1", "G5": "1", "G6": "1", "G7": "0"}
    a = [{"item_id": i, "leading": truth[i], "origin_guess": "authored" if i in ("G4", "G5") else "generated"}
         for i in ids]
    b = [{"item_id": i, "leading": truth[i] if i != "G0" else "0", "origin_guess": "generated"} for i in ids]
    adjudicated = [{"item_id": i, "leading": truth[i]} for i in ids]
    flagged = {"G0": True, "G1": True, "G2": False, "G3": False, "G4": True, "G5": True, "G6": False, "G7": False}
    verdicts = [{"item_id": i, "flagged": str(flagged[i])} for i in ids]
    r = calibration.report(items, a, b, adjudicated, verdicts, min_class=2)
    assert (r.leading, r.not_leading) == (4, 4)
    assert r.sensitivity_by_stratum == {"natural": (1, 1), "explicit": (2, 2), "subtle": (0, 1)}
    assert r.sensitivity_rule == pytest.approx(1 / 2)
    assert r.specificity == pytest.approx(3 / 4)
    assert r.labeller_raw_agreement == pytest.approx(7 / 8)
    assert r.origin_guess_accuracy == pytest.approx(10 / 16)
    assert r.sufficient is True


def test_report_requires_every_item_adjudicated_and_verdicted():
    items = _cal_items()
    full = [{"item_id": r["item_id"], "leading": "0"} for r in items]
    verdicts = [{"item_id": r["item_id"], "flagged": "False"} for r in items]
    with pytest.raises(ValueError, match="G7"):
        calibration.report(items, full, full, full[:-1], verdicts)
    with pytest.raises(ValueError, match="G7"):
        calibration.report(items, full, full, full, verdicts[:-1])


def test_report_marks_small_classes_insufficient():
    items = _cal_items()
    rows = [{"item_id": r["item_id"], "leading": "1" if n < 4 else "0"} for n, r in enumerate(items)]
    verdicts = [{"item_id": r["item_id"], "flagged": "True"} for r in items]
    assert calibration.report(items, rows, rows, rows, verdicts).sufficient is False


def test_run_guard_uses_the_items_context():
    calls = []

    class Guard:
        def check(self, question, problems, said):
            calls.append((question, problems, said))
            return GuardVerdict(flagged=True, introduced="impulse")

    rows = calibration.run_guard(_items(1, 0), Guard())
    assert rows == [{"item_id": "G00", "flagged": True, "introduced": "impulse"}]
    assert calls == [("question 0", "A1: a block", "It sticks.")]


def test_cli_sheet_calibrate_and_report(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: None)
    fake = FakeAnthropic(guard=[FakeResponse({"flagged": n % 2 == 0, "introduced": ""}) for n in range(6)])
    monkeypatch.setattr(cli, "make_backend", lambda name, role, env=None: AnthropicBackend(fake, TEST_MODELS.guard))
    items = _write(tmp_path / "items.csv", _items())
    cli.main(["guard-calibration-sheet", str(items), "--out", str(tmp_path / "sheet.csv"), "--seed", "1"])
    assert len(read_csv(tmp_path / "sheet.csv")) == 6
    cli.main(["guard-calibrate", str(items), "--out", str(tmp_path / "verdicts.csv")])
    verdicts = read_csv(tmp_path / "verdicts.csv")
    assert len(verdicts) == 6
    labels = _write(tmp_path / "labels.csv", [{"item_id": r["item_id"], "leading": "1" if r["origin"] == "variant" else "0"}
                                             for r in _items()])
    cli.main(["calibration-report", str(items), str(labels), str(labels), str(labels), str(tmp_path / "verdicts.csv"),
              "--min-class", "3"])
    out = json.loads(capsys.readouterr().out)
    assert out["leading"] == 3 and out["not_leading"] == 3


def test_committed_items_are_unscreened_and_their_ids_carry_no_origin():
    items = read_csv(calibration.ITEMS_PATH)
    originals = [r for r in items if r["origin"] == "original"]
    assert any(r["frame"] == "rejected" for r in originals), "sample the unaltered half upstream of the guard"
    origins = [r["origin"] for r in sorted(items, key=lambda r: r["item_id"])]
    runs = 1 + sum(a != b for a, b in zip(origins, origins[1:]))
    assert runs > len(items) / 4, "item IDs are grouped by origin; assign them after shuffling"
