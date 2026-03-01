# Functional Requirements: NASDX

1. Fetch raw historical series for `NASDX`.
2. Save raw CSV to `data_ingestion/OUTPUT/raw/NASDX.csv`.
3. Persist metadata JSON to `data_ingestion/OUTPUT/metadata/NASDX.json`.
4. Use local snapshot fallback when available.
