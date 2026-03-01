# DJIA

## Purpose
Ingestion module for `DJIA`.

## Source
- Full name: Dow Jones Industrial Average (^DJI)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/%5EDJI?period1=475804800&period2=1602028800&interval=1d&events=history&includeAdjustedClose=true`

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
- Raw series: `data_ingestion/OUTPUT/raw/DJIA.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/DJIA.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
