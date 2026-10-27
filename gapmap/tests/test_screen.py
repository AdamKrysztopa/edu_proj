"""Judge screening, N3's standard way to choose a closure judge (docs/plans/judge-screening-standard.md).
A fake runner stands in for the G1/G2 runners: it writes the result files a fake judge would produce,
so no test opens the network or spends money."""
import json
import sys
from pathlib import Path

import pytest

from gapmap import screen

REPO = Path(__file__).resolve().parents[2]
SOL = {"model": "gpt-6.1-sol", "reasoning_effort": "high"}
GEMMA = {"model": "google/gemma-4-31b-it", "reasoning_max_tokens": 2000}


def _root(tmp_path: Path) -> Path:
    for rel in screen.FIXTURE_FILES:
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"fixture {rel}\n")
    return tmp_path


class FakeRunner:
    """Outcomes per step, consumed in order: "pass", "fail", "incomplete" (undecided arm) or "crash"
    (non-zero exit, no result file). Each paid call appends `usd` to the spend ledger it is given."""

    def __init__(self, **outcomes):
        self.outcomes = {k: list(v) for k, v in outcomes.items()}
        self.calls: list[list[str]] = []

    def __call__(self, argv: list[str], cwd: Path) -> int:
        self.calls.append(argv)
        script = Path(argv[1]).name
        step = "S0" if "--stand-ins" in argv else "G1" if script == "g1.py" else "G2"
        outcome = self.outcomes[step].pop(0)
        live = "--judge" in argv
        if live and "--spend-ledger" in argv:
            with open(argv[argv.index("--spend-ledger") + 1], "a") as f:
                f.write(json.dumps({"usd": 0.01}) + "\n")
        if outcome == "crash":
            return 1
        if step == "S0":
            out = Path(argv[argv.index("--out") + 1])
            out.mkdir(parents=True, exist_ok=True)
            rows = [{"judge_model": "standin-length", "passes": outcome == "fail", "complete": True}]
            (out / "g2_standins_gate.json").write_text(json.dumps(rows))
            (out / "g2_oracle_gate.json").write_text(json.dumps({"passes": outcome != "no-oracle"}))
            return 1 if outcome in ("fail", "no-oracle") else 0
        if step == "G1":
            out = Path(argv[argv.index("--out-root") + 1]) / argv[argv.index("--tag") + 1] / "l73"
            out.mkdir(parents=True, exist_ok=True)
            (out / "l73.json").write_text(json.dumps({"eligible": outcome == "pass", "planted_fires": outcome == "pass",
                                                      "stand_in_fires": False}))
            return 0
        out = Path(argv[argv.index("--out") + 1])
        out.mkdir(parents=True, exist_ok=True)
        state = "closed" if outcome == "pass" else "open"
        res = {"states": {"t01": {"P": state, "N": "open"}, "t02": {"P": "closed", "N": "open"}},
               "passes": outcome == "pass", "complete": outcome != "incomplete",
               "undecided": int(outcome == "incomplete"), "diff": 1.0 if outcome == "pass" else 0.0,
               "lower90": 1.0, "rates": {"0": 0, "P": 1, "N": 0, "N+": 0, "R": 0}, "R_excess": 0.0}
        (out / "g2_gate.json").write_text(json.dumps(res))
        return 0


def _room(provider, need):
    return True, "fake headroom"


def _run(root, slug, cand, runner, *, live=True, max_usd=0.30, ledger=None, **kw):
    ledger = ledger if ledger is not None else root / "spend.jsonl"
    return screen.run(root, slug, cand, runner=runner, live=live, max_usd=max_usd if live else None,
                      spend_ledger=ledger if live else None, headroom=_room, **kw)


def _screen_to_eligible(root, slug, cand):
    runner = FakeRunner(S0=["pass"], G1=["pass"], G2=["pass", "pass"])
    for _ in range(3):
        _run(root, slug, cand, runner)
    assert screen.status(root, slug)["eligible"]
    return runner


