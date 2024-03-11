from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

def predict_future_prices(df_prices):
    if df_prices.empty or len(df_prices) < 2:
        return None, None

    # Prepare data for modeling
    df_prices['days'] = (df_prices['timestamp'] - df_prices['timestamp'].min()).dt.days
    X = df_prices[['days']]
    y = df_prices['price']

    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Linear Regression Model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predictions
    future_days = np.array([[X['days'].max() + i] for i in range(1, 31)])  # Predict the next 30 days
    future_prices = model.predict(future_days)

    return future_days.flatten(), future_prices