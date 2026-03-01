# BTC_USD

## Purpose
Ingestion module for `BTC_USD`.

## Source
- Full name: Bitcoin USD (BTC-USD)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/BTC-USD?period1=1410825600&period2=1602633600&interval=1d&events=history&includeAdjustedClose=true`

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
- Raw series: `data_ingestion/OUTPUT/raw/BTC_USD.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/BTC_USD.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
