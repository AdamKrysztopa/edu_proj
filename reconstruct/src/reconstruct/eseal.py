"""N8 E-SEAL: sealed closed-book forecasts of the Stage A operations (plan: docs/plans/n8-e-seal.md).

    uv run --directory reconstruct python -m reconstruct.eseal dry-run --live --max-usd 0.25
    uv run --directory reconstruct python -m reconstruct.eseal seal --live --max-usd 0.75 \
        --provider-logging-off
    uv run --directory reconstruct python -m reconstruct.eseal unseal --private-key KEY --k1-lock FILE --out DIR

`dry-run` sends one non-conservation problem to every arm and keeps only whether each reply fits
the schema. `seal` sends each Stage A problem statement (never its answer) to every arm, holds the
replies in memory only, and encrypts them in one piece under the public key named by
E_SEAL_PUBLIC_KEY: plaintext reaches openssl only on stdin and is never written, printed or logged.
Anyone who sees it becomes ineligible for every Track A human role (REORIENTATION.md §18.1).
`unseal` opens it only after the K1 adjudication record is committed, and only outside the repo.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import secrets
import subprocess
import sys
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Callable, Mapping

import openai

from reconstruct.llm import OPENROUTER_API_KEY_ENV, OPENROUTER_URL, CallLog, OpenRouterBackend

ROOT = Path(__file__).resolve().parents[3]
HERE = ROOT / "research" / "n8_eseal"
DEFAULT_PROBLEMS = ROOT / "instrument" / "problems" / "problems.json"
DEFAULT_PLAN = ROOT / "docs" / "plans" / "n8-e-seal.md"
KEY_HEADROOM = ROOT / "scripts" / "key_headroom.py"
PROMPTS = Path(__file__).parent / "prompts"
SYSTEM_PROMPT = (PROMPTS / "eseal_system.md").read_text()
USER_TEMPLATE = (PROMPTS / "eseal_user.md").read_text()
PUBLIC_KEY_ENV = "E_SEAL_PUBLIC_KEY"
MIN_RSA_BITS = 3072
MIN_HEADROOM_USD = 10.0  # L7.1
MAX_OPS = 12
MAX_TOKENS = 8192  # fixed by OpenRouterBackend.complete_json
PROMPT_OVERHEAD_TOKENS = 200


@dataclass(frozen=True)
class Arm:
    name: str
    model: str
    family: str


ARMS = (Arm("top_tier", "anthropic/claude-opus-5.5", "anthropic"),
        Arm("other_family", "openai/gpt-6.1-sol", "openai"),
        Arm("cheap", "anthropic/claude-haiku-4.5", "anthropic"))
# USD per 1M (input, output) tokens, https://openrouter.ai/api/v1/models, read 2026-10-27.
PRICES_PER_MTOK = {"anthropic/claude-opus-5.5": (4.0, 20.0), "openai/gpt-6.1-sol": (2.0, 10.0),
                   "anthropic/claude-haiku-4.5": (1.0, 5.0)}

OP_TYPES = ["cue", "decision", "representation", "check", "heuristic"]
SCHEMA = {
    "type": "object", "additionalProperties": False, "required": ["operations"],
    "properties": {"operations": {"type": "array", "items": {
        "type": "object", "additionalProperties": False,
        "required": ["statement", "trigger", "type", "p_omitted"],
        "properties": {"statement": {"type": "string"}, "trigger": {"type": "string"},
                       "type": {"type": "string", "enum": OP_TYPES}, "p_omitted": {"type": "number"}}}}},
}
ENC = ("enc", "-aes-256-cbc", "-pbkdf2", "-iter", "600000", "-md", "sha256", "-salt", "-pass", "stdin")
WRAP = ("-pkeyopt", "rsa_padding_mode:oaep", "-pkeyopt", "rsa_oaep_md:sha256")


class SealError(Exception):
    """Messages are written by this module and never carry forecast content."""


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _hashes() -> dict:
    return {"system_prompt_sha256": _sha(SYSTEM_PROMPT.encode()),
            "user_template_sha256": _sha(USER_TEMPLATE.encode()),
            "schema_sha256": _sha(json.dumps(SCHEMA, sort_keys=True).encode())}


def _openssl(args: list[str] | tuple[str, ...], data: bytes = b"") -> bytes:
    # stderr is dropped unread: the message must stay content-free whatever openssl says.
    r = subprocess.run(["openssl", *args], input=data, capture_output=True)
    if r.returncode != 0:
        raise SealError(f"openssl {args[0]} failed (exit {r.returncode})")
    return r.stdout


def check_public_key(path: Path) -> None:
    try:
        text = _openssl(["pkey", "-pubin", "-in", str(path), "-noout", "-text"]).decode()
    except SealError:
        raise SealError(f"{PUBLIC_KEY_ENV} does not name a readable PEM public key") from None
    bits = re.search(r"\((\d+) bit\)", text)
    if "Modulus" not in text or not bits:
        raise SealError(f"{PUBLIC_KEY_ENV} is not an RSA public key")
    if int(bits.group(1)) < MIN_RSA_BITS:
        raise SealError(f"{PUBLIC_KEY_ENV} is a {bits.group(1)}-bit key; at least {MIN_RSA_BITS} is required")


def seal_bytes(plaintext: bytes, public_key: Path, dest: Path) -> dict:
    sym = secrets.token_hex(32).encode()
    enc = _openssl(ENC, sym + b"\n" + plaintext)
    wrapped = _openssl(["pkeyutl", "-encrypt", "-pubin", "-inkey", str(public_key), *WRAP], sym)
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "forecast.enc").write_bytes(enc)
    (dest / "key.enc").write_bytes(wrapped)
    return {"forecast_enc_sha256": _sha(enc), "key_enc_sha256": _sha(wrapped),
            "public_key_sha256": _sha(public_key.read_bytes()), "plaintext_sha256": _sha(plaintext)}


def unseal_bytes(sealed: Path, private_key: Path) -> bytes:
    m = json.loads((sealed / "manifest.json").read_text())
    enc, wrapped = (sealed / "forecast.enc").read_bytes(), (sealed / "key.enc").read_bytes()
    if _sha(enc) != m["forecast_enc_sha256"] or _sha(wrapped) != m["key_enc_sha256"]:
        raise SealError("ciphertext does not match the manifest's hashes")
    sym = _openssl(["pkeyutl", "-decrypt", "-inkey", str(private_key), *WRAP], wrapped)
    plain = _openssl([ENC[0], "-d", *ENC[1:]], sym + b"\n" + enc)
    if _sha(plain) != m["plaintext_sha256"]:
        raise SealError("decrypted forecast does not match the committed plaintext hash")
    return plain


def schema_ok(data: dict) -> bool:
    ops = data.get("operations")
    if not isinstance(ops, list) or not 0 < len(ops) <= MAX_OPS:
        return False
    return all(isinstance(o, dict) and set(o) == {"statement", "trigger", "type", "p_omitted"}
               and isinstance(o["statement"], str) and o["statement"].strip() and isinstance(o["trigger"], str)
               and o["type"] in OP_TYPES and isinstance(o["p_omitted"], (int, float))
               and 0 <= o["p_omitted"] <= 1 for o in ops)


def worst_case_usd(model: str, user: str) -> float:
    pin, pout = PRICES_PER_MTOK[model]
    # A token covers at least one byte, so bytes bound tokens from above.
    tokens_in = (len(SYSTEM_PROMPT.encode()) + len(user.encode()) + len(json.dumps(SCHEMA))
                 + PROMPT_OVERHEAD_TOKENS)
    return (tokens_in * pin + MAX_TOKENS * pout) / 1e6


def _call_cost(lines: list[dict], model: str) -> float:
    pin, pout = PRICES_PER_MTOK[model]
    return sum(r["cost"] if r["cost"] is not None else
               ((r["input_tokens"] or 0) * pin + (r["output_tokens"] or 0) * pout) / 1e6 for r in lines)


def _log_lines(log: CallLog) -> list[dict]:
    return [json.loads(x) for x in log.path.read_text().splitlines()] if log.path.exists() else []


def _run_calls(items: list[tuple[str, str]], *, max_usd: float, log: CallLog, key: str,
               client_factory: Callable[[str, str], Any]) -> tuple[float, list[dict], dict]:
    """Every arm on every (id, statement). Replies stay in the returned dict and nowhere else."""
    spent, calls, replies = 0.0, [], {a.name: {} for a in ARMS}
    for arm in ARMS:
        backend = OpenRouterBackend(client=client_factory("openrouter", key), model_id=arm.model,
                                    family=arm.family, role=f"eseal_{arm.name}", log=log)
        for pid, statement in items:
            user = USER_TEMPLATE.format(statement=statement)
            wc = worst_case_usd(arm.model, user)
            rec = {"arm": arm.name, "model": arm.model, "problem": pid, "spent_before_usd": round(spent, 6),
                   "worst_case_usd": round(wc, 6)}
            if spent + wc > max_usd:
                calls.append({**rec, "outcome": "refused_cap"})
                continue
            n_before = len(_log_lines(log))
            try:
                data = backend.complete_json(f"eseal_{pid}", SYSTEM_PROMPT, user, SCHEMA)
                rec.update(outcome="ok", schema_ok=schema_ok(data))
                replies[arm.name][pid] = data
            except Exception as e:  # noqa: BLE001 — the class is recorded, the message never is
                rec.update(outcome="error", error_class=type(e).__name__)
            new = _log_lines(log)[n_before:]
            cost = _call_cost(new, arm.model)
            spent += cost
            calls.append({**rec, "log_outcomes": [r["outcome"] for r in new],
                          "input_tokens": sum(r["input_tokens"] or 0 for r in new),
                          "output_tokens": sum(r["output_tokens"] or 0 for r in new), "cost_usd": round(cost, 6)})
            data = None
    return spent, calls, replies


def _common_preflight(args, env: Mapping[str, str]) -> str:
    if not args.live:
        raise SealError("refusing to call any model without --live")
    if "OPENAI_LOG" in env:
        raise SealError("OPENAI_LOG is set: the SDK would log response bodies; unset it")
    if not env.get(OPENROUTER_API_KEY_ENV):
        raise SealError(f"{OPENROUTER_API_KEY_ENV} is not set")
    if args.out.exists() and any(args.out.iterdir()):
        raise SealError(f"{args.out} is not empty; a run never overwrites another")
    return env[OPENROUTER_API_KEY_ENV]


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _committed(repo: Path, path: Path, what: str) -> str:
    """The commit that last touched `path`, which must be tracked and unchanged."""
    rel = str(path.resolve().relative_to(repo.resolve()))
    if _git(repo, "ls-files", "--error-unmatch", rel).returncode != 0:
        raise SealError(f"{what} is not committed")
    if _git(repo, "diff", "--quiet", "HEAD", "--", rel).returncode != 0:
        raise SealError(f"{what} differs from its committed version")
    return _git(repo, "log", "-1", "--format=%H", "--", rel).stdout.strip()


def measured_headroom(env: Mapping[str, str]) -> str:
    """scripts/key_headroom.py's own line (limit fields only, never the key); refuses below the L7.1 floor."""
    r = subprocess.run([sys.executable, str(KEY_HEADROOM), "--need", str(MIN_HEADROOM_USD)], env=dict(env),
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SealError(f"key headroom is below ${MIN_HEADROOM_USD} or could not be read (L7.1)")
    return r.stdout.strip()


def _print_summary(manifest: dict, keys: tuple[str, ...]) -> None:
    print(json.dumps({k: manifest.get(k) for k in keys}, indent=1))
    print(json.dumps({"outcomes": [f"{c['arm']}/{c['problem']}: {c['outcome']}"
                                   + ("" if c.get("schema_ok", True) else " (schema fail)") for c in manifest["calls"]]}))


def cmd_dry_run(args, env: Mapping[str, str], client_factory: Callable[[str, str], Any]) -> int:
    key = _common_preflight(args, env)
    statement = args.statement_file.read_text().strip()
    log = CallLog(args.out / "calls.jsonl")
    spent, calls, replies = _run_calls([("dry", statement)], max_usd=args.max_usd, log=log, key=key,
                                       client_factory=client_factory)
    replies.clear()
    if not any(c["outcome"] != "refused_cap" for c in calls):
        raise SealError("no call fits under --max-usd; nothing was dispatched")
    manifest = {"item": "N8 E-SEAL dry run (non-conservation problem; replies discarded unread)",
                "utc": datetime.now(UTC).isoformat(), "statement_sha256": _sha(statement.encode()), **_hashes(),
                "max_usd": args.max_usd, "spent_usd": round(spent, 6), "calls": calls,
                "all_ok": all(c["outcome"] == "ok" and c["schema_ok"] for c in calls)}
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    _print_summary(manifest, ("all_ok", "spent_usd", "max_usd"))
    return 0 if manifest["all_ok"] else 1


def cmd_seal(args, env: Mapping[str, str], client_factory: Callable[[str, str], Any]) -> int:
    key = _common_preflight(args, env)
    if not args.provider_logging_off:
        raise SealError("confirm with --provider-logging-off that OpenRouter input/output logging is off")
    if not env.get(PUBLIC_KEY_ENV):
        raise SealError(f"{PUBLIC_KEY_ENV} is not set: export the path to the custodian's RSA public key")
    public_key = Path(env[PUBLIC_KEY_ENV]).expanduser()
    check_public_key(public_key)
    repo = (args.repo or ROOT).resolve()
    plan_commit = _committed(repo, args.plan, "the plan (scoring protocol)")
    dry_path = args.dry_run / "manifest.json"
    dry = json.loads(dry_path.read_text()) if dry_path.exists() else None
    if not dry or not dry["all_ok"] or any(dry[k] != v for k, v in _hashes().items()):
        raise SealError("no passing dry run with the current prompt and schema; run dry-run first")
    headroom = measured_headroom(env)
    problems_doc = json.loads(args.problems.read_text())
    problems = [(pid, problems_doc["problems"][pid]["statement"])
                for s in sorted(problems_doc["sets"]) for pid in problems_doc["sets"][s]]
    problems_sha = _sha(args.problems.read_bytes())

    started = datetime.now(UTC).isoformat()
    spent, calls, forecasts = _run_calls(problems, max_usd=args.max_usd, log=CallLog(args.out / "calls.jsonl"),
                                         key=key, client_factory=client_factory)
    if not any(c["outcome"] != "refused_cap" for c in calls):
        raise SealError("no call fits under --max-usd; nothing was dispatched")
    sealed = any(forecasts.values())
    manifest = {
        "item": "N8 E-SEAL: closed-book model forecast of the Stage A operations", "evidence_label":
        "synthetic extrapolation", "started_utc": started,
        "plan": str(args.plan.resolve().relative_to(repo)), "plan_sha256": _sha(args.plan.read_bytes()),
        "plan_commit": plan_commit, "dry_run_manifest_sha256": _sha(dry_path.read_bytes()),
        "arms": [{"name": a.name, "model": a.model, "family": a.family, "provider": "openrouter",
                  "max_tokens": MAX_TOKENS, "temperature": "provider default",
                  "response_format": "json_schema strict"} for a in ARMS],
        "max_ops_per_problem": MAX_OPS, "price_usd_per_mtok": PRICES_PER_MTOK,
        "problems_sha256": problems_sha, "problems": [pid for pid, _ in problems], **_hashes(),
        "max_usd": args.max_usd, "key_headroom": headroom,
        "provider_logging": "off, confirmed by the operator at run time",
        "spent_usd": round(spent, 6), "calls": calls,
        "complete": all(c["outcome"] == "ok" and c["schema_ok"] for c in calls), "sealed": sealed,
        "cipher": {"data": " ".join(ENC[:-2]), "key_wrap": "pkeyutl " + " ".join(WRAP),
                   "min_rsa_bits": MIN_RSA_BITS},
    }
    if sealed:
        plaintext = json.dumps({"nonce": secrets.token_hex(32), "started_utc": started,
                                "problems_sha256": problems_sha, "forecasts": forecasts},
                               sort_keys=True).encode()
        manifest.update(seal_bytes(plaintext, public_key, args.out))
        del plaintext
    forecasts.clear()
    manifest["finished_utc"] = datetime.now(UTC).isoformat()
    (args.out / "manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    _print_summary(manifest, ("sealed", "complete", "spent_usd", "max_usd", "forecast_enc_sha256",
                              "key_enc_sha256", "plaintext_sha256", "public_key_sha256"))
    return 0 if manifest["complete"] else 1


