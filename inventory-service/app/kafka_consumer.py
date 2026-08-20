import json
import os
import threading
import time

from confluent_kafka import Consumer

from app.database import SessionLocal
from app.inventory_service import reserve_inventory


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092",
)

TOPIC = "order-events"
GROUP_ID = "inventory-service-group"


consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
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

            db = SessionLocal()

            try:
                reservation = reserve_inventory(
                    db,
                    event["order_id"],
                    event["product_id"],
                    event["quantity"],
                )

                print(
                    f"Inventory reserved: "
                    f"{reservation.reservation_id}"
                )

                consumer.commit(message)

            finally:
                db.close()

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