"""control2.py: the rebuilt closure control (I1). Equal non-seed caps applied after the seed, donor
pairing independent of the config hash, a seed-free comparison on pairs where both arms are
non-empty, both splits, seed-clustered intervals, and the L7.3 discrimination proof."""
import json
import random
import re
from pathlib import Path

import pytest
from conftest import FakeJudge, a_claim, fillers, ledger

from gapmap import checks, config, control2, lenses, link
from gapmap import judge as judge_mod


def _three_sel(planted: str = "CLOSES_HERE: choose the test whose failure likelihood is highest.",
               seed_i_exact: str | None = None):
    """Candidate i's own other-source evidence states the element (`planted`); j and k are each
    other's nearest neighbour, so neither donates it into a control arm."""
    seed_i = a_claim("Diagnostic tests should be selected based on failure likelihood.",
                     exact=seed_i_exact, source_id="s-i", independence_key="k-i")
    foreign_i = a_claim("Selection practice for failure likelihood is documented.",
                        exact=planted, source_id="s-i-f", independence_key="k-i-f")
    seed_j = a_claim("Sampling rate should be selected based on the suspected event.",
                     source_id="s-j", independence_key="k-j")
    foreign_j = a_claim("Sampling rate selection practice is documented for the suspected event.",
                        source_id="s-j-f", independence_key="k-j-f")
    seed_k = a_claim("Sampling interval should be selected based on the suspected event.",
                     source_id="s-k", independence_key="k-k")
    foreign_k = a_claim("Sampling interval selection guidance is documented for the suspected event.",
                        source_id="s-k-f", independence_key="k-k-f")
    lg = ledger([seed_i, foreign_i, seed_j, foreign_j, seed_k, foreign_k, *fillers(40)])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    assert len(cands) == 3
    return lg, idx, cands, seed_i


def _length_matched_random(sentence: str, rng: random.Random, keep: set[str]) -> str:
    """Same word lengths, random letters; `keep` words survive so retrieval still ranks it."""
    letters = "abcdefghijklmnopqrstuvwxyz"
    return " ".join(w if w.strip(".:").lower() in keep else "".join(rng.choice(letters) for _ in w)
                    for w in sentence.split())


def _row(summary, comparison="seed_free", split="closed", lens="SEL"):
    return summary["by_lens"][lens][comparison][split]


# --------------------------------------------------------------------------- arm construction

def test_both_arms_carry_the_same_number_of_non_seed_sentences():
    lg, idx, cands, _ = _three_sel()
    for spec in control2.build_pairs(lg, idx, cands):
        assert len(spec.own_other) == len(spec.donor_other) == spec.k
        assert spec.k <= config.JUDGE_A_CAP
        assert spec.k == min(config.JUDGE_A_CAP, spec.own_pool, spec.donor_pool)


def test_the_cap_is_applied_after_the_seed_so_a_long_seed_cannot_crowd_out_the_control():
    long_seed = " ".join(f"Diagnostic tests should be selected based on failure likelihood {i}."
                         for i in range(config.JUDGE_A_CAP + 2))
    lg, idx, cands, seed_i = _three_sel(seed_i_exact=long_seed)
    spec = next(s for s in control2.build_pairs(lg, idx, cands) if seed_i.claim_id in s.seeds)
    assert len(spec.seed_rows) > config.JUDGE_A_CAP
    assert spec.k >= 1
    own_eq, ctrl_eq = spec.arm("own_eq"), spec.arm("ctrl_eq")
    assert len(own_eq.a_items) == len(ctrl_eq.a_items) == len(spec.seed_rows) + spec.k


def test_seed_free_arms_hold_no_seed_or_same_source_sentence():
    lg, idx, cands, _ = _three_sel()
    for spec in control2.build_pairs(lg, idx, cands):
        seed_srcs = {checks._source_of(lg, s) for s in spec.seeds}
        for arm in ("own_sf", "ctrl_sf"):
            for _id, cid, _s in spec.arm(arm).a_items:
                assert cid not in spec.seeds
                assert checks._source_of(lg, cid) not in seed_srcs


