# Evaluation runs

Each Colab execution produces two downloads:

- `<run-id>-evidence.zip` — small, reviewable experiment evidence intended for this repository.
- `<run-id>-adapter.zip` — model adapter files; keep local until publication and license decisions are complete.

## Import an evidence run

1. Extract the evidence archive into `eval/runs/<run-id>/` without changing its internal `results/` and `provenance/` directories.
2. Verify it from the repository root:

   ```powershell
   python -B scripts/verify_evidence_bundle.py eval/runs/<run-id>
   ```

3. Inspect `results/RUN_CARD.md`, `results/METRICS.md`, raw predictions, and automatic failures.
4. Complete `results/manual_review.csv` for role binding, legal-effect consistency, final conclusions, contradictions, and unsupported legal claims.
5. Commit the reviewed evidence directory intentionally. Do not commit the adapter archive by default.

## Evidence files from one run

```text
results/
  RUN_CARD.md
  METRICS.md
  predictions.jsonl
  per_case_metrics.jsonl
  summary_metrics.json
  metrics_table.csv
  automatic_failures.jsonl
  manual_review.csv
  run_metadata.json
  training_history.json
  environment.txt
provenance/
  dataset_provisional_v0.json
  gemma_2b_qlora_provisional_v0.yaml
  manifest.json
  test.jsonl
checksums.sha256
```

Automatic metrics remain provisional because expected answers are inherited from legally unreviewed synthetic data. The blank manual-review fields are deliberate and must not be silently converted into passing scores.
