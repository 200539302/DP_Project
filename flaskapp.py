import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template
import json
import threading

# Binance API endpoint
url = "https://api.binance.com/api/v3/klines"

# MongoDB configuration
mongo_uri = "mongodb+srv://200539302:3JCo1k2agFosqzHC@cluster0.oj3tfzo.mongodb.net/"
database_name = "Stockdata"
collection_name = "binance"

# Flask app configuration
app = Flask(__name__)


# Function to fetch and store data from Binance
def fetch_and_store_data():
    while True:
        # Calculate start and end times for the data fetch (last 24 hours)
        end_time = int(time.time() * 1000)
        start_time = end_time - 24 * 60 * 60 * 1000  # 24 hours in milliseconds

        # Binance API parameters
        params = {
            "symbol": "SHIBBUSD",
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

        # Connect to MongoDB
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        db = client[database_name]
        collection = db[collection_name]

        # Delete previous data
        collection.delete_many({})

        # Convert DataFrame to list of dictionaries
        data_list = df.to_dict(orient='records')

        # Insert the data into the MongoDB collection
        collection.insert_many(data_list)

        print("Fetched and stored data successfully.")
        time.sleep(24 * 60 * 60)  # Sleep for 24 hours

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chart')
def chart():
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    db = client[database_name]
    collection = db[collection_name]
    data = list(collection.find())

    # Convert Unix timestamps to JavaScript timestamps and extract high prices
    processed_data = [{'date': entry['Kline open time'], 'high': float(entry['High price'])} for entry in data]

    data_json = json.dumps(processed_data)  # Convert the processed data to JSON
    return render_template('chart.html', data=data_json)


# Create a new thread for the batch process
batch_thread = threading.Thread(target=fetch_and_store_data)

if __name__ == '__main__':
    batch_thread.start()  # Start the batch process thread
    app.run(host='0.0.0.0', port=80)
