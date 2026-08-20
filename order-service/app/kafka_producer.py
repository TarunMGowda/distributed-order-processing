import json
import os

from confluent_kafka import Producer


KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:9092",
)

ORDER_EVENTS_TOPIC = "order-events"


producer = Producer(
    {
        "bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS,
        "client.id": "order-service",
    }
)


def delivery_report(err, message):
    if err is not None:
        print(f"Kafka delivery failed: {err}")
    else:
        print(
            f"Kafka event delivered to "
            f"{message.topic()} "
            f"[{message.partition()}] "
            f"at offset {message.offset()}"
        )


def publish_order_created(order):
    event = {
        "event_type": "OrderCreated",
        "order_id": order.order_id,
        "customer_id": order.customer_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "amount": order.amount,
    }

    producer.produce(
        ORDER_EVENTS_TOPIC,
        key=order.order_id,
        value=json.dumps(event),
        callback=delivery_report,
    )

    producer.flush()