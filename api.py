from fastapi import FastAPI, HTTPException, Query, status
from pydantic import ConfigDict, BaseModel
import os
import csv
from dotenv import load_dotenv
from typing import Optional, List, Dict
import datetime
import asyncpg
import numpy as np


app = FastAPI(title="Realtime Transit Dashboard API")

load_dotenv()

# TimescaleDB configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "transit")

pool = None

# In-memory GTFS stops lookup: stop_id -> {name, lat, lon}
stops_lookup: Dict[str, dict] = {}


def load_stops():
    """Load stop metadata from GTFS static stops.txt into memory."""
    global stops_lookup
    stops_path = os.getenv("GTFS_STOPS_PATH", "google_transit/stops.txt")
    try:
        with open(stops_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                stops_lookup[row["stop_id"].strip()] = {
                    "name": row["stop_name"].strip(),
                    "lat": float(row["stop_lat"]),
                    "lon": float(row["stop_lon"]),
                }
        print(f"Loaded {len(stops_lookup)} stops from {stops_path}")
    except Exception as e:
        print(f"Warning: Could not load stops.txt: {e}")


@app.on_event("startup")
async def startup():
    global pool
    load_stops()
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


class StopInfo(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    observation_count: int
    model_config = BASE_MODEL_CONFIG


class HistogramBucket(BaseModel):
    minute: int
    count: int
    model_config = BASE_MODEL_CONFIG


class DistributionResponse(BaseModel):
    stop_id: str
    median: float
    buckets: List[HistogramBucket]
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


@app.get(
    "/api/stops",
    response_model=List[StopInfo],
    summary="Get Stops With Delay Data",
    description="Returns stops that have delay observations, enriched with GTFS metadata.",
)
async def get_stops():
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT stop_id, COUNT(*) as cnt
                FROM delay_observations
                GROUP BY stop_id
                ORDER BY cnt DESC
                """
            )

            stops = []
            for row in rows:
                sid = row["stop_id"]
                meta = stops_lookup.get(sid)
                if meta:
                    stops.append(
                        StopInfo(
                            id=sid,
                            name=meta["name"],
                            latitude=meta["lat"],
                            longitude=meta["lon"],
                            observation_count=row["cnt"],
                        )
                    )
            return stops
    except Exception as e:
        print(f"Error fetching stops: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching stops: {e}",
        )


@app.get(
    "/api/distribution/{stop_id}",
    response_model=DistributionResponse,
    summary="Get Delay Distribution for a Stop",
    description="Calculates delay distribution histogram and median for a 2-hour window around current time.",
)
async def get_delay_distribution(stop_id: str):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        # 2-hour window centered on current time (1 hour before, 1 hour after)
        # Note: In a real system we might adjust this to be 'time of day' independent of date
        window_start = (now - datetime.timedelta(hours=1)).time()
        window_end = (now + datetime.timedelta(hours=1)).time()

        is_weekend = now.weekday() >= 5
        day_type = "weekend" if is_weekend else "weekday"

        async with pool.acquire() as conn:
            # We filter by time of day (ignoring the date part for historical patterns)
            # and by weekday/weekend
            query = """
                SELECT delay_seconds 
                FROM delay_observations 
                WHERE stop_id = $1 
                AND observed_at::time >= $2 
                AND observed_at::time <= $3
                AND (
                    ($4 = 'weekend' AND EXTRACT(DOW FROM observed_at) IN (0, 6))
                    OR
                    ($4 = 'weekday' AND EXTRACT(DOW FROM observed_at) IN (1, 2, 3, 4, 5))
                )
            """
            rows = await conn.fetch(query, stop_id, window_start, window_end, day_type)

            if not rows:
                # Fallback to all data if window is empty, or return empty distribution
                return DistributionResponse(stop_id=stop_id, median=0.0, buckets=[])

            delays = np.array([row["delay_seconds"] for row in rows])

            # Median in minutes
            median_minutes = float(np.median(delays) / 60.0)

            # Histogram buckets (1-minute intervals)
            # Delays typically range from -5m to +20m
            # We'll bucket everything between -10 and 30 minutes
            bins = np.arange(-10, 31, 1)
            counts, bin_edges = np.histogram(delays / 60.0, bins=bins)

            buckets = []
            for count, edge in zip(counts, bin_edges[:-1]):
                if count > 0:  # Only return non-empty buckets to save bandwidth
                    buckets.append(HistogramBucket(minute=int(edge), count=int(count)))

            return DistributionResponse(
                stop_id=stop_id, median=median_minutes, buckets=buckets
            )

    except Exception as e:
        print(f"Error calculating distribution: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while calculating delay distribution: {e}",
        )
