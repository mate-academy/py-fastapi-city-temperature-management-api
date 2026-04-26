from fastapi import Query, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from city.crud import get_city_or_404
from city.models import City
from temperature.models import Temperature
from settings import settings
from datetime import datetime
import httpx


def get_temperatures_crud(db: Session, city_id: int = Query(default=None)):
    if city_id:
        city = get_city_or_404(db, city_id)
        return city.temperatures
    return db.scalars(select(Temperature)).all()


async def check_current_temperatures(db: Session):
    cities = db.scalars(select(City)).all()

    async with httpx.AsyncClient() as client:
        for city in cities:
            try:
                response = await client.get(
                    f"https://api.openweathermap.org/data/2.5/weather",
                    params={"q": city.name, "appid": settings.API_KEY, "units": "metric"}
                )
                response.raise_for_status()
                data = response.json()
                temp = data["main"]["temp"]
            except httpx.RequestError:
                raise HTTPException(status_code=503, detail=f"Weather service unavailable")

            except httpx.HTTPStatusError as e:
                print(f"Error for {city.name}: {e.response.status_code}")
                continue

            except KeyError:
                print(f"Unexpected response format for {city.name}")
                continue
            db_temperature = Temperature(
                city_id=city.id,
                date_time=datetime.now(),
                temperature=temp
            )
            db.add(db_temperature)
        db.commit()

    temperatures = db.scalars(select(Temperature)).all()
    return temperatures
