import unittest
from re_tan.name_helpers import split_path

class SplitPathTest(unittest.TestCase):

    def test_split_path_basic(self):
        path = "/home/users/database/studies/subjects/MikeSilva.blood.test.txt"
        expected = ("/home/users/database/studies/subjects", "MikeSilva.blood.test", ".txt")
        self.assertEqual(split_path(path), expected)

    def test_split_path_windows(self):
        path = r"C:\Study Data\MikeSilva blood test.txt"
        expected = (r"C:\Study Data", "MikeSilva blood test", ".txt")
        self.assertEqual(split_path(path), expected)

if __name__ == "__main__":
    unittest.main()