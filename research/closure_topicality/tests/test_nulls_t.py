"""Topicality-matched donors for control2 and MEC (plan §2.2). Pure functions; no network."""
import nulls_t as nt

SEED, Q = "Screen the register before release.", "Does any sentence state why this is done?"


def test_match_takes_equal_keys_closest_length_and_never_reuses():
    own = [("o", 0, "aaaa"), ("o", 1, "bbbbbbbb")]
    pool = [("p", 0, "x" * 8), ("p", 1, "y" * 5), ("p", 2, "z" * 3)]
    key = lambda s: 1
    assert nt.match(own, pool, key) == [("p", 1, "y" * 5), ("p", 0, "x" * 8)]


def test_match_returns_none_when_any_own_sentence_has_no_equal_key():
    own = [("o", 0, "screen register"), ("o", 1, "nothing")]
    pool = [("p", 0, "nothing at all")]
    key = lambda s: len(s.split())
    assert nt.match(own, pool, key) is None


def test_match_never_returns_an_excluded_row():
    own = [("o", 0, "same")]
    assert nt.match(own, [("o", 0, "same")], lambda s: 0, exclude={("o", 0)}) is None


def test_overlap_key_counts_seed_and_question_words():
    assert nt.overlap_key(SEED, Q)("screen the register now") == 2


def test_stand_in_rows_report_a_stand_in_that_favours_the_own_arm():
    pairs = [nt.ArmPair(cluster=f"c{i}", seed_text=SEED, question=Q,
                        own=[("o", 0, "Screen the register before every release.")],
                        ctrl=[("d", 0, "Coffee is served in the canteen daily at nine for all staff.")]) for i in range(6)]
    rows = nt.stand_in_rows(pairs, source_of={})
    assert rows["standin-overlap"]["diff"] == 1.0 and rows["standin-overlap"]["ci95"][0] > 0
    assert rows["standin-length"]["diff"] <= 0.5
