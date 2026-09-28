"""N1 gate fixtures: every illustrative item of docs/n1-gold-shapes.md, expressed in the schema.

Content is invented and structure-faithful (the inventory marks it ILLUSTRATIVE); no gold has
been acquired (§14.3). Section letters follow the inventory. docs/n1-schema-validation.md maps
each attribute to where it lives.
"""
from __future__ import annotations

from datetime import date

from conftest import CODER, DAY, evidence, source

from residual.claims import ClaimRecord, Scope
from residual.gates import Measurement, measure
from residual.ledger import Area, Ledger
from residual.provenance import Agent, Evidence, Selector, Source, Verdict, Verification
from residual.vocab import KnowledgeType as K
from residual.vocab import Layer, Question, SourceKind, Tacitness, Voice, World

SECOND_CODER = Agent(kind="human", id="coder-2")

MATHS = Scope(domain="mathematics", task="fractions and rounding")
GEOMETRY = Scope(domain="mathematics", task="composite-figure area")
MECHANICS = Scope(domain="mechanics", task="forces, excluding conservation")
CRIC = Scope(domain="surgery", task="cricothyrotomy")
NICU = Scope(domain="neonatal nursing", task="early detection of infant distress")
DEBUG = Scope(domain="programming", task="troubleshooting")
FIRE = Scope(domain="firefighting", task="flashover judgement")
AVIONICS = Scope(domain="aircraft maintenance", task="avionics troubleshooting")
POULTRY = Scope(domain="poultry", task="chick sexing")
LIBFOO = Scope(domain="oss", task="networking", organisation="libfoo")
LOGSTORE = Scope(domain="oss", task="storage design", organisation="logstore")


def cite(src: Source, exact: str | None, locator: str, verifier: Agent = CODER) -> Evidence:
    return Evidence(source=src, selector=Selector(exact=exact, locator=locator), retrieved=DAY,
                    verification=Verification(verdict=Verdict.SUPPORTS, verifier=verifier, on=DAY))


def gold(assertion: str, q: Question, layer: Layer, k: K, scope: Scope, *ev: Evidence,
         tacit: Tacitness = Tacitness.UNASSESSED, **kw) -> ClaimRecord:
    return ClaimRecord(assertion=assertion, question=q, layer=layer, knowledge_type=k,
                       tacitness=tacit, scope=scope, evidence=ev, **kw)


# --- A. Mathematics and education --------------------------------------------------------

EEDI_GRAPH = source("eedi-misconception-graph", kind=SourceKind.STUDY, voice=Voice.NOVICE,
                    published=date(2025, 6, 1))
NEURIPS = source("arXiv:2007.12061", kind=SourceKind.LEARNER_RESPONSE, voice=Voice.NOVICE,
                 published=date(2020, 7, 1))
DATASHOP_76 = source("datashop:76", kind=SourceKind.LOG, voice=Voice.NOVICE,
                     published=date(2012, 6, 1))
LFA = source("doi:10.1007/11774303_17", kind=SourceKind.STUDY, voice=Voice.NOVICE,
             published=date(2006, 1, 1))
AAAS = source("aaas-project-2061", kind=SourceKind.LEARNER_RESPONSE, voice=Voice.NOVICE,
              published=date(2012, 1, 1))
AAAS_DESIGN = source("aaas-project-2061-item-design", kind=SourceKind.STUDY, voice=Voice.EXPERT,
                     independence_key="aaas-project-2061", published=date(2012, 1, 1))
FCI = source("doi:10.1119/1.2343497", kind=SourceKind.STUDY, voice=Voice.EXPERT,
             published=date(1992, 3, 1))

ADD_DENOMINATORS = gold(
    "Believes that you add the denominators when adding fractions.",
    Question.DIFFICULTY, Layer.LEARNER, K.MISCONCEPTION, MATHS,
    cite(EEDI_GRAPH, "Believes that you add the denominators when adding fractions",
         "misconception id 1507"),
    cite(NEURIPS, None, "Q#4417 option C ('2/7' for 1/3 + 1/4): 31% of wrong answers"))
ROUNDING = gold(
    "When rounding to one decimal place, looks at the second digit after the one being rounded.",
    Question.DIFFICULTY, Layer.LEARNER, K.MISCONCEPTION, MATHS,
    cite(EEDI_GRAPH, "looks at the second digit after the one being rounded", "misconception id 2210"),
    cite(NEURIPS, None, "Q#8120 (round 3.4651 to 1 d.p.): A 52% correct, B 29% (linked), C 12%, D 7%"))
