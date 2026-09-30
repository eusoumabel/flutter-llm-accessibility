#!/usr/bin/env python3
"""Validate the experimental dataset against the repo's metadata contract."""

from __future__ import annotations

import re
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required. Install it with: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset"
SAMPLES_DIR = DATASET_DIR / "samples"
TAXONOMY_PATH = DATASET_DIR / "taxonomy.yaml"

VALID_ID_RE = re.compile(r"^(SEM|INT)_\d{3}$")
VALID_STATES = {"candidate", "annotated", "review_pending", "validated", "excluded", "frozen"}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def load_taxonomy():
    taxonomy = load_yaml(TAXONOMY_PATH)
    categories = taxonomy.get("categories", {})
    assert categories, "taxonomy.yaml is missing categories"
    return categories


def validate_metadata(metadata: dict, taxonomy: dict):
    required = [
        "schema_version",
        "id",
        "title",
        "category",
        "subcategory",
        "status",
        "source",
        "component",
        "files",
        "ground_truth",
        "references",
        "mutation",
        "validation",
        "created_at",
        "updated_at",
    ]

    missing = [key for key in required if key not in metadata]
    if missing:
        raise ValueError(f"Missing required metadata keys: {missing}")

    sample_id = metadata["id"]
    if not VALID_ID_RE.match(sample_id):
        raise ValueError(f"Invalid sample ID format: {sample_id}")

    category = metadata["category"]
    if category not in taxonomy:
        raise ValueError(f"Unknown category '{category}' for sample {sample_id}")

    subcategory = metadata["subcategory"]
    valid_subcategories = taxonomy[category]["violations"].keys()
    if subcategory and subcategory not in valid_subcategories:
        raise ValueError(
            f"Invalid subcategory '{subcategory}' for sample {sample_id} in category '{category}'"
        )

    if metadata["status"] not in VALID_STATES:
        raise ValueError(f"Invalid status '{metadata['status']}' for sample {sample_id}")

    files_block = metadata["files"]
    if "accessible" in files_block and "violation" in files_block:
        for variant_key in ("accessible", "violation"):
            file_name = files_block[variant_key]
            expected_path = SAMPLES_DIR / sample_id / file_name
            if not expected_path.exists():
                raise FileNotFoundError(f"Missing file for {sample_id}: {expected_path}")
    elif "component" in files_block:
        component_file = files_block["component"]
        component_path = SAMPLES_DIR / sample_id / component_file
        if not component_path.exists():
            raise FileNotFoundError(f"Missing component file for {sample_id}: {component_path}")
    else:
        raise ValueError(f"No recognized files block for sample {sample_id}")

    ground_truth = metadata["ground_truth"]
    if not isinstance(ground_truth, dict) or not ground_truth:
        raise ValueError(f"ground_truth is empty or invalid for {sample_id}")

    for variant_name, variant_data in ground_truth.items():
        if not isinstance(variant_data, dict):
            raise ValueError(f"Invalid variant payload for {sample_id}:{variant_name}")
        has_violation = variant_data.get("has_violation")
        violations = variant_data.get("violations", [])
        if not isinstance(violations, list):
            raise ValueError(f"violations must be a list for {sample_id}:{variant_name}")
        if bool(has_violation) and not violations:
            raise ValueError(f"Variant {sample_id}:{variant_name} says has_violation=true with empty violations")
        if not bool(has_violation) and violations:
            raise ValueError(f"Variant {sample_id}:{variant_name} says has_violation=false with violations")



def main():
    taxonomy = load_taxonomy()
    seen_ids = set()
    sample_files = sorted(SAMPLES_DIR.glob("*/metadata.yaml"))

    if not sample_files:
        raise SystemExit("No sample metadata files were found under dataset/samples/")

    for sample_file in sample_files:
        metadata = load_yaml(sample_file)
        sample_id = metadata.get("id")
        if sample_id in seen_ids:
            raise ValueError(f"Duplicate sample ID: {sample_id}")
        seen_ids.add(sample_id)
        validate_metadata(metadata, taxonomy)

    print(f"Validation passed for {len(sample_files)} sample metadata files.")


if __name__ == "__main__":
    main()
