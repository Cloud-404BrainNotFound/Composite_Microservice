import httpx
import configparser
from fastapi import APIRouter, HTTPException

# Read config
config = configparser.ConfigParser()
config.read('config.ini')

logic_router = APIRouter(prefix="/logic")

@logic_router.get("/weather")
async def get_ny_weather():
    """Get current weather in New York City"""
    api_key = config['openweather']['api_key']
    base_url = config['openweather']['base_url']
    city_id = config['openweather']['city_id']
    
    url = f"{base_url}/weather?id={city_id}&appid={api_key}&units=metric"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            weather_data = response.json()
            
            return {
                "temperature": weather_data["main"]["temp"],
                "humidity": weather_data["main"]["humidity"],
                "description": weather_data["weather"][0]["description"],
                "wind_speed": weather_data["wind"]["speed"]
            }
            
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail="Failed to fetch weather data from OpenWeather API"
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Internal server error: {str(e)}"
            )
