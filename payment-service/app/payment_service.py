from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import Payment


def process_payment(
    db: Session,
    order_id: str,
    amount: float,
):
    payment = Payment(
        payment_id=str(uuid4()),
        order_id=order_id,
        amount=amount,
        status="SUCCESS",
    )

    db.add(payment)
    db.commit()
    db.refresh(payment)

    return payment