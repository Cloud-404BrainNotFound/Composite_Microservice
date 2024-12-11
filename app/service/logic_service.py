import httpx
import configparser
from fastapi import APIRouter, HTTPException, Depends
import traceback
from typing import Optional
from datetime import datetime
import json
from app.config.aws_config import sqs_client, SQS_QUEUE_URL
from app.config.jwt_config import get_current_user
from app.dependencies.logging_middleware import get_correlation_id

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

logic_router = APIRouter(prefix='/composite')
order_service_url = config['services']['order']
review_service_url = config['services']['review']

async def make_request(method: str, url: str, **kwargs):
    # Get correlation ID from context
    correlation_id = get_correlation_id()
    
    # Add correlation ID to headers if it exists
    if correlation_id:
        headers = kwargs.get('headers', {})
        headers['x-correlation-id'] = correlation_id
        kwargs['headers'] = headers

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
    # Get correlation ID from context
    correlation_id = get_correlation_id()
    
    # Add correlation ID to headers if it exists
    if correlation_id:
        headers = kwargs.get('headers', {})
        headers['x-correlation-id'] = correlation_id
        kwargs['headers'] = headers

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
async def get_ny_weather(
    # current_user: dict = Depends(get_current_user)
    ):
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
async def get_order(
    order_id: str
):
    print(f"{order_service_url}orders/{order_id}")
    return await make_request("GET", f"{order_service_url}/orders/{order_id}")

@logic_router.post('/order_stringing')
async def create_order_stringing(
    order_data: dict
):
    return await make_request("POST", f"{order_service_url}/order_stringing", json=order_data)

@logic_router.delete("/orders/{order_id}")
async def delete_order(
    order_id: str
):
    return await make_request("DELETE", f"{order_service_url}/orders/{order_id}")

@logic_router.put("/orders/{order_id}")
async def update_order(
    order_id: str,
    order_data: dict
):
    return await make_request("PUT", f"{order_service_url}/orders/{order_id}", json=order_data)

@logic_router.post("/orders")
async def create_order(
    order_data: dict
):
    return await make_request("POST", f"{order_service_url}/orders/", json=order_data)

@logic_router.get("/orders/sync/{order_id}")
def get_order_sync(
    order_id: str
):
    print(f"{order_service_url}/orders/{order_id}")
    return make_sync_request("GET", f"{order_service_url}/orders/{order_id}")

@logic_router.post("/orders/finish")
async def finish_order(
    user_id: str,
    order_details: dict = None
):
    """Queue order completion notification with user ID"""
    message = {
        "event_type": "order_completed", 
        "user_id": user_id,
        "timestamp": datetime.now().isoformat()
    }
    
    try:
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
            "user_id": user_id,
            "sqs_message_id": response['MessageId']
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to queue order completion notification: {str(e)}"
        )

@logic_router.get("/available-options")
async def get_available_options(
    # current_user: dict = Depends(get_current_user)
):
    # print(current_user)
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


@logic_router.post("/orders/user/{user_id}")
async def create_user_order(
    user_id: str,
    order_data: dict
):
    """Create a new stringing order for a specific user and queue completion notification"""
    try:
        # Create the order
        order_response = await make_request(
            "POST", 
            f"{order_service_url}/order_stringing/user/{user_id}", 
            json=order_data
        )
        
        # Queue the completion notification
        await finish_order(user_id=user_id)
        
        return order_response
        
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create order: {str(e)}"
        )

@logic_router.get("/orders/user/{user_id}")
async def get_user_orders(
    user_id: str,
    skip: Optional[int] = 0,
    limit: Optional[int] = 10
):
    """Get all orders for a specific user"""
    params = {
        "skip": skip,
        "limit": limit
    }
    try:
        return await make_request(
            "GET",
            f"{order_service_url}/orders/user/{user_id}",
            params=params
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch user orders: {str(e)}"
        )

@logic_router.get("/orders/{order_id}")
async def get_order_details(order_id: str):
    """Get details of a specific order"""
    try:
        return await make_request(
            "GET",
            f"{order_service_url}/orders/{order_id}"
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch order details: {str(e)}"
        )

@logic_router.get("/reviews/order/{order_id}")
async def get_order_reviews(
    order_id: str
):
    """Get all reviews for a specific order"""
    try:
        return await make_request(
            "GET",
            f"{review_service_url}/reviews/target/{order_id}"
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch order reviews: {str(e)}"
        )

@logic_router.post("/reviews/order")
async def create_order_review(
    review_data: dict
):
    """Create a new review for an order
    
    Expected review_data format:
    {
        "user_id": str,
        "order_id": str,
        "rating": int,
        "content": str,
        "review_type": "service",
        "extra": dict (optional)
    }
    """
    try:
        # Prepare the review data for the review service
        review_request = {
            "user_id": review_data["user_id"],
            "review_type": "service",  # Fixed as service type for orders
            "target_id": review_data["order_id"],
            "rating": review_data["rating"],
            "content": review_data.get("content", ""),
            "extra": review_data.get("extra", {})
        }
        
        return await make_request(
            "POST",
            f"{review_service_url}/reviews",
            json=review_request
        )
    except Exception as e:
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create review: {str(e)}"
        )


