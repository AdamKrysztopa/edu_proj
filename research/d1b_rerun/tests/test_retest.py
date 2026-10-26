"""R4 retest helpers: reply state, seeded sample, agreement. No network."""
import retest


def test_reply_state_reads_states_then_partially():
    assert retest.state({"states": [1], "partially": []}) == "closed"
    assert retest.state({"states": [], "partially": [2]}) == "partial"
    assert retest.state({"states": [], "partially": []}) == "open"
    assert retest.state(None) == "undecided" and retest.state({"reason": "x"}) == "undecided"


def test_the_sample_is_a_seeded_fifth_of_the_unique_prompts():
    prompts = [f"p{i}" for i in range(50)] * 2
    s = retest.sample(prompts)
    assert len(s) == 10 and len(set(s)) == 10 and s == retest.sample(list(reversed(prompts)))


def test_agreement_counts_matching_states():
    a = [{"states": [1]}, {"states": []}, None]
    b = [{"states": [2]}, {"partially": [1], "states": []}, None]
    assert retest.agreement(a, b) == {"n": 3, "agree": 2, "rate": 2 / 3}
