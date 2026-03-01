#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REMOTE_POLICY="${INGEST_REMOTE_POLICY:-auto}"          # auto | never
TIMEOUT_SECONDS="${INGEST_TIMEOUT_SECONDS:-30}"        # per request timeout
DELAY_SECONDS="${INGEST_DELAY_SECONDS:-8}"             # fixed delay between requests
JITTER_SECONDS="${INGEST_JITTER_SECONDS:-2}"           # random extra delay
BEST_EFFORT="${INGEST_BEST_EFFORT:-1}"                # 1 = continue on failures
INCLUDE_CATALOG="${INGEST_INCLUDE_CATALOG:-0}"         # 1 = run full indicators catalog

TARGET_CMD=(
  python3 "${SCRIPT_DIR}/src/run_targets.py"
  --targets-dir "${SCRIPT_DIR}/targets"
  --remote-policy "${REMOTE_POLICY}"
  --timeout-seconds "${TIMEOUT_SECONDS}"
  --delay-seconds "${DELAY_SECONDS}"
  --jitter-seconds "${JITTER_SECONDS}"
)
if [[ "${BEST_EFFORT}" == "1" ]]; then
  TARGET_CMD+=(--best-effort)
fi
"${TARGET_CMD[@]}"

if [[ "${INCLUDE_CATALOG}" == "1" ]]; then
  CATALOG_CMD=(
    python3 "${SCRIPT_DIR}/src/run_batch.py"
    --availability "${SCRIPT_DIR}/OUTPUT/availability_report.csv"
    --remote-policy "${REMOTE_POLICY}"
    --timeout-seconds "${TIMEOUT_SECONDS}"
    --delay-seconds "${DELAY_SECONDS}"
    --jitter-seconds "${JITTER_SECONDS}"
  )
  if [[ "${BEST_EFFORT}" == "1" ]]; then
    CATALOG_CMD+=(--best-effort)
  fi
  "${CATALOG_CMD[@]}"
fi
