# Market Signals Platform

Market Signals Platform is a research and engineering pipeline for building actionable market-intelligence signals.
It ingests global indicators (market data, macro trends, and extensible sentiment/opinion sources), normalizes them to a weekly time base, and produces ML-ready feature tables plus trend-prediction artifacts for selected assets/indices.
The repository is the modular rebuild of the legacy MarketIndicators project, and runtime does not depend on the legacy archive folder.

## Long-Term Architecture Memory

Retained from legacy pipeline (`docs/legacy/Market Indicators pipeline.jpg`):
1. Source registry drives ingestion.
2. Raw snapshots are retained before transformations.
3. Consolidated feature tables are built before modeling.
4. Training is decoupled from prediction/report generation.

Current modular stages:
1. `data_ingestion/`
2. `data_normalization/`
3. `prediction/`

## Functional Requirements

1. Each module is independently runnable and documented.
2. Stage transitions happen through explicit file contracts only.
3. No module writes into another module's internal working files.
4. Stage handoff must be lock-free for readers and atomic for publishers.
5. Future UI (Swift) integration must call stable module entrypoints, not internal code.

## Data Boundary (Stage Contracts)

1. Ingestion -> Normalization boundary:
   - Canonical input to normalization: `data_ingestion/OUTPUT/raw/*.csv`
   - Metadata: `data_ingestion/OUTPUT/metadata/*.json`
   - Availability catalog: `data_ingestion/OUTPUT/availability_report.csv`

2. Normalization -> Prediction boundary:
   - Canonical features: `data_normalization/OUTPUT/weekly_features_wide.csv`
   - Canonical target levels: `data_normalization/OUTPUT/weekly_levels_wide.csv`
   - Growth visualization dataset: `data_normalization/OUTPUT/weekly_growth_index_wide.csv`
   - Supplementary audit table: `data_normalization/OUTPUT/weekly_normalized_long.csv`

3. Prediction outputs:
   - `prediction/OUTPUT/models/*.pkl`
   - `prediction/OUTPUT/metrics.csv`
   - `prediction/OUTPUT/predictions/*_predictions.csv`

See `DATA_BOUNDARY.md` for versioned contract details.

## Lock-Free Data Shift Policy

1. A stage writes to temp files first (same filesystem).
2. A stage publishes by atomic rename to final artifact path.
3. Downstream stages only read published artifact paths.
4. No in-place mutation of already-published artifacts.
5. Concurrent runs are isolated by run-specific temp paths.

See `LOCK_FREE_HANDOFF.md` for the operating protocol.

## Run

```bash
./run.sh
```

## Weekly Ingestion Etiquette

`data_ingestion/run.sh` is intentionally sequential and supports pacing controls to avoid aggressive traffic:

- `INGEST_DELAY_SECONDS` (default `8`)
- `INGEST_JITTER_SECONDS` (default `2`)
- `INGEST_TIMEOUT_SECONDS` (default `30`)
- `INGEST_REMOTE_POLICY` (`auto` or `never`)

This keeps fetches to one request at a time with spacing between calls.
