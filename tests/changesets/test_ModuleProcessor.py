import os
import unittest
from pathlib import Path
from shutil import rmtree

from changesets.DiffGenerator import DiffGenerator


class TestModuleProcessor(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(os.path.dirname(__file__))
        self.original_dir = self.base_dir.joinpath("original")
        self.patched_dir = self.base_dir.joinpath("patched")
        self.differ = DiffGenerator()

    def test_module_a(self):
        changeset = self.differ.diff(Path("module_a"), self.original_dir, self.patched_dir)
        self.assertEqual(changeset.path, self.patched_dir)
        self.assertEqual(set(c.path for c in changeset.changes), {Path('new_file')})

    def test_module_b(self):
        changeset = self.differ.diff(Path("module_b"), self.original_dir, self.patched_dir)
        self.assertEqual(changeset.path, self.patched_dir)
        self.assertSetEqual(set(c.path for c in changeset.changes), {Path('updated_file'), Path('updated_from_another_module')})
