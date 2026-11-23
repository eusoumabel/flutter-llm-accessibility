#!/usr/bin/env python3
"""Compare rounds with the same set of measures (ADR-R023).

For each round, model and prompt the script reports:

- conformity: valid responses, items per response, responses with at most one item;
- binary detection (RQ1): the same confusion matrix as calculate_metrics.py;
- principal violation (RQ1): among detections, whether the principal subcategory of the
  ground truth (``subcategory`` in the sample metadata, ADR-R005) is among the mapped
  predicted types (any position) or is the first one, and whether the category matches;
- noise: items in variants without violation, out-of-scope and generic items, and items
  still unmapped in analysis/type_mapping/type_mapping.csv;
- severity (prompts v2): distribution and, when the type maps to one subcategory,
  agreement with the taxonomy severity;
- cost: tokens and latency from the raw responses.

It also writes the outcome of every variant in every round (TP, FP, TN, FN, INV) so the
changes between rounds can be read variant by variant. RQ2 is reported as the P1 - P0
difference within each round.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

from build_pilot_review import load_samples
from calculate_metrics import add_prediction, empty_counts, load_ground_truth, load_predictions, with_scores
from map_types import MAPPING_PATH, TAXONOMY_PATH

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "results" / "raw"
TABLES_DIR = ROOT / "analysis" / "tables"
SEVERITIES = ("critical", "high", "medium", "low")


def load_taxonomy() -> tuple[dict, dict]:
    """Return {taxonomy key: code} and {code: severity}."""
    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    codes, severities = {}, {}
    for category in taxonomy["categories"].values():
        for key, item in category["violations"].items():
            codes[key] = item["code"]
            severities[item["code"]] = item.get("severity", "")
    return codes, severities


def load_mapping() -> dict:
    if not MAPPING_PATH.exists():
        raise SystemExit(f"Run scripts/map_types.py first: {MAPPING_PATH.relative_to(ROOT)} not found")
    with MAPPING_PATH.open("r", encoding="utf-8", newline="") as handle:
        return {(row["round"], row["model"], row["prompt"], row["raw_type"]): row for row in csv.DictReader(handle)}


def raw_record(pred: dict, round_name: str) -> dict:
    path = RAW_DIR / round_name / pred["model"] / pred["prompt"] / f"{pred['case_id']}" / f"run_{int(pred['run']):02d}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}


def outcome(expected: bool, pred: dict) -> str:
    if not pred.get("valid"):
        return "INV"
    predicted = bool(pred.get("predicted_has_violation"))
    return {(True, True): "TP", (True, False): "FN", (False, True): "FP", (False, False): "TN"}[(expected, predicted)]


def ratio(part: float, whole: float) -> float | None:
    return round(part / whole, 3) if whole else None


def summarize_round(round_name: str, truth: dict, principal: dict, mapping: dict, severity_of: dict):
    groups = defaultdict(lambda: {
        "counts": empty_counts(), "responses": 0, "items": 0, "single": 0, "detections": 0,
        "hit_any": 0, "hit_first": 0, "category_hit": 0, "items_in_correct": 0, "out_of_scope": 0,
        "generic": 0, "unmapped": 0, "severity": defaultdict(int), "severity_checked": 0,
        "severity_agree": 0, "tokens": 0, "latency_ms": 0,
    })
    outcomes = {}
    for pred in load_predictions(round_name):
        key = (pred["sample_id"], pred["variant"])
        row = truth.get(key)
        group = groups[(pred.get("model"), pred.get("prompt"))]
        expected = bool(row["has_violation"]) if row else None
        add_prediction(group["counts"], expected, pred)
        group["responses"] += 1
        if expected is None:
            continue
        outcomes[(pred["model"], pred["prompt"]) + key] = outcome(expected, pred)
        if not pred.get("valid"):
            continue

        types = pred.get("predicted_violations", [])
        group["items"] += len(types)
        group["single"] += len(types) <= 1
        mapped = [mapping.get((round_name, pred["model"], pred["prompt"], t), {}) for t in types]
        for entry in mapped:
            method = entry.get("method", "")
            group["out_of_scope"] += method == "out_of_scope"
            group["generic"] += method == "generic"
            group["unmapped"] += method in ("", "auto_multi")
        if not expected:
            group["items_in_correct"] += len(types)
        elif types:
            group["detections"] += 1
            code_sets = [set(filter(None, entry.get("subcategory", "").split("|"))) for entry in mapped]
            target = principal[key]
            group["hit_any"] += any(target in codes for codes in code_sets)
            group["hit_first"] += target in code_sets[0]
            group["category_hit"] += any(entry.get("category") == row["category"] for entry in mapped)

        for raw_type, sev in zip(types, pred.get("predicted_severities", [])):
            group["severity"][sev] += 1
            codes = mapping.get((round_name, pred["model"], pred["prompt"], raw_type), {}).get("subcategory", "")
            if codes and "|" not in codes:
                group["severity_checked"] += 1
                group["severity_agree"] += severity_of.get(codes) == sev

        raw = raw_record(pred, round_name)
        group["tokens"] += raw.get("usage", {}).get("total_tokens", 0) or 0
        group["latency_ms"] += raw.get("latency_ms", 0) or 0

    rows = []
    for (model, prompt), g in sorted(groups.items()):
        scores = with_scores(g["counts"])
        valid = g["responses"] - scores["invalid"]
        rows.append({
            "round": round_name, "model": model, "prompt": prompt,
            "responses": g["responses"], "valid": valid,
            "items": g["items"], "items_per_response": ratio(g["items"], valid),
            "single_item_rate": ratio(g["single"], valid),
            "tp": scores["tp"], "fp": scores["fp"], "tn": scores["tn"], "fn": scores["fn"],
            "recall": round(scores["recall"], 3), "precision": round(scores["precision"], 3),
            "f1": round(scores["f1"], 3), "fp_rate_correct_code": ratio(scores["fp"], scores["fp"] + scores["tn"]),
            "detections": g["detections"],
            "principal_hit_any": ratio(g["hit_any"], g["detections"]),
            "principal_hit_first": ratio(g["hit_first"], g["detections"]),
            "category_hit": ratio(g["category_hit"], g["detections"]),
            "items_in_correct_code": g["items_in_correct"],
            "out_of_scope_items": g["out_of_scope"], "generic_items": g["generic"],
            "unmapped_items": g["unmapped"],
            **{f"severity_{s}": g["severity"].get(s, 0) for s in SEVERITIES},
            "severity_agreement": ratio(g["severity_agree"], g["severity_checked"]),
            "tokens_total": g["tokens"], "latency_ms_mean": ratio(g["latency_ms"], g["responses"]),
        })
    return rows, outcomes


def fmt(value) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value)


def markdown(rows: list[dict], rounds: list[str]) -> str:
    columns = [
        ("Rodada", "round"), ("Modelo", "model"), ("Prompt", "prompt"),
        ("Itens/resp.", "items_per_response"), ("Revocação", "recall"), ("Precisão", "precision"),
        ("F1", "f1"), ("FP em código correto", "fp_rate_correct_code"),
        ("Principal (qualquer)", "principal_hit_any"), ("Principal (1º)", "principal_hit_first"),
        ("Categoria", "category_hit"), ("Fora do escopo", "out_of_scope_items"), ("Sem mapear", "unmapped_items"),
    ]
    lines = ["# Comparação entre rodadas", "",
             "| " + " | ".join(title for title, _ in columns) + " |",
             "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(fmt(row[key]) for _, key in columns) + " |")

    lines += ["", "## RQ2: diferença P1 − P0 dentro de cada rodada", "",
              "| Rodada | Modelo | Revocação | Precisão | FP em código correto | Principal (1º) |",
              "| --- | --- | --- | --- | --- | --- |"]
    index = {(r["round"], r["model"], r["prompt"]): r for r in rows}
    for round_name in rounds:
        for model in sorted({r["model"] for r in rows if r["round"] == round_name}):
            p0, p1 = index.get((round_name, model, "P0")), index.get((round_name, model, "P1"))
            if not (p0 and p1):
                continue
            deltas = []
            for key in ("recall", "precision", "fp_rate_correct_code", "principal_hit_first"):
                a, b = p0[key], p1[key]
                deltas.append(f"{b - a:+.2f}" if a is not None and b is not None else "-")
            lines.append(f"| {round_name} | {model} | " + " | ".join(deltas) + " |")
    unmapped = sum(r["unmapped_items"] for r in rows)
    if unmapped:
        lines += ["", f"{unmapped} itens ainda sem subcategoria definida em `{MAPPING_PATH.relative_to(ROOT)}`; "
                      "as colunas de violação principal e categoria são provisórias até a revisão manual."]
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rounds", nargs="+", required=True, help="Rounds in order, e.g. round_01 round_02.")
    args = parser.parse_args()

    truth = load_ground_truth()
    codes, severity_of = load_taxonomy()
    principal = {
        (sample_id, variant): codes[meta["subcategory"]]
        for sample_id, (_, meta) in load_samples().items()
        for variant, gt in meta["ground_truth"].items() if gt["has_violation"]
    }
    mapping = load_mapping()

    rounds = list(dict.fromkeys(args.rounds))
    rows, outcomes = [], {}
    for round_name in rounds:
        round_rows, round_outcomes = summarize_round(round_name, truth, principal, mapping, severity_of)
        rows += round_rows
        for key, value in round_outcomes.items():
            outcomes.setdefault(key, {})[round_name] = value

    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    with (TABLES_DIR / "rounds_comparison.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    (TABLES_DIR / "rounds_comparison.md").write_text(markdown(rows, rounds), encoding="utf-8")

    with (TABLES_DIR / "round_transitions.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["model", "prompt", "sample_id", "variant", *rounds, "transition"])
        for key, by_round in sorted(outcomes.items()):
            sequence = [by_round.get(r, "-") for r in rounds]
            writer.writerow([*key, *sequence, "stable" if len(set(sequence) - {"-"}) <= 1 else "→".join(sequence)])

    # Ground-truth review candidates: correct variants flagged by every configuration of a
    # round, or by at least three configurations in two or more rounds (ADR-R023).
    flags = defaultdict(lambda: defaultdict(int))
    configs = defaultdict(lambda: defaultdict(int))
    for (model, prompt, sample_id, variant), by_round in outcomes.items():
        for round_name, value in by_round.items():
            configs[(sample_id, variant)][round_name] += 1
            flags[(sample_id, variant)][round_name] += value == "FP"
    with (TABLES_DIR / "ground_truth_review_candidates.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["sample_id", "variant", *[f"fp_{r}" for r in rounds], "reason"])
        for key, by_round in sorted(flags.items()):
            unanimous = [r for r in rounds if by_round[r] and by_round[r] == configs[key][r]]
            repeated = [r for r in rounds if by_round[r] >= 3]
            if unanimous or len(repeated) >= 2:
                reason = f"all configurations in {', '.join(unanimous)}" if unanimous else "3+ configurations in 2+ rounds"
                writer.writerow([*key, *[f"{by_round[r]}/{configs[key][r]}" for r in rounds], reason])

    print((TABLES_DIR / "rounds_comparison.md").read_text(encoding="utf-8"))
    print(f"Tables written to {TABLES_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
