#  MarketData
import os
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

# # Trade
# from kucoin.client import Trade
# client = Trade(key=api_key, secret=api_secret, passphrase=api_passphrase, is_sandbox=False, url=url)

# # or connect to Sandbox
# # client = Trade(api_key, api_secret, api_passphrase, is_sandbox=True)

# # place a limit buy order
# order_id = client.create_limit_order('BTC-USDT', 'buy', '1', '8000')

# # place a market buy order   Use cautiously
# order_id = client.create_market_order('BTC-USDT', 'buy', size='1')

# # cancel limit order
# client.cancel_order('5bd6e9286d99522a52e458de')

# User
from kucoin.client import User
client = User(api_key, api_secret, api_passphrase)

# or connect to Sandbox
# client = User(api_key, api_secret, api_passphrase, is_sandbox=True)

address = client.get_withdrawal_quota('BTC')
print(address)