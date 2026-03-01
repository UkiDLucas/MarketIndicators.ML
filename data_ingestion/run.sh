#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "${SCRIPT_DIR}/src/run_batch.py" --availability "${SCRIPT_DIR}/OUTPUT/availability_report.csv" "$@"
