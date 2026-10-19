#!/usr/bin/env python3
"""Run the benchmark against real LLM providers and store raw responses."""

from __future__ import annotations

import argparse
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
    import anthropic
except ImportError as exc:  # pragma: no cover
    raise SystemExit("The Anthropic SDK is required. Install it with: pip install anthropic") from exc

try:
    from google import genai
    from google.genai import errors as genai_errors
except ImportError as exc:  # pragma: no cover
    raise SystemExit("The Google Gen AI SDK is required. Install it with: pip install google-genai") from exc


def load_environment():
    """Load .env, which takes precedence over variables already set in the shell.

    The experimental conditions are documented in .env, so a variable exported in the
    terminal (for example CLAUDE_EFFORT) must not silently change them.
    """
    dotenv_path = ROOT / ".env"
    if dotenv_path.exists():
        for line in dotenv_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key, value = key.strip(), value.strip().strip('"').strip("'")
            if key in os.environ and os.environ[key] != value and not key.endswith("_API_KEY"):
                print(f"Note: {key} from .env overrides the value set in the shell.")
            os.environ[key] = value


load_environment()

EXPERIMENTS_DIR = ROOT / "experiments"
DATASET_DIR = ROOT / "dataset"
PROMPTS_DIR = ROOT / "prompts"
RESULTS_DIR = ROOT / "results"

PROMPT_MAP = {
    "P0": "P0_zero_shot.md",
    "P1": "P1_guidelines.md",
}
RESPONSE_SCHEMA_PATH = PROMPTS_DIR / "response_schema.json"
SUPPORTED_PROVIDERS = ("gemini", "claude")
API_KEY_VARIABLES = {
    "gemini": "GEMINI_API_KEY",
    "claude": "ANTHROPIC_API_KEY",
}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


RESPONSE_SCHEMA = load_json(RESPONSE_SCHEMA_PATH)


def selected_providers() -> list[str]:
    raw = os.getenv("LLM_PROVIDERS", "gemini,claude")
    providers = [item.strip().lower() for item in raw.split(",") if item.strip()]
    unknown = [item for item in providers if item not in SUPPORTED_PROVIDERS]
    if not providers or unknown:
        raise SystemExit(
            f"LLM_PROVIDERS must list one or more of {', '.join(SUPPORTED_PROVIDERS)}; got {raw!r}."
        )
    return providers


def ensure_api_key(provider: str) -> str:
    variable_name = API_KEY_VARIABLES[provider]
    api_key = os.getenv(variable_name)
    if not api_key:
        raise SystemExit(
            f"{variable_name} is not configured. Copy .env.example to .env and set a valid key before running the experiment."
        )
    return api_key


def provider_settings(provider: str) -> dict:
    if provider == "gemini":
        return {
            "model": os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
            "temperature": float(os.getenv("GEMINI_TEMPERATURE", "0")),
        }
    return {
        "model": os.getenv("CLAUDE_MODEL", "claude-opus-5-5"),
        "effort": os.getenv("CLAUDE_EFFORT", "low"),
        "max_tokens": int(os.getenv("CLAUDE_MAX_TOKENS", "16000")),
    }


