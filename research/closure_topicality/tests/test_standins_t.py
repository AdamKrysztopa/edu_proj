"""Per-sentence and probe stand-ins (plan §1.6). No network."""
from gapmap import semantic, standins

import standins_t as st

Q_WHY = "Does any sentence state why this is done (the reason or the failure it prevents)?"
Q_DISC = ("Does any sentence state how to tell whether something counts as 'vulnerable data': a threshold, "
          "a defining feature, or a contrast between a case that is and one that is not?")


def _prompt(seed, question, sents):
    rows = [("c", n, s) for n, s in enumerate(sents)]
    return semantic.build_prompt(seed, question, semantic.build_retrieval(rows))


def test_probe_words_use_the_quoted_anchor_for_disc_and_the_seed_otherwise():
    p = standins.parse(_prompt("Controllers must screen processing.", Q_DISC, ["x"]))
    assert st.probe_words(p) == frozenset({"vulnerable", "data"})
    p = standins.parse(_prompt("Controllers must screen processing.", Q_WHY, ["x"]))
    assert st.probe_words(p) == frozenset({"controller", "screen", "process"})


def test_novel_func_does_not_count_random_letters():
    p = standins.parse(_prompt("Screen processing.", Q_WHY, ["x"]))
    assert st.STATS["novel_func"](p, "qwz plk mrv tsy") == -1
    assert st.STATS["novel_func"](p, "the auditor reviews logs") == 3


def test_question_lexicon_reads_the_lexicons_the_question_itself_matches():
    p = standins.parse(_prompt("Screen processing.", Q_DISC, ["x"]))
    assert st.STATS["question_lexicon"](p, "You can tell them apart by size.") == 1
    assert st.STATS["question_lexicon"](p, "The register is kept on paper.") == 0


def test_cite_judge_modes():
    prompt = _prompt("Screen the processing of data.", Q_WHY,
                     ["Screen processing data.", "Unrelated words here.", "Screen data."])
    j = st.CiteJudge("overlap", st.STATS["overlap"], "ge", cut=2)
    assert j.ask(prompt)["states"] == [1, 3]
    assert st.CiteJudge("overlap", st.STATS["overlap"], "le", cut=0).ask(prompt)["states"] == [2]
    assert st.CiteJudge("overlap", st.STATS["overlap"], "argmax", cut=0).ask(prompt)["states"] == [1]
    assert st.CiteJudge("overlap", st.STATS["overlap"], "argmin", cut=0).ask(prompt)["states"] == [2]


def test_cite_judge_reply_parses_as_closed_citing_those_sentences():
    prompt = _prompt("Screen the processing of data.", Q_WHY, ["Screen processing data.", "Nothing."])
    reply = st.CiteJudge("overlap", st.STATS["overlap"], "ge", cut=1).ask(prompt)
    rows = [("a", 0, "Screen processing data."), ("b", 0, "Nothing.")]
    out = semantic.judge_retrieval(type("J", (), {"model_id": "x", "ask": lambda self, q: reply})(),
                                   semantic.build_retrieval(rows), "Screen the processing of data.", Q_WHY)
    assert out.state == "closed" and out.a_hits == ("a",)


def test_calibrated_cut_is_the_median_over_every_offered_sentence():
    prompts = [_prompt("Screen data.", Q_WHY, ["a" * 10, "a" * 20]), _prompt("Screen data.", Q_WHY, ["a" * 30])]
    assert st.calibrate("length", st.STATS["length"], "ge", prompts).cut == 20


def test_sweep_cuts_are_every_distinct_value():
    prompts = [_prompt("Screen data.", Q_WHY, ["a" * 10, "a" * 20]), _prompt("Screen data.", Q_WHY, ["a" * 10])]
    assert st.sweep_cuts(st.STATS["length"], prompts) == [10, 20]


def test_idf_overlap_weights_rare_context_words_higher():
    prompts = [_prompt("Screen rare data.", Q_WHY, ["data data", "data rare", "data"])]
    idf = st.idf_stat(prompts)
    p = standins.parse(prompts[0])
    assert idf(p, "rare") > idf(p, "data") > 0


def test_coin_is_deterministic_per_sentence():
    prompt = _prompt("Screen data.", Q_WHY, ["one", "two", "three", "four"])
    assert st.CoinCiteJudge(1).ask(prompt) == st.CoinCiteJudge(1).ask(prompt)


def test_arm_level_judges_cover_the_new_statistics():
    prompts = [_prompt("Screen data.", Q_WHY, ["Screen data now.", "x"])]
    names = {j.model_id for j in st.arm_level(prompts)}
    assert {"standin-probe", "standin-novel_func", "standin-overlap", "standin-length"} <= names
