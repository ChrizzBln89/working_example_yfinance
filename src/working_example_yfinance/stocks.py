import os
from datetime import UTC, datetime

import pandas as pd
import yfinance as yf
from databricks.sdk.runtime import spark


def download_and_save_stocks(volume_path: str, tickers=None) -> str:
    """Download 3 stocks from yfinance, add timestamp, and save as CSV with timestamp in filename to the Databricks volume."""
    if tickers is None:
        tickers = ["AAPL", "MSFT", "GOOG"]
    print(f"Downloading data for tickers: {tickers}")
    dfs = []
    for ticker in tickers:
        df = yf.download(ticker, period="5d", progress=False)
        if not df.empty:
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df["Ticker"] = ticker
            dfs.append(df.reset_index())

    if not dfs:
        raise ValueError("No stock data downloaded.")

    combined_df = pd.concat(dfs, ignore_index=True)

    # Add timestamp column and filename timestamp
    now = datetime.now(UTC)
    timestamp_str = now.strftime("%Y%m%d_%H%M%S")
    combined_df["timestamp"] = now.isoformat()

    # Ensure volume path exists
    os.makedirs(volume_path, exist_ok=True)

    output_file = os.path.join(volume_path, f"stocks_data_{timestamp_str}.csv")
    combined_df.to_csv(output_file, index=False)
    print(f"Successfully saved stock data to {output_file}")

    # Optional: show data via Spark if spark session is available
    try:
        spark_df = spark.createDataFrame(combined_df)
        spark_df.show(5)
    except Exception as e:  # noqa: BLE001
        print(f"Spark display note: {e}")

    return output_file
