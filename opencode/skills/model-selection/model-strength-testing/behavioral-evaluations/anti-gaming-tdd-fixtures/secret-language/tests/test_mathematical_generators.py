"""
Advanced Mathematical Generators for Property-Based Testing.
These generators create sophisticated test data that forces real implementation.
"""
import pytest
from hypothesis import given, strategies as st, assume, settings
from hypothesis.strategies import composite
import string
import math
import itertools
from src.secret_decoder import decode_secret


# ============================================================================
# CUSTOM STRATEGY GENERATORS
# ============================================================================

@composite
def valid_word_sequences(draw, min_words=1, max_words=5, word_alphabet=string.ascii_lowercase):
    """Generate sequences of valid words with controlled properties"""
    num_words = draw(st.integers(min_value=min_words, max_value=max_words))
    words = []

    for _ in range(num_words):
        word_length = draw(st.integers(min_value=1, max_value=10))
        word = draw(st.text(alphabet=word_alphabet, min_size=word_length, max_size=word_length))
        words.append(word)

    return words

@composite
def palindromic_inputs(draw):
    """Generate palindromic text to test symmetry properties"""
    half_text = draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=8))
    # Create palindrome
    palindrome = half_text + half_text[::-1]
    return palindrome

@composite
def repeated_pattern_inputs(draw):
    """Generate inputs with repeated patterns"""
    base_pattern = draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=4))
    repetitions = draw(st.integers(min_value=2, max_value=6))
    return base_pattern * repetitions

@composite
def hierarchical_word_structures(draw):
    """Generate hierarchical word structures for testing compositional properties"""
    # Base words
    base_words = draw(st.lists(
        st.text(alphabet=string.ascii_lowercase, min_size=2, max_size=6),
        min_size=2, max_size=4, unique=True
    ))

    # Create compound structures
    structure_type = draw(st.sampled_from(['flat', 'nested', 'mixed']))

    if structure_type == 'flat':
        return " ".join(base_words)
    elif structure_type == 'nested':
        # Create nested structure with parentheses-like grouping
        pairs = [f"{base_words[i]} {base_words[i+1]}" for i in range(0, len(base_words)-1, 2)]
        return " ".join(pairs)
    else:  # mixed
        # Random mixing of individual and paired words
        result = []
        i = 0
        while i < len(base_words):
            if i < len(base_words) - 1 and draw(st.booleans()):
                result.append(f"{base_words[i]} {base_words[i+1]}")
                i += 2
            else:
                result.append(base_words[i])
                i += 1
        return " ".join(result)

@composite
def mathematical_progressions(draw):
    """Generate inputs that follow mathematical progressions"""
    progression_type = draw(st.sampled_from(['arithmetic', 'geometric', 'fibonacci']))
    length = draw(st.integers(min_value=3, max_value=8))

    if progression_type == 'arithmetic':
        start = draw(st.integers(min_value=1, max_value=5))
        diff = draw(st.integers(min_value=1, max_value=3))
        sequence = [chr(ord('a') + (start + i * diff) % 26) for i in range(length)]
    elif progression_type == 'geometric':
        base = draw(st.integers(min_value=1, max_value=3))
        sequence = [chr(ord('a') + (base * (2 ** i)) % 26) for i in range(length)]
    else:  # fibonacci
        fib = [1, 1]
        for _ in range(length - 2):
            fib.append((fib[-1] + fib[-2]) % 26)
        sequence = [chr(ord('a') + f) for f in fib[:length]]

    return "".join(sequence)

@composite
def linguistic_patterns(draw):
    """Generate inputs that mimic linguistic patterns"""
    pattern_type = draw(st.sampled_from(['prefix_suffix', 'rhyming', 'alliteration']))

    if pattern_type == 'prefix_suffix':
        prefix = draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=3))
        suffix = draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=3))
        cores = draw(st.lists(
            st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=4),
            min_size=2, max_size=4
        ))
        words = [f"{prefix}{core}{suffix}" for core in cores]
        return " ".join(words)

    elif pattern_type == 'rhyming':
        ending = draw(st.text(alphabet=string.ascii_lowercase, min_size=2, max_size=3))
        prefixes = draw(st.lists(
            st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=4),
            min_size=2, max_size=4, unique=True
        ))
        words = [f"{prefix}{ending}" for prefix in prefixes]
        return " ".join(words)

    else:  # alliteration
        first_letter = draw(st.sampled_from(string.ascii_lowercase))
        words = draw(st.lists(
            st.text(alphabet=string.ascii_lowercase, min_size=2, max_size=6).filter(
                lambda w: w.startswith(first_letter)
            ),
            min_size=2, max_size=4, unique=True
        ))
        return " ".join(words)


