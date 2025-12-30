# Changelog

[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

---

This file documents all notable changes in the [blockie](https://github.com/lubomilko/blockie)
template engine project.

---

## [2.0.0] - 2026-mm-dd

### Changed

- Make the `get_subblock` method to always return a `Block` object.
- Replace the `Block.autotags` attribute with `Block.config.enable_autotags`.

### Added

- Add support for *subreferences* in variable values, i.e., tags referencing other variables or
  blocks using hierarchical parent-child tag names separated using a new `subref_sep` separator.
- Add recursive filling of variables and blocks referenced in variable values.
- Add *block variables* defined using the new `Block.config.autotag_blk_var` tag to set the block
  content into the specified variable instead of keeping it in its place.


## [1.1.0] - 2025-08-04

### Changed

- Do not generate whitespace alignment characters if there is no other non-whitespace character
  until the line end.

### Added

- Add implicit iterator tag `*` used by the `fill()` method when a block is filled with just a
  list/tuple of simple data types without an explicit variable name, e.g.,
  `fill({"list": ["a", "b", "c"]})` for filling a `<LIST><*>, </LIST>` template.

### Fixed

- Fix all violations in `blockie.py` related to the newly enabled *basic* type checking, i.e., the
  `"python.analysis.typeCheckingMode": "basic"` setting.


## [1.0.0] - 2025-05-18

The first release based on the older [blocky](https://github.com/lubomilko/blocky) project that
could not be published on PyPi due to a name conflict with another existing project. The sections
below describe modifications since the last
[blocky 1.4.0](https://github.com/lubomilko/blocky/releases/tag/1.4.0) release.

### Changed

- Rework and simplify the `BlockConfig` class. Use customizable formatter functions for the
  definition of tag strings.
- Change the standard `subclass` attribute to a `children` property attribute.
- Global refactoring to decrease the amount of code and increase efficiency and clarity.
- Simplify and update all docstrings relying more on the type hints and code itself.
- Execute the external fill handler `fill_hndl` by the `fill()` method before filling the content
  of a block, instead of after.

### Removed

- Remove the `BlockData` class since object of any type can be used for filling the template.
- Remove loading of a simple template string by the `load_template()` method, making it only
  load the template from a file.
- Remove the `*name_value_args` parameter from the `set_variables()` method, making it only
  accept the keyword arguments.

### Added

- Add an option to directly set the block variation index as an integer value to the block key in
  a dictionary provided to the `fill()` method.
- Add option to remove variables by setting them to an empty list or tuple in a dictionary 
  provided to the `fill()` method.
- Add multiple simple examples used in the documentation.
- Add Sphinx documentation.


[unreleased]: https://github.com/lubomilko/blockie
[2.0.0]: https://github.com/lubomilko/blockie/releases/tag/2.0.0
[1.1.0]: https://github.com/lubomilko/blockie/releases/tag/1.1.0
[1.0.0]: https://github.com/lubomilko/blockie/releases/tag/1.0.0
