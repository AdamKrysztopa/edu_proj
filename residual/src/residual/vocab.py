"""Controlled vocabularies (REORIENTATION.md §2, §6, §10, §13).

Each vocabulary is a closed set. Where a term has a consequence, the consequence lives here
as a table, next to the term, so a change to one is a change to the other.
"""
from __future__ import annotations

from enum import StrEnum


class EpistemicLabel(StrEnum):
    """§6. Exactly one per claim, computed from its evidence (claims.py), never asserted."""

    OBSERVED_HUMAN_EVIDENCE = "observed_human_evidence"
    LITERATURE_SUPPORTED = "literature_supported"
    ORGANISATIONAL_ARTEFACT_SUPPORTED = "organisational_artefact_supported"
    INFERRED = "inferred"
    SYNTHETIC_EXTRAPOLATION = "synthetic_extrapolation"
    UNKNOWN = "unknown"


CRITERION_LABELS = frozenset({
    EpistemicLabel.OBSERVED_HUMAN_EVIDENCE,
    EpistemicLabel.LITERATURE_SUPPORTED,
    EpistemicLabel.ORGANISATIONAL_ARTEFACT_SUPPORTED,
})
"""The only labels a gate may read as a criterion. Inferred is a hypothesis; synthetic is a
predictor at most; unknown feeds the gap map."""


class World(StrEnum):
    """§13. Which body of evidence a source belongs to, not how it was accessed: public learner
    datasets are World A; a public open-source project's own artefacts are World B."""

    A = "public"
    B = "organisational"
    C = "human"


class Question(StrEnum):
    """§2. The six questions a claim can answer; they have different primary evidence."""

    DOMAIN = "domain"                    # What is the domain?
    PERFORMANCE = "performance"          # What does competent performance look like?
    DIFFICULTY = "difficulty"            # What is difficult?
    LEARNER_STATE = "learner_state"      # What does this person know?
    NEXT_STEP = "next_step"              # What should they learn next?
    INSTRUCTION = "instruction"          # How should it be taught?


class Layer(StrEnum):
    """§10: the representation layer an assertion belongs to. L0 terminology and L6 epistemics
    are not claims; L6 is this package."""

    DOMAIN_STRUCTURE = "L1"
    PERFORMANCE = "L2"
    LEARNER = "L3"
    DIAGNOSIS = "L4"
    INSTRUCTION = "L5"


class Certainty(StrEnum):
    """GRADE-like level [99] for a body of evidence; §6 gates literature 'at its graded
    certainty'. No validated scale exists for elicited knowledge (§10.2 item 4)."""

    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    VERY_LOW = "very_low"


class KnowledgeType(StrEnum):
    """What kind of unit a claim states: the content axis. Generalised from the codebook's nine
    operation types (instrument/codebook/v0.md) and the item types of §14.1. Why it goes unsaid
    is the separate Tacitness axis."""

    CONCEPT = "concept"                  # concept, principle, fact or taxonomic relation
    MENTAL_MODEL = "mental_model"        # the model of the system or situation reasoned with
    PREREQUISITE = "prerequisite"        # knowledge another unit depends on
    PROCEDURE_STEP = "procedure_step"    # an action in an ordered procedure
    DECISION = "decision"                # the condition that selects an action, method or principle, or rules one out
    CUE = "cue"                          # a feature of the situation noticed that triggers or informs a decision
    REPRESENTATION = "representation"    # choosing the form, diagram, system or quantity to work in
    STRATEGY = "strategy"                # decomposition or heuristic: how to split or approach the work
    CHECK = "check"                      # a check on a step or result, or a guard against a known error
    EXPECTANCY = "expectancy"            # what should happen next, or typical values
    INTERPRETATION = "interpretation"    # what an observed result means for the working hypothesis
    FAILURE_MODE = "failure_mode"        # a characteristic way the work goes wrong, and its signs
    METACOGNITION = "metacognition"      # monitoring of progress, difficulty, confidence or plan
    NORM = "norm"                        # what counts as acceptable work, argument or answer
    RATIONALE = "rationale"              # why something is done or was decided
    MISCONCEPTION = "misconception"      # a hypothesised erroneous belief or malrule, held with its evidence
    EXPERT_NOVICE_CONTRAST = "expert_novice_contrast"  # expert has / novice lacks or substitutes


