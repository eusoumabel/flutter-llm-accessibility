#!/usr/bin/env python3
"""Build the blind review spreadsheet for the false positives of a round.

A false positive is a response that reports at least one violation for a variant whose
ground truth has none. Every reported violation becomes one review item. Each response
is shown under a letter (A-D) per variant, so reviewers do not see which model or prompt
produced it. The letter-to-model key is written to a separate CSV that should only be
opened after the review is finished.

The spreadsheet only holds the items. Reviewers classify them with the Apps Script in
analysis/pilot_review/apps_script/, which writes each reviewer's answers to a sheet of
their own ("Revisão – <reviewer>").
"""

from __future__ import annotations

import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
SAMPLES_DIR = ROOT / "dataset" / "samples"
RAW_DIR = ROOT / "results" / "raw"
OUT_DIR = ROOT / "analysis" / "pilot_review"

HEADER_FILL = PatternFill("solid", fgColor="1F5F73")
WRAP = Alignment(wrap_text=True, vertical="top")


def load_samples():
    samples = {}
    for path in sorted(SAMPLES_DIR.glob("*/metadata.json")):
        meta = json.loads(path.read_text(encoding="utf-8"))
        samples[meta["id"]] = (path.parent, meta)
    return samples


def numbered_code(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    return "\n".join(f"{i:>3}  {line}" for i, line in enumerate(lines, 1))


def describe_violations(violations: list) -> str:
    if not violations:
        return "Sem violação"
    parts = []
    for item in violations:
        lines = item.get("affected_lines") or {}
        where = f" (linhas {lines.get('start')}-{lines.get('end')})" if lines else ""
        parts.append(f"{item['id']} {item['type']}{where}: {item.get('description', '')}")
    return "\n".join(parts)


def available_rounds() -> list[str]:
    return sorted(path.name for path in RAW_DIR.iterdir() if path.is_dir())


def load_responses(round_name: str):
    responses = defaultdict(list)
    for path in sorted((RAW_DIR / round_name).rglob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        request = record.get("request", {})
        key = (request.get("sample_id"), request.get("variant"))
        responses[key].append((path, record))
    return responses


def style_sheet(ws, widths: dict):
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEADER_FILL
        cell.alignment = WRAP
    for letter, width in widths.items():
        ws.column_dimensions[letter].width = width
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = WRAP
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = ws.dimensions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", required=True, choices=available_rounds(), help="Round directory under results/raw/, e.g. round_02.")
    parser.add_argument("--seed", type=int, default=20261023)
    args = parser.parse_args()

    samples = load_samples()
    responses = load_responses(args.round)

    fp_rows, key_rows, variants = [], [], {}
    for (sample_id, variant), records in sorted(responses.items()):
        sample_dir, meta = samples[sample_id]
        truth = meta["ground_truth"][variant]
        if truth["has_violation"]:
            continue
        # Letters are drawn over all responses of the variant, so they stay the same
        # as in earlier versions of this spreadsheet.
        records = sorted(records, key=lambda item: (item[1]["model"], item[1]["prompt"], item[1]["run"]))
        letters = [chr(ord("A") + i) for i in range(len(records))]
        random.Random(f"{args.seed}-{sample_id}-{variant}").shuffle(letters)

        flagged, alerts = 0, 0
        for letter, (path, record) in zip(letters, records):
            if record.get("status") != "ok":
                continue
            reported = [v for v in record["response"].get("violations", []) if isinstance(v, dict)]
            if not reported:
                continue
            flagged += 1
            key_rows.append({
                "sample_id": sample_id, "variant": variant, "resposta": letter,
                "model": record["model"], "prompt": record["prompt"], "run": record["run"],
                "raw_file": str(path.relative_to(ROOT)),
            })
            for index, item in enumerate(reported, 1):
                alerts += 1
                fp_rows.append([
                    sample_id, variant, meta["category"], letter, index,
                    item.get("type", ""), item.get("affected_code", ""),
                    item.get("explanation", ""), item.get("confidence", ""),
                    # Prompts v2 add severity (ADR-R022); round_01 leaves it empty.
                    item.get("severity", ""),
                ])
        if flagged:
            paired = [
                f"{other}: {describe_violations(gt['violations'])}"
                for other, gt in meta["ground_truth"].items() if other != variant
            ]
            variants[(sample_id, variant)] = {
                "flagged": flagged,
                "alerts": alerts,
                "total": len(records),
                "row": [
                    sample_id, variant, meta["category"], meta["subcategory"],
                    describe_violations(truth["violations"]),
                    "\n".join(paired) or "-",
                    meta.get("notes", ""),
                    numbered_code(sample_dir / meta["files"][variant]),
                ],
            }

    wb = Workbook()

    ws = wb.active
    ws.title = "Como usar"
    guide = [
        [f"Revisão cega da {args.round}: falsos positivos"],
        ["Passo a passo completo: analysis/pilot_review/README.md"],
        [""],
        ["Como classificar"],
        ["Use o menu 'Revisão do piloto → Abrir classificador' (Apps Script em analysis/pilot_review/apps_script/)."],
        ["Cada revisor grava numa aba própria, 'Revisão – <nome>', criada no primeiro acesso."],
        ["As demais abas são a fonte dos itens. Não as altere."],
        ["Não abra as abas de revisão do outro revisor antes de os dois terminarem."],
        [""],
        ["Classes"],
        ["FP-GT", "O problema existe e está na taxonomia: o ground truth está errado."],
        ["FP-FORA", "Problema real de acessibilidade, mas fora do escopo SEM/INT (ex.: contraste, foco, idioma)."],
        ["FP-SUG", "Recomendação de boa prática, não uma violação."],
        ["FP-FALSO", "A afirmação é falsa sobre o código ou sobre o comportamento do Flutter."],
        [""],
        [f"Não abra chave_respostas_{args.round}.csv antes de terminar a revisão."],
    ]
    for line in guide:
        ws.append(line)
    for row in (1, 4, 10):
        ws.cell(row=row, column=1).font = Font(bold=True, size=13 if row == 1 else 11)
    ws.column_dimensions["A"].width = 14
    ws.column_dimensions["B"].width = 90

    ws = wb.create_sheet("Resumo por variante")
    ws.append(["sample_id", "variant", "tipo_erro", "respostas_com_erro", "alertas"])
    for (sample_id, variant), info in sorted(variants.items()):
        ws.append([sample_id, variant, "FP", f"{info['flagged']} de {info['total']}", info["alerts"]])
    style_sheet(ws, {"A": 11, "B": 12, "C": 10, "D": 18, "E": 10})

    ws = wb.create_sheet("Codigo")
    ws.append(["sample_id", "variant", "categoria", "subcategoria", "ground_truth", "outras_variantes", "nota_anotacao", "codigo"])
    for (sample_id, variant), info in sorted(variants.items()):
        ws.append(info["row"])
    style_sheet(ws, {"A": 11, "B": 12, "C": 12, "D": 22, "E": 40, "F": 40, "G": 40, "H": 90})
    for row in ws.iter_rows(min_row=2, min_col=8, max_col=8):
        row[0].font = Font(name="Menlo", size=10)

    ws = wb.create_sheet("Falsos positivos")
    ws.append([
        "sample_id", "variant", "categoria", "resposta", "n_violacao", "tipo_modelo",
        "trecho_afetado", "explicacao", "confianca_modelo", "gravidade_modelo",
    ])
    for row in fp_rows:
        ws.append(row)
    style_sheet(ws, {"A": 11, "B": 12, "C": 12, "D": 9, "E": 7, "F": 26, "G": 40, "H": 60, "I": 10, "J": 10})

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    xlsx_path = OUT_DIR / f"revisao_{args.round}.xlsx"
    wb.save(xlsx_path)

    key_path = OUT_DIR / f"chave_respostas_{args.round}.csv"
    with key_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(key_rows[0].keys()) if key_rows else ["sample_id"])
        writer.writeheader()
        writer.writerows(key_rows)

    print(f"{len(variants)} variants, {len(key_rows)} false-positive responses, {len(fp_rows)} review items")
    print(f"Review sheet: {xlsx_path.relative_to(ROOT)}")
    print(f"Answer key:   {key_path.relative_to(ROOT)} (open only after the review)")


if __name__ == "__main__":
    main()
