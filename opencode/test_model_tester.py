#!/usr/bin/env python3
"""Unit tests for model-tester.py"""

from pathlib import Path

# Import module with hyphen in filename
import importlib.util
spec = importlib.util.spec_from_file_location("model_tester", Path(__file__).parent / "model-tester.py")
model_tester = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model_tester)

ModelConfig = model_tester.ModelConfig
ModelTestResults = model_tester.ModelTestResults
TestResult = model_tester.TestResult
extract_configured_models = model_tester.extract_configured_models
load_opencode_config = model_tester.load_opencode_config
test_model = model_tester.test_model


def test_model_config():
    """Test ModelConfig creation"""
    config = ModelConfig(
        provider="google",
        model_id="gemini-2.5-flash",
        name="Gemini 2.5 Flash",
    )
    assert config.provider == "google"
    assert config.model_id == "gemini-2.5-flash"
    assert config.name == "Gemini 2.5 Flash"
    print("✓ ModelConfig test passed")


def test_test_result():
    """Test TestResult creation"""
    result = TestResult(
        model_id="google/gemini-2.5-flash",
        working=True,
        assistant_message="WORKING",
        test_datetime="2026-02-28T12:00:00Z",
    )
    assert result.working is True
    assert result.assistant_message == "WORKING"
    assert result.error is None
    print("✓ TestResult test passed")


def test_model_test_results():
    """Test ModelTestResults container"""
    results = ModelTestResults(
        last_update_date="2026-02-28T12:00:00Z",
        models=[
            TestResult(
                model_id="google/gemini-2.5-flash",
                working=True,
                assistant_message="WORKING",
                test_datetime="2026-02-28T12:00:00Z",
            ),
            TestResult(
                model_id="openai/gpt-5.1",
                working=False,
                assistant_message=None,
                test_datetime="2026-02-28T12:00:01Z",
                error="Timeout after 20s",
            ),
        ],
    )
    assert len(results.models) == 2
    assert results.models[0].working is True
    assert results.models[1].working is False

    yaml_output = results.to_yaml()
    assert "last_update_date" in yaml_output
    assert "google/gemini-2.5-flash" in yaml_output
    print("✓ ModelTestResults test passed")
    print(f"  YAML output preview:\n{yaml_output[:200]}...")


def test_load_config():
    """Test loading opencode.json"""
    config = load_opencode_config(Path("opencode.json"))
    assert "provider" in config
    assert "google" in config["provider"]
    print(f"✓ Config loaded: {len(config['provider'])} providers")


def test_extract_models():
    """Test model extraction from config"""
    config = load_opencode_config(Path("opencode.json"))
    models = extract_configured_models(config)
    assert len(models) > 0
    print(f"✓ Extracted {len(models)} configured models")
    for m in models[:3]:
        print(f"  - {m.provider}/{m.model_id}")


def test_single_model():
    """Test a single model (integration test)"""
    config = load_opencode_config(Path("opencode.json"))
    models = extract_configured_models(config)

    if not models:
        print("✗ No models configured")
        return

    # Test first model only
    test_model_config = models[0]
    print(f"\nTesting: {test_model_config.provider}/{test_model_config.model_id}")
    result = test_model(test_model_config, timeout=20)

    print(f"  Working: {result.working}")
    print(f"  Error: {result.error}")
    if result.assistant_message:
        print(f"  Response: {result.assistant_message[:100]}")
    print("✓ Single model test completed")


if __name__ == "__main__":
    print("Running unit tests...\n")

    test_model_config()
    test_test_result()
    test_model_test_results()
    test_load_config()
    test_extract_models()

    print("\nRunning integration test (single model)...\n")
    test_single_model()

    print("\n✓ All tests passed")
