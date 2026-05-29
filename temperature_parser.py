import httpx
from sqlalchemy.orm import Session

import models

import datetime


async def get_temperature_data(cities, db: Session):
    api_key = "c04b5109c4ab415e82a90045261404"

    async with httpx.AsyncClient() as client:
        for city in cities:
            temperature_data = await client.get(f"https://weatherapi.com/v1/current.json?key={api_key}&q={city.name}&aqi=no")

            if temperature_data.status_code == 200:
                data = temperature_data.json()
                temperature = data["current"]["temp_c"]

                temperature = models.Temperature(
                    city_id=city.id,
                    date_time=datetime.datetime.now(),
                    temperature=temperature
                )
                db.add(temperature)
                db.commit()
                db.refresh(temperature)
            else:
                return f"The temperature for {city} not found"
