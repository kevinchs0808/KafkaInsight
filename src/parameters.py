month_mapping = {
    'Jan': '1',
    'Feb': '2',
    'Mar': '3',
    'Apr': '4',
    'May': '5',
    'Jun': '6',
    'Jul': '7',
    'Aug': '8',
    'Sep': '9',
    'Oct': '10',
    'Nov': '11',
    'Dec': '12'
}

status_mapping = {
    '1': 'informational',
    '2': 'Successful',
    '3': 'Redirection',
    '4': 'Client Error',
    '5': 'Server Error'
}

hour_in_minutes = 60

decimal_rounding = 1

kafka_cluster_localhost = "localhost:9093"

kafka_topic = "data_log"

kafka_production_buffer = 1

kafka_consuming_buffer = 5

kafka_poll_time = 0.1

kafka_consumer_max_poll_try = 5

log_filename = "sample_logs/apache.log"

elasticsearch_container = "https://localhost:9200"

elasticsearch_index_name = 'test-log'

elasticsearch_username = 'elastic'

http_ca_certs_location = '../certificates/http_ca.crt'

kafka_auto_offset_reset = 'earliest'

kafka_group_id='my-group'

kafka_enable_auto_commit = True