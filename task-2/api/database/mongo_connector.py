from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

#fetch environment variables
database_url = os.getenv("MONGO_URI")
database_port = os.getenv("MONGO_PORT")
database_username = os.getenv("MONGO_INITDB_ROOT_USERNAME")
database_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
base_url = os.getenv("JSON_PLACEHOLDER")

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(
        host=database_url,
        port=int(database_port),
        username=database_username,
        password=database_password
    )
    mongodb.db = mongodb.client['time-series-demo']
    print("Connected to MongoDB")

async def close_mongo_connection():
    if mongodb.client:
        mongodb.client.close()
        print("MongoDB connection closed")