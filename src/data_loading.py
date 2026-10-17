
# ============================================================
# TradeWise - Stock Market Data Loading and Cleaning
# Purpose: NSE stock data download, inspect, clean and save
# ============================================================

# Step 1: Import required libraries
import yfinance as yf
import pandas as pd
from pathlib import Path


# Step 2: Set project folder paths
# __file__ = current Python file
# parent.parent = src folder se ek level upar, TradeWise folder

PROJECT_DIR = Path(__file__).resolve().parent.parent

# Raw data folder ka path
DATA_DIR = PROJECT_DIR / "data" / "raw"

# Processed data folder ka path
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"

# Agar folders nahi hain, toh create kar do
DATA_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# Step 3: Select NSE stock
# .NS = Yahoo Finance par NSE-listed stock ka suffix

ticker = "RELIANCE.NS"


# Step 4: Download historical stock data
# period="2y" = pichhle 2 saal ka data
# interval="1d" = daily data

stock = yf.Ticker(ticker)
data = stock.history(period="2y", interval="1d")


# Step 5: Check and save raw data

if data.empty:
    print("Stock data download nahi hua. Internet ya ticker check karo.")

else:
    # Downloaded data ko raw CSV file mein save karo
    raw_file = DATA_DIR / "reliance_stock_data.csv"
    data.to_csv(raw_file)

    print("Stock data successfully downloaded!")
    print(data.head())
    print(f"Total rows: {len(data)}")


    # Step 6: Read CSV using Pandas
    # Date index ko normal column banane ke liye reset_index()
    df = pd.read_csv(raw_file, index_col=0)
    df.index.name = "Date"
    df = df.reset_index()

    # Dataset ka basic overview
    print("\nDataset shape:", df.shape)
    print("\nColumn names:")
    print(df.columns)
    print("\nMissing values by column:")
    print(df.isnull().sum())

    # Duplicate aur total missing values check karo
    print("\nDuplicate rows:", df.duplicated().sum())
    print("Total missing values:", df.isnull().sum().sum())


    # Step 7: Convert Date column to datetime format

    df["Date"] = pd.to_datetime(df["Date"])

    print("\nDate data type:", df["Date"].dtype)
    print("Missing dates:", df["Date"].isnull().sum())
    print("Date range:", df["Date"].min(), "to", df["Date"].max())


    # Step 8: Clean the dataset

    # Exact duplicate rows remove karo
    df = df.drop_duplicates()

    # Important columns mein missing values wali rows remove karo
    df = df.dropna(
        subset=["Date", "Open", "High", "Low", "Close", "Volume"]
    )

    # Dates ko ascending order mein arrange karo
    df = df.sort_values("Date")

    # Index ko dobara 0 se start karo
    df = df.reset_index(drop=True)

    # Cleaning ke baad result check karo
    print("\nRows after cleaning:", len(df))
    print("Missing values after cleaning:", df.isnull().sum().sum())
    print("Dates sorted:", df["Date"].is_monotonic_increasing)


    # Step 9: Save cleaned data in processed folder

    processed_file = PROCESSED_DIR / "reliance_cleaned.csv"

    # index=False se extra index column save nahi hoga
    df.to_csv(processed_file, index=False)

    print("\nCleaned file saved:", processed_file.exists())
    print("Saved location:", processed_file)
