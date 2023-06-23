import os

import ccxt

# KuCoin API credentials
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')
api_passphrase = os.getenv('API_PASSPHRASE')

SYMBOLS = ["SOL", "BNB"]

target_weights = {
    SYMBOLS[0]: 0.5,
    SYMBOLS[1]: 0.5
}

## Create a KuCoin client
client = ccxt.kucoin({
    'apiKey': api_key,
    'secret': api_secret,
    'password': api_passphrase,
    'enableRateLimit': True,
})

def get_last_price(symbol="BNB/USDT"):
    # Fetch ticker for BNB/USDT trading pair
    ticker = client.fetch_ticker(symbol)

    # Get the current price
    price = ticker['last']
    return price

# Retrieve account balances
balances = client.fetch_balance()

# Print balance for each currency
obj =  balances['total']

pair_a = get_last_price(f"{SYMBOLS[0]}/USDT")
pair_b = get_last_price(f"{SYMBOLS[1]}/USDT")

# Current portfolio values or quantities
current_values = {
   SYMBOLS[0]: pair_a*obj[SYMBOLS[0]],
   SYMBOLS[1]: pair_b*obj[SYMBOLS[1]]
}

# Total portfolio value
total_value = sum(current_values.values())
# Calculate target values based on weights
target_values = {asset: total_value * weight for asset, weight in target_weights.items()}

# Determine the required adjustments for rebalancing
adjustments = {}
for asset in target_weights:
    target_value = target_values[asset]
    current_value = current_values.get(asset, 0)
    adjustment = target_value - current_value
    adjustments[asset] = adjustment

# Print the adjustments needed for rebalancing
print("Rebalancing adjustments:")
# Execute trades to rebalance the portfolio
for asset, adjustment in adjustments.items():
    txt = "Nothings"
    if round(adjustment) > 0:
        # Buy the asset
        txt = "Buying"
        client.create_order(symbol=asset, side='buy', type='market', amount=adjustment)
        symbol = f"{asset}/USDT"
        market_order = client.create_market_buy_order(symbol, abs(adjustment))
    elif round(adjustment) < 0:
        # Sell the asset
        txt = "Selling"
        symbol = f"{asset}/USDT"
        market_order = client.create_market_sell_order(symbol, abs(adjustment))

    print(f"{txt} {abs(adjustment)} {asset} at market price.")
    

