from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from pymongo import ASCENDING

from ..database import mongo_connector
from ..models.timeseries import TimeSeriesModel

route = APIRouter()

@route.get("/timeseries", response_model=List[TimeSeriesModel])
async def get_time_series_data(
    turbine_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    limit: int = Query(1000, gt=0, le=10000),
):
    # Fetch time series data from the database
    try:
        query = {}
        if turbine_id:
            query['turbine_id'] = turbine_id

        if start_date and end_date:
            query['timestamp'] = {
                '$gte': start_date,
                '$lte': end_date
            }
        elif start_date:
            query['timestamp'] = {'$gte': start_date}
        elif end_date:
            query['timestamp'] = {'$lte': end_date}

        cursor = mongo_connector.mongodb.db['time-series-data'].find(query).sort('timestamp', ASCENDING).limit(limit)
        results = await cursor.to_list(length=limit)

        # Convert the fetched data to TimeSeriesModel instances
        return [TimeSeriesModel(**data) for data in results]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
     

        

        