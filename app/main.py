from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.cloudwatch_logger import setup_cloudwatch_logger
from app.service.order_service import order_router
from app.dependencies.logging_middleware import logging_dependency
service_name = "composite-service"
logger = setup_cloudwatch_logger(service_name)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

app.middleware("http")(logging_dependency)
app.include_router(order_router)
