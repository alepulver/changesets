# Changesets

## Introduction

This Python package integrates change detection with `rsync` in multiple directories,
which share the same underlying structure. The objective is to simplify the creation of patches.

## Installation

TODO

To run tests use `nosetests`.

## Usage

```
$ find original -type f
...

$ find patched -type f
...

$ python main.py original patched output
...
```