from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
import requests
from dotenv import load_dotenv
import os
from confluent_kafka import Producer
import time 
import json

load_dotenv()

realtime_url = "https://gtfsapi.translink.ca/v3/gtfsrealtime?apikey={}".format(os.getenv("API_KEY"))

kafka_config = {
	'bootstrap.servers': 'localhost:9092'
}

# This cache will store the binary data of the entity we've seen
# Key: entity.id, Value: entity.SerializeToString()
entity_cache = {}

producer = Producer(kafka_config)
KAFKA_TOPIC = 'trip-updates' # Send all entity types here

first_poll_completed = False

def poll():
    global first_poll_completed
    
    try:
        feed = gtfs_realtime_pb2.FeedMessage()
        response = requests.get(realtime_url)
        response.raise_for_status() # Check for HTTP errors
        feed.ParseFromString(response.content)
    except requests.exceptions.RequestException as e:
        print(f"HTTP Error: {e}")
        return # Skip this poll cycle
    except Exception as e:
        print(f"Feed parse error: {e}")
        return # Skip this poll cycle

    print(f"Polling feed... Found {len(feed.entity)} total entities.")
    
    new_count = 0
    updated_count = 0
    
    # Use a set to track all IDs in the *current* feed
    current_feed_ids = set()

    for entity in feed.entity:
        if not entity.id:
            continue # Ignore entities without an ID

        current_feed_ids.add(entity.id)
        entity_binary = entity.SerializeToString()

        if entity.id not in entity_cache:
            # --- 1. NEW ENTITY ---
            if first_poll_completed:
                # Only produce if it's not the first run
                producer.produce(KAFKA_TOPIC, value=entity_binary, key=entity.id)
                new_count += 1
            
            # Add to cache
            entity_cache[entity.id] = entity_binary

        elif entity_cache[entity.id] != entity_binary:
            # --- 2. UPDATED ENTITY ---
            # The ID is in our cache, but the data is different
            producer.produce(KAFKA_TOPIC, value=entity_binary, key=entity.id)
            entity_cache[entity.id] = entity_binary # Update cache
            updated_count += 1
            
        # else: Entity is in cache and unchanged, do nothing.

    # --- 3. DELETED ENTITIES ---
    # Find IDs in our cache that were NOT in the new feed
    if first_poll_completed:
        stale_ids = set(entity_cache.keys()) - current_feed_ids
        for stale_id in stale_ids:
            # Send a "tombstone" message (key with null value)
            # Your consumer can use this to delete the entry
            producer.produce(KAFKA_TOPIC, value=None, key=stale_id)
            del entity_cache[stale_id] # Remove from cache
            
        if stale_ids:
            print(f"Removed {len(stale_ids)} stale entities.")

    
    if first_poll_completed:
        print(f"Produced: {new_count} new, {updated_count} updated.")
    else:
        print(f"First poll complete. Cache populated with {len(entity_cache)} entities.")
        first_poll_completed = True
    
    producer.flush()

def main():
	while True:
		poll()
		time.sleep(30)

if __name__ == "__main__":
	main()
