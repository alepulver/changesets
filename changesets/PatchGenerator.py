import shutil
from pathlib import Path


class PatchGenerator:
    def __init__(self, changeset):
        self.changeset = changeset

    def patch_dir(self, output_dir):
        for file in self.changeset.files:
            src_file = self.changeset.path / file
            dst_file = output_dir / file
            dst_dir = Path(dst_file).parent
            dst_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(str(src_file), str(dst_file))

    def report(self):
        pass
