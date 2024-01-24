from kafka import KafkaProducer
import uuid
import json
import time
import random
import preprocessing
import time
import parameters


class LogParser:

    @staticmethod
    def fetch_log(file_obj):
        ''' To obtain each text line inside the file

        Args:

        Returns:

        '''
        for row in file_obj:
            yield row

    @staticmethod
    def read_log_file():
        filename = parameters.log_filename
        return open(filename, "r")

    @staticmethod
    def serialize_log(log):
        log.strip()
        get_message = log.split(" ")
        if len(get_message):
            ip_address = get_message[0]
            username = get_message[2]
            is_user = preprocessing.user_detection(get_message[2])
            datetime = preprocessing.reformat_time(get_message[3])
            timezone = preprocessing.find_timezone(get_message[4])
            operation = get_message[5][1:]
            source = get_message[6]
            network_protocol = get_message[7][:-1]
            status_code = get_message[8]
            status = preprocessing.simplify_status(status_code)
        log_dict = {
            "ip_address": ip_address,
            "username": username,
            "is_user": is_user,
            "timestamp": datetime,
            "timezone": timezone,
            "operation": operation,
            "source": source,
            "network_protocol": network_protocol,
            "status_code": status_code,
            "status": status
        }
        return log_dict



class LogProducer:

    def __init__(self):
        self.bootstrap_servers = parameters.kafka_cluster_localhost
        self.topic = parameters.kafka_topic

        self.p = KafkaProducer(
            bootstrap_servers=[self.bootstrap_servers],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def produce(self, msg):

        self.p.send(self.topic, msg)
        # self.p.flush()

    def flush(self):
        self.p.flush()


if __name__ == '__main__':
    logFile = LogParser.read_log_file()
    logFileGen = LogParser.fetch_log(logFile)
    producer = LogProducer()
    while True:
        try:
            data = next(logFileGen)
            serialized_data = LogParser.serialize_log(data)
            print("Message is :: {}".format(serialized_data))
            producer.produce(serialized_data)
            time.sleep(parameters.kafka_production_buffer)
        except StopIteration:
            producer.flush()
            exit()
        except KeyboardInterrupt:
            print("Printing last message before exiting :: {}".format(serialized_data))
            producer.flush()
            exit()

