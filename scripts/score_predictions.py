#!/usr/bin/env python
"""Score stored base/adapter prediction JSONL against inherited provisional states."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pocket_barrister.evaluation.metrics import aggregate_scores, score_prediction  # noqa: E402


def _read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument(
        "--references",
        type=Path,
        default=ROOT / "data" / "provisional_v0" / "splits" / "test.jsonl",
    )
    parser.add_argument("--details", type=Path)
    args = parser.parse_args()

    references = {row["sample_id"]: row for row in _read_jsonl(args.references)}
    predictions = _read_jsonl(args.predictions)
    expected_systems = {"base", "adapter"}
    seen_pairs: set[tuple[str, str]] = set()
    scores = []
    for prediction in predictions:
        sample_id = prediction.get("sample_id")
        system = prediction.get("system")
        if sample_id not in references:
            raise SystemExit(f"prediction references unknown sample: {sample_id}")
        if system not in expected_systems:
            raise SystemExit(f"invalid system for {sample_id}: {system}")
        pair = (sample_id, system)
        if pair in seen_pairs:
            raise SystemExit(f"duplicate prediction: {system}/{sample_id}")
        seen_pairs.add(pair)
        scores.append(score_prediction(references[sample_id], prediction))

    expected_pairs = {
        (sample_id, system) for sample_id in references for system in expected_systems
    }
    missing = sorted(expected_pairs - seen_pairs)
    if missing:
        raise SystemExit(f"missing {len(missing)} base/adapter predictions")

    if args.details:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        with args.details.open("w", encoding="utf-8", newline="\n") as handle:
            for score in scores:
                handle.write(json.dumps(score, sort_keys=True) + "\n")
    print(json.dumps(aggregate_scores(scores), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
