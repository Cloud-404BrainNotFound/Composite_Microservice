from fastapi import FastAPI
from app.config.cloudwatch_logger import setup_cloudwatch_logger
from app.dependencies.logging_middleware import logging_dependency
from app.service.order_service import order_router

service_name = "order-service-8004"
logger = setup_cloudwatch_logger(service_name)

app = FastAPI()
app.middleware("http")(logging_dependency)
app.include_router(order_router)
