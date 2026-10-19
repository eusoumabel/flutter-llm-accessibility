#!/usr/bin/env python3
"""Normalize raw experiment output into a reproducible analysis-ready schema."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT = ROOT / "results" / "raw"
NORMALIZED_ROOT = ROOT / "results" / "normalized"


def iterate_raw_records():
    for raw_file in sorted(RAW_ROOT.rglob("*.json")):
        with raw_file.open("r", encoding="utf-8") as handle:
            yield raw_file, json.load(handle)


def main():
    count = 0
    for raw_file, record in iterate_raw_records():
        response = record.get("response", {})
        violations = response.get("violations", []) if isinstance(response, dict) else []
        violations = [item for item in violations if isinstance(item, dict)]
        status = record.get("status", "ok")
        request = record.get("request", {})
        normalized = {
            "experiment_id": record.get("experiment_id"),
            "case_id": record.get("case_id"),
            "sample_id": request.get("sample_id"),
            "variant": request.get("variant"),
            "category": request.get("category"),
            "provider": record.get("provider"),
            "model": record.get("model"),
            "prompt": record.get("prompt"),
            "run": record.get("run"),
            "status": status,
            "valid": status == "ok",
            "predicted_has_violation": bool(violations),
            "predicted_violations": [item.get("type") for item in violations if "type" in item],
            "predicted_confidences": [item.get("confidence") for item in violations if "confidence" in item],
        }
        out_path = NORMALIZED_ROOT / raw_file.relative_to(RAW_ROOT)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")
        count += 1

    print(f"Normalized {count} raw result files.")


if __name__ == "__main__":
    main()
