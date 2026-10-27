"""Stop A counts per codebase, as D1b computes them (build_sheet.arm_of and match), plus the open
share and per-origin split. Synthetic topics and states; no model, no network."""
import stop_a


def _topic(tid, versions, lens="WHY", origin="owner", words=40, sim=0.15):
    return {"topic_id": tid, "versions": versions, "lens": lens, "k_band": "1", "ledgers": "cheap",
            "source_origin": origin, "words": words, "similarity": sim}


def test_counts_follow_d1b_arm_rule_and_matching():
    topics = [_topic("T1", [("cheap", "a")]), _topic("T2", [("cheap", "b")]),
              _topic("T3", [("cheap", "c"), ("cheap", "d")]), _topic("T4", [("cheap", "e")], origin="outside")]
    states = {("cheap", "a"): {"g": "open"}, ("cheap", "b"): {"g": "closed"},
              ("cheap", "c"): {"g": "open"}, ("cheap", "d"): {"g": "closed"}, ("cheap", "e"): {"g": "open"}}
    out = stop_a.counts(topics, states, ("g",))
    assert out == {"topics": 4, "all_open": 2, "all_closed": 1, "mixed": 1, "open_share": 0.5,
                   "matched_pairs_upper_bound": 1, "reaches_floor": False}


def test_both_arms_must_agree_for_a_topic_to_count():
    topics = [_topic("T1", [("cheap", "a")])]
    states = {("cheap", "a"): {"g": "open", "s": "closed"}}
    assert stop_a.counts(topics, states, ("g", "s"))["mixed"] == 1
    assert stop_a.counts(topics, states, ("g",))["all_open"] == 1


def test_floor_is_ten_balanced_pairs():
    gaps = [_topic(f"G{i}", [("cheap", f"g{i}")]) for i in range(10)]
    covs = [_topic(f"C{i}", [("cheap", f"c{i}")]) for i in range(10)]
    states = {**{("cheap", f"g{i}"): {"g": "open"} for i in range(10)},
              **{("cheap", f"c{i}"): {"g": "closed"} for i in range(10)}}
    out = stop_a.counts(gaps + covs, states, ("g",))
    assert out["matched_pairs_upper_bound"] == 10 and out["reaches_floor"] is True


def test_noise_stand_in_reaches_the_floor_on_a_large_pool_and_not_on_a_small_one():
    big = [_topic(f"T{i}", [("cheap", f"v{i}")]) for i in range(60)]
    assert stop_a.noise_floor_rate(big, p_open=0.5, p_closed=0.5, seeds=50) > 0.9
    assert stop_a.noise_floor_rate(big[:8], p_open=0.5, p_closed=0.5, seeds=50) == 0.0


def test_per_topic_noise_gives_every_version_of_a_topic_one_state():
    multi = [_topic(f"T{i}", [("cheap", f"a{i}"), ("top", f"b{i}")]) for i in range(60)]
    by_version = stop_a.noise_floor_rate(multi, p_open=0.3, p_closed=0.5, seeds=50)
    by_topic = stop_a.noise_floor_rate(multi, p_open=0.3, p_closed=0.5, seeds=50, per_topic=True)
    assert by_topic > by_version


def test_version_marginals_count_every_judged_version():
    states = {("c", "a"): {"g": "open"}, ("c", "b"): {"g": "closed"}, ("c", "d"): {"g": "partial"},
              ("c", "e"): {"g": "open"}}
    assert stop_a.marginals(states, "g") == {"open": 0.5, "closed": 0.25}


def test_by_origin_splits_topics():
    topics = [_topic("T1", [("cheap", "a")]), _topic("T2", [("cheap", "b")], origin="outside")]
    states = {("cheap", "a"): {"g": "open"}, ("cheap", "b"): {"g": "closed"}}
    split = stop_a.by_origin(topics, states, ("g",))
    assert split["owner"]["all_open"] == 1 and split["outside"]["all_closed"] == 1
