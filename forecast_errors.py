import numpy as np

def mad(actual, forecast):
    return np.mean(np.abs(actual - forecast))

def mse(actual, forecast):
    return np.mean((actual - forecast) ** 2)

def mape(actual, forecast):
    actual   = np.array(actual,   dtype=float)
    forecast = np.array(forecast, dtype=float)
    mask     = actual != 0
    return np.mean(np.abs((actual[mask] - forecast[mask]) / actual[mask])) * 100

def compute_errors(df, forecasts):
    actual = df['Close'].dropna().values
    errors = {}
    for name, pred in forecasts.items():
        pred_arr = np.full_like(actual, pred, dtype=float)
        errors[name] = {
            'MAD':  round(mad(actual, pred_arr),  4),
            'MSE':  round(mse(actual, pred_arr),  4),
            'MAPE': round(mape(actual, pred_arr), 4),
        }
    return errors
