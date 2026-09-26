from probe_app.human import turns_from_markers
from probe_app.transcribe import RawSegment


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
