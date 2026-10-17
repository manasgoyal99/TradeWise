
from pathlib import Path
import pandas as pd


# ---------- Project paths ----------
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "data" / "processed" / "reliance_cleaned.csv"


# ---------- Data validation function ----------
def validate_stock_data(file_path):
    print("\n========== TRADEWISE DATA VALIDATION ==========\n")

    # Check whether the file exists
    if not file_path.exists():
        print("ERROR: Stock data file not found!")
        print(f"Expected location: {file_path}")
        return False

    # Load the dataset
    df = pd.read_csv(file_path)

    print("1. FILE CHECK")
    print("File found successfully.")

    # Check number of rows and columns
    print("\n2. DATASET SIZE")
    print(f"Total rows: {df.shape[0]}")
    print(f"Total columns: {df.shape[1]}")

    # Check required columns
    print("\n3. REQUIRED COLUMNS")
    required_columns = ["Date", "Open", "High", "Low", "Close", "Volume"]

    missing_columns = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        print(f"Missing columns: {missing_columns}")
        return False

    print("All required columns are present.")

    # Check missing values
    print("\n4. MISSING VALUES")
    missing_values = df.isnull().sum()
    print(missing_values)

    total_missing = int(missing_values.sum())
    print(f"Total missing values: {total_missing}")

    # Check duplicate rows
    print("\n5. DUPLICATE ROWS")
    duplicate_rows = int(df.duplicated().sum())
    print(f"Duplicate rows: {duplicate_rows}")

    # Check duplicate dates
    print("\n6. DUPLICATE DATES")
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    invalid_dates = int(df["Date"].isna().sum())
    duplicate_dates = int(df["Date"].duplicated().sum())

    print(f"Invalid dates: {invalid_dates}")
    print(f"Duplicate dates: {duplicate_dates}")

    # Check invalid numeric values
    print("\n7. PRICE VALIDATION")
    price_columns = ["Open", "High", "Low", "Close"]

    for column in price_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    invalid_prices = int(
        (df[price_columns].isna() | (df[price_columns] <= 0)).sum().sum()
    )

    print(f"Invalid or missing price values: {invalid_prices}")

    # Check logical price relationships
    invalid_price_rows = int(
        (
            (df["High"] < df["Low"])
            | (df["High"] < df[["Open", "Close"]].max(axis=1))
            | (df["Low"] > df[["Open", "Close"]].min(axis=1))
        ).fillna(False).sum()
    )

    print(f"Rows with inconsistent price ranges: {invalid_price_rows}")

    # Check volume
    print("\n8. VOLUME VALIDATION")
    df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce")

    invalid_volume = int(
        (df["Volume"].isna() | (df["Volume"] < 0)).sum()
    )

    print(f"Invalid or missing volume values: {invalid_volume}")

    # Final validation summary
    print("\n========== VALIDATION SUMMARY ==========")

    checks_passed = (
        total_missing == 0
        and duplicate_rows == 0
        and invalid_dates == 0
        and duplicate_dates == 0
        and invalid_prices == 0
        and invalid_price_rows == 0
        and invalid_volume == 0
    )

    if checks_passed:
        print("RESULT: PASS")
        print("Stock dataset passed all validation checks.")
    else:
        print("RESULT: CHECK REQUIRED")
        print("Please review the issues reported above.")

    return checks_passed


# ---------- Run validation ----------
if __name__ == "__main__":
    validate_stock_data(DATA_FILE)