BACKWARD_AREA = gold(
    "Finding a missing side from a composite figure's area and one side ('backward area') is a "
    "separate, harder skill than computing the area from its sides.",
    Question.DIFFICULTY, Layer.LEARNER, K.PROCEDURE_STEP, GEOMETRY,
    cite(DATASHOP_76, None, "KC model 'LFA-split': steps solve-for-side-*"),
    cite(LFA, "backward area", "results, geometry dataset"),
    tacit=Tacitness.AUTOMATED)
STEP_TO_KC = gold(
    "Step solve-for-side-1 exercises the backward-area skill.",
    Question.DOMAIN, Layer.LEARNER, K.PREREQUISITE, GEOMETRY,
    cite(DATASHOP_76, None, "Q-matrix, step solve-for-side-1, KC backward-area"))
AAAS_CHOICE = gold(
    "Choosing B, 'the ball's force runs out at the top', indicates the idea that motion requires "
    "a continuing force.",
    Question.DOMAIN, Layer.DIAGNOSIS, K.MISCONCEPTION, MECHANICS,
    cite(AAAS_DESIGN, "motion requires a continuing force", "item 'energy transfer, ball thrown upward', choice B"))
AAAS_DISTRIBUTION = gold(
    "In grade 8, 34% of students choose 'the ball's force runs out at the top' for a ball thrown upward.",
    Question.DIFFICULTY, Layer.LEARNER, K.MISCONCEPTION, MECHANICS,
    cite(AAAS, None, "item 'energy transfer, ball thrown upward', grade 8: A 38%, B 34%, C 18%, D 10%"))
FCI_IMPETUS = gold(
    "On FCI item 13, option C ('the force of the throw, gradually decreasing') indicates the "
    "impetus conception: an impetus is dissipated.",
    Question.DOMAIN, Layer.DIAGNOSIS, K.MISCONCEPTION, MECHANICS,
    cite(FCI, "impetus dissipation", "Table II, item 13, option C"))

MATHS_GOLD = Ledger(
    purpose="gold",
    claims=(ADD_DENOMINATORS, ROUNDING, BACKWARD_AREA, STEP_TO_KC, AAAS_CHOICE,
            AAAS_DISTRIBUTION, FCI_IMPETUS),
)


def prevalence() -> dict[str, Measurement]:
    """E-MISC's weights: prevalence as a measurement over the item it weights (§14.1 wᵢ)."""
    return {
        ADD_DENOMINATORS.claim_id: measure("prevalence", 0.31, [ADD_DENOMINATORS]),
        ROUNDING.claim_id: measure("prevalence", 0.29, [ROUNDING]),
    }


# --- B. Clinical and professional ---------------------------------------------------------

SULLIVAN = source("doi:10.1097/ACM.0000000000000224", kind=SourceKind.ELICITATION_RECORD,
                  voice=Voice.EXPERT, published=date(2014, 5, 1))
CRANDALL = source("doi:10.1097/00012272-199309000-00006", kind=SourceKind.ELICITATION_RECORD,
                  voice=Voice.EXPERT, published=date(1993, 9, 1))
CHAO = source("doi:10.1080/10447319409526093", kind=SourceKind.ELICITATION_RECORD,
              voice=Voice.EXPERT, published=date(1994, 1, 1))
ACTA = source("acta-report-fireground", kind=SourceKind.ELICITATION_RECORD, voice=Voice.EXPERT,
              published=date(1998, 1, 1))
PARI = source("doi:10.21236/ada303654", kind=SourceKind.ELICITATION_RECORD, voice=Voice.EXPERT,
              published=date(1995, 1, 1))
BIEDERMAN = source("doi:10.1037/0278-7393.13.4.640", kind=SourceKind.STUDY, voice=Voice.EXPERT,
                   published=date(1987, 10, 1))

MEMBRANE = gold(
    "The cricothyroid membrane lies between the thyroid and cricoid cartilages; the cricothyroid "
    "arteries run along its upper border.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CONCEPT, CRIC,
    cite(SULLIVAN, "cricothyroid membrane lies between", "task list, clinical-knowledge step 3"),
    tacit=Tacitness.EXPLICIT)
STABILISE = gold(
    "Stabilise the larynx with the non-dominant hand and keep it there until the tube is secured.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.PROCEDURE_STEP, CRIC,
    cite(SULLIVAN, "Stabilise the larynx with the non-dominant hand", "task list, action step 12"),
    tacit=Tacitness.AUTOMATED)
LANDMARKS = gold(
    "If landmarks cannot be palpated (obese or swollen neck), make a longer vertical skin incision "
    "before the horizontal membrane incision.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.DECISION, CRIC,
    cite(SULLIVAN, "If landmarks cannot be palpated", "task list, decision step 2"),
    tacit=Tacitness.RELATIONAL)
