import subprocess
from pathlib import Path

from changesets.Change import Change
from changesets.ChangeSet import ChangeSet


class DiffGenerator:
    def __init__(self, original_basedir, patched_basedir):
        self.original_basedir = original_basedir
        self.patched_basedir = patched_basedir

    def diff(self, module, exclude_expressions=[]):
        original = self.original_basedir / module
        patched = self.patched_basedir / module

        exclude_args = []
        for expression in exclude_expressions:
            exclude_args.append("--exclude")
            exclude_args.append(expression)

        command = ["rsync"] + exclude_args + ["-rnic", str(patched) + '/', str(original)]
        files = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')

        files = [line.decode() for line in files]
        files = [line[10:] for line in files if len(line) > 0 and line[:2] == '>f']
        files = [Path(fn) for fn in files]
        changes = [Change(patched, fn) for fn in files]

        return ChangeSet(self.patched_basedir, changes)
