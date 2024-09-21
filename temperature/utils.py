import httpx
from datetime import datetime
from fastapi import HTTPException
from settings import settings
from city import models


async def get_temperature_data(city: models.City):
    url = f"http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={city.name.lower()}&aqi=no"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
        except httpx.HTTPError as e:
            raise HTTPException(
                status_code=502,
                detail=f"HTTP помилка при отриманні температури для {city.name}: {str(e)}",
            )
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Несподівана помилка при отриманні температури для {city.name}: {str(e)}",
            )

    try:
        data = response.json()
        temperature = data["current"]["temp_c"]
        date_time = datetime.strptime(data["current"]["last_updated"], "%Y-%m-%d %H:%M")
    except (ValueError, KeyError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"Помилка обробки даних температури для {city.name}: {str(e)}",
        )

    temperature_data = {
        "date_time": date_time,
        "temperature": temperature,
        "city_id": city.id,
    }
    return temperature_data
