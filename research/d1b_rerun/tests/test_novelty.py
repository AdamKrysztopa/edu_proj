"""D1b novelty judging (plan §3.5-3.6): lock, canary check, reveal. No model, no network."""
import json
import subprocess

import pytest

import build_sheet as bs
import novelty


def _answers(n, text="An answer."):
    return "# D1b answers\n\n" + "".join(f"## Q{i}\n\n{text} {i}\n\n" for i in range(1, n + 1))


def test_parse_answers_reads_every_heading():
    assert novelty.parse_answers(_answers(3)) == {1: "An answer. 1", 2: "An answer. 2", 3: "An answer. 3"}


def test_lock_refuses_a_missing_answer(tmp_path):
    (tmp_path / "questions.md").write_text("# q\n\n## Q1\n\nA?\n\n## Q2\n\nB?\n")
    (tmp_path / "answers.md").write_text(_answers(1))
    with pytest.raises(SystemExit, match="Q\\[2\\]"):
        novelty.lock(tmp_path)


def test_the_retriever_similarity_is_higher_for_an_on_corpus_question():
    r = novelty.Retriever([("d", "surrogate bands set the significance floor of mutual information"),
                           ("d", "the training window holds every diagnostic computation")])
    assert r.similarity("how many surrogates set the significance floor") > r.similarity("what is the weather")


def _judged(label_a, label_b):
    return {"label": label_a}, {"label": label_b}


def test_canaries_must_get_their_expected_label_from_both_judges():
    expected = {"c-filler-40": "no content", "c-copied": "already written", "c-new": "new"}
    good = {k: {"label": v} for k, v in expected.items()}
    assert novelty.canary_failures(expected, good, good) == []
    bad_b = {**good, "c-copied": {"label": "new"}}
    assert novelty.canary_failures(expected, good, bad_b) == ["judge_b:c-copied"]


def test_the_length_only_labeller_marks_answers_at_or_above_the_median_new():
    rows = [{"q": 1, "answer": "a b c"}, {"q": 2, "answer": "a"}, {"q": 3, "answer": "a b"}]
    assert novelty.length_labels(rows) == {1: "new", 2: "already written", 3: "new"}


def test_arm_guess_accuracy_and_its_binomial_p():
    res = novelty.guess_accuracy({1: "gap", 2: "covered", 3: "gap", 4: "gap"},
                                 {1: "gap", 2: "covered", 3: "gap", 4: "covered"})
    assert res["accuracy"] == 0.75 and res["unblinded"] is False
    assert res["p"] == pytest.approx(5 / 16)


def test_reveal_decides_from_the_sealed_key_and_both_judges(tmp_path):
    key, pub = tmp_path / "seal.key", tmp_path / "seal.pub"
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", str(key)], check=True, capture_output=True)
    subprocess.run(["openssl", "pkey", "-in", str(key), "-pubout", "-out", str(pub)], check=True, capture_output=True)
    n = 10
    items = [{"q": i, "arm": "gap" if i <= n else "covered"} for i in range(1, 2 * n + 1)]
    (tmp_path / "secret").mkdir()
    (tmp_path / "secret" / "key.json").write_text(json.dumps({"items": items}))
    bs.seal(tmp_path / "secret", pub, tmp_path / "sealed")
    labels = {i: ("new" if i <= n else "already written") for i in range(1, 2 * n + 1)}
    judged = [{"q": i, "answer": "x" * i, "judge_a": {"label": labels[i]}, "judge_b": {"label": labels[i]}}
              for i in labels]
    res = novelty.reveal(judged, tmp_path / "sealed", key, tmp_path / "opened")
    assert res["decision"] == "Continue"
    assert res["rows"][0]["arm"] == "gap"
