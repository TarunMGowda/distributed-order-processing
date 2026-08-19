from fastapi import FastAPI, HTTPException

from app.models import OrderCreate
from app.order_service import create_order, get_all_orders, get_order


app = FastAPI(
    title="Order Service",
    description="Handles order creation and retrieval",
    version="1.0.0",
)


@app.get("/")
def health_check():
    return {"message": "Order Service is running"}


@app.post("/orders")
def create_new_order(order: OrderCreate):
    return create_order(order)


@app.get("/orders/{order_id}")
def get_single_order(order_id: str):
    order = get_order(order_id)

    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@app.get("/orders")
def get_orders():
    return get_all_orders()