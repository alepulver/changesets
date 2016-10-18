import shutil
from pathlib import Path


class PatchGenerator:
    def __init__(self, changeset):
        self.changeset = changeset

    def patch_dir(self, output_dir):
        for change in self.changeset.changes:
            src_file = change.module / change.path
            dst_file = output_dir / change.path
            dst_dir = Path(dst_file).parent
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(src_file), str(dst_file))

    def report(self):
        files_by_module = {}
        for change in self.changeset.changes:
            if change.module not in files_by_module:
                files_by_module[change.module] = []
            files_by_module[change.module].append(change.path)

        for k, v in files_by_module.items():
            module = k.relative_to(self.changeset.path)
            print("{}: {}".format(module, ", ".join(str(path) for path in v)))
