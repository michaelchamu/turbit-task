from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict

class TurbineMetadata(BaseModel):
    turbine_id: str = Field(..., description="Unique identifier for the turbine")
    latitude: Optional[float] = Field(..., description="Latitude of the turbine location")
    longitude: Optional[float] = Field(..., description="Longitude of the turbine location")
    altitude: Optional[float] = Field(..., description="Altitude of the turbine location in meters")
class TimeSeriesModel(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the data point")
    power: float = Field(..., description="Power production in watts")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    metadata: TurbineMetadata = Field(..., description="Turbine metadata")