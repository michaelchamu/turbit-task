from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from mongoconnector import mongo_connector  # import the MongoDB connection functions
import logging
from customlogger import customlogger
from .services import csv_service  # import the CSV service
from .routes import timeseries  # import the time-series routes

from dotenv import load_dotenv
import os

load_dotenv()

customlogger.setup_logging()
logger = logging.getLogger("task-2")

# Configure CORS middleware to allow requests from the React App and other origins
origins = ["http://localhost:3000",
           "http://localhost:5173",
           "http://127.0.0.1:5173",
            os.getenv('PRODUCTION_CLIENT')
           ]

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Connecting to database.....")
    await mongo_connector.connect_to_mongo(os.getenv('TURBINES_COLLECTION'))
    logger.info("Populating data")
    await csv_service.populate_time_series(mongo_connector.mongodb.db)
    logger.info("Application started and connected to MongoDB")
    yield  # This is where the application runs
    await mongo_connector.close_mongo_connection()

app = FastAPI(lifespan=lifespan, title="TurbineDataApi")  # Use the lifespan context manager

#add CORS middleware here to allow cross-origin requests
#if added at the top, it will be overwritten and will cause CORS issues
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,  # React App origins
    allow_credentials=True,
    allow_methods=["GET"],#since we are only fetching data, allow only GET requests
    allow_headers=["*"],
    expose_headers=["*"],  # to allow downloading files
)
app.include_router(timeseries.route)

@app.get("/")
async def root():
    """
    Default endpoint.
    """
    return {"message": "Task-2 API Running!"}