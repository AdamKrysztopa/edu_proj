from collections.abc import Callable
from dataclasses import dataclass

from probe_app.contract import (ContractState, ContractViolation, check_turn, next_fallback,
                                record, uncovered)
from probe_app.llm import LLMRefused, LLMUnavailable, TurnRequest
from probe_app.models import Anchor, DialogueTurn, InterviewerTurn, Segment
from probe_app.trace import render_transcript


@dataclass
class ProbeContext:
    set_id: str
    problems: dict[str, str]
    segments: list[Segment]
    snapshots: dict[str, bytes]


class ProbeEngine:
    def __init__(self, llm, guard, stems: dict[str, str], ctx: ProbeContext, store,
                 contract: ContractState, cap_s: float, wrap_s: float, elapsed: Callable[[], float] | None = None):
        self.llm, self.guard, self.stems, self.ctx = llm, guard, stems, ctx
        self.store, self.contract, self.cap_s, self.wrap_s = store, contract, cap_s, wrap_s
        self.elapsed = elapsed

    def _past_cap(self, turn: InterviewerTurn, source: str) -> bool:
        if self.elapsed is None or self.elapsed() < self.cap_s:
            return False
        self.store.log("cap_reached", set_id=self.ctx.set_id, uncovered=uncovered(self.contract),
                       source=source, discarded=turn.model_dump())
        return True

    def _expert_text(self, dialogue: list[DialogueTurn]) -> str:
        return "\n".join([s.text for s in self.ctx.segments] +
                         [d.text for d in dialogue if d.speaker == "expert"])

    def _problem_text(self) -> str:
        return "\n".join(f"{pid}: {text}" for pid, text in self.ctx.problems.items())

    def next_turn(self, dialogue: list[DialogueTurn], elapsed_s: float) -> DialogueTurn | None:
        set_id = self.ctx.set_id
        if elapsed_s >= self.cap_s:
            self.store.log("cap_reached", set_id=set_id, uncovered=uncovered(self.contract))
            return None
        expert_text = self._expert_text(dialogue)
        rejection = None
        for attempt in (1, 2):
            request = TurnRequest(problems=self.ctx.problems, transcript=render_transcript(self.ctx.segments),
                                  snapshots=self.ctx.snapshots, dialogue=dialogue,
                                  remaining_s=self.cap_s - elapsed_s, wrap_up=elapsed_s >= self.wrap_s,
                                  unused=uncovered(self.contract), rejection=rejection)
            try:
                turn = self.llm.next_turn(request)
            except (LLMRefused, LLMUnavailable) as e:
                self.store.log("interviewer_failed", set_id=set_id, attempt=attempt, reason=repr(e))
                if isinstance(e, LLMRefused):
                    break
                continue
            try:
                check_turn(turn, self.contract, self.ctx.segments, expert_text)
            except ContractViolation as e:
                rejection = f"contract: {e}"
                self.store.log("turn_rejected", set_id=set_id, attempt=attempt, reason=rejection,
                               turn=turn.model_dump())
                continue
            if turn.end_session:
                self.store.log("session_ended_by_interviewer", set_id=set_id, closing=turn.utterance)
                return None
            try:
                verdict = self.guard.check(turn.utterance, self._problem_text(), expert_text)
            except (LLMRefused, LLMUnavailable) as e:
                self.store.log("guard_failed", set_id=set_id, attempt=attempt, reason=repr(e))
                break
            if verdict.flagged:
                rejection = f"leading: it introduces '{verdict.introduced}', which the expert has not said"
                self.store.log("turn_rejected", set_id=set_id, attempt=attempt, reason=rejection,
                               turn=turn.model_dump())
                continue
            if self._past_cap(turn, "ai"):
                return None
            record(turn, self.contract)
            return self._emit(turn, "ai", elapsed_s)
        return self._fallback(elapsed_s)

    def _fallback(self, elapsed_s: float) -> DialogueTurn | None:
        nxt = next_fallback(self.contract)
        if nxt is None:
            self.store.log("session_ended_after_fallback", set_id=self.ctx.set_id)
            return None
        problem_id, stem_id = nxt
        turn = InterviewerTurn(utterance=self.stems[stem_id], stem_id=stem_id, problem_id=problem_id,
                               anchor=Anchor(kind="none", segment_ids=[]), is_followup=False,
                               quoted_span=None, end_session=False)
        if self._past_cap(turn, "ai_fallback"):
            return None
        record(turn, self.contract)
        return self._emit(turn, "ai_fallback", elapsed_s)

    def _emit(self, turn: InterviewerTurn, source: str, elapsed_s: float) -> DialogueTurn:
        out = DialogueTurn(speaker="interviewer", text=turn.utterance, t=elapsed_s, stem_id=turn.stem_id,
                           problem_id=turn.problem_id, is_followup=turn.is_followup, anchor=turn.anchor,
                           source=source)
        self.store.log("probe", set_id=self.ctx.set_id, turn=out.model_dump(mode="json"))
        return out
