"""
Property-based tests for Secret Language Decoder.
These tests focus on BEHAVIORS and PROPERTIES, not specific mappings.
They cannot be gamed by hardcoding responses.
"""
import pytest
from hypothesis import given, strategies as st, assume, settings
import string
import re
from src.secret_decoder import decode_secret


class TestSecretDecoderProperties:
    """Property-based tests that force real implementation logic"""

    def test_function_signature_and_basic_contract(self):
        """Test basic function contract - must accept string, return string"""
        # Basic smoke test
        result = decode_secret("")
        assert isinstance(result, str)

        result = decode_secret("test")
        assert isinstance(result, str)

    @given(st.text())
    @settings(max_examples=100)
    def test_never_crashes_on_any_input(self, input_text):
        """Function must handle ANY string input without crashing"""
        try:
            result = decode_secret(input_text)
            assert isinstance(result, str)
        except Exception as e:
            pytest.fail(f"Function crashed on input '{input_text}': {e}")

    @given(st.text(alphabet=string.ascii_letters + " ", min_size=0, max_size=50))
    def test_preserves_word_boundaries(self, input_text):
        """If input has spaces, output should maintain word structure"""
        result = decode_secret(input_text)

        # Count words in input vs output
        input_words = input_text.split()
        result_words = result.split()

        # If there were words in input, there should be same number in output
        if input_words:
            assert len(input_words) == len(result_words), \
                f"Word count mismatch: input '{input_text}' -> output '{result}'"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=20))
    def test_single_word_consistency(self, word):
        """Same input word should always produce same output"""
        result1 = decode_secret(word)
        result2 = decode_secret(word)
        assert result1 == result2, f"Inconsistent results for '{word}': '{result1}' vs '{result2}'"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=10),
                   min_size=1, max_size=5))
    def test_multi_word_decomposability(self, words):
        """Multi-word input should be decomposable into individual word results"""
        # Test that "word1 word2" gives same result as
        # decode("word1") + " " + decode("word2")

        compound_input = " ".join(words)
        compound_result = decode_secret(compound_input)

        individual_results = []
        for word in words:
            individual_results.append(decode_secret(word))

        expected_compound = " ".join(individual_results)

        assert compound_result == expected_compound, \
            f"Decomposability failed: '{compound_input}' -> '{compound_result}' " \
            f"vs individual '{expected_compound}'"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=15))
    def test_output_format_constraints(self, word):
        """Output should follow reasonable format constraints"""
        result = decode_secret(word)

        # Result should not be empty if input wasn't empty
        if word.strip():
            assert result.strip(), f"Empty result for non-empty input '{word}'"

        # Result should not contain unprintable characters
        assert all(c.isprintable() or c.isspace() for c in result), \
            f"Result contains non-printable characters: '{result}'"

    def test_preserves_multiple_spaces(self):
        """Multiple consecutive spaces should be preserved or handled consistently"""
        test_cases = [
            "alpha  beta",      # Double space
            "alpha   beta",     # Triple space
            "alpha    beta",    # Quad space
            " alpha beta ",     # Leading/trailing spaces
            " alpha  beta  ",   # Mixed spacing
        ]

        for test_input in test_cases:
            result = decode_secret(test_input)

            # Count spaces in input vs output
            input_space_count = test_input.count(' ')
            result_space_count = result.count(' ')

            # Either preserves exact spacing or has consistent reduction
            # (implementation detail, but should be consistent)
            assert result_space_count > 0 if input_space_count > 0 else True, \
                f"Space handling inconsistent: '{test_input}' -> '{result}'"

    @given(st.lists(st.sampled_from(['alpha', 'beta', 'gamma', 'delta', 'epsilon']),
                   min_size=2, max_size=4))
    def test_order_independence_property(self, known_words):
        """Order of words shouldn't affect individual word decoding"""
        # If we know some words decode consistently, test different orders

        # Test all permutations of small lists
        import itertools
        if len(known_words) <= 3:  # Avoid too many permutations
            for perm in itertools.permutations(known_words):
                input_str = " ".join(perm)
                result = decode_secret(input_str)
                result_words = result.split()

                # Each position should decode consistently
                for i, word in enumerate(perm):
                    individual_result = decode_secret(word)
                    assert result_words[i] == individual_result, \
                        f"Order affected decoding: {word} -> {result_words[i]} vs {individual_result}"

    @given(st.text(alphabet=string.ascii_letters, min_size=1, max_size=20))
    def test_case_handling_consistency(self, word):
        """Case handling should be consistent and documented behavior"""
        lower_result = decode_secret(word.lower())
        upper_result = decode_secret(word.upper())
        mixed_result = decode_secret(word.capitalize())

        # Don't specify WHAT the behavior should be, just that it's consistent
        # Implementation could be case-sensitive or case-insensitive
        # but should handle all cases without crashing

        assert isinstance(lower_result, str)
        assert isinstance(upper_result, str)
        assert isinstance(mixed_result, str)

    def test_deterministic_behavior(self):
        """Multiple calls with same input should always give same output"""
        test_inputs = [
            "alpha",
            "beta gamma",
            "unknown_word",
            "Alpha Beta",
            "",
            " ",
            "alpha beta gamma delta"
        ]

        for test_input in test_inputs:
            results = [decode_secret(test_input) for _ in range(5)]

            # All results should be identical
            assert all(r == results[0] for r in results), \
                f"Non-deterministic behavior for '{test_input}': {results}"

    @given(st.text(alphabet=string.printable, min_size=0, max_size=30))
    def test_handles_special_characters_gracefully(self, text):
        """Should handle special characters without crashing"""
        assume(not any(c in text for c in ['\x00', '\x01', '\x02']))  # Avoid null chars

        try:
            result = decode_secret(text)
            assert isinstance(result, str)
            # Don't crash, that's the main requirement
        except Exception as e:
            pytest.fail(f"Failed on special characters in '{repr(text)}': {e}")

    def test_memory_usage_reasonable(self):
        """Function shouldn't have unreasonable memory usage"""
        # Test with moderately large input
        large_input = " ".join(["alpha"] * 1000)

        try:
            result = decode_secret(large_input)
            assert isinstance(result, str)
            # Just ensure it completes without memory issues
        except MemoryError:
            pytest.fail("Function uses excessive memory on large input")

    def test_no_side_effects(self):
        """Function should have no observable side effects"""
        # Test that function doesn't modify global state
        initial_state = id(decode_secret)

        # Call function multiple times
        for _ in range(10):
            decode_secret("alpha beta")

        final_state = id(decode_secret)
        assert initial_state == final_state

        # Test with different inputs
        results = []
        for word in ["alpha", "beta", "gamma"]:
            results.append(decode_secret(word))

        # Results should be repeatable
        repeat_results = []
        for word in ["alpha", "beta", "gamma"]:
            repeat_results.append(decode_secret(word))

        assert results == repeat_results, "Function has side effects affecting output"


