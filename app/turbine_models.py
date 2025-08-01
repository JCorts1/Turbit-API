from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TurbineReading(BaseModel):
    """
    Represents a single measurement from a turbine.
    Like a single row in our CSV file.
    """
    turbine_id: int = Field(..., description="Which turbine (1 or 2)")
    timestamp: datetime = Field(..., description="When the measurement was taken")
    wind_speed: float = Field(..., ge=0, description="Wind speed in m/s (must be >= 0)")
    power_output: float = Field(..., ge=0, description="Power output in kW (must be >= 0)")

    class Config:
        json_schema_extra = {
            "example": {
                "turbine_id": 1,
                "timestamp": "2024-01-01T10:00:00",
                "wind_speed": 5.5,
                "power_output": 175.0
            }
        }


class TurbineDataRequest(BaseModel):
    """
    What the user sends when requesting turbine data.
    """
    turbine_id: int = Field(..., description="Which turbine to get data for")
    start_time: Optional[datetime] = Field(None, description="Start of time range")
    end_time: Optional[datetime] = Field(None, description="End of time range")


class TurbineDataResponse(BaseModel):
    """
    What we send back to the user.
    """
    turbine_id: int
    reading_count: int
    start_time: datetime
    end_time: datetime
    readings: List[TurbineReading]


class PowerCurvePoint(BaseModel):
    """
    A single point on a power curve graph.
    """
    wind_speed: float
    average_power: float
    reading_count: int


class PowerCurveResponse(BaseModel):
    """
    Data for creating a power curve visualization.
    """
    turbine_id: int
    start_time: datetime
    end_time: datetime
    curve_points: List[PowerCurvePoint]
