# targets

## Purpose
Container for target-series ingestion modules used directly by prediction targets.

## Why separate from indicators
- Targets may need different source policies.
- Targets are business-critical and can evolve independently.

## Data Boundary
Child modules publish to:
- `data_ingestion/OUTPUT/raw/`
- `data_ingestion/OUTPUT/metadata/`
