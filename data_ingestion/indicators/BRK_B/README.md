# BRK_B

## Purpose
Ingestion module for `BRK_B`.

## Source
- Full name: Berkshire Hathaway Inc. (BRK-B)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/BRK-B?period1=831600000&period2=1607990400&interval=1d&events=history&includeAdjustedClose=true`

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
- Raw series: `data_ingestion/OUTPUT/raw/BRK_B.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/BRK_B.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
