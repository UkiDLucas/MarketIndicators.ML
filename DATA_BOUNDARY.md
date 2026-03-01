# Data Boundary Contract

## Version
- Contract version: `v0.1`

## Stage 1: data_ingestion

### Inputs
- Per-indicator config: `data_ingestion/indicators/<SYMBOL>/config.yaml`
- Optional target configs: `data_ingestion/targets/<SYMBOL>/config.yaml`

### Outputs
- Raw source data: `data_ingestion/OUTPUT/raw/<SYMBOL>.csv`
- Ingestion metadata: `data_ingestion/OUTPUT/metadata/<SYMBOL>.json`
- Registry-derived catalog: `data_ingestion/OUTPUT/availability_report.csv`

### Output Guarantees
- `<SYMBOL>.json` always contains `status` and `output_file`.
- Failed ingestion must still emit metadata with error reason.

## Stage 2: data_normalization

### Inputs
- `data_ingestion/OUTPUT/raw/*.csv`

### Outputs
- Long-form weekly data: `data_normalization/OUTPUT/weekly_normalized_long.csv`
- Weekly levels wide: `data_normalization/OUTPUT/weekly_levels_wide.csv`
- Weekly growth index wide: `data_normalization/OUTPUT/weekly_growth_index_wide.csv`
- Weekly ML features wide: `data_normalization/OUTPUT/weekly_features_wide.csv`
- Backward-compatible alias: `data_normalization/OUTPUT/weekly_normalized_wide.csv`

### Output Guarantees
- `week_end` is the temporal key.
- Level and growth datasets preserve trajectory information for visualization and sanity checks.
- ML feature dataset contains stationary features intended for model training.

## Stage 3: prediction

### Inputs
- `data_normalization/OUTPUT/weekly_features_wide.csv`
- `data_normalization/OUTPUT/weekly_levels_wide.csv`

### Outputs
- Per-target model artifact: `prediction/OUTPUT/models/<TARGET>.pkl`
- Per-target prediction table: `prediction/OUTPUT/predictions/<TARGET>_predictions.csv`
- Global training summary: `prediction/OUTPUT/metrics.csv`

### Output Guarantees
- `metrics.csv` includes one row per configured target with training status.
- Missing target series must be explicit via status value (not silent omission).
