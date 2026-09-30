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
            yield json.load(handle)


def main():
    NORMALIZED_ROOT.mkdir(parents=True, exist_ok=True)
    for record in iterate_raw_records():
        response = record.get("response", {})
        violations = response.get("violations", []) if isinstance(response, dict) else []
        normalized = {
            "case_id": record.get("case_id"),
            "model": record.get("model"),
            "prompt": record.get("prompt"),
            "run": record.get("run"),
            "predicted_has_violation": bool(violations),
            "predicted_violations": [item.get("type") for item in violations if isinstance(item, dict) and "type" in item],
        }
        out_path = NORMALIZED_ROOT / f"{record.get('case_id')}.json"
        out_path.write_text(json.dumps(normalized, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Normalized {sum(1 for _ in iter(RAW_ROOT.rglob('*.json')))} raw result files.")


if __name__ == "__main__":
    main()
