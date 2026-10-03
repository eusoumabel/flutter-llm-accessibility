#!/usr/bin/env python3
"""Validate the experimental dataset against the repo's metadata contract."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = ROOT / "dataset"
SAMPLES_DIR = DATASET_DIR / "samples"
TAXONOMY_PATH = DATASET_DIR / "taxonomy.json"

VALID_ID_RE = re.compile(r"^(SEM|INT)_\d{3}$")
VALID_STATES = {"candidate", "annotated", "review_pending", "validated", "excluded", "frozen"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_taxonomy():
    taxonomy = load_json(TAXONOMY_PATH)
    categories = taxonomy.get("categories", {})
    assert categories, "taxonomy.json is missing categories"
    return categories


def build_taxonomy_indexes(taxonomy: dict):
    violations_by_code = {}
    mutation_ids = set()
    for category_name, category_data in taxonomy.items():
        for subcategory_name, violation in category_data.get("violations", {}).items():
            violations_by_code[violation["code"]] = (category_name, subcategory_name)
            mutation_ids.update(
                mutation["id"] for mutation in violation.get("possible_mutations", [])
            )
    return violations_by_code, mutation_ids


def validate_metadata(metadata: dict, taxonomy: dict, violations_by_code: dict, mutation_ids: set):
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
        "mutations",
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

    file_keys = set(files_block)
    ground_truth_keys = set(ground_truth)
    if ground_truth_keys != file_keys:
        raise ValueError(
            f"files and ground_truth variants do not match for {sample_id}: "
            f"files={sorted(file_keys)}, ground_truth={sorted(ground_truth_keys)}"
        )

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

        for violation in violations:
            violation_id = violation.get("id") if isinstance(violation, dict) else None
            violation_type = violation.get("type") if isinstance(violation, dict) else None
            if violation_id not in violations_by_code:
                raise ValueError(f"Unknown violation code '{violation_id}' for {sample_id}:{variant_name}")
            _, expected_type = violations_by_code[violation_id]
            if violation_type != expected_type:
                raise ValueError(
                    f"Violation type '{violation_type}' does not match code '{violation_id}' "
                    f"for {sample_id}:{variant_name}"
                )

    mutations = metadata["mutations"]
    if not isinstance(mutations, list):
        raise ValueError(f"mutations must be a list for {sample_id}")
    for mutation in mutations:
        if not isinstance(mutation, dict) or not mutation.get("id"):
            raise ValueError(f"Invalid mutation entry for {sample_id}")
        if mutation["id"] not in mutation_ids:
            raise ValueError(
                f"Mutation '{mutation['id']}' is not declared as possible in taxonomy.json "
                f"for {sample_id}"
            )
        target_variants = mutation.get("target_variants", [])
        if not isinstance(target_variants, list) or not set(target_variants).issubset(ground_truth_keys):
            raise ValueError(f"Invalid target_variants for mutation '{mutation['id']}' in {sample_id}")



def main():
    taxonomy = load_taxonomy()
    violations_by_code, mutation_ids = build_taxonomy_indexes(taxonomy)
    seen_ids = set()
    sample_files = sorted(SAMPLES_DIR.glob("*/metadata.json"))

    if not sample_files:
        raise SystemExit("No sample metadata files were found under dataset/samples/")

    for sample_file in sample_files:
        metadata = load_json(sample_file)
        sample_id = metadata.get("id")
        if sample_id in seen_ids:
            raise ValueError(f"Duplicate sample ID: {sample_id}")
        seen_ids.add(sample_id)
        validate_metadata(metadata, taxonomy, violations_by_code, mutation_ids)

    print(f"Validation passed for {len(sample_files)} sample metadata files.")


if __name__ == "__main__":
    main()
