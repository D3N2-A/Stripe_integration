import stripe
from confluent_kafka import Consumer, KafkaError, KafkaException

# Global API Key
stripe.api_key = "sk_test_51ORaXpSIi59A5pjv07dus87pBbIAKTvY2ohYLDfgol9" + \
    "2cKouAkVmvxCSgwkVZW9QRWsyBuX5Ahi9fpKzktz19YOZ009AGddHLA"

# Initialisation of Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'worker',
    'auto.offset.reset': 'earliest'
})


# Polling Loop

# Subscribing to Stripe Topic
consumer.subscribe(['stripe'])

running = True

# Timeout for polling
timeout = 2.0

print('Started Polling')
while running:
    print(".")
    msg = consumer.poll(timeout)
    if msg is None:
        continue

    if msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # End of partition event
            print('%% %s [%d] reached end at offset %d\n' %
                  (msg.topic(), msg.partition(), msg.offset()))
        elif msg.error():
            raise KafkaException(msg.error())
    else:
        print(msg)

consumer.close()
