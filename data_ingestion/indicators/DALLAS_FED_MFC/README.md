# DALLAS_FED_MFC

## Purpose
Ingestion module for `DALLAS_FED_MFC`.

## Source
- Full name: Federal Reserve Bank (Fed) of Dallas Manufacturing Index
- Primary URL: `https://www.mql5.com/en/economic-calendar/united-states/dallas-fed-manufacturing-business-index/export`

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
- Raw series: `data_ingestion/OUTPUT/raw/DALLAS_FED_MFC.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/DALLAS_FED_MFC.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
