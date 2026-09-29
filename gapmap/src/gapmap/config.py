"""Every lexicon, threshold and cap the pipeline uses (spec §0, §2.7, §5, §6). Canonical JSON of
this module's fixed values is hashed into every output (`CONFIG_SHA256`); changing any of it is
a re-freeze, per the spec's in-sample warning (§0)."""
from __future__ import annotations

import hashlib
import json
import re

STOP = frozenset("""
a an the and or but if then else when while of in on at to for from by with without into onto
over under about as is are was were be been being this that these those it its it's their there
they them we you your our can could may might must should shall will would do does did done not
no nor any all each every some such more most less least other than also only very just both
either neither which who whom whose what where why how per via using use used uses make makes
made one two three first new e.g i.e etc within between before after during across through
because since so up out off down whether common commonly typically typical often usually among
issue issues most many several various
""".split())

_LEXICONS: dict[str, str] = {
    "MODAL": r"\b(must|should|shall|required?|need(?:s)? to|mandatory|necessary to)\b",
    "JUDGE": r"\b(appropriate|adequate|sufficient(?:ly)?|reasonable|significant(?:ly)?|large[- ]scale|"
             r"high[- ]risk|systematic(?:ally)?|relevant|suitable|proper(?:ly)?|excessive|abnormal|"
             r"unusual|normal|acceptable|minor|serious|severe|substantial|stable|loose|marginal|poor|"
             r"vulnerable|extensive|innovative|sensitive|expected|baseline)\b",
    "QUANT": r"\b(?:more than|less than|fewer than|at least|at most|over|under|above|below|between|"
             r"up to|exceed\w*|within)\s+\d"
             r"|\d+(?:\.\d+)?\s?(?:%|percent|vdc|vac|v|ms|s|seconds?|minutes?|hours?|days?|weeks?|months?|"
             r"years?|ohms?|mm|hz|khz|mhz|ma|a)\b",
    "CASE": r"\b(whereas|rather than|unlike|versus|vs\.?|as opposed to|but not|not (?:a|an|on|be)\b)",
    "DEFN": r"\b(means|defined as|refers? to|covers|is when|occurs when|consider\w*|factors?|criteria|"
            r"criterion|includ\w+|such as|for example|e\.g\.|examples?|concerns?)\b",
    "CAUSE": r"\b(caus(?:e|ed|es)|due to|result(?:s|ing)? (?:from|in)|lead(?:s)? to|stem(?:s)? from|"
             r"produce[sd]?|traceable to|relate[sd]? to|source of|create[sd]?)\b",
    "DISCR": r"\b(indicat\w*|signs?\b|distinguish\w*|rather than|whereas|correlat\w*|only after|"
             r"appear\w* only|symptom\w*|characteristic|signature|points? to|pattern)\b",
    "SEL": r"\b(based on|according to|depending on|most likely|most probable|prioriti[sz]\w*|choos\w*|"
           r"chosen|select\w*|decid\w*|determin\w* (?:which|whether))\b",
    "COND": r"\b(if|when|whenever|for (?:a|an)\b.*\buse)\b|\b(?:more|less) likely\b[^.;]{0,40}\bthan\b",
    "HEDGE": r"\b(in most cases|generally|typically|usually|normally|in general|as a rule|"
             r"not (?:a|an) (?:strict|absolute|hard) rule|where appropriate|where necessary|if necessary|"
             r"as needed|case[- ]by[- ]case|in (?:some|certain) cases|depend(?:s|ing)? on)\b",
    "EXC": r"\b(unless|except\w*\b(?![^.;]{0,25}\b(?:article|art\.|section|recital)\b)|"
           r"only (?:if|when|where)|does not apply|do not apply|not required|exempt\w*|"
           r"even (?:if|when)|provided that|as long as)\b",
    "ERR": r"\b(mistake\w*|pitfall\w*|overlook\w*|false (?:positive|negative|reading|result|state)\w*|"
           r"wrongly|mistaken\w*|tempting|common error\w*|misinterpret\w*|misread\w*)\b",
    "DETECT": r"\b(check\w*|verif\w*|confirm\w*|notic\w*|detect\w*|recogni\w*|tell\w*|warning sign\w*|"
              r"indicat\w*)\b",
    "RAT": r",\s*as\s|\bwill (?:destroy|damage|kill|overwrite|lose|corrupt|cause)\b|"
           r"\b(because|since|so that|in order to|to ensure|to avoid|to prevent|prevent\w*|otherwise|"
           r"reason|why|as this|this (?:helps|allows|ensures)|to (?:preserve|protect|reduce|keep|save|stop))\b",
    "AUTH": r"\b(article|regulation|gdpr|law|legal\w*|statut\w*|directive|act|authorit\w*|supervisory|"
            r"dpa|ico|regulator\w*|edpb|wp29|guideline\w*)\b",
    "TEST": r"\b(measur\w*|check\w*|test\w*|inspect\w*|verif\w*|monitor\w*|observ\w*|compar\w*|captur\w*|"
            r"trend\w*|assess\w*|evaluat\w*|review\w*)\b",
    "INTERP": r"\b(indicat\w*|means|suggest\w*|points? to|impl(?:y|ies)|reveal\w*|shows? that|confirm\w*|"
              r"rules? out|should (?:read|be|show)|expected|normal(?:ly)?|typical(?:ly)?|reading of|then)\b",
    "PROMO": r"\b(our|we offer|request a demo|book a demo|pricing|platform|solution|appliance|hub|"
             r"dashboard|live data|no cloud|we replaced|with \w+ we|our (?:customers|team)|"
             r"the agent (?:selects|decides)|ai agent)\b|™|®",
    "GUARD_AGENT": r"\b(technician|engineer|operator|practitioner|troubleshoot\w*|you|people|staff|team|"
                   r"someone|organi[sz]ation\w*|controller\w*|mistake)\b",
    "WHY_DISJUNCTION": r"require(?:s)? or (?:do|does) not require",
}
_LEXICONS["CONTRA"] = (r"\b(not|never|avoid\w*|instead|rather than|only|before|first)\b|"
                       + _LEXICONS["QUANT"])

