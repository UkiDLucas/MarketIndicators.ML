#!/usr/bin/env python3
import argparse
import random
import time
from pathlib import Path

from ingestion_lib import fetch_indicator


TARGETS = ['NASDX', 'SWPPX', 'VUG', 'QQQ', 'ATRFX', 'VTI', 'TSLA', 'DIA', 'ROBO', 'AAPL']


def main():
    parser = argparse.ArgumentParser(description='Run ingestion for prediction target symbols.')
    parser.add_argument('--targets-dir', default='../targets')
    parser.add_argument('--best-effort', action='store_true', help='Do not fail process when some targets fail.')
    parser.add_argument('--remote-policy', choices=['auto', 'never'], default='auto')
    parser.add_argument('--timeout-seconds', type=float, default=30.0)
    parser.add_argument('--delay-seconds', type=float, default=7.0)
    parser.add_argument('--jitter-seconds', type=float, default=2.0)
    args = parser.parse_args()

    targets_dir = Path(args.targets_dir).resolve()
    failures = 0
    for idx, symbol in enumerate(TARGETS):
        cfg = targets_dir / symbol / 'config.yaml'
        if not cfg.exists():
            print(f'[SKIP] {symbol} missing config')
            failures += 1
            continue
        result = fetch_indicator(
            cfg,
            remote_policy=args.remote_policy,
            timeout_seconds=args.timeout_seconds,
        )
        print(f'[{symbol}] {result.get("status")}')
        if result.get('status') == 'failed':
            failures += 1
        is_last = idx == (len(TARGETS) - 1)
        wait_s = max(args.delay_seconds, 0.0) + random.uniform(0.0, max(args.jitter_seconds, 0.0))
        if (not is_last) and wait_s > 0:
            print(f'[WAIT] sleeping {wait_s:.2f}s before next request')
            time.sleep(wait_s)

    if failures and not args.best_effort:
        print(f'Target ingestion failures: {failures}')
        raise SystemExit(1)


if __name__ == '__main__':
    main()
