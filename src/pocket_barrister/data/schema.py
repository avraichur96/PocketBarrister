"""Validation for the provisional canonical dataset schema."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Iterable

REQUIRED_OUTPUT_SECTIONS = (
    "REASONING:",
    "FINDINGS:",
    "LEGAL_EFFECT:",
    "CONCLUSION:",
    "WHY ALTERNATIVES FAIL:",
)
EOS_MARKER = "<|end_of_text|>"
PLACEHOLDER_PATTERN = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}")
VALID_SPLITS = {"train", "validation", "test"}
VALID_LEGAL_STATUSES = {"unreviewed", "reviewed"}


def parse_findings(output: str) -> dict[str, str]:
    """Extract visible key/value findings without inferring legal correctness."""
    start = output.find("FINDINGS:")
    end = output.find("LEGAL_EFFECT:")
    if start < 0 or end <= start:
        return {}

    findings: dict[str, str] = {}
    block = output[start + len("FINDINGS:") : end]
    for line in block.splitlines():
        match = re.match(r"\s*-\s*([A-Z][A-Z0-9_]*):\s*(.+?)\s*$", line)
        if match:
            findings[match.group(1)] = match.group(2)
    return findings


def parse_conclusion(output: str) -> str:
    """Return the visible conclusion section."""
    start = output.find("CONCLUSION:")
    end = output.find("WHY ALTERNATIVES FAIL:")
    if start < 0 or end <= start:
        return ""
    return output[start + len("CONCLUSION:") : end].strip()


def validate_record(record: dict[str, Any]) -> list[str]:
    """Return all schema/content errors for one record."""
    errors: list[str] = []
    required = {
        "sample_id",
        "dataset_version",
        "behavior_family",
        "template_family",
        "variant_id",
        "jurisdiction",
        "split",
        "input",
        "output",
        "source_type",
        "source",
        "provenance",
        "review",
        "expected_state",
        "metadata",
    }
    missing = sorted(required - set(record))
    if missing:
        return [f"missing keys: {', '.join(missing)}"]

    for key in ("sample_id", "behavior_family", "template_family", "input", "output"):
        if not isinstance(record[key], str) or not record[key].strip():
            errors.append(f"{key} must be a non-empty string")

    if record["split"] not in VALID_SPLITS:
        errors.append(f"invalid split: {record['split']!r}")
    if record["jurisdiction"] != "India":
        errors.append("jurisdiction must be India")
    if record["source_type"] != "adapted_legacy_synthetic":
        errors.append("source_type must identify the provisional legacy-derived source")

    review = record["review"]
    if not isinstance(review, dict) or review.get("legal_status") not in VALID_LEGAL_STATUSES:
        errors.append("review.legal_status must be unreviewed or reviewed")
    if isinstance(review, dict) and review.get("legal_status") == "unreviewed":
        if review.get("reviewer") is not None or review.get("reviewed_at") is not None:
            errors.append("unreviewed records cannot name a reviewer or review date")

    output = record["output"] if isinstance(record["output"], str) else ""
    positions = [output.find(section) for section in REQUIRED_OUTPUT_SECTIONS]
    if any(position < 0 for position in positions):
        errors.append("missing a required output section")
    elif positions != sorted(positions):
        errors.append("output sections are out of order")
    for section in REQUIRED_OUTPUT_SECTIONS:
        if output.count(section) != 1:
            errors.append(f"output must contain exactly one {section}")
    if output.count(EOS_MARKER) != 1 or not output.rstrip().endswith(EOS_MARKER):
        errors.append("output must end with exactly one EOS marker")

    joined_text = f"{record['input']}\n{output}"
    if PLACEHOLDER_PATTERN.search(joined_text):
        errors.append("unresolved generator placeholder")
    if not parse_findings(output):
        errors.append("no parseable findings")
    if not parse_conclusion(output):
        errors.append("no parseable conclusion")

    source = record["source"]
    if not isinstance(source, dict) or not all(
        source.get(key) for key in ("path", "case_id", "sha256")
    ):
        errors.append("source path, case_id, and sha256 are required")

    expected = record["expected_state"]
    if not isinstance(expected, dict) or expected.get("label_status") != "inherited_unreviewed":
        errors.append("expected_state must be labeled inherited_unreviewed")

    return errors


def validate_dataset(records: Iterable[dict[str, Any]]) -> list[str]:
    """Validate records plus dataset-level uniqueness and split isolation."""
    rows = list(records)
    errors: list[str] = []
    for index, record in enumerate(rows, start=1):
        sample_id = record.get("sample_id", f"row-{index}")
        errors.extend(f"{sample_id}: {error}" for error in validate_record(record))

    for field in ("sample_id", "input", "output"):
        values = [record.get(field) for record in rows]
        duplicates = sorted(value for value, count in Counter(values).items() if count > 1)
        if duplicates:
            errors.append(f"duplicate {field} values: {len(duplicates)}")

    family_splits: dict[str, set[str]] = {}
    template_splits: dict[str, set[str]] = {}
    for record in rows:
        family_splits.setdefault(record.get("behavior_family", ""), set()).add(
            record.get("split", "")
        )
        template_splits.setdefault(record.get("template_family", ""), set()).add(
            record.get("split", "")
        )
    leaking_families = sorted(key for key, splits in family_splits.items() if len(splits) > 1)
    leaking_templates = sorted(key for key, splits in template_splits.items() if len(splits) > 1)
    if leaking_families:
        errors.append(f"behavior-family split overlap: {', '.join(leaking_families)}")
    if leaking_templates:
        errors.append(f"template-family split overlap: {', '.join(leaking_templates)}")
    return errors
