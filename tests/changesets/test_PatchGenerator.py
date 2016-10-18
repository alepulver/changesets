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
        self.differ = DiffGenerator(self.original_dir, self.patched_dir)

    def tearDown(self):
        shutil.rmtree(str(self.output_dir.absolute()))

    def test_module_a(self):
        changeset = self.differ.diff("module_a")
        patcher = PatchGenerator(changeset)
        patcher.patch_dir(self.output_dir)

        self.assertTrue((self.output_dir / 'new_file').exists())
        self.assertFalse((self.output_dir / 'unchanged_file').exists())
        self.assertFalse((self.output_dir / 'updated_from_another_module').exists())

    def test_module_b(self):
        changeset = self.differ.diff("module_b")
        patcher = PatchGenerator(changeset)
        patcher.patch_dir(self.output_dir)

        self.assertFalse((self.output_dir / 'deleted_file').exists())
        self.assertTrue((self.output_dir / 'updated_file').exists())
        self.assertTrue((self.output_dir / 'updated_from_another_module').exists())
