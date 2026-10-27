"""Per-codebase canaries (D1c plan §5.3), tested on dependence-forecastability's committed corpus:
the source passage is picked by seeded code, the paraphrase and the planted answer are written by
a separate author and then checked in code before the owner confirms them. No model, no network."""
import json
import re
from pathlib import Path

import pytest

import canaries
import codebase
import novelty

HERE = Path(__file__).resolve().parents[1]
D1B_SPEC = json.loads((HERE / "fixtures" / "canaries.json").read_text())
D1B_NOVEL_TERMS = ["499", "300 points", "imputed", "weekly peak"]
OFF_TOPIC = ("We bake the sourdough at 245 degrees for 38 minutes, and we refuse to slice any loaf before it "
             "has rested for two hours, because the crumb collapses when it is cut warm.")


@pytest.fixture(scope="module")
def corpus():
    cb = codebase.d1b()
    passages = canaries.source_passages(cb)
    return cb, passages, novelty.Retriever([(p["title"], p["text"]) for p in passages])


def _lle_source(passages):
    (src,) = [p for p in passages if p["text"].startswith("> [!WARNING] > **Experimental feature.** Largest Lyapunov")]
    return src


def test_eligible_sources_are_owner_prose_of_bounded_length(corpus):
    _, passages, _ = corpus
    elig = canaries.eligible(passages)
    assert len(elig) >= 20
    assert all(p["owner"] and p["tag"] == "p" for p in elig)
    assert all(canaries.MIN_WORDS <= len(p["text"].split()) <= canaries.MAX_WORDS for p in elig)
    assert not any(p["owner"] is False for p in elig)


def test_the_pick_is_seeded_and_reproducible(corpus):
    _, passages, _ = corpus
    picks = {canaries.pick(passages, seed)["id"] for seed in range(5)}
    assert canaries.pick(passages, 3) == canaries.pick(list(reversed(passages)), 3)
    assert len(picks) > 1


def test_d1b_handwritten_paraphrase_passes_against_its_source(corpus):
    _, passages, retriever = corpus
    src = _lle_source(passages)
    assert canaries.paraphrase_problems(src["text"], D1B_SPEC["paraphrase_question"], D1B_SPEC["paraphrase"],
                                        retriever) == []


def test_a_verbatim_copy_is_not_a_paraphrase(corpus):
    _, passages, retriever = corpus
    src = _lle_source(passages)
    problems = canaries.paraphrase_problems(src["text"], D1B_SPEC["paraphrase_question"], src["text"], retriever)
    assert any("copy" in p for p in problems)


def test_a_paraphrase_the_judges_would_not_see_beside_its_source_is_refused(corpus):
    _, passages, retriever = corpus
    src = _lle_source(passages)
    problems = canaries.paraphrase_problems(src["text"], "How do I install the toolkit?", OFF_TOPIC, retriever)
    assert any("not among" in p for p in problems)


def test_d1b_planted_answer_passes_with_its_novel_terms(corpus):
    _, passages, retriever = corpus
    assert canaries.planted_problems(D1B_SPEC["paraphrase_question"], D1B_SPEC["planted_new"], D1B_NOVEL_TERMS,
                                     passages, retriever) == []


def test_a_planted_term_the_corpus_already_states_is_refused(corpus):
    _, passages, retriever = corpus
    problems = canaries.planted_problems(D1B_SPEC["paraphrase_question"], D1B_SPEC["planted_new"],
                                         D1B_NOVEL_TERMS + ["surrogate"], passages, retriever)
    assert problems == ["planted term in the corpus: 'surrogate'"]


def test_a_planted_term_missing_from_the_answer_or_no_terms_at_all_is_refused(corpus):
    _, passages, retriever = corpus
    q = D1B_SPEC["paraphrase_question"]
    assert canaries.planted_problems(q, D1B_SPEC["planted_new"], ["7331 lags"], passages, retriever) == [
        "planted term not in the answer: '7331 lags'"]
    assert "no planted terms" in canaries.planted_problems(q, D1B_SPEC["planted_new"], [], passages, retriever)[0]


def test_an_off_topic_planted_answer_is_refused(corpus):
    _, passages, retriever = corpus
    problems = canaries.planted_problems(D1B_SPEC["paraphrase_question"], OFF_TOPIC, ["245 degrees"],
                                         passages, retriever)
    assert any("off-topic" in p for p in problems)


def test_the_copied_canary_is_an_eligible_passage(corpus):
    _, passages, retriever = corpus
    text_ = canaries.copied("When should the largest Lyapunov exponent be used?", passages, retriever)
    assert text_ in {p["text"] for p in canaries.eligible(passages)}


def _spec(src, **kw):
    return {"source_id": src["id"], "paraphrase_question": D1B_SPEC["paraphrase_question"],
            "paraphrase": _length_matched(PLANTED_RICH), "planted_question": D1B_SPEC["paraphrase_question"],
            "planted_new": PLANTED_RICH, "planted_terms": D1B_NOVEL_TERMS,
            "owner_confirmed": True, **kw}


