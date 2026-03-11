#!/usr/bin/env python3
"""
Model Testing Pipeline for OpenCode

Tests all configured models sequentially and generates a YAML report.
Each model is tested with a simple math question (17 + 25 = 42) to verify
meaningful computation, not just echo.
"""

import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


OPENCODE_BIN = Path(
    os.environ.get(
        "OPENCODE_BIN",
        str(Path.home() / ".opencode" / "bin" / "opencode"),
    )
)


class ModelConfig(BaseModel):
    """Represents a configured model from opencode.json"""

    provider: str
    model_id: str
    name: str | None = None


class TestResult(BaseModel):
    """Result of testing a single model"""

    model_id: str
    working: bool
    assistant_message: str | None
    test_datetime: str
    error: str | None = None


class ModelTestResults(BaseModel):
    """Container for all model test results"""

    last_update_date: str
    models: list[TestResult] = Field(default_factory=list)

    def to_yaml(self) -> str:
        """Convert to YAML string"""
        return yaml.dump(
            self.model_dump(mode="json"),
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def load_opencode_config(config_path: Path = Path("opencode.json")) -> dict:
    """Load opencode.json configuration"""
    with open(config_path, "r") as f:
        return json.load(f)


def extract_configured_models(config: dict) -> list[ModelConfig]:
    """Extract all configured models, filtering disabled/blacklisted"""
    models = []
    disabled_providers = set(config.get("disabled_providers", []))
    provider_configs = config.get("provider", {})

    for provider_name, provider_data in provider_configs.items():
        if provider_name in disabled_providers:
            continue

        provider_blacklist = set(provider_data.get("blacklist", []))
        models_dict = provider_data.get("models", {})

        for model_id, model_config in models_dict.items():
            if model_id in provider_blacklist:
                continue

            model_name = model_config.get("name") if isinstance(model_config, dict) else None
            models.append(
                ModelConfig(
                    provider=provider_name,
                    model_id=model_id,
                    name=model_name,
                )
            )

    return models


def test_model(model_config: ModelConfig, timeout: int = 20) -> TestResult:
    """
    Test a single model with a math question.

    Timing:
    - opencode startup: <10s
    - model response: <3s
    - Total timeout: 20s

    Returns working=true only if response contains correct answer (42).
    """
    full_model_id = f"{model_config.provider}/{model_config.model_id}"
    test_datetime = datetime.now(timezone.utc).isoformat()
    test_prompt = "What is 17 + 25? Respond with only the number."

    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            result = subprocess.run(
                [
                    str(OPENCODE_BIN),
                    "run",
                    "--agent",
                    "Minimal",
                    "-m",
                    full_model_id,
                    test_prompt,
                ],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=tmpdir,
            )

            assistant_message = result.stdout.strip() or None
            error_message = None

            # Check stderr for API errors
            if result.stderr:
                for line in result.stderr.split("\n"):
                    if "429" in line or "Too Many Requests" in line:
                        error_message = "429 Too Many Requests (rate limit exceeded)"
                    elif "API error" in line.lower() or "connection" in line.lower():
                        error_message = error_message or line.strip()

            # Validate response
            working = False
            final_error = error_message
            if assistant_message and not error_message:
                if assistant_message.strip() == "42":
                    working = True
                else:
                    final_error = f"Incorrect response: {assistant_message[:100]}"
            elif not assistant_message and not final_error:
                final_error = "No response received"

            return TestResult(
                model_id=full_model_id,
                working=working,
                assistant_message=assistant_message,
                test_datetime=test_datetime,
                error=final_error,
            )

        except subprocess.TimeoutExpired:
            return TestResult(
                model_id=full_model_id,
                working=False,
                assistant_message=None,
                test_datetime=test_datetime,
                error=f"Timeout after {timeout}s",
            )
        except Exception as e:
            return TestResult(
                model_id=full_model_id,
                working=False,
                assistant_message=None,
                test_datetime=test_datetime,
                error=str(e),
            )


def run_pipeline(config_path: Path = Path("opencode.json"), output_path: Path = Path("model-test-results.yaml"), timeout: int = 20) -> ModelTestResults:
    """Run the complete model testing pipeline"""
    print(f"Loading configuration from {config_path}...")
    config = load_opencode_config(config_path)

    print("Extracting configured models...")
    models = extract_configured_models(config)
    print(f"Found {len(models)} configured models to test\n")

    results = []
    for i, model_config in enumerate(models, 1):
        model_name = model_config.name or model_config.model_id
        print(f"[{i}/{len(models)}] Testing {model_config.provider}/{model_config.model_id}...")
        result = test_model(model_config, timeout)
        results.append(result)
        status = "✓" if result.working else "✗"
        if result.working:
            print(f"  {status} Response: {result.assistant_message[:50]}")
        else:
            print(f"  {status} Error: {result.error}")

    output = ModelTestResults(
        last_update_date=datetime.now(timezone.utc).isoformat(),
        models=results,
    )

    print(f"\nWriting results to {output_path}...")
    with open(output_path, "w") as f:
        f.write(output.to_yaml())

    working_count = sum(1 for r in results if r.working)
    print(f"\nSummary: {working_count}/{len(results)} models working")

    return output


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test OpenCode models and generate YAML report")
    parser.add_argument("--config", type=Path, default=Path("opencode.json"), help="Path to opencode.json")
    parser.add_argument("--output", type=Path, default=Path("model-test-results.yaml"), help="Path for output YAML")
    parser.add_argument("--timeout", type=int, default=20, help="Timeout per model test in seconds")

    args = parser.parse_args()
    run_pipeline(config_path=args.config, output_path=args.output, timeout=args.timeout)
