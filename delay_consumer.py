import time
from confluent_kafka import Consumer, KafkaError
from google.transit import gtfs_realtime_pb2
from dotenv import load_dotenv
import os
import pandas as pd
from pymongo import MongoClient
import pymongo
import datetime

load_dotenv()

# MongoDB configuration
MONGO_USER = os.getenv("MONGO_USER", "root")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD", "example")
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "delays")

if os.getenv("MONGO_CONNECTION_STRING"):
    MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
else:
    MONGO_CONNECTION_STRING = (
        f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/"
    )

schedule_cache = {}


def load_schedule():
    global schedule_cache
    print("Loading schedule from google_transit/stop_times.txt...")
    start_time = time.time()

    # Load stop_times.txt
    # We only need trip_id, stop_id, and arrival_time
    df = pd.read_csv(
        "google_transit/stop_times.txt",
        usecols=["trip_id", "stop_id", "arrival_time"],
        dtype={"trip_id": str, "stop_id": str},
    )

    # Convert arrival_time to seconds since start of day for easier calculation
    def time_to_seconds(time_str):
        try:
            h, m, s = map(int, time_str.strip().split(":"))
            return h * 3600 + m * 60 + s
        except:
            return None

    df["arrival_seconds"] = df["arrival_time"].apply(time_to_seconds)

    # Create lookup dictionary {(trip_id, stop_id): arrival_seconds}
    # Use trip_id as string because GTFS-R usually provides it as string
    schedule_cache = df.set_index(["trip_id", "stop_id"])["arrival_seconds"].to_dict()

    end_time = time.time()
    print(
        f"Loaded {len(schedule_cache)} schedule entries in {end_time - start_time:.2f}s"
    )


def get_seconds_since_start_of_day(ts):
    dt = datetime.datetime.fromtimestamp(ts)
    # Translink operates in Pacific Time. Assuming system time or Translink timestamp is correct.
    return dt.hour * 3600 + dt.minute * 60 + dt.second


def main():
    load_schedule()

    KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    kafka_config = {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": "delay-consumers",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(kafka_config)
    consumer.subscribe(["trip_updates"])

    client = MongoClient(MONGO_CONNECTION_STRING)
    database = client[MONGO_DB]
    collection = database["delay_observations"]

    # Index for queries
    collection.create_index([("stop_id", pymongo.ASCENDING)])
    collection.create_index([("timestamp", pymongo.DESCENDING)])

    print("Starting delay consumer loop...")
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

                if not feed_entity.HasField("trip_update"):
                    continue

                trip_update = feed_entity.trip_update
                trip_id = trip_update.trip.trip_id
                header_timestamp = (
                    trip_update.timestamp if trip_update.timestamp else int(time.time())
                )

                # D-04: Calculate lateness using header.timestamp as anchor if needed,
                # but usually delay is provided in stop_time_update.
                # D-03: "Strict Mode" - only record if stop_time_update is present.

                # Sort updates by stop_sequence to identify logical 'next' stop
                sorted_updates = sorted(
                    trip_update.stop_time_update, key=lambda x: x.stop_sequence
                )

                # Pick the first one as the 'next' stop (logical approximation for now)
                # In a more advanced implementation, we'd compare against current_stop_sequence
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

                    # If delay is not explicitly provided, calculate it if we have scheduled time
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
                        observation = {
                            "trip_id": trip_id,
                            "stop_id": stop_id,
                            "delay_seconds": delay_seconds,
                            "next_stop_id": stop_id,  # Persist explicitly as next_stop_id
                            "route_id": trip_update.trip.route_id,
                            "timestamp": datetime.datetime.fromtimestamp(
                                header_timestamp
                            ),
                            "created_at": datetime.datetime.now(datetime.UTC),
                        }

                        # We use trip_id + stop_id + timestamp as a unique key to avoid duplicates from re-polls
                        obs_id = f"{trip_id}:{stop_id}:{header_timestamp}"
                        collection.replace_one(
                            {"_id": obs_id}, observation, upsert=True
                        )

                        # print(f"Recorded delay: {trip_id} at {stop_id} = {delay_seconds}s")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    main()
