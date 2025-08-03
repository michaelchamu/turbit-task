from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI #get the FastAPI and other modules from it
from mongoconnector import mongo_connector #import the MongoDB connection functions
from .services import populate_db
from .routes import users, posts, comments, reports #import all defined routes

app = FastAPI() #initialize the FastAPI application

#When the application starts, connect to MongoDB uisng lifespan context manager
#When the application stops, close the MongoDB connection
#This ensures that the database connection is properly managed throughout the application's lifecycle
#The lifespan context manager allows for setup and teardown operations around the application lifecycle
#This is useful for managing resources like database connections, ensuring they are opened when the app starts
#and closed when the app stops, preventing resource leaks and ensuring clean shutdowns.
#when application starts, and connects to MongoDB, Check if the 3 required collections exist.
#if they dont exist, create them and populate them with data from the JSON Placeholder API.

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_connector.connect_to_mongo('users-data')
    await populate_db.populate_db(mongo_connector.mongodb.db)
    print("Application started and connected to MongoDB")
    yield   # This is where the application runs
    await mongo_connector.close_mongo_connection()

app = FastAPI(lifespan=lifespan)  # Use the lifespan context manager

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