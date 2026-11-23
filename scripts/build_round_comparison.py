#!/usr/bin/env python3
"""Build an open, side-by-side spreadsheet of what the models returned in each round.

One row per variant: ground truth, numbered code and, for every model and prompt, the
response of each round (type, mapped subcategory, severity, confidence and
explanation) and the outcome sequence across rounds. Unlike the blind review of
round 1, models and prompts are named: the goal is to read how the responses change
between rounds (ADR-R023), not to measure agreement.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

from build_pilot_review import describe_violations, load_samples, numbered_code, style_sheet
from calculate_metrics import load_ground_truth
from map_types import MAPPING_PATH

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "results" / "raw"
OUT_DIR = ROOT / "analysis" / "round_comparison"
OUTCOME = {(True, True): "TP", (True, False): "FN", (False, True): "FP", (False, False): "TN"}


def load_mapping() -> dict:
    if not MAPPING_PATH.exists():
        return {}
    with MAPPING_PATH.open("r", encoding="utf-8", newline="") as handle:
        return {(row["round"], row["model"], row["prompt"], row["raw_type"]): row for row in csv.DictReader(handle)}


def load_round(round_name: str) -> dict:
    responses = {}
    for path in sorted((RAW_DIR / round_name).rglob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        request = record.get("request", {})
        responses[(record["model"], record["prompt"], request.get("sample_id"), request.get("variant"))] = record
    return responses


def describe_response(record: dict | None, round_name: str, mapping: dict) -> tuple[str, str]:
    """Return (text shown in the cell, outcome-relevant 'predicted' flag as Y/N/INV)."""
    if record is None:
        return "-", "-"
    if record.get("status") != "ok":
        return f"[{record.get('status')}]", "INV"
    items = [v for v in record["response"].get("violations", []) if isinstance(v, dict)]
    if not items:
        return "Sem violação", "N"
    parts = []
    for index, item in enumerate(items, 1):
        entry = mapping.get((round_name, record["model"], record["prompt"], item.get("type", "")), {})
        code = entry.get("subcategory") or entry.get("method") or "?"
        tags = ", ".join(filter(None, [code, item.get("severity", ""), item.get("confidence", "")]))
        parts.append(f"{index}. {item.get('type', '')} [{tags}]\n{item.get('explanation', '')}")
    return "\n\n".join(parts), "Y"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--rounds", nargs="+", required=True, help="Rounds in order, e.g. round_01 round_02.")
    args = parser.parse_args()

    rounds = list(dict.fromkeys(args.rounds))
    samples = load_samples()
    truth = load_ground_truth()
    mapping = load_mapping()
    responses = {r: load_round(r) for r in rounds}
    configs = sorted({key[:2] for by_round in responses.values() for key in by_round})

    header = ["sample_id", "variant", "categoria", "ground_truth", "codigo"]
    for model, prompt in configs:
        short = f"{model.split('-')[0]} {prompt}"
        header += [f"{short} · {r}" for r in rounds] + [f"{short} · resultado"]
    header.append("observacao")

    rows, changed = [], []
    for (sample_id, variant), gt in sorted(truth.items()):
        sample_dir, meta = samples[sample_id]
        row = [sample_id, variant, meta["category"],
               describe_violations(meta["ground_truth"][variant]["violations"]),
               numbered_code(sample_dir / meta["files"][variant])]
        any_change = False
        for model, prompt in configs:
            sequence = []
            for r in rounds:
                text, flag = describe_response(responses[r].get((model, prompt, sample_id, variant)), r, mapping)
                row.append(text)
                sequence.append(OUTCOME[(gt["has_violation"], flag == "Y")] if flag in ("Y", "N") else flag)
            # A round without a response ('-') is not counted as a change.
            any_change |= len(set(sequence) - {"-"}) > 1
            row.append(" → ".join(sequence))
        row.append("")
        rows.append(row)
        if any_change:
            changed.append(row)

    wb = Workbook()
    ws = wb.active
    ws.title = "Como usar"
    for line in [
        [f"Comparação aberta entre rodadas: {', '.join(rounds)}"],
        ["Uma linha por variante. Para cada modelo e prompt há a resposta de cada rodada e o resultado."],
        ["Cada item mostra: tipo devolvido [subcategoria mapeada, gravidade, confiança] e a explicação."],
        ["A subcategoria vem de analysis/type_mapping/type_mapping.csv; '?' ou um método indica item ainda não mapeado."],
        ["Resultado: TP, FP, TN, FN ou INV por rodada, na ordem das rodadas."],
        ["A aba 'Mudanças' traz só as variantes cujo resultado mudou em alguma configuração; comece por ela."],
        ["Anote o que observar na coluna 'observacao'."],
    ]:
        ws.append(line)
    ws.cell(row=1, column=1).font = Font(bold=True, size=13)
    ws.column_dimensions["A"].width = 110

    widths = {"A": 11, "B": 12, "C": 12, "D": 40, "E": 80}
    for name, data in (("Variantes", rows), ("Mudanças", changed)):
        sheet = wb.create_sheet(name)
        sheet.append(header)
        for row in data:
            sheet.append(row)
        column_widths = dict(widths)
        for index in range(len(widths), len(header)):
            letter = sheet.cell(row=1, column=index + 1).column_letter
            column_widths[letter] = 14 if header[index].endswith("resultado") else 55
        style_sheet(sheet, column_widths)
        for cells in sheet.iter_rows(min_row=2, min_col=5, max_col=5):
            cells[0].font = Font(name="Menlo", size=10)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"comparacao_{'_'.join(rounds)}.xlsx"
    wb.save(out_path)
    print(f"{len(rows)} variants, {len(changed)} with a changed outcome")
    print(f"Spreadsheet: {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
