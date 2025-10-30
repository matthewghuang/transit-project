from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
import requests
from dotenv import load_dotenv
import os
from confluent_kafka import Producer
import time 
import json

load_dotenv()

realtime_url = f"https://gtfsapi.translink.ca/v3/gtfsrealtime?apikey={os.getenv("API_KEY")}"
position_url = f"https://gtfsapi.translink.ca/v3/gtfsposition?apikey={os.getenv("API_KEY")}"

kafka_config = {
	'bootstrap.servers': 'localhost:9092'
}

# This cache will store the binary data of the entity we've seen
# Key: entity.id, Value: entity.SerializeToString()
entity_cache = {}

producer = Producer(kafka_config)
KAFKA_TOPIC = 'position' # Send all entity types here

cache = {}

first_poll = True

def poll():
	global first_poll
    
	try:
		feed = gtfs_realtime_pb2.FeedMessage()
		response = requests.get(position_url)
		response.raise_for_status() # Check for HTTP errors
		feed.ParseFromString(response.content)
	except requests.exceptions.RequestException as e:
		print(f"HTTP Error: {e}")
		return # Skip this poll cycle
	except Exception as e:
		print(f"Feed parse error: {e}")
		return # Skip this poll cycle

	seen = set()
	updated_count = 0
 
	for entity in feed.entity:
		if not entity.id:
			continue # Ignore entities without an ID

		serialized = entity.SerializeToString()
		seen.add(entity.id)

		# if first poll send everything
		if first_poll:
			producer.produce("position", key=entity.id, value=serialized)
			cache[entity.id] = serialized
		else:
			# new thing or updated
			if entity.id not in cache or cache[entity.id] != serialized:
				producer.produce("position", key=entity.id, value=serialized)
				cache[entity.id] = serialized
				updated_count = updated_count + 1
    
	print(f"updated: {updated_count}, total: {len(feed.entity)}")
    
	to_remove = [id for id in cache.keys() if id not in seen]
 
	for id in to_remove:
		print("removing", id)
		producer.produce("position", key=id, value=None)
		del cache[id]
  
	if len(to_remove) > 0:
		print(f"removed: {len(to_remove)}")
		
	producer.flush()
 
	first_poll = False

def main():
	while True:
		poll()
		time.sleep(30)

if __name__ == "__main__":
	main()
