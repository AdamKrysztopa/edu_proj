"""render.py: header, the three-tier how-to-read note, and hedged hypothesis phrasing."""
from conftest import FakeJudge, a_claim, a_claim_n, area, fillers, ledger
from residual.vocab import KnowledgeType

from gapmap import __main__ as cli
from gapmap import record, render


def _result(tmp_path):
    c1 = a_claim("Loose terminal connections cause problems in the field.",
                source_id="src-1", independence_key="key-1")
    c2 = a_claim("Loose terminal issues appear intermittently in the panel.",
                source_id="src-2", independence_key="key-2")
    lg = ledger([c1, c2], areas=[area("a-1", "Area One")],
               assignments=[(c1.claim_id, "a-1"), (c2.claim_id, "a-1")])
    return cli.build_gapmap(lg, domain="test-domain", judge=FakeJudge())


def test_header_has_domain_and_hashes(tmp_path):
    res = _result(tmp_path)
    md = render.render(res)
    assert "# Gap map: test-domain" in md
    assert res.ledger_sha256 in md
    assert res.config_sha256 in md


def test_how_to_read_names_the_three_tiers(tmp_path):
    md = render.render(_result(tmp_path))
    assert "OBSERVED EVIDENCE" in md
    assert "INFERRED GAP" in md
    assert "HIDDEN-KNOWLEDGE HYPOTHESIS" in md
    assert "not hypotheses" in md.lower()


def test_hypothesis_is_hedged_not_printed_as_bare_indicative(tmp_path):
    res = _result(tmp_path)
    assert any(r.category == "HYP" for r in res.map)
    md = render.render(res)
    assert "Predicted, not observed:" in md
    assert "label: `inferred`" in md


def test_retrieval_gap_action_is_never_ask_an_expert(tmp_path):
    md = render.render(_result(tmp_path))
    assert "never to ask an expert" in md.lower()
    assert "action: ask an expert" not in md.lower()


def test_control_slot_section_present(tmp_path):
    md = render.render(_result(tmp_path))
    assert "## Control slot" in md


def test_summary_section_precedes_how_to_read_and_reports_hyp_and_rg_and_71(tmp_path):
    md = render.render(_result(tmp_path))
    assert "## Summary" in md
    assert md.index("## Summary") < md.index("## How to read this map")
    assert "**HYP:**" in md
    assert "**Retrieval gaps:**" in md
    assert "**§7.1 anti-renaming:**" in md


def test_rg_undecided_action_is_re_judge_or_inspect_never_ask_an_expert():
    conf = record.Confidence(score=0, A=0, B=0, P=0, Q=0, breadth="narrow", robustness="0/4",
                             k_step=1, k_topic=2)
    ig = record.InferredGap(statement="undecided stmt", test_id="t", closure_state="undecided")
    rec = record.Record(gap_id="g-u", lens="SEL", category="RG-UNDECIDED", anchor="anchor",
                        observed_evidence=(), inferred_gap=ig, hypothesis=None, reasoning="r",
                        missing="m", confidence=conf, alternatives=(), question=None)
    lines = render._retrieval_gap_group_block([rec])
    assert "RG-UNDECIDED" in lines[0]
    assert "re-judge or inspect" in lines[2]
    assert "never ask an expert" in lines[2]


def test_fair_control_table_reports_own_control_and_other_source_only(tmp_path):
    md = render.render(_result(tmp_path))
    assert "own rate | control rate | other-source-only rate" in md
    assert "mismatched rate" not in md  # the old straw-man wording is gone


def test_map_index_table_precedes_the_detail_records(tmp_path):
    md = render.render(_result(tmp_path))
    assert "| rank | lens | anchor | breadth | lexical robustness | k_topic |" in md
    assert md.index("| rank | lens |") < md.index("### #1")


def test_robustness_is_labelled_lexical_robustness_everywhere_and_explained(tmp_path):
    # Fix 3: r/4 is measured on the lexical construct, not re-judged, so it must never read as
    # plain "robustness" (which would suggest the judge's own decision was re-verified 4x).
    md = render.render(_result(tmp_path))
    assert "lexical robustness" in md
    assert "not re-judged" in md.lower()


