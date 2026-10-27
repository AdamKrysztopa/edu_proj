"""The blind owner pack (plan §1.2, §1.4, §3 (b)) and the item-3 (b) recount. No network."""
import pack
import reread

H1 = {"seed_text": "Screen the register.", "question": "Does any sentence state why?", "lens": "WHY"}


def test_item_ids_are_stable_and_shared_by_the_same_sentence_under_the_same_header():
    a = pack.Pack()
    a.add(H1, "Sentence one.", {"source": "x"})
    a.add(H1, "Sentence one.", {"source": "y"})
    a.add(dict(H1, seed_text="Other seed."), "Sentence one.", {"source": "z"})
    assert len(a.items) == 2
    iid = pack.item_id(H1, "Sentence one.")
    assert [p["source"] for p in a.key[iid]] == ["x", "y"]


def test_markdown_shows_no_provenance_and_groups_by_header():
    a = pack.Pack()
    a.add(H1, "Sentence one.", {"source": "sol-cited"})
    a.add(H1, "Sentence two.", {"source": "decoy"})
    md = a.markdown()
    assert "sol" not in md and "decoy" not in md and md.count("Screen the register.") == 1
    assert pack.item_id(H1, "Sentence two.") in md


def test_decoys_are_uncited_seeded_and_equal_in_number():
    rows = [f"s{n}" for n in range(10)]
    d = pack.decoys(rows, cited={"s1", "s2"}, n=2, seed="t1")
    assert len(d) == 2 and not {"s1", "s2"} & set(d) and d == pack.decoys(rows, cited={"s1", "s2"}, n=2, seed="t1")


def test_confirmations_need_p_labelled_element_and_n_labelled_not():
    key = {"i1": [{"source": "rt-insert", "split": "gdpr", "topic": "g01", "arm": "P"}],
           "i2": [{"source": "rt-insert", "split": "gdpr", "topic": "g01", "arm": "N"}],
           "i3": [{"source": "rt-insert", "split": "gdpr", "topic": "g02", "arm": "P"}],
           "i4": [{"source": "rt-insert", "split": "gdpr", "topic": "g02", "arm": "N"}]}
    labels = {"i1": True, "i2": False, "i3": True, "i4": True}
    assert pack.confirmations(key, labels) == {"g01": {"P": True, "N": True}, "g02": {"P": True, "N": False}}


def _arm(cited, closed=True):
    return {"closed": closed, "cited": cited}


def test_recount_keeps_only_closures_citing_a_sentence_labelled_element():
    pairs = [{"cluster": f"c{i}", "own": _arm(["e"]), "ctrl": _arm(["x"])} for i in range(6)]
    assert reread.recount(pairs, {"e": True, "x": False})["diff"] == 1.0
    assert reread.recount(pairs, {"e": True, "x": True})["diff"] == 0.0


def test_planted_fake_closes_an_arm_iff_it_holds_a_sentence_labelled_element():
    arms = [{"cluster": "c1", "own": ["e", "x"], "ctrl": ["x"]}, {"cluster": "c2", "own": ["x"], "ctrl": ["e"]}]
    pl = reread.planted(arms, {"e": True, "x": False})
    assert pl[0]["own"] == _arm(["e"]) and pl[0]["ctrl"]["closed"] is False and pl[1]["ctrl"]["closed"] is True


def test_reading_rule():
    good = {"ci95": [0.05, 0.4]}
    flat = {"ci95": [-0.1, 0.2]}
    assert reread.reading(sol=good, standin=flat, planted=good) == "holds"
    assert reread.reading(sol=flat, standin=flat, planted=good) == "does not hold"
    assert reread.reading(sol=good, standin=good, planted=good) == "no reading"
    assert reread.reading(sol=good, standin=flat, planted=flat) == "no reading"
