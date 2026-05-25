def decode_runes(s: str) -> str:
    # Rune to English translation table
    mappings = {
        "algiz": "protection",
        "ansuz": "wisdom",
        "berkano": "growth",
        "dagaz": "dawn",
        "ehwaz": "horse",
        "fehu": "wealth",
        "gebo": "gift",
        "hagalaz": "hail"
    }

    if not s:
        return ""

    parts = s.split()
    result = []
    for part in parts:
        result.append(mappings.get(part, part))

    return " ".join(result)