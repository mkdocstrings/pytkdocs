from pathlib import Path

from visitor import Visitor

TESTS = Path(__file__).parent
FIXTURES = TESTS / "fixtures"


def test_module_imports():
    visitor = Visitor(FIXTURES / "module_imports")
    visitor.start_visiting()

    assert visitor.scope == {
        "module_imports": {
            "a": "a",
            "c": "b",
            "d": "d",
            "e": "e",
            "f.g": "f.g",
            "j": "h.i",
            "k": "k",
            "n": "l.m",
            "o": "o",
            "q": "p",
            "r.s": "r.s",
            "t.u": "t.u",
        }
    }
