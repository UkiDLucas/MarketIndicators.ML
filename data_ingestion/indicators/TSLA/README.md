# TSLA

## Purpose
Ingestion module for `TSLA`.

## Source
- Full name: Tesla, Inc. (TSLA)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/TSLA?period1=1277769600&period2=1602028800&interval=1d&events=history`

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
- Raw series: `data_ingestion/OUTPUT/raw/TSLA.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/TSLA.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
