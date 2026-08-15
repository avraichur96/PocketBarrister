# Data

`provisional_v0/` is deterministically derived from the immutable legacy source by `scripts/build_dataset.py`.

This is a synthetic, legally unreviewed engineering dataset. Its expected states are inherited from legacy outputs and must not be represented as legally validated. The structural placeholder repairs recorded in each sample do not change its inherited semantic label.

Build and validate from the repository root:

```powershell
python -B scripts/build_dataset.py
python -B scripts/validate_dataset.py
```

The generated manifest pins the source/config/dataset/split hashes and records excluded source IDs. Families—not rows—are assigned to one split each, preventing cosmetic variants of the same legacy template from crossing splits.
