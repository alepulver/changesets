import subprocess
import sys
import os
from pathlib import Path


# http://andreafrancia.it/2010/03/understanding-the-output-of-rsync-itemize-changes.html
from changesets.ChangeSet import FileSet
from changesets.ModuleProcessor import ModuleDiffer
from changesets.PatchGenerator import PatchGenerator


def main(args):
    if len(args) != 3:
        print("Usage: <command> <original_dir> <patched_dir> <output_dir>", file=sys.stderr)
        sys.exit(1)

    original_dir = Path(args[0]).resolve()
    patched_dir = Path(args[1]).resolve()
    output_dir = Path(args[2]).resolve()

    differ = ModuleDiffer(original_dir, patched_dir)
    changesets = differ.diff()

    for f in changesets:
        print("{}: {}".format(f.module, ", ".join(f.files)))

    differ.patch_dir(Path("blah"))

    patchgen = PatchGenerator(changesets, output_dir)

if __name__ == "__main__":
    main(sys.argv[1:])
