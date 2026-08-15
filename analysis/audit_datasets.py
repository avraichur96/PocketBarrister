"""Deterministic, read-only measurements for the Phase 1 dataset audit.

Run from the repository root:

    python -B analysis/audit_datasets.py

The script reads the preserved legacy datasets and writes a JSON report to
standard output. It never writes to or transforms a source dataset.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEGACY_ROOT = REPOSITORY_ROOT / "experiments" / "legacy_v0"
DATASET_PATHS = {
    "improved_100": LEGACY_ROOT / "legal_reasoning_improved.json",
    "final_200": LEGACY_ROOT / "legal_reasoning_final.json",
}

REQUIRED_RECORD_FIELDS = ("input", "output", "metadata")
REQUIRED_METADATA_FIELDS = (
    "case_id",
    "category",
    "difficulty",
    "sections",
    "jurisdiction",
    "token_count",
)
REQUIRED_OUTPUT_SECTIONS = (
    "REASONING:",
    "FINDINGS:",
    "LEGAL_EFFECT:",
    "CONCLUSION:",
    "WHY ALTERNATIVES FAIL:",
)
EOS_TOKEN = "<|end_of_text|>"

KNOWN_PEOPLE = (
    "Pradeep",
    "Aditya",
    "Sanjay",
    "Vikram",
    "Anjali",
    "Kavita",
    "Sunita",
    "Sneha",
    "Priya",
    "Rahul",
    "Arjun",
    "Rohan",
    "Karan",
    "Amit",
    "Meera",
    "Pooja",
    "Divya",
    "Neha",
    "Ritu",
    "Raj",
)
KNOWN_COMPANIES = (
    "DataSolutions",
    "InfoSystems",
    "NetServices",
    "CloudWorks",
    "TechCorp",
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_dataset(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise TypeError(f"Expected a JSON list in {path}")
    return data


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def extract_case_id_from_input(text: str) -> str | None:
    match = re.search(r"(?m)^CASE_ID:\s*([^\n]+)\s*$", text)
    return match.group(1).strip() if match else None


def normalize_surface(text: str) -> str:
    """Remove case IDs, known entities, and scalar surface variations."""

    normalized = re.sub(r"(?m)^CASE_ID:\s*[^\n]+\s*$", "CASE_ID: <id>", text)
    normalized = re.sub(r"\bCompany\s+[A-J]\b", "<company>", normalized)
    for company in KNOWN_COMPANIES:
        normalized = re.sub(rf"\b{re.escape(company)}\b", "<company>", normalized)
    for person in KNOWN_PEOPLE:
        normalized = re.sub(rf"\b{re.escape(person)}\b", "<person>", normalized)
    normalized = re.sub(
        r"₹\s*[\d,.]+(?:\s*(?:lakh|crore))?",
        "<amount>",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"\b\d+(?:\.\d+)?%", "<percent>", normalized)
    normalized = re.sub(r"\b\d+(?:\.\d+)?\b", "<number>", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip().casefold()
    return normalized


def duplicate_groups(values: Iterable[str]) -> list[dict[str, Any]]:
    indexes: dict[str, list[int]] = defaultdict(list)
    for index, value in enumerate(values):
        indexes[value].append(index)
    return [
        {"count": len(group), "indexes": group}
        for group in indexes.values()
        if len(group) > 1
    ]


def entity_set(text: str) -> set[str]:
    entities = {person for person in KNOWN_PEOPLE if re.search(rf"\b{person}\b", text)}
    entities.update(company for company in KNOWN_COMPANIES if re.search(rf"\b{company}\b", text))
    entities.update(re.findall(r"\bCompany\s+[A-J]\b", text))
    return entities


def output_section_status(output: str) -> dict[str, Any]:
    positions = [output.find(section) for section in REQUIRED_OUTPUT_SECTIONS]
    present_once = all(output.count(section) == 1 for section in REQUIRED_OUTPUT_SECTIONS)
    ordered = all(position >= 0 for position in positions) and positions == sorted(positions)
    return {
        "all_present_once": present_once,
        "ordered": ordered,
        "eos_count": output.count(EOS_TOKEN),
        "ends_with_eos": output.rstrip().endswith(EOS_TOKEN),
    }


def parse_findings(output: str) -> dict[str, str]:
    start = output.find("FINDINGS:")
    end = output.find("LEGAL_EFFECT:")
    if start < 0 or end < 0 or end <= start:
        return {}
    findings: dict[str, str] = {}
    block = output[start + len("FINDINGS:") : end]
    for line in block.splitlines():
        match = re.match(r"\s*-\s*([A-Z][A-Z0-9_]+):\s*(.+?)\s*$", line)
        if match:
            findings[match.group(1)] = match.group(2)
    return findings


def canonical_finding_value(value: str) -> str:
    lowered = value.strip().casefold()
    if lowered.startswith("yes"):
        return "Yes"
    if lowered.startswith("no"):
        return "No"
    if lowered.startswith("not applicable"):
        return "Not applicable"
    if lowered.startswith("unclear"):
        return "Unclear"
    return value.strip()


def summarize_dataset(path: Path, records: list[dict[str, Any]]) -> dict[str, Any]:
    malformed_indexes: list[int] = []
    missing_record_fields: Counter[str] = Counter()
    missing_metadata_fields: Counter[str] = Counter()
    input_case_id_mismatches: list[int] = []
    entity_output_extras: list[dict[str, Any]] = []
    malformed_sections: list[int] = []
    malformed_eos: list[int] = []
    empty_findings: list[int] = []
    unexpanded_placeholder_records: list[dict[str, Any]] = []
    role_collision_records: list[dict[str, Any]] = []
    finding_keys: Counter[str] = Counter()
    category_members: dict[str, list[int]] = defaultdict(list)
    category_finding_values: dict[str, dict[str, Counter[str]]] = defaultdict(
        lambda: defaultdict(Counter)
    )

    inputs: list[str] = []
    outputs: list[str] = []
    case_ids: list[str] = []
    normalized_inputs: list[str] = []
    normalized_outputs: list[str] = []
    categories: Counter[str] = Counter()
    difficulties: Counter[str] = Counter()
    jurisdictions: Counter[str] = Counter()
    referenced_sections: Counter[str] = Counter()

    for index, record in enumerate(records):
        if not isinstance(record, dict):
            malformed_indexes.append(index)
            continue
        for field in REQUIRED_RECORD_FIELDS:
            if field not in record or record[field] in (None, ""):
                missing_record_fields[field] += 1
        if not all(field in record for field in REQUIRED_RECORD_FIELDS):
            malformed_indexes.append(index)
            continue
        if not isinstance(record["input"], str) or not isinstance(record["output"], str):
            malformed_indexes.append(index)
            continue
        metadata = record["metadata"]
        if not isinstance(metadata, dict):
            malformed_indexes.append(index)
            continue
        for field in REQUIRED_METADATA_FIELDS:
            if field not in metadata or metadata[field] in (None, ""):
                missing_metadata_fields[field] += 1

        input_text = record["input"]
        output_text = record["output"]
        case_id = str(metadata.get("case_id", ""))
        inputs.append(input_text)
        outputs.append(output_text)
        case_ids.append(case_id)
        normalized_inputs.append(normalize_surface(input_text))
        normalized_outputs.append(normalize_surface(output_text))
        category = str(metadata.get("category"))
        categories[category] += 1
        category_members[category].append(index)
        difficulties[str(metadata.get("difficulty"))] += 1
        jurisdictions[str(metadata.get("jurisdiction"))] += 1
        for section in metadata.get("sections", []):
            referenced_sections[str(section)] += 1

        if extract_case_id_from_input(input_text) != case_id:
            input_case_id_mismatches.append(index)

        input_entities = entity_set(input_text)
        output_entities = entity_set(output_text)
        extras = sorted(output_entities - input_entities)
        if extras:
            entity_output_extras.append(
                {"index": index, "case_id": case_id, "output_only_entities": extras}
            )

        status = output_section_status(output_text)
        if not status["all_present_once"] or not status["ordered"]:
            malformed_sections.append(index)
        if status["eos_count"] != 1 or not status["ends_with_eos"]:
            malformed_eos.append(index)

        findings = parse_findings(output_text)
        if not findings:
            empty_findings.append(index)
        finding_keys.update(findings.keys())
        for key, value in findings.items():
            category_finding_values[category][key][canonical_finding_value(value)] += 1

        placeholders = sorted(set(re.findall(r"\{[A-Za-z_][^}]*\}", input_text + "\n" + output_text)))
        if placeholders:
            unexpanded_placeholder_records.append(
                {"index": index, "case_id": case_id, "category": category, "placeholders": placeholders}
            )

        if category == "supplier_duress":
            mentioned_companies = sorted(
                company for company in KNOWN_COMPANIES if re.search(rf"\b{company}\b", input_text)
            )
            if len(mentioned_companies) < 2:
                role_collision_records.append(
                    {
                        "index": index,
                        "case_id": case_id,
                        "category": category,
                        "companies": mentioned_companies,
                    }
                )

    normalized_group_members: dict[str, list[int]] = defaultdict(list)
    for index, signature in enumerate(normalized_inputs):
        normalized_group_members[signature].append(index)

    template_groups = []
    for group_number, members in enumerate(
        sorted(normalized_group_members.values(), key=lambda value: (-len(value), value[0])),
        start=1,
    ):
        category_counts = Counter(str(records[index]["metadata"]["category"]) for index in members)
        template_groups.append(
            {
                "provisional_id": f"surface-template-{group_number:02d}",
                "count": len(members),
                "categories": dict(sorted(category_counts.items())),
                "example_case_ids": [records[index]["metadata"]["case_id"] for index in members[:3]],
            }
        )

    exact_input_groups = duplicate_groups(inputs)
    exact_output_groups = duplicate_groups(outputs)
    exact_id_groups = duplicate_groups(case_ids)

    category_profiles: dict[str, Any] = {}
    for category, members in sorted(category_members.items()):
        category_profiles[category] = {
            "record_count": len(members),
            "normalized_input_template_count": len(
                {normalized_inputs[index] for index in members}
            ),
            "normalized_output_template_count": len(
                {normalized_outputs[index] for index in members}
            ),
            "difficulties": dict(
                sorted(Counter(str(records[index]["metadata"]["difficulty"]) for index in members).items())
            ),
            "finding_values": {
                key: dict(sorted(values.items()))
                for key, values in sorted(category_finding_values[category].items())
            },
        }

    return {
        "path": str(path.relative_to(REPOSITORY_ROOT)),
        "sha256": sha256(path),
        "record_count": len(records),
        "record_field_sets": {
            ",".join(fields): count
            for fields, count in sorted(
                Counter(
                    tuple(sorted(record.keys()))
                    for record in records
                    if isinstance(record, dict)
                ).items()
            )
        },
        "metadata_field_sets": {
            ",".join(fields): count
            for fields, count in sorted(
                Counter(
                    tuple(sorted(record.get("metadata", {}).keys()))
                    for record in records
                    if isinstance(record, dict) and isinstance(record.get("metadata"), dict)
                ).items()
            )
        },
        "malformed_record_count": len(malformed_indexes),
        "malformed_record_indexes": malformed_indexes,
        "missing_record_fields": dict(sorted(missing_record_fields.items())),
        "missing_metadata_fields": dict(sorted(missing_metadata_fields.items())),
        "input_case_id_mismatch_count": len(input_case_id_mismatches),
        "duplicate_case_id_record_count": sum(group["count"] - 1 for group in exact_id_groups),
        "duplicate_case_id_groups": exact_id_groups,
        "exact_duplicate_input_record_count": sum(group["count"] - 1 for group in exact_input_groups),
        "exact_duplicate_input_groups": exact_input_groups,
        "exact_duplicate_output_record_count": sum(group["count"] - 1 for group in exact_output_groups),
        "exact_duplicate_output_group_count": len(exact_output_groups),
        "largest_exact_output_group": max((group["count"] for group in exact_output_groups), default=1),
        "normalized_input_template_count": len(normalized_group_members),
        "records_in_repeated_normalized_input_templates": sum(
            len(members) for members in normalized_group_members.values() if len(members) > 1
        ),
        "cosmetic_variant_record_count": sum(
            max(0, len(members) - 1) for members in normalized_group_members.values()
        ),
        "normalized_output_template_count": len(set(normalized_outputs)),
        "template_groups": template_groups,
        "entity_output_extra_count": len(entity_output_extras),
        "entity_output_extras": entity_output_extras,
        "unexpanded_placeholder_record_count": len(unexpanded_placeholder_records),
        "unexpanded_placeholder_categories": dict(
            sorted(Counter(item["category"] for item in unexpanded_placeholder_records).items())
        ),
        "unexpanded_placeholder_examples": unexpanded_placeholder_records[:10],
        "obvious_role_collision_count": len(role_collision_records),
        "obvious_role_collisions": role_collision_records,
        "malformed_output_section_count": len(malformed_sections),
        "malformed_eos_count": len(malformed_eos),
        "records_without_parseable_findings": len(empty_findings),
        "unique_finding_key_count": len(finding_keys),
        "finding_keys": dict(finding_keys.most_common()),
        "categories": dict(sorted(categories.items())),
        "category_profiles": category_profiles,
        "difficulties": dict(sorted(difficulties.items())),
        "jurisdictions": dict(sorted(jurisdictions.items())),
        "metadata_section_references": dict(referenced_sections.most_common()),
    }


def cross_template_similarity(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    representatives: dict[str, int] = {}
    for index, record in enumerate(records):
        representatives.setdefault(normalize_surface(record["input"]), index)
    items = list(representatives.items())
    similarities = []
    for left in range(len(items)):
        for right in range(left + 1, len(items)):
            left_signature, left_index = items[left]
            right_signature, right_index = items[right]
            ratio = SequenceMatcher(None, left_signature, right_signature).ratio()
            if ratio >= 0.55:
                similarities.append(
                    {
                        "ratio": round(ratio, 4),
                        "left_case_id": records[left_index]["metadata"]["case_id"],
                        "left_category": records[left_index]["metadata"]["category"],
                        "right_case_id": records[right_index]["metadata"]["case_id"],
                        "right_category": records[right_index]["metadata"]["category"],
                    }
                )
    return sorted(similarities, key=lambda item: (-item["ratio"], item["left_case_id"]))


def compare_datasets(
    improved: list[dict[str, Any]], final: list[dict[str, Any]]
) -> dict[str, Any]:
    improved_records = {canonical_json(record) for record in improved}
    final_records = {canonical_json(record) for record in final}
    improved_inputs = {record["input"] for record in improved}
    improved_ids = {record["metadata"]["case_id"] for record in improved}
    added = [record for record in final if canonical_json(record) not in improved_records]
    added_categories = Counter(record["metadata"]["category"] for record in added)
    added_templates = Counter(normalize_surface(record["input"]) for record in added)
    improved_templates = {normalize_surface(record["input"]) for record in improved}
    return {
        "exact_records_from_improved_present_in_final": len(improved_records & final_records),
        "improved_records_absent_from_final": len(improved_records - final_records),
        "final_records_not_in_improved": len(final_records - improved_records),
        "final_first_100_exactly_equal_improved": final[: len(improved)] == improved,
        "added_record_count": len(added),
        "added_exact_input_overlap_with_improved": sum(
            record["input"] in improved_inputs for record in added
        ),
        "added_case_id_overlap_with_improved": sum(
            record["metadata"]["case_id"] in improved_ids for record in added
        ),
        "added_normalized_template_overlap_with_improved": sum(
            signature in improved_templates for signature in added_templates
        ),
        "added_normalized_template_count": len(added_templates),
        "added_cosmetic_variant_record_count": sum(count - 1 for count in added_templates.values()),
        "added_categories": dict(sorted(added_categories.items())),
    }


def main() -> int:
    datasets = {name: load_dataset(path) for name, path in DATASET_PATHS.items()}
    report = {
        "method": {
            "surface_normalization": (
                "case IDs, known generated person/company names, currency values, percentages, "
                "and other numeric scalars are replaced before exact template grouping"
            ),
            "near_duplicate_definition": (
                "records sharing an identical surface-normalized input are one provisional "
                "template family; fuzzy cross-template similarities are reported separately"
            ),
            "entity_check_scope": (
                "known generator person names and Company A-J tokens appearing in output but "
                "not facts are flagged; generic roles are not evaluated"
            ),
        },
        "datasets": {
            name: summarize_dataset(DATASET_PATHS[name], records)
            for name, records in datasets.items()
        },
        "delta": compare_datasets(datasets["improved_100"], datasets["final_200"]),
        "cross_template_similarity_final_200": cross_template_similarity(datasets["final_200"]),
    }
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
