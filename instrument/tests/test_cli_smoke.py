import csv
import json

import pytest

from fakes import FakeAnthropic, FakeResponse, FakeTranscriber, fake_backends, turn_payload
from probe_app import cli as app_cli
from probe_app.config import INSTRUMENT_DIR
from probe_app.models import STEMS
from probe_app.transcribe import RawSegment
from probe_code import cli as code_cli
from probe_code.export import read_csv
from test_export import make_session


@pytest.fixture(autouse=True)
def no_dotenv(monkeypatch):
    monkeypatch.setattr(app_cli, "load_dotenv", lambda *a, **k: None)
    monkeypatch.setattr(code_cli, "load_dotenv", lambda *a, **k: None)


def write_rows(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return str(path)


def test_transcribe_prints_the_segmented_transcript(tmp_path, monkeypatch, capsys):
    import probe_app.transcribe as transcribe

    chosen = []

    def fake_make_transcriber(model=None, client=None):
        chosen.append(model)
        return FakeTranscriber([[RawSegment(start=0.0, end=1.5, text="Momentum is conserved.")]])

    monkeypatch.setattr(transcribe, "make_transcriber", fake_make_transcriber)
    audio = tmp_path / "think_A1.webm"
    audio.write_bytes(b"x")
    app_cli.main(["transcribe", str(audio), "--model", "whisper-1"])
    assert chosen == ["whisper-1"]
    assert capsys.readouterr().out.strip() == "[X-s001 0.0-1.5s] Momentum is conserved."


class ScriptedExpert:
    def complete(self, kind, system, parts, schema, max_tokens, log, thinking=False):
        return " I checked the limiting case. "


def test_simulate_runs_a_session_with_fake_models(tmp_path, monkeypatch, capsys):
    import probe_app.backends as backends

    turns = []
    for pids in (["A1", "A2"], ["B1", "B2"]):
        turns += [FakeResponse(turn_payload(problem_id=p, stem_id=s)) for p in pids for s in STEMS]
        turns.append(FakeResponse(turn_payload(problem_id=pids[0], end_session=True)))
    monkeypatch.setattr(backends, "make_backend", lambda name, role, env=None: ScriptedExpert())
    monkeypatch.setattr(backends, "make_backends", lambda models, env=None: fake_backends(FakeAnthropic(interviewer=turns)))
    app_cli.main(["simulate", "--root", str(tmp_path)])
    [session] = [d for d in tmp_path.iterdir() if d.is_dir()]
    assert str(session) in capsys.readouterr().out
    state = json.loads((session / "state.json").read_text())
    assert state["phase"] == "done"
    assert state["dialogue"]["A"][1]["text"] == "I checked the limiting case."


def test_export_blind_writes_units_and_a_separate_key(tmp_path):
    out = tmp_path / "blind"
    code_cli.main(["export-blind", str(make_session(tmp_path, "E01")), "--out", str(out), "--seed", "1"])
    units = read_csv(out / "coder_units.csv")
    assert units and all("SECRET" not in v for r in units for v in r.values())
    assert read_csv(out / "key_units.csv")


def test_export_trace_writes_units_and_a_key(tmp_path):
    out = tmp_path / "trace"
    code_cli.main(["export-trace", str(make_session(tmp_path, "E01")), "--out", str(out)])
    assert [r["text"] for r in read_csv(out / "trace_units.csv")] == ["Energy first."]
    assert read_csv(out / "key_trace.csv")


def test_corroboration_prints_counts(tmp_path, capsys):
    ops = [{"op_id": "o1", "session_id": "s1", "expert_id": "E01", "problem_id": "A1", "text": "limit", "source": "ai_probe"},
           {"op_id": "o2", "session_id": "s2", "expert_id": "E02", "problem_id": "B1", "text": "stages", "source": "trace_only"}]
    out = tmp_path / "corr"
    code_cli.main(["corroboration", write_rows(tmp_path / "ops.csv", ops), "--out", str(out)])
    assert "'targets': 1" in capsys.readouterr().out
    assert (out / "corroboration_sheet.csv").exists()


def test_agreement_commands_print_the_coefficient(tmp_path, capsys):
    a = write_rows(tmp_path / "a.csv", [{"unit_id": u, "label": l} for u, l in zip("1234", "aabb")])
    b = write_rows(tmp_path / "b.csv", [{"unit_id": u, "label": l} for u, l in zip("1234", "abbb")])
    code_cli.main(["alpha", a, b])
    code_cli.main(["kappa", a, b])
    assert capsys.readouterr().out.split() == ["0.533", "0.500"]


CODEBOOK = """# Codebook

## Type (map §9 Phase 1 taxonomy)

| Type | Definition | Include | Exclude | Example (from pilots) |
|---|---|---|---|---|
| X | | | | |
| Y | | | | |
| Z | | | | |

## Source
"""


def codebook(tmp_path):
    p = tmp_path / "codebook.md"
    p.write_text(CODEBOOK)
    return str(p)


def multi_label_files(tmp_path):
    a = write_rows(tmp_path / "a.csv", [{"unit_id": u, "label": l}
                                        for u, l in zip("12345", ["X", "x; Y", "y", "None", ""])])
    b = write_rows(tmp_path / "b.csv", [{"unit_id": u, "label": l} for u, l in zip("1234", ["X", "X", "Z", "none"])])
    return a, b


def test_codebook_types_are_read_from_the_type_table():
    assert code_cli.codebook_types(INSTRUMENT_DIR / "codebook" / "v0.md")[:2] == ["Omitted prerequisite", "Perceptual cue"]


def test_multi_label_alpha_uses_masi(tmp_path, capsys):
    a, b = multi_label_files(tmp_path)
    code_cli.main(["alpha", a, b, "--multi", "--codebook", codebook(tmp_path)])
    assert capsys.readouterr().out.strip() == "0.485 (4 of 5 units coded by both; left blank or missing: A 1, B 1)"


def test_multi_label_kappa_reports_each_code(tmp_path, capsys):
    a, b = multi_label_files(tmp_path)
    code_cli.main(["kappa", a, b, "--multi", "--codebook", codebook(tmp_path)])
    assert capsys.readouterr().out.splitlines() == [
        "4 of 5 units coded by both; left blank or missing: A 1, B 1",
        "X: 1.000 (present: A 2, B 2 of 4 units)",
        "Y: 0.000 (present: A 2, B 0 of 4 units)",
        "Z: 0.000 (present: A 0, B 1 of 4 units)",
    ]


@pytest.mark.parametrize("rows, match", [
    ([{"unit_id": "1", "label": "X"}, {"unit_id": "1", "label": "Y"}], "unit 1"),
    ([{"unit_id": "1", "label": ""}, {"unit_id": "1", "label": "Y"}], "unit 1"),
    ([{"unit_id": "1", "label": "none; X"}, {"unit_id": "2", "label": "X"}], "none"),
    ([{"unit_id": "1", "label": "X; Perceptual cue"}, {"unit_id": "2", "label": "X"}], "Perceptual cue"),
    ([{"unit_id": "1", "label": "X"}, {"unit_id": "2", "label": ""}], "fewer than 2"),
])
def test_multi_label_file_errors_are_refused(tmp_path, rows, match):
    a = write_rows(tmp_path / "a.csv", rows)
    with pytest.raises(ValueError, match=match):
        code_cli.main(["kappa", a, a, "--multi", "--codebook", codebook(tmp_path)])


def test_decoys_prints_the_false_corroboration_rate(tmp_path, capsys):
    judgments = write_rows(tmp_path / "j.csv", [{"item_id": "i1", "corroborated": "yes"},
                                                {"item_id": "i2", "corroborated": "no"}])
    key = write_rows(tmp_path / "k.csv", [{"item_id": "i1", "is_decoy": "True"}, {"item_id": "i2", "is_decoy": "True"}])
    code_cli.main(["decoys", judgments, key])
    assert capsys.readouterr().out.strip() == "false corroboration on decoys: 0.500"


def test_guesses_prints_the_guess_rate(tmp_path, capsys):
    guesses = write_rows(tmp_path / "g.csv", [{"blind_session": "S1", "arm": "ai"}, {"blind_session": "S2", "arm": "ai"}])
    key = write_rows(tmp_path / "k.csv", [{"blind_session": "S1", "arm": "ai"}, {"blind_session": "S2", "arm": "human"}])
    code_cli.main(["guesses", guesses, key])
    assert capsys.readouterr().out.strip() == "condition guessed correctly: 0.500 (chance 0.5)"
