# Changesets

## Introduction

This Python package integrates change detection with `rsync` in multiple directories,
which share the same underlying structure. The objective is to simplify the creation of patches.

## Installation

TODO

To run tests use `nosetests`.

## Usage

This program requires Python >= 3.5. To manage versions you can use [pyenv](https://github.com/yyuu/pyenv).

```
$ python main.py original patched output
```

Where `output` is an existing directory, and `original` shares the underlying `target/classes` structure with `patched`.

## TODO

- automate generating patches starting from one commit and including cherry picks
- only test changed modules
- use git to estimate changed modules by looking at module folders, to avoid building everything