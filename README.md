# Market Signals Platform

This repository is the long-term rebuild of the legacy MarketIndicators project.
Legacy code and assets are preserved in `OLD/` as historical reference.

## Purpose

Build a modular system that:
1. Ingests global indicators (market and macro sources first, opinion signals next).
2. Normalizes data on a weekly cadence.
3. Trains and evaluates regression models for target symbols.
4. Keeps every stage independently runnable and replaceable.

## Architecture (Long-Term Memory)

Retained architecture from the legacy pipeline image (`OLD/src/images/Market Indicators pipeline.jpg`):
1. Source registry drives ingestion.
2. Raw snapshots are preserved before transformation.
3. Features are consolidated before model training.
4. Training and prediction are separate stages.
5. Outputs are persisted as deterministic artifacts.

Modernized architecture in this repo:
1. `data_ingestion/`: source-specific download/snapshot modules.
2. `data_normalization/`: weekly alignment + normalization output.
3. `prediction/`: per-target regression model training and predictions.

Data flow:
1. `OLD/src/DATA/Indicators.csv` -> `data_ingestion/indicators/*`
2. `data_ingestion/OUTPUT/raw/*.csv` -> `data_normalization/OUTPUT/weekly_normalized_*.csv`
3. `data_normalization/OUTPUT/weekly_normalized_wide.csv` -> `prediction/OUTPUT/*`

## Functional Requirements

1. **Module boundaries**
   - Each module must own its `README.md`, `Functional_Requirements.md`, `config.yaml`, `INPUT/`, `OUTPUT/`, `src/`, `TESTS/`, and `run.sh`.
   - Modules communicate through files, not internal imports across module boundaries.

2. **Ingestion**
   - Create one ingestion directory per indicator in `OLD/src/DATA/Indicators.csv`.
   - Store raw CSV snapshots under `data_ingestion/OUTPUT/raw/`.
   - Store ingestion metadata under `data_ingestion/OUTPUT/metadata/`.
   - Support local snapshot fallback for resilience.

3. **Weekly normalization**
   - Convert source data to weekly series.
   - Produce both long and wide normalized datasets.
   - Persist outputs deterministically:
     - `data_normalization/OUTPUT/weekly_normalized_long.csv`
     - `data_normalization/OUTPUT/weekly_normalized_wide.csv`

4. **Prediction**
   - Implement regression training for:
     - `NASDX, SWPPX, VUG, QQQ, ATRFX, VTI, TSLA, DIA, ROBO, AAPL`
   - Save trained artifacts, metrics, and prediction tables under `prediction/OUTPUT/`.

5. **Auditability**
   - Every run must generate inspectable file outputs and status traces.
   - No silent writes outside declared output folders.

## Repository Map

- `data_ingestion/` ingestion framework + per-indicator modules
- `data_normalization/` weekly feature normalization
- `prediction/` regression training/prediction
- `ARCHITECTURE_FROM_LEGACY_IMAGE.md` retained architecture value notes
- `OLD/` immutable legacy reference

## Execution

Run full pipeline:

```bash
./run.sh
```

Run module by module:

```bash
./data_ingestion/run.sh
./data_normalization/run.sh
./prediction/run.sh
```
