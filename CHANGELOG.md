# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.9.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.9.0) - 2020-09-28

<small>[Compare with 0.8.0](https://github.com/pawamoy/pytkdocs/compare/0.8.0...0.9.0)</small>

### Features
- Add `new_path_syntax` option ([a0b677c](https://github.com/pawamoy/pytkdocs/commit/a0b677c9bbe62f344dfda05b50d729c4d8e7c36a) by Timothée Mazzucotelli).
  See: ["Details on `new_path_syntax`"](https://pawamoy.github.io/pytkdocs/#details-on-new_path_syntax) in the documentation.
  Issue [#66](https://github.com/pawamoy/pytkdocs/issues/66).


## [0.8.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.8.0) - 2020-09-25

<small>[Compare with 0.7.0](https://github.com/pawamoy/pytkdocs/compare/0.7.0...0.8.0)</small>

### Features
- Add async property for coroutine functions ([a013c07](https://github.com/pawamoy/pytkdocs/commit/a013c07f73fce72f73e1267de97d041036106ab5) by Arthur Pastel). Issue [pawamoy/mkdocstrings#151](https://github.com/pawamoy/mkdocstrings/issues/151), PR [#65](https://github.com/pawamoy/pytkdocs/pull/65)


## [0.7.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.7.0) - 2020-07-24

<small>[Compare with 0.6.0](https://github.com/pawamoy/pytkdocs/compare/0.6.0...0.7.0)</small>

### Bug Fixes
- Fix code detecting dataclass fields ([4c4a18b](https://github.com/pawamoy/pytkdocs/commit/4c4a18b881865c3182eef77a95ef1a6b1f1a5b6d) by Timothée Mazzucotelli).
- Prevent crash in case of empty dataclasses ([835c066](https://github.com/pawamoy/pytkdocs/commit/835c066ac47cdb1203dc3feb9dfc3f96df7109e0) by Jared Khan). PR [#56](https://github.com/pawamoy/pytkdocs/issues/56)
- Use `inspect.cleandoc` for stripping docstrings whitespace ([8009940](https://github.com/pawamoy/pytkdocs/commit/8009940c43a551a86ca91e0f81b234933d47bd6e) by Jared Khan). Issue [#54](https://github.com/pawamoy/pytkdocs/issues/54), PR [#55](https://github.com/pawamoy/pytkdocs/issues/55)

### Features
- Add support for Marshmallow models ([c250466](https://github.com/pawamoy/pytkdocs/commit/c250466e219edf24d2f85b7337b5670e6f27a724) by Stu Fisher). References: [#51](https://github.com/pawamoy/pytkdocs/issues/51)


## [0.6.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.6.0) - 2020-06-14

<small>[Compare with 0.5.2](https://github.com/pawamoy/pytkdocs/compare/0.5.2...0.6.0)</small>

### Features
- Support attributes sections for Google-style docstrings ([02c0042](https://github.com/pawamoy/pytkdocs/commit/02c0042f9d4d8ab799550418d8474d1a6669feec) by Timothée Mazzucotelli).


## [0.5.2](https://github.com/pawamoy/pytkdocs/releases/tag/0.5.2) - 2020-06-11

<small>[Compare with 0.5.1](https://github.com/pawamoy/pytkdocs/compare/0.5.1...0.5.2)</small>

### Bug Fixes
- Ignore exceptions when trying to unwrap ([02ba876](https://github.com/pawamoy/pytkdocs/commit/02ba8762716c416499bdd4d4834c5de35bca23cb) by Timothée Mazzucotelli). References: [#45](https://github.com/pawamoy/pytkdocs/issues/45)


## [0.5.1](https://github.com/pawamoy/pytkdocs/releases/tag/0.5.1) - 2020-06-09

<small>[Compare with 0.5.0](https://github.com/pawamoy/pytkdocs/compare/0.5.0...0.5.1)</small>

### Bug Fixes
- Fix parsing tuple unpacking assignment ([6535fe8](https://github.com/pawamoy/pytkdocs/commit/6535fe813b6c4b756d1d481f097208c52470da6a) by Timothée Mazzucotelli). References: [#43](https://github.com/pawamoy/pytkdocs/issues/43)


## [0.5.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.5.0) - 2020-06-08

<small>[Compare with 0.4.0](https://github.com/pawamoy/pytkdocs/compare/0.4.0...0.5.0)</small>

### Bug Fixes
- Fix getting documentation for wrapped objects ([09f38a5](https://github.com/pawamoy/pytkdocs/commit/09f38a501edde2963af50130c11ff38107d14367) by Timothée Mazzucotelli). References: [#32](https://github.com/pawamoy/pytkdocs/issues/32)
- Dedent attributes docstrings ([1a6809c](https://github.com/pawamoy/pytkdocs/commit/1a6809ce4358707b6b144a331955974e8891c475) by Timothée Mazzucotelli). References: [#42](https://github.com/pawamoy/pytkdocs/issues/42)

### Code Refactoring
- Accept any valid loader option in JSON input ([b58f4a9](https://github.com/pawamoy/pytkdocs/commit/b58f4a98b3da3d3dcfc82738ee560c1affa6d387) by Timothée Mazzucotelli).
- Change Pydantic properties names ([fa8d2e7](https://github.com/pawamoy/pytkdocs/commit/fa8d2e7a60ebcc39012cea8a6228770a4e7db2c4) by Timothée Mazzucotelli).
- Refactor parsers ([3caefba](https://github.com/pawamoy/pytkdocs/commit/3caefba1dcbd85a0bc2d05948073677c751aa1f3) by Timothée Mazzucotelli).
- Don't serialize empty error lists in the result ([7bec6c4](https://github.com/pawamoy/pytkdocs/commit/7bec6c4aca9d3087bb5fb4e34b2801a58839dd3a) by Timothée Mazzucotelli).

### Features
- Accept docstring options in JSON input ([400af0b](https://github.com/pawamoy/pytkdocs/commit/400af0bccb4297c3e872910d13c0b44ca3ce1339) by Timothée Mazzucotelli).
- Retrieve dataclass fields docstrings ([09eb224](https://github.com/pawamoy/pytkdocs/commit/09eb224c3c961bdd82640221b888cbe52b9a489e) by Timothée Mazzucotelli). References: [#31](https://github.com/pawamoy/pytkdocs/issues/31)
- Add support for class inheritance (inherited members) ([1af9a53](https://github.com/pawamoy/pytkdocs/commit/1af9a53f6c387cad17ec50b523bc22e149fdc8d1) by Timothée Mazzucotelli). References: [#18](https://github.com/pawamoy/pytkdocs/issues/18), [#41](https://github.com/pawamoy/pytkdocs/issues/41)
- Add support for examples section ([9521c7f](https://github.com/pawamoy/pytkdocs/commit/9521c7f0f27513d18918e7260fb51d73fa548865) by Iago GR). References: [#8](https://github.com/pawamoy/pytkdocs/issues/8)
- As a consequence of the attribute parser refactor: pick attributes without docstrings. References: [#11](https://github.com/pawamoy/pytkdocs/issues/11)


## [0.4.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.4.0) - 2020-05-17

<small>[Compare with 0.3.0](https://github.com/pawamoy/pytkdocs/compare/0.3.0...0.4.0)</small>

### Bug Fixes
- Never attempt to parse a null docstring ([aa92668](https://github.com/pawamoy/pytkdocs/commit/aa926686c9f3b9922968387ec68e3a1caeee08a7) by Timothée Mazzucotelli). References: [#37](https://github.com/pawamoy/pytkdocs/issues/37)
- Restore stdout before printing a traceback ([20c21e9](https://github.com/pawamoy/pytkdocs/commit/20c21e9fa8e5a08e113cbbec2da1af240eb6ce16) by Timothée Mazzucotelli). References: [#36](https://github.com/pawamoy/pytkdocs/issues/36)
- Discard import-time stdout ([17f71af](https://github.com/pawamoy/pytkdocs/commit/17f71afb46631dc64cfac9b37a4da8d5cb001801) by Timothée Mazzucotelli). References: [#24](https://github.com/pawamoy/pytkdocs/issues/24)
- Don't allow `None` for a property's docstring ([b5868f8](https://github.com/pawamoy/pytkdocs/commit/b5868f83fc6590ee37325377e4cfd42f6dd3a566) by Timothée Mazzucotelli).
- Fix relative path for native namespace packages ([a74dccf](https://github.com/pawamoy/pytkdocs/commit/a74dccf9d753b956044ad3b643457d9ad6c86c64) by Shyam Dwaraknath). References: [#19](https://github.com/pawamoy/pytkdocs/issues/19), [#22](https://github.com/pawamoy/pytkdocs/issues/22)

### Code Refactoring
- Layout a docstring parser base ([d427bcc](https://github.com/pawamoy/pytkdocs/commit/d427bccbfd619f65ae2d12559fcd6f1f1649d036) by Timothée Mazzucotelli).

### Features
- Add dataclass and pydantic support ([a172ad8](https://github.com/pawamoy/pytkdocs/commit/a172ad88ee3b1735ee4ad0c91f3274c359e1e82e) by Shyam Dwaraknath). References: [#9](https://github.com/pawamoy/pytkdocs/issues/9), [#27](https://github.com/pawamoy/pytkdocs/issues/27)


## [0.3.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.3.0) - 2020-04-10

<small>[Compare with 0.2.1](https://github.com/pawamoy/pytkdocs/compare/0.2.1...0.3.0)</small>

### Bug Fixes
- Fix parsing of `*args` and `**kwargs` ([b81c93e](https://github.com/pawamoy/pytkdocs/commit/b81c93eef2435f2ed1d70b4d7c3946caa564c59e) by adrienhenry). Related issues/PRs: [#20](https://github.com/pawamoy/pytkdocs/issues/20), [#21](https://github.com/pawamoy/pytkdocs/issues/21)

### Features
- Support different indentations and complex markup in docstrings sections ([2f53082](https://github.com/pawamoy/pytkdocs/commit/2f53082dbd2bcb72423d4aff0cb3bf4319476be7) by Timothée Mazzucotelli). Related issues/PRs: [#17](https://github.com/pawamoy/pytkdocs/issues/17)


## [0.2.1](https://github.com/pawamoy/pytkdocs/releases/tag/0.2.1) - 2020-04-07

<small>[Compare with 0.2.0](https://github.com/pawamoy/pytkdocs/compare/0.2.0...0.2.1)</small>

### Bug Fixes
- Fix forward refs replacement for python > 3.6 ([6a90aca](https://github.com/pawamoy/pytkdocs/commit/6a90aca346209fe2a4e3eec6bfb45f353bce679f) by Timothée Mazzucotelli).
- Handle exception parsing error ([d6561f8](https://github.com/pawamoy/pytkdocs/commit/d6561f86362e7a9d8c45471f1d6eb5deffd5e0c8) by Timothée Mazzucotelli). Related issues/PRs: [#16](https://github.com/pawamoy/pytkdocs/issues/16)


## [0.2.0](https://github.com/pawamoy/py-tkdocs/releases/tag/0.2.0) - 2020-03-27

<small>[Compare with 0.1.2](https://github.com/pawamoy/pytkdocs/compare/0.1.2...V0.2.0)</small>

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


## [0.1.2](https://github.com/pawamoy/pytkdocs/releases/tag/0.1.2) - 2020-03-23

<small>[Compare with 0.1.1](https://github.com/pawamoy/pytkdocs/compare/0.1.1...0.1.2)</small>

### Fixed
- Catch error when trying to get builtins module file path ([48df6bc](https://github.com/pawamoy/pytkdocs/commit/48df6bc9cf878f3ce281fac6ccaf8fe1d4e89c84)).

## [0.1.1](https://github.com/pawamoy/pytkdocs/releases/tag/0.1.1) - 2020-03-21

<small>[Compare with 0.1.0](https://github.com/pawamoy/pytkdocs/compare/0.1.0...0.1.1)</small>

### Fixed

- Fix 'no parsing_errors attribute in Docstring' error ([0c8a986](https://github.com/pawamoy/pytkdocs/commit/0c8a986a05efe35caebb67d66320ced813065ae4)).
- Handle `KeyError` when searching for param type annotation in signature ([b87fe78](https://github.com/pawamoy/pytkdocs/commit/b87fe78fc5201bac8d54fa70ebb53476480a4126)).


## [0.1.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.1.0) - 2020-03-20

<small>[Compare with first commit](https://github.com/pawamoy/pytkdocs/compare/dce21c1b7e15e44529d3cd3ff0fc33f88328de5d...0.1.0)</small>

### Added

- Initial contents, moved from [`mkdocstrings`](https://github.com/pawamoy/mkdocstrings) and tweaked a bit.
