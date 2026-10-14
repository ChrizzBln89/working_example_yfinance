import argparse

from databricks.sdk.runtime import spark

from working_example_yfinance import stocks


def main():
    # Process command-line arguments
    parser = argparse.ArgumentParser(
        description="Download yfinance stock data and save to Databricks Volume",
    )
    parser.add_argument("--catalog", required=True)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--volume", required=True, help="Volume path or name")
    args = parser.parse_args()

    # Set the default catalog and schema
    spark.sql(f"USE CATALOG `{args.catalog}`")
    spark.sql(f"USE SCHEMA `{args.schema}`")

    # Determine volume path
    volume_path = args.volume
    if not volume_path.startswith("/Volumes/"):
        volume_path = f"/Volumes/{args.catalog}/{args.schema}/{args.volume}"

    # Download stocks and save to volume
    stocks.download_and_save_stocks(volume_path=volume_path)


if __name__ == "__main__":
    main()
