from src.mixins import mixin_test_writer, mixin_git


class TestWriter:
    """Read tests and plans, write tests, commit."""

    @classmethod
    def layers(cls) -> list[dict]:
        return [mixin_test_writer(), mixin_git()]
