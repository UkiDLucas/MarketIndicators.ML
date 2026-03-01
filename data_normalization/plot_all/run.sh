#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODULE_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"

INPUT_FILE="${PLOT_INPUT_FILE:-${MODULE_DIR}/OUTPUT/weekly_growth_index_wide.csv}"
OUTPUT_FILE="${PLOT_OUTPUT_FILE:-${MODULE_DIR}/OUTPUT/indicators_poc.png}"
LOOKBACK_WEEKS="${PLOT_LOOKBACK_WEEKS:-220}"
MAX_SERIES="${PLOT_MAX_SERIES:-10}"
REBASE_WINDOW_START="${PLOT_REBASE_WINDOW_START:-1}"

CMD=(
  python3 "${MODULE_DIR}/src/plot_indicators_poc.py"
  --input "${INPUT_FILE}" \
  --output "${OUTPUT_FILE}" \
  --lookback-weeks "${LOOKBACK_WEEKS}" \
  --max-series "${MAX_SERIES}"
)

if [[ "${REBASE_WINDOW_START}" == "1" ]]; then
  CMD+=(--rebase-window-start)
fi

"${CMD[@]}" "$@"

echo "Saved plot: ${OUTPUT_FILE}"