def test_the_two_arms_share_no_non_seed_sentence():
    lg, idx, cands, _ = _three_sel()
    for spec in control2.build_pairs(lg, idx, cands):
        own = {(cid, i) for cid, i, _s in spec.own_other}
        assert own.isdisjoint({(cid, i) for cid, i, _s in spec.donor_other})


def test_a_pair_with_an_empty_pool_is_not_discriminable_and_never_judged():
    class _Exploding:
        model_id = "x"

        def ask(self, prompt):
            raise AssertionError("must not be asked")

    seed1 = a_claim("Diagnostic tests should be selected based on failure likelihood.", source_id="s1")
    seed2 = a_claim("Sampling rate should be selected based on the suspected event.", source_id="s2")
    lg = ledger([seed1, seed2])
    idx = link.build_index(lg)
    cands = [c for c in lenses.run_all(lg, idx, link.SETTING_1) if c.lens == "SEL"]
    specs = control2.build_pairs(lg, idx, cands)
    assert specs and all(s.k == 0 for s in specs)
    pairs = control2.judge_pairs(specs, _Exploding())
    assert all(not p.discriminable and p.states == {} for p in pairs)


# --------------------------------------------------------------------------- donor pairing

def test_donor_ties_break_on_sorted_seed_ids_then_lens():
    stems = [frozenset({"a"}), frozenset({"a"}), frozenset({"a"})]
    keys = [(("c-2",), "SEL"), (("c-9",), "SEL"), (("c-1",), "SEL")]
    j, tied = control2.nearest_donor(0, stems, keys)
    assert (j, tied) == (2, True)
    j, tied = control2.nearest_donor(0, [frozenset({"a", "b"}), frozenset({"a"}), frozenset({"a", "b"})], keys)
    assert (j, tied) == (2, False)


def test_donor_pairing_does_not_move_with_the_config_hash(monkeypatch):
    lg, idx, cands, _ = _three_sel()
    before = [(s.seeds, s.donor_seeds) for s in control2.build_pairs(lg, idx, cands)]
    monkeypatch.setattr(config, "CONFIG_SHA256", "f" * 64)
    after = [(s.seeds, s.donor_seeds) for s in control2.build_pairs(lg, idx, cands)]
    assert before == after


# --------------------------------------------------------------------------- summary

def test_summary_reports_both_splits_for_both_comparisons():
    lg, idx, cands, _ = _three_sel()
    summary = control2.summarise(control2.run(lg, idx, FakeJudge(), cands))
    for comparison in ("equal_cap", "seed_free"):
        for split in ("closed_or_partial", "closed"):
            row = _row(summary, comparison, split)
            assert {"own_rate", "control_rate", "diff", "ci95", "n", "clusters"} <= row.keys()
    assert summary["total"]["n_pairs"] == 3


def test_intervals_resample_by_seed_claim():
    pairs = [control2.Pair(lens="SEL", seeds=(f"c{i % 2}",), donor_seeds=("d",), donor_tied=False,
                           k=1, own_pool=1, donor_pool=1,
                           states={"own_eq": "closed", "ctrl_eq": "open",
                                   "own_sf": "closed", "ctrl_sf": "open"})
             for i in range(6)]
    row = _row(control2.summarise(pairs))
    assert row["clusters"] == 2 and row["n"] == 6
    assert row["ci95"] == [1.0, 1.0]


def test_partial_counts_only_in_the_closed_or_partial_split():
    pairs = [control2.Pair(lens="SEL", seeds=(f"c{i}",), donor_seeds=("d",), donor_tied=False,
                           k=1, own_pool=1, donor_pool=1,
                           states={"own_eq": "partial", "ctrl_eq": "open",
                                   "own_sf": "partial", "ctrl_sf": "open"})
             for i in range(3)]
    summary = control2.summarise(pairs)
    assert _row(summary, split="closed_or_partial")["diff"] == 1.0
    assert _row(summary, split="closed")["diff"] == 0.0


