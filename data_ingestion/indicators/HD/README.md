# HD

## Purpose
Ingestion module for `HD`.

## Source
- Full name: The Home Depot, Inc. (HD)
- Primary URL: `https://query1.finance.yahoo.com/v7/finance/download/HD?period1=369964800&period2=1602028800&interval=1d&events=history`

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
- Raw series: `data_ingestion/OUTPUT/raw/HD.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/HD.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
