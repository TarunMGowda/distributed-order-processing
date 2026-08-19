from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Order, OrderCreate
from app.order_service import create_order, get_all_orders, get_order


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Order Service",
    description="Handles order creation and retrieval",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"message": "Order Service is running"}


@app.post("/orders")
def create_new_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
):
    return create_order(db, order)


@app.get("/orders/{order_id}")
def get_single_order(
    order_id: str,
    db: Session = Depends(get_db),
):
    order = get_order(db, order_id)

    if order is None:
        raise HTTPException(
            status_code=404,
            detail="Order not found",
        )

    return order


@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    return get_all_orders(db)