# --------------------------------------------------------------------------- L7.3 discrimination

def test_planted_positive_fires():
    lg, idx, cands, seed_i = _three_sel()
    pairs = control2.run(lg, idx, FakeJudge(), cands)
    planted = next(p for p in pairs if seed_i.claim_id in p.seeds)
    assert planted.discriminable
    assert planted.states["own_sf"] == "closed" and planted.states["ctrl_sf"] != "closed"
    assert planted.states["own_eq"] == "closed" and planted.states["ctrl_eq"] != "closed"
    summary = control2.summarise(pairs)
    for comparison in ("equal_cap", "seed_free"):
        assert _row(summary, comparison)["diff"] > 0


def test_length_matched_random_word_stand_in_does_not_fire():
    planted = "CLOSES_HERE: choose the test whose failure likelihood is highest."
    stand_in = _length_matched_random(planted, random.Random(7), keep={"failure", "likelihood"})
    assert len(stand_in) == len(planted) and "CLOSES_HERE" not in stand_in
    lg, idx, cands, seed_i = _three_sel(planted=stand_in)
    planted_lg, planted_idx, planted_cands, _ = _three_sel(planted=planted)
    spec = next(s for s in control2.build_pairs(lg, idx, cands) if seed_i.claim_id in s.seeds)
    planted_spec = next(s for s in control2.build_pairs(planted_lg, planted_idx, planted_cands)
                        if seed_i.claim_id in s.seeds)
    assert spec.k >= 1
    assert sorted(len(s) for _c, _i, s in spec.own_other) == sorted(
        len(s) for _c, _i, s in planted_spec.own_other)
    summary = control2.summarise(control2.run(lg, idx, FakeJudge(), cands))
    for comparison in ("equal_cap", "seed_free"):
        assert _row(summary, comparison)["diff"] <= 0


def test_a_judge_reading_only_the_sentence_count_cannot_separate_the_arms():
    class _CountJudge:
        model_id = "count"

        def ask(self, prompt):
            ids = re.findall(r"^(\d+):", prompt, re.MULTILINE)
            return {"states": ids[:1] if len(ids) >= 2 else [], "partially": []}

    lg, idx, cands, _ = _three_sel()
    pairs = control2.run(lg, idx, _CountJudge(), cands)
    assert any(p.discriminable for p in pairs)
    for p in pairs:
        if p.discriminable:
            assert p.states["own_eq"] == p.states["ctrl_eq"]
            assert p.states["own_sf"] == p.states["ctrl_sf"]


def test_verdict_names_the_three_outcomes():
    fire = {"diff": 0.3, "ci95": [0.1, 0.5]}
    null = {"diff": 0.0, "ci95": [-0.1, 0.1]}
    assert control2.verdict(fire, planted_fires=True, stand_in_fires=False) == "discriminates"
    assert control2.verdict(null, planted_fires=True, stand_in_fires=False) == "uninformative"
    assert control2.verdict(fire, planted_fires=False, stand_in_fires=False) == "design-wrong"
    assert control2.verdict(fire, planted_fires=True, stand_in_fires=True) == "design-wrong"


# --------------------------------------------------------------------------- audit of the old control

def test_audit_counts_a_seed_that_fills_the_cap_and_a_truncated_control_arm():
    long_seed = " ".join(f"Diagnostic tests should be selected based on failure likelihood {i}."
                         for i in range(config.JUDGE_A_CAP + 2))
    lg, idx, cands, _ = _three_sel(seed_i_exact=long_seed)
    audit = control2.audit_current(lg, "ledgersha", idx, FakeJudge(), cands)
    assert audit["n_pairs"] == 3
    assert audit["seed_fills_cap"] == 1
    assert audit["own_truncated"] == 0
    assert {"identical_arms", "closure_on_seed_only", "control_truncated", "donor_tied",
            "own_other_empty", "donor_other_empty"} <= audit.keys()


