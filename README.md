# Changesets

## Introduction

This Python package integrates change detection with `rsync` in multiple directories,
which share the same underlying structure. The objective is to simplify the creation of Mule Runtime patches.

## Installation

First, clone this repository.

This program requires Python >= 3.5. You can use [pyenv](https://github.com/yyuu/pyenv) to manage multiple versions,
or alternatively install Python 3 from your system package manager such as `apt-get` or `brew`. 

To run tests use `nosetests`.

## Usage

### Creating patches

```bash
# Start from you local project
cd mule

# Create two worktrees, one for the original release and another one for the patched variant
git worktree add -f ../mule-3.7.5-original mule-3.7.5
git worktree add -f ../mule-3.7.5-patched mule-3.7.5

# Apply cherry-picks and resolve conflicts
cd ../mule-3.7.5-patched
git cherry-pick ...

# Build both
cd ../mule-3.7.5-original
mvn clean compile -T 1C
cd ../mule-3.7.5-patched
mvn clean compile -T 1C

# Generate the patch
cd ..
mkdir -p patch_dir
python3 changesets/main.py mule-3.7.5-original mule-3.7.5patched patch_dir
cd patch_dir
jar -cf ../SE-combined/jar *
```

If the patch includes *mule-ee*, then the same process has to be repeated.

### Checking for patch conflicts

Checks for conflicts between patches, and outputs where it is if found.

```bash
python3 changesets/patch_analyzer/patch_conflicts.py SE-123.jar SE-456.jar ...
```

### Checking for patch applicability to another version

This command requires the Mule CE and Mule EE git repositories (it doesn't matter which branch they are on). It takes
a patch for 3.7.4 and checks if it will work on 3.7.5, otherwise will output changed classes.

```bash
python3 changesets/patch_analyzer/patch_applicable_version.py SE-123.jar mule mule-ee 3.7.4 3.7.5
```