PATTERNS: dict[str, re.Pattern[str]] = {k: re.compile(v, re.IGNORECASE) for k, v in _LEXICONS.items()}

FIXED_ANCHORS = ("high risk", "large scale")
TERMHOOD_MIN_CLAIMS = 2
"""§2.1: an anchor needs at least this many distinct A claims, else it is dropped."""

COMMON_STEM_CUTS = (0.05, 0.08)
SHARED_STEM_THRESHOLDS = (2, 3)
DEFAULT_COMMON_STEM_CUT = COMMON_STEM_CUTS[0]
DEFAULT_SHARED_STEM_THRESHOLD = SHARED_STEM_THRESHOLDS[0]

MERGE_JACCARD = 0.5
"""§6: records of the same lens and category merge above this X-Jaccard."""
ROBUSTNESS_JACCARD = 0.5
"""§1.4: a robustness setting reproduces a record at this X-Jaccard (or the same DISC anchor)."""
SIBLING_JACCARD = 0.3
"""§7.2: seed-stem Jaccard for cross-run matching outside DISC (which matches by term/head)."""

MAP_TOP_N = 12
MAP_PER_LENS = 3
MAP_PER_AREA = 4

INSTITUTIONAL_INDETERMINACY_SHARE = 0.5
"""§2.1 DISC alternative: live when at least this share of anchor claims are norm or concept."""

DIAG_CAUSE_JACCARD_MAX = 0.5
"""F6: DIAG rivals need 0 shared non-common cause stems AND a full cause-stem Jaccard below this."""

PROMO_PENALTY = 1
"""F6: score penalty when the PROMO lexicon is live on a WHY/GUARD candidate's span."""

