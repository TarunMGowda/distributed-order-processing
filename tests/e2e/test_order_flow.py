import json
import time
import urllib.request
import subprocess


ORDER_SERVICE_URL = "http://localhost:8000"


def get_json(url):
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read().decode())


def post_json(url, payload):
    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request) as response:
        return json.loads(response.read().decode())


def query_postgres(query):
    result = subprocess.run(
        [
            "docker",
            "exec",
            "order-postgres",
            "psql",
            "-U",
            "orders_user",
            "-d",
            "orders_db",
            "-t",
            "-A",
            "-c",
            query,
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    return result.stdout.strip()


def test_all_services_are_healthy():
    services = {
        "order": "http://localhost:8000/",
        "payment": "http://localhost:8001/",
        "inventory": "http://localhost:8002/",
        "notification": "http://localhost:8003/",
    }

    for name, url in services.items():
        response = get_json(url)

        assert "message" in response, (
            f"{name} service did not return "
            "a health response"
        )


def test_complete_order_flow():
    order = {
        "customer_id": 999,
        "product_id": 12345,
        "quantity": 2,
        "amount": 1999.00,
    }

    created_order = post_json(
        f"{ORDER_SERVICE_URL}/orders",
        order,
    )

    order_id = created_order["order_id"]

    assert created_order["status"] == "CREATED"

    # Give the Kafka consumers a little time
    # to process the event.
    time.sleep(3)

    payment_count = query_postgres(
        f"""
        SELECT COUNT(*)
        FROM payments
        WHERE order_id = '{order_id}';
        """
    )

    inventory_count = query_postgres(
        f"""
        SELECT COUNT(*)
        FROM inventory_reservations
        WHERE order_id = '{order_id}';
        """
    )

    notification_count = query_postgres(
        f"""
        SELECT COUNT(*)
        FROM notifications
        WHERE order_id = '{order_id}';
        """
    )

    assert payment_count == "1"
    assert inventory_count == "1"
    assert notification_count == "1"