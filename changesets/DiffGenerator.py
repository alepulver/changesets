import subprocess
from pathlib import Path

from changesets.ChangeSet import ChangeSet


class DiffGenerator:
    def diff(self, original, patched):
        command = ["rsync", "--exclude", "/codecheck", "--exclude", "META-INF",
                   "-rnic", str(patched) + '/', str(original)]
        changed_files = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')

        changed_files = [line.decode() for line in changed_files]
        changed_files = [line[10:] for line in changed_files if len(line) > 0 and line[:2] == '>f']
        changed_files = [Path(fn) for fn in changed_files]

        return ChangeSet(patched, changed_files)