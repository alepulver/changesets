import subprocess
import sys
import os
from pathlib import Path

# http://andreafrancia.it/2010/03/understanding-the-output-of-rsync-itemize-changes.html
from changesets.ModuleProcessor import ModuleProcessor
from changesets.PatchGenerator import PatchGenerator


def main(args):
    if len(args) != 3:
        print("Usage: <command> <original_dir> <patched_dir> <output_dir>", file=sys.stderr)
        sys.exit(1)

    original_dir = Path(args[0]).resolve()
    patched_dir = Path(args[1]).resolve()
    output_dir = Path(args[2]).resolve()

    processor = ModuleProcessor(original_dir, patched_dir)
    changeset = processor.diff("*/target/classes", ["META-INF", "/codecheck"])

    patch_generator = PatchGenerator(changeset)
    patch_generator.report()
    patch_generator.patch_dir(output_dir)


if __name__ == "__main__":
    main(sys.argv[1:])