def cmd_unseal(args) -> int:
    repo = (args.repo or ROOT).resolve()
    lock = args.k1_lock.resolve()
    lock_commit = _committed(repo, lock, "the K1 lock file (unsealing waits for the locked K1 adjudication)")
    try:
        lock_doc = json.loads(lock.read_text())
    except json.JSONDecodeError:
        raise SealError("the K1 lock file is not JSON") from None
    if not isinstance(lock_doc, dict) or "k1_decision" not in lock_doc:
        raise SealError("the K1 lock file has no k1_decision field")
    out = args.out.resolve()
    if out.is_relative_to(repo):
        raise SealError("--out must be outside the git working tree")
    if out.exists() and any(out.iterdir()):
        raise SealError(f"{out} is not empty")
    plain = unseal_bytes(args.sealed, args.private_key)
    out.mkdir(parents=True, exist_ok=True)
    (out / "forecast.json").write_bytes(plain)
    m = json.loads((args.sealed / "manifest.json").read_text())
    record_path = args.sealed.parent / "unseal_record.json"
    records = json.loads(record_path.read_text()) if record_path.exists() else []
    records.append({"utc": datetime.now(UTC).isoformat(), "k1_lock": str(lock.relative_to(repo)),
                    "k1_lock_sha256": _sha(lock.read_bytes()), "k1_lock_commit": lock_commit,
                    "forecast_enc_sha256": m["forecast_enc_sha256"], "plaintext_sha256": m["plaintext_sha256"]})
    record_path.write_text(json.dumps(records, indent=1) + "\n")
    print(f"unsealed into {out}; record appended to {record_path}")
    return 0


