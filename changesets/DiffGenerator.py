import subprocess
from pathlib import Path

from changesets.Change import Change
from changesets.ChangeSet import ChangeSet


class DiffGenerator:
    def diff(self, module, original_basedir, patched_basedir):
        original = original_basedir / module
        patched = patched_basedir / module
        command = ["rsync", "--exclude", "/codecheck", "--exclude", "META-INF",
                   "-rnic", str(patched) + '/', str(original)]
        files = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')

        files = [line.decode() for line in files]
        files = [line[10:] for line in files if len(line) > 0 and line[:2] == '>f']
        files = [Path(fn) for fn in files]
        changes = [Change(patched, fn) for fn in files]

        return ChangeSet(patched_basedir, changes)
