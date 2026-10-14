import os
import tempfile

import pandas as pd

from working_example_yfinance import stocks


def test_download_and_save_stocks():
    with tempfile.TemporaryDirectory() as temp_dir:
        output_file = stocks.download_and_save_stocks(volume_path=temp_dir, tickers=["AAPL"])
        assert os.path.exists(output_file)
        assert "stocks_data_" in os.path.basename(output_file)
        assert os.path.getsize(output_file) > 0
        df = pd.read_csv(output_file)
        assert "timestamp" in df.columns
        assert not df["timestamp"].empty
