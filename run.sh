#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"${ROOT_DIR}/data_ingestion/run.sh"
"${ROOT_DIR}/data_normalization/run.sh"
"${ROOT_DIR}/prediction/run.sh"
