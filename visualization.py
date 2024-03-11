import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from io import BytesIO
import logging
import matplotlib.pyplot as plt
import base64
from io import BytesIO
import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg' to prevent GUI-related errors
import matplotlib.pyplot as plt


def generate_time_series_plot_with_predictions(df, future_days, future_prices):
    plt.figure(figsize=(10, 6))
    plt.plot(df['Date'], df['Price'], label='Historical Prices')
    plt.plot(future_days, future_prices, label='Predicted Prices', linestyle='--')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Price Over Time with Predictions')
    plt.legend()

    # Convert plot to a base64 string
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    plt.close()

    return base64_string

def generate_price_plot(df):
    logging.debug("Generating price plot")
    sns.set_theme(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='Date', y='Price')  # Adjust these column names as needed
    plt.title('Token Price Over Time')
    plt.xlabel('Time')
    plt.ylabel('Price (USD)')
    plt.xticks(rotation=45)
    
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf8')
    buffer.close()
    plt.close()
    return plot_data

def generate_time_series_plot(df, title='Token Price Over Time', y='price'):
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df, x='timestamp', y=y)
    plt.title(title)
    plt.xlabel('Date')
    plt.ylabel(y.capitalize())
    plt.xticks(rotation=45)

    buffer = BytesIO()
    plt.savefig(buffer, format="png", bbox_inches="tight")
    plt.close()
    return base64.b64encode(buffer.getvalue()).decode()