import time
import asyncio
import asyncpg
from confluent_kafka import Consumer, KafkaError
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import pandas as pd
import datetime

load_dotenv()

# TimescaleDB configuration
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "transit")

schedule_cache = {}
observation_buffer = []
LAST_FLUSH_TIME = time.time()
FLUSH_INTERVAL = 10  # seconds
BATCH_SIZE = 100


def load_schedule():
    global schedule_cache
    print("Loading schedule from google_transit/stop_times.txt...")
    start_time = time.time()
    try:
        df = pd.read_csv(
            "google_transit/stop_times.txt",
            usecols=["trip_id", "stop_id", "arrival_time"],
            dtype={"trip_id": str, "stop_id": str},
        )

        def time_to_seconds(time_str):
            try:
                h, m, s = map(int, time_str.strip().split(":"))
                return h * 3600 + m * 60 + s
            except:
                return None

        df["arrival_seconds"] = df["arrival_time"].apply(time_to_seconds)
        schedule_cache = df.set_index(["trip_id", "stop_id"])[
            "arrival_seconds"
        ].to_dict()
        end_time = time.time()
        print(
            f"Loaded {len(schedule_cache)} schedule entries in {end_time - start_time:.2f}s"
        )
    except Exception as e:
        print(f"Error loading schedule: {e}")


def get_seconds_since_start_of_day(ts):
    dt = datetime.datetime.fromtimestamp(ts, datetime.timezone.utc)
    return dt.hour * 3600 + dt.minute * 60 + dt.second


async def flush_observations(conn):
    global observation_buffer, LAST_FLUSH_TIME
    if not observation_buffer:
        return

    print(f"Flushing {len(observation_buffer)} observations to TimescaleDB...")
    try:
        # observation_buffer contains tuples: (observed_at, stop_id, route_id, trip_id, delay_seconds)
        await conn.copy_records_to_table(
            "delay_observations",
            records=observation_buffer,
            columns=["observed_at", "stop_id", "route_id", "trip_id", "delay_seconds"],
        )
        observation_buffer = []
        LAST_FLUSH_TIME = time.time()
    except Exception as e:
        print(f"Error flushing observations: {e}")


async def upsert_vehicle(conn, vehicle_id, route_id, trip_id, lat, lon, updated_at):
    try:
        await conn.execute(
            """
            INSERT INTO active_vehicles (vehicle_id, route_id, trip_id, latitude, longitude, updated_at)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (vehicle_id) DO UPDATE SET
                route_id = EXCLUDED.route_id,
                trip_id = EXCLUDED.trip_id,
                latitude = EXCLUDED.latitude,
                longitude = EXCLUDED.longitude,
                updated_at = EXCLUDED.updated_at;
        """,
            vehicle_id,
            route_id,
            trip_id,
            lat,
            lon,
            updated_at,
        )
    except Exception as e:
        print(f"Error upserting vehicle {vehicle_id}: {e}")


async def upsert_trip_delay(
    conn, trip_id, route_id, delay_seconds, last_stop_id, updated_at
):
    try:
        await conn.execute(
            """
            INSERT INTO trip_delays (trip_id, route_id, delay_seconds, last_stop_id, updated_at)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (trip_id) DO UPDATE SET
                delay_seconds = EXCLUDED.delay_seconds,
                last_stop_id = EXCLUDED.last_stop_id,
                updated_at = EXCLUDED.updated_at;
        """,
            trip_id,
            route_id,
            delay_seconds,
            last_stop_id,
            updated_at,
        )
    except Exception as e:
        print(f"Error upserting trip delay for {trip_id}: {e}")


# ADV-03: Track seen cancellations to avoid duplicate inserts
seen_cancellations = set()


async def log_trip_cancellation(conn, trip_id, route_id, observed_at):
    """ADV-03: Log a trip cancellation to the database."""
    if trip_id in seen_cancellations:
        return
    seen_cancellations.add(trip_id)
    try:
        await conn.execute(
            """
            INSERT INTO trip_cancellations (observed_at, trip_id, route_id, schedule_date)
            VALUES ($1, $2, $3, $4)
        """,
            observed_at,
            trip_id,
            route_id,
            observed_at.date(),
        )
        print(f"Logged cancellation: trip={trip_id}, route={route_id}")
    except Exception as e:
        print(f"Error logging cancellation for {trip_id}: {e}")


async def main():
    global observation_buffer
    load_schedule()

    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "delay-consumers-sql",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(kafka_config)
    consumer.subscribe(["trip_updates"])

    print("Connecting to TimescaleDB...")
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )

    print("Starting delay consumer loop (SQL-backed)...")
    try:
        while True:
            msg = consumer.poll(0.1)

            # Check if we need to flush observations
            if (
                len(observation_buffer) >= BATCH_SIZE
                or (time.time() - LAST_FLUSH_TIME) >= FLUSH_INTERVAL
            ):
                await flush_observations(conn)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(f"Kafka Error: {msg.error()}")
                    continue

            feed_entity = gtfs_realtime_pb2.FeedEntity()
            if msg.value() is not None:
                feed_entity.ParseFromString(msg.value())

                if not feed_entity.HasField("trip_update"):
                    continue

                trip_update = feed_entity.trip_update
                trip_id = trip_update.trip.trip_id
                route_id = trip_update.trip.route_id
                header_timestamp = datetime.datetime.fromtimestamp(
                    trip_update.timestamp
                    if trip_update.timestamp
                    else int(time.time()),
                    datetime.timezone.utc,
                )

                # ADV-03: Detect canceled trips (schedule_relationship == CANCELED == 3)
                if trip_update.trip.schedule_relationship == 3:
                    await log_trip_cancellation(
                        conn, trip_id, route_id, header_timestamp
                    )
                    continue

                sorted_updates = sorted(
                    trip_update.stop_time_update, key=lambda x: x.stop_sequence
                )

                if sorted_updates:
                    next_stu = sorted_updates[0]
                    stop_id = next_stu.stop_id

                    delay_seconds = None
                    if next_stu.HasField("arrival") and next_stu.arrival.HasField(
                        "delay"
                    ):
                        delay_seconds = next_stu.arrival.delay
                    elif next_stu.HasField("departure") and next_stu.departure.HasField(
                        "delay"
                    ):
                        delay_seconds = next_stu.departure.delay

                    if delay_seconds is None and (trip_id, stop_id) in schedule_cache:
                        scheduled_seconds = schedule_cache[(trip_id, stop_id)]
                        if next_stu.HasField("arrival") and next_stu.arrival.time:
                            actual_seconds = get_seconds_since_start_of_day(
                                next_stu.arrival.time
                            )
                            delay_seconds = actual_seconds - scheduled_seconds
                        elif next_stu.HasField("departure") and next_stu.departure.time:
                            actual_seconds = get_seconds_since_start_of_day(
                                next_stu.departure.time
                            )
                            delay_seconds = actual_seconds - scheduled_seconds

                    if delay_seconds is not None:
                        observation_buffer.append(
                            (
                                header_timestamp,
                                stop_id,
                                route_id,
                                trip_id,
                                delay_seconds,
                            )
                        )
                        # Also upsert latest trip delay state
                        await upsert_trip_delay(
                            conn,
                            trip_id,
                            route_id,
                            delay_seconds,
                            stop_id,
                            header_timestamp,
                        )

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        await flush_observations(conn)
        await conn.close()
        consumer.close()


if __name__ == "__main__":
    asyncio.run(main())
