

from app.models import OrderCreate
from app.order_service import create_order, get_order


class FakeSession:
    def __init__(self):
        self.objects = {}

    def add(self, obj):
        self.objects[obj.order_id] = obj

    def commit(self):
        pass

    def refresh(self, obj):
        pass

    def get(self, model, order_id):
        return self.objects.get(order_id)


def test_create_order():
    db = FakeSession()

    order = OrderCreate(
        customer_id=101,
        product_id=5001,
        quantity=2,
        amount=1499.99,
    )

    created_order = create_order(db, order)

    assert created_order.customer_id == 101
    assert created_order.product_id == 5001
    assert created_order.status == "CREATED"


def test_get_order():
    db = FakeSession()

    order = OrderCreate(
        customer_id=102,
        product_id=5002,
        quantity=1,
        amount=500.00,
    )

    created_order = create_order(db, order)

    fetched_order = get_order(
        db,
        created_order.order_id,
    )

    assert fetched_order is not None
    assert fetched_order.order_id == created_order.order_id