import unittest
from re_tan.name_helpers import contains_all

class ContainsBothTest(unittest.TestCase):
    def test_contains_all_basic(self):
        named = "Alice Smith.scan"
        matches = ["Alice", "Smith"]

        self.assertTrue(contains_all(named, matches))

    def test_contains_all_empty(self):
        named = "Alice Smith.scan"
        matches = ["Alice", ""]

        self.assertFalse(contains_all(named, matches))

    def test_contains_all_short(self):
        named = "Alice Smith.scan"
        matches = ["Smith"]

        self.assertFalse(contains_all(named, matches))

if __name__ == "__main__":
    unittest.main()