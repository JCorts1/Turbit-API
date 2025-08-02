from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from app.database import db
from app.turbine_models import (
    TurbineReading,
    TurbineDataResponse,
    PowerCurveResponse,
    PowerCurvePoint
)

# Create a router - like a mini-app for turbine endpoints
router = APIRouter(
    prefix="/turbines",
    tags=["Turbines"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=dict)
async def get_turbine_info():
    """
    Get information about available turbines.

    Like asking: "What turbines do you have data for?"
    """
    # Count readings for each turbine
    turbine_1_count = await db.database.turbines.count_documents({"turbine_id": 1})
    turbine_2_count = await db.database.turbines.count_documents({"turbine_id": 2})

    return {
        "turbines": [
            {"id": 1, "name": "Turbine 1", "reading_count": turbine_1_count},
            {"id": 2, "name": "Turbine 2", "reading_count": turbine_2_count}
        ]
    }


@router.get("/{turbine_id}/data", response_model=TurbineDataResponse)
async def get_turbine_data(
    turbine_id: int,
    start_time: Optional[datetime] = Query(None, description="Start time for filtering"),
    end_time: Optional[datetime] = Query(None, description="End time for filtering"),
    limit: int = Query(1000, ge=1, le=10000, description="Maximum number of readings")
):
    """
    Get raw time series data for a specific turbine.

    Like asking: "Show me all measurements from Turbine 1 between January and February"

    Args:
        turbine_id: Which turbine (1 or 2)
        start_time: Only get data after this time
        end_time: Only get data before this time
        limit: Maximum number of readings to return
    """
    # Build the query
    query = {"turbine_id": turbine_id}

    # Add time filters if provided
    if start_time or end_time:
        query["timestamp"] = {}
        if start_time:
            query["timestamp"]["$gte"] = start_time
        if end_time:
            query["timestamp"]["$lte"] = end_time

    # Get readings from database
    readings = []
    cursor = db.database.turbines.find(query).sort("timestamp", 1).limit(limit)

    async for doc in cursor:
        # Remove MongoDB's internal _id field
        doc.pop('_id', None)
        readings.append(TurbineReading(**doc))

    if not readings:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for turbine {turbine_id}"
        )

    # Create response
    return TurbineDataResponse(
        turbine_id=turbine_id,
        reading_count=len(readings),
        start_time=readings[0].timestamp,
        end_time=readings[-1].timestamp,
        readings=readings
    )


@router.get("/{turbine_id}/power-curve", response_model=PowerCurveResponse)
async def get_power_curve(
    turbine_id: int,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None),
    wind_speed_interval: float = Query(0.5, description="Wind speed grouping interval")
):
    """
    Get power curve data (average power vs wind speed).

    A power curve shows the relationship between wind speed and power output.
    This helps identify if a turbine is performing well.

    Args:
        turbine_id: Which turbine
        start_time: Start of time range
        end_time: End of time range
        wind_speed_interval: Group wind speeds by this interval (e.g., 0.5 m/s)
    """
    # Build aggregation pipeline
    # This is like a series of data processing steps
    pipeline = [
        # Step 1: Filter by turbine and time
        {
            "$match": {
                "turbine_id": turbine_id,
                **({"timestamp": {"$gte": start_time, "$lte": end_time}}
                   if start_time and end_time else {})
            }
        },
        # Step 2: Group by wind speed intervals
        {
            "$group": {
                "_id": {
                    "$multiply": [
                        {"$floor": {"$divide": ["$wind_speed", wind_speed_interval]}},
                        wind_speed_interval
                    ]
                },
                "average_power": {"$avg": "$power_output"},
                "reading_count": {"$sum": 1},
                "min_time": {"$min": "$timestamp"},
                "max_time": {"$max": "$timestamp"}
            }
        },
        # Step 3: Sort by wind speed
        {
            "$sort": {"_id": 1}
        }
    ]

    # Execute aggregation
    curve_points = []
    min_time = None
    max_time = None

    async for doc in db.database.turbines.aggregate(pipeline):
        curve_points.append(PowerCurvePoint(
            wind_speed=doc["_id"],
            average_power=round(doc["average_power"], 2),
            reading_count=doc["reading_count"]
        ))

        if not min_time or doc["min_time"] < min_time:
            min_time = doc["min_time"]
        if not max_time or doc["max_time"] > max_time:
            max_time = doc["max_time"]

    if not curve_points:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for turbine {turbine_id}"
        )

    return PowerCurveResponse(
        turbine_id=turbine_id,
        start_time=min_time,
        end_time=max_time,
        curve_points=curve_points
    )


@router.get("/{turbine_id}/statistics", response_model=dict)
async def get_turbine_statistics(
    turbine_id: int,
    start_time: Optional[datetime] = Query(None),
    end_time: Optional[datetime] = Query(None)
):
    """
    Get statistical summary for a turbine.

    Like asking: "What's the average wind speed and power output for this turbine?"
    """
    # Build query
    query = {"turbine_id": turbine_id}
    if start_time or end_time:
        query["timestamp"] = {}
        if start_time:
            query["timestamp"]["$gte"] = start_time
        if end_time:
            query["timestamp"]["$lte"] = end_time

    # Aggregation to calculate statistics
    pipeline = [
        {"$match": query},
        {
            "$group": {
                "_id": None,
                "count": {"$sum": 1},
                "avg_wind_speed": {"$avg": "$wind_speed"},
                "min_wind_speed": {"$min": "$wind_speed"},
                "max_wind_speed": {"$max": "$wind_speed"},
                "avg_power": {"$avg": "$power_output"},
                "min_power": {"$min": "$power_output"},
                "max_power": {"$max": "$power_output"},
                "total_energy": {"$sum": "$power_output"}  # Simplified energy calculation
            }
        }
    ]

    stats = await db.database.turbines.aggregate(pipeline).to_list(1)

    if not stats:
        raise HTTPException(
            status_code=404,
            detail=f"No data found for turbine {turbine_id}"
        )

    result = stats[0]
    result.pop('_id', None)

    # Round numbers for readability
    for key in ['avg_wind_speed', 'avg_power', 'total_energy']:
        if key in result:
            result[key] = round(result[key], 2)

    result['turbine_id'] = turbine_id

    return result
