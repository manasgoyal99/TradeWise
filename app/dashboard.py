
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import yfinance as yf


# ---------- Project paths ----------
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data" / "processed"
RELIANCE_FILE = DATA_DIR / "reliance_analysis.csv"


# ---------- Stock options ----------
stock_options = {
    "Reliance Industries": "RELIANCE.NS",
    "Tata Consultancy Services": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
}


# ---------- Dashboard settings ----------
st.set_page_config(
    page_title="TradeWise | Stock Dashboard",
    page_icon="📈",
    layout="wide",
)

st.title("📈 TradeWise - Stock Analysis Dashboard")
st.caption("NSE stock market analysis and visualization")


# ---------- Sidebar ----------
st.sidebar.header("Dashboard Filters")

stock_name = st.sidebar.selectbox(
    "Select Stock",
    list(stock_options.keys()),
)

stock_symbol = stock_options[stock_name]

period = st.sidebar.selectbox(
    "Historical Data Period",
    ["6mo", "1y", "2y", "5y"],
    index=2,
)


# ---------- Load stock data ----------
@st.cache_data(ttl=900)
def load_stock_data(symbol, selected_period):
    data = yf.download(
        symbol,
        period=selected_period,
        interval="1d",
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        return pd.DataFrame()

    # Handle yfinance column formats
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.reset_index()

    if "Date" not in data.columns and "Datetime" in data.columns:
        data = data.rename(columns={"Datetime": "Date"})

    required_columns = ["Date", "Close"]

    if not all(col in data.columns for col in required_columns):
        return pd.DataFrame()

    data["Date"] = pd.to_datetime(data["Date"])
    data["Daily_Return"] = data["Close"].pct_change() * 100
    data["MA_20"] = data["Close"].rolling(window=20).mean()
    data["MA_50"] = data["Close"].rolling(window=50).mean()
    data["Volatility_20"] = (
        data["Daily_Return"].rolling(window=20).std()
    )

    return data


with st.spinner(f"Loading {stock_name} stock data..."):
    try:
        df = load_stock_data(stock_symbol, period)
    except Exception as error:
        st.error(f"Unable to load stock data: {error}")
        st.stop()


if df.empty:
    st.error(
        "Stock data could not be loaded. "
        "Please check your internet connection or try again later."
    )
    st.stop()


st.subheader(f"Selected Stock: {stock_name}")
st.caption(f"NSE Symbol: {stock_symbol}")


# ---------- Date filter ----------
min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start_date, end_date = selected_dates

    filtered_df = df[
        (df["Date"].dt.date >= start_date)
        & (df["Date"].dt.date <= end_date)
    ].copy()
else:
    filtered_df = df.copy()


if filtered_df.empty:
    st.warning("No data available for this date range.")
    st.stop()


# ---------- Key metrics ----------
latest = filtered_df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Latest Closing Price",
    f"₹{latest['Close']:,.2f}",
)

col2.metric(
    "20-Day Moving Average",
    f"₹{latest['MA_20']:,.2f}",
)

col3.metric(
    "50-Day Moving Average",
    f"₹{latest['MA_50']:,.2f}",
)

daily_return = latest["Daily_Return"]

col4.metric(
    "Latest Daily Return",
    f"{daily_return:.2f}%" if pd.notna(daily_return) else "N/A",
)


# ---------- Closing price chart ----------
st.subheader("Stock Closing Price")

price_fig = go.Figure()

price_fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Close"],
        mode="lines",
        name="Closing Price",
    )
)

price_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price (₹)",
    hovermode="x unified",
)

st.plotly_chart(price_fig, width="stretch")


# ---------- Moving averages ----------
st.subheader("Moving Averages")

ma_fig = go.Figure()

for column, label in [
    ("Close", "Closing Price"),
    ("MA_20", "20-Day MA"),
    ("MA_50", "50-Day MA"),
]:
    ma_fig.add_trace(
        go.Scatter(
            x=filtered_df["Date"],
            y=filtered_df[column],
            mode="lines",
            name=label,
        )
    )

ma_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Price (₹)",
    hovermode="x unified",
)

st.plotly_chart(ma_fig, width="stretch")


# ---------- Daily returns ----------
st.subheader("Daily Returns (%)")

returns_fig = go.Figure()

returns_fig.add_trace(
    go.Bar(
        x=filtered_df["Date"],
        y=filtered_df["Daily_Return"],
        name="Daily Return",
    )
)

returns_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Return (%)",
    hovermode="x unified",
)

st.plotly_chart(returns_fig, width="stretch")


# ---------- Volatility ----------
st.subheader("20-Day Rolling Volatility")

volatility_fig = go.Figure()

volatility_fig.add_trace(
    go.Scatter(
        x=filtered_df["Date"],
        y=filtered_df["Volatility_20"],
        mode="lines",
        name="20-Day Volatility",
    )
)

volatility_fig.update_layout(
    xaxis_title="Date",
    yaxis_title="Standard Deviation (%)",
    hovermode="x unified",
)

st.plotly_chart(volatility_fig, width="stretch")


# ---------- Stock data table ----------
with st.expander("View Stock Data"):
    st.dataframe(
        filtered_df.sort_values("Date", ascending=False),
        width="stretch",
    )


# ---------- Download analysis ----------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Stock Analysis CSV",
    data=csv_data,
    file_name=f"{stock_symbol.replace('.', '_')}_analysis.csv",
    mime="text/csv",
)


st.caption(
    "Data is retrieved from Yahoo Finance. "
    "For educational analysis only; not financial advice."
)
