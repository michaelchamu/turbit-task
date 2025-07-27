from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI #get the FastAPI and other modules from it
from .database import mongo_connector #import the MongoDB connection functions
from .routes import users #import all defined routes

app = FastAPI() #initialize the FastAPI application

#When the application starts, connect to MongoDB uisng lifespan context manager
#When the application stops, close the MongoDB connection
#This ensures that the database connection is properly managed throughout the application's lifecycle
#The lifespan context manager allows for setup and teardown operations around the application lifecycle
#This is useful for managing resources like database connections, ensuring they are opened when the app starts
#and closed when the app stops, preventing resource leaks and ensuring clean shutdowns.
@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_connector.connect_to_mongo()
    yield   # This is where the application runs
    await mongo_connector.close_mongo_connection()

app = FastAPI(lifespan=lifespan)  # Use the lifespan context manager

app.include_router(users.route)

@app.get("/")
async def root():
    """
    default endpoint.
    """
    return {"message": "Task-1 API Running!"}