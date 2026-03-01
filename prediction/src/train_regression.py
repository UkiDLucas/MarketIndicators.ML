#!/usr/bin/env python3
import argparse
import csv
import math
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


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


def safe_float(text: str, default: float):
    try:
        return float(text)
    except Exception:
        return default


def train_one(df: pd.DataFrame, target: str, alpha: float, test_fraction: float):
    feature_cols = [c for c in df.columns if c != target]
    working = df[feature_cols + [target]].copy()
    working['target_next'] = working[target].shift(-1)
    working = working.dropna()

    if len(working) < 24 or len(feature_cols) < 1:
        return None, None, 'insufficient_data'

    X = working[feature_cols].to_numpy(dtype=float)
    y = working['target_next'].to_numpy(dtype=float)

    split = max(int(len(working) * (1.0 - test_fraction)), 1)
    if split >= len(working):
        split = len(working) - 1

    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = Ridge(alpha=alpha)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    rmse = math.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    pred_df = pd.DataFrame({
        'y_actual': y_test,
        'y_predicted': y_pred,
    })

    metrics = {
        'target': target,
        'status': 'trained',
        'rows_total': len(working),
        'rows_train': len(X_train),
        'rows_test': len(X_test),
        'feature_count': len(feature_cols),
        'alpha': alpha,
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
    }

    return model, (feature_cols, pred_df), metrics


def main():
    parser = argparse.ArgumentParser(description='Train weekly ridge regression models per target symbol.')
    parser.add_argument('--config', default='config.yaml')
    args = parser.parse_args()

    cfg_path = Path(args.config).resolve()
    cfg = load_simple_yaml(cfg_path)

    in_cfg = cfg.get('input', {})
    out_cfg = cfg.get('output', {})
    model_cfg = cfg.get('model', {})
    target_cfg = cfg.get('targets', {})

    wide_file = resolve_path(cfg_path.parent, in_cfg.get('normalized_wide_file', '../data_normalization/OUTPUT/weekly_normalized_wide.csv'))
    model_dir = resolve_path(cfg_path.parent, out_cfg.get('model_dir', 'OUTPUT/models'))
    metrics_file = resolve_path(cfg_path.parent, out_cfg.get('metrics_file', 'OUTPUT/metrics.csv'))
    predictions_dir = resolve_path(cfg_path.parent, out_cfg.get('predictions_dir', 'OUTPUT/predictions'))

    alpha = safe_float(model_cfg.get('alpha', '1.0'), 1.0)
    test_fraction = safe_float(model_cfg.get('test_fraction', '0.2'), 0.2)
    targets = [t.strip() for t in target_cfg.get('symbols', '').split(',') if t.strip()]

    model_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)
    metrics_file.parent.mkdir(parents=True, exist_ok=True)

    if not wide_file.exists():
        raise SystemExit(f'Normalized dataset missing: {wide_file}')

    df = pd.read_csv(wide_file)
    if 'week_end' in df.columns:
        df = df.sort_values('week_end').set_index('week_end')

    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(how='all')

    all_metrics = []
    for target in targets:
        if target not in df.columns:
            all_metrics.append({'target': target, 'status': 'missing_target_series'})
            continue

        model, payload, metrics = train_one(df, target, alpha, test_fraction)
        if model is None:
            all_metrics.append({'target': target, 'status': 'insufficient_data'})
            continue

        feature_cols, pred_df = payload
        model_path = model_dir / f'{target}.pkl'
        with model_path.open('wb') as fh:
            pickle.dump({'model': model, 'feature_cols': feature_cols, 'target': target}, fh)

        pred_path = predictions_dir / f'{target}_predictions.csv'
        pred_df.to_csv(pred_path, index=False)

        metrics['model_path'] = str(model_path)
        metrics['predictions_path'] = str(pred_path)
        all_metrics.append(metrics)

    pd.DataFrame(all_metrics).to_csv(metrics_file, index=False)
    print(f'metrics={metrics_file}')


if __name__ == '__main__':
    main()
