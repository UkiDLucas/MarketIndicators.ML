# data_normalization

## Purpose
Convert heterogeneous raw indicator series into weekly aligned normalized datasets.

## Data Boundary

### Inputs
- `../data_ingestion/OUTPUT/raw/*.csv`

### Outputs
- `OUTPUT/weekly_normalized_long.csv`
- `OUTPUT/weekly_levels_wide.csv` (weekly levels for targets)
- `OUTPUT/weekly_growth_index_wide.csv` (rebased=100 growth trajectories)
- `OUTPUT/weekly_features_wide.csv` (ML features)
- `OUTPUT/weekly_normalized_wide.csv` (backward-compatible alias to growth index)

## Weekly Policy
1. Weekly key is week-ending Friday.
2. Last observed value in each week is used.
3. Features are stationary and forward-safe:
   - 1-week return
   - 4-week and 12-week momentum
   - 4-week volatility
   - 52-week rolling return z-score (no future lookahead)

## Lock-Free Shift to Next Stage
1. Normalization writes outputs fully before publish.
2. Prediction consumes only published canonical files.

## Run
```bash
./run.sh
```

## Proof of Concept Plot
```bash
./plot_all/run.sh
```

Notes:
- Default plot input is `OUTPUT/weekly_growth_index_wide.csv`.
- Plot wrapper rebases each visible series to 100 at the start of the plotted window for readability.
