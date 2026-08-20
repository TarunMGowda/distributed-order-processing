from uuid import uuid4

from sqlalchemy.orm import Session

from app.models import InventoryReservation


def reserve_inventory(
    db: Session,
    order_id: str,
    product_id: int,
    quantity: int,
):
    reservation = InventoryReservation(
        reservation_id=str(uuid4()),
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        status="RESERVED",
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation