#!/usr/bin/env python3
"""
Model Testing Pipeline for OpenCode

Tests all configured models sequentially and generates a YAML report.
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """Represents a configured model from opencode.json"""

    provider: str = Field(..., description="Provider name")
    model_id: str = Field(..., description="Model identifier")
    name: str | None = Field(None, description="Human-readable model name")


class TestResult(BaseModel):
    """Result of testing a single model"""

    model_id: str = Field(..., description="Full model identifier (provider/model)")
    working: bool = Field(..., description="Whether the model responded successfully")
    assistant_message: str | None = Field(None, description="The model's response")
    test_datetime: str = Field(..., description="ISO 8601 timestamp of the test")
    error: str | None = Field(None, description="Error message if test failed")


class ModelTestReport(BaseModel):
    """Complete test report for all models"""

    last_update_date: str = Field(..., description="ISO 8601 timestamp of report generation")
    models: list[TestResult] = Field(default_factory=list, description="List of model test results")

    def to_yaml(self) -> str:
        """Convert report to YAML string"""
        return yaml.dump(
            self.model_dump(mode="json"),
            default_flow_style=False,
            sort_keys=False,
            allow_unicode=True,
        )


def load_opencode_config(config_path: Path = Path("opencode.json")) -> dict[str, Any]:
    """Load and parse opencode.json configuration"""
    with open(config_path, "r") as f:
        return json.load(f)


def extract_configured_models(config: dict[str, Any]) -> list[ModelConfig]:
    """
    Extract all configured models from opencode config.

    Skips blacklisted models and disabled providers.
    """
    models = []
    disabled_providers = set(config.get("disabled_providers", []))

    provider_configs = config.get("provider", {})

    for provider_name, provider_data in provider_configs.items():
        # Skip disabled providers
        if provider_name in disabled_providers:
            continue

        # Get provider-level blacklist
        provider_blacklist = set(provider_data.get("blacklist", []))

        # Extract models from this provider
        models_dict = provider_data.get("models", {})
        for model_id, model_config in models_dict.items():
            # Skip blacklisted models
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
    Test a single model using opencode run command.

    Args:
        model_config: Model configuration to test
        timeout: Timeout in seconds for the entire run

    Returns:
        TestResult with success/failure status and response
    """
    full_model_id = f"{model_config.provider}/{model_config.model_id}"
    test_datetime = datetime.now(timezone.utc).isoformat()

    try:
        # Run opencode with JSON output format
        result = subprocess.run(
            [
                "opencode",
                "run",
                "--model",
                full_model_id,
                "--format",
                "json",
                "Respond with exactly: WORKING",
            ],
            capture_output=True,
            text=True,
            timeout=timeout,
        )

        # Parse JSON output to extract assistant message
        assistant_message = None
        if result.stdout:
            for line in result.stdout.strip().split("\n"):
                if line:
                    try:
                        event = json.loads(line)
                        if event.get("type") == "assistant" and "text" in event:
                            assistant_message = event["text"]
                            break
                    except json.JSONDecodeError:
                        continue

        # If no structured message found, use stdout as fallback
        if not assistant_message and result.stdout:
            assistant_message = result.stdout.strip()

        # Consider successful if we got a response
        working = result.returncode == 0 and (assistant_message or result.returncode == 0)

        return TestResult(
            model_id=full_model_id,
            working=working,
            assistant_message=assistant_message,
            test_datetime=test_datetime,
            error=None if working else f"Exit code: {result.returncode}",
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


def run_pipeline(
    config_path: Path = Path("opencode.json"),
    output_path: Path = Path("model-test-results.yaml"),
    timeout: int = 20,
) -> ModelTestReport:
    """
    Run the complete model testing pipeline.

    Args:
        config_path: Path to opencode.json
        output_path: Path for output YAML report
        timeout: Timeout per model test in seconds

    Returns:
        Complete ModelTestReport
    """
    print(f"Loading configuration from {config_path}...")
    config = load_opencode_config(config_path)

    print("Extracting configured models...")
    models = extract_configured_models(config)
    print(f"Found {len(models)} configured models to test")

    results = []
    for i, model_config in enumerate(models, 1):
        model_name = model_config.name or model_config.model_id
        print(f"[{i}/{len(models)}] Testing {model_config.provider}/{model_config.model_id} ({model_name})...")
        result = test_model(model_config, timeout)
        results.append(result)
        status = "✓" if result.working else "✗"
        print(f"  {status} {result.error or 'OK'}")

    report = ModelTestReport(
        last_update_date=datetime.now(timezone.utc).isoformat(),
        models=results,
    )

    print(f"\nWriting report to {output_path}...")
    with open(output_path, "w") as f:
        f.write(report.to_yaml())

    # Summary
    working_count = sum(1 for r in results if r.working)
    print(f"\nSummary: {working_count}/{len(results)} models working")

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test OpenCode models and generate YAML report")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("opencode.json"),
        help="Path to opencode.json config file",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("model-test-results.yaml"),
        help="Path for output YAML report",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=20,
        help="Timeout per model test in seconds",
    )

    args = parser.parse_args()
    run_pipeline(config_path=args.config, output_path=args.output, timeout=args.timeout)
