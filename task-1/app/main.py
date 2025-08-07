from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI #get the FastAPI and other modules from it
from mongoconnector import mongo_connector #import the MongoDB connection functions
import logging
from fastapi.middleware.cors import CORSMiddleware

from customlogger import customlogger
from .services import populate_db
from .routes import users, posts, comments, reports #import all defined routes

from dotenv import load_dotenv
import os

customlogger.setup_logging()
logger = logging.getLogger("task-1")

origins = ["http://localhost:3000",
           "http://localhost:5173",
           "http://127.0.0.1:5173",
            os.getenv('PRODUCTION_CLIENT')
           ]

load_dotenv()
'''
When the application starts, connect to MongoDB uisng lifespan context manager
When the application stops, close the MongoDB connection
This ensures that the database connection is properly managed throughout the application's lifecycle
The lifespan context manager allows for setup and teardown operations around the application lifecycle
This is useful for managing resources like database connections, ensuring they are opened when the app starts
and closed when the app stops, preventing resource leaks and ensuring clean shutdowns.
when application starts, and connects to MongoDB, Check if the 3 required collections exist.
if they dont exist, create them and populate them with data from the JSON Placeholder API.
'''

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_connector.connect_to_mongo(os.getenv('USERS_COLLECTION'))
    await populate_db.populate_db(mongo_connector.mongodb.db)
    print("Application started and connected to MongoDB")
    yield   # This is where the application runs
    await mongo_connector.close_mongo_connection()

app = FastAPI(lifespan=lifespan, title="UsersAPI")  # Use the lifespan context manager

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # React App origins
    allow_credentials=True,
    allow_methods=["GET"],#since we are only fetching data, allow only GET requests
    allow_headers=["*"],
    expose_headers=["*"],  # to allow downloading files
)
app.include_router(users.route)
app.include_router(posts.route)
app.include_router(comments.route)
app.include_router(reports.route)

@app.get("/")
async def root():
    """
    default endpoint.
    """
    return {"message": "Task-1 API Running!"}