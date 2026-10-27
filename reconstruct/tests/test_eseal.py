import base64
import hashlib
import json
import logging
import subprocess
from pathlib import Path
from types import SimpleNamespace as ns

import pytest

from reconstruct import eseal

CANARY = "CANARY-7f3e9a1c-sealed-operation"
ANSWER_MARK = "ANSWER-MARK-should-never-be-sent"
MODELS = [a.model for a in eseal.ARMS]
N_CALLS = 4 * len(eseal.ARMS)


def _keypair(d: Path, bits: int):
    priv, pub = d / f"k{bits}.key", d / f"k{bits}.pub"
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", f"rsa_keygen_bits:{bits}",
                    "-out", str(priv)], check=True, capture_output=True)
    subprocess.run(["openssl", "pkey", "-in", str(priv), "-pubout", "-out", str(pub)], check=True, capture_output=True)
    return priv, pub


@pytest.fixture(scope="session")
def keypair(tmp_path_factory):
    return _keypair(tmp_path_factory.mktemp("keys"), 3072)


def _git(repo: Path, *args: str):
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path):
    r = tmp_path / "repo"
    r.mkdir()
    _git(r, "init", "-q")
    _git(r, "config", "user.email", "t@example.org")
    _git(r, "config", "user.name", "t")
    (r / "plan.md").write_text("scoring protocol\n")
    (r / "problems.json").write_text(json.dumps({
        "sets": {"A": ["A1", "A2"], "B": ["B1", "B2"]},
        "problems": {pid: {"statement": f"Statement of {pid}: a block slides.", "answer": ANSWER_MARK}
                     for pid in ("A1", "A2", "B1", "B2")},
    }))
    (r / "dry.md").write_text("Statement of DRY: a stone is thrown.\n")
    _git(r, "add", "-A")
    _git(r, "commit", "-q", "-m", "plan")
    return r


def _reply(model, *, cost, n_ops):
    ops = [{"statement": f"{CANARY} operation {i}", "trigger": f"{CANARY} trigger", "type": "check",
            "p_omitted": 0.4} for i in range(n_ops)]
    return ns(choices=[ns(message=ns(content=json.dumps({"operations": ops}), refusal=None),
                          finish_reason="stop")],
              model=model, usage=ns(prompt_tokens=400, completion_tokens=900, cost=cost))


class Factory:
    """Builds one fake client per arm; `fail` maps a problem id to the exception its call raises."""

    def __init__(self, *, cost=0.01, fail=None, n_ops=3):
        self.cost, self.fail, self.n_ops, self.calls = cost, fail or {}, n_ops, []

    def __call__(self, provider, key):
        return ns(chat=ns(completions=ns(create=self._create)))

    def _create(self, **kw):
        self.calls.append(kw)
        user = kw["messages"][-1]["content"]
        for pid, exc in self.fail.items():
            if f"Statement of {pid}:" in user:
                raise exc
        return _reply(kw["model"], cost=self.cost, n_ops=self.n_ops)


def _headroom_file(d: Path, remaining: float) -> Path:
    f = d / f"headroom_{remaining}.json"
    f.write_text(json.dumps({"limit": 30, "limit_remaining": remaining, "usage_weekly": 1, "limit_reset": "weekly",
                             "account": {"total_credits": 20, "total_usage": 1}}))
    return f


_HEADROOM: dict[str, Path] = {}


@pytest.fixture(autouse=True)
def _fake_headroom(tmp_path):
    _HEADROOM["file"] = _headroom_file(tmp_path, 29.0)


def _env(pub, **extra):
    return {"E_SEAL_PUBLIC_KEY": str(pub), "OPENROUTER_API_KEY": "sk-fake",
            "KEY_HEADROOM_JSON": str(_HEADROOM["file"]), **extra}


def _dry_run(repo, factory, max_usd="0.25"):
    return eseal.main(["dry-run", "--live", "--max-usd", max_usd, "--statement-file", str(repo / "dry.md"),
                       "--out", str(repo / "dry_run")], env={"OPENROUTER_API_KEY": "sk-fake"},
                      client_factory=factory)


@pytest.fixture
def dry_ok(repo):
    assert _dry_run(repo, Factory()) == 0
    return repo / "dry_run"


