#!/usr/bin/env python3
"""Compute confusion-matrix metrics for benchmark evaluation.

Predictions are joined to the ground truth by sample and variant. Results that are
not valid (provider error, refusal, invalid JSON or truncated output) are left out of
the confusion matrix and counted separately, as required by the analysis protocol.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUND_TRUTH_PATH = ROOT / "dataset" / "ground_truth.jsonl"
NORMALIZED_DIR = ROOT / "results" / "normalized"
METRICS_DIR = ROOT / "analysis" / "metrics"


def load_ground_truth():
    truth = {}
    with GROUND_TRUTH_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            truth[(row["sample_id"], row["variant"])] = row
    return truth


def load_predictions(experiment: str):
    for result_path in sorted((NORMALIZED_DIR / experiment).rglob("*.json")):
        data = json.loads(result_path.read_text(encoding="utf-8"))
        if data.get("sample_id") and data.get("variant"):
            yield data


def empty_counts():
    return {"tp": 0, "fp": 0, "tn": 0, "fn": 0, "invalid": 0, "unknown_case": 0}


def add_prediction(counts: dict, expected: bool | None, pred: dict):
    if expected is None:
        counts["unknown_case"] += 1
        return
    if not pred.get("valid"):
        counts["invalid"] += 1
        return
    predicted = bool(pred.get("predicted_has_violation"))
    if expected and predicted:
        counts["tp"] += 1
    elif expected and not predicted:
        counts["fn"] += 1
    elif not expected and predicted:
        counts["fp"] += 1
    else:
        counts["tn"] += 1


def with_scores(counts: dict) -> dict:
    tp, fp, fn = counts["tp"], counts["fp"], counts["fn"]
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0
    return {**counts, "precision": precision, "recall": recall, "f1": f1}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=("pilot", "final"), default="final")
    args = parser.parse_args()

    truth = load_ground_truth()
    overall = defaultdict(empty_counts)
    by_category = defaultdict(empty_counts)

    for pred in load_predictions(args.experiment):
        row = truth.get((pred["sample_id"], pred["variant"]))
        expected = bool(row["has_violation"]) if row else None
        group = (pred.get("model"), pred.get("prompt"))
        add_prediction(overall[group], expected, pred)
        if row:
            add_prediction(by_category[group + (row["category"],)], expected, pred)

    report = {
        "experiment": args.experiment,
        "by_model_prompt": [
            {"model": model, "prompt": prompt, **with_scores(counts)}
            for (model, prompt), counts in sorted(overall.items())
        ],
        "by_model_prompt_category": [
            {"model": model, "prompt": prompt, "category": category, **with_scores(counts)}
            for (model, prompt, category), counts in sorted(by_category.items())
        ],
    }

    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = METRICS_DIR / f"metrics_{args.experiment}.json"
    out_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["by_model_prompt"], ensure_ascii=False, indent=2))
    print(f"Metrics written to {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
