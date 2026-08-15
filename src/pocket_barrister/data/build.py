"""Deterministically derive a provisional dataset without mutating legacy files."""

from __future__ import annotations

import hashlib
import json
import random
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from .schema import parse_conclusion, parse_findings, validate_dataset

REPO_ROOT = Path(__file__).resolve().parents[3]

ENTITY_PATTERNS: dict[str, re.Pattern[str]] = {
    "fraud_misrepresentation": re.compile(
        r"FACTS:\n(?P<seller>[A-Z][a-z]+) sells car to (?P<buyer>[A-Z][a-z]+)"
    ),
    "supplier_duress": re.compile(
        r"FACTS:\n(?P<supplier>[A-Za-z][A-Za-z]+) threatens .*? unless "
        r"(?P<buyer>[A-Za-z][A-Za-z]+) agrees"
    ),
    "hard_negative_duress": re.compile(
        r"FACTS:\n(?P<party_a>[A-Z][a-z]+) owes (?P<party_b>[A-Z][a-z]+)"
    ),
    "hard_negative_void": re.compile(r"FACTS:\n(?P<party_a>[A-Z][a-z]+), aged"),
    "voidable_ratification": re.compile(
        r"FACTS:\n(?P<party_a>[A-Z][a-z]+) enters contract with "
        r"(?P<party_b>[A-Z][a-z]+)"
    ),
    "medical_influence": re.compile(
        r"FACTS:\nDr\. (?P<doctor>[A-Z][a-z]+) treats (?P<patient>[A-Z][a-z]+)"
    ),
}


def sha256_file(path: Path, mode: str = "binary") -> str:
    data = path.read_bytes()
    if mode == "text-lf":
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    elif mode != "binary":
        raise ValueError(f"unsupported hash mode: {mode}")
    return hashlib.sha256(data).hexdigest()


