# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [v0.4.0](https://github.com/pawamoy/pytkdocs/releases/tag/v0.4.0) - 2020-05-17

<small>[Compare with v0.3.0](https://github.com/pawamoy/pytkdocs/compare/v0.3.0...v0.4.0)</small>

### Bug Fixes
- Never attempt to parse a null docstring ([aa92668](https://github.com/pawamoy/pytkdocs/commit/aa926686c9f3b9922968387ec68e3a1caeee08a7) by Timothée Mazzucotelli). References: [#37](https://github.com/pawamoy/pytkdocs/issues/37)
- Restore stdout before printing a traceback ([20c21e9](https://github.com/pawamoy/pytkdocs/commit/20c21e9fa8e5a08e113cbbec2da1af240eb6ce16) by Timothée Mazzucotelli). References: [#36](https://github.com/pawamoy/pytkdocs/issues/36)
- Discard import-time stdout ([17f71af](https://github.com/pawamoy/pytkdocs/commit/17f71afb46631dc64cfac9b37a4da8d5cb001801) by Timothée Mazzucotelli). References: [#24](https://github.com/pawamoy/pytkdocs/issues/24)
- Don&#39;t allow `none` for a property&#39;s docstring ([b5868f8](https://github.com/pawamoy/pytkdocs/commit/b5868f83fc6590ee37325377e4cfd42f6dd3a566) by Timothée Mazzucotelli).
- Fix relative path for native namespace packages ([a74dccf](https://github.com/pawamoy/pytkdocs/commit/a74dccf9d753b956044ad3b643457d9ad6c86c64) by Shyam Dwaraknath). References: [#19](https://github.com/pawamoy/pytkdocs/issues/19), [#22](https://github.com/pawamoy/pytkdocs/issues/22)

### Code Refactoring
- Layout a docstring parser base ([d427bcc](https://github.com/pawamoy/pytkdocs/commit/d427bccbfd619f65ae2d12559fcd6f1f1649d036) by Timothée Mazzucotelli).

### Features
- Add dataclass and pydantic support ([a172ad8](https://github.com/pawamoy/pytkdocs/commit/a172ad88ee3b1735ee4ad0c91f3274c359e1e82e) by Shyam Dwaraknath). References: [#9](https://github.com/pawamoy/pytkdocs/issues/9), [#27](https://github.com/pawamoy/pytkdocs/issues/27)


## [v0.3.0](https://github.com/pawamoy/pytkdocs/releases/tag/v0.3.0) - 2020-04-10

<small>[Compare with v0.2.1](https://github.com/pawamoy/pytkdocs/compare/v0.2.1...v0.3.0)</small>

### Bug Fixes
- Fix parsing of `*args` and `**kwargs` ([b81c93e](https://github.com/pawamoy/pytkdocs/commit/b81c93eef2435f2ed1d70b4d7c3946caa564c59e) by adrienhenry). Related issues/PRs: [#20](https://github.com/pawamoy/pytkdocs/issues/20), [#21](https://github.com/pawamoy/pytkdocs/issues/21)

### Features
- Support different indentations and complex markup in docstrings sections ([2f53082](https://github.com/pawamoy/pytkdocs/commit/2f53082dbd2bcb72423d4aff0cb3bf4319476be7) by Timothée Mazzucotelli). Related issues/PRs: [#17](https://github.com/pawamoy/pytkdocs/issues/17)


## [v0.2.1](https://github.com/pawamoy/pytkdocs/releases/tag/v0.2.1) - 2020-04-07

<small>[Compare with v0.2.0](https://github.com/pawamoy/pytkdocs/compare/v0.2.0...v0.2.1)</small>

### Bug Fixes
- Fix forward refs replacement for python > 3.6 ([6a90aca](https://github.com/pawamoy/pytkdocs/commit/6a90aca346209fe2a4e3eec6bfb45f353bce679f) by Timothée Mazzucotelli).
- Handle exception parsing error ([d6561f8](https://github.com/pawamoy/pytkdocs/commit/d6561f86362e7a9d8c45471f1d6eb5deffd5e0c8) by Timothée Mazzucotelli). Related issues/PRs: [#16](https://github.com/pawamoy/pytkdocs/issues/16)


## [v0.2.0](https://github.com/pawamoy/py-tkdocs/releases/tag/v0.2.0) - 2020-03-27

<small>[Compare with v0.1.2](https://github.com/pawamoy/pytkdocs/compare/v0.1.2...V0.2.0)</small>

###  Added
- Add members and filters options ([7af68cc](https://github.com/pawamoy/py-tkdocs/commit/7af68ccffe51557853899a04b5ce5610891d9228)).
- Read type annotations in docstrings.
- Add modules' source code to the output ([f05290b](https://github.com/pawamoy/py-tkdocs/commit/f05290b5a3fb33790c66847a71862c2026585a00)).

### Changed
- The code was refactored for readability and robustness ([ef9ba9d](https://github.com/pawamoy/py-tkdocs/commit/ef9ba9d62bceca7795a751a730fc3f64c9ec9daf)).
  This is a breaking change as some items in the JSON output have changed:
    - the object `signature` value was moved from `obj.docstring.signature` to `obj.signature`,
    - the docstring `sections` value was moved from `obj.docstring.sections` to `obj.docstring_sections`,
    - the docstring `parsing_errors` value was moved from `obj.docstring.parsing_errors` to `obj.docstring_errors`,


## [v0.1.2](https://github.com/pawamoy/pytkdocs/releases/tag/v0.1.2) - 2020-03-23

<small>[Compare with v0.1.1](https://github.com/pawamoy/pytkdocs/compare/v0.1.1...v0.1.2)</small>

### Fixed
- Catch error when trying to get builtins module file path ([48df6bc](https://github.com/pawamoy/pytkdocs/commit/48df6bc9cf878f3ce281fac6ccaf8fe1d4e89c84)).

## [v0.1.1](https://github.com/pawamoy/pytkdocs/releases/tag/v0.1.1) - 2020-03-21

<small>[Compare with v0.1.0](https://github.com/pawamoy/pytkdocs/compare/v0.1.0...v0.1.1)</small>

### Fixed

- Fix 'no parsing_errors attribute in Docstring' error ([0c8a986](https://github.com/pawamoy/pytkdocs/commit/0c8a986a05efe35caebb67d66320ced813065ae4)).
- Handle `KeyError` when searching for param type annotation in signature ([b87fe78](https://github.com/pawamoy/pytkdocs/commit/b87fe78fc5201bac8d54fa70ebb53476480a4126)).


## [v0.1.0](https://github.com/pawamoy/pytkdocs/releases/tag/v0.1.0) - 2020-03-20

<small>[Compare with first commit](https://github.com/pawamoy/pytkdocs/compare/dce21c1b7e15e44529d3cd3ff0fc33f88328de5d...v0.1.0)</small>

### Added

- Initial contents, moved from [`mkdocstrings`](https://github.com/pawamoy/mkdocstrings) and tweaked a bit.