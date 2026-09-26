"""Summarise one Stage A session directory: turns, rejections, refusals, coverage, latency, audio."""
import json
import statistics
import sys
from collections import Counter
from pathlib import Path


def main(session_dir: str) -> None:
    d = Path(session_dir)
    manifest = json.loads((d / "manifest.json").read_text())
    state = json.loads((d / "state.json").read_text())
    events = [json.loads(line) for line in (d / "events.jsonl").read_text().splitlines()]
    kinds = Counter(e["type"] for e in events)

    flags = [k for k in ("pilot", "simulated", "git_dirty") if manifest.get(k)]
    print(f"# {d.name}  expert={manifest['expert_id']} cell={manifest['cell']} phase={state['phase']}"
          f"{'  [' + ', '.join(flags) + ']' if flags else ''}")
    cfg = manifest["config"]
    print(f"config: interviewer {cfg.get('interviewer_provider', 'anthropic')}:{cfg['interviewer_model']} "
          f"effort={cfg['interviewer_effort']} guard {cfg.get('guard_provider', 'anthropic')}:{cfg['guard_model']} "
          f"transcriber={cfg['transcriber_model']} commit={manifest['git_commit'][:7]}")

    print("\n## Think-aloud")
    for pid in state["think_aloud_done"]:
        segs = [s for s in state["segments"] if s["problem_id"] == pid]
        typed = sum(s["id"].startswith(f"{pid}-m") for s in segs)
        parts = state.get("recordings", {}).get(f"think_{pid}", [])
        print(f"- {pid}: {len(segs)} segments{f' ({typed} typed)' if typed else ''}, {len(parts)} audio part(s)")
    corrected = kinds.get("segment_corrected", 0)
    print(f"corrections: {corrected}; keep-talking prompts: {kinds.get('keep_talking', 0)}; "
          f"untranscribed: {state.get('untranscribed') or 'none'}")

    for set_id in state["set_order"]:
        arm = state["arms"][set_id]
        dialogue = state["dialogue"].get(set_id, [])
        questions = [t for t in dialogue if t["speaker"] == "interviewer"]
        set_events = [e for e in events if e.get("set_id") == set_id]
        finished = next((e for e in set_events if e["type"] == "probe_finished"), None)
        print(f"\n## Set {set_id} ({arm})")
        if finished is None:
            print("not finished")
            continue
        print(f"elapsed {finished['elapsed']:.0f} s; questions {len(questions)} "
              f"({sum(t['is_followup'] for t in questions)} follow-ups); "
              f"uncovered stems: {finished['uncovered'] or 'none'}")
        if arm == "ai":
            sources = Counter(t["source"] for t in questions)
            reasons = [e["reason"] for e in set_events if e["type"] == "turn_rejected"]
            print(f"accepted {sources.get('ai', 0)}, bare-stem fallback {sources.get('ai_fallback', 0)}; "
                  f"rejected leading {sum(r.startswith('leading') for r in reasons)}, "
                  f"contract {sum(r.startswith('contract') for r in reasons)}; "
                  f"interviewer refused {sum(e['type'] == 'interviewer_failed' and e['reason'].startswith('LLMRefused') for e in set_events)}, "
                  f"unavailable {sum(e['type'] == 'interviewer_failed' and e['reason'].startswith('LLMUnavailable') for e in set_events)}, "
                  f"guard failures {sum(e['type'] == 'guard_failed' for e in set_events)}; "
                  f"cap reached: {any(e['type'] == 'cap_reached' for e in set_events)}")
            gaps, last = [], None
            for e in set_events:
                if e["type"] == "expert_answer":
                    last = e["t_mono"]
                elif e["type"] == "probe" and last is not None:
                    gaps.append(e["t_mono"] - last)
                    last = None
            if gaps:
                print(f"latency answer→question: median {statistics.median(gaps):.1f} s, max {max(gaps):.1f} s (n={len(gaps)})")
            answers = [t for t in dialogue if t["speaker"] == "expert"]
            print(f"answers: {len(answers)} ({sum(not t['text'].strip() for t in answers)} empty, "
                  f"{sum(t['source'] == 'typed' for t in answers)} typed)")
        else:
            parts = state.get("recordings", {}).get(f"probe_{set_id}", [])
            print(f"markers {len(state['markers'].get(set_id, []))}, stem ticks {len(state['ticks'].get(set_id, []))}, "
                  f"audio parts {len(parts)} (a part beyond the first means the tablet reloaded or hit a gap)")

    failures = [e for e in events if e["type"] == "transcription_failed"]
    print(f"\ntranscription failures: {len(failures)}; error now: {state.get('error') or 'none'}")
    gaps = [f"{stream} part {p['part']} from chunk {p['gap_at']}"
            for stream, parts in state.get("recordings", {}).items() for p in parts if "gap_at" in p]
    print(f"audio gaps (audio lost until the next part): {', '.join(gaps) or 'none'}")


if __name__ == "__main__":
    main(sys.argv[1])
