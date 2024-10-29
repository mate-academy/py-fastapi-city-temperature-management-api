import datetime

from fastapi import HTTPException, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from websockets.legacy import async_timeout

from temperature import utils
from weather import models
from weather.crud import get_all_cities
from dependencies import get_db


async def get_temperature_list(db: AsyncSession):
    result = await db.execute(
        select(models.Temperature)
    )
    return result.scalars()


async def get_temperatures_by_city_id(db: AsyncSession, city_id: int):
    result = await db.execute(
        select(models.Temperature).filter(models.Temperature.city_id == city_id)
    )
    temperature = result.scalars().first()

    return temperature


async def set_temperature(db: AsyncSession):
    try:
        await utils.check_service_connection()
    except HTTPException as error:
        raise error

    data_list = await utils.get_temperature(db)
    for city_name, city_data in data_list.items():
        date_time_str = city_data["current"]["last_updated"]
        date_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
        data = {
            "city_id": city_data["city_id"],
            "date_time": date_time,
            "temperature": float(city_data["current"]["temp_c"]),
        }
        temperature_obj = await get_temperatures_by_city_id(db, city_id=data["city_id"])

        if not temperature_obj:
            temperature = models.Temperature(**data)
            db.add(temperature)
            temperature_obj = temperature

        else:
            for key, value in data.items():
                setattr(temperature_obj, key, value)

        await db.commit()
        await db.refresh(temperature_obj)

    return JSONResponse(
        content={"message": "Updated successfully!"},
        status_code=status.HTTP_200_OK,
    )
