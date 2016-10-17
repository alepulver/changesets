import os
import shutil
import unittest
from pathlib import Path

from changesets.DiffGenerator import DiffGenerator
from changesets.PatchGenerator import PatchGenerator


class TestPatchGenerator(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(os.path.dirname(__file__))
        self.original_dir = self.base_dir.joinpath("original")
        self.patched_dir = self.base_dir.joinpath("patched")
        self.output_dir = self.base_dir.joinpath("output")
        self.differ = DiffGenerator()

    def tearDown(self):
        shutil.rmtree(str(self.output_dir.absolute()))

    def test_module_a(self):
        target_dir = self.patched_dir / "module_a"
        changeset = self.differ.diff(self.original_dir / "module_a", target_dir)
        patcher = PatchGenerator(changeset)
        patcher.patch_dir(self.output_dir)

        self.assertTrue((self.output_dir / 'new_file').exists())
        self.assertFalse((self.output_dir / 'unchanged_file').exists())
        self.assertFalse((self.output_dir / 'updated_from_another_module').exists())

    def test_module_b(self):
        target_dir = self.patched_dir / "module_b"
        changeset = self.differ.diff(self.original_dir / "module_b", target_dir)
        patcher = PatchGenerator(changeset)
        patcher.patch_dir(self.output_dir)

        self.assertFalse((self.output_dir / 'deleted_file').exists())
        self.assertTrue((self.output_dir / 'updated_file').exists())
        self.assertTrue((self.output_dir / 'updated_from_another_module').exists())
