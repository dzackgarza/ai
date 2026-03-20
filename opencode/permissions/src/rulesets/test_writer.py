from src.mixins import mixin_test_writer


class TestWriter:
    """Read tests and plans, write tests."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_test_writer()]
