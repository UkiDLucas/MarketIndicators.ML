#!/usr/bin/env python3
import argparse
import pickle
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Predict next week value for one trained target model.')
    parser.add_argument('--model', required=True)
    parser.add_argument('--normalized-wide', required=True)
    args = parser.parse_args()

    model_path = Path(args.model).resolve()
    wide_path = Path(args.normalized_wide).resolve()

    with model_path.open('rb') as fh:
        payload = pickle.load(fh)

    model = payload['model']
    feature_cols = payload['feature_cols']
    target = payload['target']

    df = pd.read_csv(wide_path)
    if 'week_end' in df.columns:
        df = df.sort_values('week_end').set_index('week_end')
    latest = df[feature_cols].dropna().tail(1)
    if latest.empty:
        raise SystemExit('No complete latest feature row available')

    pred = float(model.predict(latest.to_numpy(dtype=float))[0])
    print(f'target={target} next_week_prediction={pred:.6f}')


if __name__ == '__main__':
    main()
