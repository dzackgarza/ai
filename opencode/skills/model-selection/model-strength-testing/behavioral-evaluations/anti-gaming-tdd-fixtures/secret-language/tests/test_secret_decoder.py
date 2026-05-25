import pytest
from src.secret_decoder import decode_secret

class TestSecretDecoder:
    """Tests for Secret Language Decoder - EXTREMELY SPECIFIC"""

    def test_decode_alpha(self):
        """Test that 'alpha' decodes to 'hidden'"""
        assert decode_secret("alpha") == "hidden"

    def test_decode_beta(self):
        """Test that 'beta' decodes to 'message'"""
        assert decode_secret("beta") == "message"

    def test_decode_gamma(self):
        """Test that 'gamma' decodes to 'found'"""
        assert decode_secret("gamma") == "found"

    def test_decode_delta(self):
        """Test that 'delta' decodes to 'treasure'"""
        assert decode_secret("delta") == "treasure"

    def test_decode_epsilon(self):
        """Test that 'epsilon' decodes to 'secret'"""
        assert decode_secret("epsilon") == "secret"

    def test_decode_zeta(self):
        """Test that 'zeta' decodes to 'code'"""
        assert decode_secret("zeta") == "code"

    def test_decode_eta(self):
        """Test that 'eta' decodes to 'puzzle'"""
        assert decode_secret("eta") == "puzzle"

    def test_decode_theta(self):
        """Test that 'theta' decodes to 'mystery'"""
        assert decode_secret("theta") == "mystery"

    def test_decode_compound_alpha_beta(self):
        """Test that 'alpha beta' decodes to 'hidden message'"""
        assert decode_secret("alpha beta") == "hidden message"

    def test_decode_compound_gamma_delta_epsilon(self):
        """Test that 'gamma delta epsilon' decodes to 'found treasure secret'"""
        assert decode_secret("gamma delta epsilon") == "found treasure secret"