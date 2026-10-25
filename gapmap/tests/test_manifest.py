"""I7: the freeze manifest. Every test hashes a temporary copy of the repository's files, never a
literal SHA, because I2, I5 and I12 change hashed files in parallel."""
import json

import pytest

from gapmap import __main__ as cli
from gapmap import config, control2, manifest

ARMS = {"arms": [{"role": "primary", "model": "gpt-6.1-sol", "reasoning_effort": "high"},
                 {"role": "guard", "model": "guard-placeholder", "reasoning_effort": None}]}


@pytest.fixture
def root(tmp_path):
    manifest.copy_set(manifest.REPO_ROOT, tmp_path)
    (tmp_path / manifest.CLOSURE_ARMS).write_text(json.dumps(ARMS))
    return tmp_path


@pytest.fixture(scope="module")
def audit():
    return manifest.mutation_audit()


def test_config_entry_is_the_value_hash_the_pipeline_already_records():
    assert manifest.compute()["config_canonical_sha256"] == config.CONFIG_SHA256


def test_a_complete_copy_passes_its_own_sha(root):
    m = manifest.compute(root)
    assert m["complete"] and not m["missing"]
    manifest.check(m["manifest_sha256"], root)


def test_the_hashed_set_holds_every_named_file(root):
    files = set(manifest.compute(root)["files"])
    named = {*manifest.GAPMAP_REQUIRED, *manifest.RESIDUAL_REQUIRED, *manifest.CONTROLS,
             manifest.ADMISSION, manifest.PARTITION, manifest.ELIGIBLE_GOLD, manifest.CLOSURE_ARMS}
    assert named <= files
    assert manifest.CONFIG not in files
    assert f"{manifest.GAPMAP_PKG}/render.py" not in files


def test_one_character_changed_in_any_hashed_file_is_refused(audit):
    hashed = [r for r in audit["rows"] if r["change"] == "one character"]
    assert {r["path"] for r in hashed} >= {*manifest.GAPMAP_REQUIRED, *manifest.RESIDUAL_REQUIRED}
    assert all(r["observed"] == "refused" for r in hashed), [r for r in hashed if r["observed"] != "refused"]


def test_structural_and_value_changes_are_refused(audit):
    rows = {r["change"]: r for r in audit["rows"] if r["change"] != "one character"}
    for change in ("config value", "new module in the package", "required file deleted"):
        assert rows[change]["observed"] == "refused", change


def test_comment_only_changes_outside_the_set_are_accepted(audit):
    outside = [r for r in audit["rows"] if r["expected"] == "accepted"]
    assert {r["path"] for r in outside} >= {f"{manifest.GAPMAP_PKG}/render.py", manifest.CONFIG}
    assert all(r["observed"] == "accepted" for r in outside), outside


def test_the_audit_restores_its_copy_between_probes(audit):
    assert audit["ok"] and audit["base_restored"]


def test_a_missing_file_is_refused_even_when_the_sha_matches(tmp_path):
    manifest.copy_set(manifest.REPO_ROOT, tmp_path)
    (tmp_path / manifest.ELIGIBLE_GOLD).unlink()
    m = manifest.compute(tmp_path)
    assert manifest.ELIGIBLE_GOLD in m["missing"]
    with pytest.raises(manifest.Refused, match="incomplete"):
        manifest.check(m["manifest_sha256"], tmp_path)


def test_a_mismatch_names_the_changed_file_from_the_recorded_manifest(root):
    manifest.write(root)
    sha = manifest.compute(root)["manifest_sha256"]
    path = root / manifest.GAPMAP_PKG / "lenses.py"
    path.write_text(path.read_text() + "\n")
    with pytest.raises(manifest.Refused, match="lenses.py"):
        manifest.check(sha, root)


def test_the_recorded_manifest_hashes_to_its_own_sha(root):
    recorded = json.loads(manifest.write(root).read_text())
    assert manifest.body_sha256(recorded) == recorded["manifest_sha256"]


@pytest.mark.parametrize("model,effort,ok", [
    ("gpt-6.1-sol", "high", True),
    ("guard-placeholder", None, True),
    ("gpt-6.1-sol", "medium", False),
    ("qwen2.5:7b-instruct", None, False),
])
def test_only_a_registered_closure_arm_may_run(root, model, effort, ok):
    sha = manifest.compute(root)["manifest_sha256"]
    if ok:
        manifest.check(sha, root, model=model, reasoning_effort=effort)
    else:
        with pytest.raises(manifest.Refused, match="closure arm"):
            manifest.check(sha, root, model=model, reasoning_effort=effort)


def test_an_arms_file_without_both_roles_is_refused(root):
    (root / manifest.CLOSURE_ARMS).write_text(json.dumps({"arms": ARMS["arms"][:1]}))
    sha = manifest.compute(root)["manifest_sha256"]
    with pytest.raises(manifest.Refused, match="one primary and one guard"):
        manifest.check(sha, root, model="gpt-6.1-sol", reasoning_effort="high")


def test_the_gapmap_cli_refuses_before_reading_the_ledger(tmp_path):
    with pytest.raises(SystemExit):
        cli.main(["--ledger", str(tmp_path / "absent.json"), "--domain", "d", "--out", str(tmp_path),
                  "--require-manifest", "0" * 64])
    assert not (tmp_path / "gapmap.json").exists()


def test_the_control2_cli_refuses_before_reading_the_ledger(tmp_path):
    with pytest.raises(SystemExit):
        control2.main(["--ledger", str(tmp_path / "absent.json"), "--domain", "d", "--out", str(tmp_path),
                       "--require-manifest", "0" * 64])
    assert not (tmp_path / "control2.json").exists()


def test_the_cli_runs_past_the_check_when_the_manifest_holds(root, monkeypatch, tmp_path):
    sha = manifest.compute(root)["manifest_sha256"]
    monkeypatch.setattr(manifest, "REPO_ROOT", root)
    with pytest.raises(FileNotFoundError):
        control2.main(["--ledger", str(tmp_path / "absent.json"), "--domain", "d", "--out", str(tmp_path),
                       "--model", "gpt-6.1-sol", "--reasoning-effort", "high", "--require-manifest", sha])
