# pytkdocs

[![ci](https://github.com/pawamoy/pytkdocs/workflows/ci/badge.svg)](https://github.com/pawamoy/pytkdocs/actions?query=workflow%3Aci)
[![documentation](https://img.shields.io/badge/docs-mkdocs%20material-blue.svg?style=flat)](https://pawamoy.github.io/pytkdocs/)
[![pypi version](https://img.shields.io/pypi/v/pytkdocs.svg)](https://pypi.org/project/pytkdocs/)

Load Python objects documentation.

## Requirements

`pytkdocs` requires Python 3.6 or above.

<details>
<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>

```bash
# install pyenv
git clone https://github.com/pyenv/pyenv ~/.pyenv

# setup pyenv (you should also put these three lines in .bashrc or similar)
export PATH="${HOME}/.pyenv/bin:${PATH}"
export PYENV_ROOT="${HOME}/.pyenv"
eval "$(pyenv init -)"

# install Python 3.6
pyenv install 3.6.8

# make it available globally
pyenv global system 3.6.8
```
</details>

## Installation

With `pip`:
```bash
python3.6 -m pip install pytkdocs
```

With [`pipx`](https://github.com/pipxproject/pipx):
```bash
python3.6 -m pip install --user pipx

pipx install --python python3.6 pytkdocs
```

## Usage

`pytkdocs` accepts JSON on standard input and writes JSON on standard output.

Input format:

```json
{
  "objects": [
    {
      "path": "pytkdocs",
      "members": true,
      "inherited_members": false,
      "filters": [
        "!^_[^_]"
      ],
      "docstring_style": "google",
      "docstring_options": {
        "replace_admonitions": true
      }
    }
  ]
}
```

Output format:

```json
{
  "loading_errors": [
    "string (message)"
  ],
  "parsing_errors": {
    "string (object)": [
      "string (message)"
    ]
  },
  "objects": [
    {
      "name": "pytkdocs",
      "path": "pytkdocs",
      "category": "module",
      "file_path": "/media/data/dev/pawamoy/pytkdocs/src/pytkdocs/__init__.py",
      "relative_file_path": "pytkdocs/__init__.py",
      "properties": [
        "special"
      ],
      "parent_path": "pytkdocs",
      "has_contents": true,
      "docstring": "pytkdocs package.\n\nLoad Python objects documentation.",
      "docstring_sections": [
        {
          "type": "markdown",
          "value": "pytkdocs package.\n\nLoad Python objects documentation."
        }
      ],
      "source": {
        "code": "\"\"\"\npytkdocs package.\n\nLoad Python objects documentation.\n\"\"\"\n\nfrom typing import List\n\n__all__: List[str] = []\n",
        "line_start": 1
      },
      "children": {
        "pytkdocs.__all__": {
          "name": "__all__",
          "path": "pytkdocs.__all__",
          "category": "attribute",
          "file_path": "/media/data/dev/pawamoy/pytkdocs/src/pytkdocs/__init__.py",
          "relative_file_path": "pytkdocs/__init__.py",
          "properties": [
            "special"
          ],
          "parent_path": "pytkdocs",
          "has_contents": false,
          "docstring": null,
          "docstring_sections": [],
          "source": {},
          "children": {},
          "attributes": [],
          "methods": [],
          "functions": [],
          "modules": [],
          "classes": []
        }
      },
      "attributes": [
        "pytkdocs.__all__"
      ],
      "methods": [],
      "functions": [],
      "modules": [
        "pytkdocs.__main__",
        "pytkdocs.cli",
        "pytkdocs.loader",
        "pytkdocs.objects",
        "pytkdocs.parsers",
        "pytkdocs.properties",
        "pytkdocs.serializer"
      ],
      "classes": []
    }
  ]
}
```

## Command-line

Running `pytkdocs` without argument will read the whole standard input,
and output the result once.

Running `pytkdocs --line-by-line` will enter an infinite loop,
where at each iteration one line is read on the standard input,
and the result is written back on one line.
This allows other programs to use `pytkdocs` in a subprocess,
feeding it single lines of JSON, and reading back single lines of JSON as well.
This mode was actually implemented specifically for
[mkdocstrings](https://github.com/pawamoy/mkdocstrings).

## Configuration

The configuration options available are:

- `filters`: filters are regular expressions that allow to select or un-select objects based on their name.
  They are applied recursively (on every child of every object).
  If the expression starts with an exclamation mark,
  it will filter out objects matching it (the exclamation mark is removed before evaluation).
  If not, objects matching it are selected.
  Every regular expression is performed against every name.
  It allows fine-grained filtering. Example:

    - `!^_`: filter out every object whose name starts with `_` (private/protected)
    - `^__`: but still select those who start with two `_` (class-private)
    - `!^__.*__$`: except those who also end with two `_` (specials)
  
- `members`: this option allows to explicitly select the members of the top-object.
  If `True`, select every members that passes filters. If `False`, select nothing.
  If it's a list of names, select only those members, and apply filters on their children only.

- `docstring_style`: the docstring style to use when parsing the docstring. Only one parser available: `google`.

- `docstring_options`: options to pass to the docstring parser.
    - `google` accepts a `replace_admonitions` boolean option (default: true). When enabled, this option will
      replace titles of an indented block by their Markdown admonition equivalent:
      `AdmonitionType: Title` will become `!!! admonitiontype "Title"`.
    
- `inherited_members`: true or false (default). When enabled, inherited members will be selected as well.
