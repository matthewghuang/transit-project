import time
from confluent_kafka import Consumer, KafkaError
from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
from dotenv import load_dotenv
import os
import json
import pandas as pd
from pymongo import MongoClient
import pymongo
import datetime

load_dotenv()

current_data = {}

routes = pd.read_csv(filepath_or_buffer="google_transit/routes.txt", sep=",")

MONGO_CONNECTION_STRING = f"mongodb://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASSWORD")}@localhost:27017/"

route_id_to_name = {}

# load route file and create map of route_id to name
def map_route_to_name():
	def route_name(row):
		return f"{row["route_short_name"]} {row["route_long_name"]}"
	
	global route_id_to_name
	df = pd.read_csv("google_transit/routes.txt", sep=",")
	df["route_name"] = df.apply(route_name, axis=1)
	df.drop(columns=["agency_id", "route_desc", "route_type", "route_url", "route_color", "route_text_color", "route_short_name", "route_long_name"])
	route_id_to_name = df.set_index("route_id",)["route_name"].to_dict()
 
map_route_to_name()

# def analytics():
# 	print(current_data)

def main():
	kafka_config = {
		'bootstrap.servers': 'localhost:9092',
		'group.id': 'position-consumers',
		'auto.offset.reset': 'earliest'
	}
 
	consumer = Consumer(kafka_config)
	consumer.subscribe(['position'])
 
	client = MongoClient(MONGO_CONNECTION_STRING)
	database = client["position"]
	collection = database["vehicle"]
 
	# remove old records using TTL index
	collection.create_index(keys=[("timestamp", pymongo.ASCENDING)], expireAfterSeconds=60)

	try:
		while True:
			msg = consumer.poll(1.0)

			if msg is None:
				continue
			if msg.error():
				if msg.error().code() == KafkaError._PARTITION_EOF:
					continue
				else:
					print("Error: {}".format(msg.error()))
					continue
 
			feed_entity = gtfs_realtime_pb2.FeedEntity()
 
			if (msg.value() is not None):
				feed_entity.ParseFromString(msg.value())
   
				print("Received message: {}".format(feed_entity.id))
	
				current_data[feed_entity.id] = feed_entity
   
				feed_entity_as_dict = json_format.MessageToDict(feed_entity)
				feed_entity_as_dict["_id"] = feed_entity.id
				trip = feed_entity_as_dict["vehicle"]["trip"]
				# add route_name field
				trip["route_name"] = route_id_to_name[trip["routeId"]]
				# replace timestamp
				# print(feed_entity_as_dict)
				date = datetime.datetime.fromtimestamp(float(feed_entity_as_dict["vehicle"]["timestamp"]))
				feed_entity_as_dict["timestamp"] = date
	
				print(feed_entity_as_dict)
	
				collection.replace_one({'_id': feed_entity.id}, feed_entity_as_dict, upsert=True)
	
				time.sleep(0.1)
			else:
				if feed_entity.id:
					print(feed_entity)
					print(f"Received empty message, deleting {feed_entity.id}")
					collection.delete_one({"_id": feed_entity.id})
					del current_data[feed_entity.id]
	except KeyboardInterrupt:
		pass
	finally:
		consumer.close()   

if __name__ == "__main__":
	main()