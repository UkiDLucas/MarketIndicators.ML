import tempfile
import unittest
from pathlib import Path
import subprocess
import pandas as pd
import numpy as np


class TestRegressionPipeline(unittest.TestCase):
    def test_train_regression_runs(self):
        with tempfile.TemporaryDirectory() as td:
            tdp = Path(td)
            wide = tdp / 'wide.csv'
            weeks = pd.date_range('2024-01-05', periods=80, freq='W-FRI')
            data = pd.DataFrame({
                'week_end': weeks.date,
                'AAPL': np.linspace(-1, 1, 80),
                'TSLA': np.linspace(1, -1, 80),
                'QQQ': np.sin(np.linspace(0, 8, 80)),
                'DIA': np.cos(np.linspace(0, 8, 80)),
                'VTI': np.linspace(-0.5, 0.5, 80),
            })
            data.to_csv(wide, index=False)

            cfg = tdp / 'config.yaml'
            cfg.write_text(
                'input:
'
                f'  normalized_wide_file: "{wide}"
'
                'output:
'
                f'  model_dir: "{tdp / "models"}"
'
                f'  metrics_file: "{tdp / "metrics.csv"}"
'
                f'  predictions_dir: "{tdp / "preds"}"
'
                'model:
'
                '  alpha: "1.0"
'
                '  test_fraction: "0.2"
'
                'targets:
'
                '  symbols: "AAPL,TSLA"
',
                encoding='utf-8',
            )

            script = Path(__file__).resolve().parents[1] / 'src/train_regression.py'
            subprocess.run(['python3', str(script), '--config', str(cfg)], check=True)
            self.assertTrue((tdp / 'metrics.csv').exists())


if __name__ == '__main__':
    unittest.main()
