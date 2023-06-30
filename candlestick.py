import datetime
import pandas as pd
import mplfinance as mpf
import websocket
import json
import threading

# Initialize an empty DataFrame for storing real-time data
real_time_data = pd.DataFrame(columns=['date', 'open', 'high', 'low', 'close', 'volume'])

# Create a lock to synchronize access to the DataFrame
data_lock = threading.Lock()

# Define the WebSocket URL for the real-time data feed
websocket_url = 'https://api.bitkub.com/websocket-api?streams='

# Define the symbol or stock to fetch real-time data for
symbol = 'market.ticker.thb_btc'

# Define the timeframe for the candlestick chart
timeframe = '5Min'

# Function to process incoming WebSocket messages
def on_message(ws, message):
    global real_time_data

    # Parse the JSON message
    data = json.loads(message)

    # Extract the OHLCV data from the message
    ohlcv = data['ohlcv']

    # Extract the timestamp from the message and convert it to datetime format
    timestamp = datetime.datetime.fromtimestamp(data['timestamp'] / 1000)

    # Create a new row with the real-time data
    new_row = {'date': timestamp, 'open': ohlcv['open'], 'high': ohlcv['high'],
               'low': ohlcv['low'], 'close': ohlcv['close'], 'volume': ohlcv['volume']}

    # Acquire the lock before accessing the DataFrame
    data_lock.acquire()

    # Append the new row to the real-time data DataFrame
    real_time_data = real_time_data.append(new_row, ignore_index=True)

    # Release the lock after updating the DataFrame
    data_lock.release()

# Function to establish the WebSocket connection
def connect_websocket():
    ws = websocket.WebSocket(f"{websocket_url}{symbol}", on_message=on_message)

    # Start the WebSocket connection
    ws.run_forever()

# Function to plot the real-time candlestick chart
def plot_real_time_chart():
    global real_time_data

    while True:
        # Acquire the lock before accessing the DataFrame
        data_lock.acquire()

        # Create a copy of the real-time data DataFrame
        data_copy = real_time_data.copy()

        # Release the lock after accessing the DataFrame
        data_lock.release()

        if not data_copy.empty:
            # Plot the candlestick chart
            mpf.plot(data_copy, type='candle', style='yahoo', title='Real-Time Chart: ' + symbol,
                     datetime_format='%Y-%m-%d %H:%M:%S')

# Create and start a thread for establishing the WebSocket connection
websocket_thread = threading.Thread(target=connect_websocket)
websocket_thread.start()

# Create and start a thread for plotting the real-time candlestick chart
chart_thread = threading.Thread(target=plot_real_time_chart)
chart_thread.start()
