from elasticsearch import Elasticsearch
import time
from datetime import datetime
from kafka import KafkaConsumer
import os
from dotenv import load_dotenv
import json

load_dotenv() 

class Elastic:

    def __init__(self):
        self.host = parameters.elasticsearch_container_location
        self.port = parameters.elasticsearch_localhost_port
        self.es = None
        self.connect()
        self.INDEX_NAME = parameters.elasticsearch_index_name

    def connect(self):
        #self.es = Elasticsearch([{'scheme': 'https', 'host': self.host, 'port': self.port}])
        self.es = Elasticsearch(hosts=parameters.elasticsearch_container, basic_auth=(parameters.elasticsearch_username, os.environ['ELASTIC_PASSWORD']), ca_certs = parameters.http_ca_certs_location)
        
        if self.es.ping():
            print("ES connected successfully")
        else:
            print("Not connected")

    def create_index(self):
        if self.es.indices.exists(index=self.INDEX_NAME):
            print("deleting '%s' index..." % (self.INDEX_NAME))
            res = self.es.indices.delete(index=self.INDEX_NAME)
            print(" response: '%s'" % (res))
        request_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            }
        }
        print("creating '%s' index..." % (self.INDEX_NAME))
        res = self.es.indices.create(index=self.INDEX_NAME, body=request_body, ignore=400)
        print(" response: '%s'" % (res))

    def push_to_index(self, message):
        try:
            response = self.es.index(
                index=INDEX_NAME,
                #document="log",
                body=message
            )
            print("Write response is :: {}\n\n".format(response))
        except Exception as e:
            print("Exception is :: {}".format(str(e)))


if __name__ == '__main__':
    es_obj = Elastic()
    es_obj.create_index()
    consumer = KafkaConsumer(
        parameters.kafka_topic,
        bootstrap_servers=[parameters.kafka_cluster_localhost],
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset=parameters.kafka_auto_offset_reset,
        enable_auto_commit=parameters.kafka_enable_auto_commit,
        group_id=parameters.kafka_group_id
    )
    kafka_poll_count = 0
    while True:
        print(f"still on loop {kafka_poll_count}")
        sign = consumer.poll(parameters.kafka_poll_time)
        if sign != {}:
            all_topics = list(sign.values())
            for list_of_consumers in all_topics:
                for message in list_of_consumers:
                    print(message)
                    print("MESSAGE::"+str(message.value))
                    es_obj.push_to_index(message.value)
        else:
            kafka_poll_count += 1
            if kafka_poll_count == parameters.kafka_consumer_max_poll_try:
                break
            time.sleep(parameters.kafka_consuming_buffer)
            continue
