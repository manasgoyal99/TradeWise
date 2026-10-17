
# TradeWise - Stock Analysis Dashboard

TradeWise is a Python-based stock market analysis project that
analyzes historical NSE stock data and presents insights through
an interactive Streamlit dashboard.

## Project Objectives

- Download historical stock market data.
- Clean and validate stock data.
- Calculate daily returns.
- Calculate 20-day and 50-day moving averages.
- Calculate 20-day rolling volatility.
- Visualize stock trends using interactive charts.
- Export analyzed data as a CSV file.
- Test analysis calculations using pytest.

## Technologies Used

- Python
- Pandas
- NumPy
- yfinance
- Streamlit
- Plotly
- Pytest

## Project Structure

```text
TradeWise/
├── app/
│   └── dashboard.py
├── data/
│   ├── raw/
│   └── processed/
├── src/
│   ├── data_loading.py
│   ├── stock_analysis.py
│   └── data_validation.py
├── tests/
│   └── test_stock_analysis.py
└── README.md
```

## Dashboard Features

- Select a stock from the available options.
- Choose a historical data period.
- Filter data by date range.
- View closing prices.
- Compare closing prices with moving averages.
- Analyze daily percentage returns.
- Visualize rolling volatility.
- View historical stock data.
- Download analysis results as a CSV file.

## Stock Analysis Metrics

### Daily Return

Measures the percentage change in closing price compared
with the previous trading day.

### Moving Average

The 20-day and 50-day moving averages help summarize
recent and longer-term price trends.

### Volatility

The 20-day rolling standard deviation of daily returns
measures how much returns have varied over that period.

## Installation

Create and activate a virtual environment if you do not
already have one.

Install the required libraries:

```bash
pip install pandas numpy yfinance matplotlib plotly streamlit pytest
```

## Run the Project

Run data loading:

```bash
python src/data_loading.py
```

Run data validation:

```bash
python src/data_validation.py
```

Run stock analysis:

```bash
python src/stock_analysis.py
```

Launch the Streamlit dashboard:

```bash
python -m streamlit run app/dashboard.py
```

## Run Tests

```bash
python -m pytest tests/test_stock_analysis.py -v
```

## Data Source

Historical stock data is retrieved from Yahoo Finance
using the yfinance library.

The dashboard includes selected NSE stocks such as
Reliance Industries, TCS, Infosys, HDFC Bank and ICICI Bank.

## Disclaimer

This project is intended for educational and analytical
purposes only. It does not provide financial advice or
guarantee future stock market performance.
