# PocketBarrister Repository Instructions

## Immutable legacy snapshot

`experiments/legacy_v0/` is an immutable historical snapshot of the original PocketBarrister experiment.

- Read legacy files freely for audit, comparison, and evidence gathering.
- Never edit, format, rename, move, delete, regenerate, or add files inside `experiments/legacy_v0/`.
- Never move a legacy file back into the canonical implementation.
- Never silently fix defects in a legacy dataset, script, notebook, adapter artifact, image, or document.
- Create every correction, redesigned dataset, script, configuration, report, and model artifact outside `experiments/legacy_v0/`.
- If canonical work derives from a legacy artifact, preserve traceability with source paths and hashes rather than modifying the source.
- Only mutate the snapshot when the user explicitly instructs that exact legacy mutation and acknowledges that it changes the historical record.

Before and after work that reads or derives from the snapshot, verify it with:

```powershell
python -B analysis/verify_legacy_snapshot.py
```

The portable authoritative baseline is `manifests/legacy_v0.sha256`; it covers the 40 Git-tracked files and normalizes text line endings for cross-platform verification. `manifests/legacy_v0.local-artifacts.sha256` separately records the four large gitignored artifacts. Default verification accepts their absence in Git/Colab checkouts but verifies them when present. Use `python -B analysis/verify_legacy_snapshot.py --require-local-artifacts` for a complete local check. Do not update either manifest merely to make an unexpected verification failure pass. A baseline-content change requires explicit user authorization.