def test_eligibility_is_recorded_only_after_one_g1_and_two_g2_passes(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"], G2=["pass", "pass"])
    _run(root, "gemma", GEMMA, runner)
    assert screen.status(root, "gemma")["status"] == "pending"
    _run(root, "gemma", GEMMA, runner)
    v = screen.status(root, "gemma")
    assert not v["eligible"] and v["steps"]["G2"]["passes"] == 1
    _run(root, "gemma", GEMMA, runner)
    v = json.loads((root / screen.SCREEN_DIR / "gemma" / "verdict.json").read_text())
    assert v["eligible"] and v["status"] == "eligible"
    assert v["settles_alone"] is False
    assert [r["step"] for r in v["runs"]] == ["S0", "G1", "G2", "G2"]


def test_one_invocation_starts_at_most_one_paid_run(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"], G2=["pass", "pass"])
    _run(root, "gemma", GEMMA, runner)
    assert [Path(c[1]).name for c in runner.calls] == ["g2.py", "g1.py"]


def test_a_paid_step_is_refused_while_the_free_fixture_gate_fails(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["fail"])
    with pytest.raises(screen.Refused, match="S0"):
        _run(root, "gemma", GEMMA, runner)
    assert all("--judge" not in c for c in runner.calls)
    assert screen.status(root, "gemma")["status"] == "out"


def test_a_crashed_free_gate_is_pending_and_refuses_paid_runs(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["crash"])
    with pytest.raises(screen.Refused, match="S0"):
        _run(root, "gemma", GEMMA, runner)
    assert len(runner.calls) == 1 and screen.status(root, "gemma")["steps"]["S0"]["state"] == "pending"


def test_without_live_only_free_steps_run_and_no_paid_call_is_made(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"])
    res = _run(root, "gemma", GEMMA, runner, live=False)
    assert res["waiting_for"] == "G1" and "g1.py" in " ".join(res["next_command"])
    assert len(runner.calls) == 1 and "--judge" not in runner.calls[0]


def test_a_paid_run_needs_a_cap_and_a_spend_ledger(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"])
    with pytest.raises(screen.Refused, match="--max-usd"):
        screen.run(root, "gemma", GEMMA, runner=runner, live=True, max_usd=None, spend_ledger=root / "s.jsonl",
                   headroom=_room)
    with pytest.raises(screen.Refused, match="--spend-ledger"):
        screen.run(root, "gemma", GEMMA, runner=runner, live=True, max_usd=0.3, spend_ledger=None, headroom=_room)


def test_the_runner_cap_is_the_ledgers_prior_spend_plus_this_runs_cap(tmp_path):
    root = _root(tmp_path)
    ledger = root / "spend.jsonl"
    ledger.write_text(json.dumps({"usd": 0.25}) + "\n" + json.dumps({"usd": 0.04}) + "\n")
    runner = FakeRunner(S0=["pass"], G1=["pass"])
    _run(root, "gemma", GEMMA, runner, max_usd=0.30, ledger=ledger)
    g1 = runner.calls[-1]
    assert float(g1[g1.index("--max-usd") + 1]) == pytest.approx(0.59)
    run = screen.status(root, "gemma")["runs"][-1]
    assert run["spend_usd"] == pytest.approx(0.01) and run["max_usd"] == 0.30


def test_a_same_family_candidate_is_refused_paid_runs_until_an_other_family_arm_is_eligible(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass", "pass"], G1=["pass"])
    with pytest.raises(screen.Refused, match="S1"):
        _run(root, "sol", SOL, runner)
    assert all("--judge" not in c for c in runner.calls)
    _screen_to_eligible(root, "gemma", GEMMA)
    _run(root, "sol", SOL, runner)
    v = screen.status(root, "sol")
    s1 = next(r for r in v["runs"] if r["step"] == "S1")
    assert s1["outcome"] == "pass" and s1["parallel_arm"] == "gemma"
    assert v["steps"]["G1"]["passes"] == 1


def test_an_other_family_candidate_needs_no_parallel_arm_step(tmp_path):
    root = _root(tmp_path)
    _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["pass"]))
    assert screen.status(root, "gemma")["steps"]["S1"]["state"] == "n/a"


def test_a_failed_complete_run_makes_the_candidate_out_and_refuses_more_runs(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"], G2=["pass", "fail", "pass"])
    for _ in range(3):
        _run(root, "gemma", GEMMA, runner)
    assert screen.status(root, "gemma")["status"] == "out"
    with pytest.raises(screen.Refused, match="out"):
        _run(root, "gemma", GEMMA, runner)
    assert not screen.status(root, "gemma")["eligible"]


def test_an_incomplete_run_does_not_count_and_its_retry_gets_a_fresh_directory(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"], G2=["incomplete", "crash", "pass", "pass"])
    _run(root, "gemma", GEMMA, runner)
    _run(root, "gemma", GEMMA, runner)
    for _ in range(3):
        _run(root, "gemma", GEMMA, runner, owner_note="provider outage, retried")
    v = screen.status(root, "gemma")
    assert v["eligible"]
    g2_outs = [c[c.index("--out") + 1] for c in runner.calls if Path(c[1]).name == "g2.py" and "--judge" in c]
    assert len(g2_outs) == 4 and len(set(g2_outs)) == 4
    assert [r["outcome"] for r in v["runs"] if r["step"] == "G2"] == ["incomplete", "incomplete", "pass", "pass"]


def test_an_existing_run_directory_is_refused(tmp_path):
    root = _root(tmp_path)
    (root / screen.SCREEN_DIR / "gemma" / "S0-run1").mkdir(parents=True)
    with pytest.raises(screen.Refused, match="exists"):
        _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"]))


def test_a_changed_fixture_makes_earlier_runs_stale(tmp_path):
    root = _root(tmp_path)
    _screen_to_eligible(root, "gemma", GEMMA)
    (root / screen.FIXTURE_FILES[0]).write_text("changed\n")
    v = screen.status(root, "gemma")
    assert not v["eligible"] and v["stale_runs"] == 4 and v["status"] == "pending"


def test_a_fail_under_an_older_fixture_hash_still_keeps_the_candidate_out(tmp_path):
    root = _root(tmp_path)
    _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["fail"]))
    (root / screen.FIXTURE_FILES[0]).write_text("changed\n")
    assert screen.status(root, "gemma")["status"] == "out"


def test_a_failed_model_cannot_come_back_under_a_new_slug_without_an_owner_note(tmp_path):
    root = _root(tmp_path)
    _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["fail"]))
    with pytest.raises(screen.Refused, match="owner-note"):
        _run(root, "gemma-b", {**GEMMA, "reasoning_max_tokens": 4000}, FakeRunner(S0=["pass"], G1=["pass"]))
    _run(root, "gemma-b", {**GEMMA, "reasoning_max_tokens": 4000}, FakeRunner(S0=["pass"], G1=["pass"]),
         owner_note="larger reasoning budget, owner 2026-10-27")
    assert screen.status(root, "gemma-b")["readmitted"]["after"] == ["gemma"]


def test_a_second_incomplete_retry_needs_an_owner_note(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"], G2=["incomplete", "pass"])
    _run(root, "gemma", GEMMA, runner)
    _run(root, "gemma", GEMMA, runner)
    with pytest.raises(screen.Refused, match="owner-note"):
        _run(root, "gemma", GEMMA, runner)
    assert len([c for c in runner.calls if "--judge" in c]) == 2


def test_s0_fails_when_the_p_oracle_cannot_pass_the_fixtures(tmp_path):
    root = _root(tmp_path)
    with pytest.raises(screen.Refused, match="S0"):
        _run(root, "gemma", GEMMA, FakeRunner(S0=["no-oracle"]))
    assert screen.status(root, "gemma")["status"] == "out"


def test_after_refuses_a_paid_run_unless_the_plans_gate_record_says_continue(tmp_path):
    root = _root(tmp_path)
    gate = tmp_path / "stop_a.json"
    runner = FakeRunner(S0=["pass"], G1=["pass"])
    with pytest.raises(screen.Refused, match="does not exist"):
        _run(root, "gemma", GEMMA, runner, after=gate)
    gate.write_text(json.dumps({"continue": False}))
    with pytest.raises(screen.Refused, match="continue"):
        _run(root, "gemma", GEMMA, runner, after=gate)
    assert all("--judge" not in c for c in runner.calls)
    gate.write_text(json.dumps({"continue": True}))
    _run(root, "gemma", GEMMA, runner, after=gate)
    assert screen.status(root, "gemma")["runs"][-1]["after_gate"]["path"] == str(gate)


def test_a_paid_run_is_refused_while_another_holds_the_spend_ledger(tmp_path):
    root = _root(tmp_path)
    ledger = root / "spend.jsonl"
    (root / "spend.jsonl.lock").write_text("")
    with pytest.raises(screen.Refused, match="spend ledger"):
        _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["pass"]), ledger=ledger)


