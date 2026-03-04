import numpy as np

def detect_events(df, z_thresh=2.5):
    log_ret = df['Log_Return'].dropna()
    mean    = log_ret.mean()
    std     = log_ret.std()
    z_scores = (log_ret - mean) / std
    anomalies = z_scores[z_scores.abs() > z_thresh]

    events = []
    for date, z in anomalies.items():
        direction = 'surge' if z > 0 else 'drop'
        pct = df.loc[date, 'Log_Return'] * 100
        events.append({
            'date':        str(date.date()),
            'z_score':     round(z, 2),
            'pct_change':  round(pct, 2),
            'direction':   direction,
            'explanation': (
                f'Abnormal {direction} of {abs(pct):.2f}% '
                f'(z={z:.2f}) - possible news or macro event.'
            ),
        })
    return events
