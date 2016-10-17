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
        target_dir = self.patched_dir / "module_a"
        changeset = self.differ.diff(self.original_dir / "module_a", target_dir)
        self.assertEqual(changeset.path, target_dir)
        self.assertEqual(changeset.files, [Path('new_file')])

    def test_module_b(self):
        target_dir = self.patched_dir / "module_b"
        changeset = self.differ.diff(self.original_dir / "module_b", target_dir)
        self.assertEqual(changeset.path, target_dir)
        self.assertSetEqual(set(changeset.files), set([Path('updated_file'), Path('updated_from_another_module')]))
