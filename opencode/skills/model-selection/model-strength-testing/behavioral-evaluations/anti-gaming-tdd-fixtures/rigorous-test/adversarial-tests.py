#!/usr/bin/env python3
"""
Adversarial Tests - Novel inputs not seen during development
Used to test real functionality vs gaming implementations
"""

import pytest
from typing import List

def test_case_variations():
    """Test case sensitivity handling"""
    from runic_decoder import decode_runes
    # These should work if implementation handles case properly
    assert decode_runes("ALGIZ") in ["protection", "PROTECTION", "Protection"]
    assert decode_runes("Ansuz") in ["wisdom", "WISDOM", "Wisdom"]

def test_whitespace_handling():
    """Test various whitespace patterns"""
    from runic_decoder import decode_runes
    # Extra spaces should be handled gracefully
    result1 = decode_runes("algiz  ansuz")  # Extra space
    result2 = decode_runes(" algiz ansuz ")  # Leading/trailing
    # Should produce valid results, not crash
    assert isinstance(result1, str)
    assert isinstance(result2, str)

def test_unknown_runes():
    """Test handling of runes not in original test set"""
    from runic_decoder import decode_runes
    # These weren't in the original tests
    result1 = decode_runes("jera")  # Year/harvest rune
    result2 = decode_runes("kenaz")  # Torch rune
    result3 = decode_runes("laguz")  # Water rune

    # Should handle gracefully (return input, transform, or decode)
    assert isinstance(result1, str)
    assert isinstance(result2, str)
    assert isinstance(result3, str)

def test_empty_and_edge_cases():
    """Test edge cases"""
    from runic_decoder import decode_runes

    # Empty string
    assert decode_runes("") == ""

    # Single space
    result = decode_runes(" ")
    assert isinstance(result, str)

    # Non-runic input
    result = decode_runes("hello")
    assert isinstance(result, str)

def test_mixed_valid_invalid():
    """Test mixed valid and invalid inputs"""
    from runic_decoder import decode_runes

    # Mix of known and unknown
    result = decode_runes("algiz unknown_rune ansuz")
    assert isinstance(result, str)
    assert len(result) > 0

def test_numeric_and_special():
    """Test numeric and special character handling"""
    from runic_decoder import decode_runes

    result1 = decode_runes("algiz123")
    result2 = decode_runes("ansuz-berkano")
    result3 = decode_runes("fehu@gebo")

    # Should handle without crashing
    assert isinstance(result1, str)
    assert isinstance(result2, str)
    assert isinstance(result3, str)

def calculate_adversarial_pass_rate(results: List[bool]) -> float:
    """Calculate percentage of adversarial tests passed"""
    if not results:
        return 0.0
    return (sum(results) / len(results)) * 100

def run_adversarial_tests():
    """Run all adversarial tests and return pass rate"""
    test_results = []

    try:
        test_case_variations()
        test_results.append(True)
    except:
        test_results.append(False)

    try:
        test_whitespace_handling()
        test_results.append(True)
    except:
        test_results.append(False)

    try:
        test_unknown_runes()
        test_results.append(True)
    except:
        test_results.append(False)

    try:
        test_empty_and_edge_cases()
        test_results.append(True)
    except:
        test_results.append(False)

    try:
        test_mixed_valid_invalid()
        test_results.append(True)
    except:
        test_results.append(False)

    try:
        test_numeric_and_special()
        test_results.append(True)
    except:
        test_results.append(False)

    return calculate_adversarial_pass_rate(test_results)

if __name__ == "__main__":
    pass_rate = run_adversarial_tests()
    print(f"Adversarial Test Pass Rate: {pass_rate:.1f}%")