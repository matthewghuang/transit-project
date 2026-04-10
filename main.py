from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
import requests
from dotenv import load_dotenv
import os
from confluent_kafka import Producer
import time
import json

load_dotenv()

realtime_url = (
    f"https://gtfsapi.translink.ca/v3/gtfsrealtime?apikey={os.getenv('API_KEY')}"
)
position_url = (
    f"https://gtfsapi.translink.ca/v3/gtfsposition?apikey={os.getenv('API_KEY')}"
)

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

kafka_config = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}

# This cache will store the binary data of the entity we've seen
# Key: entity.id, Value: entity.SerializeToString()
entity_cache = {}

producer = Producer(kafka_config)
POSITION_TOPIC = "position"
TRIP_UPDATES_TOPIC = "trip_updates"

cache = {}

first_poll = True


def poll_endpoint(url, topic):
    global first_poll
    global cache

    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(url)
        response.raise_for_status()  # Check for HTTP errors
        feed.ParseFromString(response.content)
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error polling {url}: {e}")
        return 0, 0
    except Exception as e:
        print(f"Feed parse error polling {url}: {e}")
        return 0, 0

    updated_count = 0

    for entity in feed.entity:
        if not entity.id:
            continue  # Ignore entities without an ID

        serialized = entity.SerializeToString()

        # Use a composite key for cache to avoid collisions between topics if IDs overlap
        cache_key = f"{topic}:{entity.id}"

        # if first poll send everything
        if first_poll:
            producer.produce(topic, key=entity.id, value=serialized)
            cache[cache_key] = serialized
        else:
            # new thing or updated
            if cache_key not in cache or cache[cache_key] != serialized:
                producer.produce(topic, key=entity.id, value=serialized)
                cache[cache_key] = serialized
                updated_count = updated_count + 1

    return updated_count, len(feed.entity)


def poll():
    global first_poll

    pos_updated, pos_total = poll_endpoint(position_url, POSITION_TOPIC)
    rt_updated, rt_total = poll_endpoint(realtime_url, TRIP_UPDATES_TOPIC)

    print(
        f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] position: updated={pos_updated}, total={pos_total} | trip_updates: updated={rt_updated}, total={rt_total}"
    )

    producer.flush()

    first_poll = False


def main():
    while True:
        poll()
        time.sleep(30)


if __name__ == "__main__":
    main()
