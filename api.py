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
stop_code_to_id: Dict[str, str] = {}
id_to_stop_code: Dict[str, str] = {}
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
    global stops_lookup, stop_code_to_id, id_to_stop_code
    stops_path = os.getenv("GTFS_STOPS_PATH", "google_transit/stops.txt")
    try:
        with open(stops_path, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                sid = row["stop_id"].strip()
                code = row.get("stop_code", "").strip()
                stops_lookup[sid] = {
                    "name": row["stop_name"].strip(),
                    "lat": float(row["stop_lat"]),
                    "lon": float(row["stop_lon"]),
                }
                if code:
                    stop_code_to_id[code] = sid
                    id_to_stop_code[sid] = code
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
    arrive_by_time: Optional[str] = None  # ADV-01: 95th percentile recommendation
    confidence: float = 95.0
    low_confidence: bool = False
    is_stale: bool = False  # ADV-02: Ghost bus flag (no update in >5 min)
    last_updated: Optional[str] = None  # ADV-02: Last real-time update timestamp
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
    p05: Optional[float] = None  # ADV-01: 5th percentile (minutes)
    p95: Optional[float] = None  # ADV-01: 95th percentile (minutes)
    confidence: float = 95.0
    low_confidence: bool = False
    observation_count: int = 0
    buckets: List[HistogramBucket]
    model_config = BASE_MODEL_CONFIG


def snap_percentile(p: float) -> float:
    """Snaps input percentile to the nearest discrete step: 50, 75, 90, 95, 99."""
    steps = [50.0, 75.0, 90.0, 95.0, 99.0]
    return min(steps, key=lambda x: abs(x - p))


@app.get(
    "/api/stops/search",
    response_model=List[StopInfo],
    summary="Search for Stops",
    description="Fuzzy search for stops by name, exact search by stop_id, or search by route name.",
)
async def search_stops(q: str = Query(..., min_length=1)):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    try:
        async with pool.acquire() as conn:
            # Set similarity threshold for fuzzy search
            await conn.execute("SELECT set_limit(0.1);")

            # Check if q is a 5-digit number (common stop_id format)
            is_numeric = q.isdigit() and (len(q) >= 4 and len(q) <= 6)

            # Check if q matches any route_short_name
            matching_route_ids = [
                rid
                for rid, rname in routes_lookup.items()
                if q.lower() == rname.lower()
            ]

            if is_numeric:
                # Priority 1: Exact stop_id or stop_code match
                # Priority 2: Fuzzy name match
                rows = await conn.fetch(
                    """
                    SELECT s.stop_id, s.stop_code, s.stop_name, s.stop_lat, s.stop_lon, 
                           COALESCE(obs.cnt, 0) as observation_count,
                           COALESCE(obs.route_ids, '{}') as route_ids
                    FROM stops s
                    LEFT JOIN (
                        SELECT stop_id, COUNT(*) as cnt, array_agg(DISTINCT route_id) as route_ids
                        FROM delay_observations
                        GROUP BY stop_id
                    ) obs ON s.stop_id = obs.stop_id
                    WHERE s.stop_id = $1 OR s.stop_code = $1 OR s.stop_name % $1
                    ORDER BY (s.stop_id = $1 OR s.stop_code = $1) DESC, similarity(s.stop_name, $1) DESC
                    LIMIT 20
                    """,
                    q,
                )
            elif matching_route_ids:
                # Search by route: find stops that have observations for this route
                rows = await conn.fetch(
                    """
                    SELECT s.stop_id, s.stop_code, s.stop_name, s.stop_lat, s.stop_lon, 
                           COALESCE(obs.cnt, 0) as observation_count,
                           COALESCE(obs.route_ids, '{}') as route_ids
                    FROM stops s
                    JOIN (
                        SELECT stop_id, COUNT(*) as cnt, array_agg(DISTINCT route_id) as route_ids
                        FROM delay_observations
                        WHERE route_id = ANY($1)
                        GROUP BY stop_id
                    ) obs ON s.stop_id = obs.stop_id
                    ORDER BY obs.cnt DESC
                    LIMIT 20
                    """,
                    matching_route_ids,
                )
            else:
                # Fuzzy name match
                rows = await conn.fetch(
                    """
                    SELECT s.stop_id, s.stop_code, s.stop_name, s.stop_lat, s.stop_lon, 
                           COALESCE(obs.cnt, 0) as observation_count,
                           COALESCE(obs.route_ids, '{}') as route_ids
                    FROM stops s
                    LEFT JOIN (
                        SELECT stop_id, COUNT(*) as cnt, array_agg(DISTINCT route_id) as route_ids
                        FROM delay_observations
                        GROUP BY stop_id
                    ) obs ON s.stop_id = obs.stop_id
                    WHERE s.stop_name % $1
                    ORDER BY similarity(s.stop_name, $1) DESC
                    LIMIT 20
                    """,
                    q,
                )

            stops = []
            for row in rows:
                sid = row["stop_id"]
                scode = row["stop_code"]
                # Fallback to in-memory lookup if DB stop_code is NULL
                if not scode:
                    scode = id_to_stop_code.get(sid)
                # Map numeric route_ids to route_short_names
                route_names = set()
                if row["route_ids"]:
                    for rid in row["route_ids"]:
                        if rid:
                            route_names.add(routes_lookup.get(rid, rid))

                stops.append(
                    StopInfo(
                        id=scode if scode else sid,
                        name=row["stop_name"],
                        latitude=row["stop_lat"],
                        longitude=row["stop_lon"],
                        observation_count=row["observation_count"],
                        routes=list(route_names),
                    )
                )
            return stops
    except Exception as e:
        print(f"Error searching stops: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while searching stops: {e}",
        )


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

                    scode = id_to_stop_code.get(sid)
                    stops.append(
                        StopInfo(
                            id=scode if scode else sid,
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
async def get_delay_distribution(
    stop_id: str,
    confidence: float = Query(
        95.0, description="Confidence percentile (50, 75, 90, 95, 99)"
    ),
):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    input_id = stop_id
    # Resolve stop_code to stop_id if necessary
    if stop_id in stop_code_to_id:
        stop_id = stop_code_to_id[stop_id]

    snapped_conf = snap_percentile(confidence)
    # TimescaleDB approx_percentile uses 0-1 scale
    target_p = snapped_conf / 100.0

    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        # 2-hour window centered on current time (1 hour before, 1 hour after)
        window_start = (now - datetime.timedelta(hours=1)).time()
        window_end = (now + datetime.timedelta(hours=1)).time()

        is_weekend = now.weekday() >= 5
        day_type = "weekend" if is_weekend else "weekday"

        async with pool.acquire() as conn:
            # D-03: Use approximate aggregates if available, otherwise exact sorting
            # We use PERCENTILE_CONT (exact) since percentile_agg is missing in the environment
            stats_query = """
                WITH data AS (
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
                )
                SELECT 
                    COUNT(*) as obs_count,
                    percentile_cont(0.5) WITHIN GROUP (ORDER BY delay_seconds) as median,
                    percentile_cont(0.05) WITHIN GROUP (ORDER BY delay_seconds) as p05,
                    percentile_cont($5) WITHIN GROUP (ORDER BY delay_seconds) as pn
                FROM data
            """
            stats = await conn.fetchrow(
                stats_query, stop_id, window_start, window_end, day_type, target_p
            )

            obs_count = stats["obs_count"] if stats else 0
            if obs_count == 0:
                return DistributionResponse(
                    stop_id=input_id, median=0.0, confidence=snapped_conf, buckets=[]
                )

            median_minutes = float((stats["median"] or 0) / 60.0)
            p05_minutes = float((stats["p05"] or 0) / 60.0)
            pn_minutes = float((stats["pn"] or 0) / 60.0)
            low_confidence = obs_count < 10

            # Histogram buckets (still using DB for raw data for now, but in-DB histogram is an option)
            rows = await conn.fetch(
                """
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
                """,
                stop_id,
                window_start,
                window_end,
                day_type,
            )

            delays = np.array([row["delay_seconds"] for row in rows])
            bins = np.arange(-10, 31, 1)
            counts, bin_edges = np.histogram(delays / 60.0, bins=bins)

            buckets = []
            for count, edge in zip(counts, bin_edges[:-1]):
                if count > 0:
                    buckets.append(HistogramBucket(minute=int(edge), count=int(count)))

            return DistributionResponse(
                stop_id=input_id,
                median=median_minutes,
                p05=p05_minutes,
                p95=pn_minutes,  # We reuse p95 field for the requested percentile
                confidence=snapped_conf,
                low_confidence=low_confidence,
                observation_count=obs_count,
                buckets=buckets,
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
async def get_next_buses(
    stop_id: str,
    confidence: float = Query(
        95.0, description="Confidence percentile (50, 75, 90, 95, 99)"
    ),
):
    if pool is None:
        raise HTTPException(status_code=500, detail="Database pool not initialized")

    input_id = stop_id
    # Resolve stop_code to stop_id if necessary
    if stop_id in stop_code_to_id:
        stop_id = stop_code_to_id[stop_id]

    snapped_conf = snap_percentile(confidence)
    target_p = snapped_conf / 100.0

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
        return NextBusesResponse(stop_id=input_id, confidence=snapped_conf)

    sched_sec, sched_str, trip_id = next_bus

    actual_str = None
    predicted_str = None
    arrive_by_str = None
    is_stale = False
    last_updated_str = None
    low_confidence = False

    try:
        async with pool.acquire() as conn:
            # 2. Get real-time delay for this trip + staleness check (ADV-02)
            row = await conn.fetchrow(
                "SELECT delay_seconds, updated_at FROM trip_delays WHERE trip_id = $1",
                trip_id,
            )
            current_delay = row["delay_seconds"] if row else None

            if row and row["updated_at"]:
                last_updated = row["updated_at"]
                last_updated_str = last_updated.strftime("%H:%M:%S")
                # ADV-02: Ghost bus detection — stale if no update in >5 minutes
                now_utc = datetime.datetime.now(datetime.timezone.utc)
                age = (now_utc - last_updated).total_seconds()
                if age > 300:  # 5 minutes
                    is_stale = True

            if current_delay is not None:
                # Calculate actual time
                actual_sec = sched_sec + current_delay
                h = (actual_sec // 3600) % 24
                m = (actual_sec % 3600) // 60
                s = actual_sec % 60
                actual_str = f"{h:02d}:{m:02d}:{s:02d}"

            # 3. Calculate predicted time based on historical median + dynamic confidence arrive_by
            now_utc = datetime.datetime.now(datetime.timezone.utc)
            window_start = (now_utc - datetime.timedelta(hours=1)).time()
            window_end = (now_utc + datetime.timedelta(hours=1)).time()
            is_weekend = now_utc.weekday() >= 5
            day_type = "weekend" if is_weekend else "weekday"

            # D-03: Use approximate aggregates if available, otherwise exact sorting
            # We use PERCENTILE_CONT (exact) since percentile_agg is missing in the environment
            stats_query = """
                WITH data AS (
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
                )
                SELECT 
                    COUNT(*) as obs_count,
                    percentile_cont(0.5) WITHIN GROUP (ORDER BY delay_seconds) as median,
                    percentile_cont($5) WITHIN GROUP (ORDER BY delay_seconds) as pn
                FROM data
            """
            stats = await conn.fetchrow(
                stats_query, stop_id, window_start, window_end, day_type, target_p
            )

            if stats and stats["obs_count"] > 0:
                obs_count = stats["obs_count"]
                low_confidence = obs_count < 10

                median_delay = int(stats["median"] or 0)
                pred_sec = sched_sec + median_delay
                ph = (pred_sec // 3600) % 24
                pm = (pred_sec % 3600) // 60
                ps = pred_sec % 60
                predicted_str = f"{ph:02d}:{pm:02d}:{ps:02d}"

                # ADV-01: Dynamic "Arrive By" recommendation
                # D-05: Safety cap - arrive_by_sec = min(sched_sec, sched_sec + percentile_delay_sec)
                pn_delay = int(stats["pn"] or 0)
                arrive_by_sec = min(sched_sec, sched_sec + pn_delay)
                ah = (arrive_by_sec // 3600) % 24
                am = (arrive_by_sec % 3600) // 60
                asec = arrive_by_sec % 60
                arrive_by_str = f"{ah:02d}:{am:02d}:{asec:02d}"

    except Exception as e:
        print(f"Error calculating next buses: {e}")

    # Format scheduled_time cleanly
    sh = (sched_sec // 3600) % 24
    sm = (sched_sec % 3600) // 60
    ss = sched_sec % 60
    clean_sched_str = f"{sh:02d}:{sm:02d}:{ss:02d}"

    return NextBusesResponse(
        stop_id=input_id,
        scheduled_time=clean_sched_str,
        actual_time=actual_str,
        predicted_time=predicted_str,
        arrive_by_time=arrive_by_str,
        confidence=snapped_conf,
        low_confidence=low_confidence,
        is_stale=is_stale,
        last_updated=last_updated_str,
    )
