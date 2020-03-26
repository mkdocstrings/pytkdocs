"""In this module we simply define some path constants."""

from pathlib import Path

TESTS_DIR: Path = Path(__file__).parent
"""The tests directory path object."""

TMP_DIR: Path = TESTS_DIR / "tmp"
"""The tests/tmp directory path object."""

FIXTURES_DIR: Path = TESTS_DIR / "fixtures"
"""The tests/fixtures directory path object."""
