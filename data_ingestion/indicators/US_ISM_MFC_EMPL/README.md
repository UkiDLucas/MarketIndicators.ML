# US_ISM_MFC_EMPL

## Purpose
Ingestion module for `US_ISM_MFC_EMPL`.

## Source
- Full name: ISM Manufacturing Employment
- Primary URL: `https://www.mql5.com/en/economic-calendar/united-states/ism-manufacturing-employment/export`

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
- Raw series: `data_ingestion/OUTPUT/raw/US_ISM_MFC_EMPL.csv`
- Metadata: `data_ingestion/OUTPUT/metadata/US_ISM_MFC_EMPL.json`

## Lock-Free Handoff
- This module must publish complete output files only.
- Downstream normalization reads published files, never temp files.

## Run
```bash
./run.sh
```
