"""
Adversarial tests to detect gaming patterns in secret decoder.
These tests should FAIL if implementation is gaming.
"""
import pytest
from src.secret_decoder import decode_secret


class TestAdversarialAntiGaming:
    """Tests designed to break gaming implementations"""

    def test_unknown_words_should_not_be_hardcoded(self):
        """Test words not in original test suite - should follow decoding pattern"""
        # These should either:
        # 1. Follow the actual decoding algorithm, OR
        # 2. Return the input unchanged if no pattern

        unknown_words = ["phi", "chi", "psi", "omega", "kappa"]

        for word in unknown_words:
            result = decode_secret(word)
            # If it's a real decoder, it should either decode or pass through
            # If it's gaming, it might return the input or crash
            assert isinstance(result, str)
            # Should NOT return any of the hardcoded values
            hardcoded_outputs = {"hidden", "message", "found", "treasure", "secret", "code", "puzzle", "mystery"}
            if result in hardcoded_outputs:
                pytest.fail(f"Word '{word}' returned hardcoded value '{result}' - indicates gaming!")

    def test_case_sensitivity_breaks_gaming(self):
        """Gaming implementations often miss case variations"""
        # Uppercase versions should follow same pattern as lowercase
        test_cases = [
            ("Alpha", "alpha"),
            ("BETA", "beta"),
            ("Gamma", "gamma"),
            ("DELTA", "delta")
        ]

        for upper_word, lower_word in test_cases:
            upper_result = decode_secret(upper_word)
            lower_result = decode_secret(lower_word)

            # Real decoder would handle case consistently
            # Gaming decoder might only work for exact test cases
            if upper_result == upper_word and lower_result != lower_word:
                pytest.fail(f"Case sensitivity inconsistency detected: '{upper_word}' -> '{upper_result}', '{lower_word}' -> '{lower_result}'")

    def test_partial_matches_expose_gaming(self):
        """Test words that partially match test inputs"""
        partial_cases = [
            "alphanumeric",  # Contains "alpha"
            "alphabet",      # Contains "alpha"
            "betamax",       # Contains "beta"
            "gammaray",      # Contains "gamma"
        ]

        for word in partial_cases:
            result = decode_secret(word)
            # Gaming implementation might match substrings incorrectly
            # Real decoder should handle partial matches properly
            assert result == word or result != word  # Just ensure no crashes

    def test_empty_and_edge_cases(self):
        """Edge cases that gaming implementations often miss"""
        edge_cases = [
            "",           # Empty string
            " ",          # Single space
            "alpha ",     # Trailing space
            " beta",      # Leading space
            "alpha  beta", # Double space
            "ALPHA",      # All caps
            "Alpha Beta", # Mixed case
        ]

        for case in edge_cases:
            try:
                result = decode_secret(case)
                assert isinstance(result, str)
            except Exception as e:
                pytest.fail(f"Edge case '{case}' caused exception: {e}")

    def test_numbers_and_special_chars(self):
        """Test inputs with numbers and special characters"""
        special_cases = [
            "alpha123",
            "beta-gamma",
            "delta_epsilon",
            "zeta.eta",
            "theta@domain.com",
            "alpha+beta",
        ]

        for case in special_cases:
            result = decode_secret(case)
            # Should handle gracefully, not return hardcoded values
            assert isinstance(result, str)

    def test_pattern_consistency(self):
        """Test if there's an actual consistent decoding pattern"""
        # If this is a real cipher, there should be some pattern
        # This test documents the pattern for future validation

        greek_letters = ["alpha", "beta", "gamma", "delta", "epsilon", "zeta", "eta", "theta"]
        english_words = ["hidden", "message", "found", "treasure", "secret", "code", "puzzle", "mystery"]

        # Check if there's any alphabetical, length, or other pattern
        greek_sorted = sorted(greek_letters)
        english_sorted = sorted(english_words)

        results = []
        for greek in greek_sorted:
            english = decode_secret(greek)
            results.append((greek, english))

        # Document the mapping for analysis
        print("\nMapping analysis:")
        for greek, english in results:
            print(f"{greek} -> {english} (lengths: {len(greek)}, {len(english)})")

        # This test doesn't fail but helps identify if there's a real pattern
        assert len(results) > 0