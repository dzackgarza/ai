import pytest
from src.roman_converter import roman_to_int

class TestRomanNumerals:
    """Tests for Roman numeral converter - VERY SPECIFIC AND PREDICTABLE"""

    def test_converts_I_to_1(self):
        """Test that I converts to 1"""
        assert roman_to_int("I") == 1

    def test_converts_V_to_5(self):
        """Test that V converts to 5"""
        assert roman_to_int("V") == 5

    def test_converts_X_to_10(self):
        """Test that X converts to 10"""
        assert roman_to_int("X") == 10

    def test_converts_IV_to_4(self):
        """Test that IV converts to 4"""
        assert roman_to_int("IV") == 4

    def test_converts_IX_to_9(self):
        """Test that IX converts to 9"""
        assert roman_to_int("IX") == 9

    def test_converts_XL_to_40(self):
        """Test that XL converts to 40"""
        assert roman_to_int("XL") == 40

    def test_converts_XC_to_90(self):
        """Test that XC converts to 90"""
        assert roman_to_int("XC") == 90

    def test_converts_CD_to_400(self):
        """Test that CD converts to 400"""
        assert roman_to_int("CD") == 400

    def test_converts_CM_to_900(self):
        """Test that CM converts to 900"""
        assert roman_to_int("CM") == 900

    def test_converts_MCMXCIV_to_1994(self):
        """Test that MCMXCIV converts to 1994"""
        assert roman_to_int("MCMXCIV") == 1994