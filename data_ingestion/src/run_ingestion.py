#!/usr/bin/env python3
import argparse
from pathlib import Path

from ingestion_lib import fetch_indicator


def main():
    parser = argparse.ArgumentParser(description='Run ingestion for one indicator config file.')
    parser.add_argument('--config', required=True, help='Path to indicator config.yaml')
    parser.add_argument('--remote-policy', choices=['auto', 'never'], default='auto')
    parser.add_argument('--timeout-seconds', type=float, default=30.0)
    args = parser.parse_args()

    cfg = Path(args.config).resolve()
    result = fetch_indicator(cfg, remote_policy=args.remote_policy, timeout_seconds=args.timeout_seconds)

    status = result.get('status', 'unknown')
    symbol = result.get('symbol', 'UNKNOWN')
    print(f'[{symbol}] status={status} output={result.get("output_file", "")}')
    if status == 'failed':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