def main(argv: list[str] | None = None, *, env: Mapping[str, str] | None = None,
         client_factory: Callable[[str, str], Any] | None = None) -> int:
    for name in ("openai", "httpx", "httpcore"):
        logging.getLogger(name).setLevel(logging.WARNING)
    p = argparse.ArgumentParser(prog="reconstruct.eseal")
    sub = p.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dry-run")
    d.add_argument("--live", action="store_true")
    d.add_argument("--max-usd", type=float, required=True)
    d.add_argument("--statement-file", type=Path, default=HERE / "dry_run_problem.md")
    d.add_argument("--out", type=Path, default=HERE / "dry_run")
    s = sub.add_parser("seal")
    s.add_argument("--live", action="store_true")
    s.add_argument("--max-usd", type=float, required=True)
    s.add_argument("--provider-logging-off", action="store_true")
    s.add_argument("--problems", type=Path, default=DEFAULT_PROBLEMS)
    s.add_argument("--plan", type=Path, default=DEFAULT_PLAN)
    s.add_argument("--dry-run", type=Path, default=HERE / "dry_run")
    s.add_argument("--out", type=Path, default=HERE / "sealed")
    s.add_argument("--repo", type=Path, default=None)
    u = sub.add_parser("unseal")
    u.add_argument("--sealed", type=Path, default=HERE / "sealed")
    u.add_argument("--private-key", type=Path, required=True)
    u.add_argument("--k1-lock", type=Path, required=True)
    u.add_argument("--out", type=Path, required=True)
    u.add_argument("--repo", type=Path, default=None)
    args = p.parse_args(argv)
    env = os.environ if env is None else env
    factory = client_factory or (lambda provider, key: openai.OpenAI(api_key=key, base_url=OPENROUTER_URL))
    try:
        if args.cmd == "dry-run":
            return cmd_dry_run(args, env, factory)
        if args.cmd == "seal":
            return cmd_seal(args, env, factory)
        return cmd_unseal(args)
    except SealError as e:
        print(f"eseal: {e}", file=sys.stderr)
    except Exception as e:  # noqa: BLE001 — never print a message that could carry content
        print(f"eseal: stopped on {type(e).__name__}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
