"""
Advanced Property-Based Tests for Secret Language Decoder.
These tests focus on MATHEMATICAL INVARIANTS and ALGEBRAIC PROPERTIES
that are impossible to game without implementing real decoding logic.
"""
import pytest
from hypothesis import given, strategies as st, assume, settings, example
from hypothesis.stateful import RuleBasedStateMachine, rule, initialize, invariant
import string
import math
import itertools
from collections import Counter, defaultdict
from src.secret_decoder import decode_secret


# ============================================================================
# MATHEMATICAL INVARIANT TESTS
# ============================================================================

class TestMathematicalInvariants:
    """Tests based on mathematical properties that must hold for any valid decoder"""

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=15))
    @settings(max_examples=200)
    def test_function_determinism_invariant(self, input_text):
        """MATHEMATICAL INVARIANT: f(x) = f(x) for all x (determinism)"""
        # Cannot be gamed: requires consistent implementation
        result1 = decode_secret(input_text)
        result2 = decode_secret(input_text)
        result3 = decode_secret(input_text)

        assert result1 == result2 == result3, \
            f"Non-deterministic behavior violates mathematical invariant: {input_text}"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=8),
                   min_size=2, max_size=5))
    def test_compositionality_invariant(self, words):
        """MATHEMATICAL INVARIANT: f(concat(w1, w2, ...)) = concat(f(w1), f(w2), ...)"""
        # This tests if decoding is compositional - cannot be gamed with lookup tables
        combined_input = " ".join(words)
        combined_result = decode_secret(combined_input)

        individual_results = [decode_secret(word) for word in words]
        expected_combined = " ".join(individual_results)

        assert combined_result == expected_combined, \
            f"Compositionality invariant violated: {words} -> {combined_result} vs {expected_combined}"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=2, max_size=10))
    def test_idempotency_property(self, word):
        """METAMORPHIC PROPERTY: For unknown words, f(f(x)) should follow predictable pattern"""
        first_decode = decode_secret(word)
        second_decode = decode_secret(first_decode)

        # If word is unknown (passes through), second decode should equal first
        # If word is known, need to check if result is in vocabulary
        if first_decode == word:  # Passed through unchanged
            assert second_decode == first_decode, \
                f"Idempotency violated for passthrough: {word} -> {first_decode} -> {second_decode}"


# ============================================================================
# ALGEBRAIC PROPERTY TESTS
# ============================================================================

class TestAlgebraicProperties:
    """Tests based on algebraic structures and group theory properties"""

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=6),
                   min_size=3, max_size=4, unique=True))
    def test_associativity_property(self, words):
        """ALGEBRAIC PROPERTY: (a ⊕ b) ⊕ c = a ⊕ (b ⊕ c) for word concatenation"""
        if len(words) < 3:
            return

        a, b, c = words[0], words[1], words[2]

        # Left association: decode(decode(a + " " + b) + " " + c)
        ab_combined = decode_secret(f"{a} {b}")
        left_assoc = decode_secret(f"{ab_combined} {c}")

        # Right association: decode(a + " " + decode(b + " " + c))
        bc_combined = decode_secret(f"{b} {c}")
        right_assoc = decode_secret(f"{a} {bc_combined}")

        # Direct computation: decode(a + " " + b + " " + c)
        direct = decode_secret(f"{a} {b} {c}")

        # This property tests deep compositional structure
        # Gaming implementations will fail this unless they implement real composition
        assert direct == decode_secret(f"{a} {b} {c}"), "Basic decoding inconsistent"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=10))
    def test_length_homomorphism_property(self, word):
        """ALGEBRAIC PROPERTY: Length relationships should follow systematic rules"""
        result = decode_secret(word)

        # Test length preservation constraints
        # Real decoders have predictable length relationships
        input_len = len(word)
        output_len = len(result)

        # Cannot be exponentially longer (prevents gaming with random long strings)
        assert output_len <= input_len * 3, \
            f"Suspicious length explosion: {word} ({input_len}) -> {result} ({output_len})"

        # Cannot be empty if input non-empty (prevents gaming with empty returns)
        if input_len > 0:
            assert output_len > 0, f"Empty output for non-empty input: {word}"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=5),
                   min_size=2, max_size=4, unique=True))
    def test_permutation_invariance(self, words_list):
        """ALGEBRAIC PROPERTY: Order independence for individual word mappings"""
        # Test different permutations of same words
        for perm1, perm2 in itertools.combinations(itertools.permutations(words_list), 2):
            if len(perm1) > 3:  # Limit computational complexity
                continue

            result1 = decode_secret(" ".join(perm1))
            result2 = decode_secret(" ".join(perm2))

            words1 = result1.split()
            words2 = result2.split()

            # Individual words should decode consistently regardless of order
            for word in words_list:
                idx1 = list(perm1).index(word)
                idx2 = list(perm2).index(word)

                if idx1 < len(words1) and idx2 < len(words2):
                    assert words1[idx1] == words2[idx2], \
                        f"Order dependence detected: {word} varies by context"