def _evidence_item(cid: str, role: str, key: str) -> record.EvidenceItem:
    return record.EvidenceItem(
        claim_id=cid, epistemic_label="literature_supported", knowledge_type="procedure_step",
        area_id=None, source_identifier=cid, independence_key=key, source_kind="documentation",
        verdict="supports", span=f"span for {cid}", role=role, counts_as_attestation=True)


def _record_with_evidence(evidence, category="HYP"):
    conf = record.Confidence(score=1, A=0, B=0, P=0, Q=0, breadth="narrow", robustness="0/4",
                             k_step=1, k_topic=2)
    ig = record.InferredGap(statement="stmt", test_id="t", closure_state="open")
    hyp = (record.Hypothesis(text="t", predicted_knowledge_type=(KnowledgeType.CUE,),
                             predicted_tacitness=("relational",), channel="c")
          if category == "HYP" else None)
    return record.Record(gap_id="g-x", lens="DISC", category=category, anchor="anchor",
                         observed_evidence=tuple(evidence), inferred_gap=ig, hypothesis=hyp,
                         reasoning="r", missing="m", confidence=conf, alternatives=(), question=None,
                         rank=1)


def test_evidence_list_caps_topic_items_and_reports_the_rest():
    seed = _evidence_item("c-seed", "seed", "key-seed")
    topics = [_evidence_item(f"c-t{i}", "topic", f"key-{i % 3}") for i in range(8)]
    rec = _record_with_evidence([seed, *topics])
    lines = render._evidence_lines(rec)
    shown = [ln for ln in lines if ln.startswith("- `c-t")]
    assert len(shown) == render._EVIDENCE_TOPIC_CAP
    assert any(ln.startswith("+ 3 more topic claims across 3 keys") for ln in lines)


def test_evidence_list_prefers_distinct_independence_keys():
    seed = _evidence_item("c-seed", "seed", "key-seed")
    # 3 distinct keys among 8 topic items, cap 5: all 3 keys must be represented in the shown set.
    topics = [_evidence_item(f"c-t{i}", "topic", f"key-{i % 3}") for i in range(8)]
    rec = _record_with_evidence([seed, *topics])
    lines = render._evidence_lines(rec)
    shown_keys = {ln.split("key `")[1].split("`")[0] for ln in lines if ln.startswith("- `c-t")}
    assert shown_keys == {"key-0", "key-1", "key-2"}


def test_retrieval_gap_heading_shows_every_co_located_lens():
    shared_seed = [_evidence_item("c-shared", "seed", "key-1")]
    sel_rec = _record_with_evidence(shared_seed, category="RG-SINGLE").model_copy(
        update={"gap_id": "g-sel", "lens": "SEL", "anchor": "Diagnosis should be prioritized."})
    why_rec = _record_with_evidence(shared_seed, category="RG-SINGLE").model_copy(
        update={"gap_id": "g-why", "lens": "WHY", "anchor": "Diagnosis should be prioritized."})
    groups = render._group_retrieval_gaps([sel_rec, why_rec])
    assert len(groups) == 1
    lines = render._retrieval_gap_group_block(groups[0])
    heading = lines[0]
    assert heading.startswith("### [SEL/WHY]")
    assert "**[SEL]**" in lines and "**[WHY]**" in lines


def test_rg_unk_is_rendered_as_one_compact_table_not_one_section_each():
    claim = a_claim("An attested claim.", source_id="c1")
    a1 = area("a-1", "Fault Diagnosis")
    lg = ledger([claim], areas=[a1], assignments=[(claim.claim_id, "a-1")])
    sidecar = {"slots": [{"area_id": "a-1", "probe": "cue", "status": "unknown", "claim_ids": []},
                        {"area_id": "a-1", "probe": "decision", "status": "thin", "claim_ids": []}]}
    res = cli.build_gapmap(lg, domain="d", judge=FakeJudge(), sidecar=sidecar)
    md = render.render(res)
    assert md.count("### [RG-UNK]") == 0  # no more one heading per slot
    assert "| area | slot / question | source |" in md
    table = md.split("| area | slot / question | source |")[1].split("##")[0]
    assert "Fault Diagnosis" in table
    assert "| a-1 |" not in table  # the raw area_id never leaks into the table
