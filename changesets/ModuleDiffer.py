import shutil
import subprocess
from pathlib import Path

from changesets.ChangeSet import FileSet


class ModuleDiffer:
    def __init__(self, original, patched):
        self.original = original
        self.patched = patched
        self.filesets = None

    def diff(self):
        modules = self.find_modules()
        filesets = [FileSet(self.module_name(m), self.diff_module(m)) for m in modules]
        self.filesets = [f for f in filesets if len(f.files) > 0]
        return self.filesets

    def find_modules(self):
        command = ["find", str(self.original), "-path", "*/target/classes"]
        module_dirs = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')
        module_dirs = [Path(d.decode()).resolve() for d in module_dirs if len(d) > 0]
        return module_dirs

    def diff_module(self, module_dir):
        module_relpath = module_dir.relative_to(self.original)
        module_name = module_relpath.parents[1]

        command = ["rsync", "--exclude", "/codecheck", "--exclude", "META-INF",
                   "-rnic", str(self.patched / module_relpath) + '/', str(self.original / module_relpath)]
        changed_files = subprocess.run(command, stdout=subprocess.PIPE).stdout.split(b'\n')

        changed_files = [line.decode() for line in changed_files]
        changed_files = [line[10:] for line in changed_files if len(line) > 0 and line[:2] == '>f']
        return changed_files

    def module_name(self, path):
        module_relpath = path.relative_to(self.original)
        module_name = module_relpath.parents[1]
        return module_name

    def prepare_patch(self, output_dir):
        for fileset in self.filesets:
            for file in fileset.files:
                src_file = self.patched / fileset.module / "target" / "classes" / file
                dst_file = output_dir / file
                dst_dir = Path(dst_file).parent
                dst_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(str(src_file), str(dst_file))
                #print("({}) {} -> {}".format(fileset.module, src_file, dst_file))
