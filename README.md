# pytkdocs
[![pipeline status](https://gitlab.com/pawamoy/pytkdocs/badges/master/pipeline.svg)](https://gitlab.com/pawamoy/pytkdocs/pipelines)
[![coverage report](https://gitlab.com/pawamoy/pytkdocs/badges/master/coverage.svg)](https://gitlab.com/pawamoy/pytkdocs/commits/master)
[![documentation](https://img.shields.io/badge/docs-latest-green.svg?style=flat)](https://pawamoy.github.io/pytkdocs)
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
      "path": "my_module.my_class",
      "members": true,
      "filters": [
        "!^_[^_]"
      ]
    }
  ]
}
```

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
