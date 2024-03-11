import pandas as pd
from flask import Flask, render_template, request
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)
import pandas as pd
import logging

def process_data(raw_data):
    logging.debug("Processing raw data")
    # Assuming 'prices' in raw_data contains the date and price information
    if 'prices' in raw_data:
        prices = raw_data['prices']
        # Convert prices to DataFrame
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])
        # Convert timestamp to datetime
        df['Date'] = pd.to_datetime(df['timestamp'], unit='ms')
        df['Price'] = df['price']
        df.drop(columns=['timestamp', 'price'], inplace=True)
        return df
    else:
        logging.error("No 'prices' key in raw_data")
        return pd.DataFrame()

def process_historical_data(data):
    df_prices = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df_volumes = pd.DataFrame(data['total_volumes'], columns=['timestamp', 'volume'])

    # Convert timestamp to datetime
    df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'], unit='ms')
    df_volumes['timestamp'] = pd.to_datetime(df_volumes['timestamp'], unit='ms')

    # You can merge these DataFrames or keep them separate based on your analysis needs
    return df_prices, df_volumes

def process_contract_transactions(transactions):
    if not transactions:
        return pd.DataFrame()
    df = pd.DataFrame(transactions)
    # Convert relevant columns to numeric types
    df['gas'] = pd.to_numeric(df['gas'])
    df['gasPrice'] = pd.to_numeric(df['gasPrice'])
    df['timeStamp'] = pd.to_datetime(df['timeStamp'], unit='s')  # Convert timestamp to datetime
    return df