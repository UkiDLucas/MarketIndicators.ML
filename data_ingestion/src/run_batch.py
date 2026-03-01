#!/usr/bin/env python3
import argparse
import csv
import random
import time
from pathlib import Path

from ingestion_lib import fetch_indicator


def main():
    parser = argparse.ArgumentParser(description='Run ingestion for many indicator configs.')
    parser.add_argument('--availability', default='../OUTPUT/availability_report.csv', help='Availability CSV path')
    parser.add_argument('--limit', type=int, default=0, help='Optional max number of indicators to process')
    parser.add_argument('--remote-policy', choices=['auto', 'never'], default='auto')
    parser.add_argument('--timeout-seconds', type=float, default=30.0)
    parser.add_argument('--delay-seconds', type=float, default=7.0)
    parser.add_argument('--jitter-seconds', type=float, default=2.0)
    parser.add_argument('--best-effort', action='store_true', help='Do not fail process when some symbols fail.')
    args = parser.parse_args()

    availability_csv = Path(args.availability).resolve()
    rows = []
    with availability_csv.open(newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))

    count = 0
    failures = 0
    for idx, row in enumerate(rows):
        symbol = row['symbol']
        cfg_path = Path(row['config_path']).resolve()
        if not cfg_path.exists():
            print(f'[SKIP] {symbol} missing config: {cfg_path}')
            failures += 1
            continue

        result = fetch_indicator(
            cfg_path,
            remote_policy=args.remote_policy,
            timeout_seconds=args.timeout_seconds,
        )
        status = result.get('status')
        print(f'[{symbol}] {status}')
        count += 1
        if status == 'failed':
            failures += 1

        if args.limit and count >= args.limit:
            break

        is_last = idx == (len(rows) - 1)
        wait_s = max(args.delay_seconds, 0.0) + random.uniform(0.0, max(args.jitter_seconds, 0.0))
        if (not is_last) and wait_s > 0:
            print(f'[WAIT] sleeping {wait_s:.2f}s before next request')
            time.sleep(wait_s)

    print(f'Processed={count} Failed={failures}')
    if failures and not args.best_effort:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
