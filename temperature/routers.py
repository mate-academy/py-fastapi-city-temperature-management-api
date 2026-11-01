from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from models.temperature import DBTemperature
from models.city import DBCity
from database import get_db
from temperature import schemas, crud
from temperature.crud import get_all_temps
import os

import httpx
from dotenv import load_dotenv

load_dotenv()
YOUR_API_KEY = os.getenv("YOUR_API_KEY")

temp_router = APIRouter()


@temp_router.get("/temperatures/", response_model=list[schemas.TemperatureRead])
def temperatures_read(
    city_id: int | None = None,
    db: Session = Depends(get_db),
):
    if city_id is None:
        return get_all_temps(db)

    if db.get(DBCity, city_id) is None:
        raise HTTPException(status_code=404, detail="No such city!")

    return crud.get_temps_by_city(db, city_id)


@temp_router.post("/temperatures/update/", response_model=list[schemas.TemperatureRead])
async def temperatures_update(
    db: Session = Depends(get_db),
):
    cities = db.scalars(select(DBCity)).all()
    updated_temps = []

    async with httpx.AsyncClient() as client:
        for city in cities:
            response = await client.get(
                "https://api.weatherapi.com/v1/current.json",
                params={"key": YOUR_API_KEY, "q": city.name},
            )

            if response.status_code != 200:
                continue

            temp_cels = response.json()["current"]["temp_c"]
            create_temp = crud.create_temperature(db=db, city_id=city.id, temp=temp_cels)
            updated_temps.append(create_temp)

    return updated_temps



#SYNC version

# @temp_router.post("/temperatures/update/", response_model=list[schemas.TemperatureRead])
# def temperatures_update(
#     db: Session = Depends(get_db),
# ):
#     cities = db.scalars(select(DBCity)).all()
#     updated_temps = []
#
#     for city in cities:
#         city_id = city.id
#         city_name = city.name
#         response = requests.get(
#             f"https://api.weatherapi.com/v1/current.json?key={YOUR_API_KEY}&q={city_name}"
#         )
#         temp_cels = response.json()["current"]["temp_c"]
#
#         create_temp = crud.create_temperature(db=db, city_id=city_id, temp=temp_cels)
#         updated_temps.append(create_temp)
#
#     return updated_temps