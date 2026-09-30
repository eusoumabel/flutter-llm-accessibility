#!/usr/bin/env python3
"""Generate dataset/ground_truth.jsonl from the canonical metadata files."""

from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install it with: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset"
SAMPLES_DIR = DATASET_DIR / "samples"
OUTPUT_PATH = DATASET_DIR / "ground_truth.jsonl"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def main():
    rows = []
    for metadata_path in sorted(SAMPLES_DIR.glob("*/metadata.yaml")):
        metadata = load_yaml(metadata_path)
        sample_id = metadata["id"]
        category = metadata["category"]
        for variant_name, variant_data in metadata.get("ground_truth", {}).items():
            violations = variant_data.get("violations", [])
            rows.append({
                "sample_id": sample_id,
                "variant": variant_name,
                "category": category,
                "has_violation": bool(variant_data.get("has_violation")),
                "violations": [item["type"] for item in violations if isinstance(item, dict) and "type" in item],
            })

    with OUTPUT_PATH.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False))
            handle.write("\n")

    print(f"Wrote {len(rows)} dataset ground-truth rows to {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()
