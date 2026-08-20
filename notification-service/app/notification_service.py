from uuid import uuid4

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Notification


def send_notification(
    db: Session,
    order_id: str,
    customer_id: int,
):
    existing_notification = (
        db.query(Notification)
        .filter(Notification.order_id == order_id)
        .first()
    )

    if existing_notification is not None:
        print(
            f"Notification already sent for order "
            f"{order_id}"
        )
        return existing_notification

    notification = Notification(
        notification_id=str(uuid4()),
        order_id=order_id,
        customer_id=customer_id,
        status="SENT",
    )

    print(
        f"Notification sent for order "
        f"{order_id} to customer {customer_id}"
    )

    db.add(notification)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return (
            db.query(Notification)
            .filter(Notification.order_id == order_id)
            .one()
        )

    db.refresh(notification)

    return notification
