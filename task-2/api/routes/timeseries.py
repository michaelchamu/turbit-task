from fastapi import APIRouter, HTTPException
from typing import List
from ..database import mongo_connector
from ..models.timeseries import TimeSeriesModel

route = APIRouter()

@route.get("/timeseries", response_model=List[TimeSeriesModel])
async def get_time_series_data():
    try:
        # Fetch time series data from the database
        time_series_data = await mongo_connector.mongodb.db['time-series-data'].find().to_list(length=100)
        if not time_series_data:
            raise HTTPException(status_code=404, detail="No time series data found")
        
        # Convert the fetched data to TimeSeriesModel instances
        return [TimeSeriesModel(**data) for data in time_series_data]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))