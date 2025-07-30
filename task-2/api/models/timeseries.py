from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict

class TurbineMetadata(BaseModel):
    turbine_id: str = Field(..., description="Unique identifier for the turbine")
    rpm: float = Field(..., description="Turbines rotations per minute")
    azimuth: float = Field(..., description="Degrees or angles the direction in which points the rotor hub or a spinner of the turbine")
    external_temperature: float = Field(..., description="Turbines recorded external temperature")
    internal_temperature: float = Field(..., description="Turbines recorded internal temperature")
    latitude: Optional[float] = Field(..., description="Latitude of the turbine location")
    longitude: Optional[float] = Field(..., description="Longitude of the turbine location")
    altitude: Optional[float] = Field(..., description="Altitude of the turbine location in meters")
class TimeSeriesModel(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the data point")
    power: float = Field(..., description="Power production in watts")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    metadata: TurbineMetadata = Field(..., description="Turbine metadata")

class AggregatedTimeSeriesModel(BaseModel):
    average_power: float = Field(..., description="Average power production in watts")
    average_wind_speed: float = Field(..., description="Average wind speed in m/s")
    average_azimuth: float = Field(..., description="Average azimuth angle")
    average_external_temperature: float = Field(..., description="Average external temps")
    averate_internal_temperature: float = Field(..., description="Average internal temps")