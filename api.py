from fastapi import FastAPI, HTTPException, status
from pydantic import ConfigDict, BaseModel
import os
from dotenv import load_dotenv
from typing import Optional, List
import datetime
import asyncpg

app = FastAPI(title="Realtime Transit Dashboard API")

load_dotenv()

# TimescaleDB configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "transit")

pool = None


@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )


@app.on_event("shutdown")
async def shutdown():
    await pool.close()


BASE_MODEL_CONFIG = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
)


# Position object
class Position(BaseModel):
    latitude: float
    longitude: float
    model_config = BASE_MODEL_CONFIG


# Simplified Trip object for flattened SQL results
class Trip(BaseModel):
    tripId: str
    routeId: str
    model_config = BASE_MODEL_CONFIG


# Main vehicle data object flattened to match active_vehicles schema
class VehicleUpdate(BaseModel):
    id: str
    trip: Trip
    position: Position
    timestamp: datetime.datetime
    model_config = BASE_MODEL_CONFIG


@app.get(
    "/api/vehicles/",
    response_model=List[VehicleUpdate],
    summary="Get All Vehicle Positions",
    description="Retrieves current vehicle positions from TimescaleDB.",
)
async def get_all_vehicles():
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                "SELECT vehicle_id, route_id, trip_id, latitude, longitude, updated_at FROM active_vehicles"
            )

            vehicles = []
            for row in rows:
                vehicles.append(
                    VehicleUpdate(
                        id=row["vehicle_id"],
                        trip=Trip(tripId=row["trip_id"], routeId=row["route_id"]),
                        position=Position(
                            latitude=row["latitude"], longitude=row["longitude"]
                        ),
                        timestamp=row["updated_at"],
                    )
                )

            return vehicles
    except Exception as e:
        print(f"Error fetching vehicles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching vehicle data: {e}",
        )
