from flask import Flask, render_template, request
import traceback

from data_prep import get_stock_data
from indicators import add_indicators
from forecasting_models import run_all_models
from forecast_errors import compute_errors
from events import detect_events
from scenarios import run_scenarios
from chart_price import build_price_chart

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    ticker  = request.form.get('ticker', 'AAPL').upper().strip()
    start   = request.form.get('start', '2022-01-01')
    end     = request.form.get('end',   '2024-01-01')
    alpha   = float(request.form.get('alpha', 0.3))
    horizon = int(request.form.get('horizon', 30))

    try:
        df = get_stock_data(ticker, start, end)
        df = add_indicators(df)

        forecasts, forecast_df = run_all_models(df, alpha=alpha, horizon=horizon)
        errors        = compute_errors(df, forecasts)
        events        = detect_events(df)
        scenario_plot = run_scenarios(df, horizon=horizon)
        price_chart   = build_price_chart(df, ticker=ticker)

        # Summary stats
        close = df['Close']
        stats = {
            'last_close':  round(float(close.iloc[-1]), 2),
            'pct_change':  round(float((close.iloc[-1] - close.iloc[0]) / close.iloc[0] * 100), 2),
            'high':        round(float(close.max()), 2),
            'low':         round(float(close.min()), 2),
            'volatility':  round(float(df['Log_Return'].std() * (252**0.5) * 100), 2),
            'rsi_last':    round(float(df['RSI'].iloc[-1]), 1) if 'RSI' in df.columns else 'N/A',
            'data_points': len(df),
        }

        return render_template(
            'results.html',
            ticker=ticker,
            start=start,
            end=end,
            horizon=horizon,
            tables=[forecast_df.to_html(classes='table', index=False)],
            errors=errors,
            events=events,
            scenario_plot=scenario_plot,
            price_chart=price_chart,
            stats=stats,
        )
    except Exception as e:
        return f'<pre style="color:#ef4444;background:#0f172a;padding:20px">{traceback.format_exc()}</pre>', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
