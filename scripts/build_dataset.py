#!/usr/bin/env python
"""Build the deterministic provisional dataset and family-disjoint splits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pocket_barrister.data.build import build_dataset  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=ROOT / "configs" / "dataset_provisional_v0.json",
    )
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    manifest = build_dataset(args.config, args.output_dir)
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
