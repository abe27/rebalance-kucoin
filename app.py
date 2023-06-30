#  MarketData
import os
import pandas as pd
from binance.client import Client as BinanceClient
from kucoin.client import Client as KucoinClient
import requests


KUCOIN_API_KEY = os.getenv("KUCOIN_API_KEY")
KUCOIN_API_SECRET = os.getenv("KUCOIN_API_SECRET")
KUCOIN_API_PASSPHRASE = os.getenv("KUCOIN_API_PASSPHRASE")

BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_API_PASSPHRASE = os.getenv("BINANCE_API_PASSPHRASE")

SATANGPRO_API_KEY = os.getenv("SATANGPRO_API_KEY")
SATANGPRO_API_SECRET = os.getenv("SATANGPRO_API_SECRET")
SATANGPRO_API_PASSPHRASE = os.getenv("SATANGPRO_API_PASSPHRASE")


binance = BinanceClient(BINANCE_API_KEY, BINANCE_API_SECRET)
kucoin = KucoinClient(KUCOIN_API_KEY, KUCOIN_API_SECRET, KUCOIN_API_PASSPHRASE)


def get_kucoin_client():
    pass

def get_binance_client():
    pass

def get_satangpro_client():
    pass

def main():
    # get market depth
    # pair = ["BTC", "ETH", "SDT", "USD", "BNB","PAX", "SDC", "XRP", "SDS", "TRX", "NGN", "RUB", "TRY", "EUR", "ZAR", "KRW", "DRT"]
    pair = ["BTC", "ETH", "SDT", "USD"]
    symbols = binance.get_all_tickers()
    for s in symbols:
       try:
            symbol = s["symbol"]
            p = pair[pair.index(symbol[len(symbol)-3:])]
            x = 3
            if p == "SDT" or p == "USD":
                x = 4

            sym_pair = s["symbol"][len(symbol)-x:]
            asset = s["symbol"][:len(symbol) - len(sym_pair)]
            url = f"https://api.kucoin.com/api/v1/market/stats?symbol={asset}-{sym_pair}"
            res = requests.request("GET", url)
            obj = res.json()
            if obj['data']['last'] != None:
                print(f"{asset}-{sym_pair} ::: {float(s['price'])} ==> {float(obj['data']['last'])} ???? {float(s['price'])-float(obj['data']['last'])}")
       except:
           pass

    # symbols = kucoin.get_ticker()
    # for s in symbols:
    #     # print(s["symbol"])
    #     print(s)

if __name__ == "__main__":
    main()