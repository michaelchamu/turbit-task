from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from pymongo import ASCENDING
import logging


from mongoconnector import mongo_connector
from ..models.timeseries import TimeSeriesModel, AggregatedTimeSeriesModel

route = APIRouter()
logger = logging.getLogger("task-2")

#This was the initial endpoint I envisioned, just keeping for posterity
#it simply pulled all data, unaggregated and showed timestamps etc
#overally, it wasnt a good way of showcasing timeseries data at 10min intervals
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
        #this adjustment allows for more flexible querying using a cursor from MongoDB
        cursor = mongo_connector.mongodb.db['time-series-data'].find(query).sort('timestamp', ASCENDING).limit(limit)
        results = await cursor.to_list(length=limit)
        #return with status code to make it easier client side to handle different actions
        #not adding status 200 because it will be returned in any case on success but must make distinction on 204(empty)
        if not results:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return results
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

#data is a lot and must be cleaned and summarised (aggregated and binned) to allow creating smoother graphs
#a simple model that returns a list with windspeed and power is used
#I have skipped including the date in the model, as the dates are only passed for querying
@route.get("/aggregated_timeseries", response_model=List[AggregatedTimeSeriesModel])
async def get_power_curve(
    start_date: Optional[datetime] = Query(None, description="Start date in YYYY-MM-DD"),
    end_date: Optional[datetime] = Query(None, description="End date in YYYY-MM-DD"),
    turbine_id: Optional[str] = None
):
   #by default, the start date is set to 01.01.2016 and the end date to 02.01.2016
   # default_start = datetime.strptime('01.01.2016, 00:00', '%d.%m.%Y, %H:%M')
   # default_end = datetime.strptime('02.01.2016, 00:00', '%d.%m.%Y, %H:%M')

    try:
        #check if start_date and end_date exist.
        #if dates dont exist i.e. its an API only call, set them to default values
        if not start_date or not end_date:
            start_date = datetime.strptime('01.01.2016, 00:00', '%d.%m.%Y, %H:%M')
            end_date = datetime.strptime('02.01.2016, 00:00', '%d.%m.%Y, %H:%M')
        if start_date >= end_date:
            raise ValueError("start_date must be earlier than end_date.")
    
        # Wind speed bins
        bin_size = 0.5
        min_wind = 0.0
        max_wind = 25.0
        boundaries = [round(min_wind + i * bin_size, 2) for i in range(int((max_wind - min_wind) / bin_size) + 1)]
        boundaries.append(max_wind + bin_size)

        match_stage = {"timestamp": {"$gte": start_date, "$lt": end_date}}
        if turbine_id:
            match_stage["metadata.turbine_id"] = turbine_id

        pipeline = [
            {"$match": match_stage},
            {
                "$bucket": {
                    "groupBy": "$wind_speed",
                    "boundaries": boundaries,
                    "default": "out_of_range",
                    "output": {
                        "average_power": {"$avg": "$power"},
                        "avg_wind_speed": {"$avg": "$wind_speed"},
                        "avg_azimuth": {"$avg": "$metadata.azimuth"},
                        "average_external_temperature": {"$avg": "$metadata.external_temperature" },
                        "average_internal_temperature": {"$avg": "$metadata.internal_temperature"},
                        "average_rpm": {"$avg": "$metadata.rpm"},
                        "count": {"$sum": 1}
                    }
                }
            },
            {"$match": {"_id": {"$ne": "out_of_range"}}},
            {"$sort": {"_id": 1}}
        ]

        results = []
        async for doc in mongo_connector.mongodb.db['time-series-data'].aggregate(pipeline):
            results.append(AggregatedTimeSeriesModel(
                average_wind_speed=round(doc["avg_wind_speed"], 2),
                average_power=round(doc["average_power"], 2),
                average_azimuth=round(doc["avg_azimuth"], 2),
                average_external_temperature=round(doc["average_external_temperature"], 2),
                average_internal_temperature=round(doc["average_internal_temperature"], 2),
                average_rpm = round(doc["average_rpm"], 2)
            ))
        if not results:
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        return results
    except Exception as ex:
        logger.error(str(ex))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")

#use this route to always fetch a fresh batch of turbin IDs from the database so that we populate the db
@route.get("/turbines", response_model=List[str])
async def get_list_turbines():
   
    try:
        turbinelist = await mongo_connector.mongodb.db['time-series-data'].distinct('metadata.turbine_id')
        #to avoid serialisation problems in tests and api calls etcexplicitly  convert result to list
        turbinelist = list(turbinelist)
        if not turbinelist:
            #here, to ensure client always knows resource is available but data is empty, we set status to 204
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        #if successful, 200 is implied anyway, so no need to return json response with specific status code
        return turbinelist 
    except Exception as e:
        logger.error(str(e))
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error")