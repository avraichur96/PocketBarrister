#!/usr/bin/env python
"""Validate a generated Pocket Barrister JSONL dataset."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pocket_barrister.data.schema import validate_dataset  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=ROOT / "data" / "provisional_v0" / "dataset.jsonl",
    )
    args = parser.parse_args()
    with args.path.open("r", encoding="utf-8") as handle:
        records = [json.loads(line) for line in handle if line.strip()]
    errors = validate_dataset(records)
    if errors:
        print("Dataset validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    splits = sorted({record["split"] for record in records})
    families = {record["behavior_family"] for record in records}
    print(
        f"Dataset valid: {len(records)} records, {len(families)} families, "
        f"splits={','.join(splits)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
