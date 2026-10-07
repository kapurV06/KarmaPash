import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


MODEL_NAME = "project-free-llama/Llama-Prompt-Guard-2-86M"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

model.eval()


def detect_prompt_guard(prompt: str) -> dict:
    """
    Run Meta Llama Prompt Guard 2 on a prompt.

    Returns:
        label: benign / malicious
        malicious_score: probability assigned to malicious class
        detected: whether Prompt Guard considers the prompt malicious
    """

    inputs = tokenizer(
        prompt,
        return_tensors="pt",
        truncation=True,
        max_length=512,
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    probabilities = torch.softmax(logits, dim=-1)[0]

    id2label = model.config.id2label

    scores = {
        id2label[i].lower(): float(probabilities[i])
        for i in range(len(probabilities))
    }

    malicious_score = scores["label_1"]

    return {
        "label": "malicious" if malicious_score >= 0.5 else "benign",
        "malicious_score": malicious_score,
        "detected": bool(malicious_score >= 0.5),
    }