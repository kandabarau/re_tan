#!/usr/bin/env python3
"""
Omics Anonymizer: Matches filenames against a TAN database to suggest renames.
Ensures strict 1-to-1 matching to prevent sample swaps.
"""

import csv
import subprocess
import argparse
from pathlib import Path
from re_tan.name_helpers import split_path, contains_all, anonymize


def main():
    # --- 1. Argument Parsing ---
    parser = argparse.ArgumentParser(description="Anonymize omics filenames based on a TAN mapping.")
    parser.add_argument("--files", type=str, required=True, help="Path to txt file with file paths")
    parser.add_argument("--tans", type=str, required=True, help="Path to tan.csv database")
    parser.add_argument("--out", type=str, help="Optional: Custom output path")
    args = parser.parse_args()

    # --- 2. Path Setup ---
    FILES_PATH = Path(args.files)
    TANS_PATH = Path(args.tans)

    # Define the output file path dynamically or via argument
    if args.out:
        RENAME_SUGGESTION_FILE = Path(args.out)
    else:
        # Default to results/rename_[input_filename]
        RENAME_SUGGESTION_FILE = Path("results") / f"rename_{FILES_PATH.name}"

    # Ensure the parent directory (e.g., results/) exists
    RENAME_SUGGESTION_FILE.parent.mkdir(exist_ok=True)

    # --- 3. Load Subject Database (TAN, Name1, Name2) ---
    subjects = []
    with open(TANS_PATH, mode="r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 3:
                subjects.append(row)

    # --- 4. Process Filenames ---
    with FILES_PATH.open(encoding="latin-1") as f:
        lines = f.read().splitlines()

    with open(RENAME_SUGGESTION_FILE, "w", encoding="utf-8") as out_file:
        # Write TSV Header
        out_file.write("directory\toriginal_name\textension\tsuggested_rename\n")

        for line in lines:
            if not line.strip():
                continue

            directory, named, extension = split_path(line)
            potential_matches = []

            # Search database for all matching subjects
            for row in subjects:
                tan, name1, name2 = row[0], row[1], row[2]
                if contains_all(named, [name1, name2]):
                    potential_matches.append(anonymize(named, [name1, name2], tan))

            # Logic: If multiple subjects match one file, leave it empty (Ambiguity check)
            if len(potential_matches) == 1:
                rename_suggestion = potential_matches[0]
            elif len(potential_matches) > 1:
                rename_suggestion = ""
                print(f"  ! Warning: {named} is ambiguous (multiple matches).")
            else:
                rename_suggestion = ""

            # Save the suggestion to the output file
            out_file.write(f"{directory}\t{named}\t{extension}\t{rename_suggestion}\n")

            status = f"-> {rename_suggestion}" if rename_suggestion else "(no match/ambiguous)"
            print(f"Processed: {named} {status}")

    # --- 5. Final Report ---
    print(f"\nDone! Results saved to: {RENAME_SUGGESTION_FILE}")
    print("-" * 30 + "\nPreview of results:")
    subprocess.run(["head", "-n", "5", str(RENAME_SUGGESTION_FILE)])
    print("-" * 30)


if __name__ == "__main__":
    main()