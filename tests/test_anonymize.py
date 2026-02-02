import unittest
from re_tan.name_helpers import anonymize

class AnonymizeTest(unittest.TestCase):
    def test_anonymize_basic(self):
        named = "Alice Smith.scan"
        matches = ["Alice", "Smith"]
        tan = "e22a"
        expected = "_e22a_scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_reverse(self):
        named = "MikeSilva blood test"
        matches = ["Silva", "Mike"]
        tan = "u2ae"
        expected = "_u2ae_blood_test"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_strip(self):
        named = "Alice. Smith.scan"
        matches = ["Smith ", " Alice."]
        tan = "e22a"
        expected = "_e22a_scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_case(self):
        named = "Alice smith.scan"
        matches = ["Smith", "alice"]
        tan = "e22a"
        expected = "_e22a_scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_normalize(self):
        named = "patient Alice smith.last version ScAn"
        matches = ["Smith", "alice"]
        tan = "e22a"
        expected = "_e22a_patient_last_version_scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_mismatch(self):
        named = "Adam smith.scan"
        matches = ["Smith", "alice"]
        tan = "e22a"
        expected = "Adam smith.scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_empty(self):
        named = "Alice smith.scan"
        matches = ["Smith", ""]
        tan = "e22a"
        expected = "Alice smith.scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_short_match(self):
        named = "Alice smith.scan"
        matches = ["Alice"]
        tan = "e22a"
        expected = "Alice smith.scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

    def test_anonymize_space_in_tan(self):
        named = "Alice smith.scan"
        matches = ["Alice", "smith"]
        tan = " e22a"
        expected = "_e22a_scan"

        self.assertEqual(anonymize(named, matches, tan), expected)

if __name__ == "__main__":
    unittest.main()