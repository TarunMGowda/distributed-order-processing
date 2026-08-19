from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import Order, OrderCreate


def create_order(db: Session, order: OrderCreate):
    order_id = str(uuid4())

    new_order = Order(
        order_id=order_id,
        customer_id=order.customer_id,
        product_id=order.product_id,
        quantity=order.quantity,
        amount=order.amount,
        status="CREATED",
    )

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order


def get_order(db: Session, order_id: str):
    return db.get(Order, order_id)


def get_all_orders(db: Session):
    return db.query(Order).all()