from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.kafka_consumer import start_consumer


Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_consumer()
    yield


app = FastAPI(
    title="Payment Service",
    description="Processes order payments from Kafka events",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def health_check():
    return {"message": "Payment Service is running"}