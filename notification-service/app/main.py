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
    title="Notification Service",
    description="Sends notifications from Kafka order events",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def health_check():
    return {"message": "Notification Service is running"}