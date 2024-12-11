from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.cloudwatch_logger import setup_cloudwatch_logger
from app.dependencies.logging_middleware import logging_dependency
from app.service.logic_service import logic_router

service_name = "composite-service"
logger = setup_cloudwatch_logger(service_name)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],   
    allow_headers=["*"],  
)

app.middleware("http")(logging_dependency)
app.include_router(logic_router)
