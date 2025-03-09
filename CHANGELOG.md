# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

<!-- insertion marker -->
## [0.16.4](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.16.4) - 2025-03-09

<small>[Compare with 0.16.3](https://github.com/mkdocstrings/pytkdocs/compare/0.16.3...0.16.4)</small>

### Bug Fixes

- Stop using deprecated `ast.Str` ([7b3bace](https://github.com/mkdocstrings/pytkdocs/commit/7b3bacec73b76822066f9f60fbff8a76aea96b03) by Timothée Mazzucotelli).

## [0.16.3](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.16.3) - 2025-03-09

<small>[Compare with 0.16.2](https://github.com/mkdocstrings/pytkdocs/compare/0.16.2...0.16.3)</small>

### Build

- Drop support for Python 3.8 ([b4c5c51](https://github.com/mkdocstrings/pytkdocs/commit/b4c5c51242cc146638c6a6c2b991e81fbd4a683f) by Timothée Mazzucotelli).

### Bug Fixes

- Don't crash on attribute error when trying to detect field ([cd9407f](https://github.com/mkdocstrings/pytkdocs/commit/cd9407fd8c7c24f5752dd1c2c2dc230e98ed53e5) by Timothée Mazzucotelli). [Issue-149](https://github.com/mkdocstrings/pytkdocs/issues/149)

## [0.16.2](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.16.2) - 2024-09-07

<small>[Compare with 0.16.1](https://github.com/mkdocstrings/pytkdocs/compare/0.16.1...0.16.2)</small>

### Code Refactoring

- Swallow kwargs in all parsers constructors ([fe8e96f](https://github.com/mkdocstrings/pytkdocs/commit/fe8e96f2f79617c1b330b2ae4be543667e98a976) by Timothée Mazzucotelli).
- General maintenance ([29559e8](https://github.com/mkdocstrings/pytkdocs/commit/29559e8afa1f08006304dbba62e7f1e3fc3c351f) by Timothée Mazzucotelli).

## [0.16.1](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.16.1) - 2022-03-07

<small>[Compare with 0.16.0](https://github.com/mkdocstrings/pytkdocs/compare/0.16.0...0.16.1)</small>

### Bug Fixes
- Always return strings (not `None`) and warn about missing descriptions in numpy parser ([50b9597](https://github.com/mkdocstrings/pytkdocs/commit/50b9597d52c4b22de110821fe646d9f992e2977b) by Joseph Richardson). [Issue #137](https://github.com/mkdocstrings/pytkdocs/issues/137), [PR #138](https://github.com/mkdocstrings/pytkdocs/pull/138)


## [0.16.0](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.16.0) - 2022-02-19

<small>[Compare with 0.15.0](https://github.com/mkdocstrings/pytkdocs/compare/0.15.0...0.16.0)</small>

### Maintenance
- Drop Python 3.6 support ([0d39665](https://github.com/mkdocstrings/pytkdocs/commit/0d396653cb2cb2b286bae4c948b0dae869c32cd1) by Timothée Mazzucotelli).

### Features
- Add `trim_doctest_flag` to google and numpy parsers ([0fecc43](https://github.com/mkdocstrings/pytkdocs/commit/0fecc4338061ecfa374ce823a34be0764d550547) by Jeremy Goh). [Issue mkdocstrings/mkdocstrings#386](https://github.com/mkdocstrings/mkdocstrings/issues/386), [PR #134](https://github.com/mkdocstrings/pytkdocs/pull/134)


## [0.15.0](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.15.0) - 2021-12-27

<small>[Compare with 0.14.2](https://github.com/mkdocstrings/pytkdocs/compare/0.14.2...0.15.0)</small>

### Features
- Add support for `help_text` field parameter as docstring for django model fields ([01ac524](https://github.com/mkdocstrings/pytkdocs/commit/01ac524a1d353aa816adbb4ee46731451b58db37) by mabugaj). References: [#127](https://github.com/mkdocstrings/pytkdocs/issues/127), [#129](https://github.com/mkdocstrings/pytkdocs/issues/129)


## [0.14.2](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.14.2) - 2021-12-16

<small>[Compare with 0.14.1](https://github.com/mkdocstrings/pytkdocs/compare/0.14.1...0.14.2)</small>

### Dependencies
- Remove upper bounds on production dependencies ([22ff7df](https://github.com/mkdocstrings/pytkdocs/commit/22ff7df70361bc460ba3b92bfba51d90481112fd) by Timothée Mazzucotelli). [Issue #124](https://github.com/mkdocstrings/pytkdocs/issues/124), [PR #128](https://github.com/mkdocstrings/pytkdocs/pull/128)


## [0.14.1](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.14.1) - 2021-12-16

<small>[Compare with 0.14.0](https://github.com/mkdocstrings/pytkdocs/compare/0.14.0...0.14.1)</small>

### Code Refactoring
- Remove upper bounds on development dependencies ([e1a4eba](https://github.com/mkdocstrings/pytkdocs/commit/e1a4eba87b2253024eea5fb68510aa6cda1d9f1c) by Timothée Mazzucotelli). [PR #126](https://github.com/mkdocstrings/pytkdocs/pull/126). See https://iscinumpy.dev/post/bound-version-constraints/.


## [0.14.0](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.14.0) - 2021-10-08

<small>[Compare with 0.13.0](https://github.com/mkdocstrings/pytkdocs/compare/0.13.0...0.14.0)</small>

### Features
- Add Markdown docstring-style support ([06556e3](https://github.com/mkdocstrings/pytkdocs/commit/06556e37634e0c520b28fa323d8d4ea459c32892) by Timothée Mazzucotelli). [PR #121](https://github.com/mkdocstrings/pytkdocs/pull/121)

### Bug Fixes
- Serialize yields and keyword arguments sections ([8fb86d6](https://github.com/mkdocstrings/pytkdocs/commit/8fb86d6777f11ff9ead322b901106d1e5a6d4741) by Timothée Mazzucotelli).


## [0.13.0](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.13.0) - 2021-10-06

<small>[Compare with 0.12.0](https://github.com/mkdocstrings/pytkdocs/compare/0.12.0...0.13.0)</small>

### Features
- Support google yields sections ([4b99cbc](https://github.com/mkdocstrings/pytkdocs/commit/4b99cbc7192ab4a1093237a1c79fdf8d70c39b6b) by Timothée Mazzucotelli). [Issue #89](https://github.com/mkdocstrings/pytkdocs/issues/89), [PR #116](https://github.com/mkdocstrings/pytkdocs/pull/116)

### Bug Fixes
- Add source to class objects ([8931df8](https://github.com/mkdocstrings/pytkdocs/commit/8931df8f7ef9c98d2a36efcee09339d012a08157) by jakekaplan). [PR #120](https://github.com/mkdocstrings/pytkdocs/pull/120)
- Pass context when parsing class docstring ([4a62039](https://github.com/mkdocstrings/pytkdocs/commit/4a6203926e1ad42c0cc9652f1e42b1570d193564) by jakekaplan).[PR #118](https://github.com/mkdocstrings/pytkdocs/pull/118)
- Don't mistakenly return a 'missing annotation' error ([4afc97f](https://github.com/mkdocstrings/pytkdocs/commit/4afc97f912472e9a29931d09feb88d07376b4afd) by Timothée Mazzucotelli).

### Code Refactoring
- Set keyword-only kind on keyword arguments ([c5c2ef0](https://github.com/mkdocstrings/pytkdocs/commit/c5c2ef0655bce35fe8df4d8f2674701fc8086c48) by Timothée Mazzucotelli).


## [0.12.0](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.12.0) - 2021-09-21

<small>[Compare with 0.11.1](https://github.com/mkdocstrings/pytkdocs/compare/0.11.1...0.12.0)</small>

### Features
- Include base classes in output ([f7f6652](https://github.com/mkdocstrings/pytkdocs/commit/f7f6652f5b796c37980cc6b68865b2441a469ebd) by Brian Koropoff). [Issue mkdocstrings#269](https://github.com/mkdocstrings/mkdocstrings/issues/269), [PR #108](https://github.com/mkdocstrings/pytkdocs/pull/108)
- Support "Keyword Args" sections for Gooogle-style ([0133369](https://github.com/mkdocstrings/pytkdocs/commit/013336970029edc0ff95a025007492786d77ed9c) by HacKan). [Issue #88](https://github.com/mkdocstrings/pytkdocs/issues/88), [PR #105](https://github.com/mkdocstrings/pytkdocs/pull/105)
- Allow method descriptors to be serialized as methods ([8e1b1b2](https://github.com/mkdocstrings/pytkdocs/commit/8e1b1b2375070ab5b01757c686da4bbde3a771cd) by jmrgibson). [PR #103](https://github.com/mkdocstrings/pytkdocs/pull/103)
- Add support for Django models ([6416a05](https://github.com/mkdocstrings/pytkdocs/commit/6416a05c080d2f15206b26d641cd7d5ca18af316) by Michał Rokita). [Issue #39](https://github.com/mkdocstrings/pytkdocs/issues/39), [PR #101](https://github.com/mkdocstrings/pytkdocs/pull/101)

### Bug Fixes
- Fix getting parent module of decorated functions ([88b457f](https://github.com/mkdocstrings/pytkdocs/commit/88b457f8aae51a422470d6c34859439d97b110e0) by Timothée Mazzucotelli). [Issue mkdocstrings#162](https://github.com/mkdocstrings/mkdocstrings/issues/162), [PR #109](https://github.com/mkdocstrings/pytkdocs/pull/109)

### Code Refactoring
- Stop recording errors in the loader ([3191bac](https://github.com/mkdocstrings/pytkdocs/commit/3191bac307a85f8c1e108eea5c7ee72bd50c8803) by Timothée Mazzucotelli). [Issue #111](https://github.com/mkdocstrings/pytkdocs/issues/111), [PR #114](https://github.com/mkdocstrings/pytkdocs/pull/114)
- Remove warning about new path style option ([14b18be](https://github.com/mkdocstrings/pytkdocs/commit/14b18beb2116564c1ad2c1bb3b1f2316d813a7c7) by Timothée Mazzucotelli).
- Switch preference order between annotation and docstring type ([c4f6bdc](https://github.com/mkdocstrings/pytkdocs/commit/c4f6bdc8136497eeca43583c04fa72d9d316df4b) by Andy Challis, and [75b4024](https://github.com/mkdocstrings/pytkdocs/commit/75b40247a4002823cdc2505cc864a70db745950e) by Timothée Mazzucotelli). [Issue mkdocstrings#143](https://github.com/mkdocstrings/mkdocstrings/issues/143), [PR #110](https://github.com/mkdocstrings/pytkdocs/pull/110)


## [0.11.1](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.11.1) - 2021-04-03

<small>[Compare with 0.11.0](https://github.com/mkdocstrings/pytkdocs/compare/0.11.0...0.11.1)</small>

### Bug Fixes
- Remove duplicate dataclass attributes when they have defaults ([c0277b2](https://github.com/mkdocstrings/pytkdocs/commit/c0277b2104d615a38558ab2d93e495faf360bd63) by Bernhard Stadlbauer). [Issue #52](https://github.com/mkdocstrings/pytkdocs/issues/52), [PR #100](https://github.com/mkdocstrings/pytkdocs/pull/100)


## [0.11.0](https://github.com/mkdocstrings/pytkdocs/releases/tag/0.11.0) - 2021-02-28

<small>[Compare with 0.10.1](https://github.com/mkdocstrings/pytkdocs/compare/0.10.1...0.11.0)</small>

### Features
- Add support for Numpy docstrings ([de0424a](https://github.com/mkdocstrings/pytkdocs/commit/de0424a33e94f7dfdfd3b613c500a6fb428406aa) by Achille M). [Issue #7](https://github.com/mkdocstrings/pytkdocs/issues/7), [PR #87](https://github.com/mkdocstrings/pytkdocs/pull/87)

### Bug Fixes
- Fix type annotations parsing ([9025438](https://github.com/mkdocstrings/pytkdocs/commit/90254380a01483172c910b82844fdfb0f38fe1fb) by Timothée Mazzucotelli). [Issue #92](https://github.com/mkdocstrings/pytkdocs/issues/92), [PR #96](https://github.com/mkdocstrings/pytkdocs/pull/96)
- Fix pydantic type documentation for List/Set/Tuple ([b99c661](https://github.com/mkdocstrings/pytkdocs/commit/b99c661398ad71562bd909cebe1e40df109f058e) by Shashank Sharma). [Issue #94](https://github.com/mkdocstrings/pytkdocs/issues/94), [PR #95](https://github.com/mkdocstrings/pytkdocs/pull/95)
- Support cached properties ([4052eab](https://github.com/mkdocstrings/pytkdocs/commit/4052eabdd45a7f4fe8c3fc8591bb23e1763a5a0f) by Timothée Mazzucotelli). [Issue #86](https://github.com/mkdocstrings/pytkdocs/issues/86)
- Get inherited properties docstrings from parent class ([c88282c](https://github.com/mkdocstrings/pytkdocs/commit/c88282cc89a4d8a6c897a6d6851d832466b2360b) by Timothée Mazzucotelli). [Issue #90](https://github.com/mkdocstrings/pytkdocs/issues/90)
- Fix dedent for attributes docstrings ([0326005](https://github.com/mkdocstrings/pytkdocs/commit/032600563ae613aa14dd18c0d1f44d0c78316ecd) by Timothée Mazzucotelli). [Issue #54](https://github.com/mkdocstrings/pytkdocs/issues/54), [issue mkdocstrings#225](https://github.com/mkdocstrings/mkdocstrings/issues/225)

## [0.10.1](https://github.com/pawamoy/pytkdocs/releases/tag/0.10.1) - 2021-01-03

<small>[Compare with 0.10.0](https://github.com/pawamoy/pytkdocs/compare/0.10.0...0.10.1)</small>

### Bug Fixes
- Warn when examples section is empty ([e1d2dfc](https://github.com/pawamoy/pytkdocs/commit/e1d2dfc3a9bff690c9061892268fd480e83c6f91) by Timothée Mazzucotelli).
- Allow newer version of dataclasses backport ([4392f2e](https://github.com/pawamoy/pytkdocs/commit/4392f2e4669c76bf2acf74b6124f74b7734b638b) by Patrick Lannigan).
- Ignore errors parsing c-extension modules ([1930054](https://github.com/pawamoy/pytkdocs/commit/19300544cb31f6ad6be5828d041022d7bf917668) by Wang Yuzhi).
- Fix attribute parser for Python 3.9 ([ae80e98](https://github.com/pawamoy/pytkdocs/commit/ae80e988edf362ce99a880063639e4cd74bc44bb) by Timothée Mazzucotelli). [Issue #73](https://github.com/pawamoy/pytkdocs/issues/73) and [#75](https://github.com/pawamoy/pytkdocs/issues/75)


## [0.10.0](https://github.com/pawamoy/pytkdocs/releases/tag/0.10.0) - 2020-12-06

<small>[Compare with 0.9.0](https://github.com/pawamoy/pytkdocs/compare/0.9.0...0.10.0)</small>

### Bug Fixes
- Avoid recursion if a class has a reference to itself ([c92a791](https://github.com/pawamoy/pytkdocs/commit/c92a7911ea9f6321614bb692960f5252f79f6320) by Matthew Wardrop).

### Features
- Add initial restructured text docstring parsing ([0b58c8d](https://github.com/pawamoy/pytkdocs/commit/0b58c8d64846d3fb87588a5cf154dbd5bf60accf) by Patrick Lannigan). Issue [#67](https://github.com/pawamoy/pytkdocs/issues/67), PR [#71](https://github.com/pawamoy/pytkdocs/issues/71)


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
