from evaluation.dataset import DATASET

from app.detectors.prompt_injection import detect_prompt_injection
from app.detectors.semantic_detector import detect_semantic_injection


def get_scores(prompt):
    pattern_result = detect_prompt_injection(prompt)
    semantic_result = detect_semantic_injection(prompt)

    # Same risk aggregation used by KarmaPash
    risk_score = max(
        pattern_result["risk_score"],
        semantic_result["risk_score"],
    )

    return risk_score


def evaluate_threshold(scores, threshold):
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for item in scores:

        actual_attack = item["label"] == "attack"

        predicted_attack = item["risk_score"] >= threshold

        if actual_attack and predicted_attack:
            tp += 1

        elif not actual_attack and not predicted_attack:
            tn += 1

        elif not actual_attack and predicted_attack:
            fp += 1

        elif actual_attack and not predicted_attack:
            fn += 1

    precision = (
        tp / (tp + fp)
        if tp + fp
        else 0
    )

    recall = (
        tp / (tp + fn)
        if tp + fn
        else 0
    )

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
        "threshold": threshold,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": false_positive_rate,
    }


def run_threshold_analysis():

    print("\n===== Computing Risk Scores =====")

    scores = []

    for sample in DATASET:

        risk_score = get_scores(sample["prompt"])

        scores.append({
            "prompt": sample["prompt"],
            "label": sample["label"],
            "risk_score": risk_score,
        })

    thresholds = [
        0.30,
        0.35,
        0.40,
        0.45,
        0.50,
        0.55,
        0.60,
        0.65,
        0.70,
    ]

    print("\n===== Threshold Analysis =====")

    print(
        f"{'Threshold':<12}"
        f"{'Precision':<12}"
        f"{'Recall':<12}"
        f"{'F1':<12}"
        f"{'FPR':<12}"
    )

    print("-" * 58)

    results = []

    for threshold in thresholds:

        result = evaluate_threshold(
            scores,
            threshold,
        )

        results.append(result)

        print(
            f"{result['threshold']:<12.2f}"
            f"{result['precision']:<12.4f}"
            f"{result['recall']:<12.4f}"
            f"{result['f1']:<12.4f}"
            f"{result['false_positive_rate']:<12.4f}"
        )

    # Find the threshold with the highest F1
    best_result = max(
        results,
        key=lambda result: result["f1"]
    )

    print("\n===== BEST THRESHOLD BY F1 =====")

    print(
        f"Threshold: {best_result['threshold']:.2f}"
    )

    print(
        f"Precision: {best_result['precision']:.4f}"
    )

    print(
        f"Recall: {best_result['recall']:.4f}"
    )

    print(
        f"F1: {best_result['f1']:.4f}"
    )

    print(
        f"False Positive Rate: "
        f"{best_result['false_positive_rate']:.4f}"
    )

    print(
        f"TP: {best_result['TP']} | "
        f"TN: {best_result['TN']} | "
        f"FP: {best_result['FP']} | "
        f"FN: {best_result['FN']}"
    )


if __name__ == "__main__":
    run_threshold_analysis()