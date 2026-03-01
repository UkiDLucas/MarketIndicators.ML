# ROBO

## Purpose
Target-series ingestion module for prediction target `ROBO`.

## Shared Functionality Used
- Common ingestion engine: `data_ingestion/src/ingestion_lib.py`
- Common runner: `data_ingestion/src/run_ingestion.py`

## Corner Cases (Module-Specific)
- Optional override file: `src/override.py`
- Intended for symbol-specific source parsing or validation.

## Data Boundary

### Input
- `config.yaml`

### Output
- Raw series: `data_ingestion/OUTPUT/raw/ROBO.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/ROBO.json`

## Lock-Free Handoff
- Publish complete output file atomically.
- Prediction stage never reads intermediate files.

## Run
```bash
./run.sh
```
