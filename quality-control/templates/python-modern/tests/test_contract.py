from example_project import normalize_label


def test_normalize_label_contract() -> None:
    assert normalize_label("  Spectral   Sequence  ") == "spectral sequence"
