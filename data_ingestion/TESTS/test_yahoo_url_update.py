import unittest
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / 'src'))
from ingestion_lib import refresh_yahoo_period2


class TestYahooRefresh(unittest.TestCase):
    def test_replaces_period2(self):
        url = 'https://query1.finance.yahoo.com/v7/finance/download/AAPL?period1=1&period2=2&interval=1d&events=history'
        new_url = refresh_yahoo_period2(url)
        self.assertIn('period1=1', new_url)
        self.assertIn('period2=', new_url)
        self.assertNotIn('period2=2', new_url)


if __name__ == '__main__':
    unittest.main()
