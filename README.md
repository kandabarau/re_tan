![Tests](https://github.com/kandabarau/re_tan/actions/workflows/tests.yml/badge.svg)
# re_tan

A minimalist anonymizer for omics filenames. Matches sample names against a TAN database using strict 1-to-1 logic to prevent sample swaps.

## Setup

```
pip install -e .
```

## Usage

```
python3 rename_subjects.py \
  --files input.txt \  # List of raw file paths (both windows and unix) to be renamed
  --tans tan.csv       # Database with [TAN, Name1, Name2] mapping
```

## Testing

```
export PYTHONPATH=$PYTHONPATH:src
python3 -m unittest discover tests
```
