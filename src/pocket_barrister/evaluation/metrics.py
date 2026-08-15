"""Transparent automatic metrics for provisional base/adapter comparisons.

These metrics measure structure and agreement with inherited synthetic labels.
They do not establish that either the labels or predictions are legally correct.
"""

from __future__ import annotations

import math
import random
import re
from collections import defaultdict
from statistics import fmean
from typing import Any, Iterable

from pocket_barrister.data.schema import (
    EOS_MARKER,
    REQUIRED_OUTPUT_SECTIONS,
    parse_conclusion,
    parse_findings,
)

DOCTRINE_DECISION_KEYS = {
    "void_voidable": "MINORITY_ESTABLISHED",
    "consent": "UNDUE_INFLUENCE_ESTABLISHED",
    "fraud_misrepresentation": "MISREPRESENTATION_ESTABLISHED",
    "minor_clear": "MINORITY_ESTABLISHED",
    "mistake_edge": "MUTUAL_MISTAKE",
    "supplier_duress": "ECONOMIC_DURESS_ESTABLISHED",
    "hard_negative_duress": "ECONOMIC_DURESS_ESTABLISHED",
    "hard_negative_influence": "UNDUE_INFLUENCE_ESTABLISHED",
    "hard_negative_void": "CONTRACT_VOIDABLE",
    "ratification_void": "RATIFICATION_POSSIBLE",
    "voidable_ratification": "VALID_RATIFICATION",
    "medical_influence": "UNDUE_INFLUENCE_ESTABLISHED",
    "legal_influence": "UNDUE_INFLUENCE_ESTABLISHED",
}

EXPECTED_CONCLUSION_LABELS = {
    "void_voidable": ("void_ab_initio", re.compile(r"\bvoid\s+ab\s+initio\b", re.I)),
    "consent": ("voidable", re.compile(r"\bvoidable\b", re.I)),
    "fraud_misrepresentation": (
        "misrepresentation",
        re.compile(r"\bmisrepresentation\b", re.I),
    ),
    "minor_clear": ("void", re.compile(r"\bvoid\b(?!\s*able)", re.I)),
    "mistake_edge": ("void", re.compile(r"\bvoid\b(?!\s*able)", re.I)),
    "supplier_duress": ("voidable", re.compile(r"\bvoidable\b", re.I)),
    "hard_negative_duress": ("valid", re.compile(r"\bvalid\b", re.I)),
    "hard_negative_influence": ("valid", re.compile(r"\bvalid\b", re.I)),
    "hard_negative_void": ("voidable", re.compile(r"\bvoidable\b", re.I)),
    "ratification_void": ("ineffective", re.compile(r"\bineffective\b", re.I)),
    "voidable_ratification": ("binding", re.compile(r"\bbinding\b", re.I)),
    "medical_influence": ("voidable", re.compile(r"\bvoidable\b", re.I)),
    "legal_influence": ("voidable", re.compile(r"\bvoidable\b", re.I)),
}

BINARY_METRICS = {
    "section_adherence",
    "has_reasoning_section",
    "has_findings_section",
    "has_legal_effect_section",
    "has_conclusion_section",
    "has_alternatives_section",
    "visible_end_marker",
    "actual_eos_stop",
    "primary_doctrine_decision_accuracy",
    "conclusion_label_accuracy_heuristic",
    "conclusion_present",
    "internal_contradiction",
    "malformed_output",
}


def _section_adherence(text: str) -> bool:
    positions = [text.find(section) for section in REQUIRED_OUTPUT_SECTIONS]
    return (
        all(position >= 0 for position in positions)
        and positions == sorted(positions)
        and all(text.count(section) == 1 for section in REQUIRED_OUTPUT_SECTIONS)
    )


def _normalized_boolean(value: str | None) -> bool | None:
    if value is None:
        return None
    normalized = value.strip().casefold()
    if normalized.startswith("yes"):
        return True
    if normalized.startswith("no"):
        return False
    return None


def _contradiction_reasons(findings: dict[str, str], conclusion: str) -> list[str]:
    value = lambda key: _normalized_boolean(findings.get(key))
    reasons: list[str] = []
    if value("CONTRACT_VOID") is True and value("CONTRACT_VOIDABLE") is True:
        reasons.append("contract_marked_both_void_and_voidable")
    if value("VALID_CONTRACT_FORMED") is False and value("CONTRACT_BINDING") is True:
        reasons.append("unformed_contract_marked_binding")
    if value("FREE_CONSENT") is True and value("ECONOMIC_DURESS_ESTABLISHED") is True:
        reasons.append("free_consent_with_economic_duress")
    if value("FREE_CONSENT") is True and value("UNDUE_INFLUENCE_ESTABLISHED") is True:
        reasons.append("free_consent_with_undue_influence")
    if value("CONTRACT_VOID") is True and re.search(r"\b(valid|binding)\b", conclusion, re.I):
        reasons.append("void_contract_concluded_valid_or_binding")
    if value("VALID_CONTRACT_FORMED") is False and re.search(
        r"\b(valid|binding)\b", conclusion, re.I
    ):
        reasons.append("unformed_contract_concluded_valid_or_binding")
    return reasons