def test_a_paid_run_is_refused_when_the_provider_headroom_is_short(tmp_path):
    root = _root(tmp_path)
    runner = FakeRunner(S0=["pass"], G1=["pass"])
    with pytest.raises(screen.Refused, match="headroom"):
        screen.run(root, "gemma", GEMMA, runner=runner, live=True, max_usd=0.3, spend_ledger=root / "s.jsonl",
                   headroom=lambda provider, need: (False, "remaining=0.01"))
    assert all("--judge" not in c for c in runner.calls)


def test_a_concurrent_run_on_the_same_candidate_is_refused(tmp_path):
    root = _root(tmp_path)
    d = root / screen.SCREEN_DIR / "gemma"
    d.mkdir(parents=True)
    (d / screen.LOCK).write_text("")
    with pytest.raises(screen.Refused, match="lock"):
        _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"]))


def test_settings_cannot_change_between_runs(tmp_path):
    root = _root(tmp_path)
    _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["pass"]))
    with pytest.raises(screen.Refused, match="settings"):
        _run(root, "gemma", {**GEMMA, "reasoning_max_tokens": 4000}, FakeRunner(G2=["pass"]))


def test_a_model_with_no_recorded_price_is_refused(tmp_path):
    with pytest.raises(screen.Refused, match="price"):
        _run(_root(tmp_path), "x", {"model": "acme/unknown"}, FakeRunner())


