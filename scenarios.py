import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io, base64

def run_scenarios(df, horizon=30, simulations=200):
    log_ret    = df['Log_Return'].dropna()
    mu         = log_ret.mean()
    sig        = log_ret.std()
    last_price = float(df['Close'].iloc[-1])

    fig, ax = plt.subplots(figsize=(10, 5))
    all_paths = []

    for _ in range(simulations):
        shocks = np.random.normal(mu, sig, horizon)
        path   = [last_price]
        for s in shocks:
            path.append(path[-1] * np.exp(s))
        all_paths.append(path)
        ax.plot(path, color='steelblue', alpha=0.15, linewidth=0.8)

    all_paths = np.array(all_paths)
    ax.plot(np.percentile(all_paths, 5,  axis=0), 'r--', label='5th pct')
    ax.plot(np.percentile(all_paths, 95, axis=0), 'g--', label='95th pct')
    ax.plot(np.percentile(all_paths, 50, axis=0), 'k-',  label='Median', linewidth=2)

    bull_shocks = np.random.normal(mu + sig, sig, horizon)
    bear_shocks = np.random.normal(mu - sig, sig, horizon)
    bull_path, bear_path = [last_price], [last_price]
    for b, br in zip(bull_shocks, bear_shocks):
        bull_path.append(bull_path[-1] * np.exp(b))
        bear_path.append(bear_path[-1] * np.exp(br))
    ax.plot(bull_path, 'g-', linewidth=2, label='Bull')
    ax.plot(bear_path, 'r-', linewidth=2, label='Bear')

    ax.set_title(f'Monte Carlo Scenarios ({horizon}d horizon)')
    ax.set_xlabel('Days')
    ax.set_ylabel('Price ($)')
    ax.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
