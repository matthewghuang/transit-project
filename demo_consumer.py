import time
from confluent_kafka import Consumer, KafkaError
from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
from dotenv import load_dotenv
import os
import json
import pandas as pd

current_data = {}

routes = pd.read_csv(filepath_or_buffer="google_transit/routes.txt", sep=",")

def analytics():
	print(current_data)

def main():
	kafka_config = {
		'bootstrap.servers': 'localhost:9092',
		'group.id': 'position-consumers',
		'auto.offset.reset': 'earliest'
	}
 
	consumer = Consumer(kafka_config)
	consumer.subscribe(['position'])

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
 
			if (msg.value() is not None):
				feed_entity = gtfs_realtime_pb2.FeedEntity()
				feed_entity.ParseFromString(msg.value())
				print("Received message: {}".format(feed_entity.id))
    
				current_data[feed_entity.id] = feed_entity
    
				analytics()
    
				time.sleep(1)
			else:
				print(f"Received empty message, deleting {feed_entity.id}")
				del current_data[feed_entity.id]
	except KeyboardInterrupt:
		pass
	finally:
		consumer.close()   

if __name__ == "__main__":
    main()