def collect_samples():
    sample_rows = []
    for metadata_path in sorted((DATASET_DIR / "samples").glob("*/metadata.json")):
        metadata = load_json(metadata_path)
        files = metadata.get("files", {})
        for variant_name in metadata.get("ground_truth", {}):
            sample_rows.append({
                "sample_id": metadata["id"],
                "variant": variant_name,
                "category": metadata["category"],
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


def parse_response(content: str) -> tuple[dict, bool]:
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        return {"violations": [], "raw_text": content}, False
    if not isinstance(parsed, dict) or not isinstance(parsed.get("violations"), list):
        return {"violations": [], "raw_text": content}, False
    return parsed, True


def call_gemini(client, settings: dict, final_prompt: str) -> dict:
    started_at = time.perf_counter()
    response = client.models.generate_content(
        model=settings["model"],
        contents=final_prompt,
        config=genai.types.GenerateContentConfig(
            temperature=settings["temperature"],
            response_mime_type="application/json",
            response_json_schema=RESPONSE_SCHEMA,
        ),
    )
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    usage_metadata = getattr(response, "usage_metadata", None)
    usage = {}
    if usage_metadata:
        usage = {
            "prompt_tokens": getattr(usage_metadata, "prompt_token_count", 0),
            "completion_tokens": getattr(usage_metadata, "candidates_token_count", 0),
            "thinking_tokens": getattr(usage_metadata, "thoughts_token_count", 0),
            "total_tokens": getattr(usage_metadata, "total_token_count", 0),
        }

    candidates = getattr(response, "candidates", None) or []
    finish_reason = getattr(candidates[0], "finish_reason", None) if candidates else None
    parsed, valid = parse_response(response.text or "")
    return {
        "response": parsed,
        "valid_json": valid,
        "stop_reason": str(finish_reason) if finish_reason is not None else None,
        "usage": usage,
        "latency_ms": latency_ms,
    }


def call_claude(client, settings: dict, final_prompt: str) -> dict:
    started_at = time.perf_counter()
    response = client.messages.create(
        model=settings["model"],
        max_tokens=settings["max_tokens"],
        output_config={
            "effort": settings["effort"],
            "format": {"type": "json_schema", "schema": RESPONSE_SCHEMA},
        },
        messages=[{"role": "user", "content": final_prompt}],
    )
    latency_ms = int((time.perf_counter() - started_at) * 1000)

    usage = {
        "prompt_tokens": response.usage.input_tokens,
        "completion_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.input_tokens + response.usage.output_tokens,
    }

    text = next((block.text for block in response.content if block.type == "text"), "")
    parsed, valid = parse_response(text)
    result = {
        "response": parsed,
        "valid_json": valid,
        "stop_reason": response.stop_reason,
        "usage": usage,
        "latency_ms": latency_ms,
        "request_id": response._request_id,
    }
    if response.stop_reason == "refusal" and response.stop_details:
        result["stop_details"] = {
            "category": response.stop_details.category,
            "explanation": response.stop_details.explanation,
        }
    return result


def build_clients(providers: list[str]) -> dict:
    clients = {}
    for provider in providers:
        api_key = ensure_api_key(provider)
        if provider == "gemini":
            clients[provider] = genai.Client(api_key=api_key)
        else:
            clients[provider] = anthropic.Anthropic(api_key=api_key)
    return clients


def call_provider(provider: str, client, settings: dict, final_prompt: str) -> dict:
    try:
        if provider == "gemini":
            return call_gemini(client, settings, final_prompt)
        return call_claude(client, settings, final_prompt)
    except (anthropic.APIStatusError, anthropic.APIConnectionError, genai_errors.APIError) as exc:
        return {
            "response": {"violations": []},
            "valid_json": False,
            "stop_reason": None,
            "usage": {},
            "latency_ms": None,
            "error": {"type": type(exc).__name__, "message": str(exc)},
        }


def classify_status(result: dict) -> str:
    if result.get("error"):
        return "error"
    if result.get("stop_reason") == "refusal":
        return "refusal"
    if result.get("stop_reason") == "max_tokens":
        return "max_tokens"
    if not result.get("valid_json"):
        return "invalid_json"
    return "ok"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--experiment", choices=("pilot", "final"), default="final")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List the planned calls without contacting any provider.",
    )
    args = parser.parse_args()

    config = load_yaml(EXPERIMENTS_DIR / args.experiment / "config.yaml")
    experiment_id = config["experiment"]["id"]
    prompt_names = config["experiment"].get("prompts", ["P0"])
    repetitions = int(config["experiment"].get("repetitions", 1))
    providers = selected_providers()
    settings = {provider: provider_settings(provider) for provider in providers}
    samples = collect_samples()

    tasks = [
        (provider, sample, prompt_name, run_number)
        for provider in providers
        for sample in samples
        for prompt_name in prompt_names
        for run_number in range(1, repetitions + 1)
    ]
    random.shuffle(tasks)

    output_root = RESULTS_DIR / "raw" / args.experiment

    def output_path(provider, sample, prompt_name, run_number) -> Path:
        case_id = f"{sample['sample_id']}_{sample['variant']}"
        model_dir = settings[provider]["model"].replace("/", "_")
        return output_root / model_dir / prompt_name / case_id / f"run_{run_number:02d}.json"

    pending = [task for task in tasks if not output_path(*task).exists()]
    print(
        f"{experiment_id}: {len(tasks)} planned calls "
        f"({len(samples)} variants x {len(prompt_names)} prompts x {repetitions} runs x {len(providers)} providers); "
        f"{len(tasks) - len(pending)} already stored, {len(pending)} pending."
    )
    for provider in providers:
        print(f"  {provider}: {settings[provider]}")
    if args.dry_run:
        return

    clients = build_clients(providers)
    prompt_templates = {name: load_prompt(name) for name in prompt_names}
    errors = 0

    for index, (provider, sample, prompt_name, run_number) in enumerate(pending, start=1):
        code = load_code_for_sample(sample)
        final_prompt = prompt_templates[prompt_name].replace("{{CODE}}", code)
        result = call_provider(provider, clients[provider], settings[provider], final_prompt)
        payload = {
            "experiment_id": experiment_id,
            "case_id": f"{sample['sample_id']}_{sample['variant']}",
            "provider": provider,
            "model": settings[provider]["model"],
            "parameters": {key: value for key, value in settings[provider].items() if key != "model"},
            "prompt": prompt_name,
            "run": run_number,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request": {
                "sample_id": sample["sample_id"],
                "variant": sample["variant"],
                "category": sample["category"],
                "source_file": sample.get("source_file"),
            },
            "status": classify_status(result),
            **result,
        }
        if payload["status"] == "error":
            # API failures are logged but not stored as responses, so the call is retried on the next run.
            output_root.mkdir(parents=True, exist_ok=True)
            with (output_root / "_errors.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
            errors += 1
        else:
            path = output_path(provider, sample, prompt_name, run_number)
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[{index}/{len(pending)}] {provider} {prompt_name} {payload['case_id']} run {run_number}: {payload['status']}")

    print(f"Raw responses stored under {output_root}")
    if errors:
        print(f"{errors} calls failed and were logged in {output_root / '_errors.jsonl'}; run the script again to retry them.")


if __name__ == "__main__":
    main()
