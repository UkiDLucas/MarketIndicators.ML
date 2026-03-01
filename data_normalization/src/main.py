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
        raw = line.split('#', 1)[0].rstrip('
')
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


def weekly_normalize(df: pd.DataFrame, symbol: str, date_col: str, value_col: str):
    x = df[[date_col, value_col]].copy()
    x[date_col] = pd.to_datetime(x[date_col], errors='coerce')
    x[value_col] = pd.to_numeric(x[value_col], errors='coerce')
    x = x.dropna().sort_values(date_col)
    if x.empty:
        return pd.DataFrame(columns=['week_end', 'symbol', 'raw_value', 'weekly_return', 'z_score'])

    x['week_end'] = x[date_col].dt.to_period('W-FRI').dt.end_time.dt.date
    weekly = x.groupby('week_end', as_index=False)[value_col].last().rename(columns={value_col: 'raw_value'})
    weekly['weekly_return'] = weekly['raw_value'].pct_change()

    mean = weekly['weekly_return'].mean(skipna=True)
    std = weekly['weekly_return'].std(skipna=True)
    if pd.isna(std) or std == 0:
        weekly['z_score'] = 0.0
    else:
        weekly['z_score'] = (weekly['weekly_return'] - mean) / std

    weekly['symbol'] = symbol
    return weekly[['week_end', 'symbol', 'raw_value', 'weekly_return', 'z_score']]


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
    weekly_wide_file = resolve_path(cfg_path.parent, output_cfg.get('weekly_wide_file', 'OUTPUT/weekly_normalized_wide.csv'))

    weekly_long_file.parent.mkdir(parents=True, exist_ok=True)
    weekly_wide_file.parent.mkdir(parents=True, exist_ok=True)

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
            weekly = weekly_normalize(df, symbol, date_col, value_col)
            if not weekly.empty:
                frames.append(weekly)
        except Exception as exc:
            print(f'[WARN] {symbol}: {exc}')

    if not frames:
        print('No input data normalized.')
        raise SystemExit(1)

    long_df = pd.concat(frames, ignore_index=True).sort_values(['week_end', 'symbol'])
    long_df.to_csv(weekly_long_file, index=False)

    wide_df = long_df.pivot(index='week_end', columns='symbol', values='z_score').sort_index()
    wide_df.to_csv(weekly_wide_file)

    print(f'weekly_long={weekly_long_file}')
    print(f'weekly_wide={weekly_wide_file}')


if __name__ == '__main__':
    main()
