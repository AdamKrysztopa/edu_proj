"""The D1b sheet builder (plan §3.1-3.3): topic clusters, arm assignment by agreement, matching,
and sealing. Synthetic rows; no model, no network."""
import json
import subprocess

import pytest

import build_sheet as bs


def _row(ledger, tid, quote, lens="WHY", k=1, origin="owner", words=40, sim=0.15, anchor=None):
    return {"ledger": ledger, "test_id": tid, "lens": lens, "quote": quote, "anchor": anchor or tid,
            "k_topic": k, "source_origin": origin, "words": words, "similarity": sim,
            "question_text": f'Sources say: "{quote}". Why?'}


def test_versions_of_one_topic_across_ledgers_cluster_together():
    rows = [_row("cheap", "a", "compute the band on the training window only"),
            _row("top", "b", "compute the band on the training window only please"),
            _row("cheap", "c", "the surrogate count sets the significance floor")]
    topics = bs.cluster(rows)
    assert sorted(len(t["versions"]) for t in topics) == [1, 2]


def test_a_shared_anchor_clusters_even_when_the_quotes_differ():
    rows = [_row("cheap", "a", "first wording of a rule", anchor="X"),
            _row("top", "b", "a quite different second phrasing", anchor="X")]
    assert len(bs.cluster(rows)) == 1


def test_a_topic_enters_an_arm_only_when_every_version_and_judge_agree():
    topic = {"versions": [("cheap", "a"), ("top", "b")]}
    open_all = {("cheap", "a"): {"local": "open", "sol": "open"}, ("top", "b"): {"local": "open", "sol": "open"}}
    assert bs.arm_of(topic, open_all) == "gap"
    closed_all = {k: {"local": "closed", "sol": "closed"} for k in open_all}
    assert bs.arm_of(topic, closed_all) == "covered"
    mixed = {**open_all, ("top", "b"): {"local": "open", "sol": "closed"}}
    assert bs.arm_of(topic, mixed) is None
    partial = {**open_all, ("cheap", "a"): {"local": "partial", "sol": "open"}}
    assert bs.arm_of(topic, partial) is None
    missing = {("cheap", "a"): {"local": "open"}, ("top", "b"): {"local": "open", "sol": "open"}}
    assert bs.arm_of(topic, missing, judges=("local", "sol")) is None


def _topic(i, arm_lens="WHY", k=1, ledgers=("cheap",), origin="owner", words=40, sim=0.15):
    return {"topic_id": f"T{i}", "lens": arm_lens, "k_band": "1" if k <= 1 else ">=2",
            "ledgers": "+".join(sorted(ledgers)), "source_origin": origin, "words": words, "similarity": sim}


def test_matching_pairs_only_within_a_stratum_and_is_seeded():
    gaps = [_topic(i) for i in range(5)] + [_topic(10, arm_lens="RESULT")]
    covs = [_topic(20 + i, words=42) for i in range(5)] + [_topic(30, origin="outside")]
    pairs = bs.match(gaps, covs, n=5, seed=1)
    assert len(pairs) == 5
    assert all(bs.stratum(g) == bs.stratum(c) for g, c in pairs)
    assert pairs == bs.match(gaps, covs, n=5, seed=1)


def test_matching_returns_fewer_pairs_when_strata_do_not_fill():
    gaps = [_topic(i) for i in range(3)]
    covs = [_topic(20 + i, arm_lens="RESULT") for i in range(3)]
    assert bs.match(gaps, covs, n=3, seed=1) == []


def test_balance_reports_length_and_similarity_means_and_flags_a_length_gap():
    pairs = [(_topic(1, words=40), _topic(2, words=41)), (_topic(3, words=50), _topic(4, words=52))]
    assert bs.balance(pairs)["ok"]
    pairs = [(_topic(1, words=40), _topic(2, words=60))]
    assert not bs.balance(pairs)["ok"]


def test_the_sheet_size_falls_back_to_twelve_then_ten_then_stops():
    gaps = [_topic(i) for i in range(11)]
    covs = [_topic(20 + i) for i in range(11)]
    n, pairs = bs.choose_size(gaps, covs, seed=1)
    assert n == 10 and len(pairs) == 10
    with pytest.raises(bs.TooFew):
        bs.choose_size(gaps[:9], covs[:9], seed=1)


def test_stop_a_fires_on_the_pair_count_alone_not_on_balance():
    gaps = [_topic(i, words=40) for i in range(10)]
    covs = [_topic(20 + i, words=60) for i in range(10)]
    res = bs.count_summary(gaps + covs, gaps, covs, seed=1)
    assert res["matched_pairs_upper_bound"] == 10 and res["balance_ok"] is False
    assert res["stop_at_A"] is False
    res = bs.count_summary(gaps[:9] + covs[:9], gaps[:9], covs[:9], seed=1)
    assert res["stop_at_A"] is True


def test_the_count_also_reports_matched_pairs_beyond_the_sheet_cap():
    gaps = [_topic(i) for i in range(22)]
    covs = [_topic(100 + i) for i in range(22)]
    res = bs.count_summary(gaps + covs, gaps, covs, seed=1)
    assert res["matched_pairs_upper_bound"] == 15 and res["matched_pairs_uncapped"] == 22


def test_near_duplicate_sheet_questions_are_counted():
    quotes = ["compute the band on the training window only", "compute the band on the training window only, never the test",
              "the surrogate count sets the significance floor"]
    items = [{"question_text": f'Sources say: "{q}". Why?'} for q in quotes]
    assert bs.near_duplicates(items) == 1


def test_sealing_round_trips_only_with_the_private_key(tmp_path):
    key = tmp_path / "seal.key"
    pub = tmp_path / "seal.pub"
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-pkeyopt", "rsa_keygen_bits:2048",
                    "-out", str(key)], check=True, capture_output=True)
    subprocess.run(["openssl", "pkey", "-in", str(key), "-pubout", "-out", str(pub)], check=True, capture_output=True)
    (tmp_path / "secret").mkdir()
    (tmp_path / "secret" / "key.json").write_text(json.dumps({"arms": ["gap", "covered"]}))
    sealed = bs.seal(tmp_path / "secret", pub, tmp_path / "sealed")
    assert not (tmp_path / "secret").exists()
    assert b"covered" not in (sealed / "archive.enc").read_bytes()
    out = bs.unseal(sealed, key, tmp_path / "opened")
    assert json.loads((out / "key.json").read_text()) == {"arms": ["gap", "covered"]}
