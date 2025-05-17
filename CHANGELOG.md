# Changelog

[![Common Changelog](https://common-changelog.org/badge.svg)](https://common-changelog.org)

---

This file documents all notable changes in the [blockie](https://github.com/lubomilko/blockie)
template engine project.

---


## [unreleased] - 202y-mm-dd




## [1.0.0] - 2024-01-05

First release based on the [blocky](https://github.com/lubomilko/blocky) project that could not be
published on PyPi due to a name conflict with another existing project. The sections below
describe modifications since the last release 1.4.0 of *blocky*.

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
[1.0.0]: https://github.com/lubomilko/blockie/releases/tag/1.0.0
