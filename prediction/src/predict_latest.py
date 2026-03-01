#!/usr/bin/env python3
import argparse
import pickle
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description='Predict next week return and implied level for one target model.')
    parser.add_argument('--model', required=True)
    parser.add_argument('--features-wide', required=True)
    parser.add_argument('--levels-wide', required=True)
    args = parser.parse_args()

    model_path = Path(args.model).resolve()
    features_path = Path(args.features_wide).resolve()
    levels_path = Path(args.levels_wide).resolve()

    with model_path.open('rb') as fh:
        payload = pickle.load(fh)

    model = payload['model']
    feature_cols = payload['feature_cols']
    target = payload['target']

    features_df = pd.read_csv(features_path)
    levels_df = pd.read_csv(levels_path)
    for df in (features_df, levels_df):
        if 'week_end' not in df.columns:
            raise SystemExit('Expected week_end column')
        df['week_end'] = pd.to_datetime(df['week_end'], errors='coerce')

    features_df = features_df.dropna(subset=['week_end']).sort_values('week_end').set_index('week_end')
    levels_df = levels_df.dropna(subset=['week_end']).sort_values('week_end').set_index('week_end')

    latest_features = features_df[feature_cols].dropna().tail(1)
    if latest_features.empty:
        raise SystemExit('No complete latest feature row available')

    latest_week = latest_features.index[-1]
    if target not in levels_df.columns or latest_week not in levels_df.index:
        raise SystemExit(f'Cannot locate current level for target {target}')

    current_level = float(levels_df.loc[latest_week, target])
    pred_return = float(model.predict(latest_features)[0])
    implied_next = current_level * (1.0 + pred_return)

    print(f'target={target}')
    print(f'week_end={latest_week.date()}')
    print(f'pred_return={pred_return:.6f}')
    print(f'current_level={current_level:.6f}')
    print(f'implied_next_level={implied_next:.6f}')


if __name__ == '__main__':
    main()
