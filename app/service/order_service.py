import configparser
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import enum
from app.service.microservice_config import ServiceClient

config = configparser.ConfigParser()
config.read('config.ini')

order_service = ServiceClient(config['services']['order'])

order_router = APIRouter()

class OrderStatus(enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    user_id: str
    store_id: str
    total_amount: float
    shipping_address: str
    billing_address: str
    status: Optional[str] = "PENDING"
    notes: Optional[str] = ""
    items: List[OrderItem]

@order_router.get("/orders", response_model=List[dict])
async def get_orders(
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None
):
    params = {"skip": skip, "limit": limit}
    if status:
        params["status"] = status
    
    try:
        orders = await order_service.get("orders", params=params)
        return orders
    except HTTPException as e:
        raise e

@order_router.get("/orders/{order_id}", response_model=dict)
async def get_order(order_id: str):
    try:
        order = await order_service.get(f"orders/{order_id}")
        return order
    except HTTPException as e:
        raise e

@order_router.get("/orders/{order_id}/sync", response_model=dict)
def get_order_sync(order_id: str):
    try:
        order = order_service.get_sync(f"orders/{order_id}")
        return order
    except HTTPException as e:
        raise e

@order_router.put("/orders/{order_id}", response_model=dict)
async def update_order(order_id: str, order_data: OrderCreate):
    try:
        updated_order = await order_service.put(f"orders/{order_id}", data=order_data.dict())
        return updated_order
    except HTTPException as e:
        raise e

@order_router.post("/orders", response_model=dict)
async def create_order(order_data: OrderCreate):
    try:
        new_order = await order_service.post("orders", data=order_data.dict())
        return {"message": "Order created successfully", "order_id": new_order["id"]}
    except HTTPException as e:
        raise e

@order_router.post("/update_order_status", response_model=dict)
async def update_order_status(order_id: str, status: str):
    try:
        updated_order = await order_service.patch(f"orders/{order_id}/status", data={"status": status})
        return {"message": "Order status updated successfully", "order_id": updated_order["id"], "status": updated_order["status"]}
    except HTTPException as e:
        raise e

@order_router.post("/search_orders_by_user", response_model=List[dict])
async def get_orders_by_user(user_id: str):
    try:
        orders = await order_service.get("orders/user", params={"user_id": user_id})
        return orders
    except HTTPException as e:
        raise e

if __name__ == "__main__":
    order = get_order_sync("254a696f-ce24-4d6c-a8dd-99ae712fd35a")
    print(order)