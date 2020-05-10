"""Tests for [the `cli` module][pytkdocs.cli]."""

import io
import json

from pytkdocs import cli


def test_read_whole_stdin(monkeypatch):
    """Read whole standard input."""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            """
            {
                "objects": [
                    {
                        "path": "pytkdocs.cli.main"
                    },
                    {
                        "path": "pytkdocs.cli.get_parser"
                    }
                ]
            }
            """
        ),
    )

    cli.main()


def test_read_stdin_line_by_line(monkeypatch):
    """Read standard input line by line."""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            '{"objects": [{"path": "pytkdocs.cli.main"}]}\n{"objects": [{"path": "pytkdocs.cli.get_parser"}]}\n'
        ),
    )
    cli.main(["--line-by-line"])


def test_load_complete_tree(monkeypatch):
    """Load `pytkdocs` own documentation."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "pytkdocs"}]}'))
    cli.main(["--line-by-line"])


def test_discard_stdout(monkeypatch, capsys):
    """Discard standard output at import time."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "tests.fixtures.corrupt_output"}]}'))
    cli.main(["--line-by-line"])
    captured = capsys.readouterr()
    assert not captured.out.startswith("*corruption intensifies*")
    # assert no JSON parsing error
    json.loads(captured.out)
