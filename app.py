from flask import Flask, render_template, request
import traceback

from data_prep import get_stock_data
from indicators import add_indicators
from forecasting_models import run_all_models
from forecast_errors import compute_errors
from events import detect_events
from scenarios import run_scenarios

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
        errors = compute_errors(df, forecasts)
        events = detect_events(df)
        scenario_plot = run_scenarios(df, horizon=horizon)

        return render_template(
            'results.html',
            ticker=ticker,
            tables=[forecast_df.to_html(classes='table', index=False)],
            errors=errors,
            events=events,
            scenario_plot=scenario_plot,
        )
    except Exception as e:
        return f'<pre>{traceback.format_exc()}</pre>', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
