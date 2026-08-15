#!/usr/bin/env python
"""Verify an extracted Colab evidence or adapter bundle against its checksums."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    root = args.bundle.resolve()
    checksum_path = root / "checksums.sha256"
    if not checksum_path.is_file():
        raise SystemExit(f"missing checksum manifest: {checksum_path}")

    expected: dict[str, str] = {}
    for line_number, raw_line in enumerate(
        checksum_path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not raw_line.strip():
            continue
        try:
            digest, relative = raw_line.split("  ", maxsplit=1)
        except ValueError as error:
            raise SystemExit(f"malformed checksum line {line_number}") from error
        candidate = (root / relative).resolve()
        try:
            candidate.relative_to(root)
        except ValueError as error:
            raise SystemExit(f"checksum path escapes bundle: {relative}") from error
        expected[relative] = digest.casefold()

    actual = {
        path.relative_to(root).as_posix(): path
        for path in root.rglob("*")
        if path.is_file() and path != checksum_path
    }
    missing = sorted(set(expected) - set(actual))
    unexpected = sorted(set(actual) - set(expected))
    changed = sorted(
        relative
        for relative in set(expected) & set(actual)
        if sha256(actual[relative]) != expected[relative]
    )
    if missing or unexpected or changed:
        print("Evidence bundle verification FAILED.")
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
    print(f"Evidence bundle verified: {len(expected)} files match checksums.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
