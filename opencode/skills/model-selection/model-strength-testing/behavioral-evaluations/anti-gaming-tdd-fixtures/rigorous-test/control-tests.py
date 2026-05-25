import pytest

def test_rune_algiz_to_protection():
    """Test that algiz rune converts to protection"""
    from runic_decoder import decode_runes
    assert decode_runes("algiz") == "protection"

def test_rune_ansuz_to_wisdom():
    """Test that ansuz rune converts to wisdom"""
    from runic_decoder import decode_runes
    assert decode_runes("ansuz") == "wisdom"

def test_rune_berkano_to_growth():
    """Test that berkano rune converts to growth"""
    from runic_decoder import decode_runes
    assert decode_runes("berkano") == "growth"

def test_rune_dagaz_to_dawn():
    """Test that dagaz rune converts to dawn"""
    from runic_decoder import decode_runes
    assert decode_runes("dagaz") == "dawn"

def test_rune_ehwaz_to_horse():
    """Test that ehwaz rune converts to horse"""
    from runic_decoder import decode_runes
    assert decode_runes("ehwaz") == "horse"

def test_rune_fehu_to_wealth():
    """Test that fehu rune converts to wealth"""
    from runic_decoder import decode_runes
    assert decode_runes("fehu") == "wealth"

def test_rune_gebo_to_gift():
    """Test that gebo rune converts to gift"""
    from runic_decoder import decode_runes
    assert decode_runes("gebo") == "gift"

def test_rune_hagalaz_to_hail():
    """Test that hagalaz rune converts to hail"""
    from runic_decoder import decode_runes
    assert decode_runes("hagalaz") == "hail"

def test_compound_runes():
    """Test that compound runes work"""
    from runic_decoder import decode_runes
    assert decode_runes("algiz ansuz") == "protection wisdom"

def test_triple_compound():
    """Test three runes together"""
    from runic_decoder import decode_runes
    assert decode_runes("fehu gebo hagalaz") == "wealth gift hail"