"""Verify that the immutable legacy snapshot matches its recorded manifest.

This script is read-only. It reports changed, missing, and unexpected files and
returns a non-zero exit status if any drift is detected.
"""

from __future__ import annotations

import hashlib
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = REPOSITORY_ROOT / "experiments" / "legacy_v0"
MANIFEST_PATH = REPOSITORY_ROOT / "manifests" / "legacy_v0.sha256"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_manifest() -> dict[str, str]:
    expected: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        MANIFEST_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            digest, relative_path = line.split("  ", maxsplit=1)
        except ValueError as error:
            raise ValueError(f"Malformed manifest line {line_number}: {raw_line!r}") from error
        if not relative_path.startswith("experiments/legacy_v0/"):
            raise ValueError(
                f"Manifest path escapes the legacy snapshot on line {line_number}: {relative_path}"
            )
        expected[relative_path] = digest.casefold()
    return expected


def main() -> int:
    expected = load_manifest()
    actual_paths = {
        path.relative_to(REPOSITORY_ROOT).as_posix(): path
        for path in LEGACY_ROOT.rglob("*")
        if path.is_file()
    }

    missing = sorted(set(expected) - set(actual_paths))
    unexpected = sorted(set(actual_paths) - set(expected))
    changed = sorted(
        relative_path
        for relative_path in set(expected) & set(actual_paths)
        if sha256(actual_paths[relative_path]) != expected[relative_path]
    )

    if missing or unexpected or changed:
        print("Legacy snapshot verification FAILED.")
        for label, paths in (
            ("Missing", missing),
            ("Unexpected", unexpected),
            ("Changed", changed),
        ):
            if paths:
                print(f"{label} files ({len(paths)}):")
                for path in paths:
                    print(f"  {path}")
        return 1

    print(f"Legacy snapshot verified: {len(expected)} files match the manifest.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

