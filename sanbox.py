#  MarketData
import os
import pandas as pd
from kucoin.client import Market
# client = Market(url='https://api.kucoin.com')
# # client = Market()

url='https://openapi-sandbox.kucoin.com'
# or connect to Sandbox
client = Market(url=url)
client = Market(is_sandbox=True)

# get symbol kline
klines = client.get_kline('BTC-USDT','1min')

# get symbol ticker
server_time = client.get_server_timestamp()

api_key =  os.getenv("SAND_API_KEY")
api_secret = os.getenv("SAND_API_SECRET")
api_passphrase = os.getenv("SAND_API_PASSPHRASE")

symbols = client.get_market_list()
tickers = client.get_all_tickers()
tickers = pd.DataFrame(tickers['ticker'])
tickers.set_index('symbol', inplace=True)
tickers.head().T
print(tickers)