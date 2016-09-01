import unittest
from pathlib import Path
from shutil import rmtree


class TestModuleDiffer(unittest.TestCase):
    def setUp(self):
        self.base_dir = Path(".")
        self.original_dir = self.base_dir.joinpath("original")
        self.patched_dir = self.base_dir.joinpath("patched")
        self.output_dir = self.base_dir.joinpath("output")

        self.output_dir.mkdir(parents=True)

    def tearDown(self):
        rmtree(str(self.output_dir))

    def test_newFile(self):
        pass

    def test_updatedFileWithSameTimestamp(self):
        pass

    def test_sameFileWithDifferentTimestamp(self):
        pass

    def test_removedFile(self):
        pass

    def test_duplicatedFinalPathButDifferentModules(self):
        pass