def test_ready_needs_the_seeded_source_passing_checks_and_the_owners_confirmation(corpus):
    cb, passages, _ = corpus
    src = _lle_source(passages)
    canaries.ready(_spec(src), cb, source_id=src["id"])
    with pytest.raises(canaries.NotReady, match="owner"):
        canaries.ready(_spec(src, owner_confirmed=False), cb, source_id=src["id"])
    with pytest.raises(canaries.NotReady, match="seeded"):
        canaries.ready(_spec(src), cb, source_id="0" * 12)
    with pytest.raises(canaries.NotReady, match="copy"):
        canaries.ready(_spec(src, paraphrase=src["text"]), cb, source_id=src["id"])


PLANTED_RICH = (D1B_SPEC["planted_new"] + " None of this touches the experimental Lyapunov exponent, which stays "
                "excluded from automated triage.")


def _length_matched(planted: str = D1B_SPEC["planted_new"]):
    words = len(planted.split())
    return " ".join((D1B_SPEC["paraphrase"] + " " + D1B_SPEC["paraphrase"]).split()[:words])


def test_trivial_stand_in_labellers_must_each_get_a_canary_wrong():
    words = len(D1B_SPEC["planted_new"].split())
    assert canaries.standin_problems(_length_matched(), D1B_SPEC["planted_new"]) == []
    problems = canaries.standin_problems(D1B_SPEC["paraphrase"], D1B_SPEC["planted_new"])
    assert len(problems) == 1 and "longer" in problems[0]
    no_digits = " ".join(["fragile"] * words)
    problems = canaries.standin_problems(no_digits, D1B_SPEC["planted_new"])
    assert len(problems) == 1 and "digit" in problems[0]


def test_a_lower_overlap_is_new_labeller_must_also_fail(corpus):
    _, passages, retriever = corpus
    spec = {"paraphrase_question": D1B_SPEC["paraphrase_question"], "paraphrase": _length_matched(),
            "planted_question": D1B_SPEC["paraphrase_question"], "planted_new": D1B_SPEC["planted_new"]}
    problems = canaries.overlap_problems(spec, retriever)
    assert len(problems) == 1 and "overlap" in problems[0]
    spec["planted_new"] = spec["paraphrase"]
    assert canaries.overlap_problems(spec, retriever) == []


DRYRUN = HERE.parent / "d1c" / "dryrun-dependence-forecastability"


def test_the_dry_run_canaries_by_a_separate_author_pass_every_code_check():
    cb = codebase.load(DRYRUN / "codebase.json")
    spec = json.loads(cb.canaries.read_text())
    assert spec["source_id"] == canaries.pick(canaries.source_passages(cb), cb.seed)["id"]
    assert canaries.check(spec, cb) == []
    assert spec["owner_confirmed"] is False


def test_novelty_uses_generated_canaries_only_once_the_owner_confirms(tmp_path):
    cb = codebase.load(DRYRUN / "codebase.json")
    spec = json.loads(cb.canaries.read_text())
    question = "When should the largest Lyapunov exponent be used?"
    retriever = novelty.Retriever(novelty.passages(cb.corpus))
    with pytest.raises(canaries.NotReady, match="owner"):
        novelty._canaries(question, retriever, cb)
    (tmp_path / "canaries.json").write_text(json.dumps({**spec, "owner_confirmed": True}))
    spare = ["One source writes: \"a\". Why?", "One source writes: \"b\". Why?", "One source writes: \"c\". Why?"]
    rows, expected = novelty._canaries(question, retriever, codebase.replace(cb, canaries=tmp_path / "canaries.json"),
                                       spare_questions=spare)
    by_id = {r["id"]: r for r in rows}
    assert by_id["c-new"]["question"] == spec["planted_question"]
    assert [by_id[c]["question"] for c in ("c-filler-40", "c-filler-90", "c-copied")] == spare
    assert question not in {r["question"] for r in rows}
    assert by_id["c-copied"]["answer"] in {p["text"] for p in canaries.eligible(canaries.source_passages(cb))}
    assert expected["c-paraphrase"] == "already written" and expected["c-new"] == "new"


def test_d1b_fixed_canaries_are_built_as_before():
    cb = codebase.d1b()
    retriever = novelty.Retriever(novelty.passages(cb.corpus))
    question = "When should the largest Lyapunov exponent be used?"
    assert novelty._canaries(question, retriever, cb) == novelty._canaries(question, retriever)


def test_the_brief_carries_the_source_and_the_rules_but_no_arm(corpus):
    _, passages, _ = corpus
    src = canaries.pick(passages, 1)
    b = canaries.brief(src)
    assert src["text"] in b and "planted_terms" in b
    assert not re.search(r"\b(gap|covered|arm)\b", b.lower())
