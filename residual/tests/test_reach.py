from residual import reach as R


def test_eplant_space_respects_the_observed_baseline():
    pts = list(R.eplant_space(n_full=6, a_u_full=2))
    assert all(p["a_u"] <= 2 and p["b"] <= p["a_u"] and p["c"] <= p["n"] - p["a_u"] for p in pts)
    assert all(p["a_g"] == p["a_u"] - p["b"] + p["c"] for p in pts)
    # with every target kept, all baseline adoptions are kept
    assert {p["a_u"] for p in pts if p["n"] == 6} == {2}
    # dropping four of six can drop both adoptions
    assert 0 in {p["a_u"] for p in pts if p["n"] == 2}


def test_eabst_space_caps_false_raw_answers_at_raw_answers():
    pts = list(R.eabst_space(n_items=6, raw_answered=2))
    assert max(p["f_r"] for p in pts) == 2
    assert all(p["f_r"] <= p["n_included"] for p in pts)


def test_regions_and_best_reading():
    def decide(**p):
        return "continue" if p["b"] >= 2 and p["c"] == 0 else "stop"
    reg = R.regions(decide, R.eplant_space(n_full=4, a_u_full=2))
    assert reg.best == "continue"
    assert reg.examples["continue"]["b"] == 2
    reg = R.regions(decide, R.eplant_space(n_full=4, a_u_full=1))
    assert reg.best == "stop" and "continue" not in reg.counts


def test_collect_returns_every_matching_point():
    def decide(**p):
        return "continue" if p["b"] == p["a_u"] == 2 and p["c"] == 0 else "change"
    pts = R.collect(decide, R.eplant_space(n_full=3, a_u_full=2), "continue")
    assert pts and all(p["b"] == 2 for p in pts)
