from collections import defaultdict

from evaluation.heldout_dataset import HELDOUT_DATASET
from app.pipeline import analyze_prompt


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


def calculate_category_metrics(results):
    categories = defaultdict(list)

    for result in results:
        categories[result["category"]].append(result)

    category_metrics = {}

    for category, category_results in categories.items():
        category_metrics[category] = calculate_metrics(
            category_results
        )

    return category_metrics


def run_heldout_benchmark():
    results = []

    for sample in HELDOUT_DATASET:

        analysis = analyze_prompt(sample["prompt"])

        decision = analysis["policy"]["decision"]

        actual_attack = sample["label"] == "attack"

        predicted_attack = decision == "BLOCK"

        results.append({
            "prompt": sample["prompt"],
            "category": sample["category"],
            "actual_attack": actual_attack,
            "predicted_attack": predicted_attack,
            "decision": decision,
            "risk_score": analysis["risk_score"],
            "pattern_score": (
                analysis["detectors"]["pattern"]["risk_score"]
            ),
            "semantic_score": (
                analysis["detectors"]["semantic"]["risk_score"]
            ),
            "behavior_score": (
                analysis["detectors"]["behavior"]["risk_score"]
            ),
        })

    metrics = calculate_metrics(results)

    print("\n========================================")
    print("KarmaPash Held-Out Benchmark")
    print("========================================")

    for key, value in metrics.items():

        if isinstance(value, float):
            print(f"{key}: {value:.4f}")

        else:
            print(f"{key}: {value}")

    print("\n========================================")
    print("Metrics By Category")
    print("========================================")

    category_metrics = calculate_category_metrics(results)

    for category, category_result in category_metrics.items():

        print(f"\n[{category}]")

        print(
            f"TP={category_result['TP']} "
            f"TN={category_result['TN']} "
            f"FP={category_result['FP']} "
            f"FN={category_result['FN']}"
        )

        print(
            f"Precision={category_result['precision']:.4f} "
            f"Recall={category_result['recall']:.4f} "
            f"F1={category_result['f1']:.4f}"
        )

    print("\n========================================")
    print("Misclassified Samples")
    print("========================================")

    errors = [
        result
        for result in results
        if result["actual_attack"] != result["predicted_attack"]
    ]

    if not errors:
        print("No misclassified samples.")

    else:
        for result in errors:

            label = (
                "ATTACK"
                if result["actual_attack"]
                else "BENIGN"
            )

            print(
                f"\n[{label}] "
                f"category={result['category']}"
            )

            print(
                f"semantic={result['semantic_score']:.4f} "
                f"behavior={result['behavior_score']:.4f} "
                f"risk={result['risk_score']:.4f} "
                f"decision={result['decision']}"
            )

            print(
                f"Prompt: {result['prompt']}"
            )


if __name__ == "__main__":
    run_heldout_benchmark()