"""G2 (plan §2.2): a topicality-controlled closure check. Fake judges only; no network."""
import pytest

import g2
from gapmap import standins


def _topic(i, cluster=None, split="gate"):
    return {"topic_id": f"t{i:02d}", "cluster": cluster or f"c{i}", "split": split, "lens": "WHY",
            "seed_text": f"Compute the band on the training window for series {i}.",
            "question": "Does any sentence state why this is done?",
            "seed_rows": [["s", 0, f"Compute the band on the training window for series {i}."]],
            "background_rows": [["b", 0, "Wikipedia notes that Pearson coefficients lie in a range."],
                                ["b", 1, "The term is used interchangeably in some fields."]]}


def _insert(i, p_marker):
    p = (f"Using the training window for series {i} keeps holdout values out of the band fit."
         if not p_marker else
         f"The band uses the training window for series {i} because holdout values would leak into it.")
    n = (f"The band for series {i} uses the training window, and its default width was set in 2024."
         if not p_marker else
         f"The band uses the training window for series {i} because that window is the default for it.")
    return {"P": p, "N": n, "N_plus": [f"The training window for series {i} is the first eighty percent.",
                                       f"The band for series {i} is drawn in grey on the plot."],
            "P_marker": p_marker, "N_marker": p_marker}


class Oracle:
    model_id = "oracle"

    def __init__(self, inserts):
        self.ps = {v["P"] for v in inserts.values()}

    def ask(self, prompt):
        p = standins.parse(prompt)
        return {"states": [i for i, s in p.sentences if s in self.ps], "partially": []}


def _set(n=18, clusters=None):
    topics = [_topic(i, cluster=(clusters(i) if clusters else None)) for i in range(n)]
    inserts = {t["topic_id"]: _insert(i, p_marker=i % 2 == 0) for i, t in enumerate(topics)}
    return topics, inserts


def test_each_topic_gets_five_arms_that_differ_only_in_the_inserted_sentences():
    topics, inserts = _set(1)
    arms = g2.arms(topics[0], inserts["t00"])
    assert set(arms) == {"0", "P", "N", "N+", "R"}
    base = [r[2] for r in arms["0"]]
    for name in ("P", "N", "R"):
        assert [r[2] for r in arms[name] if r[0] != g2.INSERT] == base
    assert sum(r[0] == g2.INSERT for r in arms["N+"]) == 3


def test_the_random_letter_arm_keeps_the_plant_word_lengths_and_is_seeded():
    topics, inserts = _set(1)
    r1 = [r[2] for r in g2.arms(topics[0], inserts["t00"])["R"] if r[0] == g2.INSERT][0]
    r2 = [r[2] for r in g2.arms(topics[0], inserts["t00"])["R"] if r[0] == g2.INSERT][0]
    assert r1 == r2
    assert [len(w) for w in r1.split()] == [len(w) for w in inserts["t00"]["P"].split()]


def test_an_insert_whose_n_is_not_matched_to_p_is_rejected():
    topics, inserts = _set(1)
    ok = inserts["t00"]
    assert g2.insert_problem(topics[0], ok) is None
    short = {**ok, "N": "The band is grey."}
    assert "length" in g2.insert_problem(topics[0], short)
    off = {**ok, "N": "Wikipedia says the Pearson coefficient range sits within a band of several fixed sizes today."}
    assert "overlap" in g2.insert_problem(topics[0], off)


def test_the_oracle_passes_and_every_stand_in_fails():
    topics, inserts = _set()
    res = g2.evaluate(topics, inserts, Oracle(inserts), split="gate")
    assert res["passes"] and res["diff"] == 1.0
    for judge in g2.stand_ins(topics, inserts):
        res = g2.evaluate(topics, inserts, judge, split="gate")
        assert not res["passes"], judge.model_id


def test_a_judge_that_closes_every_on_topic_insert_fails_on_n():
    topics, inserts = _set()

    class Topical:
        model_id = "topical"

        def ask(self, prompt):
            p = standins.parse(prompt)
            return {"states": [i for i, s in p.sentences if "series" in s and "Compute" not in s], "partially": []}

    res = g2.evaluate(topics, inserts, Topical(), split="gate")
    assert res["rates"]["N"] == 1.0 and not res["passes"]