BREADTH_BROAD_K_TOPIC_MIN = 5
BREADTH_BROAD_K_STEP_MIN = 2
"""F3: `breadth == "broad"` iff k_topic >= this and k_step >= this many independent keys."""
BREADTH_MODERATE_SCORE_MIN = 3
"""F3: below `broad`, `breadth == "moderate"` iff the A+B-P(-Q) score is at least this."""

CLOSURE_NULL_DRAWS = 200
"""F2/S2: donor-null draws, `random.Random(0)`-seeded."""

PROMO_DOMAINS = frozenset({"plclogs.com", "capafy.ai", "peakboard.com", "csintegrators.com"})
"""S3 defect 1: PLC's promotional sources named by the second adversarial review -- a PlcLogs
testimonial ("We replaced three separate monitoring tools with PlcLogs..."), and vendor product
copy (capafy.ai, peakboard.com, csintegrators.com's "Edge" appliance). A seed sourced from one of
these, or whose span matches PROMO, does not fire, for any lens."""

DISC_STOP_ANCHORS = frozenset({"appropriate time", "sensitive control"})
"""S3 defect 5: anchors that are not discriminations on inspection (in-sample; see Implementation
notes) -- "appropriate time" is a temporal frame, not a contrasted category, and "sensitive
control" is a generic adjective+generic-noun pairing with no stated boundary to recover."""

IRREGULAR_STEMS = {"failure": "fail", "failures": "fail"}
"""S3 defect 4: the suffix-stripping stemmer (§1.3) does not fold "failure" to "fail" (no listed
suffix matches "-ure"), so a claim's "fail" and a corroborating span's "failure" (or vice versa)
would not share a stem and could break closure overlap. Only this pair is folded, not a general
"-ure" rule, to avoid conflating unrelated words (e.g. "pressure" -> "press")."""

JUDGE_MODEL = "qwen2.5:7b-instruct"
JUDGE_URL = "http://localhost:11434/api/chat"
JUDGE_A_CAP = 8
JUDGE_S_CAP = 4
"""S1: retrieval per candidate takes the top 8 A and top 4 S sentences scored >= 1 (plus the
seed's own span sentences, unconditionally)."""


def _canonical() -> dict:
    return {
        "stop": sorted(STOP),
        "lexicons": _LEXICONS,
        "fixed_anchors": list(FIXED_ANCHORS),
        "termhood_min_claims": TERMHOOD_MIN_CLAIMS,
        "common_stem_cuts": list(COMMON_STEM_CUTS),
        "shared_stem_thresholds": list(SHARED_STEM_THRESHOLDS),
        "merge_jaccard": MERGE_JACCARD,
        "robustness_jaccard": ROBUSTNESS_JACCARD,
        "sibling_jaccard": SIBLING_JACCARD,
        "map_top_n": MAP_TOP_N,
        "map_per_lens": MAP_PER_LENS,
        "map_per_area": MAP_PER_AREA,
        "institutional_indeterminacy_share": INSTITUTIONAL_INDETERMINACY_SHARE,
        "diag_cause_jaccard_max": DIAG_CAUSE_JACCARD_MAX,
        "promo_penalty": PROMO_PENALTY,
        "breadth_broad_k_topic_min": BREADTH_BROAD_K_TOPIC_MIN,
        "breadth_broad_k_step_min": BREADTH_BROAD_K_STEP_MIN,
        "breadth_moderate_score_min": BREADTH_MODERATE_SCORE_MIN,
        "closure_null_draws": CLOSURE_NULL_DRAWS,
        "promo_domains": sorted(PROMO_DOMAINS),
        "disc_stop_anchors": sorted(DISC_STOP_ANCHORS),
        "irregular_stems": IRREGULAR_STEMS,
        "judge_model": JUDGE_MODEL,
        "judge_url": JUDGE_URL,
        "judge_a_cap": JUDGE_A_CAP,
        "judge_s_cap": JUDGE_S_CAP,
    }


CONFIG_SHA256 = hashlib.sha256(json.dumps(_canonical(), sort_keys=True).encode()).hexdigest()
