import unittest
from unittest.mock import patch, mock_open, MagicMock
import sys  # Need this to mock argv

# Import your script
from rename_subjects import main


class TestMainWorkflow(unittest.TestCase):

    # 1. Add a patch for sys.argv to simulate the command line input
    @patch("sys.argv", ["rename_subjects.py", "--files", "fake_files.txt", "--tans", "fake_tans.csv"])
    @patch("pathlib.Path.open", new_callable=mock_open,
           read_data="C:\\Data\\Alice_Smith_WGS.vcf\nC:\\Data\\Ambiguous_Name.bam")
    @patch("builtins.open", new_callable=mock_open)
    @patch("rename_subjects.split_path")
    @patch("subprocess.run")
    def test_main_strict_logic(self, mock_subproc, mock_split, mock_file_write, mock_path_open):
        mock_subjects = [
            ["e22a", "Alice", "Smith"],
            ["1111", "Ambiguous", "Name"],
            ["2222", "Ambiguous", "Name"]
        ]

        mock_split.side_effect = [
            ("C:\\Data", "Alice_Smith_WGS", ".vcf"),
            ("C:\\Data", "Ambiguous_Name", ".bam")
        ]

        # Patch internal checks
        with patch("csv.reader", return_value=mock_subjects):
            # Also patch mkdir so it doesn't actually create folders during testing
            with patch("pathlib.Path.mkdir"):
                with patch("pathlib.Path.exists", return_value=True):
                    main()

        # Get the content written to the file
        written_content = "".join(call.args[0] for call in mock_file_write().write.call_args_list)

        # Assertions
        self.assertIn("_e22a_wgs", written_content)
        self.assertIn("Ambiguous_Name\t.bam\t\n", written_content)


if __name__ == "__main__":
    unittest.main()