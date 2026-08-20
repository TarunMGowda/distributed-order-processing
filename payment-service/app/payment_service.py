from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Payment


def process_payment(
    db: Session,
    order_id: str,
    amount: float,
):
    existing_payment = (
        db.query(Payment)
        .filter(Payment.order_id == order_id)
        .first()
    )

    if existing_payment is not None:
        print(
            f"Payment already processed for order "
            f"{order_id}"
        )
        return existing_payment

    payment = Payment(
        payment_id=str(uuid4()),
        order_id=order_id,
        amount=amount,
        status="SUCCESS",
    )

    db.add(payment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return (
            db.query(Payment)
            .filter(Payment.order_id == order_id)
            .one()
        )

    db.refresh(payment)

    return payment
