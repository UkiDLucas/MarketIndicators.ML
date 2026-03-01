# indicators

## Purpose
Container for source-specific ingestion modules derived from legacy registry.

## Module Rule
Each child symbol directory is autonomous and contains:
- README.md
- Functional_Requirements.md
- Project.toml
- config.yaml
- INPUT/
- OUTPUT/
- src/
- TESTS/
- run.sh

## Data Boundary
Child modules publish to shared ingestion boundary only:
- `data_ingestion/OUTPUT/raw/`
- `data_ingestion/OUTPUT/metadata/`
