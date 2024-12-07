from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.log import setup_logger
from app.dependecies.logging_middleware import logging_dependency
from app.service.order_service import order_router

logger = setup_logger()

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
