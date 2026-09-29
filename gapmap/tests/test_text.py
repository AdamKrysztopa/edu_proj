from conftest import a_claim, u_claim

from gapmap import text


def test_tokens_drops_short_and_stop_words():
    assert text.tokens("The PLC is a valid device") == ["plc", "valid", "device"]


def test_stem_suffix_order_and_min_length():
    assert text.stem("policies") == "policy"
    assert text.stem("checking") == "check"
    assert text.stem("checked") == "check"
    assert text.stem("faults") == "fault"
    assert text.stem("is") == "is"  # too short to strip anything down to >= 4 chars


def test_stem_never_strips_from_a_word_ending_in_ss():
    assert text.stem("process") == "process"
    assert text.stem("processes") == "process"


def test_stem_folds_failure_to_fail():
    # S3 defect 4: "failure" and "fail" must share a stem for closure overlap to see both forms.
    assert text.stem("failure") == "fail"
    assert text.stem("failures") == "fail"
    assert text.stem("fail") == "fail"


def test_domain_strips_www_and_is_empty_for_a_non_url_identifier():
    assert text.domain("https://www.plclogs.com/") == "plclogs.com"
    assert text.domain("https://capafy.ai/nl/agent/x") == "capafy.ai"
    assert text.domain("doi:10.0/test-1") == ""


def test_cw_is_the_stem_set():
    s = "Loose terminals and oxidized connections"
    assert text.cw(s) == frozenset(text.stem(t) for t in text.tokens(s))


def test_sentences_split_on_period_or_semicolon_then_space():
    out = text.sentences("First part. Second part; third part.")
    assert out == ["First part.", "Second part;", "third part."]


def test_T_is_assertion_plus_verbatim_spans():
    c = a_claim("Diagnostic tests should be selected based on likelihood.",
                exact="the field device and wiring are far more likely to fail than the card")
    assert text.T(c) == ("Diagnostic tests should be selected based on likelihood. "
                          "the field device and wiring are far more likely to fail than the card")


def test_T_with_no_evidence_is_just_the_assertion():
    c = u_claim("What signals that a device has failed?")
    assert text.T(c) == "What signals that a device has failed?"


def test_trim_leaves_short_text_untouched():
    assert text.trim("Loose terminals cause faults.") == "Loose terminals cause faults."


def test_trim_cuts_at_a_word_boundary_under_the_limit():
    s = "the field device and wiring are far more likely to fail than the card in most installations"
    out = text.trim(s, limit=40)
    assert len(out) <= 40
    assert not out.endswith(" ")
    assert s.startswith(out)


def test_trim_never_splits_a_word():
    s = "supercalifragilisticexpialidocioussupercalifragilisticexpialidocious"
    out = text.trim(s, limit=10)
    assert out == s[:10]  # no space to cut at: falls back to a hard cut


def test_sentence_containing_picks_the_sentence_spanning_the_marker_position():
    s = "First part. Second part has a marker; third part."
    pos = s.index("marker")
    assert text.sentence_containing(s, pos) == "Second part has a marker;"


def test_sentence_containing_the_first_sentence_when_pos_is_near_the_start():
    s = "First part has the marker. Second part."
    pos = s.index("marker")
    assert text.sentence_containing(s, pos) == "First part has the marker."


def test_sentence_containing_falls_back_to_the_last_sentence_past_the_end():
    s = "Only one sentence here."
    assert text.sentence_containing(s, len(s) + 5) == "Only one sentence here."

