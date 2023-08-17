import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template
import json
import threading

end_time = int(time.time() * 1000)
start_time = end_time - 24 * 60 * 60 * 1000  # 24 hours in milliseconds
url = "https://api.binance.com/api/v3/klines"

# Binance API parameters
params = {
    "symbol": "BTCUSDT",
    "interval": "15m",
    "startTime": start_time,
    "endTime": end_time
}

response = requests.get(url, params=params)
data = response.json()

columns = [
    "Kline open time", "Open price", "High price", "Low price", "Close price",
    "Volume", "Kline close time", "Quote asset volume", "Number of trades",
    "Taker buy base asset volume", "Taker buy quote asset volume", "Unused"
]

df = pd.DataFrame(data, columns=columns)
data_list = df.to_dict(orient='records')

print("data is")
print(data_list)
print(response.json)
print(response)
