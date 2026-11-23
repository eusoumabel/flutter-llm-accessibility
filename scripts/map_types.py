#!/usr/bin/env python3
"""Map the violation types predicted in a round to the taxonomy.

The models write the violation type as free text, so it has to be matched to a
subcategory before the round can be compared with the ground truth. Each distinct type
is matched once per round, model and prompt and written to a CSV that the researchers
complete by hand (ADR-R023):

- an exact taxonomy key (``missing_accessible_label``) or an exact guideline name of
  the P1 v2 prompt (``Missing semantic role``) is mapped with ``method=auto``;
- otherwise English and Portuguese keywords are tried; one subcategory gives
  ``auto``, more than one gives ``auto_multi`` (to be checked);
- the category headings of the P1 prompts are ``generic`` (category only);
- contrast, keyboard, motion and text-scaling issues are ``out_of_scope``;
- anything else is left with an empty ``method`` for manual classification.

Rows whose method is ``manual`` are never overwritten, so the script can be run again
after new results arrive.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TAXONOMY_PATH = ROOT / "dataset" / "taxonomy.json"
NORMALIZED_DIR = ROOT / "results" / "normalized"
MAPPING_PATH = ROOT / "analysis" / "type_mapping" / "type_mapping.csv"

FIELDS = ["round", "model", "prompt", "raw_type", "occurrences", "subcategory", "category", "method"]

# Item names of the P1 v2 guidelines (prompts/v2/P1_guidelines.md). They are not in
# the taxonomy, and two of them differ from the taxonomy key.
GUIDELINE_NAMES = {
    "missing accessible label": "SEM-01",
    "incorrect accessible label": "SEM-02",
    "missing semantic role": "SEM-03",
    "missing semantic state": "SEM-04",
    "inaccessible custom control": "SEM-05",
    "insufficient target size": "INT-01",
    "inaccessible custom gesture": "INT-02",
    "interaction not exposed": "INT-03",
}

# Category headings of the P1 prompts and other types that only name a category.
GENERIC_TYPES = {
    "semantics and accessible information": "semantics",
    "accessibility: semantics and accessible information": "semantics",
    "semantics": "semantics",
    "semantics violation": "semantics",
    "interaction and interactive target accessibility": "interaction",
    "interactive target accessibility": "interaction",
    "interaction": "interaction",
    "interaction accessibility": "interaction",
    "accessibility": "",
    "usability/functional accessibility": "",
    "visual accessibility": "",
}

# Keywords per subcategory, matched on lowercase text without accents.
KEYWORDS = {
    "SEM-05": [r"custom (interactive )?control", r"controle (interativo )?(customizado|personalizado)"],
    "INT-02": [r"gesture", r"\bgesto", r"\bdrag", r"arrast", r"long[- ]press", r"pressionar e segurar",
               r"\bpinch", r"\bzoom", r"\bpan(ning)?\b", r"swipe", r"desliz"],
    "INT-01": [r"target size", r"touch target", r"tap target", r"interactive target", r"target width",
               r"tamanho do alvo", r"area de toque", r"alvo de toque", r"alvo (interativo )?(pequeno|insuficiente)",
               r"area (interativa|clicavel|tocavel)"],
    "INT-03": [r"semantic(s)? (tap )?action", r"tap action", r"action not wired", r"interaction not exposed",
               r"not operable", r"inaccessible interaction", r"missing interactive",
               r"acao (semantica|de toque)", r"interacao nao exposta", r"nao (e )?operavel", r"nao exp(oe|osta|osto)"],
    "SEM-04": [r"\bstates?\b",r"\bselected\b", r"\bselection\b", r"\btoggle", r"expanded", r"\bchecked\b",
               r"\benabled\b", r"\bdisabled\b", r"\bestado", r"selecionad", r"alternanc", r"expandid",
               r"marcad", r"desabilitad", r"habilitad"],
    "SEM-03": [r"\brole\b", r"button semantics", r"exposed as button", r"header semantics", r"heading",
               r"\bpapel\b", r"funcao semantica", r"semantica de botao", r"cabecalho"],
    "SEM-02": [r"incorrect (accessible )?(label|name)", r"inaccurate", r"misleading", r"mismatch",
               r"non[- ]descriptive", r"ambiguous label", r"inadequate", r"meaningless",
               r"rotulo (incorreto|impreciso|inadequado|enganoso|ambiguo|generico)", r"nome acessivel (incorreto|impreciso)",
               r"incorret", r"enganos", r"impreci"],
    "SEM-01": [r"label", r"accessible name", r"alternative text", r"alt text", r"semantic information missing",
               r"missing semantic information", r"\brotulo", r"nome acessivel", r"texto alternativo",
               r"descricao acessivel", r"sem descricao"],
}

OUT_OF_SCOPE = [r"contrast", r"\bcolou?r", r"keyboard", r"focus", r"motion", r"animation", r"text scal",
                r"\bfont", r"overflow", r"truncat", r"readab", r"reflow", r"instructional", r"sensory",
                r"contraste", r"\bcor(es)?\b", r"teclado", r"\bfoco\b", r"animac", r"movimento", r"\bfonte",
                r"escala de texto", r"truncad", r"legibil"]


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"\s+", " ", text.replace("_", " ").lower()).strip()


def taxonomy_codes() -> dict:
    taxonomy = json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))
    codes = {}
    for category in taxonomy["categories"].values():
        for key, item in category["violations"].items():
            codes[normalize_text(key)] = item["code"]
    return codes


def category_of(codes: list[str]) -> str:
    families = {code.split("-")[0] for code in codes}
    if families == {"SEM"}:
        return "semantics"
    if families == {"INT"}:
        return "interaction"
    return ""


def classify(raw_type: str, exact: dict) -> tuple[str, str, str]:
    """Return (subcategory, category, method) for one predicted type."""
    text = normalize_text(raw_type)
    if text in exact:
        code = exact[text]
        return code, category_of([code]), "auto"
    if text in GENERIC_TYPES:
        return "", GENERIC_TYPES[text], "generic"
    codes = [code for code, patterns in KEYWORDS.items() if any(re.search(p, text) for p in patterns)]
    if "SEM-02" in codes and "SEM-01" in codes:
        codes.remove("SEM-01")
    if codes:
        method = "auto" if len(codes) == 1 else "auto_multi"
        return "|".join(codes), category_of(codes), method
    if any(re.search(p, text) for p in OUT_OF_SCOPE):
        return "", "", "out_of_scope"
    return "", "", ""


def collect_types(round_name: str) -> dict:
    round_dir = NORMALIZED_DIR / round_name
    if not round_dir.is_dir():
        raise SystemExit(f"No normalized results for {round_name!r} in {NORMALIZED_DIR.relative_to(ROOT)}")
    counts = {}
    for path in sorted(round_dir.rglob("*.json")):
        record = json.loads(path.read_text(encoding="utf-8"))
        for raw_type in record.get("predicted_violations", []):
            key = (round_name, record.get("model"), record.get("prompt"), raw_type)
            counts[key] = counts.get(key, 0) + 1
    return counts


def load_mapping() -> dict:
    if not MAPPING_PATH.exists():
        return {}
    with MAPPING_PATH.open("r", encoding="utf-8", newline="") as handle:
        return {(row["round"], row["model"], row["prompt"], row["raw_type"]): row for row in csv.DictReader(handle)}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--round", required=True, help="Round directory under results/normalized/, e.g. round_02.")
    args = parser.parse_args()

    exact = {**taxonomy_codes(), **GUIDELINE_NAMES}
    mapping = load_mapping()
    for key, occurrences in collect_types(args.round).items():
        existing = mapping.get(key)
        if existing and existing["method"] == "manual":
            existing["occurrences"] = str(occurrences)
            continue
        subcategory, category, method = classify(key[3], exact)
        mapping[key] = dict(zip(FIELDS, [*key, str(occurrences), subcategory, category, method]))

    MAPPING_PATH.parent.mkdir(parents=True, exist_ok=True)
    with MAPPING_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(row for _, row in sorted(mapping.items()))

    rows = [row for key, row in mapping.items() if key[0] == args.round]
    summary = {}
    for row in rows:
        summary[row["method"] or "(to classify)"] = summary.get(row["method"] or "(to classify)", 0) + 1
    print(f"{len(rows)} distinct types in {args.round}: " + ", ".join(f"{k} {v}" for k, v in sorted(summary.items())))
    print(f"Mapping: {MAPPING_PATH.relative_to(ROOT)} (fill the empty and auto_multi rows, then set method=manual)")


if __name__ == "__main__":
    main()