MOTTLED = gold(
    "Skin colour going from pink to mottled or grey signals distress hours before temperature changes.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CUE, NICU,
    cite(CRANDALL, "pink to mottled or grey", "cue list, category 'colour'"),
    tacit=Tacitness.PERCEPTUAL)
LIMP = gold(
    "An infant who stops fussing at handling and becomes limp may be in early distress.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CUE, NICU,
    cite(CRANDALL, "stops fussing at handling and becomes limp", "cue list, category 'muscle tone'"),
    tacit=Tacitness.PERCEPTUAL)
PRINT_PROBE = gold(
    "Insert a print before the loop exit to see whether the loop ends.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CHECK, DEBUG,
    cite(CHAO, "insert a print before the loop exit", "diagnostic action, expert 4"),
    tacit=Tacitness.AUTOMATED)
PRINT_READING = gold(
    "If the value never prints, the loop condition, not the body, is at fault.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.INTERPRETATION, DEBUG,
    cite(CHAO, "the loop condition, not the body, is at fault", "interpretation, expert 4"),
    tacit=Tacitness.AUTOMATED)
FLASHOVER_CUE = gold(
    "Smoke darkening and pushing from low openings, and heat felt through the glove, signal "
    "imminent flashover.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CUE, FIRE,
    cite(ACTA, "smoke darkening and pushing from low openings", "demands table row 1, cues"),
    tacit=Tacitness.PERCEPTUAL)
FLASHOVER_STRATEGY = gold(
    "When flashover signs appear, withdraw and ventilate before committing crews.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.STRATEGY, FIRE,
    cite(ACTA, "withdraw and ventilate first", "demands table row 1, strategies"))
FLASHOVER_ERROR = gold(
    "Crews are committed on visible flame alone.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.FAILURE_MODE, FIRE,
    cite(ACTA, "committing crews on visible flame alone", "demands table row 1, common errors"))
FLASHOVER_WHY = ClaimRecord(
    assertion="Judging imminent flashover is difficult because the cues are subtle and time is short.",
    question=Question.DIFFICULTY, layer=Layer.LEARNER, knowledge_type=K.RATIONALE, scope=FIRE,
    evidence=(cite(ACTA, "the cues are subtle and the time is short", "demands table row 1, why difficult"),))
"""Experts' account of difficulty: §2 says it cannot answer 'what is difficult', so it is
excluded and the claim is unknown, never gold."""
PSU_PRECURSOR = gold(
    "Rule out the power supply first because it is the cheapest check.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.RATIONALE, AVIONICS,
    cite(PARI, "rule out the power supply first", "problem 7, step 1, precursor"))
PSU_ACTION = gold(
    "Measure 28 V at test point J4.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CHECK, AVIONICS,
    cite(PARI, "measure 28 V at test point J4", "problem 7, step 1, action"),
    tacit=Tacitness.AUTOMATED)
PSU_READING = gold(
    "A reading near 28 V at J4 means the supply is good and the fault is downstream, in the signal path.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.INTERPRETATION, AVIONICS,
    cite(PARI, "the fault is downstream", "problem 7, step 1, interpretation"))
EMINENCE = gold(
    "A rounded, convex eminence marks a male chick, and a flat or concave one a female.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.CUE, POULTRY,
    cite(BIEDERMAN, "shape of the eminence", "instruction sheet, contrasting photographs"),
    tacit=Tacitness.PERCEPTUAL)

CLINICAL_GOLD = Ledger(
    purpose="gold",
    claims=(MEMBRANE, STABILISE, LANDMARKS, MOTTLED, LIMP, PRINT_PROBE, PRINT_READING,
            FLASHOVER_CUE, FLASHOVER_STRATEGY, FLASHOVER_ERROR, PSU_PRECURSOR, PSU_ACTION,
            PSU_READING, EMINENCE),
    areas=(Area(area_id="cric:airway-access", scope=CRIC, name="gaining airway access"),
           Area(area_id="fire:flashover", scope=FIRE, name="flashover judgement")),
    assignments=((STABILISE.claim_id, "cric:airway-access"), (LANDMARKS.claim_id, "cric:airway-access"),
                 (FLASHOVER_CUE.claim_id, "fire:flashover"), (FLASHOVER_STRATEGY.claim_id, "fire:flashover"),
                 (FLASHOVER_ERROR.claim_id, "fire:flashover")),
)


# --- C. OSS and organisational ------------------------------------------------------------

def libfoo(identifier: str, kind: SourceKind, published: date, voice: Voice = Voice.MIXED) -> Source:
    return source(identifier, kind=kind, world=World.B, voice=voice, organisation="libfoo",
                  published=published, independence_key=identifier)


