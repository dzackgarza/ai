"""Example package for the quality-control Python seed."""

__all__ = ["normalize_label"]


def normalize_label(value: str) -> str:
    """Normalize a user-visible label for stable comparison."""
    return " ".join(value.strip().casefold().split())
