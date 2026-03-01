# prediction

## Purpose
Train and evaluate weekly regression models for configured targets.

## Target Set
- NASDX
- SWPPX
- VUG
- QQQ
- ATRFX
- VTI
- TSLA
- DIA
- ROBO
- AAPL

## Data Boundary

### Inputs
- `../data_normalization/OUTPUT/weekly_features_wide.csv`
- `../data_normalization/OUTPUT/weekly_levels_wide.csv`

### Outputs
- `OUTPUT/models/<TARGET>.pkl`
- `OUTPUT/predictions/<TARGET>_predictions.csv`
- `OUTPUT/metrics.csv`

## Status Semantics
- `trained`: model produced successfully.
- `missing_target_series`: required target column not present.
- `insufficient_data`: target exists but not enough rows to train safely.

## Target Definition
- Target variable is next-week return for each symbol.
- Prediction outputs also include implied next-week level using current level.

## Lock-Free Behavior
- Existing published artifacts are replaced atomically.
- Readers should consume only fully published files.

## Run
```bash
./run.sh
```