ISSUE_2211 = libfoo("libfoo#2211", SourceKind.ISSUE, date(2019, 7, 2))
FIX_COMMIT = libfoo("libfoo@9c1e", SourceKind.COMMIT, date(2019, 8, 12))
CAP_COMMIT = libfoo("libfoo@a1b2", SourceKind.COMMIT, date(2018, 11, 5), Voice.EXPERT)
REVIEWS = [libfoo(f"libfoo!{n}", SourceKind.REVIEW_THREAD, date(2019, 5, n), Voice.EXPERT)
           for n in (3, 9, 17, 24)]
README = libfoo("libfoo:README.md@2.1", SourceKind.DOCUMENTATION, date(2020, 2, 1), Voice.EXPERT)
RELEASE_2_0 = libfoo("libfoo@v2.0", SourceKind.COMMIT, date(2020, 1, 10), Voice.EXPERT)
LOGSTORE_DISCUSSION = source("logstore/discussions/88", kind=SourceKind.FORUM_POST, world=World.B,
                             organisation="logstore", published=date(2021, 4, 2))

RATIONALE_SOUGHT = gold(
    "Contributors do not know why retry backoff in src/net/retry.c is capped at 7 attempts.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.RATIONALE, LIBFOO,
    cite(ISSUE_2211, "Does anyone know why backoff is capped at 7 retries?", "issue #2211"),
    cite(ISSUE_2211, "Does anyone know why backoff is capped at 7 retries?", "issue #2211",
         verifier=SECOND_CODER))
"""A post-t outcome item, double-coded rationale-seeking: two coders, two verifications."""
DEFECT_FIX = gold(
    "Retry backoff in src/net/retry.c overflowed its timer after the seventh attempt.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.FAILURE_MODE, LIBFOO,
    cite(FIX_COMMIT, "fix timer overflow after 7th retry", "commit 9c1e, src/net/retry.c"))
CAP_CHANGE = gold(
    "The retry limit in src/net/retry.c was raised from 3 to 7.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.DECISION, LIBFOO,
    cite(CAP_COMMIT, "retry limit 3 -> 7", "commit a1b2, src/net/retry.c"),
    valid_from=date(2018, 11, 5))
CHANGELOG_NORM = gold(
    "New public APIs need a CHANGELOG entry and a deprecation note.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.NORM, LIBFOO,
    *(cite(r, "please add a CHANGELOG entry and a deprecation note", f"review {r.identifier}")
      for r in REVIEWS),
    tacit=Tacitness.COLLECTIVE)
LEGACY_DOC = gold(
    "Start the server with the --legacy flag.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.PROCEDURE_STEP, LIBFOO,
    cite(README, "--legacy", "README, 'Running'"))
LEGACY_REMOVED = gold(
    "The --legacy flag no longer exists.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.PROCEDURE_STEP, LIBFOO,
    cite(RELEASE_2_0, "remove --legacy", "v2.0 release commit"),
    valid_from=date(2020, 1, 10))
APPEND_ONLY = gold(
    "Use an append-only log instead of in-place updates.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.DECISION, LOGSTORE,
    cite(LOGSTORE_DISCUSSION, "append-only log", "discussion #88"))
APPEND_ONLY_WHY = gold(
    "An append-only log gives crash recovery without fsync ordering, and cheaper replication.",
    Question.PERFORMANCE, Layer.PERFORMANCE, K.RATIONALE, LOGSTORE,
    cite(LOGSTORE_DISCUSSION, "crash recovery without fsync ordering", "discussion #88"))

RETRY_UNIT = Area(area_id="libfoo:src/net/retry.c", scope=LIBFOO, name="src/net/retry.c")
STORAGE_UNIT = Area(area_id="logstore:storage", scope=LOGSTORE, name="storage engine")
T = date(2019, 3, 1)
"""E-OSS freeze time: before dev_07 leaves on 2019-04-15."""

OSS_GOLD = Ledger(
    purpose="gold",
    claims=(RATIONALE_SOUGHT, DEFECT_FIX, CAP_CHANGE, CHANGELOG_NORM, LEGACY_DOC, LEGACY_REMOVED,
            APPEND_ONLY, APPEND_ONLY_WHY),
    areas=(RETRY_UNIT, STORAGE_UNIT),
    assignments=((RATIONALE_SOUGHT.claim_id, RETRY_UNIT.area_id), (DEFECT_FIX.claim_id, RETRY_UNIT.area_id),
                 (CAP_CHANGE.claim_id, RETRY_UNIT.area_id), (APPEND_ONLY.claim_id, STORAGE_UNIT.area_id),
                 (APPEND_ONLY_WHY.claim_id, STORAGE_UNIT.area_id)),
)

DOC_CONTRADICTION_METHOD = "documentation-issue taxonomy [116]: outdated"
