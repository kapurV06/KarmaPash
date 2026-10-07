import re


BEHAVIOR_PATTERNS = {
    # ---------------------------------------------------------
    # 1. Instruction override
    # ---------------------------------------------------------
    "instruction_override": [
        r"\bignore\b.{0,80}\b(previous|prior|earlier|original)\b",
        r"\bdisregard\b.{0,80}\b(previous|prior|earlier|original)\b",
        r"\bforget\b.{0,80}\b(previous|prior|earlier|original)\b",
        r"\bset aside\b.{0,80}\b(previous|prior|earlier|original|rules|constraints)\b",
        r"\breplace\b.{0,80}\b(original|previous|initial)\b.{0,40}\binstructions?\b",
        r"\bstop following\b.{0,80}\b(rules|instructions|guidelines)\b",
    ],

    # ---------------------------------------------------------
    # 2. Instruction hierarchy manipulation
    # ---------------------------------------------------------
    "instruction_hierarchy": [
        r"\bhigher[- ]priority\b",
        r"\bhigher priority instruction\b",
        r"\bhighest priority\b",
        r"\bhighest[- ]ranking\b",
        r"\badministrator override\b",
        r"\badministrator\b.{0,80}\boverrid(e|es|ing)\b",
        r"\bsystem[- ]level authorization\b",
        r"\bnew system (policy|instructions?)\b",
        r"\btreated as the new system\b",
        r"\bsupersedes?\b.{0,80}\b(instructions?|policy|rules)\b",
        r"\b(authoritative|authoritative instruction)\b",
        r"\bcontrolling policy\b",
    ],

    # ---------------------------------------------------------
    # 3. Restriction / constraint removal
    # ---------------------------------------------------------
    "restriction_removal": [
        r"\bunrestricted mode\b",
        r"\bunrestricted assistant\b",
        r"\bwithout (any )?(system )?instructions\b",
        r"\bwithout (any )?(system )?restrictions\b",
        r"\bno longer apply\b",
        r"\bconstraints? (are|is) (disabled|removed|suspended)\b",
        r"\b(previous|current|existing) constraints? (are|is) (disabled|removed|gone)\b",
        r"\bprevious constraints? no longer\b",
        r"\bdisabled\b.{0,40}\bsystem message\b",
        r"\bremove\b.{0,50}\b(constraints?|restrictions?|rules)\b",
        r"\bdisable\b.{0,50}\b(constraints?|restrictions?|rules)\b",
        r"\bno restrictions\b",
        r"\bwithout restrictions\b",
    ],

    # ---------------------------------------------------------
    # 4. Persona / operating-mode manipulation
    # ---------------------------------------------------------
    "mode_manipulation": [
        r"\benter\b.{0,40}\b(unrestricted|developer|override|admin|privileged)\b.{0,30}\bmode\b",
        r"\bswitch\b.{0,40}\b(to|into)\b.{0,40}\b(developer|override|admin|unrestricted)\b.{0,30}\bmode\b",
        r"\bactivate\b.{0,40}\b(unrestricted|developer|override|admin)\b.{0,30}\bmode\b",
        r"\bdeveloper override mode\b",
        r"\badmin mode\b",
        r"\bprivileged mode\b",
        r"\bfrom now on\b.{0,100}\b(original|current|existing)\b.{0,50}\b(rules?|instructions?|constraints?)\b",
        r"\bbehave as\b.{0,100}\bwithout\b.{0,50}\b(rules?|restrictions?|constraints?)\b",
        r"\bassume you are\b.{0,100}\bwithout\b.{0,50}\b(system|safety|security)\b",
        r"\bact as\b.{0,100}\bwithout\b.{0,50}\b(restrictions?|constraints?|rules?)\b",
    ],

    # ---------------------------------------------------------
    # 5. System / hidden instruction extraction
    # ---------------------------------------------------------
    "instruction_extraction": [
        r"\breveal\b.{0,80}\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b",
        r"\bshow\b.{0,80}\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b",
        r"\bprint\b.{0,80}\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b",
        r"\bprovide\b.{0,80}\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b",
        r"\boutput\b.{0,80}\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b",
        r"\bdisplay\b.{0,80}\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b",
        r"\bexact\b.{0,80}\b(instructions?|prompt)\b.{0,40}\binternally\b",
        r"\b(system|hidden|secret|private|confidential)\b.{0,40}\b(instructions?|prompt)\b.{0,80}\b(reveal|show|print|provide|display|output|reproduce)\b",
        r"\bconfidential\b.{0,40}\b(system|hidden|private)\b.{0,40}\b(instructions?|prompt)\b",
        r"\bprivate\b.{0,40}\b(system|hidden)\b.{0,40}\b(instructions?|prompt)\b",
    ],
}


def detect_behavioral_signals(prompt: str) -> dict:
    """
    Detect behavioral characteristics associated with
    prompt-injection attacks.

    The detector focuses on behavioral intent rather than
    requiring an exact attack phrase.

    Signals include:

    - instruction override
    - instruction hierarchy manipulation
    - restriction removal
    - operating-mode / persona manipulation
    - system-instruction extraction

    Multiple independent behavioral categories increase risk.
    """

    normalized_prompt = prompt.lower().strip()

    matched_categories = {}
    matched_patterns = []

    for category, patterns in BEHAVIOR_PATTERNS.items():

        category_matches = []

        for pattern in patterns:
            if re.search(pattern, normalized_prompt):
                category_matches.append(pattern)
                matched_patterns.append(pattern)

        if category_matches:
            matched_categories[category] = category_matches

    category_count = len(matched_categories)

    # ---------------------------------------------------------
    # Risk scoring
    # ---------------------------------------------------------
    if category_count == 0:
        risk_score = 0.0

    elif category_count == 1:
        risk_score = 0.55

    elif category_count == 2:
        risk_score = 0.75

    else:
        risk_score = 0.90

    return {
        "detected": category_count > 0,
        "matched_categories": list(matched_categories.keys()),
        "matched_patterns": matched_patterns,
        "risk_score": risk_score,
    }