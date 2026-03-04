# OM Stock Analyzer

A Flask-based stock analysis web application that combines **technical indicators**, **multiple forecasting models**, **Monte Carlo simulations**, and **anomaly event detection** into a clean, dark-themed dashboard.

---

## Features

| Section | Details |
|---|---|
| **Price Chart** | Close price + SMA-20, SMA-50, Bollinger Bands, Log Returns bar chart, RSI(14) |
| **Forecasting** | Moving Average, Simple Exponential Smoothing, Holt Linear, Linear Regression |
| **Forecast Errors** | MAD, MSE, MAPE for each model |
| **Monte Carlo** | 200 simulated paths + Bull/Bear shock scenarios |
| **Anomaly Events** | Z-score detection on log returns (threshold = 2.5) |
| **Stats Bar** | Last close, period return, high/low, annualized volatility, RSI, data points |

---

## Project Structure

```
om-stock-analyzer/
|-- app.py                  # Flask server & routes
|-- data_prep.py            # yfinance download + log returns
|-- indicators.py           # SMA, Bollinger Bands, RSI
|-- forecasting_models.py   # MA, SES, Holt Linear, Linear Regression
|-- forecast_errors.py      # MAD, MSE, MAPE
|-- events.py               # Z-score anomaly detection
|-- scenarios.py            # Monte Carlo + Bull/Bear overlays
|-- chart_price.py          # 3-panel price chart (matplotlib)
|-- requirements.txt
|-- templates/
|   |-- index.html          # Input form
|   |-- results.html        # Full results dashboard
|-- static/
    |-- style.css           # Dark navy theme
```

---

## Quick Start

### 1. Clone
```bash
git clone https://github.com/sunnyxvunti/om-stock-analyzer.git
cd om-stock-analyzer
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run
```bash
python app.py
```

Open your browser at `http://localhost:8080`

---

## Deploy on Replit

1. Import this repo into Replit (Use URL import)
2. In the Shell: `pip install -r requirements.txt`
3. Set run command to `python app.py`
4. Click Run — app serves on port 8080

---

## How It Works

### Data (`data_prep.py`)
- Downloads OHLCV data via `yfinance`
- Computes daily log returns: `ln(P_t / P_{t-1})`

### Indicators (`indicators.py`)
- **SMA-20 / SMA-50**: Rolling means
- **Bollinger Bands**: SMA-20 ± 2 standard deviations
- **RSI(14)**: Relative Strength Index using Wilder smoothing

### Forecasting Models (`forecasting_models.py`)
| Model | Method |
|---|---|
| Moving Average | Rolling 5-day mean of last window |
| Simple Exponential Smoothing | Weighted average with alpha |
| Holt Linear | Trend-adjusted exponential smoothing |
| Linear Regression | OLS fit projected h days forward |

### Forecast Errors (`forecast_errors.py`)
- **MAD**: Mean Absolute Deviation
- **MSE**: Mean Squared Error
- **MAPE**: Mean Absolute Percentage Error

### Monte Carlo (`scenarios.py`)
- Fits mu/sigma from historical log returns
- Simulates 200 GBM paths over the horizon
- Overlays 5th, 50th, 95th percentiles
- Bull scenario: mu + 1sigma drift
- Bear scenario: mu - 1sigma drift

### Events (`events.py`)
- Flags daily log returns with |z-score| > 2.5
- Labels each as a surge or drop

---

## Tech Stack

- **Backend**: Python 3, Flask
- **Data**: yfinance, pandas, numpy
- **Charts**: matplotlib (Agg backend, base64 PNG)
- **ML**: scikit-learn (LinearRegression)
- **Frontend**: Jinja2 templates, vanilla CSS

---

## Example Tickers

AAPL, TSLA, MSFT, NVDA, AMZN, RIVN, SPY, QQQ

---

*Built as Step 1 of the OM Stock Analyzer project.*
