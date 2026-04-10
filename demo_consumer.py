import time
import asyncio
import asyncpg
from confluent_kafka import Consumer, KafkaError
from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
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

route_id_to_name = {}


def map_route_to_name():
    global route_id_to_name
    try:

        def route_name(row):
            return f"{row['route_short_name']} {row['route_long_name']}"

        df = pd.read_csv("google_transit/routes.txt", sep=",")
        df["route_name"] = df.apply(route_name, axis=1)
        route_id_to_name = df.set_index("route_id")["route_name"].to_dict()
        print(f"Loaded {len(route_id_to_name)} route mappings.")
    except Exception as e:
        print(f"Error mapping routes: {e}")


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


async def delete_vehicle(conn, vehicle_id):
    try:
        await conn.execute(
            "DELETE FROM active_vehicles WHERE vehicle_id = $1", vehicle_id
        )
    except Exception as e:
        print(f"Error deleting vehicle {vehicle_id}: {e}")


async def main():
    map_route_to_name()

    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "position-consumers-sql",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(kafka_config)
    consumer.subscribe(["position"])

    print("Connecting to TimescaleDB...")
    conn = await asyncpg.connect(
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        database=POSTGRES_DB,
    )

    print("Starting position consumer loop (SQL-backed)...")
    try:
        while True:
            msg = consumer.poll(1.0)

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

                vehicle = feed_entity.vehicle
                vehicle_id = feed_entity.id
                trip_id = vehicle.trip.trip_id
                route_id = vehicle.trip.route_id
                lat = vehicle.position.latitude
                lon = vehicle.position.longitude
                updated_at = datetime.datetime.fromtimestamp(
                    float(vehicle.timestamp), datetime.timezone.utc
                )

                await upsert_vehicle(
                    conn, vehicle_id, route_id, trip_id, lat, lon, updated_at
                )
                # print(f"Updated vehicle: {vehicle_id}")
            else:
                # Note: GTFS-R feed entity deletions aren't always explicitly empty messages in Kafka,
                # but if they are, we handle it.
                if hasattr(msg, "key") and msg.key():
                    vid = msg.key().decode("utf-8")
                    await delete_vehicle(conn, vid)
                    print(f"Deleted vehicle: {vid}")

    except KeyboardInterrupt:
        print("Stopping consumer...")
    finally:
        await conn.close()
        consumer.close()


if __name__ == "__main__":
    asyncio.run(main())
