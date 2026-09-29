"""§11.8: a smoke test over the three real N2 ledgers, skipped if they (or their closure-judge
caches under research/n3/) are missing. Judging is replay-only here (no network): it reads the
same `closure_judgements.json` the real `research/n3/<domain>` run commits, so this test is fast
and reproducible from that committed cache. It asserts the counts THIS implementation actually
produces, not any earlier prototype's or revision's numbers; see research/n3/README.md for
commentary. Re-measured for the final narrow fix round (2026-09-29b, fix 1's integer-id closure
judge): the cache keys changed because the judge prompt's sentence numbering changed, so all
three domains were re-run live against Ollama and replayed byte-identical before these counts
were taken."""
import json
from pathlib import Path

import pytest
from residual.ledger import Ledger
from residual.vocab import CRITERION_LABELS, EpistemicLabel

from gapmap import __main__ as cli
from gapmap import judge as judge_mod

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "reconstruct" / "runs"
PLC_DIR = RUNS / "20260928T133336Z-59ec876b3d7e"
GDPR_V1_DIR = RUNS / "20260928T135354Z-eb840a85b7d1"
GDPR_V2_DIR = RUNS / "20260928T145943Z-bc1cc9a30a02"
N3 = ROOT / "research" / "n3"

pytestmark = pytest.mark.skipif(
    not (PLC_DIR.exists() and (N3 / "plc" / "closure_judgements.json").exists()),
    reason="reconstruct/runs/ or research/n3/*/closure_judgements.json not present")


def _load(run_dir: Path) -> tuple[Ledger, dict]:
    ledger = Ledger.from_json((run_dir / "ledger.json").read_text())
    sidecar = json.loads((run_dir / "sidecar.json").read_text())
    return ledger, sidecar


def _judge(domain_dir: str) -> judge_mod.CachedJudge:
    return judge_mod.CachedJudge(judge_mod.OllamaJudge(), N3 / domain_dir / "closure_judgements.json",
                                 live=False)


def _tally(res) -> dict:
    by_lens = {}
    for r in res.map:
        if r.category == "HYP":
            by_lens[r.lens] = by_lens.get(r.lens, 0) + 1
    counts = {"HYP": sum(1 for r in res.map if r.category == "HYP")}
    for cat in ("RG-SINGLE", "RG-UNVER", "RG-SIBLING", "RG-UNK", "RG-UNDECIDED"):
        counts[cat] = sum(1 for r in res.retrieval_gaps if r.category == cat)
    counts["CONTROL"] = sum(1 for r in res.map if r.category == "CONTROL")
    counts["by_lens"] = by_lens
    return counts


def test_plc():
    ledger, sidecar = _load(PLC_DIR)
    assert len(ledger.claims) == 375
    labels = {lab: sum(1 for c in ledger.claims if ledger.label(c.claim_id) is lab)
             for lab in EpistemicLabel}
    assert labels[EpistemicLabel.LITERATURE_SUPPORTED] == 321
    assert labels[EpistemicLabel.SYNTHETIC_EXTRAPOLATION] == 49
    assert labels[EpistemicLabel.UNKNOWN] == 5

    res = cli.build_gapmap(ledger, domain="PLC", judge=_judge("plc"), sidecar=sidecar)
    counts = _tally(res)
    # Final fix round (2026-09-29b): re-measured against the new integer-id closure judge
    # prompts (fix 1) -- the prior counts (HYP 9, DISC 1/DIAG 2/GUARD 1/RESULT 3/WHY 2, RG-SINGLE
    # 8) were partly an artefact of the silent id-drop bug turning some real judge answers into
    # `open`. No candidate came back `undecided` on this ledger (0 malformed/unresolvable-id
    # judge answers), so every candidate below got a genuine judged state.
    assert counts["HYP"] == 9
    assert counts["by_lens"] == {"DIAG": 2, "GUARD": 1, "RESULT": 3, "WHY": 3}
    assert counts["RG-SINGLE"] == 11
    assert counts["RG-UNVER"] == 0
    assert counts["RG-UNDECIDED"] == 0
    assert counts["CONTROL"] == 1


def test_gdpr_v1_with_v2_sibling():
    ledger, sidecar = _load(GDPR_V1_DIR)
    sibling, _ = _load(GDPR_V2_DIR)
    assert len(ledger.claims) == 271
    labels = {lab: sum(1 for c in ledger.claims if ledger.label(c.claim_id) is lab)
             for lab in EpistemicLabel}
    assert labels[EpistemicLabel.LITERATURE_SUPPORTED] == 193
    assert labels[EpistemicLabel.SYNTHETIC_EXTRAPOLATION] == 64
    assert labels[EpistemicLabel.UNKNOWN] == 14

    res = cli.build_gapmap(ledger, domain="GDPR v1", judge=_judge("gdpr_v1"), sidecar=sidecar, sibling=sibling)
    counts = _tally(res)
    # Final fix round (2026-09-29b): re-measured, see test_plc's note. 0 undecided here too.
    assert counts["HYP"] == 1
    assert counts["by_lens"] == {"RESULT": 1}
    assert counts["RG-SINGLE"] == 12
    assert counts["RG-UNVER"] == 4
    assert counts["RG-SIBLING"] == 2
    assert counts["RG-UNDECIDED"] == 0
    assert counts["CONTROL"] == 1


def test_gdpr_v2_with_v1_sibling():
    ledger, sidecar = _load(GDPR_V2_DIR)
    sibling, _ = _load(GDPR_V1_DIR)
    assert len(ledger.claims) == 523
    labels = {lab: sum(1 for c in ledger.claims if ledger.label(c.claim_id) is lab)
             for lab in EpistemicLabel}
    assert labels[EpistemicLabel.LITERATURE_SUPPORTED] == 203
    assert labels[EpistemicLabel.SYNTHETIC_EXTRAPOLATION] == 305
    assert labels[EpistemicLabel.UNKNOWN] == 15
    assert sidecar["n3_input"] is True
    pending = sum(1 for c in ledger.claims for e in c.evidence if e.verification.verdict.value == "pending")
    assert pending == 140

    res = cli.build_gapmap(ledger, domain="GDPR v2", judge=_judge("gdpr_v2"), sidecar=sidecar, sibling=sibling)
    assert res.admissible is False  # 140 pending verdicts
    assert "pending" in res.admissibility_note
    counts = _tally(res)
    # Final fix round (2026-09-29b): re-measured, see test_plc's note. 0 undecided here too.
    assert counts["HYP"] == 6
    assert counts["by_lens"] == {"DISC": 1, "HEDGE": 1, "RESULT": 3, "WHY": 1}
    assert counts["RG-SINGLE"] == 3
    assert counts["RG-UNVER"] == 6
    assert counts["RG-SIBLING"] == 7
    assert counts["RG-UNDECIDED"] == 0
    assert counts["CONTROL"] == 1


def test_all_a_pool_claims_are_criterion_labelled():
    ledger, _ = _load(PLC_DIR)
    for c in ledger.claims:
        lab = ledger.label(c.claim_id)
        assert (lab in CRITERION_LABELS) == (lab is EpistemicLabel.LITERATURE_SUPPORTED
                                              or lab is EpistemicLabel.OBSERVED_HUMAN_EVIDENCE
                                              or lab is EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED)
