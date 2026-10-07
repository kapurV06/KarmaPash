import re


INJECTION_PATTERNS = [
    r"ignore (all |any )?previous instructions",
    r"ignore (all |any )?prior instructions",
    r"forget (all |any )?previous instructions",
    r"disregard (all |any )?previous instructions",
    r"reveal (your |the )?system prompt",
    r"show me (your |the )?system prompt",
    r"what is your system prompt",
]


def detect_prompt_injection(prompt: str) -> dict:
    """
    Detect obvious prompt injection attempts.

    Returns:
        {
            "detected": bool,
            "matched_patterns": list[str],
            "risk_score": float
        }
    """

    normalized_prompt = prompt.lower().strip()

    matches = []

    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, normalized_prompt):
            matches.append(pattern)

    if matches:
        return {
            "detected": True,
            "matched_patterns": matches,
            "risk_score": 0.9,
        }

    return {
        "detected": False,
        "matched_patterns": [],
        "risk_score": 0.0,
    }