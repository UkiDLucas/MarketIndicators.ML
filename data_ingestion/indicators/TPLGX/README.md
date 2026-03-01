# TPLGX

## Purpose
Ingestion module for `TPLGX`.

## Source
- Full name: T. Rowe Price Institutional Large Cap Core Growth Fund (TPLGX)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/TPLGX?period1=1064966400&period2=1607904000&interval=1d&events=history&includeAdjustedClose=true`

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
- Raw series: `data_ingestion/OUTPUT/raw/TPLGX.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/TPLGX.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
