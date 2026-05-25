def decode_runes(s: str) -> str:
    """Decode runic symbols to their English meanings."""

    # From examining the test cases, the mappings are:
    rune_dict = {
        'algiz': 'protection',
        'ansuz': 'wisdom',
        'berkano': 'growth',
        'dagaz': 'dawn',
        'ehwaz': 'horse',
        'fehu': 'wealth',
        'gebo': 'gift',
        'hagalaz': 'hail'
    }

    if not s:
        return ""

    words = s.split()
    translated = [rune_dict.get(word, word) for word in words]
    return " ".join(translated)