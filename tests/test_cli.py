"""Tests for [the `cli` module][pytkdocs.cli]."""

from __future__ import annotations

import io
import json

import pytest

from pytkdocs import cli, debug


def test_show_help(capsys: pytest.CaptureFixture) -> None:
    """Show help.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-h"])
    captured = capsys.readouterr()
    assert "pytkdocs" in captured.out


def test_read_whole_stdin(monkeypatch: pytest.MonkeyPatch) -> None:
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
            """,
        ),
    )

    cli.main([])


def test_read_stdin_line_by_line(monkeypatch: pytest.MonkeyPatch) -> None:
    """Read standard input line by line."""
    monkeypatch.setattr(
        "sys.stdin",
        io.StringIO(
            '{"objects": [{"path": "pytkdocs.cli.main"}]}\n{"objects": [{"path": "pytkdocs.cli.get_parser"}]}\n',
        ),
    )
    cli.main(["--line-by-line"])


def test_load_complete_tree(monkeypatch: pytest.MonkeyPatch) -> None:
    """Load `pytkdocs` own documentation."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "pytkdocs"}]}'))
    cli.main(["--line-by-line"])


def test_discard_stdout(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """Discard standard output at import time."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "tests.fixtures.corrupt_output"}]}'))
    cli.main(["--line-by-line"])
    captured = capsys.readouterr()
    assert not captured.out.startswith("*corruption intensifies*")
    # assert no JSON parsing error
    json.loads(captured.out)


def test_exception_raised_while_discard_stdout(monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture) -> None:
    """Check that an error is still printed when an exception is raised and stdout is discarded."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "pytkdocs.cli"}]}'))
    # raise an exception during the process
    monkeypatch.setattr("pytkdocs.cli.process_json", lambda _: 1 / 0)
    # assert no exception
    cli.main(["--line-by-line"])
    # assert json error was written to stdout
    captured = capsys.readouterr()
    assert captured.out
    # assert no JSON parsing error
    json.loads(captured.out)


def test_load_complete_tests_tree(monkeypatch: pytest.MonkeyPatch) -> None:
    """Load `pytkdocs` own tests' documentation."""
    monkeypatch.setattr("sys.stdin", io.StringIO('{"objects": [{"path": "tests"}]}'))
    cli.main(["--line-by-line"])


def test_show_version(capsys: pytest.CaptureFixture) -> None:
    """Show version.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["-V"])
    captured = capsys.readouterr()
    assert debug.get_version() in captured.out


def test_show_debug_info(capsys: pytest.CaptureFixture) -> None:
    """Show debug information.

    Parameters:
        capsys: Pytest fixture to capture output.
    """
    with pytest.raises(SystemExit):
        cli.main(["--debug-info"])
    captured = capsys.readouterr().out.lower()
    assert "python" in captured
    assert "system" in captured
    assert "environment" in captured
    assert "packages" in captured
