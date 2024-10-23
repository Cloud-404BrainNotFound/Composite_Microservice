from fastapi import FastAPI
from app.config.log import setup_logger
from app.dependecies.logging_middleware import logging_dependency
from app.service.order_service import order_router

logger = setup_logger()

app = FastAPI()

app.middleware("http")(logging_dependency)

app.include_router(order_router, prefix="/orders", tags=["orders"])
