"""D1b novelty judging (plan §3.5-3.6): lock, canary check, reveal. No model, no network."""
import json
import re
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
    assert "blinding" not in res


def test_reveal_reports_the_blinding_check_from_the_owners_guesses(tmp_path):
    key, pub = tmp_path / "seal.key", tmp_path / "seal.pub"
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", str(key)], check=True, capture_output=True)
    subprocess.run(["openssl", "pkey", "-in", str(key), "-pubout", "-out", str(pub)], check=True, capture_output=True)
    items = [{"q": i, "arm": "gap" if i <= 10 else "covered"} for i in range(1, 21)]
    (tmp_path / "secret").mkdir()
    (tmp_path / "secret" / "key.json").write_text(json.dumps({"items": items}))
    bs.seal(tmp_path / "secret", pub, tmp_path / "sealed")
    judged = [{"q": i, "answer": "x", "judge_a": {"label": "new"}, "judge_b": {"label": "new"}} for i in range(1, 21)]
    guesses = {it["q"]: it["arm"] for it in items}
    res = novelty.reveal(judged, tmp_path / "sealed", key, tmp_path / "opened", guesses=guesses)
    assert res["blinding"]["accuracy"] == 1.0 and res["blinding"]["unblinded"] is True


def _mixed(tmp_path):
    canary_rows = [{"id": "c-copied", "question": "Q?", "answer": "copied passage"},
                   {"id": "c-new", "question": "Q?", "answer": "planted fact"}]
    expected = {"c-copied": "already written", "c-new": "new"}
    r = novelty.Retriever([("d", "copied passage about bands"), ("d", "another passage on windows")])
    return novelty.build_cases({1: "A?", 2: "B?"}, {1: "answer one", 2: "answer two"}, canary_rows, expected, r)


def test_canaries_and_cases_share_one_file_under_opaque_ids(tmp_path):
    cases, case_map = _mixed(tmp_path)
    assert len(cases) == 4 and set(case_map) == {c["id"] for c in cases}
    assert all(re.fullmatch(r"[0-9a-f]{8}", c["id"]) for c in cases)
    assert sorted(v.get("canary", "") for v in case_map.values()) == ["", "", "c-copied", "c-new"]
    assert all("expected" not in c and "kind" not in c for c in cases)


def test_judgements_map_back_to_canaries_and_questions(tmp_path):
    cases, case_map = _mixed(tmp_path)
    ids = {(v.get("canary") or f"q{v['q']}"): k for k, v in case_map.items()}
    a = {ids["c-copied"]: {"label": "already written"}, ids["c-new"]: {"label": "new"},
         ids["q1"]: {"label": "new"}, ids["q2"]: {"label": "partly"}}
    b = {**a, ids["c-new"]: {"label": "partly"}}
    failures, judged = novelty.split_judgements(case_map, a, b, {1: "answer one", 2: "answer two"})
    assert failures == ["judge_b:c-new"]
    assert [(r["q"], r["judge_a"]["label"], r["answer"]) for r in judged] == [(1, "new", "answer one"),
                                                                             (2, "partly", "answer two")]


def test_each_judge_gets_one_pass(tmp_path):
    cases, case_map = _mixed(tmp_path)
    (tmp_path / "case_map.json").write_text(json.dumps(case_map))
    (tmp_path / "answers.md").write_text(_answers(2))
    labels = {k: {"label": v.get("expected", "new")} for k, v in case_map.items()}
    assert novelty.ingest(tmp_path, labels, labels)["canary_failures"] == []
    with pytest.raises(SystemExit, match="one pass"):
        novelty.ingest(tmp_path, labels, labels)


def test_spare_questions_are_pool_topics_not_on_the_sheet(tmp_path):
    pool = {"topics": [{"topic_id": f"T{i}", "question_text": f"Question {i}?"} for i in range(6)]}
    (tmp_path / "pool.json").write_text(json.dumps(pool))
    (tmp_path / "questions.md").write_text("# q\n\n## Q1\n\nQuestion 0?\n\n## Q2\n\nQuestion 3?\n")
    spare = novelty.spare_questions(tmp_path / "pool.json", tmp_path / "questions.md", seed=1, k=3)
    assert len(spare) == 3 and not {"Question 0?", "Question 3?"} & set(spare)
    assert spare == novelty.spare_questions(tmp_path / "pool.json", tmp_path / "questions.md", seed=1, k=3)


def test_ingest_records_the_hash_of_each_judges_raw_output(tmp_path):
    cases, case_map = _mixed(tmp_path)
    (tmp_path / "case_map.json").write_text(json.dumps(case_map))
    (tmp_path / "answers.md").write_text(_answers(2))
    labels = {k: {"label": v.get("expected", "new")} for k, v in case_map.items()}
    (tmp_path / "a.json").write_text(json.dumps(labels))
    (tmp_path / "b.json").write_text(json.dumps(labels))
    doc = novelty.ingest(tmp_path, labels, labels, raw={"judge_a": tmp_path / "a.json", "judge_b": tmp_path / "b.json"})
    assert doc["raw_sha256"]["judge_a"] == novelty._sha(tmp_path / "a.json")


def test_a_canary_failure_voids_the_reading(tmp_path):
    key, pub = tmp_path / "seal.key", tmp_path / "seal.pub"
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", str(key)], check=True, capture_output=True)
    subprocess.run(["openssl", "pkey", "-in", str(key), "-pubout", "-out", str(pub)], check=True, capture_output=True)
    items = [{"q": i, "arm": "gap" if i <= 10 else "covered"} for i in range(1, 21)]
    (tmp_path / "secret").mkdir()
    (tmp_path / "secret" / "key.json").write_text(json.dumps({"items": items}))
    bs.seal(tmp_path / "secret", pub, tmp_path / "sealed")
    judged = [{"q": i, "answer": "x", "judge_a": {"label": "new" if i <= 10 else "already written"},
               "judge_b": {"label": "new" if i <= 10 else "already written"}} for i in range(1, 21)]
    res = novelty.reveal(judged, tmp_path / "sealed", key, tmp_path / "opened", canary_failures=["judge_b:c-new"])
    assert res["decision"] == "No reading" and res["void"] == ["judge_b:c-new"]
    assert res["agreed"]["meets"] is True


def test_guesses_are_read_only_while_the_locked_answers_are_unchanged(tmp_path):
    (tmp_path / "questions.md").write_text("# q\n\n## Q1\n\nA?\n")
    (tmp_path / "answers.md").write_text(_answers(1))
    novelty.lock(tmp_path)
    assert novelty.load_guesses(tmp_path) is None
    (tmp_path / "guesses.json").write_text(json.dumps({"1": "gap"}))
    assert novelty.load_guesses(tmp_path) == {1: "gap"}
    (tmp_path / "answers.md").write_text(_answers(1, "Edited."))
    with pytest.raises(SystemExit, match="changed"):
        novelty.load_guesses(tmp_path)
