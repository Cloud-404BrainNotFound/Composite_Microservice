from fastapi import APIRouter, HTTPException, BackgroundTasks
import httpx
import configparser
from typing import Optional
from datetime import datetime
import json
from app.config.aws_config import sqs_client, SQS_QUEUE_URL

config = configparser.ConfigParser()
config.read('config.ini')

order_router = APIRouter(prefix="/orders")
order_service_url = config['services']['order']

async def make_request(method: str, url: str, **kwargs):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json() if response.text else {}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")

def make_sync_request(method: str, url: str, **kwargs):
    with httpx.Client() as client:
        try:
            response = client.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail=str(e))
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
        
@order_router.get("")
async def get_orders_route(
    sport: Optional[str] = None,
    order_status: Optional[str] = None,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10
):
    params = {
        "sport": sport,
        "order_status": order_status,
        "skip": skip,
        "limit": limit
    }
    params = {k: v for k, v in params.items() if v is not None}
    return await make_request("GET", f"{order_service_url}/orders/", params=params)

@order_router.get("/orders/{order_id}")
async def get_order(order_id: str):
    print(f"{order_service_url}orders/{order_id}")
    return await make_request("GET", f"{order_service_url}/orders/{order_id}")

@order_router.post('/order_stringing')
async def create_order_stringing(order_data: dict):
    return await make_request("POST", f"{order_service_url}/order_stringing", json=order_data)

@order_router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    return await make_request("DELETE", f"{order_service_url}/orders/{order_id}")

@order_router.put("/orders/{order_id}")
async def update_order(order_id: str, order_data: dict):
    return await make_request("PUT", f"{order_service_url}/orders/{order_id}", json=order_data)

@order_router.post("/orders")
async def create_order(order_data: dict):
    return await make_request("POST", f"{order_service_url}/orders/", json=order_data)

@order_router.get("/orders/sync/{order_id}")
def get_order_sync(order_id: str):
    print(f"{order_service_url}/orders/{order_id}")
    return make_sync_request("GET", f"{order_service_url}/orders/{order_id}")

@order_router.post("/orders/finish/{order_id}")
async def finish_order(order_id: str, order_details: dict):
    # Prepare message for SQS
    message = {
        "event_type": "order_completed", 
        "order_id": order_id,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        # Send message to SQS
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message),
            MessageAttributes={
                'event_type': {
                    'DataType': 'String',
                    'StringValue': 'order_completed'
                }
            }
        )
        
        return {
            "message": "Order completion notification queued",
            "order_id": order_id,
            "sqs_message_id": response['MessageId']
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to queue order completion notification: {str(e)}"
        )
