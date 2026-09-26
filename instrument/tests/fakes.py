class FakeClock:
    def __init__(self, t: float = 0.0):
        self.t = t

    def now(self) -> float:
        return self.t

    def advance(self, dt: float) -> None:
        self.t += dt


from pathlib import Path

from probe_app.transcribe import RawSegment


class FakeTranscriber:
    model = "fake"

    def __init__(self, results: list):
        self.results = list(results)
        self.calls: list[Path] = []

    def transcribe(self, audio_path: Path) -> list[RawSegment]:
        self.calls.append(audio_path)
        item = self.results.pop(0)
        if isinstance(item, Exception):
            raise item
        return item
