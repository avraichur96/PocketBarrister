"""Transparent structural metrics that do not imply legal correctness."""

from __future__ import annotations

from collections import defaultdict
from statistics import fmean
from typing import Any, Iterable

from pocket_barrister.data.schema import (
    EOS_MARKER,
    REQUIRED_OUTPUT_SECTIONS,
    parse_conclusion,
    parse_findings,
)


def _section_adherence(text: str) -> bool:
    positions = [text.find(section) for section in REQUIRED_OUTPUT_SECTIONS]
    return (
        all(position >= 0 for position in positions)
        and positions == sorted(positions)
        and all(text.count(section) == 1 for section in REQUIRED_OUTPUT_SECTIONS)
    )


def score_prediction(
    reference: dict[str, Any], prediction: dict[str, Any]
) -> dict[str, Any]:
    """Score visible formatting and inherited key/value state reproduction."""
    text = prediction.get("prediction", "")
    predicted_findings = parse_findings(text)
    expected_findings = reference["expected_state"]["findings"]
    expected_pairs = set(expected_findings.items())
    predicted_pairs = set(predicted_findings.items())
    correct_pairs = expected_pairs & predicted_pairs
    precision = len(correct_pairs) / len(predicted_pairs) if predicted_pairs else 0.0
    recall = len(correct_pairs) / len(expected_pairs) if expected_pairs else 0.0
    findings_f1 = (
        2 * precision * recall / (precision + recall) if precision + recall else 0.0
    )
    sections_ok = _section_adherence(text)
    marker_ok = text.count(EOS_MARKER) == 1 and text.rstrip().endswith(EOS_MARKER)
    actual_eos = bool(prediction.get("ended_with_eos", False))
    return {
        "sample_id": reference["sample_id"],
        "system": prediction["system"],
        "section_adherence": float(sections_ok),
        "visible_end_marker": float(marker_ok),
        "actual_eos_stop": float(actual_eos),
        "findings_exact_pair_precision": precision,
        "findings_exact_pair_recall": recall,
        "findings_exact_pair_f1": findings_f1,
        "conclusion_present": float(bool(parse_conclusion(text))),
        "malformed_output": float(not (sections_ok and marker_ok)),
        "response_characters": len(text),
    }


def aggregate_scores(scores: Iterable[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Average numeric metrics by compared system."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for score in scores:
        grouped[score["system"]].append(score)

    aggregate: dict[str, dict[str, float]] = {}
    for system, rows in sorted(grouped.items()):
        numeric_keys = [
            key
            for key, value in rows[0].items()
            if key not in {"sample_id", "system"} and isinstance(value, (int, float))
        ]
        aggregate[system] = {
            "n": float(len(rows)),
            **{key: fmean(float(row[key]) for row in rows) for key in numeric_keys},
        }
    return aggregate
