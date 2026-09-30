#!/usr/bin/env python3
"""Compute a small set of confusion-matrix metrics for benchmark evaluation."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GROUND_TRUTH_PATH = ROOT / "dataset" / "ground_truth.jsonl"
NORMALIZED_DIR = ROOT / "results" / "normalized"


def load_ground_truth():
    truth = {}
    with GROUND_TRUTH_PATH.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            truth[row["sample_id"] + ":" + row["variant"]] = row
    return truth


def load_predictions():
    preds = {}
    for result_path in sorted(NORMALIZED_DIR.glob("*.json")):
        data = json.loads(result_path.read_text(encoding="utf-8"))
        case_id = data.get("case_id")
        if case_id:
            preds[case_id] = data
    return preds


def main():
    truth = load_ground_truth()
    preds = load_predictions()

    tp = fp = tn = fn = 0
    for key, row in truth.items():
        pred = preds.get(key.replace(":", "_"))
        predicted = bool(pred.get("predicted_has_violation")) if pred else False
        expected = bool(row.get("has_violation"))

        if expected and predicted:
            tp += 1
        elif expected and not predicted:
            fn += 1
        elif not expected and predicted:
            fp += 1
        else:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if (precision + recall) else 0.0

    print({
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
    })


if __name__ == "__main__":
    main()
