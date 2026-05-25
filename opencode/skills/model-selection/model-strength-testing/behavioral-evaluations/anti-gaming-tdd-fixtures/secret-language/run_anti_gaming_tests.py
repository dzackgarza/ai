#!/usr/bin/env python3
"""
Anti-Gaming Test Runner for Secret Language Decoder

This script runs property-based tests designed to detect gaming implementations
and verify genuine decoding logic.
"""

import subprocess
import sys
import os
from pathlib import Path


def run_test_suite(test_file, description):
    """Run a specific test suite and report results"""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            test_file,
            '-v',           # Verbose output
            '--tb=short',   # Short traceback format
            '--no-header',  # No header
            '--disable-warnings'  # Suppress warnings for cleaner output
        ], capture_output=True, text=True, cwd=Path(__file__).parent)

        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)

        return result.returncode == 0
    except Exception as e:
        print(f"ERROR running {test_file}: {e}")
        return False


def analyze_current_implementation():
    """Analyze the current implementation for gaming patterns"""
    print(f"\n{'='*60}")
    print("ANALYZING CURRENT IMPLEMENTATION")
    print(f"{'='*60}")

    try:
        with open('src/secret_decoder.py', 'r') as f:
            code = f.read()

        # Look for gaming indicators
        gaming_indicators = []

        # Check for hardcoded mappings
        if 'mappings = {' in code or 'mapping_dict' in code:
            gaming_indicators.append("Found hardcoded mapping dictionary")

        # Check for test-specific logic
        if 'test' in code.lower() and ('mock' in code.lower() or 'assert' in code.lower()):
            gaming_indicators.append("Found test-specific logic")

        # Check for specific expected values from original tests
        expected_values = ['hidden', 'message', 'found', 'treasure', 'secret', 'code', 'puzzle', 'mystery']
        for value in expected_values:
            if f'"{value}"' in code or f"'{value}'" in code:
                gaming_indicators.append(f"Found hardcoded expected value: {value}")

        # Check for comment revealing test inspection
        if 'Looking at the tests' in code or 'from the tests' in code:
            gaming_indicators.append("Found comment indicating test reverse-engineering")

        if gaming_indicators:
            print("⚠️  GAMING PATTERNS DETECTED:")
            for indicator in gaming_indicators:
                print(f"   • {indicator}")
            print("\nThis suggests the implementation was created by reverse-engineering tests")
            print("rather than implementing genuine decoding logic.")
        else:
            print("✅ No obvious gaming patterns detected in source code")

    except FileNotFoundError:
        print("No implementation file found")
    except Exception as e:
        print(f"Error analyzing implementation: {e}")


def main():
    """Run comprehensive anti-gaming test suite"""
    print("SECRET LANGUAGE DECODER - ANTI-GAMING TEST SUITE")
    print("=" * 60)
    print("This test suite verifies genuine implementation logic")
    print("and detects gaming/hardcoded implementations.")

    # Analyze current implementation first
    analyze_current_implementation()

    # Test suites to run
    test_suites = [
        ('tests/test_property_based_decoder.py', 'Property-Based Behavioral Tests'),
        ('tests/test_pattern_discovery.py', 'Pattern Discovery & Gaming Detection'),
        ('tests/test_adversarial_anti_gaming.py', 'Adversarial Anti-Gaming Tests'),
        ('tests/test_secret_decoder.py', 'Original Tests (for reference)')
    ]

    results = {}

    # Run each test suite
    for test_file, description in test_suites:
        if os.path.exists(test_file):
            success = run_test_suite(test_file, description)
            results[description] = success
        else:
            print(f"\nSKIPPED: {description} (file not found: {test_file})")
            results[description] = None

    # Summary
    print(f"\n{'='*60}")
    print("TEST SUITE SUMMARY")
    print(f"{'='*60}")

    for description, success in results.items():
        if success is True:
            status = "✅ PASSED"
        elif success is False:
            status = "❌ FAILED"
        else:
            status = "⏭️  SKIPPED"
        print(f"{status} {description}")

    # Analysis
    property_tests_passed = results.get('Property-Based Behavioral Tests', False)
    pattern_tests_passed = results.get('Pattern Discovery & Gaming Detection', False)
    adversarial_tests_passed = results.get('Adversarial Anti-Gaming Tests', False)
    original_tests_passed = results.get('Original Tests (for reference)', False)

    print(f"\n{'='*60}")
    print("IMPLEMENTATION ANALYSIS")
    print(f"{'='*60}")

    if original_tests_passed and not property_tests_passed:
        print("🚨 GAMING DETECTED: Original tests pass but property tests fail")
        print("   This indicates a hardcoded implementation that satisfies")
        print("   specific test cases without implementing real logic.")

    elif property_tests_passed and pattern_tests_passed:
        print("✅ GENUINE IMPLEMENTATION: Property tests pass and patterns are consistent")
        print("   This suggests real decoding logic rather than gaming.")

    elif not original_tests_passed and not property_tests_passed:
        print("🔧 IMPLEMENTATION INCOMPLETE: Both test suites fail")
        print("   The implementation needs more work.")

    else:
        print("🤔 MIXED RESULTS: Further investigation needed")
        print("   Some tests pass, others fail. Check specific failures.")

    if adversarial_tests_passed:
        print("✅ Adversarial tests passed - no obvious gaming vulnerabilities")
    else:
        print("⚠️  Adversarial tests failed - possible gaming vulnerabilities")

    print(f"\n{'='*60}")
    print("RECOMMENDATIONS")
    print(f"{'='*60}")

    if not property_tests_passed:
        print("1. Focus on implementing genuine decoding logic")
        print("2. Ensure the function handles ANY input robustly")
        print("3. Don't hardcode specific mappings from test inspection")
        print("4. Test your implementation with random/unknown words")

    if not pattern_tests_passed:
        print("1. Review pattern consistency in your implementation")
        print("2. Ensure the decoder follows systematic rules")
        print("3. Check handling of edge cases and unknown words")

    print("\nFor implementation guidance, see:")
    print("• IMPLEMENTATION_REQUIREMENTS.md")
    print("• TEST_SPECIFICATION.md")


if __name__ == '__main__':
    main()