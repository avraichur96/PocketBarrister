"""Verify the immutable legacy snapshot without mutating it.

Git-tracked text is hashed after newline normalization so Windows and Linux
checkouts verify identically. Large local-only artifacts are verified when
present and are required only with --require-local-artifacts.
"""

from __future__ import annotations

import argparse
import hashlib
from dataclasses import dataclass
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = REPOSITORY_ROOT / "experiments" / "legacy_v0"
PORTABLE_MANIFEST = REPOSITORY_ROOT / "manifests" / "legacy_v0.sha256"
LOCAL_MANIFEST = REPOSITORY_ROOT / "manifests" / "legacy_v0.local-artifacts.sha256"
VALID_MODES = {"binary", "text-lf"}


@dataclass(frozen=True)
class ManifestEntry:
    digest: str
    mode: str


def sha256(path: Path, mode: str) -> str:
    data = path.read_bytes()
    if mode == "text-lf":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_manifest(path: Path) -> dict[str, ManifestEntry]:
    expected: dict[str, ManifestEntry] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        try:
            digest, mode, relative_path = line.split("  ", maxsplit=2)
        except ValueError as error:
            raise ValueError(
                f"Malformed {path.name} line {line_number}: {raw_line!r}"
            ) from error
        if mode not in VALID_MODES:
            raise ValueError(f"Invalid hash mode on {path.name} line {line_number}: {mode}")
        if not relative_path.startswith("experiments/legacy_v0/"):
            raise ValueError(
                f"Manifest path escapes the legacy snapshot on line {line_number}: "
                f"{relative_path}"
            )
        expected[relative_path] = ManifestEntry(digest.casefold(), mode)
    return expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--require-local-artifacts",
        action="store_true",
        help="Fail if any of the four gitignored local legacy artifacts are absent.",
    )
    args = parser.parse_args()

    portable = load_manifest(PORTABLE_MANIFEST)
    local_only = load_manifest(LOCAL_MANIFEST)
    known = set(portable) | set(local_only)
    actual_paths = {
        path.relative_to(REPOSITORY_ROOT).as_posix(): path
        for path in LEGACY_ROOT.rglob("*")
        if path.is_file()
    }

    missing_portable = sorted(set(portable) - set(actual_paths))
    missing_local = sorted(set(local_only) - set(actual_paths))
    unexpected = sorted(set(actual_paths) - known)
    changed_portable = sorted(
        relative_path
        for relative_path, entry in portable.items()
        if relative_path in actual_paths
        and sha256(actual_paths[relative_path], entry.mode) != entry.digest
    )
    changed_local = sorted(
        relative_path
        for relative_path, entry in local_only.items()
        if relative_path in actual_paths
        and sha256(actual_paths[relative_path], entry.mode) != entry.digest
    )

    failed = bool(
        missing_portable
        or unexpected
        or changed_portable
        or changed_local
        or (args.require_local_artifacts and missing_local)
    )
    if failed:
        print("Legacy snapshot verification FAILED.")
        groups = [
            ("Missing portable", missing_portable),
            ("Missing required local artifact", missing_local if args.require_local_artifacts else []),
            ("Unexpected", unexpected),
            ("Changed portable", changed_portable),
            ("Changed local artifact", changed_local),
        ]
        for label, paths in groups:
            if paths:
                print(f"{label} files ({len(paths)}):")
                for path in paths:
                    print(f"  {path}")
        return 1

    present_local = len(local_only) - len(missing_local)
    print(
        f"Legacy portable snapshot verified: {len(portable)} files; "
        f"optional local artifacts present: {present_local}/{len(local_only)}."
    )
    if missing_local:
        print("Optional local artifacts are absent as expected in a Git/Colab checkout.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