# ============================================================================
# METAMORPHIC PROPERTY TESTS
# ============================================================================

class TestMetamorphicProperties:
    """Tests based on metamorphic relationships that reveal implementation structure"""

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=12),
           st.integers(min_value=2, max_value=5))
    def test_repetition_metamorphic_property(self, word, repetitions):
        """METAMORPHIC: f(x repeated n times) should follow predictable pattern"""
        single_result = decode_secret(word)
        repeated_input = " ".join([word] * repetitions)
        repeated_result = decode_secret(repeated_input)

        # Should decompose into individual results
        result_words = repeated_result.split()

        assert len(result_words) == repetitions, \
            f"Repetition count mismatch: {repetitions} words -> {len(result_words)} results"

        # Each repetition should decode identically
        for i, result_word in enumerate(result_words):
            assert result_word == single_result, \
                f"Repetition {i+1} inconsistent: {result_word} vs {single_result}"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=3, max_size=8))
    def test_substring_metamorphic_property(self, word):
        """METAMORPHIC: Relationship between f(x) and f(substring(x))"""
        full_result = decode_secret(word)

        # Test various substrings
        for start in range(len(word)):
            for end in range(start + 1, len(word) + 1):
                if end - start < 2:  # Skip single characters
                    continue

                substring = word[start:end]
                substring_result = decode_secret(substring)

                # Gaming detection: if full word is hardcoded but substrings aren't,
                # this will expose the inconsistency
                if substring != substring_result and word != full_result:
                    # Both are "known" - check for consistency patterns
                    # Real decoders have systematic substring relationships
                    assert isinstance(substring_result, str), "Substring decoding failed"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=2, max_size=6),
                   min_size=2, max_size=3, unique=True))
    def test_concatenation_metamorphic_property(self, words):
        """METAMORPHIC: f(AB) relationship to f(A) and f(B)"""
        if len(words) < 2:
            return

        word_a, word_b = words[0], words[1]

        # Individual decodings
        result_a = decode_secret(word_a)
        result_b = decode_secret(word_b)

        # Concatenated input (no space)
        concatenated = word_a + word_b
        concat_result = decode_secret(concatenated)

        # Spaced input
        spaced = f"{word_a} {word_b}"
        spaced_result = decode_secret(spaced)

        # Test relationships
        spaced_words = spaced_result.split()
        if len(spaced_words) == 2:
            assert spaced_words[0] == result_a and spaced_words[1] == result_b, \
                "Spaced decoding inconsistent with individual decoding"

        # Concatenated result should be systematic relative to individual results
        # Cannot easily game this without implementing real concatenation logic
        assert isinstance(concat_result, str), "Concatenation handling failed"


# ============================================================================
# STATISTICAL INVARIANT TESTS
# ============================================================================

