from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from pocket_barrister.data.build import REPO_ROOT, build_dataset, sha256_file
from pocket_barrister.data.schema import validate_dataset
from pocket_barrister.evaluation.metrics import aggregate_scores, score_prediction
from pocket_barrister.training.formatting import format_prompt, format_target


class DataPipelineTests(unittest.TestCase):
    def test_text_hash_is_cross_platform(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            lf = Path(directory) / "lf.txt"
            crlf = Path(directory) / "crlf.txt"
            lf.write_bytes(b"first\nsecond\n")
            crlf.write_bytes(b"first\r\nsecond\r\n")
            self.assertNotEqual(sha256_file(lf), sha256_file(crlf))
            self.assertEqual(
                sha256_file(lf, "text-lf"), sha256_file(crlf, "text-lf")
            )

    def test_build_is_deterministic_and_valid(self) -> None:
        config = REPO_ROOT / "configs" / "dataset_provisional_v0.json"
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            first_manifest = build_dataset(config, Path(first))
            second_manifest = build_dataset(config, Path(second))
            self.assertEqual(first_manifest["dataset_sha256"], second_manifest["dataset_sha256"])
            self.assertEqual(first_manifest["split_sha256"], second_manifest["split_sha256"])
            self.assertEqual(first_manifest["record_count"], 62)
            self.assertEqual(len(first_manifest["family_counts"]), 13)

    def test_generated_dataset_has_no_split_leakage(self) -> None:
        config = REPO_ROOT / "configs" / "dataset_provisional_v0.json"
        with tempfile.TemporaryDirectory() as directory:
            build_dataset(config, Path(directory))
            with (Path(directory) / "dataset.jsonl").open("r", encoding="utf-8") as handle:
                records = [json.loads(line) for line in handle]
            self.assertEqual(validate_dataset(records), [])
            split_families = {
                split: {row["behavior_family"] for row in records if row["split"] == split}
                for split in ("train", "validation", "test")
            }
            self.assertTrue(split_families["train"].isdisjoint(split_families["validation"]))
            self.assertTrue(split_families["train"].isdisjoint(split_families["test"]))
            self.assertTrue(split_families["validation"].isdisjoint(split_families["test"]))

    def test_training_format_is_explicit_and_requires_marker(self) -> None:
        prompt = format_prompt("CASE_ID: TEST\n\nFACTS:\nSynthetic facts")
        self.assertIn("### INSTRUCTION", prompt)
        self.assertTrue(prompt.endswith("### RESPONSE\n"))
        self.assertEqual(format_target("answer<|end_of_text|>", "<eos>"), "answer<|end_of_text|><eos>")
        with self.assertRaises(ValueError):
            format_target("answer without marker")

    def test_structural_metrics_are_transparent(self) -> None:
        reference = {
            "sample_id": "PB-TEST",
            "expected_state": {"findings": {"FREE_CONSENT": "Yes"}},
        }
        text = (
            "REASONING:\nVisible\nFINDINGS:\n- FREE_CONSENT: Yes\n"
            "LEGAL_EFFECT:\nVisible\nCONCLUSION:\nValid\n"
            "WHY ALTERNATIVES FAIL:\nNone<|end_of_text|>"
        )
        score = score_prediction(
            reference,
            {"sample_id": "PB-TEST", "system": "adapter", "prediction": text, "ended_with_eos": True},
        )
        self.assertEqual(score["section_adherence"], 1.0)
        self.assertEqual(score["findings_exact_pair_f1"], 1.0)
        self.assertEqual(aggregate_scores([score])["adapter"]["n"], 1.0)


if __name__ == "__main__":
    unittest.main()
