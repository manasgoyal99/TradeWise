
import pandas as pd

from src.stock_analysis import calculate_stock_indicators


# ---------- Test 1: Daily Return ----------
def test_daily_return():
    df = pd.DataFrame({
        "Close": [100, 110, 121]
    })

    result = calculate_stock_indicators(df)

    assert pd.isna(result["Daily_Return"].iloc[0])
    assert round(result["Daily_Return"].iloc[1], 2) == 10.00
    assert round(result["Daily_Return"].iloc[2], 2) == 10.00


# ---------- Test 2: 20-Day Moving Average ----------
def test_ma_20():
    df = pd.DataFrame({
        "Close": list(range(1, 21))
    })

    result = calculate_stock_indicators(df)

    assert pd.isna(result["MA_20"].iloc[18])
    assert result["MA_20"].iloc[19] == 10.5


# ---------- Test 3: 50-Day Moving Average ----------
def test_ma_50():
    df = pd.DataFrame({
        "Close": list(range(1, 51))
    })

    result = calculate_stock_indicators(df)

    assert pd.isna(result["MA_50"].iloc[48])
    assert result["MA_50"].iloc[49] == 25.5


# ---------- Test 4: Volatility ----------
def test_volatility_20():
    df = pd.DataFrame({
        "Close": [100.0 * (1.01 ** i) for i in range(21)]
    })

    result = calculate_stock_indicators(df)

    assert pd.isna(result["Volatility_20"].iloc[19])
    assert result["Volatility_20"].iloc[20] < 1e-10


# ---------- Test 5: Missing price handling ----------
def test_missing_price():
    df = pd.DataFrame({
        "Close": [100.0, float("nan"), 120.0]
    })

    result = calculate_stock_indicators(df)

    assert pd.isna(result["Daily_Return"].iloc[1])
    assert pd.isna(result["Daily_Return"].iloc[2])
