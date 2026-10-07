from app.detectors.prompt_injection import detect_prompt_injection
from app.detectors.semantic_detector import detect_semantic_injection
from app.detectors.behavior_detector import detect_behavioral_signals
from app.policy.decision import make_decision


def analyze_prompt(prompt: str) -> dict:
    """
    Run a prompt through the complete KarmaPash security pipeline.

    Pipeline:

        Prompt
          ↓
        Pattern Detector
          ↓
        Semantic Detector
          ↓
        Behavioral Detector
          ↓
        Risk Aggregation
          ↓
        Policy Decision
    """

    # ---------------------------------------------------------
    # 1. Pattern detector
    # ---------------------------------------------------------

    pattern_result = detect_prompt_injection(prompt)

    # ---------------------------------------------------------
    # 2. Semantic detector
    # ---------------------------------------------------------

    semantic_result = detect_semantic_injection(prompt)

    # ---------------------------------------------------------
    # 3. Behavioral detector
    # ---------------------------------------------------------

    behavior_result = detect_behavioral_signals(prompt)

    # ---------------------------------------------------------
    # 4. Risk aggregation
    #
    # For now, use the strongest signal from any detector.
    # ---------------------------------------------------------

    risk_score = max(
        pattern_result["risk_score"],
        semantic_result["risk_score"],
        behavior_result["risk_score"],
    )

    # ---------------------------------------------------------
    # 5. Policy decision
    # ---------------------------------------------------------

    policy_result = make_decision(risk_score)

    # ---------------------------------------------------------
    # 6. Unified result
    # ---------------------------------------------------------

    return {
        "prompt": prompt,

        "detectors": {
            "pattern": pattern_result,
            "semantic": semantic_result,
            "behavior": behavior_result,
        },

        "risk_score": risk_score,

        "policy": policy_result,
    }