def test_length_matched_keeps_only_pairs_with_close_non_seed_lengths():
    lg, idx, cands, _ = _three_sel()
    specs = control2.build_pairs(lg, idx, cands)
    pairs = control2.judge_pairs(specs, FakeJudge())
    kept = control2.length_matched(specs, pairs, tol=0.25)["n_discriminable"]
    expect = sum(1 for s in specs if s.k and abs(sum(len(r[2]) for r in s.own_other) -
                 sum(len(r[2]) for r in s.donor_other)) <= 0.25 * max(
                 sum(len(r[2]) for r in s.own_other), sum(len(r[2]) for r in s.donor_other)))
    assert kept == expect
    assert control2.length_matched(specs, pairs, tol=0.0)["n_discriminable"] <= kept
    assert control2.length_matched(specs, pairs, tol=1.0)["n_discriminable"] == sum(s.k >= 1 for s in specs)


def test_the_length_stand_in_reports_its_cut_and_interval():
    lg, idx, cands, _ = _three_sel()
    out = control2.length_stand_in(control2.build_pairs(lg, idx, cands))
    assert {"median_chars", "diff", "ci95", "n"} <= out.keys()


@pytest.mark.parametrize("comparison", ["equal_cap", "seed_free"])
def test_best_reachable_difference_is_the_discriminable_share(comparison):
    lg, idx, cands, _ = _three_sel()
    summary = control2.summarise(control2.run(lg, idx, FakeJudge(), cands))
    row = summary["by_lens"]["SEL"]
    assert row["best_reachable_diff"] == row["n_discriminable"] / row["n_pairs"]


# --------------------------------------------------------------------------- I1c: seed-free donor arm

def test_the_donor_arm_carries_no_donor_seed_sentence_or_donor_seed_source():
    lg, idx, cands, _ = _three_sel()
    specs = control2.build_pairs(lg, idx, cands)
    for spec in specs:
        donor = next(s for s in specs if s.seeds == spec.donor_seeds)
        donor_srcs = {checks._source_of(lg, s) for s in donor.seeds}
        for cid, _i, _s in spec.donor_other:
            assert cid not in donor.seeds
            assert checks._source_of(lg, cid) not in donor_srcs


GDPR_V1 = Path(__file__).resolve().parents[2] / "reconstruct/runs/20260928T135354Z-eb840a85b7d1/ledger.json"


def _gdpr_v1():
    from residual.ledger import Ledger
    lg = Ledger.from_json(GDPR_V1.read_text())
    idx = link.build_index(lg)
    return lg, idx, lenses.run_all(lg, idx, link.SETTING_1)


@pytest.mark.parametrize("build", [_three_sel, _gdpr_v1])
def test_both_arms_drop_the_seed_sources_of_both_candidates(build):
    if build is _gdpr_v1 and not GDPR_V1.exists():
        pytest.skip("reconstruct/runs/ not present")
    lg, idx, cands = build()[:3]
    specs = control2.build_pairs(lg, idx, cands)
    if build is _gdpr_v1:
        legacy = control2.build_pairs(lg, idx, cands, legacy_donor_seed=True)
        assert any(r[0] in s.donor_seeds for s in legacy for r in s.own_other)
    for spec in specs:
        excluded = {checks._source_of(lg, s) for s in (*spec.seeds, *spec.donor_seeds)}
        for rows in (spec.own_other, spec.donor_other):
            assert not {checks._source_of(lg, cid) for cid, _i, _s in rows} & excluded


def test_the_legacy_donor_pool_starts_with_the_donor_seed_as_in_I1():
    lg, idx, cands, _ = _three_sel()
    specs = control2.build_pairs(lg, idx, cands, legacy_donor_seed=True)
    assert any(spec.donor_other and spec.donor_other[0][0] in spec.donor_seeds for spec in specs)


def test_the_seed_free_comparison_holds_no_seed_text_of_either_candidate():
    lg, idx, cands, _ = _three_sel()
    specs = control2.build_pairs(lg, idx, cands)
    seed_text = {lg.by_id[s].assertion for spec in specs for s in spec.seeds}
    for spec in specs:
        for arm in ("own_sf", "ctrl_sf"):
            assert not {sent for _n, _c, sent in spec.arm(arm).a_items} & seed_text


