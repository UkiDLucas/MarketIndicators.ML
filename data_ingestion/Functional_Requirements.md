# Functional Requirements: data_ingestion

1. Module must read only from `INPUT/` and declared external inputs in `config.yaml`.
2. Module must write deterministic outputs into `OUTPUT/`.
3. Module must log key execution metadata for traceability.
4. Module must fail with explicit errors and no partial silent corruption.
5. Module must be runnable via `run.sh`.
