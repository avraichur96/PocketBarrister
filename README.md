# Pocket Barrister 

Pocket Barrister is an early-stage machine learning experiment exploring whether LoRA fine-tuning can teach Gemma 2B to produce structured legal analysis for synthetic Indian-law hypotheticals.

The current repository preserves the original dataset-generation and training experiment while a cleaner, reproducible pipeline is developed incrementally. 
This is work in progress and metrics for some interesting tests are coming soon! :)  

## Current status

- Original training notebook, dataset generators, datasets, evaluation prompts, and adapter artifacts are preserved under `experiments/legacy_v0/`.
- The existing material is an experimental legacy snapshot, not a production-ready model or validated legal dataset.
- **Phase 1 legal review is in progress:** all 13 proposed source families are registered in the [legal adjudication matrix](reports/LEGAL_ADJUDICATION_MATRIX.md); legal authority verification and expected-state approval remain at 0/13.
- The completed [dataset audit](reports/DATASET_AUDIT.md) found that neither legacy candidate dataset should be used as-is.
- **Phase 2 engineering is runnable:** a deterministic provisional build produces 62 validated records and family-disjoint 43/9/10 splits. See the [build report](reports/PROVISIONAL_DATASET.md).
- **Phase 3 core organization is underway:** data, training-format, and structural-evaluation code now live in an import-safe package with CLI wrappers and tests.
- The first [Colab QLoRA notebook](notebooks/PocketBarrister_QLoRA_Colab.ipynb) is ready to produce the adapter, raw base/adapter predictions, metrics, and run metadata.
- Large legacy adapter and tokenizer binaries are currently kept local and excluded from Git.

### Phase 1 progress

| Milestone | Progress |
|---|---:|
| Candidate-family inventory | 13/13 |
| Source-lineage and structural-defect triage | 13/13 |
| Provisional records passing validation | 62/62 |
| Family overlap across train/validation/test | 0 |
| Legal authority verification | 0/13 |
| Expected-state approval | 0/13 |
| Canonical admission decisions | 0/13 |

The provisional dataset lets engineering and initial adapter training proceed without implying that inherited legal labels are correct. Legal review is still required before a reviewed canonical dataset or legal-accuracy claim.

## Reproduce the data pipeline

The local pipeline uses only the Python standard library:

```powershell
python -B scripts/build_dataset.py
python -B scripts/validate_dataset.py
$env:PYTHONPATH = "src"
python -B -m unittest discover -s tests -v
```

The build pins its source hash, records every structural repair and exclusion, and produces deterministic dataset and split hashes in `data/provisional_v0/manifest.json`.

## Repository layout

```text
configs/          Versioned dataset and QLoRA settings
data/             Provisional dataset, splits, and immutable build manifest
notebooks/        Colab training and base-versus-adapter runbook
scripts/          Build, validate, and prediction-scoring CLIs
src/              Import-safe canonical Python package
tests/            Data, formatting, and metric tests
reports/          Audit, matrix, and dataset-build evidence
experiments/
  legacy_v0/    Original experiment preserved for traceability
```

Generated adapters and evaluation results remain ignored until an actual run is inspected and intentionally selected for publication.

## Using the legacy experiment

Legacy scripts use paths relative to their working directory. If you inspect or run them, start from the snapshot directory:

```powershell
Set-Location experiments/legacy_v0
```

The legacy files have known reproducibility and data-quality limitations. They are retained as historical experiment artifacts and will not be silently rewritten.

## Intended project outcomes

The completed repository should provide:

- A documented and validated dataset format.
- Deterministic dataset generation and split manifests.
- Reproducible LoRA training configuration.
- Base-model versus adapter evaluation cases and metrics.
- Raw predictions, representative examples, and failure analysis.
- A clear model card, dataset card, limitations, and licensing information.

## Disclaimer

This project is for machine learning research and educational demonstration only. It does not provide legal advice, and its synthetic examples and model outputs must not be relied upon for legal decisions.
