from confluent_kafka import Consumer, KafkaError
from google.transit import gtfs_realtime_pb2
from google.protobuf import json_format
from dotenv import load_dotenv
import os

def load_token(file):
	with open(file, 'r') as f:
		return f.read().strip()

INFLUXDB2_ADMIN_USERNAME = load_token('.env.influxdb2-admin-username')
INFLUXDB2_ADMIN_PASSWORD = load_token('.env.influxdb2-admin-password')
INFLUXDB2_ADMIN_TOKEN = load_token('.env.influxdb2-admin-token')

def main():
	kafka_config = {
		'bootstrap.servers': 'localhost:9092',
		'group.id': 'trip-update-consumers',
		'auto.offset.reset': 'earliest'
	}

	consumer = Consumer(kafka_config)
	consumer.subscribe(['trip-updates'])

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
				print(feed_entity)
				print("Received message: {}".format(feed_entity.id))
			else:
				print("Received empty message")

	except KeyboardInterrupt:
		pass
	finally:
		consumer.close()   

if __name__ == "__main__":
    main()