def _seal(repo, env, factory, *, max_usd="0.75", flags=("--provider-logging-off",)):
    out = repo / "sealed"
    code = eseal.main(["seal", "--live", "--max-usd", max_usd, *flags,
                       "--problems", str(repo / "problems.json"), "--plan", str(repo / "plan.md"),
                       "--dry-run", str(repo / "dry_run"), "--out", str(out), "--repo", str(repo)],
                      env=env, client_factory=factory)
    return code, out


def _encodings(s: str) -> list[bytes]:
    b = s.encode()
    return [b, json.dumps(s).encode(), base64.b64encode(b), b.hex().encode(), s.encode("utf-16-le")]


def _assert_nowhere(root: Path, text: str, *streams: str):
    for enc in _encodings(text):
        for f in root.rglob("*"):
            if f.is_file():
                assert enc not in f.read_bytes(), f"{text!r} leaked into {f}"
        for s in streams:
            assert enc.decode("latin-1") not in s


# --- seal ----------------------------------------------------------------------------------

def test_canary_reaches_only_the_ciphertext(tmp_path, repo, dry_ok, keypair, capsys, caplog):
    caplog.set_level(logging.DEBUG)
    priv, pub = keypair
    factory = Factory()
    code, out = _seal(repo, _env(pub), factory)
    assert code == 0
    assert len(factory.calls) == N_CALLS
    captured = capsys.readouterr()
    _assert_nowhere(tmp_path, CANARY, captured.out, captured.err, caplog.text)

    plain = eseal.unseal_bytes(out, priv)
    assert CANARY in plain.decode()
    doc = json.loads(plain)
    assert set(doc["forecasts"]) == {a.name for a in eseal.ARMS}
    assert all(set(v) == {"A1", "A2", "B1", "B2"} for v in doc["forecasts"].values())
    assert hashlib.sha256(plain).hexdigest() == json.loads((out / "manifest.json").read_text())["plaintext_sha256"]


def test_manifest_records_settings_and_hashes_only(repo, dry_ok, keypair):
    _, pub = keypair
    code, out = _seal(repo, _env(pub), Factory())
    assert code == 0
    m = json.loads((out / "manifest.json").read_text())
    sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()  # noqa: E731
    assert m["problems_sha256"] == sha(repo / "problems.json")
    assert m["plan_sha256"] == sha(repo / "plan.md") and len(m["plan_commit"]) == 40
    assert m["dry_run_manifest_sha256"] == sha(dry_ok / "manifest.json")
    assert m["system_prompt_sha256"] == hashlib.sha256(eseal.SYSTEM_PROMPT.encode()).hexdigest()
    assert m["user_template_sha256"] == hashlib.sha256(eseal.USER_TEMPLATE.encode()).hexdigest()
    assert m["forecast_enc_sha256"] == sha(out / "forecast.enc")
    assert m["key_enc_sha256"] == sha(out / "key.enc")
    assert m["public_key_sha256"] == sha(pub)
    assert [a["model"] for a in m["arms"]] == MODELS
    assert {a["family"] for a in m["arms"]} == {"anthropic", "openai"}
    assert m["max_usd"] == 0.75 and "remaining=29.0" in m["key_headroom"] and "sk-fake" not in json.dumps(m)
    assert m["spent_usd"] == pytest.approx(0.01 * N_CALLS)
    assert all(c["outcome"] == "ok" and c["schema_ok"] and c["log_outcomes"] == ["ok"] for c in m["calls"])
    assert m["complete"] is True
    assert "\"operations\":" not in json.dumps(m) and "statement" not in json.dumps(m)
    assert (out / "calls.jsonl").exists()


def test_answer_is_never_sent_and_statement_is(repo, dry_ok, keypair):
    _, pub = keypair
    factory = Factory()
    _seal(repo, _env(pub), factory)
    sent = json.dumps([c["messages"] for c in factory.calls])
    assert ANSWER_MARK not in sent
    assert "Statement of B2:" in sent
    assert {c["model"] for c in factory.calls} == set(MODELS)


