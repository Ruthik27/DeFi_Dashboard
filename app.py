from flask import Flask, render_template, request
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
import io
from flask import send_file
import matplotlib.pyplot as plt
from data_fetching import fetch_defi_data  # Ensure you have a function to fetch the data
from data_processing import process_data  # Ensure you have a function to process the data

# Import your module functions
from data_fetching import fetch_defi_data, fetch_historical_data, fetch_contract_transactions
from data_processing import process_data, process_historical_data, process_contract_transactions
from visualization import generate_price_plot, generate_time_series_plot
from predictive_modeling import predict_future_prices

from flask import Flask, render_template, request
import logging

# Import your modules here
from data_fetching import fetch_defi_data
from data_processing import process_data
from visualization import generate_price_plot

# Setup logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/')
def index():
    logging.info("Index route called")
    token_id = request.args.get('token', 'uniswap')
    time_range = request.args.get('time_range', '7d')
    logging.debug(f"Fetching data for token: {token_id} and time range: {time_range}")
    
    raw_data = fetch_defi_data(token_id, time_range)
    if raw_data:
        logging.debug("Processing data")
        df = process_data(raw_data)
        logging.debug("Generating price plot")
        price_plot = generate_price_plot(df)
    else:
        logging.error("Failed to fetch data")
        price_plot = None

    return render_template('index.html', price_plot=price_plot)


@app.route('/time_series')
def time_series():
    logging.info("Time series page requested")
    token_id = request.args.get('token', 'uniswap')
    days = request.args.get('days', '365')

    historical_data = fetch_historical_data(token_id, days)
    if historical_data:
        logging.info(f"Historical data fetched for token: {token_id}, days: {days}")
        df_prices, df_volumes = process_historical_data(historical_data)
        price_plot = generate_time_series_plot(df_prices)
        return render_template('time_series.html', price_plot=price_plot)
    else:
        logging.error(f"Failed to fetch historical data for token: {token_id}, days: {days}")
        return "Failed to fetch historical data."

@app.route('/contract_analysis')
def contract_analysis():
    logging.info("Contract analysis page requested")
    contract_address = request.args.get('address')
    transactions = fetch_contract_transactions(contract_address)
    df_transactions = process_contract_transactions(transactions)
    avg_gas_used = "Data not available." if df_transactions.empty else str(df_transactions['gas'].mean())

    return render_template('contract_analysis.html', avg_gas_used=avg_gas_used)

@app.route('/price_plot')
def price_plot():
    token = request.args.get('token', 'uniswap')
    
    # Fetch and process the data
    raw_data = fetch_defi_data(token)
    if not raw_data:
        return "Data not found", 404
    df = process_data(raw_data)
    
    # Generate the plot
    plt.figure()
    plt.plot(df['Date'], df['Price'])  # Adjust field names as per your DataFrame
    plt.title(f'Price Plot for {token}')
    plt.xlabel('Date')
    plt.ylabel('Price')
    
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Return the buffer content as a response
    return send_file(buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
