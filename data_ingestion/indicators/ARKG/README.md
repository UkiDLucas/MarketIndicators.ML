# ARKG

## Purpose
Ingestion module for `ARKG`.

## Source
- Full name: ARK Genomic Revolution ETF (ARKG)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/ARKG?period1=1577404800&period2=1608249600&interval=1d&events=history&includeAdjustedClose=true`

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
- Raw series: `data_ingestion/OUTPUT/raw/ARKG.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/ARKG.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
