def make_decision(risk_score: float) -> dict:

    if risk_score < 0.30:
        decision = "ALLOW"

    elif risk_score < 0.45:
        decision = "FLAG"

    else:
        decision = "BLOCK"

    return {
        "decision": decision,
        "risk_score": risk_score,
    }