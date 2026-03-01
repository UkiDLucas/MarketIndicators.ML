#!/usr/bin/env python3
import argparse
import csv
from pathlib import Path

from ingestion_lib import fetch_indicator


def main():
    parser = argparse.ArgumentParser(description='Run ingestion for many indicator configs.')
    parser.add_argument('--availability', default='../OUTPUT/availability_report.csv', help='Availability CSV path')
    parser.add_argument('--limit', type=int, default=0, help='Optional max number of indicators to process')
    args = parser.parse_args()

    availability_csv = Path(args.availability).resolve()
    rows = []
    with availability_csv.open(newline='', encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))

    count = 0
    failures = 0
    for row in rows:
        symbol = row['symbol']
        cfg_path = Path(row['config_path']).resolve()
        if not cfg_path.exists():
            print(f'[SKIP] {symbol} missing config: {cfg_path}')
            failures += 1
            continue

        result = fetch_indicator(cfg_path)
        status = result.get('status')
        print(f'[{symbol}] {status}')
        count += 1
        if status == 'failed':
            failures += 1

        if args.limit and count >= args.limit:
            break

    print(f'Processed={count} Failed={failures}')
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