def test_runner_commands_pass_each_providers_settings(tmp_path):
    root = _root(tmp_path)
    r1 = FakeRunner(S0=["pass"], G1=["pass"])
    _run(root, "gemma", GEMMA, r1)
    assert r1.calls[-1][r1.calls[-1].index("--reasoning-max-tokens") + 1] == "2000"
    _screen_to_eligible(root, "gemma2", GEMMA)
    r2 = FakeRunner(S0=["pass"], G1=["pass"])
    _run(root, "sol", SOL, r2)
    g1 = r2.calls[-1]
    assert g1[g1.index("--model") + 1] == "gpt-6.1-sol" and g1[g1.index("--reasoning-effort") + 1] == "high"
    assert g1[g1.index("--judge") + 1] == "openai"


def test_pair_needs_an_eligible_cheap_other_family_arm_and_an_eligible_top_tier_arm(tmp_path):
    root = _root(tmp_path)
    _screen_to_eligible(root, "gemma", GEMMA)
    assert not screen.pair(root, "gemma", "sol")["ready"]
    _screen_to_eligible(root, "sol", SOL)
    p = screen.pair(root, "gemma", "sol")
    assert p["ready"] and p["fixtures_sha256"] == screen.fixture_hash(root)
    assert p["g2_state_agreement"] == {"n": 8, "agreement": 1.0, "kappa": 1.0}
    assert not screen.pair(root, "sol", "gemma")["ready"]