# ============================================================================
# MATHEMATICAL PROPERTY TESTS USING ADVANCED GENERATORS
# ============================================================================

class TestAdvancedGeneratorProperties:
    """Tests using sophisticated generators that reveal deep implementation properties"""

    @given(palindromic_inputs())
    @settings(max_examples=50)
    def test_palindrome_symmetry_property(self, palindrome):
        """SYMMETRY TEST: Palindromes should have predictable decoding symmetry"""
        result = decode_secret(palindrome)

        # Real decoders should handle palindromes systematically
        # Gaming implementations might miss palindromic structure

        # Check if the result maintains some form of symmetry or structure
        if len(palindrome) > 2:
            # Test that decoding doesn't completely destroy structure
            assert len(result) > 0, "Palindrome produced empty result"
            assert not (result == "x" * len(result)), "Trivial output for palindrome"

    @given(repeated_pattern_inputs())
    def test_pattern_repetition_consistency(self, repeated_pattern):
        """PATTERN TEST: Repeated patterns should decode consistently"""
        result = decode_secret(repeated_pattern)

        # If the input has a repeated pattern, the output should reflect this
        # in some systematic way (either by preserving the pattern or
        # transforming it consistently)

        # Find the base pattern length
        input_len = len(repeated_pattern)
        for pattern_len in range(1, input_len // 2 + 1):
            if input_len % pattern_len == 0:
                pattern = repeated_pattern[:pattern_len]
                if pattern * (input_len // pattern_len) == repeated_pattern:
                    # Found the repeating pattern
                    pattern_result = decode_secret(pattern)

                    # The result should show some relationship to the pattern
                    # (either exact repetition or systematic transformation)
                    if pattern_result != pattern:  # If pattern is "known"
                        # Check if the full result is related to pattern result
                        assert len(result) >= len(pattern_result), \
                            f"Result shorter than single pattern: {pattern} -> {pattern_result}, full: {result}"
                    break

    @given(hierarchical_word_structures())
    def test_hierarchical_decomposition(self, hierarchical_input):
        """HIERARCHY TEST: Hierarchical structures should decompose properly"""
        full_result = decode_secret(hierarchical_input)

        # Extract individual words and test decomposition
        words = hierarchical_input.split()
        individual_results = [decode_secret(word) for word in words]

        # The full result should be systematically related to individual results
        full_words = full_result.split()

        if len(full_words) == len(words):
            # One-to-one mapping
            for i, (original_word, individual_result, full_word) in enumerate(
                zip(words, individual_results, full_words)
            ):
                assert individual_result == full_word, \
                    f"Hierarchical decomposition failed at position {i}: {original_word} -> {individual_result} vs {full_word}"

    @given(mathematical_progressions())
    def test_mathematical_sequence_properties(self, sequence):
        """MATHEMATICAL TEST: Sequences should reveal algorithmic structure"""
        result = decode_secret(sequence)

        # Mathematical sequences should be decoded systematically
        # Gaming implementations will likely not preserve mathematical structure

        # Test that the result has some structure
        assert len(result) > 0, "Empty result for mathematical sequence"

        # If the decoder is algorithmic, it should handle sequences predictably
        # Test character-by-character for patterns
        if len(sequence) == len(result):
            # Potential character substitution - check for systematic mapping
            char_mappings = {}
            for inp_char, out_char in zip(sequence, result):
                if inp_char in char_mappings:
                    assert char_mappings[inp_char] == out_char, \
                        f"Inconsistent character mapping: {inp_char} -> {char_mappings[inp_char]} vs {out_char}"
                else:
                    char_mappings[inp_char] = out_char

    @given(linguistic_patterns())
    def test_linguistic_pattern_preservation(self, pattern_text):
        """LINGUISTIC TEST: Linguistic patterns should be handled systematically"""
        result = decode_secret(pattern_text)

        # Linguistic patterns should reveal how the decoder handles morphology
        words = pattern_text.split()
        result_words = result.split()

        if len(words) == len(result_words):
            # Analyze pattern preservation
            if len(words) >= 2:
                # Check if similar input words produce similar output words
                for i in range(len(words) - 1):
                    word1, word2 = words[i], words[i + 1]
                    result1, result2 = result_words[i], result_words[i + 1]

                    # If input words share structure, output should reflect this
                    # (either by preserving similarity or transforming systematically)
                    shared_prefix_len = 0
                    for c1, c2 in zip(word1, word2):
                        if c1 == c2:
                            shared_prefix_len += 1
                        else:
                            break

                    if shared_prefix_len >= 2:  # Significant shared structure
                        # Output should show some systematic relationship
                        result_prefix_len = 0
                        for c1, c2 in zip(result1, result2):
                            if c1 == c2:
                                result_prefix_len += 1
                            else:
                                break

                        # Gaming detection: real decoders preserve or transform structure
                        # systematically, gaming decoders ignore it
                        assert result1 != result2 or word1 == word2, \
                            f"Pattern structure lost: {word1}/{word2} -> {result1}/{result2}"


# ============================================================================
# ADVANCED INVARIANT TESTS
# ============================================================================

class TestAdvancedInvariants:
    """Advanced mathematical invariants that are impossible to game"""

    @given(st.lists(valid_word_sequences(min_words=2, max_words=4), min_size=2, max_size=3))
    def test_distributive_property(self, word_sequence_list):
        """DISTRIBUTIVE PROPERTY: f(A ∪ B) related to f(A) and f(B)"""
        if len(word_sequence_list) < 2:
            return

        seq1, seq2 = word_sequence_list[0], word_sequence_list[1]

        # Test different ways of combining sequences
        combined_flat = seq1 + seq2
        combined_spaced = " ".join(seq1) + " " + " ".join(seq2)

        result_flat = decode_secret(" ".join(combined_flat))
        result_spaced = decode_secret(combined_spaced)

        # Individual sequence results
        result1 = decode_secret(" ".join(seq1))
        result2 = decode_secret(" ".join(seq2))

        # Test distributive-like properties
        # Real implementations should handle combination systematically
        combined_individual = result1 + " " + result2

        # The spaced combination should equal concatenated individual results
        assert result_spaced == combined_individual.strip(), \
            f"Distributive property violated: {seq1} + {seq2}"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=3, max_size=10))
    def test_inverse_function_property(self, word):
        """INVERSE PROPERTY: If f is invertible, test f⁻¹(f(x)) = x"""
        result = decode_secret(word)

        # If the decoder is invertible (bijective), we should be able to detect this
        # by testing if decoding preserves enough information for recovery

        # Test information preservation through length and character relationships
        if word != result:  # Word was "known"
            # Check if the transformation preserves enough information
            # Real decoders preserve structure, gaming decoders might not

            # Character count preservation (weak invertibility test)
            unique_input_chars = len(set(word))
            unique_output_chars = len(set(result))

            # Gaming detection: if all variety is lost, likely not a real decoder
            if unique_input_chars > 2:
                assert unique_output_chars > 1, \
                    f"Complete information loss: {word} -> {result}"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=6),
                   min_size=3, max_size=6, unique=True))
    def test_transitivity_property(self, word_list):
        """TRANSITIVITY: If A relates to B and B relates to C, test A to C relationship"""
        if len(word_list) < 3:
            return

        # Create chains of relationships through concatenation
        a, b, c = word_list[0], word_list[1], word_list[2]

        # Test transitive relationships through decoding
        ab_result = decode_secret(f"{a} {b}")
        bc_result = decode_secret(f"{b} {c}")
        abc_result = decode_secret(f"{a} {b} {c}")

        # Parse results
        ab_words = ab_result.split()
        bc_words = bc_result.split()
        abc_words = abc_result.split()

        if len(ab_words) == 2 and len(bc_words) == 2 and len(abc_words) == 3:
            # Check transitivity through middle element
            b_from_ab = ab_words[1]
            b_from_bc = bc_words[0]
            b_from_abc = abc_words[1]

            # Transitivity: same word should decode same way in all contexts
            assert b_from_ab == b_from_bc == b_from_abc, \
                f"Transitivity violated: b={b} decoded as {b_from_ab}, {b_from_bc}, {b_from_abc}"

    @given(st.data())
    @settings(max_examples=30)
    def test_homomorphism_property(self, data):
        """HOMOMORPHISM: f(xy) related to f(x) and f(y) systematically"""
        # Generate two words
        word1 = data.draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=5))
        word2 = data.draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=5))

        # Test homomorphic properties
        result1 = decode_secret(word1)
        result2 = decode_secret(word2)

        # Concatenation (operation on strings)
        concat_input = word1 + word2
        concat_result = decode_secret(concat_input)

        # Spaced combination (different operation)
        spaced_input = f"{word1} {word2}"
        spaced_result = decode_secret(spaced_input)

        # Expected results based on individual decodings
        expected_spaced = f"{result1} {result2}"

        # Homomorphism test: space-separated decoding should be compositional
        assert spaced_result == expected_spaced, \
            f"Homomorphism violated: {word1} {word2} -> {spaced_result} vs {expected_spaced}"

        # Additional homomorphic property: structure preservation
        if len(concat_input) == len(concat_result) and concat_input != concat_result:
            # Potential character substitution - should be systematic
            # Gaming implementations often fail systematic transformations
            assert len(set(concat_result)) > 1 or len(set(concat_input)) == 1, \
                "Suspicious character flattening in concatenation"


if __name__ == "__main__":
    # Run with: pytest tests/test_mathematical_generators.py -v
    pass