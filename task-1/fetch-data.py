# Import the requests module
import aiohttp
import asyncio
import json
import pymongo
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

#fetch environment variables
database_url = os.getenv("MONGO_URI")
database_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
database_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
base_url = os.getenv("JSON_PLACEHOLDER")

# MongoDB connection setup
mongo_client = pymongo.MongoClient(database_url, database_username, database_password)
db = mongo_client['users-demo']  # Change to your database name

resource_endpoints = ['posts', 'comments', 'users']

async def fetch_data(url):
    try:
        # Create an asynchronous session
        async with aiohttp.ClientSession() as session:
            # Send a GET request to the desired API URL
            async with session.get(url, timeout=5) as response:
                response.raise_for_status()  # Raise an error for bad responses
                # Parse the response and return it
                data = await response.json()
                return data
    except aiohttp.ClientError as e:
        print(f"Request failed: {e}")

async def main():
    for endpoint in resource_endpoints:
        url = f"{base_url}/{endpoint}"
        data = await fetch_data(url)
        if data:
            # Log the fetched data
            print(f"Data from {endpoint}:")
            try:
            # save the data to mongodb collection matching the endpoint
                collection = db[endpoint]
                if isinstance(data, list):
                    collection.insert_many(data)  # Insert multiple documents
                else:
                    collection.insert_one(data)  # Insert a single document
                print(f"Data saved to MongoDB collection: {endpoint}")
            except Exception as e:
                print(f"Error saving data to MongoDB for {endpoint}")
                print(f"Error: {e}")

asyncio.run(main())