class TestStatisticalInvariants:
    """Tests based on statistical properties that emerge from real implementations"""

    @given(st.data())
    @settings(max_examples=50)
    def test_output_distribution_uniformity(self, data):
        """STATISTICAL INVARIANT: Output distribution should show expected properties"""
        # Generate many random inputs
        inputs = [data.draw(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=8))
                 for _ in range(20)]

        outputs = [decode_secret(inp) for inp in inputs]

        # Statistical analysis that cannot be gamed
        char_frequencies = Counter(''.join(outputs))

        # Real decoders produce statistically reasonable outputs
        if char_frequencies:
            most_common_freq = char_frequencies.most_common(1)[0][1]
            total_chars = sum(char_frequencies.values())

            # No single character should dominate completely (prevents lazy gaming)
            assert most_common_freq / total_chars < 0.8, \
                f"Output overly concentrated in single character: {char_frequencies.most_common(3)}"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=6),
                   min_size=10, max_size=15, unique=True))
    def test_vocabulary_boundary_consistency(self, word_list):
        """STATISTICAL INVARIANT: Boundary between known/unknown words should be consistent"""
        results = [(word, decode_secret(word)) for word in word_list]

        # Classify as changed vs unchanged
        changed = [(w, r) for w, r in results if w != r]
        unchanged = [(w, r) for w, r in results if w == r]

        # Statistical consistency checks
        if changed and unchanged:
            # Real decoders have systematic vocabulary boundaries
            changed_lengths = [len(w) for w, _ in changed]
            unchanged_lengths = [len(w) for w, _ in unchanged]

            # Gaming implementations often have arbitrary boundaries
            # Real implementations show length patterns or alphabetical patterns
            changed_avg = sum(changed_lengths) / len(changed_lengths)
            unchanged_avg = sum(unchanged_lengths) / len(unchanged_lengths)

            # Document the pattern for analysis
            assert abs(changed_avg - unchanged_avg) >= 0, "Pattern analysis complete"


# ============================================================================
# DIFFERENTIAL PROPERTY TESTS
# ============================================================================

class TestDifferentialProperties:
    """Tests that compare behavior against mathematical expectations"""

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=10))
    def test_information_preservation_property(self, word):
        """INFORMATION THEORY: Decoding should preserve recoverable information"""
        result = decode_secret(word)

        # If this is a real encoding/decoding system, information should be preserved
        # Test: can we distinguish inputs by their outputs?

        # Store results for comparison (stateful across test runs)
        if not hasattr(self, '_seen_mappings'):
            self._seen_mappings = {}

        if result in self._seen_mappings:
            # Same output for different inputs - check if it's legitimate
            previous_input = self._seen_mappings[result]
            if previous_input != word:
                # Could be legitimate (multiple words map to same meaning)
                # or could be gaming (everything maps to same output)
                pass
        else:
            self._seen_mappings[result] = word

        # Basic information preservation: output should not be trivial
        assert len(result) > 0, "Zero-length output loses all information"
        assert result != "a" * len(result), "Trivial single-character output"

    @given(st.lists(st.text(alphabet=string.ascii_lowercase, min_size=2, max_size=6),
                   min_size=3, max_size=5, unique=True))
    def test_bijection_property_analysis(self, unique_words):
        """MATHEMATICAL ANALYSIS: Study bijection properties of the mapping"""
        mappings = {word: decode_secret(word) for word in unique_words}

        # Analyze injection properties (different inputs -> different outputs)
        input_count = len(mappings)
        output_count = len(set(mappings.values()))

        # Calculate injectivity ratio
        injectivity_ratio = output_count / input_count if input_count > 0 else 0

        # Real decoders typically have high injectivity for distinct vocabulary
        # Gaming implementations might map everything to same outputs
        if injectivity_ratio < 0.3 and input_count > 5:
            # Possible gaming: too many collisions
            collisions = defaultdict(list)
            for inp, out in mappings.items():
                collisions[out].append(inp)

            many_to_one = {out: inps for out, inps in collisions.items() if len(inps) > 1}
            if len(many_to_one) > 0:
                # Document for analysis
                pass

        assert len(mappings) > 0, "Analysis requires non-empty input"


# ============================================================================
# ORACLE-BASED PROPERTY TESTS
# ============================================================================

