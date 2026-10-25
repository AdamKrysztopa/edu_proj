"""I7: the pre-registration freeze manifest (finding 13; REORIENTATION.md §14.3). One SHA over the
predictor and gate code, the config values, the closure arms, the area partition and the eligible-gold
list. A run given `--require-manifest <sha>` refuses unless the repository hashes to exactly that.

Files are hashed byte for byte, so even a comment in a hashed file is refused; `config.py` alone is
hashed by value (`config._canonical()`), as `CONFIG_SHA256` already is. The two packages are hashed
as file sets, so a module added to either is caught without being named here.

    uv run --directory gapmap python -m gapmap.manifest --write
    uv run --directory gapmap python -m gapmap.manifest --audit ../research/freeze_manifest/mutation.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import tempfile
import types
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

GAPMAP_PKG = "gapmap/src/gapmap"
CONFIG = f"{GAPMAP_PKG}/config.py"
GAPMAP_OUTSIDE = (CONFIG, f"{GAPMAP_PKG}/render.py")
GAPMAP_REQUIRED = tuple(f"{GAPMAP_PKG}/{m}.py" for m in (
    "lenses", "link", "text", "semantic", "judge", "rank", "record", "checks", "control2", "area", "__main__"))
RESIDUAL_PKG = "residual/src/residual"
RESIDUAL_REQUIRED = tuple(f"{RESIDUAL_PKG}/{m}.py" for m in ("features", "auroc", "baselines"))
CONTROLS = ("research/n3_control_v3/compare.py", "research/n3_control_v3/l73.py",
            "gapmap/tests/l73_fixtures.py", "gapmap/tests/conftest.py")
"""conftest.py builds the ledgers l73_fixtures.py plants into, so it is part of the L7.3 control."""
ADMISSION = "reconstruct/src/reconstruct/admission.py"
FREEZE_DIR = "research/freeze_manifest"
PARTITION = f"{FREEZE_DIR}/area_partition.json"
ELIGIBLE_GOLD = f"{FREEZE_DIR}/eligible_gold.json"
CLOSURE_ARMS = f"{FREEZE_DIR}/closure_arms.json"
"""{"arms": [{"role": "primary" | "guard", "model": str, "reasoning_effort": str | null}, ...]}"""
MANIFEST = f"{FREEZE_DIR}/manifest.json"

_PLACEHOLDERS = {PARTITION: "{}\n", ELIGIBLE_GOLD: "[]\n", CLOSURE_ARMS: '{"arms": []}\n'}


class Refused(RuntimeError):
    pass


def _sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def _sha_json(obj: object) -> str:
    return _sha_bytes(json.dumps(obj, sort_keys=True).encode())


def _package(root: Path, pkg: str, required: tuple[str, ...], outside: tuple[str, ...] = ()) -> list[str]:
    found = {p.relative_to(root).as_posix() for p in (root / pkg).rglob("*.py") if "__pycache__" not in p.parts}
    return sorted((found | set(required)) - set(outside))


def roles(root: Path) -> dict[str, list[str]]:
    return {"gapmap": _package(root, GAPMAP_PKG, GAPMAP_REQUIRED, GAPMAP_OUTSIDE),
            "residual": _package(root, RESIDUAL_PKG, RESIDUAL_REQUIRED),
            "controls": list(CONTROLS), "admission": [ADMISSION], "partition": [PARTITION],
            "eligible_gold": [ELIGIBLE_GOLD], "closure_arms": [CLOSURE_ARMS]}


def _canonical_sha(root: Path) -> str | None:
    path = root / CONFIG
    if not path.exists():
        return None
    # Compiled from source, not imported: an import can load a stale __pycache__ entry when a value
    # edit keeps the file's size and mtime second, and the mutation audit caught exactly that.
    module = types.ModuleType("_gapmap_config_hashed")
    exec(compile(path.read_bytes(), str(path), "exec"), module.__dict__)
    return _sha_json(module._canonical())


def body_sha256(m: dict) -> str:
    return _sha_json({k: m[k] for k in ("roles", "files", "config_canonical_sha256")})


def compute(root: Path | None = None) -> dict:
    root = root or REPO_ROOT
    r = roles(root)
    files = {rel: (_sha_bytes((root / rel).read_bytes()) if (root / rel).is_file() else None)
             for rel in sorted({f for fs in r.values() for f in fs})}
    m = {"roles": r, "files": files, "config_canonical_sha256": _canonical_sha(root)}
    missing = [rel for rel, h in files.items() if h is None]
    if m["config_canonical_sha256"] is None:
        missing.append(CONFIG)
    return {"manifest_sha256": body_sha256(m), "complete": not missing, "missing": missing, **m}


def _changed(root: Path, sha: str, now: dict) -> list[str]:
    path = root / MANIFEST
    if not path.is_file():
        return []
    recorded = json.loads(path.read_text())
    if recorded.get("manifest_sha256") != sha:
        return []
    keys = set(recorded["files"]) | set(now["files"])
    out = sorted(k for k in keys if recorded["files"].get(k) != now["files"].get(k))
    if recorded["config_canonical_sha256"] != now["config_canonical_sha256"]:
        out.append(f"{CONFIG} (values)")
    return out


def _arm_problem(root: Path, model: str, reasoning_effort: str | None) -> str | None:
    try:
        arms = json.loads((root / CLOSURE_ARMS).read_text())["arms"]
        by_role = {a["role"]: a for a in arms}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        return f"{CLOSURE_ARMS} is unreadable: {exc!r}"
    if len(arms) != 2 or set(by_role) != {"primary", "guard"}:
        return f"{CLOSURE_ARMS} must name exactly one primary and one guard arm"
    for a in arms:
        if a["model"] == model and a.get("reasoning_effort") in (None, reasoning_effort):
            return None
    return (f"{model} at reasoning effort {reasoning_effort} is not a registered closure arm "
            f"({', '.join(f'{a['role']}: {a['model']} @ {a.get('reasoning_effort')}' for a in arms)})")


def check(sha: str, root: Path | None = None, *, model: str | None = None,
          reasoning_effort: str | None = None) -> dict:
    """The computed manifest, or `Refused` naming every reason the run may not proceed."""
    root = root or REPO_ROOT
    now = compute(root)
    reasons = []
    if not now["complete"]:
        reasons.append(f"incomplete manifest, missing: {', '.join(now['missing'])}")
    if now["manifest_sha256"] != sha:
        changed = _changed(root, sha, now)
        reasons.append(f"manifest {now['manifest_sha256']} != required {sha}"
                       + (f"; changed: {', '.join(changed)}" if changed else ""))
    if model is not None and (problem := _arm_problem(root, model, reasoning_effort)):
        reasons.append(problem)
    if reasons:
        raise Refused("; ".join(reasons))
    return now


def write(root: Path | None = None) -> Path:
    root = root or REPO_ROOT
    path = root / MANIFEST
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(compute(root), sort_keys=True, indent=1) + "\n")
    return path


def copy_set(src: Path, dst: Path) -> list[str]:
    """Copy every hashed file, `config.py` and `render.py` from `src` to `dst`; write a placeholder
    for each named file `src` lacks. Returns the placeholders."""
    m = compute(src)
    placeholders = []
    for rel in [*m["files"], *GAPMAP_OUTSIDE]:
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if (src / rel).is_file():
            shutil.copyfile(src / rel, target)
        else:
            target.write_text(_PLACEHOLDERS.get(rel, "# placeholder\n"))
            placeholders.append(rel)
    return placeholders


def _flip_one_char(b: bytes) -> bytes:
    i = len(b) // 2
    return b[:i] + (b"y" if b[i:i + 1] == b"x" else b"x") + b[i + 1:]


def _bump_config_value(b: bytes) -> bytes:
    text = b.decode()
    match = re.search(r"^[A-Z_]+ = (\d+)$", text, re.M)
    return (text[:match.start(1)] + str(int(match.group(1)) + 1) + text[match.end(1):]).encode()


def _append_comment(b: bytes) -> bytes:
    return b + b"\n# I7 mutation probe: comment only\n"


def mutation_audit(src: Path | None = None) -> dict:
    """L7.3 for the manifest, on a scratch copy of `src`: one character changed in each hashed file
    in turn, a config value, a new module, a deleted file (all must be refused), and comment-only
    changes outside the set (all must be accepted)."""
    src = src or REPO_ROOT
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        placeholders = copy_set(src, root)
        base = compute(root)["manifest_sha256"]

        def probe(rel: str, change: str, expected: str, mutate) -> dict:
            path = root / rel
            before = path.read_bytes() if path.exists() else None
            mutate(path, before)
            try:
                check(base, root)
                observed = "accepted"
            except Refused:
                observed = "refused"
            if before is None:
                path.unlink()
            else:
                path.write_bytes(before)
            return {"path": rel, "change": change, "expected": expected, "observed": observed}

        def rewrite(f):
            return lambda path, before: path.write_bytes(f(before))

        rows = [probe(rel, "one character", "refused", rewrite(_flip_one_char)) for rel in compute(root)["files"]]
        rows += [
            probe(CONFIG, "config value", "refused", rewrite(_bump_config_value)),
            probe(f"{GAPMAP_PKG}/zz_i7_probe.py", "new module in the package", "refused",
                  lambda path, before: path.write_text("X = 1\n")),
            probe(f"{GAPMAP_PKG}/area.py", "required file deleted", "refused", lambda path, before: path.unlink()),
            probe(CONFIG, "comment only", "accepted", rewrite(_append_comment)),
            probe(f"{GAPMAP_PKG}/render.py", "comment only", "accepted", rewrite(_append_comment)),
        ]
        restored = compute(root)["manifest_sha256"] == base
    return {"placeholders": placeholders, "base_restored": restored, "rows": rows,
            "ok": restored and all(r["observed"] == r["expected"] for r in rows),
            "refused": sum(r["observed"] == "refused" for r in rows if r["expected"] == "refused"),
            "expected_refused": sum(r["expected"] == "refused" for r in rows),
            "accepted": sum(r["observed"] == "accepted" for r in rows if r["expected"] == "accepted"),
            "expected_accepted": sum(r["expected"] == "accepted" for r in rows)}


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(prog="gapmap.manifest")
    p.add_argument("--write", action="store_true", help=f"write {MANIFEST}")
    p.add_argument("--audit", metavar="PATH", help="write the mutation audit (L7.3) to PATH")
    args = p.parse_args(argv)
    if args.write:
        path = write()
        m = json.loads(path.read_text())
        print(f"{m['manifest_sha256']} complete={m['complete']} missing={m['missing']}")
    if args.audit:
        result = mutation_audit()
        Path(args.audit).write_text(json.dumps(result, sort_keys=True, indent=1) + "\n")
        print(f"ok={result['ok']} refused {result['refused']}/{result['expected_refused']}, "
              f"accepted {result['accepted']}/{result['expected_accepted']}")


if __name__ == "__main__":
    main()
