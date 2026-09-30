#!/usr/bin/env python3
"""Generate a CSV summary of the dataset for human inspection."""

from __future__ import annotations

import csv
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install it with: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset"
SAMPLES_DIR = DATASET_DIR / "samples"
OUTPUT_PATH = DATASET_DIR / "dataset.csv"

FIELDS = [
    "sample_id",
    "variant",
    "category",
    "subcategory",
    "has_violation",
    "source_type",
    "mutation",
    "validation_status",
    "wcag",
    "flutter_guideline",
]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main():
    rows = []
    for metadata_path in sorted(SAMPLES_DIR.glob("*/metadata.yaml")):
        metadata = load_yaml(metadata_path)
        sample_id = metadata["id"]
        category = metadata["category"]
        source_type = metadata.get("source", {}).get("type", "")
        mutation = bool(metadata.get("mutation", {}).get("applied", False))
        validation_status = metadata.get("status", "")
        for variant_name, variant_data in metadata.get("ground_truth", {}).items():
            rows.append({
                "sample_id": sample_id,
                "variant": variant_name,
                "category": category,
                "subcategory": metadata.get("subcategory", ""),
                "has_violation": str(bool(variant_data.get("has_violation"))).lower(),
                "source_type": source_type,
                "mutation": str(mutation).lower(),
                "validation_status": validation_status,
                "wcag": "",
                "flutter_guideline": "",
            })

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} rows to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
