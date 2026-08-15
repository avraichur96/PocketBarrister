#!/usr/bin/env python
"""Create a complete provisional evaluation evidence set from raw predictions."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from pocket_barrister.evaluation.metrics import (  # noqa: E402
    score_prediction,
    summarize_with_confidence,
)

DISPLAY_METRICS = (
    "section_adherence",
    "actual_eos_stop",
    "findings_exact_pair_f1",
    "primary_doctrine_decision_accuracy",
    "conclusion_label_accuracy_heuristic",
    "internal_contradiction",
    "malformed_output",
    "generated_token_count",
)
FAILURE_METRICS = (
    "section_adherence",
    "actual_eos_stop",
    "primary_doctrine_decision_accuracy",
    "conclusion_label_accuracy_heuristic",
)


def _read_jsonl(path: Path) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def _write_jsonl(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _metric_table(summary: dict) -> list[dict]:
    rows = []
    for metric in DISPLAY_METRICS:
        base = summary["systems"]["base"]["metrics"][metric]
        adapter = summary["systems"]["adapter"]["metrics"][metric]
        delta = summary["adapter_minus_base"][metric]
        rows.append(
            {
                "metric": metric,
                "base_mean": base["mean"],
                "base_ci95_low": base["ci95_low"],
                "base_ci95_high": base["ci95_high"],
                "adapter_mean": adapter["mean"],
                "adapter_ci95_low": adapter["ci95_low"],
                "adapter_ci95_high": adapter["ci95_high"],
                "adapter_minus_base": delta["mean"],
                "delta_ci95_low": delta["ci95_low"],
                "delta_ci95_high": delta["ci95_high"],
            }
        )
    return rows


def _write_metrics_markdown(path: Path, summary: dict, table: list[dict], failures: int) -> None:
    lines = [
        "# Automatic Metrics",
        "",
        "> Provisional engineering evidence only. Expected states are inherited from legally unreviewed synthetic data.",
        "",
        f"Test cases: {summary['systems']['base']['n']} (the same paired cases for base and adapter).",
        "",
        "| Metric | Base (95% CI) | Adapter (95% CI) | Adapter − base (95% CI) |",
        "|---|---:|---:|---:|",
    ]
    for row in table:
        lines.append(
            "| {metric} | {base_mean:.3f} [{base_ci95_low:.3f}, {base_ci95_high:.3f}] "
            "| {adapter_mean:.3f} [{adapter_ci95_low:.3f}, {adapter_ci95_high:.3f}] "
            "| {adapter_minus_base:+.3f} [{delta_ci95_low:+.3f}, {delta_ci95_high:+.3f}] |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            f"Automatically flagged system/case outputs: {failures}.",
            "",
            "## Metric boundaries",
            "",
            "- `primary_doctrine_decision_accuracy` compares the family-specific doctrine finding key with its inherited expected Yes/No value.",
            "- `conclusion_label_accuracy_heuristic` uses an explicit keyword pattern over the visible conclusion; it is not human legal grading.",
            "- `internal_contradiction` applies a small published rule set to parsed findings and the conclusion.",
            "- Wilson intervals are used for binary proportions; deterministic bootstrap intervals are used for other means and paired deltas.",
            "- Higher is better except for `internal_contradiction`, `malformed_output`, and usually response length/token count; their negative deltas indicate improvement.",
            "- Party-role correctness, full legal-effect consistency, unsupported legal claims, and legal correctness require the accompanying manual review.",
            "",
        ]
    )
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines))


def _write_manual_review(
    path: Path, references: dict[str, dict], predictions: dict[tuple[str, str], dict]
) -> None:
    fields = [
        "sample_id",
        "behavior_family",
        "expected_conclusion",
        "base_prediction",
        "adapter_prediction",
        "base_role_binding_correct",
        "adapter_role_binding_correct",
        "base_primary_doctrine_correct",
        "adapter_primary_doctrine_correct",
        "base_legal_effect_chain_consistent",
        "adapter_legal_effect_chain_consistent",
        "base_final_conclusion_correct",
        "adapter_final_conclusion_correct",
        "base_internal_contradiction",
        "adapter_internal_contradiction",
        "base_unsupported_legal_claim",
        "adapter_unsupported_legal_claim",
        "reviewer",
        "reviewed_at",
        "notes",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for sample_id, reference in sorted(references.items()):
            writer.writerow(
                {
                    "sample_id": sample_id,
                    "behavior_family": reference["behavior_family"],
                    "expected_conclusion": reference["expected_state"]["conclusion"],
                    "base_prediction": predictions[(sample_id, "base")]["prediction"],
                    "adapter_prediction": predictions[(sample_id, "adapter")]["prediction"],
                }
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("predictions", type=Path)
    parser.add_argument(
        "--references",
        type=Path,
        default=ROOT / "data" / "provisional_v0" / "splits" / "test.jsonl",
    )
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--details", type=Path, help="Backward-compatible per-case output path.")
    args = parser.parse_args()

    references = {row["sample_id"]: row for row in _read_jsonl(args.references)}
    prediction_rows = _read_jsonl(args.predictions)
    expected_systems = {"base", "adapter"}
    predictions: dict[tuple[str, str], dict] = {}
    scores = []
    for prediction in prediction_rows:
        sample_id = prediction.get("sample_id")
        system = prediction.get("system")
        if sample_id not in references:
            raise SystemExit(f"prediction references unknown sample: {sample_id}")
        if system not in expected_systems:
            raise SystemExit(f"invalid system for {sample_id}: {system}")
        pair = (sample_id, system)
        if pair in predictions:
            raise SystemExit(f"duplicate prediction: {system}/{sample_id}")
        predictions[pair] = prediction
        scores.append(score_prediction(references[sample_id], prediction))

    expected_pairs = {
        (sample_id, system) for sample_id in references for system in expected_systems
    }
    missing = sorted(expected_pairs - set(predictions))
    if missing:
        raise SystemExit(f"missing {len(missing)} base/adapter predictions")

    summary = summarize_with_confidence(scores)
    print(json.dumps(summary, indent=2, sort_keys=True))
    if args.details:
        args.details.parent.mkdir(parents=True, exist_ok=True)
        _write_jsonl(args.details, scores)
    if not args.output_dir:
        return 0

    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    _write_jsonl(output_dir / "per_case_metrics.jsonl", scores)
    with (output_dir / "summary_metrics.json").open(
        "w", encoding="utf-8", newline="\n"
    ) as handle:
        handle.write(json.dumps(summary, indent=2, sort_keys=True) + "\n")
    table = _metric_table(summary)
    with (output_dir / "metrics_table.csv").open(
        "w", encoding="utf-8", newline=""
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(table[0]))
        writer.writeheader()
        writer.writerows(table)

    score_by_pair = {(row["sample_id"], row["system"]): row for row in scores}
    failures = []
    for pair, prediction in sorted(predictions.items()):
        score = score_by_pair[pair]
        failed_metrics = [metric for metric in FAILURE_METRICS if score[metric] < 1.0]
        if score["internal_contradiction"] > 0:
            failed_metrics.append("internal_contradiction")
        if failed_metrics:
            failures.append(
                {
                    **prediction,
                    "behavior_family": score["behavior_family"],
                    "failed_metrics": failed_metrics,
                    "contradiction_reasons": score["contradiction_reasons"],
                }
            )
    _write_jsonl(output_dir / "automatic_failures.jsonl", failures)
    _write_metrics_markdown(output_dir / "METRICS.md", summary, table, len(failures))
    _write_manual_review(output_dir / "manual_review.csv", references, predictions)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
