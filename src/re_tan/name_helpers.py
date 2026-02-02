import re
from pathlib import Path, PureWindowsPath

def normalize(raw: str) -> str:
    """
    Normalize a string for safe comparison:
    - Remove all dots and whitespace
    - Convert to lowercase

    Args:
        raw: input string

    Returns:
        Normalized string
    """
    return re.sub(r'[.\s]+', '', raw).lower()


def split_path(path: str) -> tuple[str, str, str]:
    """
    Split a path string into directory, filename (without extension), and extension.
    Handles both Linux/Unix (/) and Windows (\) paths.

    :param path: full file path string
    :return: tuple of (directory/path, filename without extension, extension)
    """
    if "\\" in path:
        p = PureWindowsPath(path)
    else:
        p = Path(path)

    return str(p.parent), p.stem, p.suffix

def contains_all(named: str, matches: list[str]) -> bool:
    """
    Check if all strings in `matches` are present in `named` after normalization.

    :param named: the main string to check
    :param matches: list of substrings to look for
    :return: True if all matches are in named, False otherwise
    """
    if "" in matches or len(matches) < 2:
        return False
    normalized_named = normalize(named)
    return all(normalize(m) in normalized_named for m in matches)


def anonymize(named: str, matches: list[str], tan: str) -> str:
    """
    Remove all `matches` from `named`, collapse dots/spaces/underscores,
    convert to lowercase, and prefix with _<tan>_.
    Returns the original string if any match is missing.
    """
    cleared = named.lower()  # convert everything to lowercase

    # Check all matches exist using normalized strings
    normalized = normalize(cleared)

    if "" in matches or len(matches) < 2:
        return named

    for m in matches:
        if normalize(m) not in normalized:
            return named

    # Remove matches from cleared string
    for m in matches:
        cleared = re.sub(re.escape(m.strip().lower()), "", cleared, flags=re.IGNORECASE)

    # Clean string: remove dots, collapse spaces/underscores, strip
    cleared = re.sub(r'[.\s_]+', "_", cleared).strip("_")

    return f"_{normalize(tan)}_{cleared}"