from uuid import uuid4

from app.models import OrderCreate


orders = {}


def create_order(order: OrderCreate):
    order_id = str(uuid4())

    new_order = {
        "order_id": order_id,
        "customer_id": order.customer_id,
        "product_id": order.product_id,
        "quantity": order.quantity,
        "amount": order.amount,
        "status": "CREATED",
    }

    orders[order_id] = new_order

    return new_order


def get_order(order_id: str):
    return orders.get(order_id)


def get_all_orders():
    return list(orders.values())