def test_the_lower_bound_resamples_clusters_not_topics():
    topics, inserts = _set(18, clusters=lambda i: f"c{i // 6}")

    class Half:
        model_id = "half"

        def __init__(self):
            self.ps = {inserts[f"t{i:02d}"]["P"] for i in range(18) if i < 12}

        def ask(self, prompt):
            p = standins.parse(prompt)
            return {"states": [i for i, s in p.sentences if s in self.ps], "partially": []}

    clustered = g2.evaluate(topics, inserts, Half(), split="gate")
    flat = g2.evaluate([{**t, "cluster": t["topic_id"]} for t in topics], inserts, Half(), split="gate")
    assert clustered["lower90"] < flat["lower90"]


def test_only_the_named_split_is_scored():
    topics, inserts = _set(4)
    topics[0]["split"] = "selection"
    res = g2.evaluate(topics, inserts, Oracle(inserts), split="selection")
    assert res["n_topics"] == 1


def test_the_pass_rule_needs_every_term():
    good = {"diff": 0.6, "lower90": 0.35, "rates": {"0": 0.0, "P": 0.7, "N": 0.1, "N+": 0.2, "R": 0.0}}
    assert g2.passes(good)
    for change in ({"diff": 0.45}, {"lower90": 0.29}, {"rates": {**good["rates"], "N": 0.3}},
                   {"rates": {**good["rates"], "N+": 0.3}}, {"rates": {**good["rates"], "R": 0.12}},
                   {"rates": {**good["rates"], "0": 0.3}}):
        assert not g2.passes({**good, **change}), change


def test_running_refuses_unconfirmed_fixtures():
    topics, inserts = _set(2)
    with pytest.raises(g2.Unconfirmed):
        g2.require_confirmed(topics, inserts, {"t00": {"P": True, "N": True, "N_plus": True, "seed_open": True}})


def test_closing_markers_must_be_balanced_between_p_and_n_over_the_set():
    topics, inserts = _set(4)
    assert g2.marker_problem(topics, inserts) is None
    for t in topics:
        inserts[t["topic_id"]] = {**inserts[t["topic_id"]],
                                  "P": inserts[t["topic_id"]]["P"].replace("keeps", "because it keeps")}
    assert "marker" in g2.marker_problem(topics, inserts)


def test_any_undecided_arm_makes_the_verdict_incomplete_not_fail():
    topics, inserts = _set()

    class Sometimes(Oracle):
        def ask(self, prompt):
            return None if "series 3 " in prompt else super().ask(prompt)

    res = g2.evaluate(topics, inserts, Sometimes(inserts), split="gate")
    assert res["undecided"] > 0 and res["complete"] is False and res["passes"] is False


def test_topics_the_owner_dropped_are_left_out_before_any_check():
    topics, inserts = _set(3)
    kept = g2.kept_topics(topics, {"_dropped": {"t01": "seed states the element"}})
    assert [t["topic_id"] for t in kept] == ["t00", "t02"]


def test_a_seed_is_dropped_only_when_every_reader_closes_its_no_insert_arm():
    states = {"t1": {"a": "closed", "b": "closed"}, "t2": {"a": "closed", "b": "open"}, "t3": {"a": "open", "b": "open"}}
    assert g2.seed_drops(states) == ["t1"]


def test_r_is_scored_on_what_the_random_letters_add_over_the_no_insert_arm():
    topics, inserts = _set()
    seeds_close = {"t00", "t01"}

    class SeedReader(Oracle):
        def ask(self, prompt):
            p = standins.parse(prompt)
            hit = [i for i, s in p.sentences if s.startswith("Compute") and p.seed.endswith(("series 0.", "series 1."))]
            return {"states": hit, "partially": []} if hit else super().ask(prompt)

    res = g2.evaluate(topics, inserts, SeedReader(inserts), split="gate")
    assert res["rates"]["R"] == pytest.approx(2 / 18) and res["rates"]["0"] == pytest.approx(2 / 18)
    assert res["R_excess"] == 0.0 and res["passes"]


def test_a_judge_closing_on_random_letters_still_fails_r():
    topics, inserts = _set()

    class Gibberish(Oracle):
        def ask(self, prompt):
            p = standins.parse(prompt)
            hit = [i for i, s in p.sentences if s in self.ps or (s.islower() and " " in s and not any(c in s for c in ".,"))]
            return {"states": hit, "partially": []}

    res = g2.evaluate(topics, inserts, Gibberish(inserts), split="gate")
    assert res["R_excess"] > 0.10 and not res["passes"]
