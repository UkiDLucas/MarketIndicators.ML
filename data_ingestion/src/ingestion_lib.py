import argparse
import csv
import json
import re
import shutil
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


def _parse_scalar(raw: str):
    value = raw.strip()
    if not value:
        return ""
    if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    lower = value.lower()
    if lower == 'true':
        return True
    if lower == 'false':
        return False
    return value


def load_simple_yaml(path: Path):
    data = {}
    section = None
    for line in path.read_text(encoding='utf-8').splitlines():
        raw = line.split('#', 1)[0].rstrip()
        if not raw.strip():
            continue
        if raw.lstrip() != raw:
            if section is None:
                continue
            if ':' not in raw:
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
    p = Path(str(raw_path).strip())
    if p.is_absolute():
        return p
    return (base / p).resolve()


def refresh_yahoo_period2(url: str):
    if 'query1.finance.yahoo.com' not in url:
        return url
    if 'period2=' not in url:
        return url
    now_unix = str(int(time.time()))
    return re.sub(r'period2=[^&]*', f'period2={now_unix}', url)


def fetch_indicator(config_path: Path, remote_policy: str = 'auto', timeout_seconds: float = 30.0):
    cfg = load_simple_yaml(config_path)
    source = cfg.get('source', {})
    output = cfg.get('output', {})

    symbol = str(source.get('symbol', 'UNKNOWN')).strip() or 'UNKNOWN'
    url = str(source.get('url', '')).strip()
    raw_dir = resolve_path(config_path.parent, output.get('raw_dir', '../../OUTPUT/raw'))
    metadata_dir = resolve_path(config_path.parent, output.get('metadata_dir', '../../OUTPUT/metadata'))

    output_filename = str(source.get('output_filename', '')).strip()
    if not output_filename:
        output_filename = str(source.get('original_file_name', '')).strip() or f'{symbol}.csv'

    raw_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)

    out_file = raw_dir / output_filename
    metadata_file = metadata_dir / f'{symbol}.json'

    metadata = {
        'symbol': symbol,
        'url': url,
        'requested_at_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'pending',
        'output_file': str(out_file),
        'remote_policy': remote_policy,
        'timeout_seconds': timeout_seconds,
    }

    remote_allowed = bool(source.get('remote_allowed', True))

    def copy_snapshot(reason: str):
        snapshot_path = str(source.get('snapshot_path', '')).strip()
        if snapshot_path:
            snapshot = resolve_path(config_path.parent, snapshot_path)
            if snapshot.exists() and snapshot.is_file():
                shutil.copy2(snapshot, out_file)
                metadata['source'] = 'local_snapshot'
                metadata['status'] = 'copied_snapshot'
                metadata['snapshot_file'] = str(snapshot)
                metadata['warning'] = reason
            else:
                metadata['status'] = 'failed'
                metadata['error'] = f'{reason}; snapshot_missing={snapshot}'
        else:
            metadata['status'] = 'failed'
            metadata['error'] = reason

    if remote_policy not in {'auto', 'never'}:
        metadata['status'] = 'failed'
        metadata['error'] = f'Unsupported remote_policy={remote_policy}'
        metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        return metadata

    if (remote_policy == 'never') or (not remote_allowed):
        copy_snapshot('remote_skipped_by_policy')
        metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
        return metadata

    try:
        if not url:
            raise ValueError('Missing source.url in config')

        live_url = refresh_yahoo_period2(url)
        req = urllib.request.Request(live_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=float(timeout_seconds)) as response:
            with out_file.open('wb') as fh:
                shutil.copyfileobj(response, fh)
            metadata['http_status'] = int(response.getcode())
            metadata['source'] = 'remote'
            metadata['status'] = 'downloaded'
            metadata['resolved_url'] = live_url
    except Exception as exc:
        copy_snapshot(f'remote_fetch_failed: {type(exc).__name__}: {exc}')

    metadata_file.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return metadata


def load_indicator_rows(indicators_csv: Path):
    with indicators_csv.open(newline='', encoding='utf-8') as fh:
        return list(csv.DictReader(fh))
