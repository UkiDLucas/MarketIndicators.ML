#!/usr/bin/env python3
from pathlib import Path
import subprocess


def main():
    here = Path(__file__).resolve().parent.parent
    script = here.parent.parent / 'src' / 'run_ingestion.py'
    cfg = here / 'config.yaml'
    subprocess.run(['python3', str(script), '--config', str(cfg)], check=True)


if __name__ == '__main__':
    main()
