#!/usr/bin/env python3
"""Run the benchmark against a real LLM provider and store raw responses."""

from __future__ import annotations

import json
import os
import random
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required for experiment configuration. Install it with: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parent.parent

try:
    from openai import OpenAI
except ImportError as exc:  # pragma: no cover
    raise SystemExit("The OpenAI SDK is required. Install it with: pip install openai") from exc

try:
    from google import genai
except ImportError as exc:  # pragma: no cover
    raise SystemExit("The Google Gen AI SDK is required. Install it with: pip install google-genai") from exc


def load_environment():
    dotenv_path = ROOT / ".env"
    if dotenv_path.exists():
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_environment()

EXPERIMENTS_DIR = ROOT / "experiments"
DATASET_DIR = ROOT / "dataset"
PROMPTS_DIR = ROOT / "prompts"
RESULTS_DIR = ROOT / "results"

PROMPT_MAP = {
    "P0": "P0_zero_shot.md",
    "P1": "P1_guidelines.md",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def ensure_api_key(provider: str) -> str:
    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        variable_name = "GEMINI_API_KEY"
    else:
        api_key = os.getenv("OPENAI_API_KEY")
        variable_name = "OPENAI_API_KEY"
    if not api_key:
        raise SystemExit(
            f"{variable_name} is not configured. Copy .env.example to .env and set a valid key before running the experiment."
        )
    return api_key


def collect_samples():
    sample_rows = []
    for metadata_path in sorted((DATASET_DIR / "samples").glob("*/metadata.json")):
        metadata = load_json(metadata_path)
        files = metadata.get("files", {})
        for variant_name, variant_data in metadata.get("ground_truth", {}).items():
            sample_rows.append({
                "sample_id": metadata["id"],
                "variant": variant_name,
                "category": metadata["category"],
                "ground_truth": bool(variant_data.get("has_violation")),
                "source_file": files.get(variant_name) or files.get("component"),
                "metadata_path": metadata_path,
            })
    return sample_rows


def load_prompt(prompt_name: str) -> str:
    file_name = PROMPT_MAP.get(prompt_name)
    if not file_name:
        raise ValueError(f"Unsupported prompt {prompt_name!r}")
    path = PROMPTS_DIR / file_name
    return path.read_text(encoding="utf-8")


def load_code_for_sample(sample: dict) -> str:
    sample_dir = sample["metadata_path"].parent
    file_name = sample.get("source_file")
    if not file_name:
        raise ValueError(f"No code file found for {sample['sample_id']}:{sample['variant']}")
    return (sample_dir / file_name).read_text(encoding="utf-8")


def parse_response(content: str) -> dict:
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {"violations": [], "raw_text": content}


def call_openai(prompt_name: str, final_prompt: str) -> dict:
    ensure_api_key("openai")
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0"))

    started_at = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        response_format={"type": "json_object"},
        messages=[
            {"role": "user", "content": final_prompt},
        ],
    )
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    content = response.choices[0].message.content or "{}"

    usage = {}
    if getattr(response, "usage", None):
        usage = {
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }

    return {
        "response": parse_response(content),
        "usage": usage,
        "latency_ms": latency_ms,
        "model": model,
    }


def call_gemini(prompt_name: str, final_prompt: str) -> dict:
    api_key = ensure_api_key("gemini")
    client = genai.Client(api_key=api_key)
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    temperature = float(os.getenv("GEMINI_TEMPERATURE", os.getenv("OPENAI_TEMPERATURE", "0")))

    started_at = time.perf_counter()
    response = client.models.generate_content(
        model=model,
        contents=final_prompt,
        config=genai.types.GenerateContentConfig(
            temperature=temperature,
            response_mime_type="application/json",
        ),
    )
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    usage_metadata = getattr(response, "usage_metadata", None)
    usage = {}
    if usage_metadata:
        usage = {
            "prompt_tokens": getattr(usage_metadata, "prompt_token_count", 0),
            "completion_tokens": getattr(usage_metadata, "candidates_token_count", 0),
            "total_tokens": getattr(usage_metadata, "total_token_count", 0),
        }

    return {
        "response": parse_response(response.text or "{}"),
        "usage": usage,
        "latency_ms": latency_ms,
        "model": model,
    }


def call_provider(prompt_name: str, code: str) -> dict:
    provider = os.getenv("LLM_PROVIDER", "openai").strip().lower()
    prompt_template = load_prompt(prompt_name)
    final_prompt = prompt_template.replace("{{CODE}}", code)
    if provider == "openai":
        return call_openai(prompt_name, final_prompt)
    if provider == "gemini":
        return call_gemini(prompt_name, final_prompt)
    raise SystemExit("LLM_PROVIDER must be either 'openai' or 'gemini'.")


def main():
    config_path = EXPERIMENTS_DIR / "final" / "config.yaml"
    config = load_yaml(config_path)
    samples = collect_samples()
    random.shuffle(samples)

    experiment_id = config["experiment"]["id"]
    prompt_names = config["experiment"].get("prompts", ["P0"])
    output_root = RESULTS_DIR / "raw" / "final"
    output_root.mkdir(parents=True, exist_ok=True)

    case_index = 1
    for sample in samples:
        for prompt_name in prompt_names:
            for run_number in range(1, int(config["experiment"].get("repetitions", 1)) + 1):
                case_id = f"CASE_{case_index:04d}"
                code = load_code_for_sample(sample)
                provider_payload = call_provider(prompt_name, code)
                payload = {
                    "experiment_id": experiment_id,
                    "case_id": case_id,
                    "model": provider_payload["model"],
                    "prompt": prompt_name,
                    "run": run_number,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "request": {
                        "sample_id": sample["sample_id"],
                        "variant": sample["variant"],
                        "category": sample["category"],
                        "source_file": sample.get("source_file"),
                    },
                    "response": provider_payload["response"],
                    "usage": provider_payload["usage"],
                    "latency_ms": provider_payload["latency_ms"],
                }
                case_dir = output_root / provider_payload["model"].replace("/", "_") / prompt_name / case_id
                case_dir.mkdir(parents=True, exist_ok=True)
                (case_dir / f"run_{run_number:02d}.json").write_text(
                    json.dumps(payload, ensure_ascii=False, indent=2),
                    encoding="utf-8",
                )
                case_index += 1

    print(f"Prepared experimental cases under {output_root}")


if __name__ == "__main__":
    main()
