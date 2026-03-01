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
            features = tdp / 'features.csv'
            levels = tdp / 'levels.csv'
            weeks = pd.date_range('2024-01-05', periods=80, freq='W-FRI')
            feat_data = pd.DataFrame({
                'week_end': weeks.date,
                'AAPL__ret_1w': np.sin(np.linspace(0, 8, 80)),
                'TSLA__ret_1w': np.cos(np.linspace(0, 8, 80)),
                'QQQ__mom_4w': np.sin(np.linspace(0, 4, 80)),
                'VTI__vol_4w': np.linspace(0.01, 0.04, 80),
            })
            lvl_data = pd.DataFrame(
                {
                    'week_end': weeks.date,
                    'AAPL': 100 * np.cumprod(1 + 0.002 + 0.01 * np.sin(np.linspace(0, 8, 80))),
                    'TSLA': 200 * np.cumprod(1 + 0.003 + 0.015 * np.cos(np.linspace(0, 8, 80))),
                }
            )
            feat_data.to_csv(features, index=False)
            lvl_data.to_csv(levels, index=False)

            cfg = tdp / 'config.yaml'
            cfg.write_text(
                "input:\n"
                f"  features_wide_file: \"{features}\"\n"
                f"  levels_wide_file: \"{levels}\"\n"
                "output:\n"
                f"  model_dir: \"{tdp / 'models'}\"\n"
                f"  metrics_file: \"{tdp / 'metrics.csv'}\"\n"
                f"  predictions_dir: \"{tdp / 'preds'}\"\n"
                "model:\n"
                "  alpha: \"1.0\"\n"
                "  test_fraction: \"0.2\"\n"
                "targets:\n"
                "  symbols: \"AAPL,TSLA\"\n",
                encoding='utf-8',
            )

            script = Path(__file__).resolve().parents[1] / 'src/train_regression.py'
            subprocess.run(['python3', str(script), '--config', str(cfg)], check=True)
            self.assertTrue((tdp / 'metrics.csv').exists())


if __name__ == '__main__':
    unittest.main()
