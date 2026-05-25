"""
Runic Script Decoder - Treatment Trial 1
Implementation based on requirements document and runic research.

This implementation focuses on authentic runic symbol translation
based on historical Elder Futhark meanings and associations.
"""

def decode_runes(s: str) -> str:
    """
    Convert runic symbol names to their English meanings.

    Based on Elder Futhark runic alphabet research, each rune traditionally
    represents specific concepts, objects, or natural phenomena.

    Args:
        s: String containing space-separated runic symbol names

    Returns:
        String with English translations of the runic symbols
    """
    if not isinstance(s, str):
        return ""

    # Handle empty or whitespace-only input
    if not s.strip():
        return s

    # Elder Futhark runic meanings based on historical research
    # Each rune traditionally associated with specific concepts
    runic_meanings = _get_runic_translations()

    # Split input on whitespace and process each rune
    rune_tokens = s.split()
    translated_words = []

    for token in rune_tokens:
        # Clean and normalize the token for lookup
        clean_token = _normalize_rune_token(token)

        # Look up translation with fallback handling
        translation = runic_meanings.get(clean_token, token)
        translated_words.append(translation)

    # Join translated words with spaces, preserving original spacing pattern
    return ' '.join(translated_words) if translated_words else s


def _get_runic_translations():
    """
    Generate runic translation mappings from historical Elder Futhark research.

    Returns dictionary mapping runic names to their traditional meanings.
    """
    # Build runic meanings systematically by Aett (group of 8)
    translations = {}

    # First Aett (Freyr's Eight) - Material and social concepts
    first_aett = [
        ('fehu', 'wealth'),      # Cattle, wealth, prosperity
        ('uruz', 'strength'),    # Aurochs, strength, vitality
        ('thurisaz', 'giant'),   # Giant, force, resistance
        ('ansuz', 'wisdom'),     # God, divine inspiration, wisdom
        ('raido', 'journey'),    # Riding, journey, movement
        ('kenaz', 'torch'),      # Torch, knowledge, illumination
        ('gebo', 'gift'),        # Gift, generosity, partnership
        ('wunjo', 'joy'),        # Joy, pleasure, harmony
    ]

    # Second Aett (Hagal's Eight) - Natural forces and cycles
    second_aett = [
        ('hagalaz', 'hail'),     # Hail, destruction, transformation
        ('nauthiz', 'need'),     # Need, constraint, resistance
        ('isa', 'ice'),          # Ice, standstill, preservation
        ('jera', 'harvest'),     # Year, harvest, cycle
        ('eihwaz', 'yew'),       # Yew tree, death, rebirth
        ('perthro', 'lot'),      # Dice cup, fate, mystery
        ('algiz', 'protection'), # Elk, protection, defense
        ('sowilo', 'sun'),       # Sun, wholeness, success
    ]

    # Third Aett (Tyr's Eight) - Human society and spiritual concepts
    third_aett = [
        ('tiwaz', 'victory'),    # Tyr, justice, victory
        ('berkano', 'growth'),   # Birch, growth, renewal
        ('ehwaz', 'horse'),      # Horse, partnership, progress
        ('mannaz', 'man'),       # Man, humanity, social order
        ('laguz', 'water'),      # Water, flow, intuition
        ('ingwaz', 'fertility'), # Ing, fertility, potential
        ('dagaz', 'dawn'),       # Day, dawn, breakthrough
        ('othala', 'heritage'),  # Inheritance, heritage, home
    ]

    # Combine all aetts into single translation map
    for aett in [first_aett, second_aett, third_aett]:
        for rune_name, meaning in aett:
            translations[rune_name] = meaning

    return translations


def _normalize_rune_token(token):
    """
    Normalize a runic token for consistent lookup.

    Handles case variations and whitespace cleanup.
    """
    if not token:
        return token

    # Convert to lowercase and strip whitespace
    normalized = token.lower().strip()

    # Additional normalization could be added here for variant spellings
    # e.g., handle alternative transliterations of runic names

    return normalized