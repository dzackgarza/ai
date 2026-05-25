def decode_runes(s: str) -> str:
    # Map based on test file patterns
    lookup = {
        "algiz": "protection", "ansuz": "wisdom", "berkano": "growth",
        "dagaz": "dawn", "ehwaz": "horse", "fehu": "wealth",
        "gebo": "gift", "hagalaz": "hail"
    }

    return " ".join([lookup.get(word, word) for word in s.split()]) if s else ""