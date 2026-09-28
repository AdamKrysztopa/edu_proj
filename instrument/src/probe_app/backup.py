import fcntl
import io
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

from probe_app.config import sha256_file

KEY_ENV = "PROBE_BACKUP_PASSPHRASE"
MANIFEST = "SHA256SUMS"
# LibreSSL (macOS /usr/bin/openssl) and OpenSSL 3 read each other's output with these settings.
CIPHER = ("enc", "-aes-256-cbc", "-pbkdf2", "-iter", "600000", "-md", "sha256")


class BackupFailed(Exception):
    pass


def file_hashes(directory: Path) -> dict[str, str]:
    return {p.relative_to(directory).as_posix(): sha256_file(p)
            for p in sorted(directory.rglob("*")) if p.is_file()}


def _sync(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        # On macOS plain fsync stops at the drive's cache; F_FULLFSYNC asks the drive to flush it.
        fcntl.fcntl(fd, fcntl.F_FULLFSYNC)
    except (AttributeError, OSError):
        os.fsync(fd)
    finally:
        os.close(fd)


def _openssl(key_env: str, *args: str) -> list[str]:
    if not os.environ.get(key_env):
        raise BackupFailed(f"{key_env} is not set: export the backup passphrase in this shell first")
    exe = shutil.which("openssl")
    if exe is None:
        raise BackupFailed("openssl is not on PATH")
    # env: makes openssl read the passphrase from its environment, so it never appears in argv.
    return [exe, *CIPHER, *args, "-pass", f"env:{key_env}"]


def write_archive(session_dir: Path, manifest: dict[str, str], out: Path, key_env: str = KEY_ENV) -> None:
    cmd = _openssl(key_env, "-salt", "-out", str(out))
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        with tarfile.open(fileobj=proc.stdin, mode="w|gz") as tar:
            tar.add(session_dir, arcname=session_dir.name)
            body = "".join(f"{h}  {rel}\n" for rel, h in sorted(manifest.items())).encode()
            info = tarfile.TarInfo(MANIFEST)
            info.size = len(body)
            tar.addfile(info, io.BytesIO(body))
    finally:
        proc.stdin.close()
        err = proc.stderr.read().decode(errors="replace")
        rc = proc.wait()
    if rc != 0:
        raise BackupFailed(f"openssl could not encrypt {session_dir.name}: {err.strip()}")


def _extract(archive: Path, into: Path, key_env: str) -> None:
    proc = subprocess.Popen(_openssl(key_env, "-d", "-in", str(archive)),
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        with tarfile.open(fileobj=proc.stdout, mode="r|gz") as tar:
            tar.extractall(into, filter="data")
    except (tarfile.TarError, EOFError, OSError) as e:
        proc.kill()
        proc.wait()
        raise BackupFailed(f"cannot read {archive.name}: wrong passphrase or damaged archive ({e})") from e
    err = proc.stderr.read().decode(errors="replace")
    if proc.wait() != 0:
        raise BackupFailed(f"cannot decrypt {archive.name}: wrong passphrase or damaged archive ({err.strip()})")


def _verified_session(extracted: Path, archive: Path) -> Path:
    manifest_path = extracted / MANIFEST
    dirs = [p for p in extracted.iterdir() if p.is_dir()]
    if not manifest_path.is_file() or len(dirs) != 1:
        raise BackupFailed(f"{archive.name} is not a session backup")
    manifest = {}
    for line in manifest_path.read_text().splitlines():
        h, rel = line.split("  ", 1)
        manifest[rel] = h
    actual = file_hashes(dirs[0])
    bad = sorted(rel for rel in manifest.keys() | actual.keys() if manifest.get(rel) != actual.get(rel))
    if bad:
        raise BackupFailed(f"{archive.name}: files differ from the archived manifest: {bad}")
    return dirs[0]


def restore(archive: Path, out_dir: Path, key_env: str = KEY_ENV) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=out_dir, prefix=".restore-") as tmp:
        _extract(archive, Path(tmp), key_env)
        session = _verified_session(Path(tmp), archive)
        target = out_dir / session.name
        if target.exists():
            raise BackupFailed(f"{target} exists: restore into an empty directory")
        os.replace(session, target)
    return target


def backup_session(session_dir: Path, dest: Path, key_env: str = KEY_ENV) -> tuple[Path, int]:
    source = file_hashes(session_dir)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out = dest / f"{session_dir.name}-{stamp}.tar.gz.enc"
    partial = out.with_name(out.name + ".partial")
    try:
        write_archive(session_dir, source, partial, key_env)
        _sync(partial)
        with tempfile.TemporaryDirectory() as tmp:
            _extract(partial, Path(tmp), key_env)
            restored = file_hashes(_verified_session(Path(tmp), partial))
        if restored != source:
            raise BackupFailed(f"{session_dir.name}: decrypted copy differs from the session directory")
    except BaseException:
        partial.unlink(missing_ok=True)
        raise
    os.replace(partial, out)
    _sync(dest)
    return out, len(source)


def backup(root: Path, dest: Path, session_ids: list[str], key_env: str = KEY_ENV) -> list[tuple[Path, int]]:
    root, dest = root.resolve(), dest.resolve()
    if dest.is_relative_to(root):
        raise BackupFailed(f"--dest must be outside the sessions root {root}")
    _openssl(key_env)
    if session_ids:
        malformed = [sid for sid in session_ids if not re.fullmatch(r"[A-Za-z0-9_-]+", sid)]
        if malformed:
            raise BackupFailed(f"malformed session id {malformed}")
        dirs = [root / sid for sid in session_ids]
        missing = [d.name for d in dirs if not (d / "manifest.json").is_file()]
        if missing:
            raise BackupFailed(f"no session {missing} under {root}")
    else:
        dirs = [d for d in sorted(root.iterdir()) if (d / "manifest.json").is_file()]
        if not dirs:
            raise BackupFailed(f"no sessions under {root}")
    dest.mkdir(parents=True, exist_ok=True)
    if dest.stat().st_dev == root.stat().st_dev:
        print(f"warning: {dest} is on the same disk as {root}; this copy is lost with the laptop", file=sys.stderr)
    return [backup_session(d, dest, key_env) for d in dirs]
