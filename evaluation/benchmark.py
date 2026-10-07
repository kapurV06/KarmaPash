from evaluation.dataset import DATASET

from app.pipeline import analyze_prompt


def classify_prediction(prompt: str) -> dict:
    """
    Run a prompt through the exact same security pipeline
    used by the KarmaPash API.
    """

    result = analyze_prompt(prompt)

    return {
        "decision": result["policy"]["decision"],
        "risk_score": result["risk_score"],
        "pattern_score": result["detectors"]["pattern"]["risk_score"],
        "semantic_score": result["detectors"]["semantic"]["risk_score"],
        "behavior_score": result["detectors"]["behavior"]["risk_score"],
    }


def calculate_metrics(results):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for result in results:
        actual_attack = result["actual_attack"]
        predicted_attack = result["predicted_attack"]

        if actual_attack and predicted_attack:
            tp += 1

        elif not actual_attack and not predicted_attack:
            tn += 1

        elif not actual_attack and predicted_attack:
            fp += 1

        elif actual_attack and not predicted_attack:
            fn += 1

    precision = tp / (tp + fp) if tp + fp else 0

    recall = tp / (tp + fn) if tp + fn else 0

    f1 = (
        2 * precision * recall / (precision + recall)
        if precision + recall
        else 0
    )

    false_positive_rate = (
        fp / (fp + tn)
        if fp + tn
        else 0
    )

    return {
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": false_positive_rate,
        "total": len(results),
    }


def run_benchmark():
    results = []

    for sample in DATASET:
        prediction = classify_prediction(sample["prompt"])

        actual_attack = sample["label"] == "attack"

        predicted_attack = (
            prediction["decision"] == "BLOCK"
        )

        results.append({
            "prompt": sample["prompt"],
            "category": sample["category"],
            "actual_attack": actual_attack,
            "predicted_attack": predicted_attack,
            "decision": prediction["decision"],
            "risk_score": prediction["risk_score"],
            "pattern_score": prediction["pattern_score"],
            "semantic_score": prediction["semantic_score"],
            "behavior_score": prediction["behavior_score"],
        })

    metrics = calculate_metrics(results)

    print("\n===== KarmaPash Benchmark =====")

    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")

    print("\n===== ALL SAMPLES =====")

    for result in results:
        label = (
            "ATTACK"
            if result["actual_attack"]
            else "BENIGN"
        )

        print(
            f"\n[{label}] "
            f"category={result['category']} "
            f"semantic={result['semantic_score']:.4f} "
            f"behavior={result['behavior_score']:.4f} "
            f"pattern={result['pattern_score']:.4f} "
            f"risk={result['risk_score']:.4f} "
            f"decision={result['decision']}"
        )

        print(f"Prompt: {result['prompt']}")


if __name__ == "__main__":
    run_benchmark()