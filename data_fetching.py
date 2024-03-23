import requests
import logging

logging.getLogger('matplotlib').setLevel(logging.WARNING)

def fetch_defi_data(token_id='uniswap', time_range='7d'):
    """
    Fetch DeFi data for a given token ID and time range.
    
    Args:
        token_id (str): The ID of the token to fetch data for.
        time_range (str): The time range for which to fetch data (e.g., '7d', '30d', '1y').
        
    Returns:
        dict: DeFi data retrieved from the API response.
    """
    logging.debug(f"Fetching DEFI data for {token_id} with time range {time_range}")
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}/market_chart"
    params = {"vs_currency": "usd", "days": time_range}
    try:
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # This will raise an exception for 4xx/5xx errors
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching DEFI data for {token_id}: {e}")
        return None

def fetch_contract_transactions(contract_address, api_key="FPZ5GZ6EBDS1R2SD7IRMQNKSXF4JS4MMI5"):
    """
    Fetch contract transactions for a given contract address.
    
    Args:
        contract_address (str): The contract address to fetch transactions for.
        api_key (str): The API key for accessing the Etherscan API (default is a placeholder key).
        
    Returns:
        list: List of transaction data retrieved from the API response.
    """
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
        logging.error(f"Error fetching contract transactions: {response.status_code}")
        return []

def fetch_historical_data(token_id='uniswap', days='90', interval='daily'):
    """
    Fetch historical market data for a given token ID.
    
    Args:
        token_id (str): The ID of the token to fetch historical data for.
        days (str): The number of days of historical data to fetch (default is '90').
        interval (str): The interval of historical data (e.g., 'daily', 'hourly', etc.).
        
    Returns:
        dict: Historical market data retrieved from the API response.
    """
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
        logging.error(f"Error fetching historical data: {response.status_code}")
        return None

def fetch_market_cap(token_id='uniswap'):
    """
    Fetch market capitalization data for a given token ID.
    
    Args:
        token_id (str): The ID of the token to fetch market cap for.
        
    Returns:
        float: Market capitalization of the token.
    """
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data.get('market_data', {}).get('market_cap', {}).get('usd')
    except requests.RequestException as e:
        logging.error(f"Error fetching market cap for {token_id}: {e}")
        return None

def fetch_trading_volume(token_id='uniswap'):
    """
    Fetch trading volume data for a given token ID.
    
    Args:
        token_id (str): The ID of the token to fetch trading volume for.
        
    Returns:
        float: Trading volume of the token.
    """
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data.get('market_data', {}).get('total_volume', {}).get('usd')
    except requests.RequestException as e:
        logging.error(f"Error fetching trading volume for {token_id}: {e}")
        return None

def fetch_liquidity(token_id='uniswap'):
    """
    Fetch liquidity data for a given token ID.
    
    Args:
        token_id (str): The ID of the token to fetch liquidity for.
        
    Returns:
        float: Liquidity of the token.
    """
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}"
    try:
        response = requests.get(endpoint)
        response.raise_for_status()
        data = response.json()
        return data.get('market_data', {}).get('total_liquidity', {}).get('usd')
    except requests.RequestException as e:
        logging.error(f"Error fetching liquidity for {token_id}: {e}")
        return None

def fetch_extended_historical_data(token_id='uniswap', start_date=None, end_date=None):
    # Fetch historical data beyond the CoinGecko API's limitations (e.g., beyond 90 days)
    if not start_date:
        start_date = datetime.now() - timedelta(days=365)  # Default to one year ago
    if not end_date:
        end_date = datetime.now()
    base_url = "https://api.coingecko.com/api/v3"
    endpoint = f"{base_url}/coins/{token_id}/market_chart/range"
    params = {
        "vs_currency": "usd",
        "from": int(start_date.timestamp()),
        "to": int(end_date.timestamp())
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(f"Error fetching extended historical data: {response.status_code}")
        return None
