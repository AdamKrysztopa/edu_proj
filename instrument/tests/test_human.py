from probe_app.human import turns_from_markers, unmarked_warning
from probe_app.transcribe import RawSegment
from test_session import new_session, seg, through_think_aloud


def test_turns_split_by_markers_and_ticks_attach():
    raw = [RawSegment(start=0.5, end=2, text="Tell me about the collision."),
           RawSegment(start=3, end=5, text="Well, they stick."),
           RawSegment(start=5, end=6, text="So momentum."),
           RawSegment(start=7, end=8, text="How did you check it?")]
    markers = [{"speaker": "interviewer", "t": 0.0}, {"speaker": "expert", "t": 2.5},
               {"speaker": "interviewer", "t": 6.5}]
    ticks = [{"problem_id": "A1", "stem_id": "cues", "t": 1.0}, {"problem_id": "A1", "stem_id": "checks", "t": 7.5}]
    turns = turns_from_markers(raw, markers, ticks)
    assert [(x.speaker, x.text) for x in turns] == [
        ("interviewer", "Tell me about the collision."),
        ("expert", "Well, they stick. So momentum."),
        ("interviewer", "How did you check it?")]
    assert (turns[0].stem_id, turns[2].stem_id) == ("cues", "checks")
    assert turns[0].source == "human" and turns[1].source == "transcribed"


def test_tick_before_speech_attaches_to_that_interviewer_turn():
    raw = [RawSegment(start=0.4, end=1, text="What did you see?"), RawSegment(start=2, end=3, text="The stick."),
           RawSegment(start=5, end=6, text="And then?")]
    markers = [{"speaker": "interviewer", "t": 0.0}, {"speaker": "expert", "t": 1.5},
               {"speaker": "interviewer", "t": 4.0}]
    ticks = [{"problem_id": "A1", "stem_id": "cues", "t": 0.1}, {"problem_id": "A1", "stem_id": "checks", "t": 4.2}]
    turns = turns_from_markers(raw, markers, ticks)
    assert [(x.speaker, x.stem_id) for x in turns] == [("interviewer", "cues"), ("expert", None),
                                                       ("interviewer", "checks")]


def test_speaker_is_decided_by_segment_midpoint_not_start():
    raw = [RawSegment(start=99.7, end=102.0, text="Why did you split it there?")]
    markers = [{"speaker": "expert", "t": 50.0}, {"speaker": "interviewer", "t": 100.0}]
    assert turns_from_markers(raw, markers, [])[0].speaker == "interviewer"


def test_speech_before_the_first_marker_is_unmarked_and_takes_no_tick():
    raw = [RawSegment(start=0.2, end=1, text="Okay, so"), RawSegment(start=1.2, end=2, text="where were we."),
           RawSegment(start=3, end=4, text="What did you notice?")]
    markers = [{"speaker": "interviewer", "t": 2.5}]
    ticks = [{"problem_id": "A1", "stem_id": "cues", "t": 0.5}]
    turns = turns_from_markers(raw, markers, ticks)
    assert [(x.speaker, x.text, x.stem_id) for x in turns] == [
        ("unmarked", "Okay, so where were we.", None), ("interviewer", "What did you notice?", "cues")]
    assert turns[0].source == "transcribed"


def test_unmarked_warning_names_lost_words_and_a_set_without_expert_speech():
    marked = turns_from_markers([RawSegment(start=1, end=2, text="Why?"), RawSegment(start=3, end=4, text="Because.")],
                                [{"speaker": "interviewer", "t": 0}, {"speaker": "expert", "t": 2.5}], [])
    assert unmarked_warning(marked) is None
    late = turns_from_markers([RawSegment(start=0, end=1, text="Why that?"), RawSegment(start=3, end=4, text="Eh.")],
                              [{"speaker": "expert", "t": 2.5}], [])
    assert "2 words before the first I/E marker" in unmarked_warning(late)
    never = turns_from_markers([RawSegment(start=0, end=1, text="Why that?")], [], [])
    assert "no speech is marked as the expert's" in unmarked_warning(never)


def test_human_probe_without_markers_sets_error_and_logs(tmp_path):
    s = new_session(tmp_path, arms={"A": "human", "B": "ai"},
                    transcripts=[seg("A1"), seg("A2"), seg("B1"), seg("B2"), seg("What did you see? The stick.")])
    through_think_aloud(s)
    s.start_probe()
    s.end_probe()
    s.finalize_human_probe(b"audio")
    assert "set A" in s.state.error and "no speech is marked as the expert's" in s.state.error
    assert [e["words"] for e in s.store.events() if e["type"] == "unmarked_speech"] == [6]


def test_without_markers_all_speech_is_unmarked():
    raw = [RawSegment(start=0, end=1, text="Hello."), RawSegment(start=2, end=3, text="Hi.")]
    assert [(x.speaker, x.text) for x in turns_from_markers(raw, [], [])] == [("unmarked", "Hello. Hi.")]
