# legacy_snapshots

Fallback-only historical source data copied from the legacy project.

## Contract
1. Files in `original/*.csv` are read-only baselines.
2. Ingestion may copy them to `OUTPUT/raw/` when remote fetch is skipped or fails.
3. These files are not treated as current market data.