def score_prediction(
    reference: dict[str, Any], prediction: dict[str, Any]
) -> dict[str, Any]:
    """Score one prediction against visible inherited fields and format rules."""
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

    family = reference["behavior_family"]
    decision_key = DOCTRINE_DECISION_KEYS[family]
    expected_decision = _normalized_boolean(expected_findings.get(decision_key))
    predicted_decision = _normalized_boolean(predicted_findings.get(decision_key))
    doctrine_accuracy = float(
        expected_decision is not None and predicted_decision == expected_decision
    )

    conclusion = parse_conclusion(text)
    expected_conclusion_label, conclusion_pattern = EXPECTED_CONCLUSION_LABELS[family]
    conclusion_accuracy = float(bool(conclusion_pattern.search(conclusion)))
    contradiction_reasons = _contradiction_reasons(predicted_findings, conclusion)
    sections_ok = _section_adherence(text)
    marker_ok = text.count(EOS_MARKER) == 1 and text.rstrip().endswith(EOS_MARKER)
    actual_eos = bool(prediction.get("ended_with_eos", False))

    section_metrics = {
        "has_reasoning_section": float(text.count("REASONING:") == 1),
        "has_findings_section": float(text.count("FINDINGS:") == 1),
        "has_legal_effect_section": float(text.count("LEGAL_EFFECT:") == 1),
        "has_conclusion_section": float(text.count("CONCLUSION:") == 1),
        "has_alternatives_section": float(text.count("WHY ALTERNATIVES FAIL:") == 1),
    }
    return {
        "sample_id": reference["sample_id"],
        "behavior_family": family,
        "system": prediction["system"],
        "section_adherence": float(sections_ok),
        **section_metrics,
        "visible_end_marker": float(marker_ok),
        "actual_eos_stop": float(actual_eos),
        "findings_exact_pair_precision": precision,
        "findings_exact_pair_recall": recall,
        "findings_exact_pair_f1": findings_f1,
        "primary_doctrine_decision_key": decision_key,
        "primary_doctrine_decision_accuracy": doctrine_accuracy,
        "expected_conclusion_label": expected_conclusion_label,
        "conclusion_label_accuracy_heuristic": conclusion_accuracy,
        "conclusion_present": float(bool(conclusion)),
        "internal_contradiction": float(bool(contradiction_reasons)),
        "contradiction_reasons": contradiction_reasons,
        "malformed_output": float(not (sections_ok and marker_ok)),
        "response_characters": len(text),
        "generated_token_count": int(prediction.get("generated_token_count", 0)),
    }


def _wilson_interval(successes: float, count: int, z: float = 1.96) -> tuple[float, float]:
    if count == 0:
        return 0.0, 0.0
    proportion = successes / count
    denominator = 1 + z * z / count
    center = (proportion + z * z / (2 * count)) / denominator
    margin = z * math.sqrt(
        proportion * (1 - proportion) / count + z * z / (4 * count * count)
    ) / denominator
    return max(0.0, center - margin), min(1.0, center + margin)


def _bootstrap_interval(values: list[float], seed: int) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    if len(values) == 1:
        return values[0], values[0]
    rng = random.Random(seed)
    means = sorted(
        fmean(values[rng.randrange(len(values))] for _ in values) for _ in range(4000)
    )
    return means[int(0.025 * len(means))], means[int(0.975 * len(means))]


def aggregate_scores(scores: Iterable[dict[str, Any]]) -> dict[str, dict[str, float]]:
    """Backward-compatible numeric means by system."""
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for score in scores:
        grouped[score["system"]].append(score)
    aggregate: dict[str, dict[str, float]] = {}
    for system, rows in sorted(grouped.items()):
        numeric_keys = sorted(
            key
            for key, value in rows[0].items()
            if key not in {"sample_id", "system"}
            and isinstance(value, (int, float))
            and not isinstance(value, bool)
        )
        aggregate[system] = {
            "n": float(len(rows)),
            **{key: fmean(float(row[key]) for row in rows) for key in numeric_keys},
        }
    return aggregate


def summarize_with_confidence(
    scores: Iterable[dict[str, Any]], seed: int = 20260815
) -> dict[str, Any]:
    """Return per-system 95% intervals and paired adapter-minus-base deltas."""
    rows = list(scores)
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["system"]].append(row)
    numeric_metrics = sorted(
        key
        for key, value in rows[0].items()
        if isinstance(value, (int, float))
        and not isinstance(value, bool)
        and key not in {"generated_token_count", "response_characters"}
    )
    numeric_metrics.extend(["generated_token_count", "response_characters"])

    systems: dict[str, Any] = {}
    for system, system_rows in sorted(grouped.items()):
        metric_summary: dict[str, Any] = {}
        for metric in numeric_metrics:
            values = [float(row[metric]) for row in system_rows]
            if metric in BINARY_METRICS:
                low, high = _wilson_interval(sum(values), len(values))
                method = "wilson"
            else:
                metric_seed = seed + sum(ord(char) for char in f"{system}:{metric}")
                low, high = _bootstrap_interval(values, metric_seed)
                method = "bootstrap"
            metric_summary[metric] = {
                "mean": fmean(values),
                "ci95_low": low,
                "ci95_high": high,
                "ci_method": method,
            }
        systems[system] = {"n": len(system_rows), "metrics": metric_summary}

    by_pair = {(row["sample_id"], row["system"]): row for row in rows}
    sample_ids = sorted({row["sample_id"] for row in rows})
    deltas: dict[str, Any] = {}
    for metric in numeric_metrics:
        values = [
            float(by_pair[(sample_id, "adapter")][metric])
            - float(by_pair[(sample_id, "base")][metric])
            for sample_id in sample_ids
        ]
        metric_seed = seed + sum(ord(char) for char in f"delta:{metric}")
        low, high = _bootstrap_interval(values, metric_seed)
        deltas[metric] = {
            "mean": fmean(values),
            "ci95_low": low,
            "ci95_high": high,
            "ci_method": "paired_bootstrap",
        }
    return {
        "scope": "automatic provisional metrics against inherited unreviewed labels",
        "confidence_level": 0.95,
        "systems": systems,
        "adapter_minus_base": deltas,
    }