@pytest.mark.parametrize("breach", ["key_unset", "key_garbage", "key_small", "openai_log", "no_logging_flag",
                                    "low_headroom", "headroom_unreadable", "no_dry_run", "stale_dry_run", "dirty_plan", "not_live"])
def test_bad_preconditions_stop_before_any_call(tmp_path, repo, dry_ok, keypair, breach):
    _, pub = keypair
    env, kw = _env(pub), {}
    if breach == "key_unset":
        del env["E_SEAL_PUBLIC_KEY"]
    elif breach == "key_garbage":
        (tmp_path / "bad.pub").write_text("not a key")
        env["E_SEAL_PUBLIC_KEY"] = str(tmp_path / "bad.pub")
    elif breach == "key_small":
        env["E_SEAL_PUBLIC_KEY"] = str(_keypair(tmp_path, 2048)[1])
    elif breach == "openai_log":
        env["OPENAI_LOG"] = "debug"
    elif breach == "no_logging_flag":
        kw["flags"] = ()
    elif breach == "low_headroom":
        env["KEY_HEADROOM_JSON"] = str(_headroom_file(tmp_path, 9.99))
    elif breach == "headroom_unreadable":
        env["KEY_HEADROOM_JSON"] = str(tmp_path / "missing.json")
    elif breach == "no_dry_run":
        (dry_ok / "manifest.json").unlink()
    elif breach == "stale_dry_run":
        m = json.loads((dry_ok / "manifest.json").read_text())
        m["system_prompt_sha256"] = "0" * 64
        (dry_ok / "manifest.json").write_text(json.dumps(m))
    elif breach == "dirty_plan":
        (repo / "plan.md").write_text("scoring edited after commit\n")
    factory = Factory()
    if breach == "not_live":
        out = repo / "sealed"
        code = eseal.main(["seal", "--max-usd", "0.75", "--provider-logging-off",
                           "--out", str(out)], env=env, client_factory=factory)
    else:
        code, out = _seal(repo, env, factory, **kw)
    assert code != 0
    assert factory.calls == []
    assert not out.exists()


def test_cap_below_one_worst_case_call_dispatches_nothing(repo, dry_ok, keypair):
    _, pub = keypair
    factory = Factory()
    code, out = _seal(repo, _env(pub), factory, max_usd="0.01")
    assert code != 0 and factory.calls == [] and not out.exists()


def test_cap_refuses_a_call_whose_worst_case_would_overshoot(repo, dry_ok, keypair):
    _, pub = keypair
    factory = Factory(cost=0.04)
    code, out = _seal(repo, _env(pub), factory, max_usd="0.20")
    m = json.loads((out / "manifest.json").read_text())
    assert code != 0
    assert m["complete"] is False
    assert m["spent_usd"] <= 0.20
    refused = [c for c in m["calls"] if c["outcome"] == "refused_cap"]
    assert refused and all(c["spent_before_usd"] + c["worst_case_usd"] > 0.20 for c in refused)
    assert len(factory.calls) == sum(c["outcome"] == "ok" for c in m["calls"])


def test_a_failing_call_leaks_nothing_and_the_rest_is_sealed(tmp_path, repo, dry_ok, keypair, capsys, caplog):
    caplog.set_level(logging.DEBUG)
    priv, pub = keypair
    code, out = _seal(repo, _env(pub), Factory(fail={"A2": RuntimeError(f"provider said {CANARY}")}))
    assert code != 0
    captured = capsys.readouterr()
    _assert_nowhere(tmp_path, CANARY, captured.out, captured.err, caplog.text)
    m = json.loads((out / "manifest.json").read_text())
    failed = [(c["problem"], c["outcome"], c["error_class"]) for c in m["calls"] if c["outcome"] != "ok"]
    assert failed == [("A2", "error", "RuntimeError")] * len(eseal.ARMS)
    doc = json.loads(eseal.unseal_bytes(out, priv))
    assert "A2" not in doc["forecasts"]["top_tier"] and "B2" in doc["forecasts"]["cheap"]


def test_an_over_long_list_is_sealed_but_flagged(repo, dry_ok, keypair):
    _, pub = keypair
    code, out = _seal(repo, _env(pub), Factory(n_ops=eseal.MAX_OPS + 1))
    m = json.loads((out / "manifest.json").read_text())
    assert code != 0 and m["sealed"] and not m["complete"]
    assert not any(c["schema_ok"] for c in m["calls"])


