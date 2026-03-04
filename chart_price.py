import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import io, base64
import numpy as np

def build_price_chart(df, ticker='Stock'):
    """
    Returns a base64 PNG with 3 subplots:
      1. Price + SMA20 + SMA50 + Bollinger Bands
      2. Volume (if available) or Log Returns
      3. RSI with overbought/oversold lines
    """
    fig = plt.figure(figsize=(12, 9), facecolor='#0f172a')
    gs  = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.08)

    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    ax3 = fig.add_subplot(gs[2], sharex=ax1)

    for ax in [ax1, ax2, ax3]:
        ax.set_facecolor('#1e293b')
        ax.tick_params(colors='#94a3b8', labelsize=8)
        ax.spines['bottom'].set_color('#334155')
        ax.spines['top'].set_color('#334155')
        ax.spines['left'].set_color('#334155')
        ax.spines['right'].set_color('#334155')
        ax.yaxis.label.set_color('#94a3b8')

    dates = df.index

    # --- Subplot 1: Price + Indicators ---
    ax1.plot(dates, df['Close'],    color='#38bdf8', linewidth=1.5, label='Close',    zorder=3)
    if 'SMA_20' in df.columns:
        ax1.plot(dates, df['SMA_20'], color='#f59e0b', linewidth=1.0, label='SMA 20', zorder=2)
    if 'SMA_50' in df.columns:
        ax1.plot(dates, df['SMA_50'], color='#a78bfa', linewidth=1.0, label='SMA 50', zorder=2)
    if 'BB_Upper' in df.columns:
        ax1.fill_between(dates, df['BB_Lower'], df['BB_Upper'],
                         alpha=0.12, color='#38bdf8', label='Bollinger Band')
        ax1.plot(dates, df['BB_Upper'], color='#38bdf8', linewidth=0.5, linestyle='--')
        ax1.plot(dates, df['BB_Lower'], color='#38bdf8', linewidth=0.5, linestyle='--')

    ax1.set_title(f'{ticker} — Price & Technical Indicators',
                  color='#e2e8f0', fontsize=13, pad=10)
    ax1.set_ylabel('Price ($)', color='#94a3b8')
    ax1.legend(loc='upper left', facecolor='#0f172a', edgecolor='#334155',
               labelcolor='#e2e8f0', fontsize=8)
    ax1.grid(color='#334155', linewidth=0.4, alpha=0.6)
    plt.setp(ax1.get_xticklabels(), visible=False)

    # --- Subplot 2: Log Returns ---
    if 'Log_Return' in df.columns:
        ret = df['Log_Return'].fillna(0)
        pos = ret >= 0
        ax2.bar(dates[pos],  ret[pos],  color='#22c55e', width=1, alpha=0.8)
        ax2.bar(dates[~pos], ret[~pos], color='#ef4444', width=1, alpha=0.8)
        ax2.axhline(0, color='#334155', linewidth=0.6)
        ax2.set_ylabel('Log Ret', color='#94a3b8')
        ax2.grid(color='#334155', linewidth=0.4, alpha=0.6)
    plt.setp(ax2.get_xticklabels(), visible=False)

    # --- Subplot 3: RSI ---
    if 'RSI' in df.columns:
        ax3.plot(dates, df['RSI'], color='#fb923c', linewidth=1.2, label='RSI(14)')
        ax3.axhline(70, color='#ef4444', linewidth=0.8, linestyle='--', alpha=0.7)
        ax3.axhline(30, color='#22c55e', linewidth=0.8, linestyle='--', alpha=0.7)
        ax3.fill_between(dates, df['RSI'], 70,
                         where=(df['RSI'] >= 70), alpha=0.15, color='#ef4444')
        ax3.fill_between(dates, df['RSI'], 30,
                         where=(df['RSI'] <= 30), alpha=0.15, color='#22c55e')
        ax3.set_ylim(0, 100)
        ax3.set_ylabel('RSI', color='#94a3b8')
        ax3.legend(loc='upper left', facecolor='#0f172a', edgecolor='#334155',
                   labelcolor='#e2e8f0', fontsize=8)
        ax3.grid(color='#334155', linewidth=0.4, alpha=0.6)

    ax3.tick_params(axis='x', rotation=30)
    fig.patch.set_facecolor('#0f172a')
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=130, bbox_inches='tight', facecolor='#0f172a')
    plt.close(fig)
    buf.seek(0)
    return base64.b64encode(buf.read()).decode('utf-8')
