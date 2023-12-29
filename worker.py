import stripe
from confluent_kafka import Consumer, KafkaError
import json
# from app.database.crud import create_customer

# Global API Key
stripe.api_key = "sk_test_51ORaXpSIi59A5pjv07dus87pBbIAKTvY2ohYLDfgol9" + \
    "2cKouAkVmvxCSgwkVZW9QRWsyBuX5Ahi9fpKzktz19YOZ009AGddHLA"

# Initialisation of Kafka Consumer
consumer = Consumer({
    'bootstrap.servers': 'localhost:29092',
    'group.id': 'worker',
    'auto.offset.reset': 'earliest',
    "allow.auto.create.topics": "true",
})


# Message Handeling
def message_handler(msg):
    action = msg['action']

    if action == "customer.created":
        try:
            stripe.Customer.create(
                id=msg['id'],
                name=msg['name'],
                email=msg['email']
            )
            print(f"Customer {msg['id']} created on stripe")
        except Exception as e:
            print(f"Error Occured: {str(e)}")

    elif action == "customer.updated":
        try:
            customer_data = {}
            if 'email' in msg:
                customer_data['email'] = msg['email']
            if 'name' in msg:
                customer_data['name'] = msg['name']

            stripe.Customer.modify(msg['id'],
                                   **customer_data
                                   )
            print(f"Customer {msg['id']} edited on stripe")
        except Exception as e:
            print(f"Error Occured: {str(e)}")

    elif action == "customer.deleted":
        try:
            stripe.Customer.delete(msg['id'])
            print(f"Customer {msg['id']} deleted on stripe")
        except Exception as e:
            print(f"Error Occured: {str(e)}")


# Polling Loop


# Subscribing to Stripe Topic
consumer.subscribe(['stripe'])

running = True

# Timeout for polling
timeout = 1.0

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
            print(msg.error())
    else:
        message_handler(json.loads(msg.value()))
        # print(json.loads(msg.value()))
    consumer.commit()

consumer.close()
