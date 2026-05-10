import os
from http import HTTPStatus
from datetime import datetime

import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.temperature.models import Temperature
from app.city import crud
from app.settings import settings


load_dotenv()


async def get_temperature_list(db: AsyncSession) -> list[Temperature]:
    queryset = select(Temperature)
    temperature_list = await db.execute(queryset)

    return [temperature[0] for temperature in temperature_list]


async def get_temperature_list_by_city_id(
    db: AsyncSession,
    city_id: int
) -> list[Temperature]:
    temperature_list = await get_temperature_list(db)

    if city_id is not None:
        return [
            temp for temp in temperature_list
            if temp.city_id == city_id
        ]

    return temperature_list


async def update_temperatures(db: AsyncSession) -> None:
    city_list = await crud.get_all_cities(db)

    for city in city_list:
        response = requests.get(
            settings.WEATHER_API_URL,
            params={
                "key": os.environ.get("API_KEY") ,
                "q": city.name
            }
        )
        if response.status_code != HTTPStatus.OK:
            raise HTTPException(
                status_code=507,
                detail=(
                    "There are no any location data about city "
                    f"'{city.name}' with id {city.id}"
                )
            )

        json_data = response.json()
        queryset = insert(Temperature).values(
			date_time=datetime.now(),
			city_id=city.id,
			temperature=str(json_data["current"]["temp_c"])
		)

        await db.execute(queryset)

    await db.commit()
