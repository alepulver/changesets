import os
import unittest
from pathlib import Path

from changesets.ModuleProcessor import ModuleProcessor


class TestModuleProcessor(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(os.path.dirname(__file__))
        self.original_dir = self.base_dir.joinpath("original")
        self.patched_dir = self.base_dir.joinpath("patched")
        self.processor = ModuleProcessor(self.original_dir, self.patched_dir)

    def test_module_a(self):
        changeset = self.processor.diff("*/module_a")
        self.assertEqual(set(c.path for c in changeset.changes), {Path("new_file")})
