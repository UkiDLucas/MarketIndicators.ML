# Legacy Pipeline Architecture Value

Source: `docs/legacy/Market Indicators pipeline.jpg`

## What Still Has High Value
1. Source registry as first-class input (`Indicators.csv`) is correct and should stay.
2. Keep raw immutable snapshots before transformations.
3. Build a unified feature table before model training.
4. Separate training from prediction/report generation.
5. Keep generated artifacts (tables/plots) deterministic and reviewable.

## What Needed Modernization
1. Replace ad-hoc looping with module CLIs and explicit scheduling.
2. Move from daily-heavy logic to weekly normalization for stability/noise reduction.
3. Remove tight coupling between ingestion and modeling code paths.
4. Add model metrics and persisted regression artifacts per target symbol.
