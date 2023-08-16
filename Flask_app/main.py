from flask import Flask, render_template
from pymongo import MongoClient
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://200539302:3JCo1k2agFosqzHC@cluster0.oj3tfzo.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


app = Flask(__name__)
db = client["Stockdata"]  # Replace 'your_database_name' with your actual database name
collection = db["binance"]  # Replace 'your_collection_name' with your actual collection name

@app.route('/')
def index():
    stock_data = list(collection.find({}))  # Retrieve all data from the collection
    return render_template('index.html', stock_data=stock_data)
