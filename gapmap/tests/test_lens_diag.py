"""DIAG: rival causes without discriminating signs (spec §2.2). Judged per rival (S1): each
unsigned rival gets its own judge call over its own cause+effect stems; the group survives only if
>= 2 rivals remain unsigned after judging (`semantic._judge_diag`). `run_lens`'s default
`FakeJudge` closes a rival whose OWN span (always retrieved, §2.2's "r itself, using its span")
contains the literal marker CLOSES_HERE.

§2.2 grouping is a *star*: one seed plus its DIRECT rivals only (Implementation notes). Every
claim in a mutual-rival trio qualifies as its own seed, so a fully symmetric fixture like
`_three_rivals()` below yields 3 raw (unmerged) candidates over the same 3-claim group, one per
seed -- deduplicating those into one record is `rank.merge`'s job (X-Jaccard >= 0.5)."""
from conftest import a_claim, fillers, ledger, run_lens, s_claim
from residual.vocab import KnowledgeType

from gapmap import link, rank, record


def _rivals(results):
    return [(c, o, cat) for c, o, cat in results if c.lens == "DIAG"]


def _three_rivals(**kw):
    return [
        a_claim("Race conditions cause intermittent faults in the system.",
               source_id="src-1", independence_key=kw.get("k1", "key-1"),
               knowledge_type=KnowledgeType.FAILURE_MODE),
        a_claim("Ground loops cause intermittent faults in the system.",
               source_id="src-2", independence_key=kw.get("k2", "key-2"),
               knowledge_type=KnowledgeType.FAILURE_MODE),
        a_claim("Loose terminals cause intermittent faults in the system.",
               source_id="src-3", independence_key=kw.get("k3", "key-3"),
               knowledge_type=KnowledgeType.FAILURE_MODE),
    ]


def test_fires_stays_open_and_becomes_hyp_at_k_topic_2():
    hits = _rivals(run_lens("DIAG", ledger(_three_rivals())))
    assert len(hits) == 3  # one star per seed; all 3 share the same 3-claim group (see docstring)
    expected_group = hits[0][0].seeds | hits[0][0].rivals
    for cand, outcome, cat in hits:
        assert outcome.state == "open"
        assert cat == "HYP"
        assert cand.seeds | cand.rivals == expected_group  # every star covers the same 3-claim group


def test_downstream_merge_collapses_the_three_seed_views_into_one_record():
    lg = ledger(_three_rivals())
    records = []
    for cand, outcome, cat in _rivals(run_lens("DIAG", lg)):
        records.append(record.build_record(lg, "ledgersha", cand, outcome, cat, r=1))
    merged = rank.merge(records)
    assert len(merged) == 1
    assert set(merged[0].merged_from) == {r.gap_id for r in records} - {merged[0].gap_id}


def test_group_excluded_once_signs_leave_fewer_than_2_unsigned():
    # 2 of the 3 causes self-sign (their own span states a distinguishing sign, legitimately per
    # §2.2's "r itself, using its span"): every star's 2-rival set then has at most 1 unsigned
    # rival left, so no group survives.
    ground = a_claim("Ground loops cause intermittent faults in the system.",
                     exact="CLOSES_HERE: ground loop interference has a facility-wide pattern.",
                     source_id="src-2", independence_key="key-2", knowledge_type=KnowledgeType.FAILURE_MODE)
    loose = a_claim("Loose terminals cause intermittent faults in the system.",
                    exact="CLOSES_HERE: a loose terminal shows visible play under load.",
                    source_id="src-3", independence_key="key-3", knowledge_type=KnowledgeType.FAILURE_MODE)
    race = a_claim("Race conditions cause intermittent faults in the system.",
                   source_id="src-1", independence_key="key-1", knowledge_type=KnowledgeType.FAILURE_MODE)
    hits = _rivals(run_lens("DIAG", ledger([race, ground, loose])))
    assert len(hits) == 3  # diag() still fires a star per seed; judging drops all 3 afterward
    assert all(outcome.state == "closed" for _cand, outcome, cat in hits)
    assert all(cat is None for _cand, _outcome, cat in hits)


def test_a_synthetic_only_sign_leaves_the_rival_unsigned():
    # Only a CLOSED (A) sign removes a rival from "unsigned" -- a synthetic (S) sign still counts
    # as unsigned, so the group survives (state stays open, unlike a genuine A closure above).
    claims = _three_rivals()
    synth = s_claim("Ground loop interference has a facility-wide pattern.",
                    exact="CLOSES_HERE: ground loop interference has a facility-wide pattern.",
                    source_id="synth-sign")
    hits = _rivals(run_lens("DIAG", ledger([*claims, synth])))
    assert len(hits) == 3
    assert all(outcome.state == "open" for _cand, outcome, _cat in hits)


