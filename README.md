# Pocket Barrister 

Pocket Barrister is an early-stage machine learning experiment exploring whether LoRA fine-tuning can teach Gemma 2B to produce structured legal analysis for synthetic Indian-law hypotheticals.

The current repository preserves the original dataset-generation and training experiment while a cleaner, reproducible pipeline is developed incrementally. 
This is work in progress and metrics for some interesting tests are coming soon! :)  

## Current status

- Original training notebook, dataset generators, datasets, evaluation prompts, and adapter artifacts are preserved under `experiments/legacy_v0/`.
- The existing material is an experimental legacy snapshot, not a production-ready model or validated legal dataset.
- **Phase 1 is in progress:** all 13 proposed source families are now registered in the [legal adjudication matrix](reports/LEGAL_ADJUDICATION_MATRIX.md); legal authority verification and expected-state approval remain at 0/13.
- The completed [dataset audit](reports/DATASET_AUDIT.md) found that neither legacy candidate dataset should be used as-is.
- Dataset validation, reproducible training, formal evaluation, and documented before/after results remain future work.
- Large legacy adapter and tokenizer binaries are currently kept local and excluded from Git.

### Phase 1 progress

| Milestone | Progress |
|---|---:|
| Candidate-family inventory | 13/13 |
| Source-lineage and structural-defect triage | 13/13 |
| Legal authority verification | 0/13 |
| Expected-state approval | 0/13 |
| Canonical admission decisions | 0/13 |

The current task is to adjudicate each candidate family before repairing records, generating variants, or creating train/evaluation splits.

## Repository layout

```text
experiments/
  legacy_v0/    Original experiment preserved for traceability
```

The canonical package, configurations, evaluation pipeline, reports, and tests will be added as the project is refactored.

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
