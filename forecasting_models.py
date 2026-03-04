import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def moving_average(series, window=5):
    return series.rolling(window).mean().iloc[-1]

def simple_exp_smoothing(series, alpha=0.3):
    result = series.iloc[0]
    for val in series.iloc[1:]:
        result = alpha * val + (1 - alpha) * result
    return result

def holt_linear(series, alpha=0.3, beta=0.1, horizon=1):
    l = series.iloc[0]
    b = series.iloc[1] - series.iloc[0]
    for val in series.iloc[1:]:
        l_prev, b_prev = l, b
        l = alpha * val + (1 - alpha) * (l_prev + b_prev)
        b = beta * (l - l_prev) + (1 - beta) * b_prev
    return l + horizon * b

def linear_regression_forecast(series, horizon=1):
    x = np.arange(len(series)).reshape(-1, 1)
    y = series.values
    model = LinearRegression().fit(x, y)
    future_x = np.array([[len(series) + horizon - 1]])
    return float(model.predict(future_x)[0])

def run_all_models(df, alpha=0.3, horizon=30):
    close = df['Close'].dropna()
    ma   = moving_average(close)
    ses  = simple_exp_smoothing(close, alpha=alpha)
    holt = holt_linear(close, alpha=alpha, horizon=horizon)
    lr   = linear_regression_forecast(close, horizon=horizon)

    forecasts = {'MA': ma, 'SES': ses, 'Holt': holt, 'LR': lr}
    forecast_df = pd.DataFrame([
        {'Model': 'Moving Average (5d)',            'Forecast': round(ma,   2)},
        {'Model': 'Simple Exp Smoothing',            'Forecast': round(ses,  2)},
        {'Model': f'Holt Linear (h={horizon})',      'Forecast': round(holt, 2)},
        {'Model': f'Linear Regression (h={horizon})','Forecast': round(lr,   2)},
    ])
    return forecasts, forecast_df
