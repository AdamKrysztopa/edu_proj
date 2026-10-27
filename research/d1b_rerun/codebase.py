"""The codebase a targeting test runs on (D1c plan §2). One JSON file names everything that is
codebase-specific; relative paths resolve against that file's directory, which is also where the
test's outputs (pool, fixtures, questions, sealed key) live. `codebase.json` beside this module is
D1b's own, and replays D1b's committed outputs byte for byte."""
from __future__ import annotations

import dataclasses
import glob
import json
from pathlib import Path

D1B_CONFIG = Path(__file__).resolve().parent / "codebase.json"
PLACEHOLDER = "TODO"
# informant-video is E-ABST's private-objective repository (reconstruct/src/reconstruct/eabst.py),
# registered as future validation; edu_proj is this project itself; turbo-design carries Track A
# content (REORIENTATION.md §18.1; owner, 2026-10-27).
EXCLUDED_REPOS = ("AdamKrysztopa/informant-video", "AdamKrysztopa/edu_proj", "AdamKrysztopa/turbo-design")


class Unfilled(ValueError):
    pass


class Excluded(ValueError):
    pass


class Incomplete(ValueError):
    pass


@dataclasses.dataclass(frozen=True)
class Codebase:
    name: str
    title: str
    root: Path
    owner_repo: str
    domain: str
    seed: int
    corpus: Path
    ledgers: dict[str, Path]
    prior_items_path: Path | None
    prior_label: str
    canaries: Path
    canary_mode: str
    allow_incomplete_ledgers: bool = False

    @property
    def pool(self) -> Path:
        return self.root / "pool.json"

    @property
    def review_pack(self) -> Path:
        return self.root / "fixtures" / "topic_review_pack.md"

    @property
    def review(self) -> Path:
        return self.root / "fixtures" / "topic_review.json"

    def ledger_path(self, name: str) -> Path:
        (path,) = glob.glob(str(self.ledgers[name] / "*" / "ledger.json"))
        return Path(path)

    def prior_items(self) -> list[dict]:
        if self.prior_items_path is None:
            return []
        return json.loads(self.prior_items_path.read_text())["items"]


def _placeholders(value, where: str = "") -> list[str]:
    if isinstance(value, str):
        return [where or "(root)"] if PLACEHOLDER in value else []
    if isinstance(value, dict):
        return [p for k, v in value.items() for p in _placeholders(v, f"{where}.{k}".lstrip("."))]
    if isinstance(value, list):
        return [p for i, v in enumerate(value) for p in _placeholders(v, f"{where}[{i}]")]
    return []


def _repo_tail(name: str) -> str:
    name = name.strip().lower().rstrip("/")
    return name[:-4] if name.endswith(".git") else name


def reconstruction_problems(run_dir: Path) -> list[str]:
    """Why a reconstruction run does not count as complete (D1c plan §3.2). The sidecar's own
    `complete` flag means only that no exception or budget stop ended the run: D1's top-tier run
    says complete with 823 calls failed. Failed calls are counted after retries, so a transient
    error that a retry fixed does not count."""
    side = json.loads((Path(run_dir) / "sidecar.json").read_text())
    out = list(side.get("incomplete_reasons") or [])
    if side.get("complete") is not True and not out:
        out.append("sidecar not complete")
    failed = (side.get("stats") or {}).get("failed_calls_by_task") or {}
    out += [f"{task}: {n} failed calls" for task, n in sorted(failed.items()) if n]
    return out


def load(path: Path) -> Codebase:
    path = Path(path).resolve()
    cfg = json.loads(path.read_text())
    unfilled = _placeholders(cfg)
    if unfilled:
        raise Unfilled(f"{path}: {PLACEHOLDER} left in {', '.join(unfilled)}")
    named = [cfg["owner_repo"], cfg.get("corpus_build", {}).get("repo_url", "")]
    hit = [r for r in EXCLUDED_REPOS for n in named if _repo_tail(n).endswith(r.lower())]
    if hit:
        raise Excluded(f"{path}: {hit[0]} is excluded from targeting tests (D1c plan §4, Stop 0)")
    root = path.parent
    rel = lambda p: (root / p).resolve()
    return Codebase(name=cfg["name"], title=cfg["title"], root=root, owner_repo=cfg["owner_repo"],
                    domain=cfg["domain"], seed=int(cfg["seed"]), corpus=rel(cfg["corpus"]),
                    ledgers={k: rel(v) for k, v in cfg["ledgers"].items()},
                    prior_items_path=rel(cfg["prior_items"]) if cfg.get("prior_items") else None,
                    prior_label=cfg.get("prior_label", ""), canaries=rel(cfg["canaries"]),
                    canary_mode=cfg.get("canary_mode", "generated"),
                    allow_incomplete_ledgers=cfg.get("allow_incomplete_ledgers", False) is True)


def require_complete(cb: Codebase, names) -> None:
    """D1c plan §3.2: an incomplete reconstruction never enters a pool, unless the config says so
    (D1b and the dry run reuse D1's ledgers, which are both incomplete, and say why)."""
    if cb.allow_incomplete_ledgers:
        return
    problems = [f"{n}: {p}" for n in names for p in reconstruction_problems(cb.ledger_path(n).parent)]
    if problems:
        raise Incomplete("incomplete ledgers: " + "; ".join(problems))


def d1b() -> Codebase:
    return load(D1B_CONFIG)


replace = dataclasses.replace
