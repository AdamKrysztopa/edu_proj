"""__main__.py: byte-identical output across runs, and no network (spec §11.7); byte-identical
output across PYTHONHASHSEED values (F8). Replay mode (no `--judge`) never opens a socket: these
tests pass a `FakeJudge` directly (S1: "the existing no-network test must still pass in replay
mode"), which never touches the network regardless of cache state."""
import json
import os
import shutil
import socket
import subprocess
import sys
from pathlib import Path

from conftest import FakeJudge, a_claim, area, ledger

from gapmap import __main__ as cli
from gapmap import config
from gapmap import judge as judge_mod


def _fixture_ledger():
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="key-1")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="key-2")
    c3 = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="src-3")
    lg = ledger([c1, c2, c3], areas=[area("a-1", "Area One")],
               assignments=[(c1.claim_id, "a-1"), (c2.claim_id, "a-1"), (c3.claim_id, "a-1")])
    return lg


def test_no_network(monkeypatch, tmp_path):
    def _raise(*a, **k):
        raise AssertionError("gapmap must not open a socket")
    monkeypatch.setattr(socket, "socket", _raise)

    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(_fixture_ledger().to_json())
    out = tmp_path / "out"
    cli.run(str(ledger_path), domain="test", out_dir=str(out), judge=FakeJudge())
    assert (out / "gapmap.json").exists()
    assert (out / "gapmap.md").exists()


def test_byte_identical_across_two_runs(tmp_path):
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(_fixture_ledger().to_json())

    out1, out2 = tmp_path / "out1", tmp_path / "out2"
    cli.run(str(ledger_path), domain="test", out_dir=str(out1), judge=FakeJudge())
    cli.run(str(ledger_path), domain="test", out_dir=str(out2), judge=FakeJudge())

    assert (out1 / "gapmap.json").read_bytes() == (out2 / "gapmap.json").read_bytes()
    assert (out1 / "gapmap.md").read_bytes() == (out2 / "gapmap.md").read_bytes()


def test_byte_identical_across_pythonhashseed_0_1_2(tmp_path):
    # F8: sort every iteration over sets/frozensets that reaches output; verified end to end by
    # running the CLI as a subprocess under 3 different hash seeds (in-process os.environ changes
    # do not affect str hash randomization, which is fixed at interpreter start). The subprocess
    # runs in REPLAY mode (no --judge), so its `OllamaJudge`-shaped cache key must already be
    # filled: pre-seed one cache with a network-free judge sharing `OllamaJudge`'s model id, then
    # copy it into each seed's `--out` directory.
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(_fixture_ledger().to_json())
    cache_seed_dir = tmp_path / "cache-seed"
    cached = judge_mod.CachedJudge(FakeJudge(model_id=config.JUDGE_MODEL),
                                   cache_seed_dir / "closure_judgements.json", live=True)
    cli.run(str(ledger_path), domain="test", out_dir=str(cache_seed_dir), judge=cached)
    seed_cache = cache_seed_dir / "closure_judgements.json"

    src_root = Path(__file__).resolve().parents[1] / "src"
    outputs = []
    for seed in ("0", "1", "2"):
        out = tmp_path / f"out-{seed}"
        out.mkdir()
        shutil.copy(seed_cache, out / "closure_judgements.json")
        env = {**os.environ, "PYTHONHASHSEED": seed, "PYTHONPATH": str(src_root)}
        subprocess.run([sys.executable, "-m", "gapmap", "--ledger", str(ledger_path),
                       "--domain", "test", "--out", str(out)], check=True, env=env)
        outputs.append(((out / "gapmap.json").read_bytes(), (out / "gapmap.md").read_bytes()))
    assert len({o[0] for o in outputs}) == 1
    assert len({o[1] for o in outputs}) == 1


def test_gapmap_json_is_well_formed_and_sorted_keys(tmp_path):
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(_fixture_ledger().to_json())
    out = tmp_path / "out"
    cli.run(str(ledger_path), domain="test-domain", out_dir=str(out), judge=FakeJudge())
    data = json.loads((out / "gapmap.json").read_text())
    assert data["domain"] == "test-domain"
    assert "ledger_sha256" in data and "config_sha256" in data
    assert isinstance(data["map"], list)
    assert isinstance(data["retrieval_gaps"], list)
    assert "checks" in data


def test_replay_mode_raises_a_clear_error_naming_judge_ollama_on_cache_miss(tmp_path):
    ledger_path = tmp_path / "ledger.json"
    ledger_path.write_text(_fixture_ledger().to_json())
    out = tmp_path / "out"
    try:
        cli.run(str(ledger_path), domain="test", out_dir=str(out))
    except judge_mod.JudgeCacheMiss as e:
        assert "--judge ollama" in str(e)
    else:
        raise AssertionError("expected a JudgeCacheMiss on an empty cache in replay mode")
