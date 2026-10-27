"""RT (plan §1): arms, citation scoring, part I rule, insert checks, owner gate. Fake judges only."""
import pytest

import rt
import standins_t as st

Q = "Does any sentence state why this is done (the reason or the failure it prevents)?"


def _topic(i, cluster=None, k=8, split="d1"):
    bg = [[f"b{i}", n, f"Background sentence {n} about screening the register for series {i}."] for n in range(k)]
    return {"topic_id": f"t{i:02d}", "split": split, "cluster": cluster or f"c{i}", "lens": "WHY",
            "seed_text": f"Screen the register for series {i} before release.", "question": Q,
            "background_rows": bg, "probe": ["screen", "register", "series", "release"]}


def _ins(i):
    return {"P": f"Screening the register early keeps series {i} faults away from customers after a release.",
            "N": f"Screening the register for series {i} is logged in form B-7 by the release desk each Monday."}


def _set(n=12):
    topics = [_topic(i) for i in range(n)]
    return topics, {t["topic_id"]: _ins(i) for i, t in enumerate(topics)}


class Oracle:
    model_id = "oracle"

    def __init__(self, inserts):
        self.p = {v["P"] for v in inserts.values()}

    def ask(self, prompt):
        ids = [i for i, s in st.standins.parse(prompt).sentences if s in self.p]
        return {"states": [int(i) for i in ids], "partially": [], "reason": ""}


class CiteAll:
    model_id = "all"

    def ask(self, prompt):
        return {"states": [int(i) for i, _s in st.standins.parse(prompt).sentences], "partially": []}


class Broken:
    model_id = "broken"

    def ask(self, prompt):
        return {}


def test_background_is_capped_at_seven_and_the_insert_sits_at_one_position_in_every_arm():
    t, ins = _topic(1), _ins(1)
    arms = rt.arm_rows(t, ins)
    assert len(arms["0"]) == 7 and all(len(arms[a]) == 8 for a in ("P", "N", "R"))
    pos = {a: [r[0] for r in arms[a]].index(rt.INSERT) for a in ("P", "N", "R")}
    assert len(set(pos.values())) == 1
    assert [r for r in arms["P"] if r[0] != rt.INSERT] == arms["0"]
    assert rt.arm_rows(_topic(1, k=3), ins)["0"] == [tuple(r) for r in _topic(1, k=3)["background_rows"]]


def test_random_letters_keep_p_word_lengths():
    p = _ins(1)["P"]
    assert [len(w) for w in rt.letters(p).split()] == [len(w) for w in p.split()]


def test_oracle_passes_part_one():
    topics, ins = _set()
    res = rt.evaluate(topics, ins, Oracle(ins))
    assert res["part1"]["passes"] and res["part1"]["diff"] == 1.0 and res["part1"]["lower90"] == 1.0
    assert res["complete"]


def test_a_judge_citing_every_sentence_fails_on_n_and_r():
    topics, ins = _set()
    res = rt.evaluate(topics, ins, CiteAll())
    assert not res["part1"]["passes"] and res["part1"]["hit"]["N"] == 1.0


def test_overlap_stand_in_fails_when_n_is_at_least_as_on_topic():
    topics, ins = _set()
    prompts = rt.prompts(topics, ins)
    j = st.calibrate("overlap", st.STATS["overlap"], "ge", prompts)
    assert not rt.evaluate(topics, ins, j)["part1"]["passes"]


def test_undecided_makes_the_run_incomplete_not_a_fail():
    topics, ins = _set()
    res = rt.evaluate(topics, ins, Broken())
    assert not res["complete"] and res["part1"]["passes"] is False and res["verdict"] == "incomplete"


def test_cited_background_keys_are_recorded():
    topics, ins = _set(2)
    res = rt.evaluate(topics, ins, CiteAll())
    assert ("b0", 0) in {tuple(k) for k in res["cited_background"]["t00"]}


class CitesOneRowPartlyAnother:
    model_id = "one-row"

    def ask(self, prompt):
        return {"states": [1], "partially": [2]}


def test_citations_map_to_rows_by_number_even_when_rows_share_a_claim():
    t = _topic(1, k=3)
    t["background_rows"] = [["same", 0, "First sentence of a claim."], ["same", 1, "Second sentence of a claim."],
                            ["other", 0, "Another claim entirely."]]
    t["topic_id"] = "tx"
    while rt.position(t) != 3:
        t["topic_id"] += "x"
    res = rt.evaluate([t], {t["topic_id"]: _ins(1)}, CitesOneRowPartlyAnother())
    assert res["cited_background"][t["topic_id"]] == [["same", 0]]
    assert res["partial_background"][t["topic_id"]] == [["same", 1]]


def test_lower_bound_resamples_whole_clusters():
    per = [("a", 1), ("a", 1), ("b", 0), ("b", 0)]
    assert rt.lower90(per) == 0.0
    assert rt.lower90([("a", 1), ("b", 1)]) == 1.0


def test_insert_problem_strict_checks():
    t = _topic(1)
    assert rt.insert_problem(t, _ins(1), strict=False) is None
    bad = dict(_ins(1), N="Short.")
    assert "length" in rt.insert_problem(t, bad, strict=False)
    longer = dict(_ins(1), N=_ins(1)["P"] + " Screen register series release screen.")
    assert rt.insert_problem(t, longer, strict=True) is not None


def test_insert_problem_two_sided_overlap_and_novelty():
    t = _topic(1)
    p = "Doing this first stops faults reaching customers in the field later on."
    n_over = "Screen register series release screen register series release screen."
    assert "overlap" in (rt.insert_problem(t, {"P": p, "N": n_over + " " * (len(p) - len(n_over))}, strict=True) or "")


def test_lexicon_balance_over_a_split():
    topics, ins = _set(4)
    assert rt.lexicon_problem(topics, ins) is None
    marked = {k: dict(v, P=v["P"].replace("keeps", "because it keeps")) for k, v in ins.items()}
    assert "lexicon" in rt.lexicon_problem(topics, marked)


def test_gdpr_split_refuses_without_the_owner_labels():
    topics, ins = _set(2)
    for t in topics:
        t["split"] = "gdpr"
    with pytest.raises(rt.Unconfirmed):
        rt.require_confirmed(topics, ins, {})
    rt.require_confirmed(topics, ins, {t["topic_id"]: {"P": True, "N": True} for t in topics})


def test_stand_in_report_flags_a_passing_stand_in_and_marks_the_split_unusable():
    topics, ins = _set()
    rep = rt.stand_in_report(topics, ins, extra=[Oracle(ins)])
    assert not rep["usable"] and "oracle" in rep["passing"]
    rep = rt.stand_in_report(topics, ins)
    assert rep["usable"], rep["passing"]


def test_part_two_share_of_non_element_citations():
    labels = {"k1": False, "k2": False, "k3": True, "k4": True, "k5": True, "k6": True}
    assert rt.part_two(["k1", "k2", "k3", "k4", "k5", "k6"], labels) == {
        "cited": 6, "non_element": 2, "share": 2 / 6, "passes": False, "trivial": False}
    assert rt.part_two(["k3"], labels)["trivial"] is True