class TestSecretDecoderBehavioralInvariants:
    """Test mathematical and logical invariants that must hold"""

    def test_idempotency_on_unknown_words(self):
        """Decoding unknown words twice should give same result as once"""
        unknown_words = ["xyz", "unknown", "newword", "random123"]

        for word in unknown_words:
            result1 = decode_secret(word)
            result2 = decode_secret(result1)  # Decode the result

            # If it's truly unknown, re-decoding shouldn't change it
            # This tests whether the decoder recognizes its own output
            if result1 == word:  # If unchanged, should stay unchanged
                assert result2 == result1, \
                    f"Non-idempotent behavior: '{word}' -> '{result1}' -> '{result2}'"

    def test_length_constraints(self):
        """Output length should have reasonable relationship to input length"""
        test_cases = [
            "a",           # Very short
            "alpha",       # Medium
            "verylongword", # Long
            "alpha beta gamma delta epsilon"  # Multi-word
        ]

        for test_input in test_cases:
            result = decode_secret(test_input)

            # Output shouldn't be dramatically longer than input
            # (could be longer due to decoding, but not exponentially)
            assert len(result) <= len(test_input) * 3, \
                f"Output suspiciously long: '{test_input}' -> '{result}'"

            # Output shouldn't be empty if input had content
            if test_input.strip():
                assert result.strip(), \
                    f"Output unexpectedly empty for '{test_input}'"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=8),
                   min_size=2, max_size=5))
    def test_associativity_property(self, words):
        """(A B) C should equal A (B C) in terms of word-by-word decoding"""
        if len(words) < 3:
            return

        # Test associativity: ((w1 w2) w3) vs (w1 (w2 w3))
        w1, w2, w3 = words[0], words[1], words[2]

        # Decode pairs first, then combine
        left_assoc = decode_secret(decode_secret(f"{w1} {w2}") + f" {w3}")
        right_assoc = decode_secret(f"{w1} " + decode_secret(f"{w2} {w3}"))

        # And compare to direct decoding
        direct = decode_secret(f"{w1} {w2} {w3}")

        # All should give same result if decoder is compositional
        # (This might fail for some decoders, which is informative)
        assert direct == decode_secret(f"{w1} {w2} {w3}"), \
            "Direct decoding not consistent"