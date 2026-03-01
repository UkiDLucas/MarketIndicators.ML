# US_HOUS_STRS_M

## Purpose
Ingestion module for `US_HOUS_STRS_M`.

## Source
- Full name: United States Housing Starts m/m
- Primary URL: `https://www.mql5.com/en/economic-calendar/united-states/housing-starts-mm/export`

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
- Raw series: `data_ingestion/OUTPUT/raw/US_HOUS_STRS_M.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/US_HOUS_STRS_M.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
