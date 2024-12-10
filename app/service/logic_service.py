import httpx
import configparser
from fastapi import APIRouter, HTTPException, Depends
import traceback
from typing import Optional
from datetime import datetime
import json
from app.config.aws_config import sqs_client, SQS_QUEUE_URL
from app.config.jwt_config import get_current_user

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
async def get_ny_weather(current_user: dict = Depends(get_current_user)):
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
    limit: Optional[int] = 10,
    current_user: dict = Depends(get_current_user)
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
async def get_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    print(f"{order_service_url}orders/{order_id}")
    return await make_request("GET", f"{order_service_url}/orders/{order_id}")

@logic_router.post('/order_stringing')
async def create_order_stringing(
    order_data: dict,
    current_user: dict = Depends(get_current_user)
):
    return await make_request("POST", f"{order_service_url}/order_stringing", json=order_data)

@logic_router.delete("/orders/{order_id}")
async def delete_order(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    return await make_request("DELETE", f"{order_service_url}/orders/{order_id}")

@logic_router.put("/orders/{order_id}")
async def update_order(
    order_id: str,
    order_data: dict,
    current_user: dict = Depends(get_current_user)
):
    return await make_request("PUT", f"{order_service_url}/orders/{order_id}", json=order_data)

@logic_router.post("/orders")
async def create_order(
    order_data: dict,
    current_user: dict = Depends(get_current_user)
):
    return await make_request("POST", f"{order_service_url}/orders/", json=order_data)

@logic_router.get("/orders/sync/{order_id}")
def get_order_sync(
    order_id: str,
    current_user: dict = Depends(get_current_user)
):
    print(f"{order_service_url}/orders/{order_id}")
    return make_sync_request("GET", f"{order_service_url}/orders/{order_id}")

@logic_router.post("/orders/finish/{order_id}")
async def finish_order(
    order_id: str,
    order_details: dict,
    current_user: dict = Depends(get_current_user)
):
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

@logic_router.get("/available-options")
async def get_available_options(
    
):
    """Get available options for stringing orders"""
    available_options = {
        "sports": [
            {
                "name": "Tennis",
                "rackets": [
                    {"name": "Wilson Pro Staff v13", "price": 25.00},
                    {"name": "Babolat Pure Drive", "price": 22.00},
                    {"name": "Head Graphene 360 Speed", "price": 24.00}
                ],
                "strings": [
                    {"name": "Luxilon ALU Power", "price": 18.00},
                    {"name": "Wilson NXT", "price": 16.00},
                    {"name": "Babolat RPM Blast", "price": 17.50}
                ]
            },
            {
                "name": "Badminton",
                "rackets": [
                    {"name": "Yonex Nanoflare 800", "price": 100.00},
                    {"name": "Li-Ning 3D Calibar 900", "price": 90.00},
                    {"name": "Victor Thruster K Falcon", "price": 85.00}
                ],
                "strings": [
                    {"name": "Yonex BG65", "price": 7.00},
                    {"name": "Yonex Exbolt 63", "price": 10.00},
                    {"name": "Li-Ning No.1", "price": 9.00}
                ]
            },
            {
                "name": "Squash",
                "rackets": [
                    {"name": "Dunlop Precision Elite", "price": 40.00},
                    {"name": "Tecnifibre Carboflex", "price": 38.00},
                    {"name": "Head Graphene 360 Speed", "price": 42.00}
                ],
                "strings": [
                    {"name": "Ashaway SuperNick XL", "price": 12.00},
                    {"name": "Tecnifibre 305", "price": 14.00},
                    {"name": "Dunlop Silk", "price": 13.50}
                ]
            }
        ],
        "price_info": {
            "base_price": 20.00,
            "same_day_pickup_extra": 5.00
        }
    }
    return available_options

@logic_router.post("/submit-order")
async def submit_order(
    order_data: dict,
    payment_data: dict,
    current_user: dict = Depends(get_current_user)
):
    """
    Submit an order with payment information
    """
    try:
        # Add payment info to extras and set status to completed
        order_data["extras"] = {
            "payment": {
                "card_number": payment_data.get("card_number"),
                "expiry_month": payment_data.get("expiry_month"),
                "expiry_year": payment_data.get("expiry_year"),
                "payment_date": datetime.now().isoformat()
            }
        }
        order_data["order_status"] = "completed"
        
        # Create the order
        created_order = await make_request(
            "POST", 
            f"{order_service_url}/orders/", 
            json=order_data
        )
        
        # Send completion notification to SQS
        await finish_order(
            order_id=created_order["id"],
            order_details={
                "payment_processed": True,
                "completion_date": datetime.now().isoformat()
            }
        )
        
        return {
            "message": "Order submitted successfully",
            "order_id": created_order["id"],
            "status": "completed"
        }
        
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to submit order: {str(e)}"
        )
