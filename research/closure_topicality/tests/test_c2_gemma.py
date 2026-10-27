"""The gemma control2 arm replays sol's pairs; an undecided arm makes it incomplete. No network."""
import c2_gemma


class Silent:
    model_id = "fake"

    def ask(self, prompt):
        return {"states": [], "partially": []}


class Broken:
    model_id = "fake"

    def ask(self, prompt):
        return {}


def test_same_pairs_as_sol_and_an_open_judge_reads_direction_zero():
    res = c2_gemma.run(Silent())
    assert res["complete"] and res["direction"] == "0"
    assert res["summary"]["total"]["n_discriminable"] == 44


def test_undecided_arms_make_the_run_incomplete():
    res = c2_gemma.run(Broken())
    assert not res["complete"] and res["direction"] == "incomplete"
