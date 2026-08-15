from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvaluationArtifactTests(unittest.TestCase):
    def test_scoring_cli_writes_complete_evidence_set(self) -> None:
        references_path = ROOT / "data" / "provisional_v0" / "splits" / "test.jsonl"
        references = [
            json.loads(line)
            for line in references_path.read_text(encoding="utf-8").splitlines()
            if line
        ]
        predictions = []
        for reference in references:
            for system in ("base", "adapter"):
                predictions.append(
                    {
                        "sample_id": reference["sample_id"],
                        "system": system,
                        "prediction": reference["output"],
                        "ended_with_eos": True,
                        "generated_token_count": 128,
                    }
                )

        with tempfile.TemporaryDirectory() as directory:
            temporary = Path(directory)
            predictions_path = temporary / "predictions.jsonl"
            predictions_path.write_text(
                "".join(json.dumps(row) + "\n" for row in predictions),
                encoding="utf-8",
            )
            output_dir = temporary / "evidence"
            environment = {**os.environ, "PYTHONPATH": str(ROOT / "src")}
            completed = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "scripts" / "score_predictions.py"),
                    str(predictions_path),
                    "--references",
                    str(references_path),
                    "--output-dir",
                    str(output_dir),
                ],
                check=False,
                cwd=ROOT,
                env=environment,
                capture_output=True,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            expected_files = {
                "automatic_failures.jsonl",
                "manual_review.csv",
                "METRICS.md",
                "metrics_table.csv",
                "per_case_metrics.jsonl",
                "summary_metrics.json",
            }
            self.assertEqual({path.name for path in output_dir.iterdir()}, expected_files)
            summary = json.loads((output_dir / "summary_metrics.json").read_text())
            adapter = summary["systems"]["adapter"]["metrics"]
            self.assertEqual(adapter["section_adherence"]["mean"], 1.0)
            self.assertEqual(adapter["primary_doctrine_decision_accuracy"]["mean"], 1.0)

            checksum_lines = []
            for path in sorted(output_dir.iterdir()):
                checksum_lines.append(
                    f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}"
                )
            (output_dir / "checksums.sha256").write_text(
                "\n".join(checksum_lines) + "\n", encoding="utf-8"
            )
            verified = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(ROOT / "scripts" / "verify_evidence_bundle.py"),
                    str(output_dir),
                ],
                check=False,
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
