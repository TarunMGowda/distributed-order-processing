import json
import os
import threading
import time

from confluent_kafka import Consumer, TopicPartition

from app.database import SessionLocal
from app.payment_service import process_payment


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092",
)

TOPIC = "order-events"
GROUP_ID = "payment-service-group"
MAX_RETRIES = 3


consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
        "enable.auto.commit": False,
    }
)


def process_message(message):
    event = json.loads(
        message.value().decode("utf-8")
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(
                f"Processing payment for "
                f"order {event['order_id']} "
                f"(attempt {attempt}/{MAX_RETRIES})"
            )

            db = SessionLocal()

            try:
                payment = process_payment(
                    db,
                    event["order_id"],
                    event["amount"],
                )
            finally:
                db.close()

            print(
                f"Payment processed: "
                f"{payment.payment_id}"
            )

            return True

        except Exception as exc:
            print(
                f"Payment attempt {attempt} failed: "
                f"{exc}"
            )

            if attempt < MAX_RETRIES:
                time.sleep(attempt * 2)

    return False


def consume_orders():
    consumer.subscribe([TOPIC])

    while True:
        message = consumer.poll(1.0)

        if message is None:
            continue

        if message.error():
            print(f"Kafka error: {message.error()}")
            continue

        success = process_message(message)

        if success:
            consumer.commit(message)
            continue

        print(
            "Payment processing failed after retries. "
            "Retrying the same Kafka message."
        )

        consumer.seek(
            TopicPartition(
                message.topic(),
                message.partition(),
                message.offset(),
            )
        )

        time.sleep(2)


def start_consumer():
    thread = threading.Thread(
        target=consume_orders,
        daemon=True,
    )

    thread.start()

    return thread