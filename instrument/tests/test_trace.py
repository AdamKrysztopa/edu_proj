from types import SimpleNamespace

import pytest

from fakes import FakeTranscriber
from probe_app.trace import build_segments, correct_segment, render_transcript
from probe_app.transcribe import (RawSegment, ScribeTranscriber, TranscriptionFailed, make_transcriber,
                                  transcribe_with_retry, words_to_segments)

RAW = [RawSegment(start=0.0, end=2.0, text="Energy first."), RawSegment(start=2.0, end=5.5, text="Then momentum.")]


def test_build_segments_offsets_and_ids():
    segs = build_segments("A1", 10.0, RAW)
    assert [s.id for s in segs] == ["A1-s001", "A1-s002"]
    assert (segs[1].start, segs[1].end) == (12.0, 15.5)
    assert segs[0].problem_id == "A1"


def test_correct_segment_returns_diff():
    segs = build_segments("A1", 0.0, RAW)
    new, diff = correct_segment(segs, "A1-s002", "Then momentum conservation.")
    assert new[1].text == "Then momentum conservation."
    assert diff == {"segment_id": "A1-s002", "old": "Then momentum.", "new": "Then momentum conservation."}
    assert segs[1].text == "Then momentum."


def test_correct_unknown_segment_raises():
    with pytest.raises(KeyError):
        correct_segment(build_segments("A1", 0.0, RAW), "A1-s999", "x")


def test_render_transcript():
    assert render_transcript(build_segments("A1", 0.0, RAW)).splitlines()[0] == "[A1-s001 0.0-2.0s] Energy first."


def test_retry_succeeds_on_third_attempt(tmp_path):
    t = FakeTranscriber([RuntimeError("a"), RuntimeError("b"), RAW])
    assert transcribe_with_retry(t, tmp_path / "x.webm") == RAW
    assert len(t.calls) == 3


def test_retry_gives_up_after_three(tmp_path):
    t = FakeTranscriber([RuntimeError("a"), RuntimeError("b"), RuntimeError("c")])
    with pytest.raises(TranscriptionFailed, match="c"):
        transcribe_with_retry(t, tmp_path / "x.webm")


def w(text, start, end, type_="word"):
    return {"text": text, "start": start, "end": end, "type": type_}


def test_words_group_on_sentence_end_and_pause():
    sp = lambda s: w(" ", s, s, "spacing")
    words = [w("Energy", 0.0, 0.4), sp(0.4), w("first.", 0.5, 0.9), sp(0.9),
             w("Then", 1.0, 1.2), sp(1.2), w("momentum", 1.3, 1.8),
             w("(laughs)", 1.9, 2.0, "audio_event"), sp(1.8), w("so", 3.0, 3.1)]
    segs = words_to_segments(words)
    assert [(x.text, x.start, x.end) for x in segs] == [
        ("Energy first.", 0.0, 0.9), ("Then momentum", 1.0, 1.8), ("so", 3.0, 3.1)]


def test_scribe_transcriber_sends_keyterms(tmp_path):
    calls = []

    def convert(**kwargs):
        calls.append(kwargs)
        return SimpleNamespace(words=[w("Momentum.", 0.0, 0.6)])

    client = SimpleNamespace(speech_to_text=SimpleNamespace(convert=convert))
    audio = tmp_path / "a.webm"
    audio.write_bytes(b"x")
    segs = ScribeTranscriber(client=client).transcribe(audio)
    assert segs[0].text == "Momentum."
    assert calls[0]["model_id"] == "scribe_v2" and "ballistic pendulum" in calls[0]["keyterms"]
    assert calls[0]["timestamps_granularity"] == "word"


def test_make_transcriber_picks_provider():
    assert type(make_transcriber("scribe_v2", client=object())).__name__ == "ScribeTranscriber"
    assert type(make_transcriber("whisper-1", client=object())).__name__ == "OpenAITranscriber"
