# Provisional Dataset Build

Status: **Ready for an engineering-only adapter run**

The first pipeline dataset is intentionally labeled `0.1.0-provisional`. It exists to test data preparation, QLoRA training, artifact capture, and base-versus-adapter evaluation before legal adjudication is complete.

## Build result

| Measure | Result |
|---|---:|
| Records | 62 |
| Candidate families represented | 13/13 |
| Train / validation / test | 43 / 9 / 10 |
| Family overlap across splits | 0 |
| Unresolved placeholders | 0 |
| Opposing-role collision records retained | 0 |
| Exact duplicate inputs | 0 |
| Exact duplicate outputs | 0 |
| Legally reviewed records | 0/62 |

The build selects at most five deterministic variants per family. Five supplier records in which one company occupied both opposing roles are excluded, as are exact repeated outputs. Named generator placeholders are resolved from the saved facts, and each repair is recorded per sample. No inherited legal finding, conclusion, or remedy is silently corrected.

## Reproduce

```powershell
python -B scripts/build_dataset.py
python -B scripts/validate_dataset.py
```

Hashes and exclusions are recorded in `data/provisional_v0/manifest.json`.

## Claim boundary

Results from this dataset can support engineering claims about reproducibility, output structure, stopping, and reproduction of inherited expected-state fields. They cannot support claims that the model is legally correct. The dataset remains ineligible for a canonical reviewed release until the adjudication matrix is completed.
