# data_ingestion

## Purpose
Ingest indicator/source series into canonical raw artifacts with metadata.

## Shared vs Specific Logic

1. Shared ingestion logic (common path)
- URL preparation and provider handling
- Download/copy execution
- Snapshot fallback
- Metadata emission

2. Per-indicator corner cases (local path)
- Optional per-indicator override at:
  - `data_ingestion/indicators/<SYMBOL>/src/override.py`
- Intended hook points:
  - request customization
  - source parsing tweaks
  - validation rules

## Data Boundary

### Inputs
- Indicator configs under `indicators/<SYMBOL>/config.yaml`
- Target configs under `targets/<SYMBOL>/config.yaml`
- Legacy snapshot fallback CSVs under `INPUT/legacy_snapshots/original/`
- Legacy registry copy under `INPUT/legacy_registry/Indicators.csv`

### Outputs
- `OUTPUT/raw/<SYMBOL>.csv`
- `OUTPUT/metadata/<SYMBOL>.json`
- `OUTPUT/availability_report.csv`

## Lock-Free Shift to Next Stage

1. Ingestion writes raw and metadata files completely.
2. Each file is published atomically at final path.
3. Normalization reads only `OUTPUT/raw/*.csv` and never ingestion temp files.

## Run Modes

1. Default safe run
```bash
./run.sh
```

2. Full catalog strict run
```bash
python3 src/run_batch.py --availability OUTPUT/availability_report.csv
```

## Network Politeness (Recommended for Weekly Jobs)

- One request at a time only (no parallel fetches).
- Delay + jitter between requests to avoid burst traffic.
- Configurable environment knobs for `./run.sh`:
  - `INGEST_REMOTE_POLICY=auto|never`
  - `INGEST_TIMEOUT_SECONDS=30`
  - `INGEST_DELAY_SECONDS=8`
  - `INGEST_JITTER_SECONDS=2`
  - `INGEST_BEST_EFFORT=1`
  - `INGEST_INCLUDE_CATALOG=0`
