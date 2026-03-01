import tempfile
import unittest
from pathlib import Path
import subprocess
import pandas as pd


class TestWeeklyNormalization(unittest.TestCase):
    def test_runs_on_sample_data(self):
        with tempfile.TemporaryDirectory() as td:
            td_path = Path(td)
            raw_dir = td_path / 'raw'
            out_dir = td_path / 'out'
            raw_dir.mkdir(parents=True)
            out_dir.mkdir(parents=True)

            sample = pd.DataFrame({
                'Date': ['2026-01-01', '2026-01-02', '2026-01-08', '2026-01-09'],
                'Close': [100.0, 101.0, 102.0, 103.0],
            })
            sample.to_csv(raw_dir / 'AAPL.csv', index=False)

            cfg = td_path / 'config.yaml'
            cfg.write_text(
                "input:\n"
                f"  raw_dir: \"{raw_dir}\"\n"
                "output:\n"
                f"  weekly_long_file: \"{out_dir / 'long.csv'}\"\n"
                f"  weekly_levels_wide_file: \"{out_dir / 'levels.csv'}\"\n"
                f"  weekly_growth_wide_file: \"{out_dir / 'growth.csv'}\"\n"
                f"  weekly_features_wide_file: \"{out_dir / 'features.csv'}\"\n"
                f"  weekly_normalized_wide_file: \"{out_dir / 'normalized.csv'}\"\n",
                encoding='utf-8',
            )

            script = Path(__file__).resolve().parents[1] / 'src/main.py'
            subprocess.run(['python3', str(script), '--config', str(cfg)], check=True)

            self.assertTrue((out_dir / 'long.csv').exists())
            self.assertTrue((out_dir / 'levels.csv').exists())
            self.assertTrue((out_dir / 'growth.csv').exists())
            self.assertTrue((out_dir / 'features.csv').exists())
            self.assertTrue((out_dir / 'normalized.csv').exists())


if __name__ == '__main__':
    unittest.main()
