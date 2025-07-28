from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from .database import mongo_connector  # import the MongoDB connection functions
from .services import csv_service  # import the CSV service
from .routes import time_series  # import the time-series routes

app = FastAPI()  # initialize the FastAPI application

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_connector.connect_to_mongo()
    await csv_service.populate_time_series(mongo_connector.mongodb.db)
    print("Application started and connected to MongoDB")
    yield  # This is where the application runs
    await mongo_connector.close_mongo_connection()

app = FastAPI(lifespan=lifespan)  # Use the lifespan context manager

app.include_router(time_series.route)

@app.get("/")
async def root():
    """
    Default endpoint.
    """
    return {"message": "Task-2 API Running!"}