"""Trivial stand-in judges (L7.3): each answers a closure prompt from a surface statistic, so a check
that one of them passes is shown not to need a reader of the element."""
import pytest

from gapmap import semantic, standins


def _prompt(sentences, seed="Use surrogates to set the significance band.", question="Why do this?"):
    retrieval = semantic.build_retrieval([("c1", i, s) for i, s in enumerate(sentences)], [])
    return semantic.build_prompt(seed, question, retrieval), retrieval, seed, question


def _state(judge, sentences, **kw):
    _p, retrieval, seed, question = _prompt(sentences, **kw)
    return semantic.judge_retrieval(judge, retrieval, seed, question).state


def test_parse_recovers_seed_question_and_numbered_sentences():
    prompt, *_ = _prompt(["First sentence.", "Second one."])
    parsed = standins.parse(prompt)
    assert parsed.seed == "Use surrogates to set the significance band."
    assert parsed.question == "Why do this?"
    assert [s for _i, s in parsed.sentences] == ["First sentence.", "Second one."]


def test_a_score_judge_closes_at_or_above_its_cut_and_cites_an_offered_sentence():
    judge = standins.ScoreJudge("length", standins.length, cut=30)
    assert _state(judge, ["A sentence long enough to pass the cut."]) == "closed"
    assert _state(judge, ["Too short."]) == "open"


def test_calibrate_sets_the_cut_at_the_median_score_of_the_prompts():
    prompts = [_prompt([s])[0] for s in ("aa.", "aaaa.", "aaaaaa.")]
    judge = standins.calibrate("length", standins.length, prompts)
    assert judge.cut == standins.length(standins.parse(prompts[1]))


def test_overlap_scores_topical_words_shared_with_the_seed_and_question():
    on = standins.overlap(standins.parse(_prompt(["Surrogates set the significance band here."])[0]))
    off = standins.overlap(standins.parse(_prompt(["The weather in Warsaw was cold."])[0]))
    assert on > off == 0


def test_specificity_counts_digits_conditionals_and_code_like_settings():
    plain = standins.specificity(standins.parse(_prompt(["It is a useful step."])[0]))
    concrete = standins.specificity(standins.parse(_prompt(["If n_surrogates is 99, use alpha 0.05."])[0]))
    assert concrete > plain == 0


def test_the_lexicon_judge_closes_on_a_closing_marker_alone():
    judge = standins.LexiconJudge()
    assert _state(judge, ["We do it because the band needs it."]) == "closed"
    assert _state(judge, ["The band is drawn in grey."]) == "open"


def test_the_source_count_judge_reads_sources_through_a_supplied_map():
    sources = {"One.": "s1", "Two.": "s2", "Three.": "s2"}
    judge = standins.ScoreJudge("sources", standins.source_count(sources), cut=2)
    assert _state(judge, ["One.", "Two."]) == "closed"
    assert _state(judge, ["Two.", "Three."]) == "open"


def test_the_coin_flip_is_deterministic_and_near_half():
    judge = standins.CoinFlipJudge()
    prompts = [_prompt([f"Sentence number {i}."])[0] for i in range(200)]
    closed = [bool(judge.ask(p)["states"]) for p in prompts]
    assert closed == [bool(judge.ask(p)["states"]) for p in prompts]
    assert 70 < sum(closed) < 130


def test_the_recording_judge_keeps_every_prompt_and_answers_open():
    judge = standins.RecordingJudge()
    assert _state(judge, ["Anything at all."]) == "open"
    assert len(judge.prompts) == 1


@pytest.mark.parametrize("judge", [standins.ScoreJudge("length", standins.length, cut=0),
                                   standins.LexiconJudge(), standins.CoinFlipJudge(),
                                   standins.RecordingJudge()])
def test_every_stand_in_has_a_model_id_outside_any_vendor_family(judge):
    from gapmap import judge as judge_mod
    assert judge_mod.family(judge.model_id) == "other"
