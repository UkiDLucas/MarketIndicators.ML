# data_ingestion

Downloads or snapshots indicator CSVs into `OUTPUT/raw/`.

## Inputs
- Source registry: `OLD/src/DATA/Indicators.csv`
- Per-source configs under `indicators/<SYMBOL>/config.yaml`

## Outputs
- Raw files: `OUTPUT/raw/*.csv`
- Metadata: `OUTPUT/metadata/*.json`
- Availability index: `OUTPUT/availability_report.csv`

## Implemented Source Runners (explicit)
- `AAPL`, `TSLA`, `BABA`, `GSPC`, `VIX`

Other source directories are scaffolded and runnable through the generic ingestion runner.
