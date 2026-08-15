# Pocket Barrister 

Pocket Barrister is an early-stage machine learning experiment exploring whether LoRA fine-tuning can teach Gemma 2B to produce structured legal analysis for synthetic Indian-law hypotheticals.

The current repository preserves the original dataset-generation and training experiment while a cleaner, reproducible pipeline is developed incrementally.

## Current status

- Original training notebook, dataset generators, datasets, evaluation prompts, and adapter artifacts are preserved under `experiments/legacy_v0/`.
- The existing material is an experimental legacy snapshot, not a production-ready model or validated legal dataset.
- Dataset validation, reproducible training, formal evaluation, and documented before/after results are planned next.
- Large legacy adapter and tokenizer binaries are currently kept local and excluded from Git.

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