class Tacitness(StrEnum):
    """Why the knowledge may be unsaid: Collins's relational / somatic / collective [15] and the
    two omission mechanisms of §2. It routes a gap to its channel (§10.3)."""

    UNASSESSED = "unassessed"
    EXPLICIT = "explicit"                # written, or verbalised on request
    RELATIONAL = "relational"            # unwritten for contingent reasons; explicable in principle
    AUTOMATED = "automated"              # compiled procedure or self-check; not available to introspection
    PERCEPTUAL = "perceptual"            # a discrimination learned by exposure to contrasting cases
    SOMATIC = "somatic"                  # tied to the body; explanation does not confer the skill
    COLLECTIVE = "collective"            # held in social practice


BEHAVIOUR_ONLY = frozenset({Tacitness.AUTOMATED, Tacitness.PERCEPTUAL,
                            Tacitness.SOMATIC, Tacitness.COLLECTIVE})
"""Text cannot cover these (§10.3, R12): an area holding them is never 'covered' by text alone."""


class Practice(StrEnum):
    """Safety-II [19]: what a source can say about how work is done."""

    IMAGINED = "imagined"    # prescribes or describes work as it should be done
    DONE = "done"            # records work as it was done
    REPORTED = "reported"    # someone's account of work, neither prescription nor record


class Voice(StrEnum):
    """Whose performance or judgement a source records. §2: learner difficulty is never taken
    from expert or machine judgement alone."""

    EXPERT = "expert"
    NOVICE = "novice"        # learners, newcomers, trainees
    MIXED = "mixed"          # boundary material where a novice's error makes an expert articulate
    MACHINE = "machine"


class SourceKind(StrEnum):
    TEXTBOOK = "textbook"
    STUDY = "study"
    STANDARD = "standard"
    PROCEDURE_DOCUMENT = "procedure_document"   # SOP, protocol, guideline, runbook
    DOCUMENTATION = "documentation"             # wiki, README, CONTRIBUTING, manual
    FORUM_POST = "forum_post"
    DESIGN_RECORD = "design_record"             # ADR, design doc, rationale artefact
    ISSUE = "issue"                             # ticket, bug report
    COMMIT = "commit"
    REVIEW_THREAD = "review_thread"
    LOG = "log"                                 # event, process or work-order log
    INCIDENT_REPORT = "incident_report"
    LEARNER_RESPONSE = "learner_response"       # response data, individual or aggregate
    THINK_ALOUD = "think_aloud"
    INTERVIEW = "interview"
    OBSERVATION = "observation"
    ELICITATION_RECORD = "elicitation_record"   # a CTA task list, cue inventory or coded operation list


HUMAN_RECORD_KINDS = frozenset({
    SourceKind.LEARNER_RESPONSE, SourceKind.THINK_ALOUD, SourceKind.INTERVIEW,
    SourceKind.OBSERVATION,
})
"""Direct records of human performance or response (§6 'observed human evidence'). A published
elicitation record is not one: it is a synthesis in published work, so literature (§6)."""

WORLD_C_KINDS = HUMAN_RECORD_KINDS | {SourceKind.ELICITATION_RECORD}
"""World C holds only what this project records from humans, including its own coded lists."""

DIFFICULTY_KINDS = frozenset({SourceKind.LEARNER_RESPONSE, SourceKind.LOG, SourceKind.STUDY})
"""§2: 'What is difficult?' is answered by learner response data and error logs, or a study
reporting them, never by expert or machine judgement."""

PRACTICE: dict[SourceKind, Practice] = {
    SourceKind.TEXTBOOK: Practice.IMAGINED,
    SourceKind.STUDY: Practice.REPORTED,
    SourceKind.STANDARD: Practice.IMAGINED,
    SourceKind.PROCEDURE_DOCUMENT: Practice.IMAGINED,
    SourceKind.DOCUMENTATION: Practice.IMAGINED,
    SourceKind.FORUM_POST: Practice.REPORTED,
    SourceKind.DESIGN_RECORD: Practice.IMAGINED,
    SourceKind.ISSUE: Practice.DONE,
    SourceKind.COMMIT: Practice.DONE,
    SourceKind.REVIEW_THREAD: Practice.DONE,
    SourceKind.LOG: Practice.DONE,
    SourceKind.INCIDENT_REPORT: Practice.REPORTED,
    SourceKind.LEARNER_RESPONSE: Practice.DONE,
    SourceKind.THINK_ALOUD: Practice.DONE,
    SourceKind.INTERVIEW: Practice.REPORTED,
    SourceKind.OBSERVATION: Practice.DONE,
    SourceKind.ELICITATION_RECORD: Practice.REPORTED,
}

QUOTABLE_KINDS = frozenset(PRACTICE) - {SourceKind.LEARNER_RESPONSE, SourceKind.LOG,
                                         SourceKind.OBSERVATION}
"""Prose kinds: supporting evidence from them must carry the exact quote a verifier checks."""
