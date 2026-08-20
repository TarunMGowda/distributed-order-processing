from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    notification_id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
    )

    order_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    customer_id: Mapped[int] = mapped_column(
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )