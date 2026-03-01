#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd


def _parse_scalar(raw: str):
    value = raw.strip()
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    return value


def load_simple_yaml(path: Path):
    data = {}
    section = None
    for line in path.read_text(encoding='utf-8').splitlines():
        raw = line.split('#', 1)[0].rstrip()
        if not raw.strip():
            continue
        if raw.lstrip() != raw:
            if section is None or ':' not in raw:
                continue
            k, v = raw.strip().split(':', 1)
            data[section][k.strip()] = _parse_scalar(v)
            continue
        if raw.endswith(':'):
            section = raw[:-1].strip()
            data[section] = {}
            continue
        if ':' in raw:
            k, v = raw.split(':', 1)
            data[k.strip()] = _parse_scalar(v)
            section = None
    return data


def resolve_path(base: Path, raw_path: str):
    p = Path(raw_path)
    return p if p.is_absolute() else (base / p).resolve()


def detect_date_column(df: pd.DataFrame):
    candidates = ['Date', 'date', 'DATE', 'timestamp', 'Time', 'time']
    for c in candidates:
        if c in df.columns:
            return c
    return df.columns[0]


def detect_value_column(df: pd.DataFrame):
    preferred = ['Adj Close', 'Close', 'close', 'VALUE', 'Actual', 'Price', 'price']
    for c in preferred:
        if c in df.columns:
            return c
    numeric_scores = []
    for c in df.columns:
        converted = pd.to_numeric(df[c], errors='coerce')
        score = converted.notna().mean()
        numeric_scores.append((score, c))
    numeric_scores.sort(reverse=True)
    return numeric_scores[0][1]


def weekly_transform(df: pd.DataFrame, symbol: str, date_col: str, value_col: str):
    x = df[[date_col, value_col]].copy()
    x[date_col] = pd.to_datetime(x[date_col], errors='coerce')
    x[value_col] = pd.to_numeric(x[value_col], errors='coerce')
    x = x.dropna().sort_values(date_col)
    if x.empty:
        return pd.DataFrame(
            columns=[
                'week_end',
                'symbol',
                'raw_value',
                'growth_index',
                'weekly_return',
                'momentum_4w',
                'momentum_12w',
                'volatility_4w',
                'return_z_52',
            ]
        )

    x['week_end'] = x[date_col].dt.to_period('W-FRI').dt.end_time.dt.date
    weekly = x.groupby('week_end', as_index=False)[value_col].last().rename(columns={value_col: 'raw_value'})
    weekly['weekly_return'] = weekly['raw_value'].pct_change()
    weekly['momentum_4w'] = weekly['raw_value'].pct_change(4)
    weekly['momentum_12w'] = weekly['raw_value'].pct_change(12)
    weekly['volatility_4w'] = weekly['weekly_return'].rolling(window=4, min_periods=2).std()

    ret_mean_52 = weekly['weekly_return'].rolling(window=52, min_periods=20).mean()
    ret_std_52 = weekly['weekly_return'].rolling(window=52, min_periods=20).std()
    weekly['return_z_52'] = (weekly['weekly_return'] - ret_mean_52) / ret_std_52

    first = weekly['raw_value'].iloc[0]
    if pd.isna(first) or first == 0:
        weekly['growth_index'] = pd.NA
    else:
        weekly['growth_index'] = (weekly['raw_value'] / first) * 100.0

    weekly['symbol'] = symbol
    return weekly[
        [
            'week_end',
            'symbol',
            'raw_value',
            'growth_index',
            'weekly_return',
            'momentum_4w',
            'momentum_12w',
            'volatility_4w',
            'return_z_52',
        ]
    ]


def pivot_feature(long_df: pd.DataFrame, value_col: str, suffix: str):
    wide = long_df.pivot(index='week_end', columns='symbol', values=value_col).sort_index()
    wide.columns = [f'{c}{suffix}' for c in wide.columns]
    return wide


def main():
    parser = argparse.ArgumentParser(description='Weekly normalization for raw indicator CSV files.')
    parser.add_argument('--config', default='config.yaml')
    args = parser.parse_args()

    cfg_path = Path(args.config).resolve()
    cfg = load_simple_yaml(cfg_path)
    input_cfg = cfg.get('input', {})
    output_cfg = cfg.get('output', {})

    raw_dir = resolve_path(cfg_path.parent, input_cfg.get('raw_dir', '../data_ingestion/OUTPUT/raw'))
    include_symbols = [s.strip() for s in input_cfg.get('include_symbols', '').split(',') if s.strip()]

    weekly_long_file = resolve_path(cfg_path.parent, output_cfg.get('weekly_long_file', 'OUTPUT/weekly_normalized_long.csv'))
    weekly_levels_wide_file = resolve_path(
        cfg_path.parent, output_cfg.get('weekly_levels_wide_file', 'OUTPUT/weekly_levels_wide.csv')
    )
    weekly_growth_wide_file = resolve_path(
        cfg_path.parent, output_cfg.get('weekly_growth_wide_file', 'OUTPUT/weekly_growth_index_wide.csv')
    )
    weekly_features_wide_file = resolve_path(
        cfg_path.parent, output_cfg.get('weekly_features_wide_file', 'OUTPUT/weekly_features_wide.csv')
    )
    # Backward compatibility path. This now points to growth index wide data for visualization.
    weekly_normalized_wide_file = resolve_path(
        cfg_path.parent, output_cfg.get('weekly_normalized_wide_file', 'OUTPUT/weekly_normalized_wide.csv')
    )

    weekly_long_file.parent.mkdir(parents=True, exist_ok=True)
    weekly_levels_wide_file.parent.mkdir(parents=True, exist_ok=True)
    weekly_growth_wide_file.parent.mkdir(parents=True, exist_ok=True)
    weekly_features_wide_file.parent.mkdir(parents=True, exist_ok=True)
    weekly_normalized_wide_file.parent.mkdir(parents=True, exist_ok=True)

    frames = []
    for file in sorted(raw_dir.glob('*.csv')):
        symbol = file.stem
        if include_symbols and symbol not in include_symbols:
            continue
        try:
            df = pd.read_csv(file)
            if df.empty:
                continue
            date_col = detect_date_column(df)
            value_col = detect_value_column(df)
            weekly = weekly_transform(df, symbol, date_col, value_col)
            if not weekly.empty:
                frames.append(weekly)
        except Exception as exc:
            print(f'[WARN] {symbol}: {exc}')

    if not frames:
        print('No input data normalized.')
        raise SystemExit(1)

    long_df = pd.concat(frames, ignore_index=True).sort_values(['week_end', 'symbol'])
    long_df.to_csv(weekly_long_file, index=False)

    levels_wide = long_df.pivot(index='week_end', columns='symbol', values='raw_value').sort_index()
    growth_wide = long_df.pivot(index='week_end', columns='symbol', values='growth_index').sort_index()

    feature_wide_parts = [
        pivot_feature(long_df, 'weekly_return', '__ret_1w'),
        pivot_feature(long_df, 'momentum_4w', '__mom_4w'),
        pivot_feature(long_df, 'momentum_12w', '__mom_12w'),
        pivot_feature(long_df, 'volatility_4w', '__vol_4w'),
        pivot_feature(long_df, 'return_z_52', '__ret_z52'),
    ]
    features_wide = pd.concat(feature_wide_parts, axis=1).sort_index()

    levels_wide.to_csv(weekly_levels_wide_file)
    growth_wide.to_csv(weekly_growth_wide_file)
    features_wide.to_csv(weekly_features_wide_file)
    growth_wide.to_csv(weekly_normalized_wide_file)

    print(f'weekly_long={weekly_long_file}')
    print(f'weekly_levels_wide={weekly_levels_wide_file}')
    print(f'weekly_growth_wide={weekly_growth_wide_file}')
    print(f'weekly_features_wide={weekly_features_wide_file}')
    print(f'weekly_normalized_wide(backward_compat)={weekly_normalized_wide_file}')


if __name__ == '__main__':
    main()
