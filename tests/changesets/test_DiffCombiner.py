import unittest
from pathlib import Path

from changesets.Change import Change
from changesets.ChangeSet import ChangeSet
from changesets.DiffCombiner import DiffCombiner


class TestDiffCombiner(unittest.TestCase):
    def setUp(self):
        self.set_one = ChangeSet("one", [Change("one", Path("first")), Change("one", Path("second"))])
        self.set_two = ChangeSet("two", [Change("two", Path("third"))])
        self.set_three = ChangeSet("two", [Change("two", Path("first")), Change("two", Path("fourth"))])
        self.diff_combiner = DiffCombiner()

    def test_disjoint(self):
        result = self.diff_combiner.combine([self.set_one, self.set_two])
        self.assertSetEqual(set(c.path for c in result.changes),
                            {Path("first"), Path("second"), Path("third")})

    def test_override(self):
        with self.assertRaises(RuntimeError) as error:
            result = self.diff_combiner.combine([self.set_one, self.set_three])
        self.assertEquals(error.exception.args[0], "duplicated entry")