def test_a_second_run_cannot_overwrite_a_seal(repo, dry_ok, keypair):
    _, pub = keypair
    code, out = _seal(repo, _env(pub), Factory())
    before = (out / "forecast.enc").read_bytes()
    factory = Factory()
    code2, _ = _seal(repo, _env(pub), factory)
    assert code == 0 and code2 != 0 and factory.calls == []
    assert (out / "forecast.enc").read_bytes() == before


def test_module_never_uses_temporary_files():
    src = Path(eseal.__file__).read_text()
    assert "tempfile" not in src and "NamedTemporary" not in src


# --- dry run -------------------------------------------------------------------------------

def test_dry_run_keeps_only_outcomes(tmp_path, repo, capsys, caplog):
    caplog.set_level(logging.DEBUG)
    factory = Factory()
    assert _dry_run(repo, factory) == 0
    assert len(factory.calls) == len(eseal.ARMS)
    captured = capsys.readouterr()
    _assert_nowhere(tmp_path, CANARY, captured.out, captured.err, caplog.text)
    m = json.loads((repo / "dry_run" / "manifest.json").read_text())
    assert m["all_ok"] and m["system_prompt_sha256"] == hashlib.sha256(eseal.SYSTEM_PROMPT.encode()).hexdigest()


def test_dry_run_with_a_schema_failure_blocks_the_seal(repo, keypair):
    _, pub = keypair
    assert _dry_run(repo, Factory(n_ops=0)) != 0
    factory = Factory()
    code, out = _seal(repo, _env(pub), factory)
    assert code != 0 and factory.calls == [] and not out.exists()


# --- unseal gate ---------------------------------------------------------------------------

@pytest.fixture
def sealed_repo(repo, dry_ok, keypair):
    _, pub = keypair
    code, out = _seal(repo, _env(pub), Factory())
    assert code == 0
    lock = repo / "k1_lock.json"
    lock.write_text(json.dumps({"k1_decision": {"a": True, "b": True, "c": True}}))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "seal and K1 lock")
    return repo, out, lock


def _unseal(repo, out, lock, priv, dest):
    return eseal.main(["unseal", "--sealed", str(out), "--private-key", str(priv), "--k1-lock", str(lock),
                       "--out", str(dest), "--repo", str(repo)], env={})


def test_unseal_after_a_committed_k1_lock(sealed_repo, keypair, tmp_path, capsys):
    repo, out, lock = sealed_repo
    priv, _ = keypair
    dest = tmp_path / "opened"
    assert _unseal(repo, out, lock, priv, dest) == 0
    assert CANARY in (dest / "forecast.json").read_text()
    assert CANARY not in capsys.readouterr().out
    rec = json.loads((out.parent / "unseal_record.json").read_text())[-1]
    assert rec["k1_lock_sha256"] == hashlib.sha256(lock.read_bytes()).hexdigest()
    assert len(rec["k1_lock_commit"]) == 40


@pytest.mark.parametrize("breach", ["untracked_lock", "dirty_lock", "lock_without_decision", "out_inside_repo",
                                    "tampered"])
def test_unseal_refuses(sealed_repo, keypair, tmp_path, breach):
    repo, out, lock = sealed_repo
    priv, _ = keypair
    dest = tmp_path / "opened"
    if breach == "untracked_lock":
        lock = repo / "other_lock.json"
        lock.write_text(json.dumps({"k1_decision": {}}))
    elif breach == "dirty_lock":
        lock.write_text(json.dumps({"k1_decision": "edited"}))
    elif breach == "lock_without_decision":
        lock.write_text("{}")
        _git(repo, "commit", "-q", "-am", "lock without a decision")
    elif breach == "out_inside_repo":
        dest = repo / "opened"
    else:
        enc = bytearray((out / "forecast.enc").read_bytes())
        enc[-1] ^= 1
        (out / "forecast.enc").write_bytes(bytes(enc))
    assert _unseal(repo, out, lock, priv, dest) != 0
    assert not dest.exists()
