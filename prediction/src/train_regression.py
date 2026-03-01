#!/usr/bin/env python3
import argparse
import math
import pickle
from pathlib import Path

import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


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


def safe_float(text: str, default: float):
    try:
        return float(text)
    except Exception:
        return default


def train_one(
    features_df: pd.DataFrame,
    levels_df: pd.DataFrame,
    target: str,
    alpha: float,
    test_fraction: float,
):
    if target not in levels_df.columns:
        return None, None, {'target': target, 'status': 'missing_target_series'}

    # Target = next-week return. This is a stationary target and avoids direct scale drift.
    target_return = levels_df[target].pct_change().shift(-1).rename('target_next_return')
    current_level = levels_df[target].rename('current_level')

    merged = pd.concat([features_df, target_return, current_level], axis=1)
    merged = merged.dropna()
    if len(merged) < 52:
        return None, None, {'target': target, 'status': 'insufficient_data'}

    feature_cols = list(features_df.columns)
    X = merged[feature_cols]
    y = merged['target_next_return']
    lvl = merged['current_level']

    split = max(int(len(merged) * (1.0 - test_fraction)), 1)
    if split >= len(merged):
        split = len(merged) - 1

    X_train, X_test = X.iloc[:split], X.iloc[split:]
    y_train, y_test = y.iloc[:split], y.iloc[split:]
    lvl_test = lvl.iloc[split:]

    model = make_pipeline(StandardScaler(), Ridge(alpha=alpha))
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    rmse = math.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    pred_df = pd.DataFrame(
        {
            'week_end': X_test.index,
            'current_level': lvl_test.values,
            'y_actual_return': y_test.values,
            'y_pred_return': y_pred,
        }
    )
    pred_df['implied_actual_next_level'] = pred_df['current_level'] * (1.0 + pred_df['y_actual_return'])
    pred_df['implied_pred_next_level'] = pred_df['current_level'] * (1.0 + pred_df['y_pred_return'])

    metrics = {
        'target': target,
        'status': 'trained',
        'rows_total': len(merged),
        'rows_train': len(X_train),
        'rows_test': len(X_test),
        'feature_count': len(feature_cols),
        'alpha': alpha,
        'rmse_return': rmse,
        'mae_return': mae,
        'r2_return': r2,
    }

    payload = {
        'model': model,
        'feature_cols': feature_cols,
        'target': target,
    }
    return payload, pred_df, metrics


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

    features_wide_file = resolve_path(
        cfg_path.parent, in_cfg.get('features_wide_file', '../data_normalization/OUTPUT/weekly_features_wide.csv')
    )
    levels_wide_file = resolve_path(
        cfg_path.parent, in_cfg.get('levels_wide_file', '../data_normalization/OUTPUT/weekly_levels_wide.csv')
    )
    model_dir = resolve_path(cfg_path.parent, out_cfg.get('model_dir', 'OUTPUT/models'))
    metrics_file = resolve_path(cfg_path.parent, out_cfg.get('metrics_file', 'OUTPUT/metrics.csv'))
    predictions_dir = resolve_path(cfg_path.parent, out_cfg.get('predictions_dir', 'OUTPUT/predictions'))

    alpha = safe_float(model_cfg.get('alpha', '1.0'), 1.0)
    test_fraction = safe_float(model_cfg.get('test_fraction', '0.2'), 0.2)
    targets = [t.strip() for t in target_cfg.get('symbols', '').split(',') if t.strip()]

    model_dir.mkdir(parents=True, exist_ok=True)
    predictions_dir.mkdir(parents=True, exist_ok=True)
    metrics_file.parent.mkdir(parents=True, exist_ok=True)

    if not features_wide_file.exists():
        raise SystemExit(f'Features dataset missing: {features_wide_file}')
    if not levels_wide_file.exists():
        raise SystemExit(f'Levels dataset missing: {levels_wide_file}')

    features_df = pd.read_csv(features_wide_file)
    levels_df = pd.read_csv(levels_wide_file)

    if 'week_end' not in features_df.columns or 'week_end' not in levels_df.columns:
        raise SystemExit('Expected week_end column in both features and levels datasets')

    features_df['week_end'] = pd.to_datetime(features_df['week_end'], errors='coerce')
    levels_df['week_end'] = pd.to_datetime(levels_df['week_end'], errors='coerce')

    features_df = features_df.dropna(subset=['week_end']).sort_values('week_end').set_index('week_end')
    levels_df = levels_df.dropna(subset=['week_end']).sort_values('week_end').set_index('week_end')

    for col in features_df.columns:
        features_df[col] = pd.to_numeric(features_df[col], errors='coerce')
    for col in levels_df.columns:
        levels_df[col] = pd.to_numeric(levels_df[col], errors='coerce')

    # Keep rows where at least one feature exists; per-target training does final dropna.
    features_df = features_df.dropna(how='all')
    levels_df = levels_df.dropna(how='all')

    all_metrics = []
    for target in targets:
        model_payload, pred_df, metrics = train_one(features_df, levels_df, target, alpha, test_fraction)
        if metrics['status'] != 'trained':
            all_metrics.append(metrics)
            continue

        model_path = model_dir / f'{target}.pkl'
        with model_path.open('wb') as fh:
            pickle.dump(model_payload, fh)

        pred_path = predictions_dir / f'{target}_predictions.csv'
        pred_df.to_csv(pred_path, index=False)

        metrics['model_path'] = str(model_path)
        metrics['predictions_path'] = str(pred_path)
        all_metrics.append(metrics)

    pd.DataFrame(all_metrics).to_csv(metrics_file, index=False)
    print(f'metrics={metrics_file}')


if __name__ == '__main__':
    main()
