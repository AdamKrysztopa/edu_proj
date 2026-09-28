import json
import subprocess

import pytest

from probe_app import backup, cli
from probe_app.config import sha256_file

PASSPHRASE = "correct horse battery staple"
SECRET_SPEECH = b"the expert said something confidential"


def fake_session(root, sid):
    d = root / sid
    (d / "audio").mkdir(parents=True)
    (d / "llm").mkdir()
    (d / "manifest.json").write_text(json.dumps({"expert_id": sid.split("-")[0]}))
    (d / "audio" / "think_A1.part1.webm").write_bytes(SECRET_SPEECH)
    (d / "llm" / "0001.json").write_text('{"kind": "interviewer"}')
    return d


def hashes(d):
    return {p.relative_to(d).as_posix(): sha256_file(p) for p in d.rglob("*") if p.is_file()}


@pytest.fixture
def root(tmp_path):
    r = tmp_path / "sessions"
    fake_session(r, "E01-aa")
    fake_session(r, "E02-bb")
    (r / "not-a-session").mkdir()
    return r


@pytest.fixture
def key(monkeypatch):
    monkeypatch.setenv(backup.KEY_ENV, PASSPHRASE)


def test_backup_is_encrypted_and_restores_every_file(root, tmp_path, key, capsys):
    dest, out = tmp_path / "drive", tmp_path / "restored"
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(dest)])
    [archive] = dest.iterdir()
    assert archive.name.startswith("E01-aa-") and archive.name.endswith(".tar.gz.enc")
    assert SECRET_SPEECH not in archive.read_bytes()
    assert "verified" in capsys.readouterr().out
    cli.main(["restore", str(archive), "--out", str(out)])
    assert hashes(out / "E01-aa") == hashes(root / "E01-aa")


def test_backup_without_session_ids_covers_every_session(root, tmp_path, key):
    dest = tmp_path / "drive"
    cli.main(["backup", "--root", str(root), "--dest", str(dest)])
    assert sorted(p.name.split("-")[0] for p in dest.iterdir()) == ["E01", "E02"]


def test_backup_refuses_without_the_passphrase(root, tmp_path, monkeypatch):
    monkeypatch.delenv(backup.KEY_ENV, raising=False)
    with pytest.raises(backup.BackupFailed, match=backup.KEY_ENV):
        cli.main(["backup", "--root", str(root), "--dest", str(tmp_path / "drive")])
    assert not (tmp_path / "drive").exists() or not any((tmp_path / "drive").iterdir())


def test_passphrase_is_never_read_from_the_dotenv_file(root, tmp_path, monkeypatch):
    monkeypatch.delenv(backup.KEY_ENV, raising=False)
    monkeypatch.setattr(cli, "load_dotenv", lambda *a, **k: monkeypatch.setenv(backup.KEY_ENV, PASSPHRASE))
    with pytest.raises(backup.BackupFailed, match=backup.KEY_ENV):
        cli.main(["backup", "--root", str(root), "--dest", str(tmp_path / "drive")])


def test_passphrase_never_reaches_a_command_line_or_the_output(root, tmp_path, key, monkeypatch, capsys):
    argv = []
    real = subprocess.Popen

    def spy(args, *a, **k):
        argv.append(args)
        return real(args, *a, **k)

    monkeypatch.setattr(backup.subprocess, "Popen", spy)
    dest = tmp_path / "drive"
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(dest)])
    cli.main(["restore", str(next(dest.iterdir())), "--out", str(tmp_path / "restored")])
    assert argv and not any(PASSPHRASE in " ".join(map(str, a)) for a in argv)
    captured = capsys.readouterr()
    assert PASSPHRASE not in captured.out + captured.err


def test_restore_with_the_wrong_passphrase_fails_and_leaves_nothing(root, tmp_path, key, monkeypatch):
    dest, out = tmp_path / "drive", tmp_path / "restored"
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(dest)])
    monkeypatch.setenv(backup.KEY_ENV, "wrong")
    with pytest.raises(backup.BackupFailed):
        cli.main(["restore", str(next(dest.iterdir())), "--out", str(out)])
    assert not (out / "E01-aa").exists()


def test_restore_detects_a_damaged_archive(root, tmp_path, key):
    dest, out = tmp_path / "drive", tmp_path / "restored"
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(dest)])
    archive = next(dest.iterdir())
    data = archive.read_bytes()
    archive.write_bytes(data[: len(data) // 2])
    with pytest.raises(backup.BackupFailed):
        cli.main(["restore", str(archive), "--out", str(out)])
    assert not (out / "E01-aa").exists()


def test_restore_checks_files_against_the_archived_manifest(root, tmp_path, key):
    archive, out = tmp_path / "bad.tar.gz.enc", tmp_path / "restored"
    manifest = {**backup.file_hashes(root / "E01-aa"), "audio/think_A1.part1.webm": "0" * 64}
    backup.write_archive(root / "E01-aa", manifest, archive, backup.KEY_ENV)
    with pytest.raises(backup.BackupFailed, match="think_A1"):
        cli.main(["restore", str(archive), "--out", str(out)])
    assert not (out / "E01-aa").exists()


def test_archive_reaches_the_disk_before_it_is_verified(root, tmp_path, key, monkeypatch):
    events = []
    real_sync, real_extract = backup._sync, backup._extract
    monkeypatch.setattr(backup, "_sync", lambda p: (events.append(("sync", p.name)), real_sync(p)))
    monkeypatch.setattr(backup, "_extract", lambda a, i, k: (events.append(("verify", a.name)), real_extract(a, i, k)))
    dest = tmp_path / "drive"
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(dest)])
    [archive] = dest.iterdir()
    partial = archive.name + ".partial"
    assert events.index(("sync", partial)) < events.index(("verify", partial))
    assert events[-1] == ("sync", "drive")


def test_backup_warns_when_the_destination_shares_the_sessions_disk(root, tmp_path, key, capsys):
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(tmp_path / "drive")])
    assert "same disk" in capsys.readouterr().err


def test_backup_refuses_a_destination_inside_the_sessions_root(root, key):
    with pytest.raises(backup.BackupFailed, match="outside"):
        cli.main(["backup", "--root", str(root), "--dest", str(root / "copies")])


def test_restore_refuses_to_overwrite_a_session(root, tmp_path, key):
    dest = tmp_path / "drive"
    cli.main(["backup", "E01-aa", "--root", str(root), "--dest", str(dest)])
    with pytest.raises(backup.BackupFailed, match="exists"):
        cli.main(["restore", str(next(dest.iterdir())), "--out", str(root)])
