from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from .database import mongo_connector  # import the MongoDB connection functions
from .services import csv_service  # import the CSV service
from .routes import timeseries  # import the time-series routes

app = FastAPI()  # initialize the FastAPI application

# Configure CORS middleware to allow requests from the React App and other origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React App origins
    allow_credentials=True,
    allow_methods=["GET"]#since we are only fetching data, allow only GET requests
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_connector.connect_to_mongo()
    await csv_service.populate_time_series(mongo_connector.mongodb.db)
    print("Application started and connected to MongoDB")
    yield  # This is where the application runs
    await mongo_connector.close_mongo_connection()

app = FastAPI(lifespan=lifespan)  # Use the lifespan context manager

app.include_router(timeseries.route)

@app.get("/")
async def root():
    """
    Default endpoint.
    """
    return {"message": "Task-2 API Running!"}