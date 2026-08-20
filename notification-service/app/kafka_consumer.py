import json
import os
import threading
import time

from confluent_kafka import Consumer


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "localhost:9092",
)

TOPIC = "order-events"
GROUP_ID = "notification-service-group"


consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
)


def send_notification(event):
    print(
        f"Notification sent for order "
        f"{event['order_id']} "
        f"to customer {event['customer_id']}"
    )


def consume_orders():
    consumer.subscribe([TOPIC])

    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(f"Kafka error: {message.error()}")
            continue

        try:
            event = json.loads(
                message.value().decode("utf-8")
            )

            print(
                f"Received OrderCreated event: "
                f"{event['order_id']}"
            )

            send_notification(event)

            consumer.commit(message)

        except Exception as exc:
            print(f"Failed to process event: {exc}")
            time.sleep(2)


def start_consumer():
    thread = threading.Thread(
        target=consume_orders,
        daemon=True,
    )

    thread.start()

    return thread