import requests
from flask import Flask, render_template, request
import logging
logging.getLogger('matplotlib').setLevel(logging.WARNING)

def fetch_defi_data(token_id='uniswap', time_range='7d'):
    logging.debug(f"Fetching DEFI data for {token_id} with time range {time_range}")
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}/market_chart"
    params = {"vs_currency": "usd", "days": time_range}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # This will raise an exception for 4xx/5xx errors
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching data for {token_id}: {e}")
        return None

def fetch_contract_transactions(contract_address, api_key="FPZ5GZ6EBDS1R2SD7IRMQNKSXF4JS4MMI5"):
    etherscan_api_url = "https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",  # For normal transactions; use "txlistinternal" for internal transactions
        "address": contract_address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    response = requests.get(etherscan_api_url, params=params)
    if response.status_code == 200:
        transactions = response.json().get('result', [])
        return transactions
    else:
        print(f"Error fetching contract transactions: {response.status_code}")
        return []

def fetch_historical_data(token_id='uniswap', days='90', interval='daily'):
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}/market_chart"
    params = {
        "vs_currency": "usd",
        "days": days,
        "interval": interval  # 'daily', 'hourly', etc.
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching historical data: {response.status_code}")
        return None
