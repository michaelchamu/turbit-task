from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Dict

class TimeSeriesModel(BaseModel):
    timestamp: datetime = Field(..., description="Timestamp of the data point")
    power: float = Field(..., description="Power production in watts")
    wind_speed: float = Field(..., description="Wind speed in m/s")
    turbine_id: str = Field(..., description="Unique identifier for the turbine")
    metadata: Optional[Dict[str, float]] = Field(
        None, description="Additional data points related to the turbine"
    )