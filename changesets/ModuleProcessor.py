import shutil
import subprocess
from pathlib import Path

from changesets.DiffCombiner import DiffCombiner
from changesets.DiffGenerator import DiffGenerator


class ModuleProcessor:
    def __init__(self, original, patched):
        self.original = original
        self.patched = patched
        self.diff_generator = DiffGenerator()
        self.diff_combiner = DiffCombiner()

    def diff(self):
        modules = [self.module_name(m) for m in self.find_modules()]

        changesets = []
        for m in modules:
            change_set = self.diff_generator.diff(m, self.original, self.patched)
            changesets.append(change_set)

        result = self.diff_combiner.combine(changesets)
        return result

    def find_modules(self):
        command = ["find", str(self.original), "-path", "*/target/classes"]
        module_dirs = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')
        module_dirs = [Path(d.decode()).resolve() for d in module_dirs if len(d) > 0]
        return module_dirs

    def module_name(self, path):
        module_relpath = path.relative_to(self.original)
        #module_name = module_relpath.parents[1]
        module_name = module_relpath
        return module_name

