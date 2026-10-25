import hashlib
import json
import subprocess
import sys

import pytest

from residual.presence import count_items, presence

SECRET = "palpate the cricothyroid membrane"


def test_csv_counts_data_rows_after_the_header(tmp_path):
    p = tmp_path / "gold.csv"
    p.write_text("item,type\nstep one,action\n\nstep two,decision\n")
    assert count_items(p) == 2


def test_json_counts_list_items_and_refuses_an_object(tmp_path):
    p = tmp_path / "gold.json"
    p.write_text(json.dumps([{"item": "a"}, {"item": "b"}, {"item": "c"}]))
    assert count_items(p) == 3
    p.write_text(json.dumps({"items": []}))
    with pytest.raises(ValueError):
        count_items(p)


def test_absent_and_empty_lists_are_not_present(tmp_path):
    assert presence(tmp_path / "missing.csv") == "list absent"
    empty = tmp_path / "empty.csv"
    empty.write_text("item,type\n")
    assert presence(empty) == "list empty"


def test_output_carries_count_and_hash_but_no_item_text(tmp_path):
    p = tmp_path / "gold.txt"
    p.write_text(f"{SECRET}\nsecure the airway\n")
    out = subprocess.run([sys.executable, "-m", "residual.presence", str(p)],
                         capture_output=True, text=True)
    assert out.returncode == 0
    assert out.stdout.strip() == f"list present, 2 rows, sha256 {hashlib.sha256(p.read_bytes()).hexdigest()}"
    assert SECRET not in out.stdout + out.stderr


def test_a_missing_list_exits_nonzero(tmp_path):
    out = subprocess.run([sys.executable, "-m", "residual.presence", str(tmp_path / "none.csv")],
                         capture_output=True, text=True)
    assert out.returncode == 1 and out.stdout.strip() == "list absent"


@pytest.mark.parametrize("name,body", [("bad.json", b'{"items": [' + SECRET.encode()),
                                       ("obj.json", json.dumps({"x": SECRET}).encode()),
                                       ("binary.txt", b"\xff\xfe" + SECRET.encode("utf-16-le"))])
def test_unreadable_lists_name_the_error_type_only(tmp_path, name, body):
    p = tmp_path / name
    p.write_bytes(body)
    out = subprocess.run([sys.executable, "-m", "residual.presence", str(p)],
                         capture_output=True, text=True)
    assert out.returncode == 1 and out.stdout.startswith("list unreadable (")
    assert SECRET not in out.stdout + out.stderr and "Traceback" not in out.stderr


def test_no_argument_prints_usage():
    out = subprocess.run([sys.executable, "-m", "residual.presence"], capture_output=True, text=True)
    assert out.returncode == 2 and out.stdout.startswith("usage:")
