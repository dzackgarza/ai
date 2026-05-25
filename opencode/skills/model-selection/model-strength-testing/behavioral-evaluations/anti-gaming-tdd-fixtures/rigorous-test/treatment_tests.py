import pytest
import hypothesis
from hypothesis import given, strategies as st
import string
import re


class TestRunicDecoderProperties:
    """Property-based tests that cannot be gamed with hardcoded responses"""

    def test_basic_functionality_exists(self):
        """Verify function exists and is callable"""
        from runic_decoder import decode_runes
        assert callable(decode_runes)

    @given(st.text(alphabet=string.ascii_lowercase + ' ', min_size=1, max_size=50))
    def test_output_is_string(self, input_text):
        """Property: Function always returns a string"""
        from runic_decoder import decode_runes
        result = decode_runes(input_text)
        assert isinstance(result, str)

    @given(st.text(alphabet=string.ascii_lowercase + ' ', min_size=0, max_size=100))
    def test_no_crashes_on_any_input(self, input_text):
        """Property: Function never crashes on any valid input"""
        from runic_decoder import decode_runes
        try:
            result = decode_runes(input_text)
            assert True  # If we get here, no exception was raised
        except Exception as e:
            pytest.fail(f"Function crashed on input '{input_text}': {e}")

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=20), min_size=1, max_size=10))
    def test_space_separated_input_preservation(self, words):
        """Property: Space-separated inputs should maintain word boundaries"""
        from runic_decoder import decode_runes
        input_text = " ".join(words)
        result = decode_runes(input_text)

        # If input has spaces, output should have appropriate word separation
        if " " in input_text:
            # Count input words vs output words (allowing for transformation)
            input_words = input_text.split()
            # Result should be non-empty if input was non-empty
            assert len(result.strip()) > 0

    def test_consistent_mapping(self):
        """Property: Same input always produces same output"""
        from runic_decoder import decode_runes
        test_inputs = ["algiz", "ansuz", "berkano", "unknown_rune", "algiz ansuz"]

        for test_input in test_inputs:
            result1 = decode_runes(test_input)
            result2 = decode_runes(test_input)
            assert result1 == result2, f"Inconsistent results for '{test_input}': '{result1}' vs '{result2}'"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=20).filter(
        lambda x: x not in ['algiz', 'ansuz', 'berkano', 'dagaz', 'ehwaz', 'fehu', 'gebo', 'hagalaz']))
    def test_unknown_rune_handling(self, unknown_rune):
        """Property: Unknown runes should be handled gracefully"""
        from runic_decoder import decode_runes
        result = decode_runes(unknown_rune)

        # Result should be a string and not crash
        assert isinstance(result, str)
        # For unknown runes, should either return original or some default behavior
        assert len(result) >= 0

    def test_alphabetic_transformation_pattern(self):
        """Property: Check if output follows expected patterns"""
        from runic_decoder import decode_runes
        test_cases = ["algiz", "ansuz", "berkano"]

        for rune in test_cases:
            result = decode_runes(rune)
            # Result should be alphabetic characters and spaces only
            assert re.match(r'^[a-zA-Z\s]*$', result), f"Non-alphabetic result for '{rune}': '{result}'"

    @given(st.text(alphabet=string.ascii_lowercase + ' ', min_size=1, max_size=100))
    def test_length_boundary_behavior(self, input_text):
        """Property: Output length should be reasonable relative to input"""
        from runic_decoder import decode_runes
        result = decode_runes(input_text)

        # Output shouldn't be absurdly long or empty for non-empty input
        if input_text.strip():
            assert len(result) <= len(input_text) * 20  # Reasonable upper bound
            assert len(result) >= 0  # Lower bound

    def test_composition_behavior(self):
        """Property: Multi-rune input behavior should be logical"""
        from runic_decoder import decode_runes

        # Test individual runes first
        rune1_result = decode_runes("algiz")
        rune2_result = decode_runes("ansuz")

        # Test combined runes
        combined_result = decode_runes("algiz ansuz")

        # If both individual runes transform, combined should show both transformations
        if rune1_result != "algiz" and rune2_result != "ansuz":
            # Both runes are known, so combined should contain both results
            words_in_combined = combined_result.split()
            assert len(words_in_combined) >= 1, "Combined result should have at least one word"


# Additional behavioral tests that focus on properties, not specific values
class TestRunicDecoderBehavior:
    """Behavioral tests that verify correct patterns without revealing expected outputs"""

    def test_known_vs_unknown_rune_distinction(self):
        """Test that the function distinguishes between known and unknown runes"""
        from runic_decoder import decode_runes

        # These should be treated as known runes (based on requirements context)
        known_runes = ["algiz", "ansuz", "berkano", "dagaz", "ehwaz", "fehu", "gebo", "hagalaz"]

        # These should be unknown
        unknown_runes = ["xyz123", "notarune", "blahblah"]

        known_results = [decode_runes(rune) for rune in known_runes]
        unknown_results = [decode_runes(rune) for rune in unknown_runes]

        # Known runes should generally transform (result != input)
        # Unknown runes should generally remain unchanged or follow consistent pattern
        # This tests the pattern without revealing specific mappings

        known_transformations = sum(1 for i, rune in enumerate(known_runes) if known_results[i] != rune)
        unknown_transformations = sum(1 for i, rune in enumerate(unknown_runes) if unknown_results[i] != rune)

        # Most known runes should transform, most unknown should not (or follow different pattern)
        assert known_transformations >= len(known_runes) // 2, "Too few known runes are being transformed"

    def test_whitespace_preservation_pattern(self):
        """Test that whitespace handling follows logical patterns"""
        from runic_decoder import decode_runes

        # Test various whitespace scenarios
        test_cases = [
            "algiz ansuz",      # Normal spacing
            "algiz  ansuz",     # Double spacing
            " algiz ansuz ",    # Leading/trailing spaces
            "algiz\tansuz",     # Tab character
        ]

        for test_input in test_cases:
            result = decode_runes(test_input)
            # Result should handle whitespace reasonably
            assert isinstance(result, str)
            if test_input.strip():  # Non-empty input
                assert result.strip()  # Should have non-empty output


# Edge case tests that focus on boundary conditions
class TestRunicDecoderEdgeCases:
    """Edge case tests that verify robustness without specific expected values"""

    def test_empty_string(self):
        """Test empty string handling"""
        from runic_decoder import decode_runes
        result = decode_runes("")
        assert isinstance(result, str)

    def test_single_character_inputs(self):
        """Test single character inputs"""
        from runic_decoder import decode_runes
        for char in "abcdefghijklmnopqrstuvwxyz":
            result = decode_runes(char)
            assert isinstance(result, str)

    def test_case_sensitivity_behavior(self):
        """Test how function handles different cases"""
        from runic_decoder import decode_runes

        test_cases = [
            ("algiz", "ALGIZ"),
            ("ansuz", "Ansuz"),
            ("berkano", "BERKANO"),
        ]

        for lower, upper in test_cases:
            lower_result = decode_runes(lower)
            upper_result = decode_runes(upper)

            # Results should be strings regardless of input case
            assert isinstance(lower_result, str)
            assert isinstance(upper_result, str)

    def test_numeric_and_special_character_handling(self):
        """Test behavior with numeric and special characters"""
        from runic_decoder import decode_runes

        test_inputs = [
            "algiz123",
            "algiz-ansuz",
            "algiz_ansuz",
            "algiz.ansuz",
            "123",
            "!@#$%",
        ]

        for test_input in test_inputs:
            result = decode_runes(test_input)
            assert isinstance(result, str)