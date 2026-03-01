# GER_RET_SALES_M

## Purpose
Ingestion module for `GER_RET_SALES_M`.

## Source
- Full name: Germany Retail Sales m/m
- Primary URL: `https://www.mql5.com/en/economic-calendar/germany/retail-sales-mm/export`

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
- Raw series: `data_ingestion/OUTPUT/raw/GER_RET_SALES_M.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/GER_RET_SALES_M.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