def _old_g2_run(tmp_path, outcome="pass"):
    src = tmp_path / "old-run"
    FakeRunner(G2=[outcome])([sys.executable, "g2.py", "--out", str(src)], tmp_path)
    (src / "closure_judgements.json").write_text("{}")
    return src


def test_adopt_replays_a_committed_cache_without_a_live_flag(tmp_path):
    root = _root(tmp_path)
    _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["pass"]))
    src = _old_g2_run(tmp_path)
    runner = FakeRunner(G2=["pass"])
    screen.adopt(root, "gemma", GEMMA, "G2", src, note="D1b gate1, cold cache", runner=runner)
    argv = runner.calls[-1]
    assert "--judge" not in argv and "--max-usd" not in argv
    out = Path(argv[argv.index("--out") + 1])
    assert (out / "closure_judgements.json").read_text() == "{}"
    run = screen.status(root, "gemma")["runs"][-1]
    assert run["adopted_from"] == "old-run" and run["note"] == "D1b gate1, cold cache"
    assert run["outcome"] == "pass"


def test_adopt_records_nothing_when_the_replay_does_not_reproduce_the_source(tmp_path):
    root = _root(tmp_path)
    _run(root, "gemma", GEMMA, FakeRunner(S0=["pass"], G1=["pass"]))
    src = _old_g2_run(tmp_path, "pass")
    with pytest.raises(screen.Refused, match="not adopted"):
        screen.adopt(root, "gemma", GEMMA, "G2", src, note="n", runner=FakeRunner(G2=["fail"]))
    assert [r["step"] for r in screen.status(root, "gemma")["runs"]] == ["S0", "G1"]
    assert not (root / screen.SCREEN_DIR / "gemma" / "G2-run1").exists()


def test_adopt_keeps_the_order_of_steps(tmp_path):
    root = _root(tmp_path)
    src = _old_g2_run(tmp_path)
    with pytest.raises(screen.Refused, match="G1"):
        screen.adopt(root, "gemma", GEMMA, "G2", src, note="n", runner=FakeRunner(S0=["pass"], G2=["pass"]))


def test_the_result_readers_accept_d1bs_committed_outputs():
    g2 = screen.read_outcome("G2", REPO / "research/d1b_rerun/g2/sol-gate1", 0)
    assert g2["outcome"] == "pass" and g2["figures"]["diff"] == 1.0
    g1 = screen.read_outcome("G1", REPO / "research/d1b_rerun/g1/sol-r1", 0)
    assert g1["outcome"] == "pass"


def _l73(tmp_path, states):
    (tmp_path / "l73").mkdir(exist_ok=True)
    (tmp_path / "l73" / "l73.json").write_text(json.dumps(
        {"eligible": True, "planted_fires": True, "stand_in_fires": False,
         "topics": {"t": {"planted": {"all_pairs": [{"states": states}]}}}}))
    return screen.read_outcome("G1", tmp_path, 0)


def test_an_undecided_seed_free_g1_arm_makes_the_run_incomplete(tmp_path):
    res = _l73(tmp_path, {"own_sf": "undecided", "ctrl_sf": "open", "own_eq": "open", "ctrl_eq": "open"})
    assert res["outcome"] == "incomplete" and res["figures"]["undecided"]["own_sf"] == 1
    res = _l73(tmp_path, {"own_sf": "closed", "ctrl_sf": "open", "own_eq": "undecided", "ctrl_eq": "open"})
    assert res["outcome"] == "pass"


def test_the_cli_status_prints_the_verdict_and_never_calls_a_runner(tmp_path, capsys):
    root = _root(tmp_path)
    assert screen.main(["--root", str(root), "status", "--candidate", "nobody"]) == 0
    assert json.loads(capsys.readouterr().out)["status"] == "pending"
