from app.models import OrderCreate
from app.order_service import create_order, get_order


def test_create_order():
    order = OrderCreate(
        customer_id=101,
        product_id=5001,
        quantity=2,
        amount=1499.99,
    )

    created_order = create_order(order)

    assert created_order["customer_id"] == 101
    assert created_order["product_id"] == 5001
    assert created_order["status"] == "CREATED"


def test_get_order():
    order = OrderCreate(
        customer_id=102,
        product_id=5002,
        quantity=1,
        amount=500.00,
    )

    created_order = create_order(order)

    fetched_order = get_order(created_order["order_id"])

    assert fetched_order is not None
    assert fetched_order["order_id"] == created_order["order_id"]