def _load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def _write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=False, indent=2, sort_keys=True)
        handle.write("\n")


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def _resolve_placeholders(category: str, input_text: str, output_text: str) -> tuple[str, list[str]]:
    placeholders = sorted(set(re.findall(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", output_text)))
    if not placeholders:
        return output_text, []

    pattern = ENTITY_PATTERNS.get(category)
    match = pattern.search(input_text) if pattern else None
    if not match:
        raise ValueError(f"{category}: cannot bind placeholders {placeholders}")

    entities = match.groupdict()
    unresolved = sorted(set(placeholders) - set(entities))
    if unresolved:
        raise ValueError(f"{category}: no binding rule for {unresolved}")

    repaired = output_text
    repairs: list[str] = []
    for placeholder in placeholders:
        repaired = repaired.replace("{" + placeholder + "}", entities[placeholder])
        repairs.append(f"resolved_placeholder:{placeholder}")
    return repaired, repairs


def _has_role_collision(category: str, input_text: str) -> bool:
    if category != "supplier_duress":
        return False
    match = ENTITY_PATTERNS[category].search(input_text)
    return bool(match and match.group("supplier") == match.group("buyer"))


def _canonical_record(
    source_record: dict[str, Any], config: dict[str, Any], source_path: str
) -> dict[str, Any]:
    metadata = source_record["metadata"]
    category = metadata["category"]
    case_id = metadata["case_id"]
    repaired_output, repairs = _resolve_placeholders(
        category, source_record["input"], source_record["output"]
    )
    findings = parse_findings(repaired_output)
    return {
        "sample_id": f"PB-PROV-{case_id}",
        "dataset_version": config["dataset_version"],
        "behavior_family": category,
        "template_family": f"legacy-{category}-v1",
        "variant_id": case_id,
        "jurisdiction": metadata["jurisdiction"],
        "split": config["families"][category],
        "input": source_record["input"],
        "output": repaired_output,
        "source_type": "adapted_legacy_synthetic",
        "source": {
            "path": source_path,
            "case_id": case_id,
            "sha256": config["source_sha256"],
        },
        "provenance": {
            "type": "adapted_legacy_synthetic",
            "generator": "legacy-unseeded-template",
            "structural_repairs": repairs,
            "semantic_label_changed": False,
        },
        "review": {
            "structural_status": "passed",
            "legal_status": "unreviewed",
            "reviewer": None,
            "reviewed_at": None,
            "notes": [
                "Expected state is inherited from synthetic legacy output and is not legal advice."
            ],
        },
        "expected_state": {
            "label_status": "inherited_unreviewed",
            "findings": findings,
            "conclusion": parse_conclusion(repaired_output),
        },
        "metadata": {
            "difficulty": metadata["difficulty"],
            "sections": metadata["sections"],
            "legacy_token_estimate": metadata["token_count"],
        },
    }


def build_dataset(config_path: Path, output_dir: Path | None = None) -> dict[str, Any]:
    """Build dataset/splits/manifest and return the manifest."""
    config_path = config_path.resolve()
    config = _load_json(config_path)
    source_path_text = config["source_path"]
    source_path = (REPO_ROOT / source_path_text).resolve()
    source_hash_mode = config.get("source_hash_mode", "binary")
    if sha256_file(source_path, source_hash_mode) != config["source_sha256"]:
        raise ValueError("legacy source hash does not match the pinned configuration")

    destination = (output_dir or (REPO_ROOT / config["output_dir"])).resolve()
    source_records = _load_json(source_path)
    requested = set(config["families"])
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    exclusions: dict[str, list[str]] = defaultdict(list)

    for source_record in source_records:
        category = source_record.get("metadata", {}).get("category")
        if category not in requested:
            continue
        case_id = source_record["metadata"]["case_id"]
        if _has_role_collision(category, source_record["input"]):
            exclusions["opposing_role_collision"].append(case_id)
            continue
        grouped[category].append(source_record)

    missing = sorted(requested - set(grouped))
    if missing:
        raise ValueError(f"no usable records for families: {', '.join(missing)}")

    selected: list[dict[str, Any]] = []
    cap = int(config["records_per_family"])
    rng = random.Random(int(config["seed"]))
    for category in sorted(requested):
        candidates = sorted(grouped[category], key=lambda row: row["metadata"]["case_id"])
        rng.shuffle(candidates)
        retained: list[dict[str, Any]] = []
        seen_outputs: set[str] = set()
        for source_record in candidates:
            case_id = source_record["metadata"]["case_id"]
            candidate = _canonical_record(source_record, config, source_path_text)
            if candidate["output"] in seen_outputs:
                exclusions["exact_duplicate_output"].append(case_id)
                continue
            if len(retained) >= cap:
                exclusions["beyond_family_cap"].append(case_id)
                continue
            retained.append(candidate)
            seen_outputs.add(candidate["output"])
        selected.extend(retained)

    selected.sort(key=lambda row: row["sample_id"])
    errors = validate_dataset(selected)
    if errors:
        raise ValueError("dataset validation failed:\n- " + "\n- ".join(errors))

    dataset_path = destination / "dataset.jsonl"
    _write_jsonl(dataset_path, selected)
    split_counts: dict[str, int] = {}
    split_families: dict[str, list[str]] = {}
    split_hashes: dict[str, str] = {}
    for split in ("train", "validation", "test"):
        rows = [row for row in selected if row["split"] == split]
        split_path = destination / "splits" / f"{split}.jsonl"
        _write_jsonl(split_path, rows)
        split_counts[split] = len(rows)
        split_families[split] = sorted({row["behavior_family"] for row in rows})
        split_hashes[split] = sha256_file(split_path)

    family_counts = Counter(row["behavior_family"] for row in selected)
    difficulty_counts = Counter(str(row["metadata"]["difficulty"]) for row in selected)
    manifest = {
        "dataset_id": config["dataset_id"],
        "dataset_version": config["dataset_version"],
        "release_status": "provisional_synthetic_unreviewed",
        "canonical_eligible": False,
        "seed": config["seed"],
        "config_path": str(config_path.relative_to(REPO_ROOT)).replace("\\", "/"),
        "config_sha256": sha256_file(config_path),
        "source_path": source_path_text,
        "source_sha256": config["source_sha256"],
        "source_hash_mode": source_hash_mode,
        "dataset_sha256": sha256_file(dataset_path),
        "record_count": len(selected),
        "family_counts": dict(sorted(family_counts.items())),
        "difficulty_counts": dict(sorted(difficulty_counts.items())),
        "split_counts": split_counts,
        "split_families": split_families,
        "split_sha256": split_hashes,
        "exclusions": {key: sorted(value) for key, value in sorted(exclusions.items())},
    }
    _write_json(destination / "manifest.json", manifest)
    return manifest
