import httpx
import configparser
from fastapi import APIRouter, HTTPException
import traceback
from typing import Optional
from datetime import datetime
import json
from app.config.aws_config import sqs_client, SQS_QUEUE_URL

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

logic_router = APIRouter(prefix='/composite')
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

# Weather endpoint
@logic_router.get("/weather")
async def get_ny_weather():
    """Get current weather in New York City"""
    api_key = config['openweather']['api_key']
    city_id = config['openweather']['city_id']
    
    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}&units=metric"
    
    try:
        weather_data = await make_request("GET", url)
        return {
            "temperature": weather_data["main"]["temp"],
            "humidity": weather_data["main"]["humidity"],
            "description": weather_data["weather"][0]["description"],
            "wind_speed": weather_data["wind"]["speed"]
        }
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Order endpoints
@logic_router.get("/orders")
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

@logic_router.get("/orders/{order_id}")
async def get_order(order_id: str):
    print(f"{order_service_url}orders/{order_id}")
    return await make_request("GET", f"{order_service_url}/orders/{order_id}")

@logic_router.post('/order_stringing')
async def create_order_stringing(order_data: dict):
    return await make_request("POST", f"{order_service_url}/order_stringing", json=order_data)

@logic_router.delete("/orders/{order_id}")
async def delete_order(order_id: str):
    return await make_request("DELETE", f"{order_service_url}/orders/{order_id}")

@logic_router.put("/orders/{order_id}")
async def update_order(order_id: str, order_data: dict):
    return await make_request("PUT", f"{order_service_url}/orders/{order_id}", json=order_data)

@logic_router.post("/orders")
async def create_order(order_data: dict):
    return await make_request("POST", f"{order_service_url}/orders/", json=order_data)

@logic_router.get("/orders/sync/{order_id}")
def get_order_sync(order_id: str):
    print(f"{order_service_url}/orders/{order_id}")
    return make_sync_request("GET", f"{order_service_url}/orders/{order_id}")

@logic_router.post("/orders/finish/{order_id}")
async def finish_order(order_id: str, order_details: dict):
    message = {
        "event_type": "order_completed", 
        "order_id": order_id,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
        response = sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(message),
            MessageAttributes={
                'event_type': {
                    'DataType': 'String',
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