def test_verdict_is_design_wrong_when_the_length_only_judge_passes():
    fire = {"diff": 0.3, "ci95": [0.1, 0.5]}
    assert control2.verdict(fire, planted_fires=True, stand_in_fires=False,
                            length_row={"diff": 0.28, "ci95": [0.06, 0.49]}) == "design-wrong"
    assert control2.verdict(fire, planted_fires=True, stand_in_fires=False,
                            length_row={"diff": 0.11, "ci95": [-0.08, 0.32]}) == "discriminates"
    assert control2.verdict(fire, planted_fires=True, stand_in_fires=False,
                            length_row={"n": 0}) == "discriminates"


# --------------------------------------------------------------------------- ADR 0009

_SIDECAR = {"config": {"models": {"extractor": {"family": "anthropic"}, "verifier": {"family": "openai"}}}}


def _arm(specs, judge_model="qwen2.5:7b-instruct", ledger_sha256="L"):
    return {"judge_model": judge_model, "ledger_sha256": ledger_sha256,
            "pairs_sha256": control2.pairs_sha256(specs)}


def test_a_live_same_family_judge_runs_only_beside_an_other_family_arm_on_the_same_pairs():
    lg, idx, cands, _ = _three_sel()
    specs = control2.build_pairs(lg, idx, cands)
    problem = control2.parallel_arm_problem
    assert problem("qwen2.5:7b-instruct", _SIDECAR, None, "L", specs) is None
    assert problem("gpt-6.1-sol", _SIDECAR, _arm(specs), "L", specs) is None
    assert "--parallel-arm" in problem("gpt-6.1-sol", _SIDECAR, None, "L", specs)
    assert "--sidecar" in problem("gpt-6.1-sol", None, _arm(specs), "L", specs)
    assert "other-family" in problem("gpt-6.1-sol", _SIDECAR, _arm(specs, "gpt-5.6-luna"), "L", specs)
    assert "different ledger" in problem("gpt-6.1-sol", _SIDECAR, _arm(specs, ledger_sha256="M"), "L", specs)
    assert "different pairs" in problem("gpt-6.1-sol", _SIDECAR, _arm(specs[:-1]), "L", specs)
    legacy = control2.build_pairs(lg, idx, cands, legacy_donor_seed=True)
    assert [(a.lens, a.seeds, a.k) for a in legacy] == [(b.lens, b.seeds, b.k) for b in specs]
    assert "different pairs" in problem("gpt-6.1-sol", _SIDECAR, _arm(legacy), "L", specs)
    assert "different pairs" in problem("gpt-6.1-sol", _SIDECAR, {**_arm(specs), "pairs_sha256": None}, "L", specs)


def _cli_inputs(tmp_path):
    lg, *_ = _three_sel()
    (tmp_path / "ledger.json").write_text(lg.to_json())
    (tmp_path / "sidecar.json").write_text(json.dumps(_SIDECAR))
    return ["--ledger", str(tmp_path / "ledger.json"), "--sidecar", str(tmp_path / "sidecar.json"),
            "--domain", "test", "--out", str(tmp_path / "out")]


def test_control2_refuses_a_live_same_family_judge_before_any_call(tmp_path, capsys):
    with pytest.raises(SystemExit):
        control2.main([*_cli_inputs(tmp_path), "--judge", "openai", "--model", "gpt-6.1-sol",
                       "--max-usd", "1"])
    assert "--parallel-arm" in capsys.readouterr().err
    assert not (tmp_path / "out" / "closure_judgements.json").exists()


def test_control2_replay_cache_miss_names_judge_openai_for_an_openai_model(tmp_path):
    with pytest.raises(judge_mod.JudgeCacheMiss, match="--judge openai"):
        control2.main([*_cli_inputs(tmp_path), "--model", "gpt-6.1-sol"])
