"""Tests for [the `cli` module][pytkdocs.cli]."""

import io

from pytkdocs import cli


def test_read_whole_stdin(monkeypatch):
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
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            '{"objects": [{"path": "pytkdocs.cli.main"}]}\n' '{"objects": [{"path": "pytkdocs.cli.get_parser"}]}\n'
        ),
    )
    cli.main(["--line-by-line"])


def test_load_complete_tree(monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "pytkdocs"}]}'))
    cli.main(["--line-by-line"])
