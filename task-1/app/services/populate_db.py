#is used to do the initial population of the mongo database if it is empty
# Import the requests module
import httpx
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv() 

from fastapi import FastAPI

collection_names = ["users", "posts", "comments"]
base_url = os.getenv("JSON_PLACEHOLDER")
#TODO Check duplication and only write new records
async def populate_db(db: AsyncIOMotorClient):
    #1st fetch all collections in the database to prevent multiple round trips
    existing_collections = await db.list_collection_names()
    # loop through the collection names and check if they exist and if they are not empty
    try:
        for collection in collection_names:
            # If the collection does not exist or is empty, populate it
            if collection not in existing_collections or await db[collection].count_documents({}) == 0:
                async with httpx.AsyncClient() as client:
                    # Fetch data from the JSON Placeholder API
                    response = await client.get(f"{base_url}/{collection}")
                    if response.status_code == 200:
                        data = response.json()
                    # Insert data into the MongoDB collection
                        await db[collection].insert_many(data)
                        print(f"Populated {collection} collection with {len(data)} documents.")
                    else:
                        print(f"Failed to fetch {collection} data: {response.status_code}")
            print(f"{collection} collection is already populated or does not need to be populated.")
    except Exception as e:
        print(f"An error occurred while populating the database: {e}")