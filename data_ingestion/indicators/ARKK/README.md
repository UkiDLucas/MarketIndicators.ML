# ARKK

## Purpose
Ingestion module for `ARKK`.

## Source
- Full name: ARK Innovation ETF (ARKK)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/ARKK?period1=1414713600&period2=1608249600&interval=1d&events=history&includeAdjustedClose=true`

## Shared Functionality Used
- Common ingestion engine: `data_ingestion/src/ingestion_lib.py`
- Common runner: `data_ingestion/src/run_ingestion.py`

## Corner Cases (Module-Specific)
- Optional override file: `src/override.py`
- Use this only when config-only behavior is insufficient.

## Data Boundary

### Input
- `config.yaml` in this directory

### Output
- Raw series: `data_ingestion/OUTPUT/raw/ARKK.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/ARKK.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
