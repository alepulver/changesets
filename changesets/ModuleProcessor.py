import shutil
import subprocess
from pathlib import Path

from changesets.DiffCombiner import DiffCombiner
from changesets.DiffGenerator import DiffGenerator


class ModuleProcessor:
    def __init__(self, original, patched):
        self.original = original
        self.patched = patched
        self.filesets = None
        self.diff_generator = DiffGenerator()
        self.diff_combiner = DiffCombiner()

    def diff(self):
        modules = self.find_modules()
        changesets = [self.diff_generator.diff(m) for m in modules]
        result = self.diff_combiner.combine(changesets)
        return result

    def find_modules(self):
        command = ["find", str(self.original), "-path", "*/target/classes"]
        module_dirs = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')
        module_dirs = [Path(d.decode()).resolve() for d in module_dirs if len(d) > 0]
        return module_dirs

    def module_name(self, path):
        module_relpath = path.relative_to(self.original)
        module_name = module_relpath.parents[1]
        return module_name

