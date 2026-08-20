from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class InventoryReservation(Base):
    __tablename__ = "inventory_reservations"

    reservation_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    order_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )