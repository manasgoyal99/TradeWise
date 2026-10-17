
# ---------- Imports ----------
from pathlib import Path
import pandas as pd


# ---------- Project paths ----------
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "reliance_cleaned.csv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "reliance_analysis.csv"


# ---------- Calculate Stock Indicators ----------
def calculate_stock_indicators(df):
    """Calculate stock returns, moving averages and volatility."""

    df = df.copy()

    df["Daily_Return"] = df["Close"].pct_change(fill_method=None) * 100

    df["MA_20"] = df["Close"].rolling(window=20).mean()

    df["MA_50"] = df["Close"].rolling(window=50).mean()

    df["Volatility_20"] = (
        df["Daily_Return"].rolling(window=20).std()
    )

    return df


# ---------- Generate Stock Analysis ----------
def main():
    if not DATA_FILE.exists():
        print(f"ERROR: Data file not found: {DATA_FILE}")
        return

    # Read cleaned stock data
    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    print("\n========== TRADEWISE STOCK ANALYSIS ==========\n")
    print(df.head())

    # Calculate indicators using the project function
    df = calculate_stock_indicators(df)

    print("\nDaily Returns:")
    print(df[["Date", "Close", "Daily_Return"]].head(10))

    print("\nMoving Averages:")
    print(df[["Date", "Close", "MA_20", "MA_50"]].tail(10))

    # Stock analysis summary
    print("\n========== ANALYSIS SUMMARY ==========")
    print("Latest Closing Price:", df["Close"].iloc[-1])
    print("Average Daily Return:", df["Daily_Return"].mean())
    print("Highest Closing Price:", df["Close"].max())
    print("Lowest Closing Price:", df["Close"].min())
    print("Latest 20-Day MA:", df["MA_20"].iloc[-1])
    print("Latest 50-Day MA:", df["MA_50"].iloc[-1])
    print("Latest 20-Day Volatility:", df["Volatility_20"].iloc[-1])
    print("Maximum Daily Return (%):", df["Daily_Return"].max())
    print("Minimum Daily Return (%):", df["Daily_Return"].min())

    # Save analysis output
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print("\nAnalysis file saved:", OUTPUT_FILE)

    # Verify saved file
    saved_df = pd.read_csv(OUTPUT_FILE)

    print("Analysis rows:", len(saved_df))
    print("Analysis columns:", saved_df.columns.tolist())
    print("Missing values:", saved_df.isnull().sum().sum())
    print("File exists:", OUTPUT_FILE.exists())


# ---------- Run the program ----------
if __name__ == "__main__":
    main()