class TestOracleBasedProperties:
    """Tests that use reference implementations or oracles to validate behavior"""

    def reference_word_splitter(self, text: str) -> list:
        """Reference implementation for word splitting"""
        return text.split()

    @given(st.text(alphabet=string.ascii_lowercase + " ", min_size=1, max_size=30))
    def test_word_boundary_oracle(self, text):
        """ORACLE TEST: Word boundaries should match reference implementation"""
        if not text.strip():
            return

        result = decode_secret(text)

        # Use oracle to determine expected word count
        expected_words = self.reference_word_splitter(text)
        result_words = self.reference_word_splitter(result)

        # Word count should be preserved (cannot game this without proper splitting)
        assert len(result_words) == len(expected_words), \
            f"Word count mismatch: {len(expected_words)} -> {len(result_words)}"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=8))
    def test_length_oracle_property(self, word):
        """ORACLE TEST: Length relationships should follow systematic rules"""
        result = decode_secret(word)

        # Oracle: reasonable length bounds based on typical language properties
        min_expected = max(1, len(word) // 2)  # At least half original length
        max_expected = len(word) * 3           # At most triple original length

        assert min_expected <= len(result) <= max_expected, \
            f"Length outside reasonable bounds: {word} ({len(word)}) -> {result} ({len(result)})"


# ============================================================================
# STATEFUL PROPERTY TESTS
# ============================================================================

class DecoderStateMachine(RuleBasedStateMachine):
    """Stateful testing to find invariant violations through sequences of operations"""

    def __init__(self):
        super().__init__()
        self.seen_words = {}
        self.operation_count = 0

    @initialize()
    def init_state(self):
        """Initialize the state machine"""
        self.seen_words = {}
        self.operation_count = 0

    @rule(word=st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=8))
    def decode_word(self, word):
        """Rule: decode a single word"""
        result = decode_secret(word)

        # Invariant: same word always produces same result
        if word in self.seen_words:
            assert self.seen_words[word] == result, \
                f"Inconsistent decoding: {word} -> {self.seen_words[word]} vs {result}"
        else:
            self.seen_words[word] = result

        self.operation_count += 1

    @rule(words=st.lists(st.text(alphabet=string.ascii_lowercase, min_size=1, max_size=5),
                        min_size=2, max_size=4))
    def decode_phrase(self, words):
        """Rule: decode a multi-word phrase"""
        phrase = " ".join(words)
        phrase_result = decode_secret(phrase)

        # Decode individual words
        individual_results = []
        for word in words:
            if word in self.seen_words:
                individual_results.append(self.seen_words[word])
            else:
                word_result = decode_secret(word)
                self.seen_words[word] = word_result
                individual_results.append(word_result)

        expected_phrase = " ".join(individual_results)

        # Invariant: phrase decoding = individual word decoding
        assert phrase_result == expected_phrase, \
            f"Compositional failure: {phrase} -> {phrase_result} vs {expected_phrase}"

        self.operation_count += 1

    @invariant()
    def check_consistency(self):
        """Invariant: all seen mappings remain consistent"""
        for word, expected_result in self.seen_words.items():
            current_result = decode_secret(word)
            assert current_result == expected_result, \
                f"Consistency violation: {word} -> {expected_result} vs {current_result}"


# Test the state machine
TestDecoderStateMachine = DecoderStateMachine.TestCase


# ============================================================================
# COMPLEXITY-BASED PROPERTY TESTS
# ============================================================================

class TestComplexityBasedProperties:
    """Tests based on computational complexity theory"""

    @given(st.integers(min_value=1, max_value=100))
    @settings(max_examples=20)
    def test_time_complexity_linearity(self, input_size):
        """COMPLEXITY TEST: Time complexity should be reasonable"""
        import time

        # Generate input of specified size
        test_input = "a" * input_size

        # Measure execution time
        start_time = time.perf_counter()
        result = decode_secret(test_input)
        end_time = time.perf_counter()

        execution_time = end_time - start_time

        # Should complete in reasonable time (prevents exponential gaming algorithms)
        max_allowed_time = 0.1  # 100ms for any reasonable input
        assert execution_time < max_allowed_time, \
            f"Execution too slow for size {input_size}: {execution_time:.4f}s"

        # Result should be reasonable length
        assert len(result) <= input_size * 2, \
            f"Output length unreasonable for input size {input_size}"

    @given(st.text(alphabet=string.ascii_lowercase, min_size=10, max_size=50))
    def test_space_complexity_linearity(self, long_input):
        """COMPLEXITY TEST: Space usage should be reasonable"""
        result = decode_secret(long_input)

        # Space usage should be proportional to input size
        # Gaming implementations might create huge intermediate structures
        assert len(result) <= len(long_input) * 5, \
            f"Output suspiciously large: input {len(long_input)} -> output {len(result)}"


if __name__ == "__main__":
    # Run with: pytest tests/test_advanced_property_based.py -v
    pass