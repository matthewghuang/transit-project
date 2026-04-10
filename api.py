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

# In-memory GTFS lookups
stops_lookup: Dict[str, dict] = {}
routes_lookup: Dict[str, str] = {}
stop_times_lookup: Dict[str, list] = {}  # route_id -> route_short_name


def time_str_to_seconds(time_str):
    h, m, s = map(int, time_str.split(":"))
    return h * 3600 + m * 60 + s


def load_stop_times():
    global stop_times_lookup
    stop_times_path = os.getenv("GTFS_STOP_TIMES_PATH", "google_transit/stop_times.txt")
    try:
        with open(stop_times_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row["stop_id"].strip()
                if sid not in stop_times_lookup:
                    stop_times_lookup[sid] = []
                arr_str = row["arrival_time"].strip()
                try:
                    sec = time_str_to_seconds(arr_str)
                    stop_times_lookup[sid].append(
                        (sec, arr_str, row["trip_id"].strip())
                    )
                except:
                    pass
        for sid in stop_times_lookup:
            stop_times_lookup[sid].sort(key=lambda x: x[0])
        print(f"Loaded stop_times for {len(stop_times_lookup)} stops")
    except Exception as e:
        print(f"Warning: Could not load stop_times.txt: {e}")


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


def load_routes():
    """Load route names from GTFS static routes.txt into memory."""
    global routes_lookup
    routes_path = os.getenv("GTFS_ROUTES_PATH", "google_transit/routes.txt")
    try:
        with open(routes_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                routes_lookup[row["route_id"].strip()] = row["route_short_name"].strip()
        print(f"Loaded {len(routes_lookup)} routes from {routes_path}")
    except Exception as e:
        print(f"Warning: Could not load routes.txt: {e}")


@app.on_event("startup")
async def startup():
    global pool
    load_stops()
    load_routes()
    load_stop_times()
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
    routeName: str
    model_config = BASE_MODEL_CONFIG


# Main vehicle data object flattened to match active_vehicles schema
class VehicleUpdate(BaseModel):
    id: str
    trip: Trip
    position: Position
    timestamp: datetime.datetime
    model_config = BASE_MODEL_CONFIG


class NextBusesResponse(BaseModel):
    stop_id: str
    scheduled_time: Optional[str] = None
    actual_time: Optional[str] = None
    predicted_time: Optional[str] = None
    model_config = BASE_MODEL_CONFIG


class StopInfo(BaseModel):
    id: str
    name: str
    latitude: float
    longitude: float
    observation_count: int
    routes: List[str]
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
                route_id = row["route_id"]
                vehicles.append(
                    VehicleUpdate(
                        id=row["vehicle_id"],
                        trip=Trip(
                            tripId=row["trip_id"],
                            routeId=route_id,
                            routeName=routes_lookup.get(route_id, route_id),
                        ),
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
    description="Returns stops that have delay observations, enriched with GTFS metadata and route information.",
)
async def get_stops():
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    try:
        async with pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT stop_id, COUNT(*) as cnt, array_agg(DISTINCT route_id) as route_ids
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
                    # Map numeric route_ids to route_short_names
                    route_names = set()
                    if row["route_ids"]:
                        for rid in row["route_ids"]:
                            if rid:
                                route_names.add(routes_lookup.get(rid, rid))

                    stops.append(
                        StopInfo(
                            id=sid,
                            name=meta["name"],
                            latitude=meta["lat"],
                            longitude=meta["lon"],
                            observation_count=row["cnt"],
                            routes=list(route_names),
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


@app.get(
    "/api/stops/{stop_id}/next_buses",
    response_model=NextBusesResponse,
    summary="Get Next Bus Predicted Times",
    description="Returns scheduled, actual, and predicted times for the next bus.",
)
async def get_next_buses(stop_id: str):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    # 1. Find next scheduled bus
    now = datetime.datetime.now()
    now_sec = now.hour * 3600 + now.minute * 60 + now.second

    # If it's past midnight but before 3AM, consider it part of the previous day's >24h schedule
    if now.hour < 3:
        now_sec += 24 * 3600

    next_bus = None
    if stop_id in stop_times_lookup:
        for arr_sec, arr_str, trip_id in stop_times_lookup[stop_id]:
            if arr_sec >= now_sec:
                next_bus = (arr_sec, arr_str, trip_id)
                break

    if not next_bus:
        return NextBusesResponse(stop_id=stop_id)

    sched_sec, sched_str, trip_id = next_bus

    actual_str = None
    predicted_str = None

    try:
        async with pool.acquire() as conn:
            # 2. Get real-time delay for this trip
            # active_vehicles contains the current delay if we calculate it, or we just get updated_at?
            # Wait, delay is in delay_observations, or maybe not in active_vehicles.
            # Actually, active_vehicles has updated_at, latitude, longitude.
            # Wait, do we have real-time delay in active_vehicles?
            # Looking at the code: "SELECT vehicle_id, route_id, trip_id, latitude, longitude, updated_at FROM active_vehicles"
            # Maybe delay isn't stored there. But the prompt says "fetch its current real-time delay (from active_vehicles or realtime state)".
            # Let's check delay_observations for the most recent delay for this trip.

            row = await conn.fetchrow(
                "SELECT delay_seconds FROM delay_observations WHERE trip_id = $1 ORDER BY observed_at DESC LIMIT 1",
                trip_id,
            )
            current_delay = row["delay_seconds"] if row else 0

            if current_delay is not None:
                # Calculate actual time
                actual_sec = sched_sec + current_delay
                h = (actual_sec // 3600) % 24
                m = (actual_sec % 3600) // 60
                s = actual_sec % 60
                actual_str = f"{h:02d}:{m:02d}:{s:02d}"

            # 3. Calculate predicted time based on historical median
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            window_start = (now_utc - datetime.timedelta(hours=1)).time()
            window_end = (now_utc + datetime.timedelta(hours=1)).time()
            is_weekend = now_utc.weekday() >= 5
            day_type = "weekend" if is_weekend else "weekday"

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
            hist_rows = await conn.fetch(
                query, stop_id, window_start, window_end, day_type
            )
            if hist_rows:
                delays = [r["delay_seconds"] for r in hist_rows]
                median_delay = int(np.median(delays))
                pred_sec = sched_sec + median_delay
                ph = (pred_sec // 3600) % 24
                pm = (pred_sec % 3600) // 60
                ps = pred_sec % 60
                predicted_str = f"{ph:02d}:{pm:02d}:{ps:02d}"
            else:
                predicted_str = (
                    actual_str if actual_str else sched_str
                )  # fallback to actual or scheduled

    except Exception as e:
        print(f"Error calculating next buses: {e}")

    # Format scheduled_time cleanly
    sh = (sched_sec // 3600) % 24
    sm = (sched_sec % 3600) // 60
    ss = sched_sec % 60
    clean_sched_str = f"{sh:02d}:{sm:02d}:{ss:02d}"

    return NextBusesResponse(
        stop_id=stop_id,
        scheduled_time=clean_sched_str,
        actual_time=actual_str,
        predicted_time=predicted_str,
    )
