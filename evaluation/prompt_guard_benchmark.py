from evaluation.heldout_dataset import HELDOUT_DATASET
from app.detectors.prompt_guard import detect_prompt_guard


def main():
    tp = tn = fp = fn = 0

    print("=" * 70)
    print("PROMPT GUARD — FROZEN HELD-OUT BENCHMARK")
    print("=" * 70)

    for sample in HELDOUT_DATASET:
        prompt = sample["prompt"]
        expected_attack = sample["label"] == "attack"

        result = detect_prompt_guard(prompt)
        predicted_attack = result["detected"]

        if predicted_attack and expected_attack:
            tp += 1
        elif not predicted_attack and not expected_attack:
            tn += 1
        elif predicted_attack and not expected_attack:
            fp += 1
        elif not predicted_attack and expected_attack:
            fn += 1

        print(
            f"\n[{sample['category']}]"
            f"\nExpected: {'ATTACK' if expected_attack else 'BENIGN'}"
            f"\nPredicted: {'ATTACK' if predicted_attack else 'BENIGN'}"
            f"\nMalicious score: {result['malicious_score']:.4f}"
            f"\nPrompt: {prompt}"
        )

    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = (
        2 * precision * recall / (precision + recall)
        if (precision + recall)
        else 0
    )
    fpr = fp / (fp + tn) if (fp + tn) else 0

    print("\n" + "=" * 70)
    print("RESULTS")
    print("=" * 70)

    print(f"TP:        {tp}")
    print(f"TN:        {tn}")
    print(f"FP:        {fp}")
    print(f"FN:        {fn}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1:        {f1:.4f}")
    print(f"FPR:       {fpr:.4f}")
    print(f"Total:     {tp + tn + fp + fn}")


if __name__ == "__main__":
    main()