def test_k_topic_1_becomes_rg_single():
    hits = _rivals(run_lens("DIAG", ledger(_three_rivals(k1="same", k2="same", k3="same"))))
    assert len(hits) == 3
    assert all(cat == "RG-SINGLE" for _cand, _outcome, cat in hits)


def test_f6_regression_cause_stem_jaccard_blocks_near_duplicate_causes():
    # F6: rivals need 0 shared non-common cause stems AND a full cause-stem Jaccard below 0.5.
    # Three causes that differ by one word each but are otherwise identical share a high
    # full-stem Jaccard and must not be treated as rivals, even with 0 *non-common* stems shared.
    a = a_claim("Primary sensor calibration drift causes intermittent widget failure events "
               "during startup.", source_id="dup-a", independence_key="dup-a",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    b = a_claim("Secondary sensor calibration drift causes intermittent widget failure events "
               "during startup.", source_id="dup-b", independence_key="dup-b",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    c = a_claim("Tertiary sensor calibration drift causes intermittent widget failure events "
               "during startup.", source_id="dup-c", independence_key="dup-c",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    hits = _rivals(run_lens("DIAG", ledger([a, b, c])))
    assert hits == []  # near-duplicate causes never form a rival group


def test_s3_defect3_pairwise_dedup_drops_a_near_duplicate_rival():
    # S3 defect 3: even among ONE seed's own direct rivals, drop a rival whose cause-stem
    # Jaccard with an already-kept rival is >= 0.5 (or which shares a non-common cause stem with
    # it). "loose terminals" and "loose connectors" are both direct rivals of "race conditions"
    # (each independently clears the seed's rival_edge test) but are themselves near-duplicates.
    race = a_claim("Race conditions cause intermittent faults in the system.",
                   source_id="r-1", independence_key="r-1", knowledge_type=KnowledgeType.FAILURE_MODE)
    ground = a_claim("Ground loops cause intermittent faults in the system.",
                     source_id="r-2", independence_key="r-2", knowledge_type=KnowledgeType.FAILURE_MODE)
    loose_a = a_claim("Loose terminals cause intermittent faults in the system.",
                      source_id="r-3a", independence_key="r-3a", knowledge_type=KnowledgeType.FAILURE_MODE)
    loose_b = a_claim("Loose connectors cause intermittent faults in the system.",
                      source_id="r-3b", independence_key="r-3b", knowledge_type=KnowledgeType.FAILURE_MODE)
    # Filler claims dilute "loose"'s share of the A pool below the 5% common-stem cut, so it is
    # not excluded from the cause-stem comparison between loose_a and loose_b (§1.3).
    hits = _rivals(run_lens("DIAG", ledger([race, ground, loose_a, loose_b, *fillers(40)])))
    race_star = next(c for c, _o, _cat in hits if race.claim_id in c.seeds)
    assert not ({loose_a.claim_id, loose_b.claim_id} <= race_star.rivals)


def test_regression_chain_does_not_blob_transitively_linked_members():
    # A group is one seed plus its DIRECT rivals only. Build a rivalry path A-B-C-D (each
    # adjacent pair shares >= 2 effect stems; A/C, B/D and A/D do not) -- no group may contain
    # both chain ends.
    a = a_claim("Alpha beta conditions lead to intermittent widget failure.",
               source_id="chain-a", independence_key="chain-a", knowledge_type=KnowledgeType.FAILURE_MODE)
    b = a_claim("Gamma delta conditions lead to intermittent widget malfunction.",
               source_id="chain-b", independence_key="chain-b", knowledge_type=KnowledgeType.FAILURE_MODE)
    c = a_claim("Epsilon zeta conditions lead to widget malfunction event.",
               source_id="chain-c", independence_key="chain-c", knowledge_type=KnowledgeType.FAILURE_MODE)
    d = a_claim("Eta theta conditions lead to malfunction event occurrence.",
               source_id="chain-d", independence_key="chain-d", knowledge_type=KnowledgeType.FAILURE_MODE)
    hits = _rivals(run_lens("DIAG", ledger([a, b, c, d])))
    assert len(hits) == 2  # only b and c have >= 2 direct rivals each; a and d have only 1
    for cand, _outcome, _cat in hits:
        members = cand.seeds | cand.rivals
        assert not ({a.claim_id, d.claim_id} <= members)


def test_anchor_is_the_full_sentence_trimmed_to_80_chars_at_a_word_boundary():
    # Fix 4: the earlier "never trimmed" behaviour produced fragments like "of intermittent PLC
    # faults and should be checked during" when the CAUSE marker split mid-sentence (see
    # test_anchor_regression_full_sentence_not_a_mid_sentence_fragment below). The anchor is now
    # the FULL sentence containing the marker, trimmed at a word boundary to <= 80 characters.
    long_effect = ("an extremely long and detailed intermittent failure description that "
                   "exceeds eighty characters in total printed length for this regression test")
    a = a_claim(f"Race conditions cause {long_effect}.", source_id="long-a", independence_key="long-a",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    b = a_claim(f"Ground loops cause {long_effect}.", source_id="long-b", independence_key="long-b",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    c = a_claim(f"Loose terminals cause {long_effect}.", source_id="long-c", independence_key="long-c",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    hits = _rivals(run_lens("DIAG", ledger([a, b, c])))
    assert hits
    for cand, _outcome, _cat in hits:
        assert len(cand.anchor) <= 80
        assert "rival causes of" not in cand.anchor  # the anchor is the clause, not a stem-soup label


def test_anchor_regression_full_sentence_not_a_mid_sentence_fragment():
    # The motivating bug (task 4): "Loose terminal connections are a common cause of intermittent
    # PLC faults and should be checked during troubleshooting." splits the CAUSE marker "cause"
    # mid-sentence; the old effect-only anchor was the fragment "of intermittent PLC faults and
    # should be checked during troubleshooting." (no subject, starts with a preposition). The new
    # anchor is the full sentence, trimmed at a word boundary to <= 80 chars, so it never starts
    # with a bare preposition like "of ".
    a = a_claim("Loose terminal connections are a common cause of intermittent PLC faults and "
               "should be checked during troubleshooting.", source_id="frag-a", independence_key="frag-a",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    b = a_claim("Ground loops are a common cause of intermittent PLC faults and should be "
               "checked during troubleshooting.", source_id="frag-b", independence_key="frag-b",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    c = a_claim("Race conditions are a common cause of intermittent PLC faults and should be "
               "checked during troubleshooting.", source_id="frag-c", independence_key="frag-c",
               knowledge_type=KnowledgeType.FAILURE_MODE)
    hits = _rivals(run_lens("DIAG", ledger([a, b, c])))
    a_star = next(cand for cand, _o, _cat in hits if a.claim_id in cand.seeds)
    assert not a_star.anchor.lower().startswith("of ")
    assert a_star.anchor.startswith("Loose terminal connections")
    assert len(a_star.anchor) <= 80


def test_hypothesis_text_lists_verbatim_rival_cause_phrases():
    hits = _rivals(run_lens("DIAG", ledger(_three_rivals())))
    all_text = " ".join(cand.hypothesis_text for cand, _o, _cat in hits)
    for word in ("Race conditions", "Ground loops", "Loose terminals"):
        assert word in all_text  # each appears as a RIVAL's bullet in at least one star
    assert "- " in all_text  # a bullet list, not a fragment-concatenated sentence


def test_undecided_rival_makes_the_whole_group_undecided_not_open():
    # Fix 1: an undecided per-rival judgement (malformed JSON / an unresolvable cited id) must not
    # silently count as "genuinely unsigned" and leave the group looking like an ordinary open HYP.
    from gapmap import semantic

    class _MalformedJudge:
        model_id = "malformed"

        def ask(self, prompt):
            return None  # OllamaJudge's own sentinel for unparseable model output

    hits = _rivals(run_lens("DIAG", ledger(_three_rivals()), judge=_MalformedJudge()))
    assert len(hits) == 3
    assert all(outcome.state == "undecided" for _cand, outcome, _cat in hits)
    assert all(cat == "RG-UNDECIDED" for _cand, _outcome, cat in hits)


def test_s3_defect1_promo_excluded_seed_does_not_fire():
    claims = _three_rivals()
    promo = a_claim("Race conditions cause intermittent faults in the system.",
                    exact="We replaced the old scanner with our new AI agent for this.",
                    source_id="https://www.plclogs.com/post", independence_key="key-1",
                    knowledge_type=KnowledgeType.FAILURE_MODE)
    hits = _rivals(run_lens("DIAG", ledger([promo, *claims[1:]])))
    assert all(promo.claim_id not in (c.seeds | c.rivals) for c, _o, _cat in hits)
