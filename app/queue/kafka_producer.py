from confluent_kafka import Producer

# Kafka Producer initialization
producer = Producer({
    'bootstrap.servers': 'localhost:29092'
})

# Function to publish message to queue


def publish(topic, payload):
    producer.produce(topic, key=None, value=payload)
    producer.flush()
